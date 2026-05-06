# SLAM Phylogenetic Taxonomy v0.1

Source: SLAM Handbook public release, compiled April 21, 2026.

Unit: `Phylum > Class > Order > Genus`

Rule: each paper should receive one primary path. Cross-cutting traits such as "deep", "real-time", or "multi-modal" are only primary when they are the central contribution.

## 1. Problem & System Context

- **SLAM Problem Definition**
  - Localization vs Mapping vs SLAM
    - Known-map Localization
    - Mapping with Known Poses
    - Joint Localization and Mapping
  - Autonomy Role
    - Navigation Support
    - Manipulation Support
    - Exploration Support
    - Long-term Spatial Memory
- **System Architecture**
  - Modern SLAM Pipeline
    - Front-end / Back-end Split
    - Odometry Stream
    - Loop-Closure Stream
    - Map Update Loop
  - Autonomy Integration
    - Control Loop Interface
    - Planning Loop Interface
    - Latency and Rate Separation
    - Online Operation
- **Historical and Scope Framing**
  - SLAM Eras
    - Probabilistic Robotics Era
    - Graph Optimization Era
    - Robust Perception Era
    - Spatial AI Era

## 2. State, Geometry & Probabilistic Modeling

- **Factor Graph Modeling**
  - Graphical Model Formulation
    - Variables and Factors
    - Landmark-based Models
    - Pose-Graph Models
    - Hybrid Factor Graphs
  - MAP Inference
    - Negative Log-Likelihood
    - Least-Squares Formulation
    - Noise Models
- **State Representations**
  - Lie Groups and Manifolds
    - SO(3) Rotation States
    - SE(3) Pose States
    - Retractions and Local Coordinates
  - Continuous-Time Trajectories
    - Gaussian Process Trajectories
    - Spline Trajectories
    - Asynchronous Sensor Fusion
- **Observability and Uncertainty**
  - Estimation Consistency
    - Gauge Freedom
    - Degeneracy
    - Covariance and Marginals
  - Inertial Observability
    - Bias Observability
    - Gravity Alignment
    - Scale Observability

## 3. Measurement Front-End

- **Raw-to-Pseudo Measurement Processing**
  - Feature Extraction
    - Keypoints and Descriptors
    - Lines and Planes
    - Learned Features
  - Direct Measurement Formation
    - Photometric Residuals
    - Range Residuals
    - Event Residuals
  - Registration
    - ICP
    - Scan-to-Map Matching
    - Point-to-Plane Matching
- **Odometry Front-End**
  - Frame-to-Frame Motion Estimation
    - Visual Odometry
    - LiDAR Odometry
    - Radar Odometry
    - Event Odometry
  - Preintegration and Propagation
    - IMU Preintegration
    - Leg Odometry Propagation
    - Wheel / Kinematic Propagation
- **Place Recognition and Loop Closure**
  - Place Recognition
    - Visual Place Recognition
    - LiDAR Place Recognition
    - Radar Place Recognition
    - Cross-Modal Place Recognition
  - Loop Closure Validation
    - Geometric Verification
    - Temporal Consistency
    - Outlier-aware Loop Closure
- **Data Association**
  - Correspondence Estimation
    - Landmark Association
    - Scan Correspondence
    - Object Association
  - Ambiguity Handling
    - Perceptual Aliasing
    - Incorrect Association Detection
    - Multi-Hypothesis Association

## 4. Back-End Optimization & Inference

- **Least-Squares Solvers**
  - Linear Least Squares
    - Normal Equations
    - QR / Cholesky
    - Sparse Linear Algebra
  - Nonlinear Optimization
    - Gauss-Newton
    - Levenberg-Marquardt
    - Trust Region Methods
- **Sparsity and Incrementality**
  - Variable Elimination
    - Bayes Trees
    - Fill-in Reduction
    - Schur Complement
  - Incremental SLAM
    - iSAM-style Updates
    - Fixed-Lag Smoothing
    - Marginalization
- **Robust Back-End**
  - Robust Cost Functions
    - M-estimators
    - Switchable Constraints
    - Graduated Non-Convexity
  - Outlier-Robust Optimization
    - Max-Mixture Models
    - Pairwise Consistency
    - Robust Pose Graph Optimization
- **Certifiable and Differentiable Solvers**
  - Certifiably Optimal SLAM
    - Semidefinite Relaxation
    - Tightness Certification
    - SE-Sync-style Solvers
  - Differentiable Optimization
    - Differentiating Through Least Squares
    - Implicit Differentiation
    - Differentiation on Manifolds

## 5. Map Representations

- **Sparse Geometric Maps**
  - Landmark Maps
    - Point Landmarks
    - Line Landmarks
    - Plane Landmarks
  - Pose Graph Maps
    - Topological Graphs
    - Submap Graphs
    - Multi-Session Graphs
- **Dense Geometric Maps**
  - Range-Derived Maps
    - Occupancy Grids
    - TSDF / ESDF
    - Point Cloud Maps
    - Mesh Maps
  - Dense Reconstruction
    - Real-Time Dense Reconstruction
    - RGB-D Reconstruction
    - Large-Scale Dense Mapping
- **Neural and Differentiable Maps**
  - Neural Implicit Maps
    - NeRF Maps
    - Neural SDF Maps
    - Learned Occupancy Fields
  - Gaussian Maps
    - 3D Gaussian Splatting
    - Differentiable Rendering Maps
    - Hybrid Explicit-Implicit Maps
- **Semantic and Structured Maps**
  - Metric-Semantic Maps
    - Sparse Semantic Landmarks
    - Dense Semantic Maps
    - Object-Level Maps
  - Hierarchical Spatial Maps
    - 3D Scene Graphs
    - Room / Place Graphs
    - Open-Vocabulary Maps
- **Dynamic and Deformable Maps**
  - Dynamic SLAM Maps
    - Short-Term Dynamic Objects
    - Long-Term Lifelong Changes
    - Multi-Body Scene Models
  - Deformable SLAM Maps
    - Non-Rigid Surfaces
    - Deformable Object Maps
    - Elastic Scene Models

## 6. Sensor & Odometry Modalities

- **Visual SLAM**
  - Camera Models and Pipelines
    - Monocular SLAM
    - Stereo SLAM
    - RGB-D SLAM
  - Visual System Families
    - Feature-Based Visual SLAM
    - Direct Visual SLAM
    - Hybrid Visual SLAM
- **LiDAR SLAM**
  - LiDAR Sensing
    - 2D LiDAR
    - 3D Spinning LiDAR
    - Solid-State LiDAR
  - LiDAR System Families
    - LOAM-style Odometry
    - Scan-Matching SLAM
    - LiDAR-Inertial SLAM
- **Radar SLAM**
  - Radar Sensing
    - FMCW Radar
    - Imaging Radar
    - 4D Radar
  - Radar System Families
    - Radar Odometry
    - Radar Place Recognition
    - Radar Mapping
- **Event-Based SLAM**
  - Event Sensor Processing
    - Event Representations
    - Event Feature Tracking
    - Event Time Surfaces
  - Event System Families
    - Event Odometry
    - Event-Inertial Odometry
    - Event-Based Mapping
- **Proprioceptive and Aided Odometry**
  - Inertial Odometry
    - Strapdown Integration
    - IMU Preintegration
    - Visual-Inertial Odometry
  - Leg Odometry
    - Contact Estimation
    - Kinematic Factors
    - Legged State Estimation
  - Other Aiding Signals
    - Wheel Odometry
    - GNSS Factors
    - UWB / Radio Factors
- **Multi-Modal Fusion**
  - Sensor Fusion Architectures
    - Tightly Coupled Fusion
    - Loosely Coupled Fusion
    - Cross-Modal Factors
  - Calibration and Synchronization
    - Extrinsic Calibration
    - Temporal Calibration
    - Online Calibration

## 7. Robustness, Evaluation & Operations

- **Outlier and Failure Robustness**
  - Front-End Robustness
    - RANSAC-style Rejection
    - Descriptor Ambiguity Handling
    - Dynamic Object Rejection
  - Back-End Robustness
    - Robust Kernels
    - Certifiable Outlier Rejection
    - Failure Recovery
- **Evaluation**
  - Metrics
    - Absolute Trajectory Error
    - Relative Pose Error
    - Map Quality Metrics
    - Place Recognition Metrics
  - Datasets and Benchmarks
    - Visual SLAM Datasets
    - LiDAR SLAM Datasets
    - Radar SLAM Datasets
    - Event SLAM Datasets
    - Legged SLAM Datasets
- **Operational Constraints**
  - Real-Time Performance
    - Embedded Runtime
    - Latency Budgets
    - Memory Growth Control
  - Deployment Conditions
    - GPS-Denied Operation
    - Large-Scale Operation
    - Long-Term Operation
    - Resource-Constrained Operation

## 8. Learning, Semantics & Spatial AI

- **Learning for Classical SLAM Components**
  - Learned Geometry
    - Depth Prediction
    - Camera Pose Prediction
    - Optical Flow
  - Learned Correspondence
    - Feature Matching
    - Dense Matching
    - Learned Place Recognition
  - Learned Optimization
    - Differentiable Bundle Adjustment
    - DROID-SLAM-style Recurrent Updates
    - Learned Priors
- **Foundation and Open-World Spatial AI**
  - Foundation Models for Spatial AI
    - Vision-Language Grounding
    - Open-Vocabulary Recognition
    - Large-Scale Semantic Priors
  - Open-World Mapping
    - Open-Set Object Maps
    - Language-Grounded Maps
    - Continual Map Expansion
- **Computational Structure**
  - Spatial AI Graphs
    - Factor-Graph Computation
    - Scene-Graph Computation
    - Hybrid Neural-Symbolic Graphs
  - Distributed and Hardware-Aware Computation
    - Processor / Sensor Co-Design
    - Gaussian Belief Propagation
    - Continual Learning in Graphs

## Primary Label Rules

- If the contribution is a new sensor-specific full system, assign to `Sensor & Odometry Modalities`.
- If the contribution is a new residual, association, registration, or loop detection module, assign to `Measurement Front-End`.
- If the contribution is a solver, inference method, robust objective, or differentiable optimizer, assign to `Back-End Optimization & Inference`.
- If the contribution is a representation of the world, assign to `Map Representations`.
- If the contribution is mainly about benchmarks, metrics, runtime, or deployment reliability, assign to `Robustness, Evaluation & Operations`.
- If the contribution uses learning as the core algorithmic novelty, assign to `Learning, Semantics & Spatial AI`; if learning is only a component inside a sensor pipeline, keep the primary label under that sensor or front-end branch.

