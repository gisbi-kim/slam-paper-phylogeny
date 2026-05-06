import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
INPUT = DATA / "slam_handbook_references_with_contexts.json"
OUT_JSON = DATA / "slam_handbook_references_semantic.json"
OUT_CSV = DATA / "slam_handbook_references_semantic.csv"
OUT_JS = DATA / "references_semantic.js"


PathTriple = tuple[str, str, str]


SECTION_MAP: list[tuple[str, PathTriple, str]] = [
    ("I.1", ("Problem & System Context", "SLAM Problem Definition", "Localization vs Mapping vs SLAM"), "Handbook prelude defines the SLAM problem."),
    ("I.2", ("Problem & System Context", "System Architecture", "Modern SLAM Pipeline"), "Handbook prelude discusses modern SLAM system architecture."),
    ("I.3", ("Problem & System Context", "System Architecture", "Autonomy Integration"), "Handbook prelude cites this in autonomy integration context."),
    ("I.4", ("Problem & System Context", "Historical and Scope Framing", "SLAM Eras"), "Handbook prelude cites this in historical/scope context."),
    ("1.1", ("State, Geometry & Probabilistic Modeling", "Factor Graph Modeling", "Graphical Model Formulation"), "Cited in factor graph formulation context."),
    ("1.2", ("State, Geometry & Probabilistic Modeling", "Factor Graph Modeling", "MAP Inference"), "Cited in MAP inference / least-squares modeling context."),
    ("1.3", ("Back-End Optimization & Inference", "Least-Squares Solvers", "Linear Least Squares"), "Cited in linear least-squares solver context."),
    ("1.4", ("Back-End Optimization & Inference", "Least-Squares Solvers", "Nonlinear Optimization"), "Cited in nonlinear optimization context."),
    ("1.5", ("Back-End Optimization & Inference", "Sparsity and Incrementality", "Variable Elimination"), "Cited in sparsity / factor graph structure context."),
    ("1.6", ("Back-End Optimization & Inference", "Sparsity and Incrementality", "Variable Elimination"), "Cited in variable elimination context."),
    ("1.7", ("Back-End Optimization & Inference", "Sparsity and Incrementality", "Incremental SLAM"), "Cited in incremental SLAM context."),
    ("2.1", ("State, Geometry & Probabilistic Modeling", "State Representations", "Lie Groups and Manifolds"), "Cited in manifold state representation context."),
    ("2.2", ("State, Geometry & Probabilistic Modeling", "State Representations", "Continuous-Time Trajectories"), "Cited in continuous-time trajectory context."),
    ("3.1", ("Measurement Front-End", "Data Association", "Ambiguity Handling"), "Cited in outlier/data-association problem context."),
    ("3.2", ("Robustness, Evaluation & Operations", "Outlier and Failure Robustness", "Front-End Robustness"), "Cited in front-end outlier rejection context."),
    ("3.3", ("Back-End Optimization & Inference", "Robust Back-End", "Outlier-Robust Optimization"), "Cited in robust back-end optimization context."),
    ("3.4", ("Back-End Optimization & Inference", "Robust Back-End", "Outlier-Robust Optimization"), "Cited in robustness chapter further-reading context."),
    ("4.", ("Back-End Optimization & Inference", "Certifiable and Differentiable Solvers", "Differentiable Optimization"), "Cited in differentiable optimization chapter."),
    ("5.1", ("Map Representations", "Dense Geometric Maps", "Range-Derived Maps"), "Cited in range sensing preliminaries for dense mapping."),
    ("5.2", ("Map Representations", "Dense Geometric Maps", "Range-Derived Maps"), "Cited in dense mapping foundations."),
    ("5.3", ("Map Representations", "Dense Geometric Maps", "Range-Derived Maps"), "Cited in map representation context."),
    ("5.4", ("Map Representations", "Dense Geometric Maps", "Dense Reconstruction"), "Cited in map construction / dense reconstruction context."),
    ("5.5", ("Map Representations", "Dense Geometric Maps", "Dense Reconstruction"), "Cited in map usage considerations."),
    ("6.1", ("Back-End Optimization & Inference", "Certifiable and Differentiable Solvers", "Certifiably Optimal SLAM"), "Cited in certifiably optimal solver context."),
    ("6.2", ("State, Geometry & Probabilistic Modeling", "Observability and Uncertainty", "Estimation Consistency"), "Cited in solution accuracy / uncertainty context."),
    ("6.3", ("Back-End Optimization & Inference", "Certifiable and Differentiable Solvers", "Certifiably Optimal SLAM"), "Cited in theoretical properties chapter further-reading context."),
    ("II.3", ("Robustness, Evaluation & Operations", "Evaluation", "Metrics"), "Cited in evaluation context."),
    ("7.1", ("Sensor & Odometry Modalities", "Visual SLAM", "Visual System Families"), "Cited in visual SLAM history/terminology."),
    ("7.2", ("Sensor & Odometry Modalities", "Visual SLAM", "Visual System Families"), "Cited in visual SLAM processing pipeline."),
    ("7.3", ("Measurement Front-End", "Raw-to-Pseudo Measurement Processing", "Feature Extraction"), "Cited in visual SLAM fundamentals / feature processing."),
    ("7.4", ("Back-End Optimization & Inference", "Least-Squares Solvers", "Nonlinear Optimization"), "Cited in image alignment / bundle adjustment context."),
    ("7.5", ("Sensor & Odometry Modalities", "Visual SLAM", "Visual System Families"), "Cited among full visual SLAM systems."),
    ("7.6", ("Map Representations", "Dense Geometric Maps", "Dense Reconstruction"), "Cited in real-time dense reconstruction context."),
    ("7.7", ("Sensor & Odometry Modalities", "Visual SLAM", "Camera Models and Pipelines"), "Cited in depth-camera/RGB-D SLAM context."),
    ("7.8", ("Sensor & Odometry Modalities", "Multi-Modal Fusion", "Sensor Fusion Architectures"), "Cited in visual + other modality fusion context."),
    ("7.9", ("Sensor & Odometry Modalities", "Visual SLAM", "Visual System Families"), "Cited in visual SLAM further-reading context."),
    ("8.1", ("Sensor & Odometry Modalities", "LiDAR SLAM", "LiDAR Sensing"), "Cited in LiDAR sensing preliminaries."),
    ("8.2", ("Measurement Front-End", "Odometry Front-End", "Frame-to-Frame Motion Estimation"), "Cited in LiDAR odometry context."),
    ("8.3", ("Measurement Front-End", "Place Recognition and Loop Closure", "Place Recognition"), "Cited in LiDAR place recognition context."),
    ("8.4", ("Sensor & Odometry Modalities", "LiDAR SLAM", "LiDAR System Families"), "Cited in LiDAR SLAM system context."),
    ("8.5", ("Sensor & Odometry Modalities", "LiDAR SLAM", "LiDAR System Families"), "Cited in LiDAR SLAM further-reading context."),
    ("9.1", ("Sensor & Odometry Modalities", "Radar SLAM", "Radar Sensing"), "Cited in radar sensing introduction."),
    ("9.2", ("Measurement Front-End", "Odometry Front-End", "Frame-to-Frame Motion Estimation"), "Cited in radar odometry context."),
    ("9.3", ("Measurement Front-End", "Place Recognition and Loop Closure", "Place Recognition"), "Cited in radar place recognition context."),
    ("9.4", ("Sensor & Odometry Modalities", "Radar SLAM", "Radar System Families"), "Cited in radar SLAM context."),
    ("9.5", ("Robustness, Evaluation & Operations", "Evaluation", "Datasets and Benchmarks"), "Cited in radar datasets context."),
    ("9.6", ("Sensor & Odometry Modalities", "Radar SLAM", "Radar System Families"), "Cited in radar SLAM further-reading context."),
    ("10.1", ("Sensor & Odometry Modalities", "Event-Based SLAM", "Event Sensor Processing"), "Cited in event sensor description."),
    ("10.2", ("Sensor & Odometry Modalities", "Event-Based SLAM", "Event System Families"), "Cited in event-based challenges/applications."),
    ("10.3", ("Sensor & Odometry Modalities", "Event-Based SLAM", "Event System Families"), "Cited in event-based SLAM taxonomy."),
    ("10.4", ("Measurement Front-End", "Raw-to-Pseudo Measurement Processing", "Direct Measurement Formation"), "Cited in event-based front-end context."),
    ("10.5", ("Back-End Optimization & Inference", "Least-Squares Solvers", "Nonlinear Optimization"), "Cited in event-based back-end context."),
    ("10.6", ("Sensor & Odometry Modalities", "Event-Based SLAM", "Event System Families"), "Cited in event-based SOTA systems."),
    ("10.7", ("Robustness, Evaluation & Operations", "Evaluation", "Datasets and Benchmarks"), "Cited in event datasets/simulators/benchmarks context."),
    ("10.8", ("Sensor & Odometry Modalities", "Event-Based SLAM", "Event System Families"), "Cited in event-based SLAM further-reading context."),
    ("11.1", ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Inertial Odometry"), "Cited in inertial sensing/navigation basics."),
    ("11.2", ("Measurement Front-End", "Odometry Front-End", "Preintegration and Propagation"), "Cited in IMU preintegration/factor context."),
    ("11.3", ("State, Geometry & Probabilistic Modeling", "Observability and Uncertainty", "Inertial Observability"), "Cited in aided inertial observability context."),
    ("11.4", ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Inertial Odometry"), "Cited in VIO practical context."),
    ("11.5", ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Inertial Odometry"), "Cited in inertial odometry further-reading context."),
    ("12.1", ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Leg Odometry"), "Cited in leg odometry background."),
    ("12.2", ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Leg Odometry"), "Cited in leg motion estimation context."),
    ("12.3", ("Measurement Front-End", "Odometry Front-End", "Preintegration and Propagation"), "Cited in contact estimation context."),
    ("12.4", ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Leg Odometry"), "Cited in leg odometry for state estimation."),
    ("12.5", ("Robustness, Evaluation & Operations", "Operational Constraints", "Deployment Conditions"), "Cited in leg odometry open challenges."),
    ("12.6", ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Leg Odometry"), "Cited in leg odometry further-reading context."),
    ("13.1", ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Geometry"), "Cited in deep learning for depth/camera pose."),
    ("13.2", ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Correspondence"), "Cited in deep feature matching / optical flow context."),
    ("13.3", ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Optimization"), "Cited in differentiable BA / DROID-SLAM context."),
    ("13.4", ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Geometry"), "Cited in DuSt3R context."),
    ("13.5", ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Correspondence"), "Cited in MASt3R context."),
    ("13.6", ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Optimization"), "Cited in learned SfM/SLAM extension context."),
    ("13.7", ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Geometry"), "Cited in deep SLAM further-reading context."),
    ("14.1", ("Map Representations", "Neural and Differentiable Maps", "Neural Implicit Maps"), "Cited in learnable 3D scene representation context."),
    ("14.2", ("Map Representations", "Neural and Differentiable Maps", "Neural Implicit Maps"), "Cited in NeRF/neural fields context."),
    ("14.3", ("Map Representations", "Neural and Differentiable Maps", "Gaussian Maps"), "Cited in 3D Gaussian Splatting context."),
    ("14.4", ("Map Representations", "Neural and Differentiable Maps", "Neural Implicit Maps"), "Cited in differentiable volume rendering further-reading context."),
    ("15.1", ("Map Representations", "Dynamic and Deformable Maps", "Dynamic SLAM Maps"), "Cited in dynamic SLAM problem characterization."),
    ("15.2", ("Map Representations", "Dynamic and Deformable Maps", "Dynamic SLAM Maps"), "Cited in short-term dynamic SLAM context."),
    ("15.3", ("Map Representations", "Dynamic and Deformable Maps", "Dynamic SLAM Maps"), "Cited in long-term/lifelong SLAM context."),
    ("15.4", ("Map Representations", "Dynamic and Deformable Maps", "Deformable SLAM Maps"), "Cited in deformable SLAM context."),
    ("15.5", ("Map Representations", "Dynamic and Deformable Maps", "Dynamic SLAM Maps"), "Cited in dynamic/deformable SLAM further-reading context."),
    ("16.1", ("Map Representations", "Semantic and Structured Maps", "Metric-Semantic Maps"), "Cited in traditional to metric-semantic SLAM context."),
    ("16.2", ("Map Representations", "Semantic and Structured Maps", "Metric-Semantic Maps"), "Cited in sparse metric-semantic representation context."),
    ("16.3", ("Map Representations", "Semantic and Structured Maps", "Metric-Semantic Maps"), "Cited in dense metric-semantic representation context."),
    ("16.4", ("Map Representations", "Semantic and Structured Maps", "Hierarchical Spatial Maps"), "Cited in 3D scene graph / hierarchical representation context."),
    ("16.5", ("Map Representations", "Semantic and Structured Maps", "Metric-Semantic Maps"), "Cited in metric-semantic SLAM further-reading context."),
    ("17.1", ("Learning, Semantics & Spatial AI", "Foundation and Open-World Spatial AI", "Foundation Models for Spatial AI"), "Cited in foundation model background context."),
    ("17.2", ("Learning, Semantics & Spatial AI", "Foundation and Open-World Spatial AI", "Foundation Models for Spatial AI"), "Cited in foundation models for Spatial AI context."),
    ("17.3", ("Learning, Semantics & Spatial AI", "Foundation and Open-World Spatial AI", "Open-World Mapping"), "Cited in open-world mapping context."),
    ("17.4", ("Learning, Semantics & Spatial AI", "Foundation and Open-World Spatial AI", "Open-World Mapping"), "Cited in open-world Spatial AI further-reading context."),
    ("18.1", ("Learning, Semantics & Spatial AI", "Computational Structure", "Spatial AI Graphs"), "Cited in SLAM to Spatial AI computational structure."),
    ("18.2", ("Learning, Semantics & Spatial AI", "Computational Structure", "Spatial AI Graphs"), "Cited in overall computational structure."),
    ("18.3", ("Learning, Semantics & Spatial AI", "Computational Structure", "Spatial AI Graphs"), "Cited in state estimation + ML in Spatial AI."),
    ("18.4", ("Learning, Semantics & Spatial AI", "Computational Structure", "Distributed and Hardware-Aware Computation"), "Cited in processor/sensor hardware context."),
    ("18.5", ("Learning, Semantics & Spatial AI", "Computational Structure", "Distributed and Hardware-Aware Computation"), "Cited in hardware mapping / close-to-sensor computation context."),
    ("18.6", ("Learning, Semantics & Spatial AI", "Computational Structure", "Distributed and Hardware-Aware Computation"), "Cited in Gaussian belief propagation / distributed computation context."),
    ("18.7", ("Learning, Semantics & Spatial AI", "Computational Structure", "Spatial AI Graphs"), "Cited in continual learning within factor graphs."),
    ("18.8", ("Robustness, Evaluation & Operations", "Evaluation", "Metrics"), "Cited in Spatial AI performance metrics context."),
]


TITLE_SEMANTIC_HINTS: list[tuple[tuple[str, ...], PathTriple, str]] = [
    (("place recognition", "loop closure", "loop candidates", "netvlad", "minkloc", "pointnetvlad"), ("Measurement Front-End", "Place Recognition and Loop Closure", "Place Recognition"), "Title is primarily about place recognition / loop closure."),
    (("lidar odometry", "loam", "fast-lio", "lio-sam"), ("Sensor & Odometry Modalities", "LiDAR SLAM", "LiDAR System Families"), "Title is a LiDAR odometry/SLAM system."),
    (("radar odometry", "radar slam", "radarodometry"), ("Sensor & Odometry Modalities", "Radar SLAM", "Radar System Families"), "Title is a radar odometry/SLAM system."),
    (("visual-inertial", "vio", "inertial odometry", "imu preintegration"), ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Inertial Odometry"), "Title is primarily visual-inertial/inertial odometry."),
    (("event camera", "event-based", "dynamic vision sensor"), ("Sensor & Odometry Modalities", "Event-Based SLAM", "Event System Families"), "Title is primarily event-based perception/SLAM."),
    (("factor graph", "bayes tree"), ("State, Geometry & Probabilistic Modeling", "Factor Graph Modeling", "Graphical Model Formulation"), "Title is primarily about factor graph modeling."),
    (("certifiably", "certifiable", "semidefinite", "burer-monteiro"), ("Back-End Optimization & Inference", "Certifiable and Differentiable Solvers", "Certifiably Optimal SLAM"), "Title is about certifiable or SDP-style optimization."),
    (("robust pose graph", "switchable constraints", "dynamic covariance", "outlier-robust"), ("Back-End Optimization & Inference", "Robust Back-End", "Outlier-Robust Optimization"), "Title is about robust back-end optimization."),
    (("nerf", "neural radiance", "implicit mapping", "neural field"), ("Map Representations", "Neural and Differentiable Maps", "Neural Implicit Maps"), "Title is about neural implicit map representation."),
    (("gaussian splatting", "3dgs"), ("Map Representations", "Neural and Differentiable Maps", "Gaussian Maps"), "Title is about Gaussian map representation."),
    (("scene graph", "spatial ontology"), ("Map Representations", "Semantic and Structured Maps", "Hierarchical Spatial Maps"), "Title is about hierarchical/scene-graph map representation."),
    (("semantic slam", "metric-semantic", "semantic map"), ("Map Representations", "Semantic and Structured Maps", "Metric-Semantic Maps"), "Title is about metric-semantic map representation."),
    (("dataset", "benchmark"), ("Robustness, Evaluation & Operations", "Evaluation", "Datasets and Benchmarks"), "Title is primarily a dataset/benchmark contribution."),
]


def section_key(ctx: dict) -> str:
    return ctx.get("section") or ctx.get("chapter") or ""


def path_from_context(ctx: dict):
    key = section_key(ctx)
    for prefix, path, rationale in SECTION_MAP:
        if key.startswith(prefix):
            return path, rationale, key
    return None, "", key


def path_from_title(title: str):
    low = title.lower()
    for hints, path, rationale in TITLE_SEMANTIC_HINTS:
        if any(h in low for h in hints):
            return path, rationale
    return None, ""


def choose_path(ref: dict):
    votes: Counter[PathTriple] = Counter()
    reasons: dict[PathTriple, list[str]] = {}
    sections: dict[PathTriple, list[str]] = {}
    for ctx in ref.get("citation_contexts", []):
        path, rationale, key = path_from_context(ctx)
        if path:
            votes[path] += 1
            reasons.setdefault(path, []).append(rationale)
            sections.setdefault(path, []).append(key)
    title_path, title_reason = path_from_title(ref.get("title", ""))
    if title_path:
        votes[title_path] += 2
        reasons.setdefault(title_path, []).append(title_reason)
    if votes:
        path, score = votes.most_common(1)[0]
        context_count = sum(votes.values())
        confidence = min(0.96, 0.58 + 0.08 * score + (0.08 if title_path == path else 0))
        if sections.get(path):
            rationale = f"{reasons[path][0]} Strongest Handbook context: {sections[path][0]}."
        else:
            rationale = reasons[path][0]
        return path, confidence, rationale, "codex_context_semantic"

    seed = (ref["phylum"], ref["class"], ref["order"])
    return seed, 0.42, "No reliable citation section was recovered; retained parser seed as low-confidence fallback.", "codex_context_fallback"


def write_outputs(refs):
    OUT_JSON.write_text(json.dumps(refs, ensure_ascii=False, indent=2), encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fields = ["id", "year", "title", "entry", "phylum", "class", "order", "genus", "match_method", "confidence", "rationale"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for ref in refs:
            writer.writerow({k: ref.get(k, "") for k in fields})
    compact = [
        {k: ref.get(k, "") for k in ["id", "year", "title", "phylum", "class", "order", "genus", "match_method", "confidence", "rationale"]}
        for ref in refs
    ]
    OUT_JS.write_text(
        "window.SLAM_REFERENCES_SEMANTIC = "
        + json.dumps(compact, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )


def main():
    refs = json.loads(INPUT.read_text(encoding="utf-8"))
    results = []
    for ref in refs:
        path, confidence, rationale, method = choose_path(ref)
        updated = dict(ref)
        updated.update(
            {
                "phylum": path[0],
                "class": path[1],
                "order": path[2],
                "genus": "(general)",
                "match_method": method,
                "confidence": round(confidence, 2),
                "rationale": rationale,
            }
        )
        results.append(updated)
    write_outputs(results)
    print(f"wrote semantic labels for {len(results)} references")
    print(json.dumps(Counter(r["phylum"] for r in results).most_common(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
