# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 06 EXECUTION + ADJUDICATION PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Persisted executable global calendar:** `111 candidates / 42 resolved / 69 unresolved / 0 FAIL`
- **Persisted executable candidate window:** `68 candidates / 19 resolved / 49 unresolved / 0 FAIL`
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
- **Recovery Batch 06 integration:** NOT YET APPLIED
- **Historical attempt ledger entries persisted:** `25` — pre-Batch06 integration
- **Registered material capability changes:** `0`
- **Persisted attempted BLOCKED / execution-ineligible:** `6` — pre-Batch06 integration
- **Persisted execution-eligible unresolved:** `43` — **STALE FOR FUTURE SCHEDULING UNTIL BATCH06 INTEGRATION**
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Authoritative Batch 06 execution runtime commit:

`b50529991d9af6e27170090bd45b42eb751d0958`

Authoritative Batch 06 adjudication commit:

`874f8fe2c809d1f3c1442ba61aaabb4056a03e3d`

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH06-ADJUDICATION-PASS.md`

Backup commit:

`c609f837707f6e3822eab56af2384e91cbb7cf4d`

Current boundary report update commit:

`158a3d55841ba2cb5bc8f4cbd00aac0daf6eed83`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH06-ADJUDICATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH06-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch06_policy_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch06_runtime.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_batch06_adjudication.json`
9. `reports/data-qualification/historical_trading_breaks_recovery_batch06_qualification.md`
10. `tools/trading_breaks_recovery_batch06.py`
11. `tools/trading_breaks_recovery_batch06_execute.py`
12. `tools/trading_breaks_recovery_batch06_adjudication.py`
13. `tests/test_trading_breaks_recovery_batch06.py`
14. `tests/test_trading_breaks_recovery_batch06_adjudication.py`
15. `tools/integrate_trading_breaks_recovery_batch05.py`
16. `tests/test_trading_breaks_recovery_batch05_integration_contract.py`
17. `tests/test_trading_breaks_recovery_batch05_integration.py`
18. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
19. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
20. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
21. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
22. `tools/trading_breaks_recovery_progression.py`
23. `tests/test_trading_breaks_recovery_progression.py`
24. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
25. `tools/trading_breaks_recovery_protocol.py`
26. `tests/test_trading_breaks_recovery_protocol.py`
27. `tools/dukascopy_usatech_calendar.py`
28. `tools/dukascopy_usatech_calendar_coverage.py`
29. `tests/test_dukascopy_usatech_calendar_coverage.py`
30. `tests/test_coverage_execution_window_boundary.py`
31. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct state from conversation.

## 3. BATCH 06 MEMBERSHIP REMAINS IMMUTABLE

Fixed size:

`BATCH_SIZE = 5`

Selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Frozen membership:

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
3. `2023-09-04 — LABOR_DAY`
4. `2023-11-23 — THANKSGIVING_DAY`
5. `2023-11-24 — THANKSGIVING_FRIDAY`

These identities and this order MUST NOT be recalculated, substituted, reordered, expanded, shortened or rewritten.

## 4. BATCH 06 AUTHORITATIVE BROWSER EXECUTION — PASS

Execution runner:

`tools/trading_breaks_recovery_batch06_execute.py`

Runner creation commit:

`ae98364bfd5f9f3cbecd3de1137a4fbca4dd792b`

Execution workflow trigger/probe commit:

`e968db2be1fbfd4d2c419f9dad717ca479b52edd`

Authoritative execution:

- run: `34954308324`
- job: `104332522379`
- conclusion: SUCCESS
- pre-browser parent/progression/Batch06 suite: `170 passed in 0.72s`
- checkpoint ancestry + governed parent-state immutability: PASS
- exact immutable Batch 06 identity before Chromium: PASS
- no live membership recalculation in execution runner: PASS
- Playwright/Chromium installation occurred only after every pre-browser gate passed.

Runtime evidence artifact:

- artifact ID: `10390926878`
- SHA-256: `1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052`
- retained files: `31`

Runtime report:

`reports/data-qualification/historical_trading_breaks_recovery_batch06_runtime.json`

Runtime persistence commit:

`b50529991d9af6e27170090bd45b42eb751d0958`

## 5. BATCH 06 INDEPENDENT ADJUDICATION — PASS

Adjudicator:

`tools/trading_breaks_recovery_batch06_adjudication.py`

Adversarial tests:

`tests/test_trading_breaks_recovery_batch06_adjudication.py`

Authoritative independent adjudication:

- run: `34954764562`
- job: `104334032049`
- trigger commit: `44bac8e3ebb8c783d02295f052fe17c86c222049`
- conclusion: SUCCESS
- adversarial/regression suite: `114 passed in 0.36s`
- authoritative runtime ancestry/immutability: PASS
- exact final accounting assertion: PASS
- no-browser/no-probe/no-live-queue adjudication guard: PASS

Final verdict:

**PASS — `BATCH06_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Adjudication persistence commit:

`874f8fe2c809d1f3c1442ba61aaabb4056a03e3d`

Reports:

- `reports/data-qualification/historical_trading_breaks_recovery_batch06_adjudication.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch06_qualification.md`

## 6. DATE-LEVEL FINAL OUTCOMES

### 2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `56233`
- start `2023-07-03T17:14:00Z`
- final closed minute `2023-07-04T21:59:00Z`
- reopen `2023-07-04T22:00:00Z`
- target-day fully closed hours `18–23 UTC`
- partial `17h` remains open.

### 2023-07-04 — INDEPENDENCE_DAY_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlap witness record `56233`
- record starts `2023-07-03T17:14:00Z`, not on the exact target date
- cross-date overlap MUST NOT be promoted to PASS.

### 2023-09-04 — LABOR_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `57462`
- start `2023-09-04T16:59:00Z`
- final closed minute `2023-09-04T21:59:00Z`
- reopen `2023-09-04T22:00:00Z`
- fully closed hours `17–21 UTC`.

### 2023-11-23 — THANKSGIVING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `59358`
- start `2023-11-23T16:59:00Z`
- final closed minute `2023-11-23T22:59:00Z`
- reopen `2023-11-23T23:00:00Z`
- fully closed hours `17–22 UTC`.

### 2023-11-24 — THANKSGIVING_FRIDAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `59359`
- start `2023-11-24T17:14:00Z`
- final closed minute `2023-11-26T22:59:00Z`
- reopen `2023-11-26T23:00:00Z`
- target-day fully closed hours `18–23 UTC`
- partial `17h` remains open; weekend continuation is not promoted to another target date.

Final Batch 06 accounting:

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

Only the four PASS records may later modify executable calendar evidence. `2023-07-04` remains unresolved and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## 7. CRITICAL PRE-INTEGRATION STATE INVARIANT

The five Batch 06 factual attempts have happened, but they are **not yet atomically written** to calendar/attempt-ledger/progression state.

Therefore the currently persisted counts remain pre-integration:

- global `111 / 42 resolved / 69 unresolved / 0 FAIL`;
- execution window `68 / 19 resolved / 49 unresolved / 0 FAIL`;
- ledger `25`;
- material changes `0`;
- attempted BLOCKED/ineligible `6`;
- eligible unresolved `43` — **STALE FOR FUTURE SCHEDULING**.

Do NOT:

- freeze Batch 07 from the currently persisted eligible queue;
- rerun Batch 06 merely because integration is pending;
- add the four PASS calendar records without also recording all five factual attempts;
- convert the `2023-07-04` BLOCKED result to resolved evidence;
- populate `NO_SPECIAL_CHANGE_EVIDENCE` from the July 4 overlap.

The integration must be atomic.

After correct integration, `2023-07-04` must remain unresolved and, under the unchanged capability, become:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

## 8. WORKFLOW CLOSURE

Batch 06 execution workflow archived to `workflow_dispatch` only:

`224a4f99daf4fce09f7c07759a8fd89f4aa2b77a`

Batch 06 independent adjudication workflow archived to `workflow_dispatch` only:

`285d94e11a7887d1cc62858390c4c29752ef5588`

No normal push may silently repeat completed Batch 06 browser execution or adjudication.

## 9. CURRENT BOUNDARY MATRIX

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

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Atomically integrate Batch 06: add only the four independently adjudicated PASS records to executable calendar evidence, record all five Batch 06 factual attempts in the immutable attempt ledger, regenerate attempt-aware progression, adversarially rerun and persist calendar/coverage/progression regressions, then perform an independent persisted-HEAD re-break before any Batch 07 freeze.**

Required integration semantics:

- integrate PASS only:
  - `2023-07-03`
  - `2023-09-04`
  - `2023-11-23`
  - `2023-11-24`
- do NOT resolve `2023-07-04`;
- record all five Batch 06 factual attempts;
- `2023-07-04` must remain unresolved and become same-capability execution-ineligible after the attempt write;
- regenerate progression only after the atomic state mutation;
- no Batch 07 membership freeze until integration + independent persisted-HEAD re-break are PASS.

No `.bi5`. No real backtest.
