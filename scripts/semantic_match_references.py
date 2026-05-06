import argparse
import csv
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
INPUT_JSON = DATA / "slam_handbook_references.json"
ENRICHED_JSON = DATA / "slam_handbook_references_with_contexts.json"
TAXONOMY_JSON = DATA / "taxonomy_tree.json"
OUT_JSON = DATA / "slam_handbook_references_semantic.json"
OUT_CSV = DATA / "slam_handbook_references_semantic.csv"
OUT_JS = DATA / "references_semantic.js"


SYSTEM_PROMPT = """You are classifying cited works into a SLAM research phylogeny.

Task:
- Assign each reference to exactly one primary taxonomy path.
- Use semantic contribution, not surface keyword matching.
- Prefer the path that captures the work's main technical contribution in SLAM.
- If a work is general infrastructure, textbook, benchmark, survey, or non-SLAM background, still choose the closest path and lower confidence.
- Do not invent new taxonomy labels. Use only the provided allowed paths.

Important distinctions:
- A sensor-specific full system belongs under Sensor & Odometry Modalities.
- A feature, registration, odometry, place-recognition, loop-closure, or data-association module belongs under Measurement Front-End.
- A solver, factor-graph inference method, robust objective, certifiable method, or differentiable optimizer belongs under Back-End Optimization & Inference.
- A representation of the world belongs under Map Representations.
- Observability, manifolds, Lie groups, factor-graph modeling, and uncertainty foundations belong under State, Geometry & Probabilistic Modeling.
- Deep learning is primary only when the learning method itself is the contribution; otherwise classify by the SLAM component it improves.

Return strict JSON only:
{
  "items": [
    {
      "id": 1,
      "phylum": "...",
      "class": "...",
      "order": "...",
      "genus": "(general)",
      "confidence": 0.0,
      "rationale": "short reason"
    }
  ]
}
"""


def leaf_paths(tree):
    paths = []

    def walk(node, path):
        new_path = path + [node["name"]]
        children = node.get("children") or []
        if not children and len(new_path) >= 4:
            paths.append(new_path[1:4])
            return
        for child in children:
            walk(child, new_path)

    walk(tree, [])
    return paths


def load_allowed_paths():
    tree = json.loads(TAXONOMY_JSON.read_text(encoding="utf-8"))
    paths = leaf_paths(tree)
    return sorted({tuple(p) for p in paths})


def compact_ref(ref):
    return {
        "id": ref["id"],
        "year": ref.get("year", ""),
        "title": ref.get("title", ""),
        "citation": ref.get("entry", "")[:900],
        "citation_contexts": [
            {
                "chapter": ctx.get("chapter", ""),
                "section": ctx.get("section", ""),
                "excerpt": ctx.get("excerpt", "")[:700],
            }
            for ctx in ref.get("citation_contexts", [])[:5]
        ],
        "rule_seed": {
            "phylum": ref.get("phylum", ""),
            "class": ref.get("class", ""),
            "order": ref.get("order", ""),
            "method": ref.get("match_method", ""),
        },
    }


def build_user_prompt(batch, allowed_paths):
    allowed = [
        {"phylum": p[0], "class": p[1], "order": p[2]}
        for p in allowed_paths
    ]
    payload = {
        "allowed_paths": allowed,
        "references": [compact_ref(r) for r in batch],
    }
    return json.dumps(payload, ensure_ascii=False)


def call_openai_responses(model, messages, base_url, api_key, temperature=0):
    url = base_url.rstrip("/") + "/v1/responses"
    body = {
        "model": model,
        "input": messages,
        "temperature": temperature,
        "text": {"format": {"type": "json_object"}},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    chunks = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in ("output_text", "text"):
                chunks.append(content.get("text", ""))
    if not chunks and "output_text" in data:
        chunks.append(data["output_text"])
    return json.loads("".join(chunks))


def write_outputs(refs):
    OUT_JSON.write_text(json.dumps(refs, ensure_ascii=False, indent=2), encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fields = [
            "id",
            "year",
            "title",
            "entry",
            "phylum",
            "class",
            "order",
            "genus",
            "match_method",
            "confidence",
            "rationale",
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for ref in refs:
            writer.writerow({k: ref.get(k, "") for k in fields})
    compact = [
        {
            k: ref.get(k, "")
            for k in [
                "id",
                "year",
                "title",
                "phylum",
                "class",
                "order",
                "genus",
                "match_method",
                "confidence",
                "rationale",
            ]
        }
        for ref in refs
    ]
    OUT_JS.write_text(
        "window.SLAM_REFERENCES_SEMANTIC = "
        + json.dumps(compact, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )


def generate_review_jsonl(refs, allowed_paths, batch_size, path):
    lines = []
    for i in range(0, len(refs), batch_size):
        batch = refs[i : i + batch_size]
        body = {
            "model": "<set-model-here>",
            "input": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(batch, allowed_paths)},
            ],
            "temperature": 0,
            "text": {"format": {"type": "json_object"}},
        }
        lines.append(
            json.dumps(
                {
                    "custom_id": f"slam-ref-semantic-{batch[0]['id']}-{batch[-1]['id']}",
                    "method": "POST",
                    "url": "/v1/responses",
                    "body": body,
                },
                ensure_ascii=False,
            )
        )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-5.5"))
    parser.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com"))
    parser.add_argument("--batch-size", type=int, default=12)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--sleep", type=float, default=0.2)
    parser.add_argument("--dry-run-jsonl", default="")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    source_json = ENRICHED_JSON if ENRICHED_JSON.exists() else INPUT_JSON
    refs = json.loads(source_json.read_text(encoding="utf-8"))
    if args.limit:
        refs = refs[: args.limit]
    allowed_paths = load_allowed_paths()

    if args.dry_run_jsonl:
        generate_review_jsonl(refs, allowed_paths, args.batch_size, args.dry_run_jsonl)
        print(f"wrote {args.dry_run_jsonl}")
        return

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set. Set it, then rerun this script.")

    done = {}
    if args.resume and OUT_JSON.exists():
        for ref in json.loads(OUT_JSON.read_text(encoding="utf-8")):
            if ref.get("match_method") == "semantic_llm":
                done[int(ref["id"])] = ref

    results = []
    for i in range(0, len(refs), args.batch_size):
        batch = refs[i : i + args.batch_size]
        pending = [ref for ref in batch if int(ref["id"]) not in done]
        if not pending:
            results.extend(done[int(ref["id"])] for ref in batch)
            continue
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(pending, allowed_paths)},
        ]
        for attempt in range(4):
            try:
                response = call_openai_responses(args.model, messages, args.base_url, api_key)
                break
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
                if attempt == 3:
                    raise
                wait = 2 ** attempt
                print(f"retry batch {pending[0]['id']}-{pending[-1]['id']} after {wait}s: {e}")
                time.sleep(wait)
        by_id = {int(item["id"]): item for item in response["items"]}
        for ref in batch:
            rid = int(ref["id"])
            if rid in done:
                results.append(done[rid])
                continue
            item = by_id[rid]
            updated = dict(ref)
            updated.update(
                {
                    "phylum": item["phylum"],
                    "class": item["class"],
                    "order": item["order"],
                    "genus": item.get("genus", "(general)") or "(general)",
                    "match_method": "semantic_llm",
                    "confidence": item.get("confidence", ""),
                    "rationale": item.get("rationale", ""),
                }
            )
            results.append(updated)
        write_outputs(results + refs[len(results) :])
        print(f"classified {min(i + args.batch_size, len(refs))}/{len(refs)}")
        time.sleep(args.sleep)

    write_outputs(results)
    print(f"wrote {OUT_JSON}, {OUT_CSV}, {OUT_JS}")


if __name__ == "__main__":
    main()
