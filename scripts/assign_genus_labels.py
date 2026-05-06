import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
from codex_context_semantic_match import path_from_context, path_from_title


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TAXONOMY_JSON = DATA / "taxonomy_tree.json"
SEMANTIC_JSON = DATA / "slam_handbook_references_semantic.json"
CONTEXT_JSON = DATA / "slam_handbook_references_with_contexts.json"
OUT_JSON = DATA / "slam_handbook_references_semantic.json"
OUT_CSV = DATA / "slam_handbook_references_semantic.csv"
OUT_JS = DATA / "references_semantic.js"


STOPWORDS = {
    "and",
    "or",
    "with",
    "for",
    "the",
    "a",
    "an",
    "of",
    "in",
    "on",
    "to",
    "based",
    "style",
    "maps",
    "map",
    "slam",
    "systems",
    "system",
    "methods",
    "models",
    "model",
}


ALIASES = {
    "Known-map Localization": ["known map", "global localization", "relocalization", "localisation", "localization"],
    "Mapping with Known Poses": ["known poses", "mapping with known", "offline mapping"],
    "Joint Localization and Mapping": ["simultaneous localization", "simultaneous localisation", "slam"],
    "Navigation Support": ["navigation", "autonomous driving", "valet parking"],
    "Manipulation Support": ["manipulation", "grasp", "hand"],
    "Exploration Support": ["exploration", "active mapping", "next best view"],
    "Long-term Spatial Memory": ["long-term", "lifelong", "spatial memory", "multi-session"],
    "Front-end / Back-end Split": ["front-end", "backend", "back-end", "pipeline"],
    "Odometry Stream": ["odometry", "tracking"],
    "Loop-Closure Stream": ["loop closure", "loop candidates"],
    "Map Update Loop": ["map update", "mapping loop"],
    "Control Loop Interface": ["control", "feedback control"],
    "Planning Loop Interface": ["planning", "planner", "motion planning"],
    "Latency and Rate Separation": ["latency", "rate", "real-time"],
    "Online Operation": ["online", "real-time", "incremental"],
    "Probabilistic Robotics Era": ["probabilistic robotics", "ekf", "particle filter"],
    "Graph Optimization Era": ["graph optimization", "pose graph", "factor graph"],
    "Robust Perception Era": ["robust perception", "outlier", "robust"],
    "Spatial AI Era": ["spatial ai", "foundation", "open-world"],
    "Variables and Factors": ["variables", "factors", "factor graph"],
    "Landmark-based Models": ["landmark", "landmarks"],
    "Pose-Graph Models": ["pose graph", "pose-graph"],
    "Hybrid Factor Graphs": ["hybrid factor", "multi-modal factor"],
    "Negative Log-Likelihood": ["negative log", "likelihood", "maximum likelihood"],
    "Least-Squares Formulation": ["least squares", "least-squares"],
    "Noise Models": ["noise model", "covariance", "uncertainty"],
    "SO(3) Rotation States": ["so(3)", "rotation", "attitude"],
    "SE(3) Pose States": ["se(3)", "pose", "rigid body"],
    "Retractions and Local Coordinates": ["retraction", "local coordinates", "manifold"],
    "Gaussian Process Trajectories": ["gaussian process", "gp trajectory"],
    "Spline Trajectories": ["spline", "b-spline", "continuous-time"],
    "Asynchronous Sensor Fusion": ["asynchronous", "time offset", "multi-rate"],
    "Gauge Freedom": ["gauge freedom", "gauge"],
    "Degeneracy": ["degeneracy", "degenerate", "rank deficient"],
    "Covariance and Marginals": ["covariance", "marginal", "marginals"],
    "Bias Observability": ["bias", "imu bias"],
    "Gravity Alignment": ["gravity", "alignment"],
    "Scale Observability": ["scale observability", "scale"],
    "Keypoints and Descriptors": ["keypoint", "descriptor", "orb", "sift", "surf", "brief"],
    "Lines and Planes": ["line", "plane", "planar"],
    "Learned Features": ["learned feature", "deep feature", "cnn feature"],
    "Photometric Residuals": ["photometric", "brightness", "direct"],
    "Range Residuals": ["range residual", "range", "point-to-plane"],
    "Event Residuals": ["event residual", "event"],
    "ICP": ["icp", "iterative closest point"],
    "Scan-to-Map Matching": ["scan-to-map", "scan to map", "ndt"],
    "Point-to-Plane Matching": ["point-to-plane", "point to plane"],
    "Visual Odometry": ["visual odometry", "vo"],
    "LiDAR Odometry": ["lidar odometry", "loam", "lio", "scan matching"],
    "Radar Odometry": ["radar odometry", "radarodometry"],
    "Event Odometry": ["event odometry"],
    "IMU Preintegration": ["imu preintegration", "preintegration"],
    "Leg Odometry Propagation": ["leg odometry", "contact"],
    "Wheel / Kinematic Propagation": ["wheel", "kinematic", "encoder"],
    "Visual Place Recognition": ["visual place", "netvlad", "image retrieval"],
    "LiDAR Place Recognition": ["lidar place", "scan context", "minkloc", "pointnetvlad"],
    "Radar Place Recognition": ["radar place"],
    "Cross-Modal Place Recognition": ["cross-modal", "cross modal"],
    "Geometric Verification": ["geometric verification", "ransac"],
    "Temporal Consistency": ["temporal consistency", "sequence"],
    "Outlier-aware Loop Closure": ["outlier", "robust loop", "false positive"],
    "Landmark Association": ["landmark association", "data association"],
    "Scan Correspondence": ["scan correspondence", "correspondence"],
    "Object Association": ["object association", "object"],
    "Perceptual Aliasing": ["perceptual aliasing", "aliasing"],
    "Incorrect Association Detection": ["incorrect association", "false association"],
    "Multi-Hypothesis Association": ["multi-hypothesis", "hypothesis"],
    "Normal Equations": ["normal equation"],
    "QR / Cholesky": ["qr", "cholesky"],
    "Sparse Linear Algebra": ["sparse linear algebra", "sparse matrix"],
    "Gauss-Newton": ["gauss-newton", "gauss newton"],
    "Levenberg-Marquardt": ["levenberg", "marquardt", "lm"],
    "Trust Region Methods": ["trust region", "dogleg"],
    "Bayes Trees": ["bayes tree", "isam2"],
    "Fill-in Reduction": ["fill-in", "ordering"],
    "Schur Complement": ["schur"],
    "iSAM-style Updates": ["isam", "incremental smoothing"],
    "Fixed-Lag Smoothing": ["fixed-lag", "fixed lag"],
    "Marginalization": ["marginalization", "marginalisation"],
    "M-estimators": ["m-estimator", "huber", "cauchy", "geman", "robust kernel"],
    "Switchable Constraints": ["switchable constraint", "switchable"],
    "Graduated Non-Convexity": ["graduated non", "gnc"],
    "Max-Mixture Models": ["max-mixture", "mixture"],
    "Pairwise Consistency": ["pairwise consistency", "pcm"],
    "Robust Pose Graph Optimization": ["robust pose graph", "pose graph optimization"],
    "Semidefinite Relaxation": ["semidefinite", "sdp"],
    "Tightness Certification": ["tightness", "certificate", "certification"],
    "SE-Sync-style Solvers": ["se-sync", "sesync"],
    "Differentiating Through Least Squares": ["differentiating through least squares", "least squares layer"],
    "Implicit Differentiation": ["implicit differentiation"],
    "Differentiation on Manifolds": ["differentiation on manifolds", "manifold"],
    "Point Landmarks": ["point landmark", "point landmarks"],
    "Line Landmarks": ["line landmark", "line landmarks"],
    "Plane Landmarks": ["plane landmark", "plane landmarks"],
    "Topological Graphs": ["topological graph", "topological"],
    "Submap Graphs": ["submap", "submaps"],
    "Multi-Session Graphs": ["multi-session", "multi session"],
    "Occupancy Grids": ["occupancy grid", "occupancy"],
    "TSDF / ESDF": ["tsdf", "esdf", "signed distance"],
    "Point Cloud Maps": ["point cloud", "pointcloud"],
    "Mesh Maps": ["mesh"],
    "Real-Time Dense Reconstruction": ["real-time dense", "realtime dense"],
    "RGB-D Reconstruction": ["rgb-d", "rgbd"],
    "Large-Scale Dense Mapping": ["large-scale dense", "large scale dense"],
    "NeRF Maps": ["nerf", "neural radiance"],
    "Neural SDF Maps": ["neural sdf", "sdf"],
    "Learned Occupancy Fields": ["learned occupancy", "occupancy field"],
    "3D Gaussian Splatting": ["3d gaussian", "gaussian splatting", "3dgs", "gaussian"],
    "Differentiable Rendering Maps": ["differentiable rendering", "rendering"],
    "Hybrid Explicit-Implicit Maps": ["hybrid explicit", "explicit-implicit", "implicit"],
    "Sparse Semantic Landmarks": ["sparse semantic", "semantic landmark"],
    "Dense Semantic Maps": ["dense semantic"],
    "Object-Level Maps": ["object-level", "object map"],
    "3D Scene Graphs": ["3d scene graph", "scene graph"],
    "Room / Place Graphs": ["room", "place graph"],
    "Open-Vocabulary Maps": ["open-vocabulary", "open vocabulary"],
    "Short-Term Dynamic Objects": ["short-term dynamic", "moving object", "dynamic object"],
    "Long-Term Lifelong Changes": ["long-term", "lifelong", "change detection"],
    "Multi-Body Scene Models": ["multi-body", "multiple body"],
    "Non-Rigid Surfaces": ["non-rigid surface", "nonrigid surface"],
    "Deformable Object Maps": ["deformable object"],
    "Elastic Scene Models": ["elastic"],
    "Monocular SLAM": ["monocular"],
    "Stereo SLAM": ["stereo"],
    "RGB-D SLAM": ["rgb-d", "rgbd"],
    "Feature-Based Visual SLAM": ["feature-based", "orb-slam", "feature based"],
    "Direct Visual SLAM": ["direct visual", "dso", "direct"],
    "Hybrid Visual SLAM": ["hybrid visual"],
    "2D LiDAR": ["2d lidar"],
    "3D Spinning LiDAR": ["spinning lidar", "3d lidar"],
    "Solid-State LiDAR": ["solid-state", "solid state"],
    "LOAM-style Odometry": ["loam"],
    "Scan-Matching SLAM": ["scan matching"],
    "LiDAR-Inertial SLAM": ["lidar-inertial", "lio", "fast-lio", "lio-sam"],
    "FMCW Radar": ["fmcw"],
    "Imaging Radar": ["imaging radar"],
    "4D Radar": ["4d radar"],
    "Radar Odometry": ["radar odometry", "radarodometry"],
    "Radar Place Recognition": ["radar place"],
    "Radar Mapping": ["radar mapping"],
    "Event Representations": ["event representation", "time surface"],
    "Event Feature Tracking": ["event feature", "feature tracking"],
    "Event Time Surfaces": ["time surface"],
    "Event Odometry": ["event odometry"],
    "Event-Inertial Odometry": ["event-inertial", "event inertial"],
    "Event-Based Mapping": ["event-based mapping", "event mapping"],
    "Strapdown Integration": ["strapdown", "inertial navigation", "imu", "mems imu", "inertial odometry"],
    "Visual-Inertial Odometry": ["visual-inertial", "vio"],
    "Contact Estimation": ["contact estimation", "contact"],
    "Kinematic Factors": ["kinematic factor", "kinematic"],
    "Legged State Estimation": ["legged state", "legged"],
    "Wheel Odometry": ["wheel odometry", "wheel-mounted", "wheelmounted", "wheel-ins", "wheel ins", "wheeled", "wheel aided", "dead reckoning"],
    "GNSS Factors": ["gnss", "gps"],
    "UWB / Radio Factors": ["uwb", "radio"],
    "Tightly Coupled Fusion": ["tightly coupled"],
    "Loosely Coupled Fusion": ["loosely coupled"],
    "Cross-Modal Factors": ["cross-modal", "cross modal"],
    "Extrinsic Calibration": ["extrinsic"],
    "Temporal Calibration": ["temporal calibration", "time offset"],
    "Online Calibration": ["online calibration"],
    "RANSAC-style Rejection": ["ransac", "magsac"],
    "Descriptor Ambiguity Handling": ["descriptor ambiguity"],
    "Dynamic Object Rejection": ["dynamic object rejection"],
    "Robust Kernels": ["robust kernel", "m-estimator"],
    "Certifiable Outlier Rejection": ["certifiable outlier", "outlier rejection"],
    "Failure Recovery": ["failure recovery"],
    "Absolute Trajectory Error": ["absolute trajectory error", "ate"],
    "Relative Pose Error": ["relative pose error", "rpe"],
    "Map Quality Metrics": ["map quality"],
    "Place Recognition Metrics": ["place recognition metric"],
    "Visual SLAM Datasets": ["visual dataset", "tum", "euroc"],
    "LiDAR SLAM Datasets": ["lidar dataset", "kitti", "newer college"],
    "Radar SLAM Datasets": ["radar dataset"],
    "Event SLAM Datasets": ["event dataset"],
    "Legged SLAM Datasets": ["legged dataset"],
    "Embedded Runtime": ["embedded", "low power"],
    "Latency Budgets": ["latency"],
    "Memory Growth Control": ["memory growth", "memory"],
    "GPS-Denied Operation": ["gps-denied", "gps denied"],
    "Large-Scale Operation": ["large-scale", "large scale"],
    "Long-Term Operation": ["long-term", "long term"],
    "Resource-Constrained Operation": ["resource-constrained", "resource constrained"],
    "Depth Prediction": ["depth prediction", "monodepth"],
    "Camera Pose Prediction": ["camera pose prediction", "pose prediction"],
    "Optical Flow": ["optical flow"],
    "Feature Matching": ["feature matching"],
    "Dense Matching": ["dense matching"],
    "Learned Place Recognition": ["learned place", "place recognition"],
    "Differentiable Bundle Adjustment": ["differentiable bundle", "bundle adjustment"],
    "DROID-SLAM-style Recurrent Updates": ["droid-slam", "recurrent"],
    "Learned Priors": ["learned prior", "priors"],
    "Vision-Language Grounding": ["vision-language", "vlm", "language grounding"],
    "Open-Vocabulary Recognition": ["open-vocabulary", "open vocabulary"],
    "Large-Scale Semantic Priors": ["semantic prior", "large-scale semantic"],
    "Open-Set Object Maps": ["open-set", "open set"],
    "Language-Grounded Maps": ["language-grounded", "language grounded"],
    "Continual Map Expansion": ["continual map", "continual"],
    "Factor-Graph Computation": ["factor graph"],
    "Scene-Graph Computation": ["scene graph"],
    "Hybrid Neural-Symbolic Graphs": ["neural-symbolic", "symbolic"],
    "Processor / Sensor Co-Design": ["processor", "co-design", "hardware"],
    "Gaussian Belief Propagation": ["gaussian belief propagation"],
    "Continual Learning in Graphs": ["continual learning"],
}


PATH_OVERRIDES = {
    813: (
        "Sensor & Odometry Modalities",
        "Proprioceptive and Aided Odometry",
        "Other Aiding Signals",
        "Wheel Odometry",
        "Wheel-mounted IMU dead reckoning is a wheel/proprioceptive aiding signal rather than a visual-inertial odometry family.",
    ),
}


ORDER_DEFAULTS = {
    "Gaussian Maps": "3D Gaussian Splatting",
    "Neural Implicit Maps": "NeRF Maps",
    "Range-Derived Maps": "Point Cloud Maps",
    "Dense Reconstruction": "Real-Time Dense Reconstruction",
    "Visual System Families": "Feature-Based Visual SLAM",
    "LiDAR System Families": "LiDAR-Inertial SLAM",
    "Radar System Families": "Radar Odometry",
    "Event System Families": "Event Odometry",
    "Inertial Odometry": "Strapdown Integration",
    "Place Recognition": "LiDAR Place Recognition",
    "Frame-to-Frame Motion Estimation": "LiDAR Odometry",
    "Robust Cost Functions": "M-estimators",
    "Outlier-Robust Optimization": "Robust Pose Graph Optimization",
    "Datasets and Benchmarks": "LiDAR SLAM Datasets",
    "Metrics": "Absolute Trajectory Error",
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def taxonomy_order_to_genus():
    tree = json.loads(TAXONOMY_JSON.read_text(encoding="utf-8"))
    out = {}
    for phylum in tree["children"]:
        for cls in phylum.get("children", []):
            for order in cls.get("children", []):
                out[(phylum["name"], cls["name"], order["name"])] = [
                    genus["name"] for genus in order.get("children", [])
                ]
    return out


def context_text(context_ref: dict) -> str:
    chunks = []
    for ctx in context_ref.get("citation_contexts", [])[:8]:
      chunks.extend([ctx.get("chapter", ""), ctx.get("section", ""), ctx.get("excerpt", "")])
    return " ".join(chunks)


def score_genus(genus: str, text: str) -> int:
    score = 0
    low = normalize(text)
    genus_low = normalize(genus)
    if genus_low in low:
        score += 20
    for alias in ALIASES.get(genus, []):
        if alias in low:
            score += 16
    tokens = [t for t in re.findall(r"[a-z0-9]+", genus_low) if t not in STOPWORDS and len(t) > 1]
    for token in tokens:
        if token in low:
            score += 3
    return score


def choose_genus(ref: dict, context_ref: dict, genus_choices: list[str]) -> tuple[str, str, int]:
    text = " ".join(
        [
            ref.get("title", ""),
            ref.get("entry", ""),
            ref.get("rationale", ""),
            context_text(context_ref),
        ]
    )
    scored = [(score_genus(genus, text), genus) for genus in genus_choices]
    scored.sort(reverse=True)
    if scored and scored[0][0] > 0:
        return scored[0][1], "codex_context_genus", scored[0][0]
    default = ORDER_DEFAULTS.get(ref.get("order", ""), genus_choices[0] if genus_choices else "(general)")
    if default not in genus_choices and genus_choices:
        default = genus_choices[0]
    return default, "codex_context_genus_default", 0


def apply_path_override(ref: dict) -> bool:
    override = PATH_OVERRIDES.get(ref.get("id"))
    if not override:
        low = normalize(" ".join([ref.get("title", ""), ref.get("entry", "")]))
        if any(
            term in low
            for term in [
                "gaussian splat",
                "3d gaussian",
                "3dgs",
                "splatam",
                "loopsplat",
                "wildgs",
                "surface gaussian",
                "surface gaussians",
                "monocular gaussian reconstruction",
            ]
        ):
            override = (
                "Map Representations",
                "Neural and Differentiable Maps",
                "Gaussian Maps",
                "3D Gaussian Splatting",
                "Gaussian splatting papers are representation papers and should live under Gaussian Maps.",
            )
        elif any(term in low for term in ["nerf", "neural radiance field", "radiance fields"]):
            override = (
                "Map Representations",
                "Neural and Differentiable Maps",
                "Neural Implicit Maps",
                "NeRF Maps",
                "NeRF and neural radiance-field papers should live under Neural Implicit Maps.",
            )
        else:
            return False
    phy, cls, order, genus, reason = override
    ref["phylum"] = phy
    ref["class"] = cls
    ref["order"] = order
    ref["genus"] = genus
    ref["match_method"] = ref.get("match_method", "codex_context_semantic")
    note = f" Path override: {reason}"
    if note not in ref.get("rationale", ""):
        ref["rationale"] = (ref.get("rationale", "") + note).strip()
    return True


def path_dict(path: tuple[str, str, str], genus: str, role: str, confidence: float, reason: str) -> dict:
    return {
        "phylum": path[0],
        "class": path[1],
        "order": path[2],
        "genus": genus,
        "role": role,
        "confidence": round(confidence, 2),
        "reason": reason,
    }


def path_key(item: dict) -> tuple[str, str, str, str]:
    return (item.get("phylum", ""), item.get("class", ""), item.get("order", ""), item.get("genus", ""))


def semantic_path_votes(ref: dict, context_ref: dict) -> list[tuple[tuple[str, str, str], float, str]]:
    votes: Counter[tuple[str, str, str]] = Counter()
    reasons: dict[tuple[str, str, str], str] = {}
    for ctx in context_ref.get("citation_contexts", [])[:8]:
        path, reason, section = path_from_context(ctx)
        if path:
            votes[path] += 1
            reasons.setdefault(path, f"{reason} Context: {section}.")

    title_path, title_reason = path_from_title(ref.get("title", ""))
    if title_path:
        votes[title_path] += 2
        reasons.setdefault(title_path, title_reason)

    out = []
    for path, count in votes.most_common():
        confidence = min(0.94, 0.48 + 0.12 * count)
        out.append((path, confidence, reasons.get(path, "Semantic citation/title context.")))
    return out


def conceptual_facets(ref: dict) -> list[tuple[tuple[str, str, str], float, str]]:
    title = normalize(ref.get("title", ""))
    entry = normalize(ref.get("entry", ""))
    text = f"{title} {entry}"
    facets: list[tuple[tuple[str, str, str], float, str]] = []

    def add(path: tuple[str, str, str], confidence: float, reason: str) -> None:
        facets.append((path, confidence, reason))

    if any(term in text for term in ["gaussian splat", "3d gaussian", "3dgs", "splatam", "loopsplat", "wildgs", "surface gaussian", "monocular gaussian reconstruction"]):
        add(("Map Representations", "Neural and Differentiable Maps", "Gaussian Maps"), 0.92, "Conceptually a Gaussian map representation, even when the paper also contributes tracking, dynamics, or semantics.")
    if any(term in text for term in ["nerf", "neural radiance field", "radiance fields", "neural field"]):
        add(("Map Representations", "Neural and Differentiable Maps", "Neural Implicit Maps"), 0.9, "Conceptually a neural implicit/radiance-field map representation.")
    if any(term in text for term in ["visual-inertial", "vio", "imu", "inertial odometry"]):
        add(("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Inertial Odometry"), 0.82, "Uses inertial/proprioceptive odometry as a system modality.")
    if any(term in text for term in ["lidar odometry", "lidar slam", "loam", "fast-lio", "lio-sam", "lidar-inertial"]):
        add(("Sensor & Odometry Modalities", "LiDAR SLAM", "LiDAR System Families"), 0.86, "Belongs to the LiDAR SLAM system family.")
        add(("Measurement Front-End", "Odometry Front-End", "Frame-to-Frame Motion Estimation"), 0.72, "Also contributes odometry/front-end motion estimation.")
    if any(term in text for term in ["radar odometry", "radarodometry", "radar slam"]):
        add(("Sensor & Odometry Modalities", "Radar SLAM", "Radar System Families"), 0.86, "Belongs to the radar SLAM system family.")
        add(("Measurement Front-End", "Odometry Front-End", "Frame-to-Frame Motion Estimation"), 0.72, "Also contributes odometry/front-end motion estimation.")
    if any(term in text for term in ["event camera", "event-based", "dynamic vision sensor", "event-inertial"]):
        add(("Sensor & Odometry Modalities", "Event-Based SLAM", "Event System Families"), 0.84, "Belongs to the event-based SLAM system family.")
    if any(term in text for term in ["place recognition", "loop closure", "loop-closure", "scan context", "netvlad", "minkloc", "pointnetvlad"]):
        add(("Measurement Front-End", "Place Recognition and Loop Closure", "Place Recognition"), 0.86, "Contributes place recognition or loop-closure candidate generation.")
    if any(term in text for term in ["dataset", "benchmark"]):
        add(("Robustness, Evaluation & Operations", "Evaluation", "Datasets and Benchmarks"), 0.88, "Dataset/benchmark papers participate in evaluation even when the data is sensor-specific.")
    robust_frontend = any(term in text for term in ["outlier rejection", "certifiable outlier", "failure recovery", "failure detection"])
    robust_frontend = robust_frontend or bool(re.search(r"\b(?:ransac|magsac)\b", text))
    if robust_frontend:
        add(("Robustness, Evaluation & Operations", "Outlier and Failure Robustness", "Front-End Robustness"), 0.62, "Robustness/failure handling is a cross-cutting operational concern.")
    if any(term in text for term in ["factor graph", "bayes tree", "graph optimization"]):
        add(("State, Geometry & Probabilistic Modeling", "Factor Graph Modeling", "Graphical Model Formulation"), 0.78, "Uses factor-graph structure as a modeling contribution.")
    if any(term in text for term in ["semidefinite", "certifiably", "certifiable", "globally optimal"]):
        add(("Back-End Optimization & Inference", "Certifiable and Differentiable Solvers", "Certifiably Optimal SLAM"), 0.88, "Contributes certifiable/global optimization.")
    if any(term in text for term in ["wheel-mounted", "wheelmounted", "wheel-ins", "dead reckoning"]):
        add(("Sensor & Odometry Modalities", "Proprioceptive and Aided Odometry", "Other Aiding Signals"), 0.9, "Wheel-mounted dead reckoning is an aided proprioceptive odometry signal.")
    return facets


def build_matched_paths(ref: dict, context_ref: dict, order_to_genus: dict) -> list[dict]:
    primary_path = (ref.get("phylum", ""), ref.get("class", ""), ref.get("order", ""))
    primary_genus = ref.get("genus", "(general)")
    paths = [
        path_dict(
            primary_path,
            primary_genus,
            "primary",
            float(ref.get("confidence") or 0.8),
            ref.get("rationale", "Primary curated placement."),
        )
    ]

    for semantic_path, confidence, reason in [*semantic_path_votes(ref, context_ref), *conceptual_facets(ref)]:
        choices = order_to_genus.get(semantic_path, [])
        genus, _, _ = choose_genus({**ref, "phylum": semantic_path[0], "class": semantic_path[1], "order": semantic_path[2]}, context_ref, choices)
        paths.append(path_dict(semantic_path, genus, "secondary", confidence, reason))

    deduped = {}
    for item in paths:
        key = path_key(item)
        if key not in deduped or item["confidence"] > deduped[key]["confidence"]:
            deduped[key] = item
        if key == path_key(paths[0]):
            deduped[key]["role"] = "primary"
    return sorted(deduped.values(), key=lambda item: (item["role"] != "primary", -item["confidence"], item["phylum"]))


def write_outputs(refs):
    OUT_JSON.write_text(json.dumps(refs, ensure_ascii=False, indent=2), encoding="utf-8")
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
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for ref in refs:
            row = {k: ref.get(k, "") for k in fields}
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
    compact = [{k: ref.get(k, "") for k in compact_fields} for ref in refs]
    OUT_JS.write_text(
        "window.SLAM_REFERENCES_SEMANTIC = "
        + json.dumps(compact, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )


def main():
    order_to_genus = taxonomy_order_to_genus()
    refs = json.loads(SEMANTIC_JSON.read_text(encoding="utf-8"))
    contexts = {ref["id"]: ref for ref in json.loads(CONTEXT_JSON.read_text(encoding="utf-8"))}
    updated = []
    methods = Counter()
    genus_counts = Counter()
    missing_paths = []
    for ref in refs:
        item = dict(ref)
        if apply_path_override(item):
            methods["codex_context_path_override"] += 1
            genus_counts[item["genus"]] += 1
            item["matched_paths"] = build_matched_paths(item, contexts.get(item["id"], {}), order_to_genus)
            updated.append(item)
            continue
        key = (item.get("phylum"), item.get("class"), item.get("order"))
        choices = order_to_genus.get(key, [])
        if choices:
            genus, method, score = choose_genus(item, contexts.get(item["id"], {}), choices)
            item["genus"] = genus
            item["match_method"] = item.get("match_method", "codex_context_semantic")
            suffix = f" Genus label: {genus} ({method}, score={score})."
            if suffix not in item.get("rationale", ""):
                item["rationale"] = (item.get("rationale", "") + suffix).strip()
            methods[method] += 1
            genus_counts[genus] += 1
        else:
            item["genus"] = "(unmapped)"
            missing_paths.append(key)
        item["matched_paths"] = build_matched_paths(item, contexts.get(item["id"], {}), order_to_genus)
        updated.append(item)
    write_outputs(updated)
    print(f"updated {len(updated)} references")
    print("methods", dict(methods))
    print("top genus", genus_counts.most_common(20))
    if missing_paths:
        print("missing paths", Counter(missing_paths).most_common())


if __name__ == "__main__":
    main()
