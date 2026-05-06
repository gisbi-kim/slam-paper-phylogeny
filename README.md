# SLAM Paper Phylogeny

SLAM Handbook를 기준으로 SLAM 연구 지형을 `Phylum > Class > Order > Genus` 4단계 계통도로 재구성한 초안입니다.

이 작업의 기준은 장 번호를 그대로 베끼는 것이 아니라, SLAM 시스템 안에서의 기능적 역할을 기준으로 MECE하게 재배열하는 것입니다. 같은 장에서 나온 내용도 역할이 다르면 서로 다른 가지로 분해합니다.

## Inputs

- `../robotics-paper-phylogeny`: 기존 robotics phylogeny 프로젝트의 산출물 구조 참고
- `../slam-handbook-public-release/main.pdf`: SLAM Handbook 공개 PDF
- `../slam-handbook-public-release/README.md`: 장 제목과 citation metadata

## Deliverables

- `docs/SLAM_TAXONOMY.md`: SLAM 전용 4-depth 계통도
- `data/slam_handbook_chapter_map.csv`: Handbook 장/절을 새 taxonomy에 대응시킨 seed map
- `data/taxonomy_tree.json`: 시각화와 자동 분류기에 사용할 tree seed
- `data/slam_handbook_references.csv`: Handbook References 1320 entries mapped to one taxonomy path each
- `data/slam_handbook_references.json`: full reference matching output
- `data/references.js`: compact browser dataset used by `index.html`
- `scripts/build_reference_dataset.py`: reproducible PDF References parser and rule-based matcher

## Design Principle

Top-level Phylum은 논문 제목이나 장 제목의 표면 단어가 아니라, SLAM 시스템 안에서의 주 기능으로 나눕니다.

1. Problem & System Context
2. State, Geometry & Probabilistic Modeling
3. Measurement Front-End
4. Back-End Optimization & Inference
5. Map Representations
6. Sensor & Odometry Modalities
7. Robustness, Evaluation & Operations
8. Learning, Semantics & Spatial AI

이렇게 나누면 Visual/LiDAR/Radar/Event 같은 센서별 장과 Factor Graph/Robustness/Differentiable Optimization 같은 수학 장이 서로 침범하지 않고, "이 논문의 주 기여가 무엇인가?"라는 기준으로 단일 라벨을 줄 수 있습니다.

## Reference Matching

```bash
python scripts/build_reference_dataset.py
```

The script extracts the `References` section from `../slam-handbook-public-release/main.pdf`, parses `[1]` through `[1320]`, assigns each cited work to one primary taxonomy path, and rewrites the CSV/JSON/JS outputs under `data/`.
