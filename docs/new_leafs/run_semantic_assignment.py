#!/usr/bin/env python3
"""
SLAM Handbook Semantic Reassignment Pipeline
=============================================

Re-assigns 1,320 SLAM Handbook references to the 4-depth taxonomy with
fresh per-paper LLM judgment. Uses Anthropic API with prompt caching
(taxonomy block is cached so it's only billed once).

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python run_semantic_assignment.py \
        --inventory SLAM_HANDBOOK_REFERENCES_INVENTORY.md \
        --leaves SLAM_4DEPTH_TAXONOMY_LEAVES.md \
        --output slam_handbook_references_semantic.json \
        --model claude-sonnet-4-6   # or claude-haiku-4-5-20251001 for cheaper
        --start 1 --end 1320 \
        --concurrency 8

Outputs are appended atomically to a JSONL log so you can resume after a
crash and merge into a single JSON at the end.

Design notes:
  - System prompt holds the 204-leaf taxonomy + decision policy + few-shot
    examples and is marked cache_control:ephemeral so subsequent calls are
    ~10x cheaper on input.
  - User message is per-paper (id, title, year, citation contexts, current
    label as a hint). The LLM is told the current label may be wrong.
  - Output is structured JSON, validated against the leaf set. If the LLM
    hallucinates a path, the script logs and re-asks once.
  - Concurrency is bounded; 1,320 calls take ~10-20 minutes at concurrency 8.
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

try:
    from anthropic import AsyncAnthropic
except ImportError:
    sys.exit("pip install anthropic>=0.40.0")


# ----------------------------- Parsing ----------------------------------- #

def parse_inventory(path: Path) -> list[dict]:
    """Parse the SLAM_HANDBOOK_REFERENCES_INVENTORY.md into structured records."""
    text = path.read_text(encoding="utf-8")
    ref_re = re.compile(r"^### \[(\d+)\] (.+?)$", re.MULTILINE)
    matches = list(ref_re.finditer(text))
    refs = []
    for i, m in enumerate(matches):
        rid = int(m.group(1))
        title = m.group(2).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()

        year_m = re.search(r"^- Year: (.+?)$", body, re.MULTILINE)
        year = year_m.group(1).strip() if year_m else ""

        pp_m = re.search(r"^- Current primary path: (.+?)$", body, re.MULTILINE)
        current_primary = pp_m.group(1).strip() if pp_m else ""

        ctx_m = re.search(r"- Handbook citation contexts:\s*\n(.*?)$", body, re.DOTALL)
        contexts: list[str] = []
        if ctx_m:
            ctx_lines = re.findall(r"^\s*-\s+(.+?)$", ctx_m.group(1), re.MULTILINE)
            contexts = [c.strip() for c in ctx_lines if c.strip()]

        refs.append({
            "id": rid,
            "title": title,
            "year": year,
            "current_primary_path": current_primary,
            "contexts": contexts[:5],  # cap at 5 contexts to keep tokens low
        })
    return refs


def parse_leaves(path: Path) -> list[list[str]]:
    """Parse leaf paths into list of [SLAM, Phylum, Class, Order, Genus]."""
    leaves = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- SLAM > "):
            parts = [p.strip() for p in line[2:].split(" > ")]
            if len(parts) == 5 and parts[0] == "SLAM":
                leaves.append(parts)
    return leaves


# ----------------------------- LLM Prompt -------------------------------- #

DECISION_POLICY = """\
You are a frontier-level SLAM literature curator. Assign each SLAM Handbook
reference to one or more 4-depth taxonomy leaves under root SLAM:

  SLAM > Phylum > Class > Order > Genus

CRITICAL RULES
1. ONLY use leaf paths from the taxonomy below. Do not invent new leaves.
2. Output 1 to 3 paths per paper. One path is fine when contribution is narrow.
   Use multiple ONLY when the paper genuinely contributes to multiple SLAM roles.
3. Think semantically. Title keywords and venue strings are weak clues; rely on
   the paper's actual contribution and the Handbook citation context.
4. The "current_primary_path" provided is a noisy hint from a prior pipeline.
   Correct it freely if wrong.
5. Do NOT add a secondary path just because a word appears (e.g. "transactions"
   contains "ransac"; ignore).
6. Calibrated confidence in [0.4, 0.99]. If genuinely ambiguous, set
   uncertainty and lower confidence rather than fabricating certainty.

PRIMARY LABEL HEURISTICS
- New sensor-specific full system  -> Sensor & Odometry Modalities
- New residual/association/registration/loop module -> Measurement Front-End
- New solver/inference/robust objective/differentiable optimizer
                                    -> Back-End Optimization & Inference
- New world representation         -> Map Representations
- Benchmark/metric/runtime/deployment-> Robustness, Evaluation & Operations
- Learning is the core algorithmic novelty
                                    -> Learning, Semantics & Spatial AI
  (If learning is only a sub-component, prefer the sensor/front-end branch.)
- Foundational textbooks/historical/era pieces
                                    -> Problem & System Context
- Manifolds/Lie/observability/factor-graph theory
                                    -> State, Geometry & Probabilistic Modeling

PROBLEM FAMILIES TO BE CAREFUL WITH
- NeRF vs 3D Gaussian Splatting vs generic neural implicit map (different leaves).
- Wheel/leg/inertial/other proprioceptive odometry are distinct leaves.
- Pure place recognition vs full SLAM system: place recognition belongs to
  Measurement Front-End > Place Recognition and Loop Closure, even if cited
  inside a sensor chapter.
- Sensor-specific system family vs measurement front-end contribution: a
  system paper goes under Sensor & Odometry Modalities; a pure new front-end
  module goes under Measurement Front-End.
- Dataset/benchmark papers should also be assigned to evaluation leaves
  even when the dataset is sensor-specific.
- "Robust" papers: only use Robust Back-End leaves when the contribution is
  actual robust estimation, not a generic adjective in the title.

OUTPUT
Strict JSON only, no prose, no markdown fences. Schema:
{
  "id": <int>,
  "title": "<string>",
  "primary_path": ["SLAM", "<Phylum>", "<Class>", "<Order>", "<Genus>"],
  "matched_paths": [
    {"path": ["SLAM",...], "role": "primary",   "confidence": <float>, "reason": "<<=200 chars>"},
    {"path": ["SLAM",...], "role": "secondary", "confidence": <float>, "reason": "<<=200 chars>"}
  ],
  "uncertainty": "<short note or empty string>"
}
The primary_path MUST equal the path of the matched_paths entry with role "primary".
"""


def build_system_prompt(leaves: list[list[str]]) -> str:
    leaf_lines = "\n".join(" > ".join(p) for p in leaves)
    return (
        DECISION_POLICY
        + "\n\nALLOWED LEAF PATHS (204 total):\n"
        + leaf_lines
    )


def build_user_message(ref: dict) -> str:
    contexts_block = "\n".join(f"  - {c[:600]}" for c in ref["contexts"]) or "  (no contexts)"
    return (
        f"Reference to classify:\n"
        f"  id: {ref['id']}\n"
        f"  title: {ref['title']}\n"
        f"  year: {ref['year']}\n"
        f"  current_primary_path (HINT, may be wrong): {ref['current_primary_path']}\n"
        f"  handbook_citation_contexts:\n{contexts_block}\n\n"
        f"Return strict JSON per the schema."
    )


# ----------------------------- LLM Call ---------------------------------- #

@dataclass
class CallResult:
    id: int
    title: str
    raw: str
    parsed: dict | None
    error: str | None
    elapsed_s: float


async def call_llm(
    client: AsyncAnthropic,
    model: str,
    system_blocks: list[dict],
    ref: dict,
    leaf_set: set[tuple[str, ...]],
    max_retries: int = 2,
) -> CallResult:
    user_msg = build_user_message(ref)
    last_err = None
    raw = ""
    t0 = time.time()
    for attempt in range(max_retries + 1):
        try:
            resp = await client.messages.create(
                model=model,
                max_tokens=800,
                system=system_blocks,
                messages=[{"role": "user", "content": user_msg}],
            )
            raw = "".join(b.text for b in resp.content if hasattr(b, "text")).strip()
            # strip markdown fences if any
            cleaned = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
            obj = json.loads(cleaned)
            # validate paths
            paths = [tuple(mp["path"]) for mp in obj.get("matched_paths", [])]
            bad = [p for p in paths if p not in leaf_set]
            if bad:
                last_err = f"hallucinated paths: {bad}"
                if attempt < max_retries:
                    user_msg = (
                        build_user_message(ref)
                        + f"\n\nPREVIOUS ATTEMPT had invalid paths: {bad}\n"
                          "Fix and return ONLY valid leaf paths from the allowed list."
                    )
                    continue
            return CallResult(ref["id"], ref["title"], raw, obj, None, time.time() - t0)
        except Exception as e:  # noqa: BLE001
            last_err = f"{type(e).__name__}: {e}"
            if attempt < max_retries:
                await asyncio.sleep(1.5 * (attempt + 1))
    return CallResult(ref["id"], ref["title"], raw, None, last_err, time.time() - t0)


# ----------------------------- Driver ------------------------------------ #

async def run(args: argparse.Namespace) -> None:
    refs = parse_inventory(Path(args.inventory))
    leaves = parse_leaves(Path(args.leaves))
    leaf_set = {tuple(p) for p in leaves}
    print(f"[info] {len(refs)} refs, {len(leaves)} leaves")

    refs = [r for r in refs if args.start <= r["id"] <= args.end]
    print(f"[info] processing IDs {args.start}..{args.end}: {len(refs)} refs")

    # Resume support: skip IDs already in JSONL log
    log_path = Path(args.output).with_suffix(".jsonl")
    done_ids: set[int] = set()
    if log_path.exists() and not args.no_resume:
        for line in log_path.read_text(encoding="utf-8").splitlines():
            try:
                done_ids.add(json.loads(line)["id"])
            except Exception:  # noqa: BLE001
                pass
        print(f"[info] resume: {len(done_ids)} already done in {log_path}")
    refs = [r for r in refs if r["id"] not in done_ids]
    if not refs:
        print("[info] nothing to do")
        return

    client = AsyncAnthropic()
    sys_text = build_system_prompt(leaves)
    system_blocks = [
        {"type": "text", "text": sys_text, "cache_control": {"type": "ephemeral"}}
    ]
    sem = asyncio.Semaphore(args.concurrency)
    log_f = log_path.open("a", encoding="utf-8")
    err_log = Path(args.output).with_suffix(".errors.jsonl").open("a", encoding="utf-8")

    completed = 0
    errors = 0

    async def worker(ref: dict) -> None:
        nonlocal completed, errors
        async with sem:
            res = await call_llm(client, args.model, system_blocks, ref, leaf_set)
            if res.parsed is not None:
                log_f.write(json.dumps(res.parsed, ensure_ascii=False) + "\n")
                log_f.flush()
                completed += 1
            else:
                err_log.write(json.dumps({
                    "id": res.id, "title": res.title, "error": res.error, "raw": res.raw
                }, ensure_ascii=False) + "\n")
                err_log.flush()
                errors += 1
            if (completed + errors) % 25 == 0:
                print(f"[progress] done={completed} err={errors} t={res.elapsed_s:.1f}s id={res.id}")

    await asyncio.gather(*(worker(r) for r in refs))
    log_f.close()
    err_log.close()

    # Merge JSONL into final JSON
    out: list[dict] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except Exception:  # noqa: BLE001
            pass
    out.sort(key=lambda x: x["id"])
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[done] wrote {len(out)} records to {args.output} (errors={errors})")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--inventory", required=True)
    p.add_argument("--leaves", required=True)
    p.add_argument("--output", default="slam_handbook_references_semantic.json")
    p.add_argument("--model", default="claude-sonnet-4-6")
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--end", type=int, default=10**9)
    p.add_argument("--concurrency", type=int, default=8)
    p.add_argument("--no-resume", action="store_true")
    args = p.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
