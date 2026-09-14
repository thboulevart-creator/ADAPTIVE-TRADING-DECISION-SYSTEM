# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 04 execution and independent adjudication

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Global calendar: **111 candidates / 34 resolved / 77 unresolved / 0 FAIL**
- Execution-window candidate: **68 candidates / 11 resolved / 57 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Attempt-aware recovery progression contract: **PASS**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL**
- Batch 04 membership policy: **PASS**
- Batch 04 execution/adjudication: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Batch 04 executable integration: **NOT YET APPLIED**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened, or lengthened to avoid unresolved dates.

## Calendar state remains unchanged until Batch 04 atomic integration

The independent Batch 04 adjudication authorizes three exact-target positive records for later integration, but no calendar evidence has yet been mutated in this step. Therefore the current persisted executable calendar still contains exactly **11** resolved in-window dates and **57** unresolved dates.

`BLOCKED` remains unresolved. Empty/no-record results and cross-date overlaps MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

The historical attempt ledger also remains at **15** entries until the next atomic integration step records all five Batch 04 factual attempts together with any authorized calendar additions. Consequently the previously generated live progression projection (`53` eligible unresolved before Batch 04 execution) is now **stale for future scheduling** and MUST NOT be used to freeze Batch 05 before Batch 04 integration is completed.

## Batch 04 frozen membership

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1`

Immutable membership:

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

This membership was frozen and adversarially qualified before observation. Execution and adjudication consumed the frozen tuple only; neither recalculated membership from the live recovery queues.

## Batch 04 authoritative browser execution

Authoritative runtime:

- workflow run: `34895457466`
- job: `104148201341`
- probe commit: `11a81294720898802e49dd1131a64e20e7e7ae3a`
- artifact ID: `10369230708`
- artifact SHA-256: `3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc`
- persisted runtime commit: `2fb64b3857dcbe53f08c9dcabe85669f0eb5c81f`
- pre-browser suite: `110 passed in 0.59s`
- exact frozen identity guard: **PASS**
- no-live-membership-recalculation guard: **PASS**
- browser execution: **SUCCESS**

Chromium was installed and opened only after all pre-browser parent/progression/Batch04 gates passed.

Runtime report:

`reports/data-qualification/historical_trading_breaks_recovery_batch04_runtime.json`

## Batch 04 independent adjudication

Final verdict:

**PASS — `BATCH04_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Adversarial adjudication run:

- workflow run: `34895985689`
- job: `104149952523`
- trigger commit: `e3c40f3bfcd7300bfbe7383c21e4d70c16df783e`
- suite: `81 passed in 0.27s`
- browser-free adjudication guard: **PASS**
- exact final accounting assertion: **PASS**

Date-level verdicts:

1. `2022-11-24 — THANKSGIVING_DAY` → **PASS** — broker record `45119`, fully closed UTC hours `18–22`.
2. `2022-11-25 — THANKSGIVING_FRIDAY` → **PASS** — broker record `45120`, exact target-date start `18:14Z`, fully closed target-day UTC hours `19–23`.
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION` → **PASS** — broker record `46756`, exact target-date start `21:14Z`, fully closed target-day UTC hours `22–23`.
4. `2022-12-26 — CHRISTMAS_OBSERVED` → **BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE**. The only overlapping record `46756` starts on `2022-12-23`, so it cannot be promoted as exact-target evidence.
5. `2023-01-02 — NEW_YEARS_OBSERVED` → **BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE**. The overlapping record `48045` starts on `2022-12-30`, so it cannot be promoted as exact-target evidence.

Batch accounting:

- attempted: `5`
- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch04_qualification.md`

Adjudication JSON:

`reports/data-qualification/historical_trading_breaks_recovery_batch04_adjudication.json`

The overlap boundary was adversarially attacked: unrelated non-overlapping neighbor records fail closed; DOM/network contradictions fail closed; multiple records are not silently selected; exact-target records cannot be routed through the overlap-only BLOCKED path.

## Workflow closure

The completed Batch 04 execution and independent adjudication workflows are archived to `workflow_dispatch` only. No normal push can silently repeat the browser execution or adjudication.

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
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED / pending downstream:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_INTEGRATION — NOT_YET_APPLIED`
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Atomically integrate Batch 04: add only the three independently adjudicated PASS records to executable calendar evidence, record all five Batch 04 factual attempts in the immutable attempt ledger, regenerate the attempt-aware progression state, and adversarially rerun the required calendar/coverage/progression regressions on the persisted result.**

The two BLOCKED dates (`2022-12-26`, `2023-01-02`) MUST remain unresolved and become same-capability execution-ineligible once their factual attempts are recorded.

Do not freeze Batch 05 before this atomic integration and persisted-HEAD proof are complete.

No `.bi5` acquisition. No real backtest.
