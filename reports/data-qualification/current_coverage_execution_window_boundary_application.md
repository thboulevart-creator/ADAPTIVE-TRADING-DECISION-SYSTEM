# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 06 execution + independent adjudication PASS

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
- Recovery Batch 06 execution/adjudication: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — NOT YET INTEGRATED**
- Historical attempt ledger entries persisted: **25** (pre-Batch06 integration)
- Registered material capability changes: **0**
- Persisted attempted BLOCKED / execution-ineligible: **6** (pre-Batch06 integration)
- Persisted execution-eligible unresolved: **43** — **STALE FOR FUTURE SCHEDULING UNTIL BATCH06 INTEGRATION**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 06 immutable membership

Frozen membership:

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
3. `2023-09-04 — LABOR_DAY`
4. `2023-11-23 — THANKSGIVING_DAY`
5. `2023-11-24 — THANKSGIVING_FRIDAY`

Selection rule at freeze:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

The membership is immutable. It MUST NOT be recalculated, substituted, reordered, expanded or shortened after observation.

## Batch 06 authoritative browser execution

Execution workflow:

`.github/workflows/trading-breaks-recovery-batch06.yml`

Authoritative run:

- workflow run: `34954308324`
- job: `104332522379`
- probe/trigger commit: `e968db2be1fbfd4d2c419f9dad717ca479b52edd`
- runtime persistence commit: `b50529991d9af6e27170090bd45b42eb751d0958`
- artifact: `10390926878`
- artifact SHA-256: `1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052`
- artifact files: `31`
- pre-browser adversarial/regression suite: `170 passed in 0.72s`
- exact frozen Batch 06 execution identity before Chromium: **PASS**
- no live membership recalculation before Chromium: **PASS**
- conclusion: **SUCCESS**

Chromium/Playwright was installed only after every checkpoint, parent protocol, progression and Batch06 membership gate had passed.

Runtime evidence:

`reports/data-qualification/historical_trading_breaks_recovery_batch06_runtime.json`

## Batch 06 independent adjudication — PASS

Independent adjudication workflow:

`.github/workflows/trading-breaks-recovery-batch06-adjudication.yml`

Authoritative run:

- workflow run: `34954764562`
- job: `104334032049`
- trigger commit: `44bac8e3ebb8c783d02295f052fe17c86c222049`
- adjudication persistence commit: `874f8fe2c809d1f3c1442ba61aaabb4056a03e3d`
- adversarial/regression suite: `114 passed in 0.36s`
- runtime ancestry and immutability gate: **PASS**
- no-browser/no-probe/no-live-queue adjudication guard: **PASS**
- exact final accounting assertion: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL**

Final verdict:

**PASS — `BATCH06_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Adjudication evidence:

- `reports/data-qualification/historical_trading_breaks_recovery_batch06_adjudication.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch06_qualification.md`

### Date-level outcomes

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - broker record `56233`
   - start `2023-07-03T17:14:00Z`
   - final closed minute `2023-07-04T21:59:00Z`
   - reopen `2023-07-04T22:00:00Z`
   - target-day whole closed UTC hours: `18–23`
   - hour `17` remains open because the closure starts at `17:14Z`.

2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
   - **BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**
   - overlap witness: broker record `56233`
   - record starts `2023-07-03T17:14:00Z`, not on the exact target date
   - the overlap is retained as evidence of why adjudication is blocked, but MUST NOT be promoted to exact-target PASS.

3. `2023-09-04 — LABOR_DAY`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - broker record `57462`
   - start `2023-09-04T16:59:00Z`
   - final closed minute `2023-09-04T21:59:00Z`
   - reopen `2023-09-04T22:00:00Z`
   - whole closed UTC hours: `17–21`.

4. `2023-11-23 — THANKSGIVING_DAY`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - broker record `59358`
   - start `2023-11-23T16:59:00Z`
   - final closed minute `2023-11-23T22:59:00Z`
   - reopen `2023-11-23T23:00:00Z`
   - whole closed UTC hours: `17–22`.

5. `2023-11-24 — THANKSGIVING_FRIDAY`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - broker record `59359`
   - start `2023-11-24T17:14:00Z`
   - final closed minute `2023-11-26T22:59:00Z`
   - reopen `2023-11-26T23:00:00Z`
   - only target-day whole closed UTC hours are projected: `18–23`
   - hour `17` remains open and the weekend continuation is not promoted to another target date.

Only the four PASS records are authorized for future executable calendar integration. The `2023-07-04` BLOCKED outcome MUST remain unresolved and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Pre-integration state invariant

The five Batch 06 factual executions have occurred, but they have **not yet been atomically integrated** into the attempt ledger/calendar/progression state.

Therefore:

- do NOT freeze Batch 07 from the current persisted `eligible_recovery_queue()`;
- do NOT treat the persisted `43` eligible count as authoritative for future scheduling;
- do NOT rerun Batch 06 merely because integration is pending;
- do NOT integrate calendar PASS records separately from recording all five factual attempts;
- `2023-07-04` must remain unresolved after integration and become same-capability execution-ineligible unless a separately qualified material capability change later addresses its blocker.

Current persisted counts remain mechanically pre-integration:

- global: `111 / 42 resolved / 69 unresolved / 0 FAIL`;
- execution window: `68 / 19 resolved / 49 unresolved / 0 FAIL`;
- attempt ledger: `25`;
- material capability changes: `0`;
- attempted BLOCKED / execution-ineligible: `6`;
- eligible unresolved: `43` (stale for scheduling).

## Workflow closure

Batch 06 execution workflow archived to `workflow_dispatch` only:

`224a4f99daf4fce09f7c07759a8fd89f4aa2b77a`

Batch 06 adjudication workflow archived to `workflow_dispatch` only:

`285d94e11a7887d1cc62858390c4c29752ef5588`

No normal push may silently repeat completed Batch 06 browser execution or adjudication.

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_EXECUTION_ADJUDICATION`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

PENDING/BLOCKED downstream:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_INTEGRATION — NOT_YET_APPLIED`
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Atomically integrate Batch 06: add only the four independently adjudicated PASS records to executable calendar evidence, record all five Batch 06 factual attempts in the immutable attempt ledger, regenerate attempt-aware progression, then adversarially rerun and persist the required calendar/coverage/progression regressions followed by an independent persisted-HEAD re-break.**

Required semantics:

- integrate PASS only: `2023-07-03`, `2023-09-04`, `2023-11-23`, `2023-11-24`;
- do **not** integrate `2023-07-04` as resolved;
- record all five factual attempts;
- after attempt recording, `2023-07-04` must be `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED` and remain unresolved;
- no Batch 07 membership freeze until Batch 06 integration and persisted-HEAD re-break are PASS.

No `.bi5`. No real backtest.
