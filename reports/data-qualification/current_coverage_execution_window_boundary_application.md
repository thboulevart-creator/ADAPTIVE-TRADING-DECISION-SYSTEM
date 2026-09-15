# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 06 membership qualification PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 42 resolved / 69 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 19 resolved / 49 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Attempt-aware progression: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — integrated**
- Recovery Batch 04: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL — integrated + persisted-HEAD re-break PASS**
- Recovery Batch 05: **PASS — 5 PASS / 0 BLOCKED / 0 FAIL — atomically integrated + persisted-HEAD re-break PASS**
- Recovery Batch 06 membership: **PASS — frozen before observation**
- Recovery Batch 06 execution/adjudication: **NOT YET PERFORMED**
- Historical attempt ledger entries: **25**
- Registered material capability changes: **0**
- Attempted BLOCKED / execution-ineligible: **6**
- Execution-eligible unresolved: **43**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 05 integrated boundary

Batch 05 remains fully closed and integrated:

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

Authoritative integration:

- workflow run: `34949197265`
- job: `104315829990`
- atomic integration commit: `99c2f38842a0c4ea66ba6ff90496380986d02e52`
- pre-mutation suite: `76 passed`
- post-mutation suite: `166 passed`

Corrected independent persisted-HEAD re-break:

- workflow run: `34949499981`
- job: `104316813519`
- verified commit: `70428e536689793a74420d35c84744b8ad0f2f3d`
- adversarial regression: `166 passed in 0.99s`
- exact persisted state: PASS
- no-browser/no-capture guard: PASS
- deterministic progression regeneration + `git diff --exit-code`: PASS

The earlier persisted-head run `34949393807` / job `104316469582` failed only because its guard searched for forbidden strings present in its own literals. The 166 tests and exact persisted-state assertion had already passed; the corrected guard then passed without changing executable state.

## Persisted progression state after Batch 05

- calendar unresolved in execution window: **49**
- attempt ledger: **25**
- registered material capability changes: **0**
- attempted BLOCKED / execution-ineligible: **6**
- execution-eligible unresolved: **43**
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

The six historical same-capability BLOCKED dates remain unresolved and execution-ineligible:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Each remains `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`.

## Batch 06 immutable membership — PASS

Batch 06 was mechanically frozen from the persisted post-Batch05:

`eligible_recovery_queue()[:5]`

with fixed `BATCH_SIZE = 5` and selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Frozen membership:

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
3. `2023-09-04 — LABOR_DAY`
4. `2023-11-23 — THANKSGIVING_DAY`
5. `2023-11-24 — THANKSGIVING_FRIDAY`

Freeze provenance:

- pre-freeze checkpoint: `289d7f4432efba4ad2bc1e97d5b23f14f587019e`
- source post-Batch05 atomic integration/progression commit: `99c2f38842a0c4ea66ba6ff90496380986d02e52`
- source post-Batch05 persisted-head re-break: `70428e536689793a74420d35c84744b8ad0f2f3d`
- freeze module creation: `2cfd7d8c82cc12ce5904a60ed0720cd17ec15efd`

All five are unresolved, chronologically ordered, unique, `INITIAL_ATTEMPT`, execution-eligible, and absent from the attempt ledger before freeze.

Raw `recovery_queue()[:5]` is explicitly inadmissible because it contains already-attempted same-capability BLOCKED dates.

## Batch 06 adversarial membership qualification

First qualification run:

- workflow run: `34951530594`
- job: `104323377439`
- trigger commit: `0aec58ccab9222b0e86c401b156a9cb965e1c974`
- result: `96 passed / 1 failed`

The only failure was a guard false positive. The source guard searched for the bare substring `eligible_recovery_queue`, which appeared only inside the immutable metadata string `FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`. No live queue call existed in the freeze module.

Minimal test-only correction:

`3ce94bb8c586fe4472ccf37d2a849f87bd9c03ef`

Corrected authoritative qualification:

- workflow run: `34951726033`
- job: `104324020570`
- trigger commit: `6a85c1c4c7d8c38861626b3eb8367274f015d118`
- conclusion: **SUCCESS**
- adversarial/regression suite: **97 passed in 0.35s**
- exact `batch06_targets() == eligible_recovery_queue()[:5]` assertion: **PASS**
- governed-state immutability since checkpoint: **PASS**
- no-browser/no-probe path: **PASS**
- read-only `git diff --exit-code`: **PASS**
- token permissions: `contents: read`, `metadata: read`

Final membership verdict:

**PASS — `BATCH06_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch06_policy_qualification.md`

The qualification attacks skip, reorder, substitution, raw-queue bypass, batch-size drift, reinsertion of BLOCKED dates, re-entry of Batch 05 PASS dates, caller mutation/selection surfaces, prior-attempt contamination, semantic-capability/progression drift, and outcome/manual/source-based selection.

## Browser and mutation boundary

No Batch 06 browser observation has occurred.

The freeze module contains no Playwright, Chromium, `probe_candidate`, asyncio, live `eligible_recovery_queue()` call or live `recovery_queue()` call. The qualification installed pytest only.

Batch 06 membership PASS is scheduling/governance only. Therefore it did **not**:

- resolve any date;
- modify `SPECIAL_SESSION_EVIDENCE` or negative evidence;
- append attempts;
- change semantic capability;
- regenerate or alter progression state;
- change calendar/coverage counts.

The Batch 06 policy qualification workflow is archived to `workflow_dispatch` only after completion. Historical membership may not be silently re-frozen on normal pushes.

## Current boundary decisions

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_CONTRACT`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_EXECUTION_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_POLICY`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Execute exactly the five already-frozen Batch 06 dates under the qualified Trading Breaks capture chain, with parent protocol/progression/Batch06 gates PASS before Chromium opens, then independently adjudicate all five results.**

At execution time membership MUST come from immutable `batch06_targets()`. It MUST NOT be recalculated from live `eligible_recovery_queue()` or raw `recovery_queue()`.

No `.bi5`. No real backtest.
