# Execution Window Freeze Qualification — PASS

**Date:** 16 septembre 2026  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `feat/multi-year-dukascopy-acquisition`  
**Qualified persisted HEAD:** `1662a671d70a63b5afb62b01cf821de7da10051c`  
**Contract:** `EXECUTION_WINDOW_FREEZE_V1`  
**Verdict:** **PASS — `EXECUTION_WINDOW_DURABLY_FROZEN_FROM_QUALIFIED_EVIDENCE`**

## 1. Object

This report closes the durable freeze of the primary execution window selected and qualified by the existing governed contracts.

Frozen window:

`2021-08-14 → 2026-08-14`

The freeze is not a declaration-only boolean. It is persisted in `04-REFERENCE/EXECUTION-WINDOW-FREEZE.json` and revalidated fail-closed by `tools/frozen_execution_window.py` against the current evidence-derived `BoundaryState`.

No `.bi5` acquisition, broker probe, Strategy Tester run, or real backtest occurred in this block.

## 2. Upstream P0.1 qualification

The freeze is bound to the P0.1 evidence-derived boundary qualification:

- P0.1 qualified HEAD: `bdee1cde6bc261c34f8584b2a3ec0ec460c7f898`
- Full Suite Regression: run `35126075513`
- Persisted-HEAD re-break: run `35126075438`
- boundary derivation contract: `CURRENT_EXECUTION_WINDOW_BOUNDARY_STATE_DERIVATION_V1`
- boundary contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`
- selection rule: `EXECUTION_WINDOW_SELECTION_RULE_V1`
- eligibility verdict: `PASS`
- eligibility reason: `EXECUTION_WINDOW_ADMISSIBLE_WITH_OUTSIDE_GAPS_PRESERVED`

P0.1 derives the boundary from versioned evidence rather than caller-supplied eligibility booleans.

## 3. Frozen facts

### Global coverage truth preserved

- candidates: `111`
- resolved: `91`
- unresolved: `20`
- global coverage PASS: **NO**
- global coverage remains **BLOCKED**

The freeze does not erase or reclassify the 20 unresolved candidates outside the execution window.

### Frozen execution window

- start: `2021-08-14`
- end: `2026-08-14`
- candidates: `68`
- resolved: `68`
- unresolved: `0`
- FAIL: `0`
- first included open slot: `2021-08-15T22:00:00+00:00`
- last included open slot: `2026-08-14T20:00:00+00:00`
- warm-up: `20` completed H1 bars
- OOS split policy: `DEFERRED_TO_RUN_BY_VERSIONED_MOMENTUM_V1_PROTOCOL`

The outer execution window is now durably frozen. The exact OOS split remains a separate future pre-run obligation and may not be moved after results are observed.

## 4. Fail-closed freeze mechanism

Persisted artifact:

`04-REFERENCE/EXECUTION-WINDOW-FREEZE.json`

Verifier:

`tools/frozen_execution_window.py`

Adversarial tests:

`tests/test_frozen_execution_window.py`

The verifier rejects or blocks at minimum:

- altered start or end date;
- altered global unresolved count;
- altered P0.1 source HEAD;
- disappearance of current freeze eligibility;
- a current boundary regression;
- an attempt by the freeze artifact to self-authorize massive acquisition;
- mismatch between the freeze artifact and current derived evidence.

The public freeze derivation accepts no caller-supplied window or freeze record.

## 5. Acquisition remains separate and blocked

The frozen `BoundaryState` sets:

- `execution_window_frozen=True`
- `mandatory_window_gates_pass=False`
- `acquisition_protocol_ready=False`
- `explicit_acquisition_authorization=False`

Therefore evaluation of `AUTHORIZE_MASSIVE_ACQUISITION` remains:

**BLOCKED — `MANDATORY_WINDOW_GATES_NOT_PASS`**

The persisted artifact also explicitly records:

- `massive_acquisition_authorized=false`
- `real_backtest_authorized=false`

No acquisition or backtest authorization can be inferred from this freeze PASS.

## 6. First adversarial execution and correction

Initial freeze implementation commit:

`5ef0b4b66c2414bb0c022d714dfae389247e50c3`

The first complete suite produced:

`1 failed / 684 passed`

The sole failure was in the adversarial test harness itself: the test attempted to instantiate `CurrentFreezeEvaluation` through `tools.frozen_execution_window`, while the class is defined in `tools.current_execution_window_boundary_state`.

No freeze artifact or production freeze logic was defective.

Correction commit:

`1662a671d70a63b5afb62b01cf821de7da10051c`

The correction changed only the adversarial test import/constructor.

## 7. Final persisted-HEAD proof

### Full Suite Regression

- run/job: `35129069078 / 104905242593`
- HEAD: `1662a671d70a63b5afb62b01cf821de7da10051c`
- result: **`685 passed in 17.96s`**
- conclusion: success
- worktree: clean
- permissions: `contents: read`, `metadata: read`

### P0 Full Suite Persisted HEAD Rebreak

- run/job: `35129069133 / 104905242777`
- exact HEAD checkout: PASS
- historical baseline manifest `115 node IDs / 42 files`: PASS
- result: **`685 passed in 16.40s`**
- conclusion: success
- worktree: clean
- permissions: `contents: read`, `metadata: read`

Both independent gates qualified the same persisted SHA.

## 8. Verdict

**PASS — `EXECUTION_WINDOW_DURABLY_FROZEN_FROM_QUALIFIED_EVIDENCE`**

The exact outer execution window `2021-08-14 → 2026-08-14` is durably frozen and machine-verifiable. Global coverage remains BLOCKED at `111/91/20`. Massive `.bi5` acquisition and real backtesting remain unauthorized.

## 9. Next governed action

**P0.2 — create the authoritative integration branch `integration/system-v1` from `main`, then perform the first controlled import of the already-qualified `feat/decision-producer-contract` block while preserving the full governance corpus; re-break the imported critical boundaries on the integration branch before importing multi-year work.**

Do not blind-merge feature branches.  
Do not authorize `.bi5`.  
Do not run a real backtest.
