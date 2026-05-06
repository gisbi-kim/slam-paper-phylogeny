import csv
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HANDBOOK = ROOT.parent / "slam-handbook-public-release" / "main.pdf"
OUT_DIR = ROOT / "data"


TAXONOMY_RULES = [
    (
        ("Learning, Semantics & Spatial AI", "Foundation and Open-World Spatial AI", "Foundation Models for Spatial AI"),
        ["gpt", "llama", "gemini", "foundation model", "large language", "vision-language", "open-vocabulary", "open vocabulary", "clip", "language-enabled", "language enabled"],
    ),
    (
        ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Optimization"),
        ["droid-slam", "differentiable bundle", "ba-net", "deep visual slam", "learned optimization", "bundle adjustment network", "tangent space backpropagation"],
    ),
    (
        ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Correspondence"),
        ["loftr", "feature matching", "optical flow", "raft", "pwc-net", "dense matching", "detector-free", "deep patch visual odometry"],
    ),
    (
        ("Learning, Semantics & Spatial AI", "Learning for Classical SLAM Components", "Learned Geometry"),
        ["depth prediction", "monocular depth", "deepv2d", "dust3r", "mast3r", "depth and camera pose", "neural feature"],
    ),
    (
        ("Map Representations", "Neural and Differentiable Maps", "Gaussian Maps"),
        ["gaussian splat", "3dgs", "splatting"],
    ),
    (
        ("Map Representations", "Neural and Differentiable Maps", "Neural Implicit Maps"),
        ["nerf", "neural radiance", "implicit mapping", "imap", "nice-slam", "neural implicit", "radiance field", "voxel grid optimization", "implicit surface"],
    ),
    (
        ("Map Representations", "Semantic and Structured Maps", "Hierarchical Spatial Maps"),
        ["scene graph", "3d scene graph", "spatial ontology", "hierarchical metric-semantic"],
    ),
    (
        ("Map Representations", "Semantic and Structured Maps", "Metric-Semantic Maps"),
        ["semantic slam", "metric-semantic", "semantic map", "object oriented", "object-oriented", "object-level", "panoptic"],
    ),
    (
        ("Map Representations", "Dynamic and Deformable Maps", "Deformable SLAM Maps"),
        ["deformable", "non-rigid", "nonrigid", "embedded deformation", "shape manipulation"],
    ),
    (
        ("Map Representations", "Dynamic and Deformable Maps", "Dynamic SLAM Maps"),
        ["dynamic slam", "dynamic scene", "lifelong slam", "long-term dynamic", "change detection", "moving object"],
    ),
    (
        ("Map Representations", "Dense Geometric Maps", "Dense Reconstruction"),
        ["dense reconstruction", "dense geometry", "rgb-d slam", "surfel", "kinectfusion", "elasticfusion", "copyme3d", "dense 3d"],
    ),
    (
        ("Map Representations", "Dense Geometric Maps", "Range-Derived Maps"),
        ["occupancy grid", "tsdf", "esdf", "signed-distance", "signed distance", "octree", "octomap", "voxel map", "point cloud map"],
    ),
    (
        ("Map Representations", "Sparse Geometric Maps", "Pose Graph Maps"),
        ["pose graph", "pose-graph", "topological map", "submap"],
    ),
    (
        ("Back-End Optimization & Inference", "Certifiable and Differentiable Solvers", "Certifiably Optimal SLAM"),
        ["certifiably", "certifiable", "semidefinite", "se-sync", "lagrangian dual", "globally optimal"],
    ),
    (
        ("Back-End Optimization & Inference", "Certifiable and Differentiable Solvers", "Differentiable Optimization"),
        ["differentiable optimization", "implicit differentiation", "differentiating through", "convex optimization layers"],
    ),
    (
        ("Back-End Optimization & Inference", "Robust Back-End", "Outlier-Robust Optimization"),
        ["switchable constraints", "max-mixture", "dynamic covariance scaling", "robust pose graph", "robust map optimization", "incorrect data association"],
    ),
    (
        ("Back-End Optimization & Inference", "Robust Back-End", "Robust Cost Functions"),
        ["m-estimator", "robust cost", "re-weighted least squares", "ransac"],
    ),
    (
        ("Back-End Optimization & Inference", "Sparsity and Incrementality", "Incremental SLAM"),
        ["incremental smoothing", "isam", "bayes tree", "constant time visual slam", "fixed-lag"],
    ),
    (
        ("Back-End Optimization & Inference", "Sparsity and Incrementality", "Variable Elimination"),
        ["variable elimination", "sparse linear", "schur complement", "fill-in"],
    ),
    (
        ("Back-End Optimization & Inference", "Least-Squares Solvers", "Nonlinear Optimization"),
        ["nonlinear least squares", "gauss-newton", "levenberg", "ceres solver", "g2o"],
    ),
    (
        ("Back-End Optimization & Inference", "Least-Squares Solvers", "Linear Least Squares"),
        ["linear least squares", "cholesky", "qr factorization"],
    ),
    (
        ("Measurement Front-End", "Place Recognition and Loop Closure", "Place Recognition"),
        ["place recognition", "loop closure detection", "loop-closure detection", "loop detection", "visual place", "pointnetvlad", "image retrieval", "scan context"],
    ),
    (
        ("Measurement Front-End", "Place Recognition and Loop Closure", "Loop Closure Validation"),
        ["loop closure validation", "loop candidates", "trust but verify", "geometric verification"],
    ),
    (
        ("Measurement Front-End", "Data Association", "Correspondence Estimation"),
        ["data association", "correspondence", "registration", "icp", "iterative closest point", "point matching"],
    ),
    (
        ("Measurement Front-End", "Data Association", "Ambiguity Handling"),
        ["perceptual aliasing", "outlier rejection", "multi-hypothesis", "ambiguous"],
    ),
    (
        ("Measurement Front-End", "Odometry Front-End", "Preintegration and Propagation"),
        ["preintegration", "contact estimation", "kinematic chain", "strapdown", "inertial navigation"],
    ),
    (
        ("Measurement Front-End", "Odometry Front-End", "Frame-to-Frame Motion Estimation"),
        ["visual odometry", "lidar odometry", "radar odometry", "event odometry", "motion estimation", "camera tracking"],
    ),
    (
        ("Measurement Front-End", "Raw-to-Pseudo Measurement Processing", "Direct Measurement Formation"),
        ["direct visual", "photometric", "direct method", "image alignment", "event residual"],
    ),
    (
        ("Measurement Front-End", "Raw-to-Pseudo Measurement Processing", "Feature Extraction"),
        ["feature", "descriptor", "keypoint", "harris corner", "sift", "orb", "superpoint"],
    ),
    (
        ("Sensor & Odometry Modalities", "Radar SLAM", "Radar System Families"),
        ["radar slam", "radar odometry", "radarodometry", "radar localization", "uwb radar"],
    ),
    (
        ("Sensor & Odometry Modalities", "LiDAR SLAM", "LiDAR System Families"),
        ["lidar slam", "lidar odometry", "loam", "fast-lio", "lio-sam", "lidar-inertial"],
    ),
    (
        ("Sensor & Odometry Modalities", "Event-Based SLAM", "Event System Families"),
        ["event-based slam", "event camera", "dynamic vision sensor", "event-based", "neuromorphic"],
    ),
    (
        ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Inertial Odometry"),
        ["inertial odometry", "visual-inertial", "vio", "imu", "invariant extended kalman"],
    ),
    (
        ("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Leg Odometry"),
        ["leg odometry", "legged robot state estimation", "proprioceptive state estimation"],
    ),
    (
        ("Sensor & Odometry Modalities", "Visual SLAM", "Visual System Families"),
        ["visual slam", "orb-slam", "dso", "lsd-slam", "svo", "monocular slam", "stereo slam", "rgb-d slam"],
    ),
    (
        ("Sensor & Odometry Modalities", "Multi-Modal Fusion", "Calibration and Synchronization"),
        ["calibration", "extrinsic", "temporal calibration", "synchronization"],
    ),
    (
        ("Sensor & Odometry Modalities", "Multi-Modal Fusion", "Sensor Fusion Architectures"),
        ["multi-modal", "multimodal", "sensor fusion", "tightly coupled", "loosely coupled"],
    ),
    (
        ("State, Geometry & Probabilistic Modeling", "Observability and Uncertainty", "Inertial Observability"),
        ["observability", "gravity alignment", "bias observability"],
    ),
    (
        ("State, Geometry & Probabilistic Modeling", "State Representations", "Continuous-Time Trajectories"),
        ["continuous-time", "continuous time", "gaussian process trajectory", "spline"],
    ),
    (
        ("State, Geometry & Probabilistic Modeling", "State Representations", "Lie Groups and Manifolds"),
        ["lie group", "lie algebra", "manifold", "so(3)", "se(3)", "rotation group"],
    ),
    (
        ("State, Geometry & Probabilistic Modeling", "Factor Graph Modeling", "Graphical Model Formulation"),
        ["factor graph", "factor graphs", "probabilistic robotics", "bayesian"],
    ),
    (
        ("Problem & System Context", "Historical and Scope Framing", "SLAM Eras"),
        ["survey", "past present and future", "quo vadis", "history"],
    ),
    (
        ("Robustness, Evaluation & Operations", "Evaluation", "Datasets and Benchmarks"),
        ["dataset", "benchmark", "evaluation", "image matching challenge"],
    ),
    (
        ("Robustness, Evaluation & Operations", "Operational Constraints", "Real-Time Performance"),
        ["real-time", "accelerator", "embedded", "energy-efficient", "vlsi", "graphcore", "processor"],
    ),
    (
        ("Robustness, Evaluation & Operations", "Outlier and Failure Robustness", "Front-End Robustness"),
        ["introspection", "robust perception", "failure", "outlier"],
    ),
]


def pdf_text() -> str:
    return subprocess.check_output(
        ["pdftotext", "-layout", str(HANDBOOK), "-"],
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def clean(s: str) -> str:
    s = s.replace("\u00ad", "")
    s = re.sub(r"\f\s*(?:References\s+\d+|\d+\s+References)\s*", "\n", s)
    s = re.sub(r"(?<=\d)\ufffd\s*(?=\d)", "-", s)
    s = re.sub(r"\s*\ufffd\s*", " - ", s)
    s = s.replace("\ufffd", "")
    replacements = {
        "Cram - er": "Cramer",
        "Nystro - m": "Nystrom",
        "Burer - Monteiro": "Burer-Monteiro",
        "visual - inertial": "visual-inertial",
        "Visual - Inertial": "Visual-Inertial",
        "GNSS - Visual - Inertial": "GNSS-Visual-Inertial",
        "Event - Visual - Inertial": "Event-Visual-Inertial",
        "multi - modal": "multi-modal",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    s = re.sub(r"-\s*\n\s*", "", s)
    s = re.sub(r"\s*\n\s*", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def extract_title(entry: str) -> str:
    cleaned = clean(entry)
    match = re.search(r"\b(?:19|20)\d{2}[a-z]?(?:\s*\([^)]*\))?\.\s+(.+)", cleaned)
    if not match:
        return ""
    rest = match.group(1)
    stop_patterns = [
        r"\.\s+In:",
        r"\.\s+Pages\s+",
        r"\.\s+IEEE\s+",
        r"\.\s+Intl\.\s+",
        r"\.\s+International\s+",
        r"\.\s+Proc\.\s+",
        r"\.\s+Proceedings\s+",
        r"\.\s+arXiv\s+",
        r"\.\s+URL\s+",
        r"\.\s+ACM\s+",
        r"\.\s+Springer\s+",
    ]
    stops = [m.start() for p in stop_patterns if (m := re.search(p, rest))]
    if stops:
        rest = rest[: min(stops)]
    else:
        parts = rest.split(". ")
        rest = parts[0]
    return clean(rest).rstrip(".")


def infer_year(entry: str) -> str:
    match = re.search(r"\b((?:19|20)\d{2})[a-z]?", entry)
    return match.group(1) if match else ""


def classify(ref: dict) -> tuple[str, str, str, str]:
    blob = f"{ref['title']} {ref['entry']}".lower()
    for path, keywords in TAXONOMY_RULES:
        if any(k in blob for k in keywords):
            return (*path, "rule")
    return ("Problem & System Context", "Historical and Scope Framing", "SLAM Eras", "fallback")


def parse_references(text: str) -> list[dict]:
    author_matches = list(re.finditer(r"(?:\n|\f)\s*Author index\s*(?:\n|\f)", text))
    end = author_matches[-1].start() if author_matches else len(text)
    first_ref_matches = list(re.finditer(r"(?m)^\[1\]\s+", text[:end]))
    if not first_ref_matches:
        raise RuntimeError("Could not find reference [1] before Author index")
    start = first_ref_matches[-1].start()
    refs_text = text[start:end]
    refs_text = re.sub(r"\f\s*(?:References\s+\d+|\d+\s+References)\s*", "\n", refs_text)
    matches = list(re.finditer(r"(?m)^\s*\[(\d+)\]\s+", refs_text))
    refs = []
    for i, match in enumerate(matches):
        number = int(match.group(1))
        entry_start = match.end()
        entry_end = matches[i + 1].start() if i + 1 < len(matches) else len(refs_text)
        entry = clean(refs_text[entry_start:entry_end])
        title = extract_title(entry)
        year = infer_year(entry)
        phy, cls, order, method = classify({"title": title, "entry": entry})
        refs.append(
            {
                "id": number,
                "year": year,
                "title": title or "(title parse needed)",
                "entry": entry,
                "phylum": phy,
                "class": cls,
                "order": order,
                "genus": "(general)",
                "match_method": method,
            }
        )
    return refs


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    refs = parse_references(pdf_text())

    with (OUT_DIR / "slam_handbook_references.json").open("w", encoding="utf-8") as f:
        json.dump(refs, f, ensure_ascii=False, indent=2)

    with (OUT_DIR / "slam_handbook_references.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(refs[0].keys()))
        writer.writeheader()
        writer.writerows(refs)

    compact = [
        {k: r[k] for k in ["id", "year", "title", "phylum", "class", "order", "genus", "match_method"]}
        for r in refs
    ]
    with (OUT_DIR / "references.js").open("w", encoding="utf-8") as f:
        f.write("window.SLAM_REFERENCES = ")
        json.dump(compact, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")

    counts = {}
    for r in refs:
        counts[r["phylum"]] = counts.get(r["phylum"], 0) + 1
    print(f"parsed={len(refs)}")
    print(json.dumps(dict(sorted(counts.items(), key=lambda kv: -kv[1])), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
