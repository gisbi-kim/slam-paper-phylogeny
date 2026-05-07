import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TAXONOMY_JSON = DATA / "taxonomy_tree.json"
SEMANTIC_JSON = DATA / "slam_handbook_references_semantic.json"
SEMANTIC_CSV = DATA / "slam_handbook_references_semantic.csv"
SEMANTIC_JS = DATA / "references_semantic.js"


def leaf_paths():
    taxonomy = json.loads(TAXONOMY_JSON.read_text(encoding="utf-8"))
    leaves = set()

    def walk(node, path=None):
        path = (path or []) + [node["name"]]
        children = node.get("children") or []
        if not children:
            leaves.add(tuple(path))
        for child in children:
            walk(child, path)

    walk(taxonomy)
    return leaves


def normalize_path(path):
    if len(path) != 5 or path[0] != "SLAM":
        raise ValueError(f"Expected [SLAM, Phylum, Class, Order, Genus], got {path}")
    return {
        "phylum": path[1],
        "class": path[2],
        "order": path[3],
        "genus": path[4],
    }


def import_assignment(ref, assignment):
    primary = normalize_path(assignment["primary_path"])
    matched_paths = []
    primary_seen = False
    for item in assignment.get("matched_paths", []):
        path = normalize_path(item["path"])
        role = item.get("role", "secondary")
        if role == "primary":
            primary_seen = True
        matched_paths.append(
            {
                **path,
                "role": role,
                "confidence": item.get("confidence", ""),
                "reason": item.get("reason", ""),
            }
        )
    if not primary_seen:
        matched_paths.insert(
            0,
            {
                **primary,
                "role": "primary",
                "confidence": assignment.get("confidence", ""),
                "reason": "Primary path supplied by semantic assignment.",
            },
        )

    ref.update(primary)
    ref["matched_paths"] = matched_paths
    ref["match_method"] = "llm_semantic_assignment"
    primary_conf = next(
        (p.get("confidence") for p in matched_paths if p.get("role") == "primary"),
        "",
    )
    ref["confidence"] = primary_conf
    primary_reason = next(
        (p.get("reason") for p in matched_paths if p.get("role") == "primary"),
        "",
    )
    uncertainty = assignment.get("uncertainty") or ""
    rationale = primary_reason
    if uncertainty:
        rationale = f"{rationale} Uncertainty: {uncertainty}".strip()
    ref["rationale"] = rationale
    return ref


def write_outputs(refs):
    SEMANTIC_JSON.write_text(json.dumps(refs, ensure_ascii=False, indent=2), encoding="utf-8")
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
        "matched_paths",
    ]
    with SEMANTIC_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for ref in refs:
            row = {key: ref.get(key, "") for key in fields}
            row["matched_paths"] = json.dumps(ref.get("matched_paths", []), ensure_ascii=False)
            writer.writerow(row)

    compact_fields = [
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
        "matched_paths",
    ]
    compact = [{key: ref.get(key, "") for key in compact_fields} for ref in refs]
    SEMANTIC_JS.write_text(
        "window.SLAM_REFERENCES_SEMANTIC = "
        + json.dumps(compact, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignments", required=True)
    args = parser.parse_args()

    allowed = leaf_paths()
    assignments = json.loads(Path(args.assignments).read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in assignments}
    for item in assignments:
        paths = [item["primary_path"], *[p["path"] for p in item.get("matched_paths", [])]]
        bad = [path for path in paths if tuple(path) not in allowed]
        if bad:
            raise ValueError(f"Reference {item['id']} uses paths outside taxonomy: {bad}")

    refs = json.loads(SEMANTIC_JSON.read_text(encoding="utf-8"))
    updated = 0
    for ref in refs:
        assignment = by_id.get(ref["id"])
        if assignment:
            import_assignment(ref, assignment)
            updated += 1
    write_outputs(refs)
    print(f"updated {updated} references from {args.assignments}")


if __name__ == "__main__":
    main()
