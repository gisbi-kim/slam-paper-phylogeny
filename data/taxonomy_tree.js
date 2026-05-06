window.SLAM_TAXONOMY = {
  "name": "SLAM",
  "children": [
    {
      "name": "Problem & System Context",
      "children": [
        {
          "name": "SLAM Problem Definition",
          "children": [
            {
              "name": "Localization vs Mapping vs SLAM",
              "children": [
                {
                  "name": "Known-map Localization"
                },
                {
                  "name": "Mapping with Known Poses"
                },
                {
                  "name": "Joint Localization and Mapping"
                }
              ]
            },
            {
              "name": "Autonomy Role",
              "children": [
                {
                  "name": "Navigation Support"
                },
                {
                  "name": "Manipulation Support"
                },
                {
                  "name": "Exploration Support"
                },
                {
                  "name": "Long-term Spatial Memory"
                }
              ]
            }
          ]
        },
        {
          "name": "System Architecture",
          "children": [
            {
              "name": "Modern SLAM Pipeline",
              "children": [
                {
                  "name": "Front-end / Back-end Split"
                },
                {
                  "name": "Odometry Stream"
                },
                {
                  "name": "Loop-Closure Stream"
                },
                {
                  "name": "Map Update Loop"
                }
              ]
            },
            {
              "name": "Autonomy Integration",
              "children": [
                {
                  "name": "Control Loop Interface"
                },
                {
                  "name": "Planning Loop Interface"
                },
                {
                  "name": "Latency and Rate Separation"
                },
                {
                  "name": "Online Operation"
                }
              ]
            }
          ]
        },
        {
          "name": "Historical and Scope Framing",
          "children": [
            {
              "name": "SLAM Eras",
              "children": [
                {
                  "name": "Probabilistic Robotics Era"
                },
                {
                  "name": "Graph Optimization Era"
                },
                {
                  "name": "Robust Perception Era"
                },
                {
                  "name": "Spatial AI Era"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "State, Geometry & Probabilistic Modeling",
      "children": [
        {
          "name": "Factor Graph Modeling",
          "children": [
            {
              "name": "Graphical Model Formulation",
              "children": [
                {
                  "name": "Variables and Factors"
                },
                {
                  "name": "Landmark-based Models"
                },
                {
                  "name": "Pose-Graph Models"
                },
                {
                  "name": "Hybrid Factor Graphs"
                }
              ]
            },
            {
              "name": "MAP Inference",
              "children": [
                {
                  "name": "Negative Log-Likelihood"
                },
                {
                  "name": "Least-Squares Formulation"
                },
                {
                  "name": "Noise Models"
                }
              ]
            }
          ]
        },
        {
          "name": "State Representations",
          "children": [
            {
              "name": "Lie Groups and Manifolds",
              "children": [
                {
                  "name": "SO(3) Rotation States"
                },
                {
                  "name": "SE(3) Pose States"
                },
                {
                  "name": "Retractions and Local Coordinates"
                }
              ]
            },
            {
              "name": "Continuous-Time Trajectories",
              "children": [
                {
                  "name": "Gaussian Process Trajectories"
                },
                {
                  "name": "Spline Trajectories"
                },
                {
                  "name": "Asynchronous Sensor Fusion"
                }
              ]
            }
          ]
        },
        {
          "name": "Observability and Uncertainty",
          "children": [
            {
              "name": "Estimation Consistency",
              "children": [
                {
                  "name": "Gauge Freedom"
                },
                {
                  "name": "Degeneracy"
                },
                {
                  "name": "Covariance and Marginals"
                }
              ]
            },
            {
              "name": "Inertial Observability",
              "children": [
                {
                  "name": "Bias Observability"
                },
                {
                  "name": "Gravity Alignment"
                },
                {
                  "name": "Scale Observability"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "Measurement Front-End",
      "children": [
        {
          "name": "Raw-to-Pseudo Measurement Processing",
          "children": [
            {
              "name": "Feature Extraction",
              "children": [
                {
                  "name": "Keypoints and Descriptors"
                },
                {
                  "name": "Lines and Planes"
                },
                {
                  "name": "Learned Features"
                }
              ]
            },
            {
              "name": "Direct Measurement Formation",
              "children": [
                {
                  "name": "Photometric Residuals"
                },
                {
                  "name": "Range Residuals"
                },
                {
                  "name": "Event Residuals"
                }
              ]
            },
            {
              "name": "Registration",
              "children": [
                {
                  "name": "ICP"
                },
                {
                  "name": "Scan-to-Map Matching"
                },
                {
                  "name": "Point-to-Plane Matching"
                }
              ]
            }
          ]
        },
        {
          "name": "Odometry Front-End",
          "children": [
            {
              "name": "Frame-to-Frame Motion Estimation",
              "children": [
                {
                  "name": "Visual Odometry"
                },
                {
                  "name": "LiDAR Odometry"
                },
                {
                  "name": "Radar Odometry"
                },
                {
                  "name": "Event Odometry"
                }
              ]
            },
            {
              "name": "Preintegration and Propagation",
              "children": [
                {
                  "name": "IMU Preintegration"
                },
                {
                  "name": "Leg Odometry Propagation"
                },
                {
                  "name": "Wheel / Kinematic Propagation"
                }
              ]
            }
          ]
        },
        {
          "name": "Place Recognition and Loop Closure",
          "children": [
            {
              "name": "Place Recognition",
              "children": [
                {
                  "name": "Visual Place Recognition"
                },
                {
                  "name": "LiDAR Place Recognition"
                },
                {
                  "name": "Radar Place Recognition"
                },
                {
                  "name": "Cross-Modal Place Recognition"
                }
              ]
            },
            {
              "name": "Loop Closure Validation",
              "children": [
                {
                  "name": "Geometric Verification"
                },
                {
                  "name": "Temporal Consistency"
                },
                {
                  "name": "Outlier-aware Loop Closure"
                }
              ]
            }
          ]
        },
        {
          "name": "Data Association",
          "children": [
            {
              "name": "Correspondence Estimation",
              "children": [
                {
                  "name": "Landmark Association"
                },
                {
                  "name": "Scan Correspondence"
                },
                {
                  "name": "Object Association"
                }
              ]
            },
            {
              "name": "Ambiguity Handling",
              "children": [
                {
                  "name": "Perceptual Aliasing"
                },
                {
                  "name": "Incorrect Association Detection"
                },
                {
                  "name": "Multi-Hypothesis Association"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "Back-End Optimization & Inference",
      "children": [
        {
          "name": "Least-Squares Solvers",
          "children": [
            {
              "name": "Linear Least Squares",
              "children": [
                {
                  "name": "Normal Equations"
                },
                {
                  "name": "QR / Cholesky"
                },
                {
                  "name": "Sparse Linear Algebra"
                }
              ]
            },
            {
              "name": "Nonlinear Optimization",
              "children": [
                {
                  "name": "Gauss-Newton"
                },
                {
                  "name": "Levenberg-Marquardt"
                },
                {
                  "name": "Trust Region Methods"
                }
              ]
            }
          ]
        },
        {
          "name": "Sparsity and Incrementality",
          "children": [
            {
              "name": "Variable Elimination",
              "children": [
                {
                  "name": "Bayes Trees"
                },
                {
                  "name": "Fill-in Reduction"
                },
                {
                  "name": "Schur Complement"
                }
              ]
            },
            {
              "name": "Incremental SLAM",
              "children": [
                {
                  "name": "iSAM-style Updates"
                },
                {
                  "name": "Fixed-Lag Smoothing"
                },
                {
                  "name": "Marginalization"
                }
              ]
            }
          ]
        },
        {
          "name": "Robust Back-End",
          "children": [
            {
              "name": "Robust Cost Functions",
              "children": [
                {
                  "name": "M-estimators"
                },
                {
                  "name": "Switchable Constraints"
                },
                {
                  "name": "Graduated Non-Convexity"
                }
              ]
            },
            {
              "name": "Outlier-Robust Optimization",
              "children": [
                {
                  "name": "Max-Mixture Models"
                },
                {
                  "name": "Pairwise Consistency"
                },
                {
                  "name": "Robust Pose Graph Optimization"
                }
              ]
            }
          ]
        },
        {
          "name": "Certifiable and Differentiable Solvers",
          "children": [
            {
              "name": "Certifiably Optimal SLAM",
              "children": [
                {
                  "name": "Semidefinite Relaxation"
                },
                {
                  "name": "Tightness Certification"
                },
                {
                  "name": "SE-Sync-style Solvers"
                }
              ]
            },
            {
              "name": "Differentiable Optimization",
              "children": [
                {
                  "name": "Differentiating Through Least Squares"
                },
                {
                  "name": "Implicit Differentiation"
                },
                {
                  "name": "Differentiation on Manifolds"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "Map Representations",
      "children": [
        {
          "name": "Sparse Geometric Maps",
          "children": [
            {
              "name": "Landmark Maps",
              "children": [
                {
                  "name": "Point Landmarks"
                },
                {
                  "name": "Line Landmarks"
                },
                {
                  "name": "Plane Landmarks"
                }
              ]
            },
            {
              "name": "Pose Graph Maps",
              "children": [
                {
                  "name": "Topological Graphs"
                },
                {
                  "name": "Submap Graphs"
                },
                {
                  "name": "Multi-Session Graphs"
                }
              ]
            }
          ]
        },
        {
          "name": "Dense Geometric Maps",
          "children": [
            {
              "name": "Range-Derived Maps",
              "children": [
                {
                  "name": "Occupancy Grids"
                },
                {
                  "name": "TSDF / ESDF"
                },
                {
                  "name": "Point Cloud Maps"
                },
                {
                  "name": "Mesh Maps"
                }
              ]
            },
            {
              "name": "Dense Reconstruction",
              "children": [
                {
                  "name": "Real-Time Dense Reconstruction"
                },
                {
                  "name": "RGB-D Reconstruction"
                },
                {
                  "name": "Large-Scale Dense Mapping"
                }
              ]
            }
          ]
        },
        {
          "name": "Neural and Differentiable Maps",
          "children": [
            {
              "name": "Neural Implicit Maps",
              "children": [
                {
                  "name": "NeRF Maps"
                },
                {
                  "name": "Neural SDF Maps"
                },
                {
                  "name": "Learned Occupancy Fields"
                }
              ]
            },
            {
              "name": "Gaussian Maps",
              "children": [
                {
                  "name": "3D Gaussian Splatting"
                },
                {
                  "name": "Differentiable Rendering Maps"
                },
                {
                  "name": "Hybrid Explicit-Implicit Maps"
                }
              ]
            }
          ]
        },
        {
          "name": "Semantic and Structured Maps",
          "children": [
            {
              "name": "Metric-Semantic Maps",
              "children": [
                {
                  "name": "Sparse Semantic Landmarks"
                },
                {
                  "name": "Dense Semantic Maps"
                },
                {
                  "name": "Object-Level Maps"
                }
              ]
            },
            {
              "name": "Hierarchical Spatial Maps",
              "children": [
                {
                  "name": "3D Scene Graphs"
                },
                {
                  "name": "Room / Place Graphs"
                },
                {
                  "name": "Open-Vocabulary Maps"
                }
              ]
            }
          ]
        },
        {
          "name": "Dynamic and Deformable Maps",
          "children": [
            {
              "name": "Dynamic SLAM Maps",
              "children": [
                {
                  "name": "Short-Term Dynamic Objects"
                },
                {
                  "name": "Long-Term Lifelong Changes"
                },
                {
                  "name": "Multi-Body Scene Models"
                }
              ]
            },
            {
              "name": "Deformable SLAM Maps",
              "children": [
                {
                  "name": "Non-Rigid Surfaces"
                },
                {
                  "name": "Deformable Object Maps"
                },
                {
                  "name": "Elastic Scene Models"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "Sensor & Odometry Modalities",
      "children": [
        {
          "name": "Visual SLAM",
          "children": [
            {
              "name": "Camera Models and Pipelines",
              "children": [
                {
                  "name": "Monocular SLAM"
                },
                {
                  "name": "Stereo SLAM"
                },
                {
                  "name": "RGB-D SLAM"
                }
              ]
            },
            {
              "name": "Visual System Families",
              "children": [
                {
                  "name": "Feature-Based Visual SLAM"
                },
                {
                  "name": "Direct Visual SLAM"
                },
                {
                  "name": "Hybrid Visual SLAM"
                }
              ]
            }
          ]
        },
        {
          "name": "LiDAR SLAM",
          "children": [
            {
              "name": "LiDAR Sensing",
              "children": [
                {
                  "name": "2D LiDAR"
                },
                {
                  "name": "3D Spinning LiDAR"
                },
                {
                  "name": "Solid-State LiDAR"
                }
              ]
            },
            {
              "name": "LiDAR System Families",
              "children": [
                {
                  "name": "LOAM-style Odometry"
                },
                {
                  "name": "Scan-Matching SLAM"
                },
                {
                  "name": "LiDAR-Inertial SLAM"
                }
              ]
            }
          ]
        },
        {
          "name": "Radar SLAM",
          "children": [
            {
              "name": "Radar Sensing",
              "children": [
                {
                  "name": "FMCW Radar"
                },
                {
                  "name": "Imaging Radar"
                },
                {
                  "name": "4D Radar"
                }
              ]
            },
            {
              "name": "Radar System Families",
              "children": [
                {
                  "name": "Radar Odometry"
                },
                {
                  "name": "Radar Place Recognition"
                },
                {
                  "name": "Radar Mapping"
                }
              ]
            }
          ]
        },
        {
          "name": "Event-Based SLAM",
          "children": [
            {
              "name": "Event Sensor Processing",
              "children": [
                {
                  "name": "Event Representations"
                },
                {
                  "name": "Event Feature Tracking"
                },
                {
                  "name": "Event Time Surfaces"
                }
              ]
            },
            {
              "name": "Event System Families",
              "children": [
                {
                  "name": "Event Odometry"
                },
                {
                  "name": "Event-Inertial Odometry"
                },
                {
                  "name": "Event-Based Mapping"
                }
              ]
            }
          ]
        },
        {
          "name": "Proprioceptive and Aided Odometry",
          "children": [
            {
              "name": "Inertial Odometry",
              "children": [
                {
                  "name": "Strapdown Integration"
                },
                {
                  "name": "IMU Preintegration"
                },
                {
                  "name": "Visual-Inertial Odometry"
                }
              ]
            },
            {
              "name": "Leg Odometry",
              "children": [
                {
                  "name": "Contact Estimation"
                },
                {
                  "name": "Kinematic Factors"
                },
                {
                  "name": "Legged State Estimation"
                }
              ]
            },
            {
              "name": "Other Aiding Signals",
              "children": [
                {
                  "name": "Wheel Odometry"
                },
                {
                  "name": "GNSS Factors"
                },
                {
                  "name": "UWB / Radio Factors"
                }
              ]
            }
          ]
        },
        {
          "name": "Multi-Modal Fusion",
          "children": [
            {
              "name": "Sensor Fusion Architectures",
              "children": [
                {
                  "name": "Tightly Coupled Fusion"
                },
                {
                  "name": "Loosely Coupled Fusion"
                },
                {
                  "name": "Cross-Modal Factors"
                }
              ]
            },
            {
              "name": "Calibration and Synchronization",
              "children": [
                {
                  "name": "Extrinsic Calibration"
                },
                {
                  "name": "Temporal Calibration"
                },
                {
                  "name": "Online Calibration"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "Robustness, Evaluation & Operations",
      "children": [
        {
          "name": "Outlier and Failure Robustness",
          "children": [
            {
              "name": "Front-End Robustness",
              "children": [
                {
                  "name": "RANSAC-style Rejection"
                },
                {
                  "name": "Descriptor Ambiguity Handling"
                },
                {
                  "name": "Dynamic Object Rejection"
                }
              ]
            },
            {
              "name": "Back-End Robustness",
              "children": [
                {
                  "name": "Robust Kernels"
                },
                {
                  "name": "Certifiable Outlier Rejection"
                },
                {
                  "name": "Failure Recovery"
                }
              ]
            }
          ]
        },
        {
          "name": "Evaluation",
          "children": [
            {
              "name": "Metrics",
              "children": [
                {
                  "name": "Absolute Trajectory Error"
                },
                {
                  "name": "Relative Pose Error"
                },
                {
                  "name": "Map Quality Metrics"
                },
                {
                  "name": "Place Recognition Metrics"
                }
              ]
            },
            {
              "name": "Datasets and Benchmarks",
              "children": [
                {
                  "name": "Visual SLAM Datasets"
                },
                {
                  "name": "LiDAR SLAM Datasets"
                },
                {
                  "name": "Radar SLAM Datasets"
                },
                {
                  "name": "Event SLAM Datasets"
                },
                {
                  "name": "Legged SLAM Datasets"
                }
              ]
            }
          ]
        },
        {
          "name": "Operational Constraints",
          "children": [
            {
              "name": "Real-Time Performance",
              "children": [
                {
                  "name": "Embedded Runtime"
                },
                {
                  "name": "Latency Budgets"
                },
                {
                  "name": "Memory Growth Control"
                }
              ]
            },
            {
              "name": "Deployment Conditions",
              "children": [
                {
                  "name": "GPS-Denied Operation"
                },
                {
                  "name": "Large-Scale Operation"
                },
                {
                  "name": "Long-Term Operation"
                },
                {
                  "name": "Resource-Constrained Operation"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "name": "Learning, Semantics & Spatial AI",
      "children": [
        {
          "name": "Learning for Classical SLAM Components",
          "children": [
            {
              "name": "Learned Geometry",
              "children": [
                {
                  "name": "Depth Prediction"
                },
                {
                  "name": "Camera Pose Prediction"
                },
                {
                  "name": "Optical Flow"
                }
              ]
            },
            {
              "name": "Learned Correspondence",
              "children": [
                {
                  "name": "Feature Matching"
                },
                {
                  "name": "Dense Matching"
                },
                {
                  "name": "Learned Place Recognition"
                }
              ]
            },
            {
              "name": "Learned Optimization",
              "children": [
                {
                  "name": "Differentiable Bundle Adjustment"
                },
                {
                  "name": "DROID-SLAM-style Recurrent Updates"
                },
                {
                  "name": "Learned Priors"
                }
              ]
            }
          ]
        },
        {
          "name": "Foundation and Open-World Spatial AI",
          "children": [
            {
              "name": "Foundation Models for Spatial AI",
              "children": [
                {
                  "name": "Vision-Language Grounding"
                },
                {
                  "name": "Open-Vocabulary Recognition"
                },
                {
                  "name": "Large-Scale Semantic Priors"
                }
              ]
            },
            {
              "name": "Open-World Mapping",
              "children": [
                {
                  "name": "Open-Set Object Maps"
                },
                {
                  "name": "Language-Grounded Maps"
                },
                {
                  "name": "Continual Map Expansion"
                }
              ]
            }
          ]
        },
        {
          "name": "Computational Structure",
          "children": [
            {
              "name": "Spatial AI Graphs",
              "children": [
                {
                  "name": "Factor-Graph Computation"
                },
                {
                  "name": "Scene-Graph Computation"
                },
                {
                  "name": "Hybrid Neural-Symbolic Graphs"
                }
              ]
            },
            {
              "name": "Distributed and Hardware-Aware Computation",
              "children": [
                {
                  "name": "Processor / Sensor Co-Design"
                },
                {
                  "name": "Gaussian Belief Propagation"
                },
                {
                  "name": "Continual Learning in Graphs"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
};
