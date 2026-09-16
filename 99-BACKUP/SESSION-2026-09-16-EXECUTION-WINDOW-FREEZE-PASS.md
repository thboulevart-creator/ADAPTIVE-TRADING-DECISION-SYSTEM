# SESSION BACKUP — 2026-09-16 — EXECUTION WINDOW FREEZE PASS

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Recovery rule

GitHub is the source of truth. Re-read `04-REFERENCE/AI-OPERATING-MEMORY.md`, the current checkpoint, this backup and the freeze qualification report before continuing.

## Qualified persisted freeze HEAD

`1662a671d70a63b5afb62b01cf821de7da10051c`

## Durable freeze verdict

**PASS — `EXECUTION_WINDOW_DURABLY_FROZEN_FROM_QUALIFIED_EVIDENCE`**

Frozen outer execution window:

`2021-08-14 → 2026-08-14`

Persisted contract/artifact:

- contract: `EXECUTION_WINDOW_FREEZE_V1`
- artifact: `04-REFERENCE/EXECUTION-WINDOW-FREEZE.json`
- verifier: `tools/frozen_execution_window.py`
- adversarial tests: `tests/test_frozen_execution_window.py`

## Upstream P0.1 evidence

P0.1 qualified HEAD:

`bdee1cde6bc261c34f8584b2a3ec0ec460c7f898`

P0.1 proves the `BoundaryState` is derived from versioned evidence and rejects stale, moved, incomplete, inconsistent or forged boundary inputs.

P0.1 runs:

- Full Suite Regression: `35126075513`
- Persisted-HEAD re-break: `35126075438`

Freeze eligibility from P0.1:

`PASS — EXECUTION_WINDOW_ADMISSIBLE_WITH_OUTSIDE_GAPS_PRESERVED`

## Freeze implementation path

Initial implementation commit:

`5ef0b4b66c2414bb0c022d714dfae389247e50c3`

Initial full-suite result:

`1 failed / 684 passed`

The only failure was the adversarial harness using `CurrentFreezeEvaluation` from the wrong module. Freeze logic and persisted artifact were not defective.

Correction commit:

`1662a671d70a63b5afb62b01cf821de7da10051c`

The correction changed only the adversarial test import/constructor.

## Final proof

### Full Suite Regression

- run/job: `35129069078 / 104905242593`
- SHA: `1662a671d70a63b5afb62b01cf821de7da10051c`
- result: `685 passed in 17.96s`
- success
- worktree clean
- read-only contents permission

### P0 Full Suite Persisted HEAD Rebreak

- run/job: `35129069133 / 104905242777`
- SHA: `1662a671d70a63b5afb62b01cf821de7da10051c`
- exact persisted-HEAD checkout PASS
- historical manifest `115 node IDs / 42 files` PASS
- result: `685 passed in 16.40s`
- success
- worktree clean
- read-only contents permission

## Frozen facts

### Global envelope

- `111` candidates
- `91` resolved
- `20` unresolved
- `0` FAIL
- global coverage remains **BLOCKED**

### Frozen window

- `68` candidates
- `68` resolved
- `0` unresolved
- `0` FAIL
- first open slot: `2021-08-15T22:00:00+00:00`
- last open slot: `2026-08-14T20:00:00+00:00`
- warm-up: `20 H1`
- exact OOS split remains a separate pre-run freeze obligation.

## Explicit non-authorizations

The freeze does not authorize data acquisition or execution.

- `.bi5` massive acquisition: **NOT AUTHORIZED**
- acquisition verdict: **BLOCKED — `MANDATORY_WINDOW_GATES_NOT_PASS`**
- acquisition protocol readiness: not qualified by this block
- explicit acquisition authorization: NO
- real backtest: **NOT AUTHORIZED**
- global coverage PASS: NO

No broker probe, `.bi5` download, Strategy Tester run or real backtest was executed in this block.

## Next action — exactly one

**P0.2 — create `integration/system-v1` from `main` and perform the first controlled import of the already-qualified `feat/decision-producer-contract` block while preserving the complete governance corpus, then independently re-break the imported Tier-A boundaries before importing multi-year work.**

Do not blind-merge.  
Do not acquire `.bi5`.  
Do not run a real backtest.
