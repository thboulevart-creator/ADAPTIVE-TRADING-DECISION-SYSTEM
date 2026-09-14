# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — TRADING BREAKS BATCH 04 ADJUDICATION PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Persisted executable global calendar:** `111 candidates / 34 resolved / 77 unresolved / 0 FAIL`
- **Persisted executable candidate window:** `68 candidates / 11 resolved / 57 unresolved / 0 FAIL`
- **Historical Trading Breaks positive-record route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Recovery Batch 01:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Recovery Batch 02:** PASS (`2 PASS / 3 BLOCKED / 0 FAIL`)
- **Attempt-aware recovery progression contract:** PASS
- **Recovery Batch 03:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) and integrated
- **Batch 04 membership policy:** PASS
- **Batch 04 execution/adjudication:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Batch 04 atomic integration:** NOT YET APPLIED
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Current capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Persisted attempt ledger entries:** `15` (pre-Batch04-integration)
- **Registered material capability changes:** `0`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest atomic integrated state remains Batch 03:

`d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Batch 04 runtime persistence commit:

`2fb64b3857dcbe53f08c9dcabe85669f0eb5c81f`

Session backup for this checkpoint:

`99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH04-ADJUDICATION-PASS.md`

Backup commit:

`994fd724c5c8a0a8070ef6a6dca9df4d3aab5a5a`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH04-ADJUDICATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH04-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch04_policy_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch04_runtime.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_batch04_qualification.md`
9. `reports/data-qualification/historical_trading_breaks_recovery_batch04_adjudication.json`
10. `tools/trading_breaks_recovery_batch04.py`
11. `tools/trading_breaks_recovery_batch04_execute.py`
12. `tools/trading_breaks_recovery_batch04_adjudication.py`
13. `tests/test_trading_breaks_recovery_batch04.py`
14. `tests/test_trading_breaks_recovery_batch04_adjudication.py`
15. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH03-POLICY.md`
16. `reports/data-qualification/historical_trading_breaks_recovery_batch03_qualification.md`
17. `reports/data-qualification/historical_trading_breaks_recovery_batch03_adjudication.json`
18. `reports/data-qualification/historical_trading_breaks_recovery_batch03_runtime.json`
19. `tools/integrate_trading_breaks_recovery_batch03.py`
20. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
21. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
22. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
23. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
24. `tools/trading_breaks_recovery_progression.py`
25. `tests/test_trading_breaks_recovery_progression.py`
26. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
27. `tools/trading_breaks_recovery_protocol.py`
28. `tests/test_trading_breaks_recovery_protocol.py`
29. `LOCAL-EVIDENCE/README.md`
30. `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`
31. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct this work from conversational memory.

## 3. BATCH 04 MEMBERSHIP — HISTORICALLY FROZEN

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1`

Immutable membership:

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

Membership was mechanically derived and frozen before observation. It MUST NOT be recalculated from any future live queue during execution, adjudication, integration, replay or audit.

Membership qualification:

- run: `34894947834`
- job: `104146491103`
- trigger commit: `641b0e0369ed5a47c4adb69370e2b166b8088c06`
- suite: `104 passed in 0.35s`
- verdict: PASS

## 4. BATCH 04 AUTHORITATIVE BROWSER EXECUTION

- workflow run: `34895457466`
- job: `104148201341`
- probe commit: `11a81294720898802e49dd1131a64e20e7e7ae3a`
- artifact ID: `10369230708`
- artifact SHA-256: `3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc`
- persisted runtime commit: `2fb64b3857dcbe53f08c9dcabe85669f0eb5c81f`
- pre-browser suite: `110 passed in 0.59s`
- frozen identity guard: PASS
- no-live-membership-recalculation guard: PASS
- browser execution: SUCCESS

Chromium was installed and launched only after all pre-browser parent/progression/Batch04 gates passed.

The execution runner consumes only `batch04_targets()` and contains no call to `eligible_recovery_queue()` or `recovery_queue()`.

## 5. BATCH 04 INDEPENDENT ADJUDICATION

Final verdict:

**PASS — `BATCH04_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Adjudication run:

- run: `34895985689`
- job: `104149952523`
- trigger commit: `e3c40f3bfcd7300bfbe7383c21e4d70c16df783e`
- adversarial suite: `81 passed in 0.27s`
- final accounting assertion: PASS
- browser-free/no-live-queue adjudication guard: PASS

Date-level verdicts:

### 2022-11-24 — THANKSGIVING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `45119`
- reason `Thanksgiving Day`
- start `2022-11-24T17:59:00Z`
- final closed minute `2022-11-24T22:59:00Z`
- reopen `2022-11-24T23:00:00Z`
- fully closed UTC hours `18–22`

### 2022-11-25 — THANKSGIVING_FRIDAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `45120`
- reason `Thanksgiving Day`
- exact target-date start `2022-11-25T18:14:00Z`
- final closed minute `2022-11-27T22:59:00Z`
- fully closed target-day UTC hours `19–23`

The record spans the weekend, but its start date is exactly the target date. Only target-day full hours are projected.

### 2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `46756`
- reason `Christmas Day`
- exact target-date start `2022-12-23T21:14:00Z`
- final closed minute `2022-12-26T22:59:00Z`
- fully closed target-day UTC hours `22–23`

### 2022-12-26 — CHRISTMAS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

The only overlapping record is `46756`, starting `2022-12-23T21:14:00Z`. It overlaps 26 December but does not begin on the target date and therefore cannot be promoted as exact-target evidence.

### 2023-01-02 — NEW_YEARS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

The overlapping record `48045` starts `2022-12-30T21:14:00Z`. It overlaps 2 January but does not begin on the target date and therefore cannot be promoted as exact-target evidence.

Batch accounting:

- attempted: `5`
- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

Only the three PASS records are authorized for later executable calendar integration. The two BLOCKED dates remain unresolved; overlap is not negative evidence and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## 6. ADVERSARIAL ADJUDICATION BOUNDARY

The final 81-test re-break rejects/proves against at least:

- frozen membership tampering;
- result reordering;
- artifact digest provenance tampering;
- wrong DOM instrument identity;
- DOM/network contradiction on exact positives;
- DOM/network contradiction on overlap witnesses;
- unrelated neighboring record falsely treated as an overlap witness;
- multiple matching records silently selected;
- exact-target records being routed through the overlap-only BLOCKED path;
- browser/probe code inside adjudication;
- live `eligible_recovery_queue()` membership recalculation inside adjudication.

No second browser observation was required for adjudication.

## 7. EXECUTABLE STATE IS DELIBERATELY PRE-INTEGRATION

No Batch 04 executable integration has occurred yet.

Persisted executable state therefore remains:

- global calendar: `111 / 34 resolved / 77 unresolved / 0 FAIL`
- execution-window candidate: `68 / 11 resolved / 57 unresolved / 0 FAIL`
- attempt ledger: `15`
- registered material capability changes: `0`

The old progression runtime was generated before the five Batch 04 factual attempts existed. Its previously reported `53` eligible unresolved candidates is therefore **stale for future scheduling** until Batch 04 is atomically integrated.

Do NOT use the current live eligible queue to define Batch 05 before integration. Doing so would permit already-attempted Batch 04 dates to appear as never-attempted.

## 8. WORKFLOW CLOSURE

Completed Batch 04 workflows are archived to `workflow_dispatch` only:

- `.github/workflows/trading-breaks-recovery-batch04.yml`
- `.github/workflows/trading-breaks-recovery-batch04-adjudication.yml`

No normal push can silently repeat completed Batch 04 observation or adjudication.

## 9. CURRENT BOUNDARY MATRIX

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

PENDING / BLOCKED downstream:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_INTEGRATION — NOT_YET_APPLIED`
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 10. WHAT MUST NOT BE REPEATED

- do not rerun Batch 04 browser execution merely because integration is pending;
- do not recalculate/replace Batch 04 membership;
- do not promote `2022-12-26` or `2023-01-02` from their overlapping records;
- do not update calendar PASS records without simultaneously recording all five Batch 04 factual attempts in the integration transaction;
- do not use the stale pre-integration eligible queue to freeze Batch 05;
- do not move the execution window;
- do not acquire massive `.bi5` data;
- do not start a real backtest.

## 11. EXACTLY ONE NEXT GOVERNED ACTION

**Atomically integrate Batch 04: add only the three independently adjudicated PASS records to executable calendar evidence, record all five Batch 04 factual attempts in the immutable attempt ledger, regenerate the attempt-aware progression runtime, then adversarially rerun and persist the required calendar/coverage/progression regressions.**

The two BLOCKED dates:

- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

MUST remain unresolved and, after their attempts are recorded, become same-capability execution-ineligible under `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`.

Only after the atomic integration and an independent persisted-HEAD re-break may the next batch membership be derived.

No `.bi5`. No real backtest.
