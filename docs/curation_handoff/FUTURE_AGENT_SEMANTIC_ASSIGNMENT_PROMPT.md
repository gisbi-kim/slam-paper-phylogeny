# Prompt: Semantic Multi-Path Assignment for SLAM Handbook References

You are a frontier-level SLAM literature curator. Your job is to assign SLAM Handbook references to the 4-depth taxonomy leaves in this repository.

## Inputs

Use these files:

- `docs/SLAM_HANDBOOK_REFERENCES_INVENTORY.md`: all 1,320 extracted Handbook references, current labels, and citation context excerpts.
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
{
  "id": 493,
  "title": "...",
  "primary_path": ["SLAM", "...", "...", "...", "..."],
  "matched_paths": [
    {
      "path": ["SLAM", "...", "...", "...", "..."],
      "role": "primary",
      "confidence": 0.0,
      "reason": "Why this paper belongs here."
    },
    {
      "path": ["SLAM", "...", "...", "...", "..."],
      "role": "secondary",
      "confidence": 0.0,
      "reason": "Why this additional membership is justified."
    }
  ],
  "uncertainty": "Short note if the assignment is ambiguous."
}
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
