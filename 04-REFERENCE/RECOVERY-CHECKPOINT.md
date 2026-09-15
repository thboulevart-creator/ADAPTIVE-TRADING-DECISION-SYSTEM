# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 07 EXECUTION + ADJUDICATION PASS

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
- **Recovery Batch 04:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 05:** PASS (`5 PASS / 0 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 06:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 07 membership:** PASS — immutable and frozen before observation
- **Recovery Batch 07 execution/adjudication:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Recovery Batch 07 integration:** NOT YET APPLIED
- **Historical attempt ledger entries persisted:** `30` — pre-Batch07 integration
- **Registered material capability changes:** `0`
- **Persisted attempted BLOCKED / execution-ineligible:** `7` — pre-Batch07 integration
- **Persisted execution-eligible unresolved:** `38` — **STALE FOR FUTURE SCHEDULING UNTIL BATCH07 INTEGRATION**
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Batch 08 membership:** NOT FROZEN
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH07-ADJUDICATION-PASS.md`

Backup commit:

`20e391af1c0a98ef205812ac61b1215ec62aab93`

Current boundary report update commit:

`754edcfe950d3f78285c0897ceb2e64fd6c7f2ca`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH07-ADJUDICATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH07-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch07_policy_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch07_runtime.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_batch07_adjudication.json`
9. `reports/data-qualification/historical_trading_breaks_recovery_batch07_qualification.md`
10. `tools/trading_breaks_recovery_batch07.py`
11. `tools/trading_breaks_recovery_batch07_execute.py`
12. `tools/trading_breaks_recovery_batch07_adjudication.py`
13. `tests/test_trading_breaks_recovery_batch07.py`
14. `tests/test_trading_breaks_recovery_batch07_adjudication.py`
15. `tools/integrate_trading_breaks_recovery_batch06.py`
16. `tests/test_trading_breaks_recovery_batch06_integration_contract.py`
17. `tests/test_trading_breaks_recovery_batch06_integration.py`
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

## 3. BATCH 07 MEMBERSHIP REMAINS IMMUTABLE

Frozen size:

`BATCH_SIZE = 5`

Selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Frozen membership:

1. `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`
2. `2023-12-25 — CHRISTMAS_OBSERVED`
3. `2024-01-01 — NEW_YEARS_OBSERVED`
4. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
5. `2024-02-19 — PRESIDENTS_DAY`

These identities and this order MUST NOT be recalculated, substituted, reordered, expanded, shortened, or rewritten after observation.

## 4. BATCH 07 AUTHORITATIVE BROWSER EXECUTION — PASS

Execution runner:

`tools/trading_breaks_recovery_batch07_execute.py`

Runner creation commit:

`71e6fea58cc9ac4a47a9ccbb5102acabe285f78a`

Execution workflow trigger/probe commit:

`3d434dda9bd293d48cbe2f35df3d464abd5938a4`

Authoritative execution:

- run: `34958083459`
- job: `104344855871`
- conclusion: SUCCESS
- pre-browser parent/progression/Batch07 suite: `207 passed in 0.91s`
- exact immutable Batch 07 identity before Chromium: PASS
- no live membership recalculation in execution runner: PASS
- Chromium/Playwright installation occurred only after every pre-browser gate passed.

Runtime evidence artifact:

- artifact ID: `10392510730`
- SHA-256: `0df18b4bfcae04c0bf5e3670e789fc1253fde7317a50d108b35e10dd1cc2676a`
- retained files: `31`

Runtime report:

`reports/data-qualification/historical_trading_breaks_recovery_batch07_runtime.json`

Runtime persistence commit:

`071c2240dc6205ee8ffc6b8a0dbd7f2bc08a8632`

## 5. BATCH 07 INDEPENDENT ADJUDICATION — PASS

Adjudicator:

`tools/trading_breaks_recovery_batch07_adjudication.py`

Adversarial tests:

`tests/test_trading_breaks_recovery_batch07_adjudication.py`

Authoritative independent adjudication:

- run: `34958613649`
- job: `104346566865`
- trigger commit: `8ad831104f1d00ba049f458b1db772b316b44ebe`
- conclusion: SUCCESS
- adversarial/regression suite: `120 passed in 0.30s`
- authoritative runtime ancestry/immutability: PASS
- exact final accounting assertion: PASS
- no-browser/no-probe/no-live-queue adjudication guard: PASS

Final verdict:

**PASS — `BATCH07_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Adjudication persistence commit:

`2551595485923931cd47028cbc741f2f5580b6c3`

Reports:

- `reports/data-qualification/historical_trading_breaks_recovery_batch07_adjudication.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch07_qualification.md`

## 6. DATE-LEVEL FINAL OUTCOMES

### 2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `63023`
- start `2023-12-22T21:14:00Z`
- final closed instant `2023-12-25T22:59:00Z`
- reopen `2023-12-25T23:00:00Z`
- target-day fully closed hours `22–23 UTC`
- partial `21h` remains open.

### 2023-12-25 — CHRISTMAS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlap witness record `63023`
- record starts `2023-12-22T21:14:00Z`, not on the exact target date
- cross-date overlap MUST NOT be promoted to PASS.

### 2024-01-01 — NEW_YEARS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlap witness record `63024`
- record starts `2023-12-29T21:14:00Z`, not on the exact target date
- cross-date overlap MUST NOT be promoted to PASS.

### 2024-01-15 — MARTIN_LUTHER_KING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `63883`
- start `2024-01-15T18:00:00Z`
- final closed instant `2024-01-15T22:59:00Z`
- reopen `2024-01-15T23:00:00Z`
- fully closed hours `18–22 UTC`.

### 2024-02-19 — PRESIDENTS_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- record `65120`
- start `2024-02-19T18:00:00Z`
- broker final closed instant `2024-02-19T22:59:59Z`
- existing protocol-derived reopen `2024-02-19T23:00:59Z`
- fully closed hours `18–22 UTC`
- broker second precision is preserved and not silently rounded.

Final Batch 07 accounting:

- attempted: `5`
- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

Only the three PASS records may later modify executable calendar evidence. `2023-12-25` and `2024-01-01` remain unresolved and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## 7. CRITICAL PRE-INTEGRATION STATE INVARIANT

The five Batch 07 factual attempts have happened, but they are **not yet atomically written** to calendar/attempt-ledger/progression state.

Therefore the currently persisted counts remain pre-integration:

- global `111 / 46 resolved / 65 unresolved / 0 FAIL`;
- execution window `68 / 23 resolved / 45 unresolved / 0 FAIL`;
- ledger `30`;
- material capability changes `0`;
- attempted BLOCKED/ineligible `7`;
- eligible unresolved `38` — **STALE FOR FUTURE SCHEDULING**.

Do NOT:

- freeze Batch 08 from the currently persisted eligible queue;
- rerun Batch 07 merely because integration is pending;
- add the three PASS calendar records without also recording all five factual attempts;
- convert `2023-12-25` or `2024-01-01` to resolved evidence;
- populate `NO_SPECIAL_CHANGE_EVIDENCE` from either overlap.

After correct integration under unchanged capability, both blocked dates must remain unresolved and become:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

## 8. WORKFLOW CLOSURE

Batch 07 execution workflow archived to `workflow_dispatch` only:

`3719d6d02e06913b4037f073d329328b985d8e63`

Batch 07 independent adjudication workflow archived to `workflow_dispatch` only:

`b05f1a7ef8a1b430d7a2ef4a48c35fe5fad48d91`

No normal push may silently repeat completed Batch 07 browser execution or adjudication.

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

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Atomically integrate Batch 07: add only the three independently adjudicated PASS records to executable calendar evidence, record all five Batch 07 factual attempts in the immutable attempt ledger, leave `2023-12-25` and `2024-01-01` unresolved, regenerate attempt-aware progression, adversarially rerun and persist calendar/coverage/progression regressions, then perform an independent persisted-HEAD re-break before any Batch 08 freeze.**

Required integration semantics:

- integrate PASS only:
  - `2023-12-22`
  - `2024-01-15`
  - `2024-02-19`
- do NOT resolve:
  - `2023-12-25`
  - `2024-01-01`
- record all five factual Batch 07 attempts;
- the two BLOCKED dates must remain unresolved and become same-capability execution-ineligible after attempt recording;
- regenerate progression only after the atomic calendar + ledger mutation;
- no Batch 08 membership freeze until Batch 07 integration + independent persisted-HEAD re-break are PASS.

No `.bi5`. No real backtest.
