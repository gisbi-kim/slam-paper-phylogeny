import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
HANDBOOK = ROOT.parent / "slam-handbook-public-release" / "main.pdf"
INPUT_JSON = DATA / "slam_handbook_references.json"
OUT_JSON = DATA / "slam_handbook_references_with_contexts.json"


CHAPTER_PAT = re.compile(
    r"^(?:"
    r"(?P<part>PART\s+[IVX]+\s+.+)|"
    r"(?P<prelude>[IVX]+\s+Prelude)|"
    r"(?P<chapter>\d{1,2}\s+[A-Z][^\n]{3,120})|"
    r"(?P<section>\d{1,2}\.\d+(?:\.\d+)?\s+[A-Z][^\n]{3,140})"
    r")\s*$"
)


def pdf_text() -> str:
    return subprocess.check_output(
        ["pdftotext", "-layout", str(HANDBOOK), "-"],
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def main_body(text: str) -> str:
    first_ref_matches = list(re.finditer(r"(?m)^\s*\[1\]\s+", text))
    if not first_ref_matches:
        raise RuntimeError("Could not find References [1]")
    return text[: first_ref_matches[-1].start()]


def clean(s: str) -> str:
    s = s.replace("\u00ad", "")
    s = re.sub(r"\f\s*", "\n", s)
    s = re.sub(r"-\s*\n\s*", "", s)
    s = re.sub(r"\s*\n\s*", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def heading_timeline(text: str):
    timeline = []
    current = {"part": "", "chapter": "", "section": ""}
    pos = 0
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        match = CHAPTER_PAT.match(stripped)
        if match:
            if match.group("part"):
                current["part"] = stripped
            elif match.group("prelude"):
                current["chapter"] = stripped
                current["section"] = ""
            elif match.group("chapter"):
                # Avoid page headers such as "18.5 Mapping..." handled by section branch.
                current["chapter"] = stripped
                current["section"] = ""
            elif match.group("section"):
                current["section"] = stripped
            timeline.append((pos, dict(current)))
        pos += len(line)
    return timeline


def heading_at(timeline, pos):
    lo, hi = 0, len(timeline)
    while lo < hi:
        mid = (lo + hi) // 2
        if timeline[mid][0] <= pos:
            lo = mid + 1
        else:
            hi = mid
    return timeline[lo - 1][1] if lo else {"part": "", "chapter": "", "section": ""}


def citation_ids(raw: str):
    ids = []
    for bracket in re.finditer(r"\[([0-9,\-\s]+)\]", raw):
        content = bracket.group(1)
        for token in re.split(r",", content):
            token = token.strip()
            if not token:
                continue
            if "-" in token:
                a, b = [x.strip() for x in token.split("-", 1)]
                if a.isdigit() and b.isdigit():
                    ids.extend(range(int(a), int(b) + 1))
            elif token.isdigit():
                ids.append(int(token))
    return ids


def extract_contexts(text: str, window=360, max_per_ref=8):
    body = main_body(text)
    timeline = heading_timeline(body)
    contexts = defaultdict(list)
    seen = defaultdict(set)
    for match in re.finditer(r"\[[0-9,\-\s]+\]", body):
        ids = citation_ids(match.group(0))
        if not ids:
            continue
        start = max(0, match.start() - window)
        end = min(len(body), match.end() + window)
        excerpt = clean(body[start:end])
        heading = heading_at(timeline, match.start())
        for rid in ids:
            if len(contexts[rid]) >= max_per_ref:
                continue
            key = (heading.get("chapter", ""), heading.get("section", ""), excerpt[:220])
            if key in seen[rid]:
                continue
            seen[rid].add(key)
            contexts[rid].append(
                {
                    "part": heading.get("part", ""),
                    "chapter": heading.get("chapter", ""),
                    "section": heading.get("section", ""),
                    "excerpt": excerpt,
                }
            )
    return contexts


def main():
    refs = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
    contexts = extract_contexts(pdf_text())
    enriched = []
    for ref in refs:
        updated = dict(ref)
        updated["citation_contexts"] = contexts.get(int(ref["id"]), [])
        enriched.append(updated)
    OUT_JSON.write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
    with_context = sum(1 for ref in enriched if ref["citation_contexts"])
    total_contexts = sum(len(ref["citation_contexts"]) for ref in enriched)
    print(f"refs={len(enriched)} with_context={with_context} total_contexts={total_contexts}")


if __name__ == "__main__":
    main()
