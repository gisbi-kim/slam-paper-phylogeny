import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data"


def md_escape(value):
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def path_text(path):
    return " > ".join(
        part
        for part in [
            path.get("phylum", ""),
            path.get("class", ""),
            path.get("order", ""),
            path.get("genus", ""),
        ]
        if part
    )


def walk_leaves(node, path=None):
    path = (path or []) + [node["name"]]
    children = node.get("children") or []
    if not children:
        yield path
    for child in children:
        yield from walk_leaves(child, path)


def emit_tree(node, lines, depth=0):
    lines.append(f'{"  " * depth}- {node["name"]}')
    for child in node.get("children") or []:
        emit_tree(child, lines, depth + 1)


def write_reference_inventory(refs):
    lines = [
        "# SLAM Handbook Reference Inventory",
        "",
        "Source corpus: 1,320 references extracted from the SLAM Handbook public release.",
        "This file is an inventory for later semantic curation. Current `Primary path` and `Matched paths` are working labels in this repository, not final truth.",
        "",
        "## Summary",
        "",
        f"- References: {len(refs):,}",
        f"- References with multiple matched paths: {sum(len(r.get('matched_paths', [])) > 1 for r in refs):,}",
        f"- Total path memberships: {sum(max(1, len(r.get('matched_paths', []))) for r in refs):,}",
        "",
        "## References",
        "",
    ]

    for ref in refs:
        primary = path_text(
            {
                "phylum": ref.get("phylum"),
                "class": ref.get("class"),
                "order": ref.get("order"),
                "genus": ref.get("genus"),
            }
        )
        lines.extend(
            [
                f'### [{ref.get("id")}] {ref.get("title") or "(untitled)"}',
                "",
                f'- Year: {ref.get("year") or ""}',
                f"- Current primary path: {primary}",
                f'- Match method: {ref.get("match_method", "")}; confidence: {ref.get("confidence", "")}',
            ]
        )
        if ref.get("rationale"):
            lines.append(f'- Current rationale: {ref.get("rationale")}')

        matched = ref.get("matched_paths") or []
        if matched:
            lines.append("- Current matched paths:")
            for path in matched:
                lines.append(
                    f'  - {path.get("role", "secondary")}; confidence {path.get("confidence", "")}: {path_text(path)}'
                )
                if path.get("reason"):
                    lines.append(f'    - Reason: {path.get("reason")}')

        contexts = ref.get("citation_contexts") or []
        if contexts:
            lines.append("- Handbook citation contexts:")
            for context in contexts[:4]:
                section = context.get("section") or context.get("chapter") or ""
                excerpt = md_escape(context.get("excerpt", ""))
                if len(excerpt) > 360:
                    excerpt = excerpt[:357] + "..."
                lines.append(f"  - {section}: {excerpt}")
            if len(contexts) > 4:
                lines.append(f"  - ... {len(contexts) - 4} more contexts")
        lines.append("")

    (DOCS / "SLAM_HANDBOOK_REFERENCES_INVENTORY.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_taxonomy_leaves(taxonomy):
    leaves = list(walk_leaves(taxonomy))
    lines = [
        "# SLAM 4-Depth Taxonomy Leaf System",
        "",
        "The taxonomy is a four-depth paper classification system under root `SLAM`:",
        "",
        "`SLAM > Phylum > Class > Order > Genus`",
        "",
        "A `Genus` is the leaf-level assignment target. A single paper may belong to multiple Genus leaves when it contributes to multiple SLAM roles.",
        "",
        f'- Phyla: {len(taxonomy.get("children", []))}',
        f"- Leaf Genus nodes: {len(leaves)}",
        "",
        "## Leaf Paths",
        "",
    ]
    lines.extend(f"- {' > '.join(leaf)}" for leaf in leaves)
    lines.extend(["", "## Tree", ""])
    emit_tree(taxonomy, lines)
    (DOCS / "SLAM_4DEPTH_TAXONOMY_LEAVES.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_future_prompt(ref_count):
    prompt = f"""# Prompt: Semantic Multi-Path Assignment for SLAM Handbook References

You are a frontier-level SLAM literature curator. Your job is to assign SLAM Handbook references to the 4-depth taxonomy leaves in this repository.

## Inputs

Use these files:

- `docs/SLAM_HANDBOOK_REFERENCES_INVENTORY.md`: all {ref_count:,} extracted Handbook references, current labels, and citation context excerpts.
- `docs/SLAM_4DEPTH_TAXONOMY_LEAVES.md`: the allowed taxonomy leaves.
- `docs/SLAM_TAXONOMY.md`: human-readable taxonomy design notes.
- `data/slam_handbook_references_with_contexts.json`: full citation-context data if you need structured context.

## Output Goal

For every reference, assign one or more taxonomy leaf paths:

`SLAM > Phylum > Class > Order > Genus`

Multiple memberships are allowed and expected. A paper can be primarily a sensor-system paper while also contributing to front-end odometry, map representation, back-end optimization, evaluation, or learning.

## Required Output Schema

Return JSON records with this shape:

```json
{{
  "id": 493,
  "title": "...",
  "primary_path": ["SLAM", "...", "...", "...", "..."],
  "matched_paths": [
    {{
      "path": ["SLAM", "...", "...", "...", "..."],
      "role": "primary",
      "confidence": 0.0,
      "reason": "Why this paper belongs here."
    }},
    {{
      "path": ["SLAM", "...", "...", "...", "..."],
      "role": "secondary",
      "confidence": 0.0,
      "reason": "Why this additional membership is justified."
    }}
  ],
  "uncertainty": "Short note if the assignment is ambiguous."
}}
```

## Decision Policy

Think semantically, not by regex. Use title keywords only as weak clues. Prefer the paper's actual contribution and the Handbook citation context.

Use `primary_path` for the paper's main intellectual contribution. Use `secondary` paths for substantial additional roles.

Examples:

- A LiDAR-inertial SLAM system can be primary under `Sensor & Odometry Modalities > LiDAR SLAM > LiDAR System Families > LiDAR-Inertial SLAM`, and secondary under inertial odometry and front-end odometry if those are real contributions.
- A Gaussian Splatting SLAM paper can be primary under `Map Representations > Neural and Differentiable Maps > Gaussian Maps > 3D Gaussian Splatting`, and secondary under dense reconstruction, visual SLAM, loop closure, or dynamic maps only when the paper actually contributes those aspects.
- A Scan Context paper belongs to place recognition / loop closure even if it appears inside a LiDAR chapter.
- Dataset and benchmark papers should also be assigned to evaluation leaves, even when the dataset is sensor-specific.
- Do not add secondary paths just because a word appears in the venue name, publisher name, or generic phrase. For example, `transactions` contains `ransac` as a substring; ignore such accidental matches.

## Quality Rules

- Only use leaf paths that exist in `docs/SLAM_4DEPTH_TAXONOMY_LEAVES.md`.
- Keep duplicate memberships only when they represent different SLAM roles.
- Do not force every paper into many paths. One path is fine when the contribution is narrow.
- Prefer 1 to 3 paths for most papers; use more only for genuinely multi-role system papers.
- Flag ambiguous cases rather than inventing certainty.
- Preserve the reference ID exactly.
- If the current repository label is wrong, correct it. Current labels are hints, not ground truth.

## Review Focus

Pay special attention to these likely problem families:

- NeRF vs Gaussian Splatting vs generic neural implicit mapping.
- Wheel, leg, inertial, and other proprioceptive odometry.
- Place recognition vs full SLAM system papers.
- Sensor-specific system family vs measurement front-end contribution.
- Dataset/benchmark papers that should also participate in evaluation.
- Robustness papers where `robust` is just a generic adjective versus an actual robust estimation/failure contribution.

## Deliverable

Produce a JSON file suitable for updating `data/slam_handbook_references_semantic.json` and `data/references_semantic.js`. Include concise reasons so a human can audit the curation.
"""
    (DOCS / "FUTURE_AGENT_SEMANTIC_ASSIGNMENT_PROMPT.md").write_text(
        prompt, encoding="utf-8"
    )


def main():
    DOCS.mkdir(exist_ok=True)
    refs = json.loads((DATA / "slam_handbook_references_semantic.json").read_text(encoding="utf-8"))
    taxonomy = json.loads((DATA / "taxonomy_tree.json").read_text(encoding="utf-8"))
    write_reference_inventory(refs)
    write_taxonomy_leaves(taxonomy)
    write_future_prompt(len(refs))
    print("wrote docs/SLAM_HANDBOOK_REFERENCES_INVENTORY.md")
    print("wrote docs/SLAM_4DEPTH_TAXONOMY_LEAVES.md")
    print("wrote docs/FUTURE_AGENT_SEMANTIC_ASSIGNMENT_PROMPT.md")
    print(f"refs={len(refs)} leaves={len(list(walk_leaves(taxonomy)))}")


if __name__ == "__main__":
    main()
