# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — POST-3.1.2 PROTOCOL

## 1. ÉTAT ACTUEL

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Branch:** `feat/v4-3-instrument-contracts`
- **PR:** #8 — draft, unmerged
- **Main baseline:** `ff50b6d5d123969e091b5df18c46d438f7cb8052`
- **Locked qualification:** B09 — PASS
- **3.1.1 Momentum V1:** PASS — definition only
- **3.1.2 baseline protocol:** **PASS**
- **3.1.2 actual execution:** **BLOCKED** by dataset/execution-environment gate

## 2. RECOVERY ORDER

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/README.md`
4. latest `99-BACKUP/SESSION-YYYY-MM-DD.md`
5. `docs/00-MASTER-EXECUTION-CHECKLIST.md`
6. referenced reports/artifacts
7. actual GitHub/worktree state

## 3. LOCKED WORK — DO NOT RERUN

B02–B08 and B09.7 remain locked historical qualification results. No rerun is authorized merely to reconstruct memory.

B09 final remains PASS as historical qualification evidence.

## 4. DURABLE DATA IDENTITIES

- B05 corpus SHA256: `868a21c6a1bedf095b30bc64b6c2ef60b5db9d30146ac53034360254413f8ad7`
- B05 contract SHA256: `49e272534bf5061522eb624afe4e27d6585f730e0271b5284bff2442d5c04b07`
- Historical B08 stream SHA256: `4768c0e66647a15ba703d2dcdc88c03db84846a625e8eb3f70914428bf11c8d7`
- B09 canonical stream SHA256: `d8da494b2a1380ea0db0e0370ece4f609374ecb3e5647b6c1fb290836867abda`
- B05 corpus: `C:\ALGO-DATA\qualification\v4_3_multi_year_acquisition\candidate_b03_3_repaired\USATECHIDXUSD`
- B05 files: 495
- B05 ticks: 5,130,393

## 5. B08-A/B09 PERSISTENCE

The four historical source files were not recoverable from accessible GitHub history. The exact former Windows worktree is not accessible from the current environment. Per the recovery rule, the source was replaced by a controlled reconstruction explicitly labeled **RECONSTRUCTION ≠ RÉCUPÉRATION**.

Reconstructed files now versioned on the governed branch:
- `src/research/input_binding.py` — `fad72675f2e7ee44083b0cbc89910d8786829f4c`
- `src/research/bi5_reader.py` — `74005e2751782d91436d793ca9dc58c224bfe5f5`
- `src/research/engine.py` — `63d98f1a8e8829143260b2a81fbb14f821c5be66`
- `src/research/execution.py` — `eca03288338e6142ad5c23c400d18dab7e560e9b`
- `src/research/__init__.py` — `800aaab8a0e908ae2efbf719545d5ce34d7b53f9`

Historical B08-A/B09 PASS results were not rerun and remain historical evidence. The reconstruction itself is not silently upgraded to historical PASS.

## 6. 3.1.1 — MOMENTUM V1

- H1 / Close / horizon 20
- `M_t = Close_t / Close_{t-20} - 1`
- positive → LONG; negative → SHORT; zero → NEUTRE
- insufficient history → UNDEFINED
- computed after close `t`; usable from `t+1`
- no regime filter; no optimization
- directional signal only

**PASS = formal definition only.**

## 7. 3.1.2 — BASELINE PROTOCOL

Persisted:
- `docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md` — final protocol commit `c9901af955189e3edc78f4f0c20091b3ef2050c4`
- `reports/research/3_1_2_momentum_v1_baseline_adversarial_report.md` — final report commit `8271e740f6882b3f2038858991457945f0fc29e7`

The protocol was adversarially broken and corrected.

Final frozen harness:
- signal at close `t`;
- action only at `t+1`;
- normalized unit position;
- LONG → +1;
- SHORT → -1;
- NEUTRE → flat;
- opposite signal → close/reverse at next admissible execution point;
- no SL/TP/trailing/BE/pyramiding/scaling/discretionary exit;
- realistic spread/commission/slippage required;
- minimum five years required for qualification;
- OOS split fixed before execution;
- no optimization.

**3.1.2 PROTOCOL — PASS.**

## 8. EXECUTION STATUS

Actual baseline execution is **BLOCKED**.

Reason: the accessible GitHub context does not provide a verified five-year execution dataset plus the execution environment needed to identify the first admissible `t+1` price and realistic transaction costs. The B05 one-month corpus cannot substitute for the five-year gate.

No partial, synthetic, or fabricated backtest was executed.

## 9. NEXT ACTION — EXACTLY ONE

**Rendre accessible le dataset d'exécution multi-années qualifié (≥5 ans) et l'environnement d'exécution permettant de calculer le prix admissible de `t+1` et les coûts réels, puis exécuter le baseline 3.1.2 sans modifier le protocole.**

No other qualification block is reopened. No B02–B08 rerun. No B09.7 rerun.
