# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 05 membership qualification

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Global calendar: **111 candidates / 37 resolved / 74 unresolved / 0 FAIL**
- Execution-window candidate: **68 candidates / 14 resolved / 54 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Attempt-aware recovery progression contract: **PASS**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — integrated**
- Recovery Batch 04: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL — atomically integrated**
- Recovery Batch 05 membership policy: **PASS — frozen before observation**
- Historical attempt ledger entries: **20**
- Registered material capability changes: **0**
- Attempted BLOCKED / currently execution-ineligible: **6**
- Currently execution-eligible unresolved: **48**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened, or lengthened to avoid unresolved dates.

Batch 05 membership qualification is scheduling/governance only. It did not change executable calendar evidence, attempt history, capability identity, or coverage accounting.

## Persisted executable calendar state

The execution-window candidate contains exactly **14** resolved dates:

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
6. `2022-02-21 — PRESIDENTS_DAY`
7. `2022-05-30 — MEMORIAL_DAY`
8. `2022-06-20 — JUNETEENTH_OBSERVED`
9. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
10. `2022-09-05 — LABOR_DAY`
11. `2022-11-24 — THANKSGIVING_DAY`
12. `2022-11-25 — THANKSGIVING_FRIDAY`
13. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
14. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

Global coverage remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

`BLOCKED` remains unresolved. Empty/no-record responses and cross-date overlaps MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Attempt-aware progression after Batch 04 integration

Current deterministic state remains:

- calendar unresolved: **54**
- historical attempts: **20**
- registered material capability changes: **0**
- attempted BLOCKED / execution-ineligible: **6**
- execution-eligible unresolved: **48**
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

The six same-capability attempted BLOCKED dates remain unresolved but execution-ineligible:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Each is classified:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

No retry is authorized without a separately qualified material capability change addressing the exact blocker.

## Batch 04 closure retained

Batch 04 remains fully closed through independent adjudication, atomic integration and persisted-HEAD re-break.

Authoritative references:

- `reports/data-qualification/historical_trading_breaks_recovery_batch04_qualification.md`
- `reports/data-qualification/historical_trading_breaks_recovery_batch04_integration_qualification.md`
- `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH04-INTEGRATION-PASS.md`

The independent persisted-HEAD proof remains:

- verified commit: `9ad19ede0052f37ce8aa2ccd30a117cd0525bc10`
- workflow run: `34897126921`
- job: `104153918828`
- conclusion: **SUCCESS**
- regression: **139 passed in 0.73s**
- exact persisted calendar / ledger / progression assertion: **PASS**
- `git diff --exit-code`: **PASS**

## Batch 05 membership qualification

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY_V1`

Freeze baseline HEAD:

`601310a55b64233ada9e481d3cb2f11dc20a30d5`

Selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Fixed batch size:

`BATCH_SIZE = 5`

Authoritative frozen membership:

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

The membership was mechanically proven to equal persisted post-Batch04:

`eligible_recovery_queue()[:5]`

Raw `recovery_queue()[:5]` was explicitly rejected as a selection source.

Authoritative membership qualification:

- workflow run: `34942590738`
- job: `104294478304`
- trigger commit: `71d33ea99b83a03f1ed916f447b95e24b9059b3b`
- conclusion: **SUCCESS**
- adversarial/regression suite: **94 passed in 0.33s**
- exact eligible-prefix assertion: **PASS**
- no-browser/no-probe guard: **PASS**

Verdict:

**PASS — `BATCH05_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

No Playwright/Chromium dependency was installed or opened during this qualification. No historical Batch 05 broker observation occurred.

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch05_policy_qualification.md`

The completed policy workflow is archived to `workflow_dispatch` only.

## Batch 05 immutability boundary

From this point onward, Batch 05 membership is historical frozen scope.

At execution/adjudication time it MUST come from `tools.trading_breaks_recovery_batch05.batch05_targets()` / `FROZEN_BATCH05_TARGETS`.

It MUST NOT be recalculated from a live queue after outcomes or later state changes occur.

The five frozen dates remain unresolved until independent broker observation and adjudication produce admissible evidence.

## Current boundary decisions

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_CONTRACT`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_EXECUTION_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Execute the already-frozen Batch 05 membership under the qualified Trading Breaks capture chain, with all parent/progression/Batch05 gates passing before Chromium opens, then independently adjudicate all five results.**

Execution MUST use exactly the five frozen members above. Membership MUST NOT be recalculated at execution time.

No `.bi5` acquisition. No real backtest.
