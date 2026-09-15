# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 07 execution + independent adjudication PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 46 resolved / 65 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 23 resolved / 45 unresolved / 0 FAIL**
- Historical Trading Breaks broker-evidence route: **PASS**
- Attempt-aware recovery progression: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — integrated**
- Recovery Batch 04: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL — integrated + persisted-HEAD re-break PASS**
- Recovery Batch 05: **PASS — 5 PASS / 0 BLOCKED / 0 FAIL — integrated + persisted-HEAD re-break PASS**
- Recovery Batch 06: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — integrated + persisted-HEAD re-break PASS**
- Recovery Batch 07 membership: **PASS — immutable and frozen before observation**
- Recovery Batch 07 execution/adjudication: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL — NOT YET INTEGRATED**
- Persisted attempt ledger: **30** — pre-Batch07 integration
- Registered material capability changes: **0**
- Persisted attempted BLOCKED / execution-ineligible: **7** — pre-Batch07 integration
- Persisted execution-eligible unresolved: **38 — STALE FOR FUTURE SCHEDULING UNTIL BATCH07 INTEGRATION**
- Current capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- Capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`; it must not be moved, shortened, or lengthened to avoid unresolved dates.

## Batch 07 immutable membership

1. `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`
2. `2023-12-25 — CHRISTMAS_OBSERVED`
3. `2024-01-01 — NEW_YEARS_OBSERVED`
4. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
5. `2024-02-19 — PRESIDENTS_DAY`

Selection rule at freeze:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Membership source:

`eligible_recovery_queue()[:5]`

The historical membership is immutable and must never be recalculated from current state after observation.

## Batch 07 authoritative browser execution — PASS

Execution workflow:

`.github/workflows/trading-breaks-recovery-batch07.yml`

Authoritative execution:

- run: `34958083459`
- job: `104344855871`
- trigger/probe commit: `3d434dda9bd293d48cbe2f35df3d464abd5938a4`
- runtime persistence commit: `071c2240dc6205ee8ffc6b8a0dbd7f2bc08a8632`
- artifact ID: `10392510730`
- artifact SHA-256: `0df18b4bfcae04c0bf5e3670e789fc1253fde7317a50d108b35e10dd1cc2676a`
- artifact files: `31`
- pre-browser parent/progression/Batch07 suite: **207 passed in 0.91s**
- exact frozen execution identity before Chromium: **PASS**
- no live membership recalculation before Chromium: **PASS**
- Chromium installation occurred only after every pre-browser gate passed
- conclusion: **SUCCESS**

Runtime report:

`reports/data-qualification/historical_trading_breaks_recovery_batch07_runtime.json`

## Batch 07 independent adjudication — PASS

Adjudicator:

`tools/trading_breaks_recovery_batch07_adjudication.py`

Adversarial tests:

`tests/test_trading_breaks_recovery_batch07_adjudication.py`

Authoritative independent adjudication:

- run: `34958613649`
- job: `104346566865`
- trigger commit: `8ad831104f1d00ba049f458b1db772b316b44ebe`
- adjudication persistence commit: `2551595485923931cd47028cbc741f2f5580b6c3`
- adversarial/regression suite: **120 passed in 0.30s**
- runtime ancestry and immutability gate: **PASS**
- exact final accounting assertion: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- no-browser/no-probe/no-live-queue adjudication guard: **PASS**

Final verdict:

**PASS — `BATCH07_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Evidence:

- `reports/data-qualification/historical_trading_breaks_recovery_batch07_adjudication.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch07_qualification.md`

### Date-level outcomes

1. `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - record `63023`
   - start `2023-12-22T21:14:00Z`
   - final closed instant `2023-12-25T22:59:00Z`
   - calibrated reopen `2023-12-25T23:00:00Z`
   - target-day whole closed UTC hours: `22–23`
   - partial hour `21` remains open.

2. `2023-12-25 — CHRISTMAS_OBSERVED`
   - **BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**
   - overlap witness record `63023`
   - record starts `2023-12-22T21:14:00Z`, not on the exact target date
   - the overlap must not be promoted to exact-target PASS.

3. `2024-01-01 — NEW_YEARS_OBSERVED`
   - **BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**
   - overlap witness record `63024`
   - record starts `2023-12-29T21:14:00Z`, not on the exact target date
   - the overlap must not be promoted to exact-target PASS.

4. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - record `63883`
   - start `2024-01-15T18:00:00Z`
   - final closed instant `2024-01-15T22:59:00Z`
   - reopen `2024-01-15T23:00:00Z`
   - whole closed UTC hours: `18–22`.

5. `2024-02-19 — PRESIDENTS_DAY`
   - **PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**
   - record `65120`
   - start `2024-02-19T18:00:00Z`
   - broker final closed instant `2024-02-19T22:59:59Z`
   - calibrated reopen under the existing protocol `2024-02-19T23:00:59Z`
   - whole closed UTC hours: `18–22`
   - second precision is retained; it is not silently rounded.

Only the three PASS dates are authorized for future executable calendar integration. The two BLOCKED dates must remain unresolved and must not populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Pre-integration state invariant

The five Batch 07 factual executions have occurred, but calendar/attempt-ledger/progression state has **not** yet been atomically integrated.

Therefore:

- do not freeze Batch 08 from the current persisted eligible queue;
- do not treat the persisted `38` eligible count as authoritative for future scheduling;
- do not rerun Batch 07 merely because integration is pending;
- do not add only the three PASS records without also recording all five factual attempts;
- `2023-12-25` and `2024-01-01` must remain unresolved after integration and become same-capability execution-ineligible unless a separately qualified material capability change later addresses their blocker.

Current persisted counts remain pre-integration:

- global: `111 / 46 resolved / 65 unresolved / 0 FAIL`;
- execution window: `68 / 23 resolved / 45 unresolved / 0 FAIL`;
- attempt ledger: `30`;
- material capability changes: `0`;
- attempted BLOCKED / execution-ineligible: `7`;
- eligible unresolved: `38` — **stale for scheduling**.

## Workflow closure

Batch 07 execution workflow archived to `workflow_dispatch` only:

`3719d6d02e06913b4037f073d329328b985d8e63`

Batch 07 adjudication workflow archived to `workflow_dispatch` only:

`b05f1a7ef8a1b430d7a2ef4a48c35fe5fad48d91`

No normal push may silently repeat completed Batch 07 browser execution or adjudication.

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_EXECUTION_ADJUDICATION`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

PENDING/BLOCKED downstream:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_INTEGRATION — NOT_YET_APPLIED`
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Atomically integrate Batch 07: add only the three independently adjudicated PASS records to executable calendar evidence, record all five factual Batch 07 attempts in the immutable attempt ledger, leave `2023-12-25` and `2024-01-01` unresolved, regenerate attempt-aware progression, adversarially rerun calendar/coverage/progression regressions, then independently re-break the persisted HEAD before any Batch 08 freeze.**

No `.bi5`. No real backtest.
