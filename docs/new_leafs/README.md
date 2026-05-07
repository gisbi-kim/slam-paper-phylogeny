# SLAM Handbook Semantic Reassignment — Pipeline & Demo

전달물 3종:

| 파일 | 용도 |
|---|---|
| `run_semantic_assignment.py` | 1,320개 references 전체를 Anthropic API로 처리하는 production 파이프라인 |
| `demo_30_semantic.json` | 다양한 30개 reference에 대한 high-quality LLM judgment 결과 (품질 검증용) |
| `refs_parsed.json` / `leaves.json` | inventory.md를 구조화한 입력 데이터 |

---

## 1. 30-paper Demo 결과 요약

다양한 phylum과 난이도를 포함한 30개를 직접 처리.

- **전체 8 phyla 모두 커버**됨
- **20/30 (67%)이 primary-path 교정**됨 (현재 자동 라벨이 틀렸던 케이스)
- **23/30이 multi-membership** (평균 1.87 paths/ref, 정책의 1–3 범위 준수)
- 모든 path가 204개 leaf set에 속함 (구조 검증 통과)

대표적 교정 사례:

| ID | Title | 기존 라벨 | 새 primary |
|---|---|---|---|
| 1 | Socratic Models | Robust Pose Graph Optimization (오인용) | Vision-Language Grounding |
| 50 | Batch CT GP Regression (Anderson&Barfoot) | SLAM Eras > Spatial AI Era | Continuous-Time > **Gaussian Process Trajectories** |
| 200 | UMI: Universal Manipulation Interface | Open-Set Object Maps | Autonomy Role > **Manipulation Support** |
| 400 | TORO (Grisetti et al.) | SE-Sync-style Solvers (잘못) | Nonlinear Optimization > **Gauss-Newton** |
| 500 | ICRA Quadruped Challenge | Visual-Inertial Odometry | **Legged State Estimation** |
| 700 | Lu & Milios 1997 | Spatial AI Era (시대 오류) | **Probabilistic Robotics Era** |
| 800 | DTAM (Newcombe 2011) | Processor / Sensor Co-Design (잘못) | **Real-Time Dense Reconstruction** |
| 1200 | Wheel-SLAM 2023 | Visual-Inertial Odometry | **Wheel Odometry** |
| 1250 | M2DGR | Event SLAM Datasets (오류) | **Visual SLAM Datasets** |

Multi-membership 잘 잡힌 예시:

- `[3] Kimera2`: primary=Dense Semantic Maps + secondary=VIO
- `[450] BodySLAM++`: primary=Multi-Body Scene Models + secondary=VIO + tertiary=Deformable Object Maps
- `[700] Lu&Milios`: primary=Probabilistic Robotics Era + secondary=Scan-to-Map Matching + tertiary=Pose-Graph Models

---

## 2. Production 파이프라인 사용법

```bash
# Anthropic SDK 설치
pip install "anthropic>=0.40.0"

# API 키 설정
export ANTHROPIC_API_KEY="sk-ant-..."

# 입력 파일을 같은 폴더에 두고 실행
python run_semantic_assignment.py \
    --inventory SLAM_HANDBOOK_REFERENCES_INVENTORY.md \
    --leaves SLAM_4DEPTH_TAXONOMY_LEAVES.md \
    --output slam_handbook_references_semantic.json \
    --model claude-sonnet-4-6 \
    --concurrency 8
```

### 핵심 설계

- **Prompt caching**: 204-leaf taxonomy + decision policy를 system block에 `cache_control:ephemeral`로 캐싱 → 두 번째 호출부터 input 비용이 약 1/10로 떨어짐.
- **Resume 지원**: 결과를 `*.jsonl` 로그에 즉시 flush. 중단되어도 동일 명령 재실행 시 이미 끝난 ID는 건너뜀.
- **Path validation + 1회 retry**: LLM이 leaf set 밖 path를 만들면 잘못된 path를 알려주고 한 번 다시 묻고, 그래도 실패하면 `*.errors.jsonl`로 분리 저장.
- **부분 실행**: `--start 1 --end 100` 같은 범위 지정 가능 (배치 분할용).
- **Concurrency 8** 기본 (Anthropic Tier 2 안전구간).

### 비용 추정 (1,320 papers)

per-call 토큰 (대략):
- system (cached after 1st call): ~3.2K tokens
- user message: ~700–1500 tokens (제목 + 5개 context, 600자 cap)
- output: ~300–500 tokens

**Sonnet 4.6** ($3 / $15 per M tokens, cached input $0.30 / M):
- 첫 호출: ~$0.013 / 이후 호출: ~$0.005
- 1,320 호출 ≈ **$8 ~ $12**

**Haiku 4.5** ($1 / $5 per M tokens, cached $0.10 / M, 빠른 처리):
- per-call ~$0.0015
- 1,320 호출 ≈ **$2 ~ $3**

**Batch API** 사용 시 위 비용에 50% 할인 추가 적용 가능.

처리 시간 기준치: concurrency 8 + Sonnet → ~10–15분.

### 결과 schema

각 record는 prompt에 정의된 schema 그대로:

```json
{
  "id": 1,
  "title": "...",
  "primary_path": ["SLAM", "Phylum", "Class", "Order", "Genus"],
  "matched_paths": [
    {"path": [...], "role": "primary",   "confidence": 0.92, "reason": "..."},
    {"path": [...], "role": "secondary", "confidence": 0.85, "reason": "..."}
  ],
  "uncertainty": ""
}
```

`primary_path`는 `matched_paths`의 `"role":"primary"`인 entry의 path와 항상 일치 (스크립트가 검증).

---

## 3. 권장 검증 워크플로우

1. **Demo 30개부터 검토** — `demo_30_semantic.json`을 보고 reasoning이 lab의 의도와 맞는지 확인.
2. 필요하면 `run_semantic_assignment.py`의 `DECISION_POLICY` / few-shot 예시를 lab 취향대로 수정.
3. 작은 배치부터 검증: `--start 1 --end 50`으로 50개 먼저 돌려보고 품질이 demo 수준인지 확인.
4. 만족하면 `--end 1320`으로 전체 실행.
5. 결과 JSON을 기존 `data/slam_handbook_references_semantic.json`과 diff해서 spot-check.

---

## 4. 한계 및 주의사항

- **Citation-key collision**: ref [1] Socratic Models처럼 inventory의 context excerpt가 실제 논문과 무관할 수 있음. LLM은 제목 우선으로 판단하므로 일부 reference에서 판단 근거가 weak해질 수 있음.
- **Survey/Historical refs**: e.g. [900] 같은 1차 SLAM 연관 약한 paper는 single-path moderate-confidence로 처리됨.
- **`Multi-Body Scene Models`** vs **`Object-Level Maps`** vs **`Sparse Semantic Landmarks`** 같이 인접 leaf끼리 ambiguity가 있는 경우는 `uncertainty` 필드에 명시되도록 prompt 설계함.
- 1,320개 전체에 LLM judgment를 도는 만큼 ~1–3% 정도 borderline 케이스는 사람 검토 필요. `confidence < 0.6` filter로 빠르게 후보 추출 가능.
