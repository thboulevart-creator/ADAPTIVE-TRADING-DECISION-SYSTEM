# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 06 INTEGRATION + PERSISTED-HEAD REBREAK PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Persisted executable global calendar:** `111 candidates / 46 resolved / 65 unresolved / 0 FAIL`
- **Persisted executable candidate window:** `68 candidates / 23 resolved / 45 unresolved / 0 FAIL`
- **Historical Trading Breaks positive-record route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Attempt-aware recovery progression:** PASS
- **Recovery Batch 01:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Recovery Batch 02:** PASS (`2 PASS / 3 BLOCKED / 0 FAIL`)
- **Recovery Batch 03:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) and integrated
- **Recovery Batch 04:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`) and atomically integrated + persisted-HEAD re-break PASS
- **Recovery Batch 05:** PASS (`5 PASS / 0 BLOCKED / 0 FAIL`) and atomically integrated + persisted-HEAD re-break PASS
- **Recovery Batch 06 membership:** PASS — immutable and frozen before observation
- **Recovery Batch 06 execution/adjudication:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`)
- **Recovery Batch 06 atomic integration:** PASS
- **Recovery Batch 06 persisted-HEAD re-break:** PASS
- **Historical attempt ledger entries:** `30`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `7`
- **Execution-eligible unresolved:** `38`
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Batch 07 membership:** NOT FROZEN
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Authoritative Batch 06 atomic integration commit:

`a2a59baefd7986f65efb4d625acd2c47c085ae31`

Authoritative Batch 06 persisted-HEAD re-break trigger commit:

`3feb9f937bf74202f68642992ca3fe8b363398d9`

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH06-INTEGRATION-PASS.md`

Backup commit:

`1874f536a82b305e83b52056c530e587c2bc0972`

Current boundary report commit:

`574c8efa61115b0d0908cc8f7e40f525a1cfed3c`

Persisted-head evidence report commit:

`94707d92192230be48074e044c5d47c1b37a8a25`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH06-INTEGRATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `reports/data-qualification/historical_trading_breaks_recovery_batch06_persisted_head_rebreak.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch06_integration_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch06_adjudication.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_batch06_runtime.json`
9. `tools/integrate_trading_breaks_recovery_batch06.py`
10. `tests/test_trading_breaks_recovery_batch06_integration_contract.py`
11. `tests/test_trading_breaks_recovery_batch06_integration.py`
12. `tests/test_dukascopy_usatech_calendar_2023_batch06.py`
13. `tools/trading_breaks_recovery_batch06.py`
14. `tests/test_trading_breaks_recovery_batch06.py`
15. `tools/trading_breaks_recovery_batch06_adjudication.py`
16. `tests/test_trading_breaks_recovery_batch06_adjudication.py`
17. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
18. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
19. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
20. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
21. `tools/trading_breaks_recovery_progression.py`
22. `tests/test_trading_breaks_recovery_progression.py`
23. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
24. `tools/trading_breaks_recovery_protocol.py`
25. `tests/test_trading_breaks_recovery_protocol.py`
26. `tools/dukascopy_usatech_calendar.py`
27. `tools/dukascopy_usatech_calendar_coverage.py`
28. `tests/test_dukascopy_usatech_calendar_coverage.py`
29. `tests/test_coverage_execution_window_boundary.py`
30. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct state from conversation.

## 3. BATCH 06 MEMBERSHIP REMAINS HISTORICALLY IMMUTABLE

Frozen membership:

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
3. `2023-09-04 — LABOR_DAY`
4. `2023-11-23 — THANKSGIVING_DAY`
5. `2023-11-24 — THANKSGIVING_FRIDAY`

Final independent adjudication:

1. `2023-07-03` — PASS — record `56233`
2. `2023-07-04` — BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`
3. `2023-09-04` — PASS — record `57462`
4. `2023-11-23` — PASS — record `59358`
5. `2023-11-24` — PASS — record `59359`

The July 4 record is only the cross-date overlap record `56233`, which starts on `2023-07-03`. It was never promoted to exact-target PASS.

## 4. AUTHORITATIVE BATCH 06 SOURCE EVIDENCE

Browser execution:

- run: `34954308324`
- job: `104332522379`
- probe commit: `e968db2be1fbfd4d2c419f9dad717ca479b52edd`
- artifact: `10390926878`
- artifact SHA-256: `1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052`
- runtime persistence commit: `b50529991d9af6e27170090bd45b42eb751d0958`

Independent adjudication:

- run: `34954764562`
- job: `104334032049`
- trigger commit: `44bac8e3ebb8c783d02295f052fe17c86c222049`
- adjudication persistence commit: `874f8fe2c809d1f3c1442ba61aaabb4056a03e3d`
- regression: `114 passed in 0.36s`
- result: `4 PASS / 1 BLOCKED / 0 FAIL`

## 5. BATCH 06 ATOMIC INTEGRATION — PASS

Authoritative integration:

- workflow run: `34956127849`
- job: `104338497611`
- trigger commit: `0fd09cf0ac2083b32c97dafe090db0e7d5b82999`
- conclusion: SUCCESS
- pre-mutation contract/regression: `110 passed`
- post-mutation adversarial/regression: `206 passed in 0.77s`
- exact integrated accounting assertion: PASS
- no-negative-evidence/no-browser executable-surface guard: PASS

Atomic integration commit:

`a2a59baefd7986f65efb4d625acd2c47c085ae31`

Exact mutation:

- executable calendar evidence added only for:
  - `2023-07-03`
  - `2023-09-04`
  - `2023-11-23`
  - `2023-11-24`
- `2023-07-04` was not resolved;
- all five factual attempts were appended as sequences `26..30`;
- progression runtime was regenerated only after calendar + ledger mutation;
- material capability changes remained `0`.

Batch 06 attempt sequence:

- `26` — `batch06:2023-07-03` — PASS
- `27` — `batch06:2023-07-04` — BLOCKED
- `28` — `batch06:2023-09-04` — PASS
- `29` — `batch06:2023-11-23` — PASS
- `30` — `batch06:2023-11-24` — PASS

The July 4 attempt retains blocker:

`NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

Its current progression state is exactly:

`UNRESOLVED + INELIGIBLE — SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

No `NO_SPECIAL_CHANGE_EVIDENCE` was created from the overlap.

## 6. FAIL-CLOSED INTEGRATION QUALIFICATION HISTORY

Two non-authoritative attempts failed before any persistent executable mutation:

### Attempt A

- run: `34955611637`
- job: `104336823027`
- contract tests: PASS
- failure: preparer rewrite guard expected one Batch 05 attempt-count assertion but found two legitimate assertions
- correction: minimal cardinality fix at `4543556dc572e1ee7e0a18656e53bdcfd9a62c67`
- persistent calendar/ledger/progression mutation: NONE

### Attempt B

- run: `34956027482`
- job: `104338171283`
- simulated integration: PASS
- progression regeneration: PASS
- `206` post-mutation regressions: PASS
- exact state assertion: PASS
- failure: whole-file lexical browser guard matched browser tokens contained only in generated test-source strings
- correction: guard scoped to executable integration functions
- persistent calendar/ledger/progression mutation: NONE

These failures are retained as qualification history and were not hidden or promoted.

## 7. INDEPENDENT PERSISTED-HEAD REBREAK — PASS

Authoritative read-only re-break:

- run: `34956317590`
- job: `104339111722`
- trigger commit: `3feb9f937bf74202f68642992ca3fe8b363398d9`
- authoritative integration ancestor: `a2a59baefd7986f65efb4d625acd2c47c085ae31`
- only file between integration commit and re-break trigger: `.github/workflows/trading-breaks-recovery-batch06-persisted-head.yml`
- permissions: `contents: read`
- adversarial/regression suite: `206 passed in 0.83s`
- exact persisted-state assertion: PASS
- no-browser/no-capture dependency guard: PASS
- deterministic progression regeneration + `git diff --exit-code`: PASS

Persisted state independently proven:

- global `111 / 46 resolved / 65 unresolved / 0 FAIL`
- window `68 / 23 resolved / 45 unresolved / 0 FAIL`
- ledger `30`
- material changes `0`
- attempted BLOCKED/ineligible `7`
- eligible unresolved `38`

The eligible queue is chronological. Its first current candidate is:

`2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`

This is a post-integration progression fact only. **Batch 07 is not frozen.**

## 8. SEVEN SAME-CAPABILITY BLOCKED DATES

These remain unresolved and execution-ineligible:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`
- `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`

Each is:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

They remain visible in unresolved calendar accounting and cannot be retried under the unchanged semantic capability.

## 9. WORKFLOW CLOSURE

Historical Batch 06 execution and adjudication workflows were already archived manual-only.

Batch 06 persisted-head re-break workflow archived to `workflow_dispatch` only:

`6caa402c21a78faccb7ac3897c5b280f4dbdca6a`

Batch 06 atomic integration workflow archived to `workflow_dispatch` only:

`da6cff32eae7c8c863753aaff0875aeb0fe42774`

No normal push may silently repeat completed Batch 06 execution, adjudication, integration or persisted-head verification.

## 10. CURRENT BOUNDARY MATRIX

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
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 11. WHAT MUST NOT BE REPEATED OR BYPASSED

- do not rewrite or recalculate historical Batch 06 membership;
- do not rerun Batch 06 because its workstream is closed PASS;
- do not promote `2023-07-04` or any other same-capability BLOCKED date;
- do not treat an overlap as exact-target proof;
- do not retry a same-capability BLOCKED date without separately qualified material capability change;
- do not freeze Batch 07 from raw `recovery_queue()`;
- do not select Batch 07 using expected outcome, convenience or source availability;
- do not move or shorten the execution window;
- do not acquire massive `.bi5` data;
- do not start a real backtest.

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Freeze Batch 07 membership from the freshly persisted post-Batch06 `eligible_recovery_queue()[:5]`, with fixed batch size and immutable membership versioned before any Batch 07 observation.**

Requirements for that next action:

- read this checkpoint and recovery order first;
- verify active HEAD contains this checkpoint before any write;
- derive membership mechanically from current attempt-aware eligible queue;
- fix/version batch size before observation;
- prove every member is unresolved, eligible and chronologically selected;
- freeze immutable membership before any browser/probe execution;
- adversarially attack skip/reorder/substitution/raw-queue bypass/manual selection/outcome dependence;
- no Chromium/Playwright/probe during membership qualification;
- do not execute Batch 07 in the same membership-freeze action;
- no `.bi5`;
- no real backtest.
