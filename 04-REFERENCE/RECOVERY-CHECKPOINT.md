# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — EXECUTION WINDOW FREEZE PASS / INTEGRATION NEXT

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Source of truth

GitHub code, persisted reports, tests, qualification artifacts and workflow evidence are authoritative. Do not reconstruct state from conversation memory.

Construction rule remains:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

A prior PASS does not authorize the next gate automatically. `BLOCKED` is never `PASS`.

## Calendar / Trading Breaks truth

### Global envelope

- candidates: `111`
- resolved: `91`
- unresolved: `20`
- FAIL: `0`
- global coverage verdict: **BLOCKED**

All 20 unresolved global dates remain preserved and are outside the frozen execution window.

### Frozen execution window

Exact durable window:

`2021-08-14 → 2026-08-14`

- candidates: `68`
- resolved: `68`
- unresolved: `0`
- FAIL: `0`
- first included open slot: `2021-08-15T22:00:00+00:00`
- last included open slot: `2026-08-14T20:00:00+00:00`
- warm-up: `20` completed H1 bars
- OOS exact split: not yet selected; must be frozen separately before execution and cannot move after results are observed.

Persisted freeze contract:

`EXECUTION_WINDOW_FREEZE_V1`

Artifact:

`04-REFERENCE/EXECUTION-WINDOW-FREEZE.json`

Verifier:

`tools/frozen_execution_window.py`

## P0.0 — full-suite historical/current rebaseline CLOSED

Historical regression contract remains:

- schema: `HISTORICAL_REGRESSION_BASELINES_V1`
- historical node IDs: `115`
- historical files: `42`
- manifest: `tests/historical_regression_baselines.json`
- fail-closed replay hook: `tests/conftest.py`

P0.0 verdict remains:

**PASS — `P0_FULL_SUITE_REBASELINE_PERSISTED_HEAD_REBREAK_CONFIRMS_CURRENT_AND_HISTORICAL_REGRESSION_CORPUS`**

Governance contract remains:

`GOVERNANCE_RELAXATION_COOLING_OFF_V1`

## P0.1 — evidence-derived BoundaryState CLOSED

Implementation:

`tools/current_execution_window_boundary_state.py`

Adversarial tests:

`tests/test_current_execution_window_boundary_state.py`

Qualified P0.1 HEAD:

`bdee1cde6bc261c34f8584b2a3ec0ec460c7f898`

Authoritative P0.1 workflow runs:

- Full Suite Regression: `35126075513`
- Persisted-HEAD re-break: `35126075438`

Derived freeze eligibility:

- action: `FREEZE_EXECUTION_WINDOW`
- verdict: **PASS**
- reason: `EXECUTION_WINDOW_ADMISSIBLE_WITH_OUTSIDE_GAPS_PRESERVED`

The derivation is fail-closed against moved boundaries, omitted candidates, hidden unresolved dates, stale reports, global/window mismatch, recovery/progression mismatch and provenance/identity mismatch.

## Durable execution-window freeze — CLOSED

Initial freeze implementation commit:

`5ef0b4b66c2414bb0c022d714dfae389247e50c3`

The first complete suite exposed one adversarial test-harness error only (`1 failed / 684 passed`). The test imported `CurrentFreezeEvaluation` through the wrong module. No freeze artifact or freeze logic defect was observed.

Correction commit / qualified persisted HEAD:

`1662a671d70a63b5afb62b01cf821de7da10051c`

### Final Full Suite Regression

- run/job: `35129069078 / 104905242593`
- HEAD: `1662a671d70a63b5afb62b01cf821de7da10051c`
- result: **`685 passed in 17.96s`**
- worktree: clean
- permissions: read-only

### Final persisted-HEAD re-break

- run/job: `35129069133 / 104905242777`
- exact persisted HEAD checkout: PASS
- baseline manifest `115 / 42`: PASS
- result: **`685 passed in 16.40s`**
- worktree: clean
- permissions: read-only

Freeze verdict:

**PASS — `EXECUTION_WINDOW_DURABLY_FROZEN_FROM_QUALIFIED_EVIDENCE`**

Durable report:

`reports/data-qualification/execution_window_freeze_qualification.md`

## Recovery / progression state preserved

- attempt ledger: `73`
- material capability changes: `1`
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`
- recovery queue: empty
- progression decisions: empty
- eligible recovery queue: empty

## Explicit current prohibitions / non-verdicts

- `DECLARE_GLOBAL_COVERAGE_PASS`: **BLOCKED** (`111 / 91 / 20`)
- execution-window formally frozen: **YES — PASS**
- massive native `.bi5` acquisition: **NOT AUTHORIZED**
- acquisition gate: **BLOCKED — `MANDATORY_WINDOW_GATES_NOT_PASS`**
- acquisition protocol ready: **NO VERDICT / NOT QUALIFIED BY FREEZE**
- explicit acquisition authorization: **NO**
- real backtest: **NOT AUTHORIZED**
- exact OOS split: **NOT YET FROZEN**
- `src/research/ ↔ research_run_evidence` junction: **NOT YET QUALIFIED ON AN AUTHORITATIVE INTEGRATION BRANCH**
- inter-process attestation: **NOT YET QUALIFIED**

## Mandatory recovery order before next substantive write

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-EXECUTION-WINDOW-FREEZE-PASS.md`
4. `reports/data-qualification/execution_window_freeze_qualification.md`
5. `04-REFERENCE/EXECUTION-WINDOW-FREEZE.json`
6. `tools/frozen_execution_window.py`
7. `tools/current_execution_window_boundary_state.py`
8. `tests/test_frozen_execution_window.py`
9. `tests/test_current_execution_window_boundary_state.py`
10. current governance corpus and historical-regression manifest/hook
11. compare active branch HEAD against this checkpoint before any mutation.

## Exactly one next governed action

**P0.2 — create the authoritative integration branch `integration/system-v1` from `main`, then perform the first controlled import of the already-qualified `feat/decision-producer-contract` block while preserving the complete governance corpus; independently re-break the imported Tier-A boundaries before importing the multi-year block.**

Rules for P0.2:

- `main` remains the final authoritative destination; `integration/system-v1` is the controlled integration work branch.
- no blind merge of feature branches;
- governance deletions from feature history must not be replayed;
- import already-qualified blocks in explicit bounded sets;
- critical boundaries inherit Tier A and require independent re-break after import;
- record covered and not-covered governance scope in the audit register;
- do not acquire `.bi5`;
- do not run a real backtest.
