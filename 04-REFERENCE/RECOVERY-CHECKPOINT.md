# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — POST-RECOVERY

> Versioned durable handoff point for recovery across conversations.
> This checkpoint is authoritative for the current workstream on `feat/v4-3-instrument-contracts`.

## 1. ÉTAT ACTUEL

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Branch:** `feat/v4-3-instrument-contracts`
- **PR:** #8 — draft, unmerged
- **Main baseline:** `ff50b6d5d123969e091b5df18c46d438f7cb8052`
- **Last locked qualification:** B09 — PASS
- **Current research block:** Phase 3 → 3.1 Expert Momentum → **3.1.1 PASS**
- **Current persistence state:** B08-A/B09 production research layer **RECONSTRUCTED AND VERSIONED**
- **Next governed block:** **3.1.2 — Premier backtest baseline**

## 2. RECOVERY ORDER

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/README.md`
4. latest `99-BACKUP/SESSION-YYYY-MM-DD.md`
5. `docs/00-MASTER-EXECUTION-CHECKLIST.md`
6. referenced reports/artifacts
7. actual GitHub/worktree state

Conversation memory is not sufficient source of truth.

## 3. LOCKED QUALIFICATION — DO NOT RERUN

B02, B03/B03.1/B03.2/B03.3 historical states, B02', B03.1', B04, B05, B06-A, B07-A, B07-B, B06-B, B08, B08-A, B08-B.1, B09.0.1, B09.1, B09.2, B09.3, B09.4 historical BLOCKED, B09.5, B09.6, B09.7 synthetic, B09.7 full-stream, B09 `run()` exposure closure, and B09 final remain locked historical qualification results.

**Explicit prohibition:** do not rerun B02–B08 or B09.7 merely to reconstruct memory.

## 4. IMPORTANT IDENTITIES

- B05 corpus SHA256: `868a21c6a1bedf095b30bc64b6c2ef60b5db9d30146ac53034360254413f8ad7`
- B05 contract SHA256: `49e272534bf5061522eb624afe4e27d6585f730e0271b5284bff2442d5c04b07`
- Historical B08 stream SHA256: `4768c0e66647a15ba703d2dcdc88c03db84846a625e8eb3f70914428bf11c8d7`
- B09 canonical stream SHA256: `d8da494b2a1380ea0db0e0370ece4f609374ecb3e5647b6c1fb290836867abda`
- Corpus: `C:\ALGO-DATA\qualification\v4_3_multi_year_acquisition\candidate_b03_3_repaired\USATECHIDXUSD`
- Physical files: 495
- Full stream: 5,130,393 ticks

## 5. 3.1.1 — MOMENTUM V1 LOCKED PASS

- H1 / Close / horizon 20
- `M_t = Close_t / Close_{t-20} - 1`
- positive → LONG; negative → SHORT; zero → NEUTRE
- insufficient history → UNDEFINED
- computed at close of `t`, usable from `t+1`
- no regime filter; no massive optimization
- directional signal only; risk/SL/TP/execution outside definition

**3.1.1 PASS validates the formal definition only. It does not validate profitability, robustness, economic value, or regime superiority.**

Persisted artifacts:
- `docs/03.1.1-MOMENTUM-V1-DEFINITION.md` — `b98f4e547e09b31b3b45efc22705238c15ffdbb7`
- `reports/research/3_1_1_momentum_v1_adversarial_report.md` — `14d6274f8f4ab30fccef6ca41190ffc0894b57c6`

## 6. B08-A/B09 PERSISTENCE INCIDENT — RESOLVED BY CONTROLLED RECONSTRUCTION

### Historical recovery result

The four historical production files were exhaustively checked against the accessible GitHub branch/history and were **NOT FOUND**:

- `src/research/input_binding.py`
- `src/research/bi5_reader.py`
- `src/research/engine.py`
- `src/research/execution.py`

The exact Windows worktree previously used was known as:
`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM-PR8-TEST`

That filesystem is not accessible from the current execution environment, so no claim of local recovery is made.

### Controlled replacement

Per the durable recovery rule, the missing implementation was replaced by a **controlled reconstruction from persistent architectural evidence**.

**RECONSTRUCTION ≠ RÉCUPÉRATION.**

The reconstruction preserves the known architecture:

- `BoundResearchInput` is immutable and is created only by `bind_execution_input()`.
- `BI5ResearchEngine` accepts only `BoundResearchInput`.
- official path: `run_qualified_research()` → binding → engine → `iter_ticks()`.
- BI5 reader performs no silent sort, deduplication, repair, interpolation or substitution of ticks.
- deterministic file ordering is allowed/required; duplicate hours are rejected.
- global tick monotonicity is enforced on the iterator path.
- production stream hashing uses exact IEEE-754 `struct.pack(">d", value)` for numeric fields.
- `run()` is retained only as a compatibility helper and is not the qualification entrypoint.

### Reconstruction artifacts

- `src/research/input_binding.py` — commit `fad72675f2e7ee44083b0cbc89910d8786829f4c`
- `src/research/bi5_reader.py` — commit `74005e2751782d91436d793ca9dc58c224bfe5f5`
- `src/research/engine.py` — commit `63d98f1a8e8829143260b2a81fbb14f821c5be66`
- `src/research/execution.py` — commit `eca03288338e6142ad5c23c400d18dab7e560e9b`
- `src/research/__init__.py` — commit `800aaab8a0e908ae2efbf719545d5ce34d7b53f9`

These commits prove versioning of the reconstructed replacement, not identity with the lost historical source.

### Qualification status of reconstruction

The reconstruction is **not** automatically certified as B08-A/B09 revalidated code. Historical B08-A/B09 PASS results remain locked as historical evidence; the reconstructed source now requires its own focused code-level verification before being treated as current executable evidence.

No B02–B08 or B09.7 rerun is authorized merely for this purpose.

## 7. BACKUP LAYER

`99-BACKUP/` remains the durable context layer. The session snapshot must be updated whenever material state changes.

Current snapshot: `99-BACKUP/SESSION-2026-09-13.md`.

## 8. NEXT GOVERNED ACTION — EXACTLY ONE

**Formaliser le protocole de `3.1.2 — Premier backtest baseline`, puis le casser adversarialement avant toute exécution.**

The protocol must explicitly fix, before execution:
- dataset and temporal window;
- timeframe and OHLC field used by Momentum V1;
- signal timing `t` → usable `t+1`;
- baseline vs comparison controls;
- transaction/cost assumptions;
- out-of-sample split;
- metrics and acceptance/rejection criteria;
- prohibition on parameter optimization during the baseline;
- reproducibility and evidence artifacts;
- separation between research signal and actual order/execution logic.

No backtest execution occurs until the protocol itself reaches PASS through:
**formalisation → candidate → adversarial break → correction → re-break → verdict.**
