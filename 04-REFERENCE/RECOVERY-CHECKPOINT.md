# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 05 ATOMIC INTEGRATION + PERSISTED-HEAD REBREAK PASS

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
- **Historical attempt ledger entries:** `25`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `6`
- **Execution-eligible unresolved:** `43`
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Authoritative Batch 05 atomic integration commit:

`99c2f38842a0c4ea66ba6ff90496380986d02e52`

Authoritative corrected persisted-HEAD verification commit:

`70428e536689793a74420d35c84744b8ad0f2f3d`

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH05-INTEGRATION-PASS.md`

Backup commit:

`07d72a7da0569d34c329c3f209bcece00dca3932`

Current boundary report update commit:

`7056750c2b370f21fe92db7212fc000907dc1760`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH05-INTEGRATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `reports/data-qualification/historical_trading_breaks_recovery_batch05_integration_qualification.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch05_adjudication.json`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch05_runtime.json`
8. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH05-POLICY.md`
9. `tools/trading_breaks_recovery_batch05.py`
10. `tools/trading_breaks_recovery_batch05_adjudication.py`
11. `tools/integrate_trading_breaks_recovery_batch05.py`
12. `tests/test_trading_breaks_recovery_batch05.py`
13. `tests/test_trading_breaks_recovery_batch05_adjudication.py`
14. `tests/test_trading_breaks_recovery_batch05_integration_contract.py`
15. `tests/test_trading_breaks_recovery_batch05_integration.py`
16. `tests/test_dukascopy_usatech_calendar_2023_batch05.py`
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

## 3. BATCH 05 HISTORICAL MEMBERSHIP REMAINS IMMUTABLE

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

This historical Batch 05 membership MUST NOT be recalculated, substituted, reordered, expanded, shortened or rewritten.

## 4. BATCH 05 AUTHORITATIVE EXECUTION + ADJUDICATION

Browser execution:

- run: `34947146056`
- job: `104309150262`
- probe commit: `33ae476c48372bce64421a411066db2ddea6125c`
- artifact: `10386998786`
- artifact SHA-256: `ad96e1850ca53910c092abd444f02a04e2a84ea192fa6c0b5189a7e349ea800c`
- pre-browser gates: `134 passed in 0.58s`

Independent adjudication:

- run: `34947662443`
- job: `104310794052`
- adversarial suite: `83 passed in 0.28s`
- final result: `5 PASS / 0 BLOCKED / 0 FAIL`

Verdict:

**PASS — `BATCH05_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

Records:

- `2023-01-16` → `49338`, closed hours `18–22 UTC`;
- `2023-02-20` → `50456`, closed hours `18–22 UTC`;
- `2023-04-07` → `52290`, target-day closed hours `15–23 UTC`, with weekend continuation not promoted to another target date;
- `2023-05-29` → `54373`, closed hours `17–21 UTC`;
- `2023-06-19` → `55281`, closed hours `17–21 UTC`.

## 5. BATCH 05 ATOMIC INTEGRATION — PASS

Authoritative integration workflow:

- run: `34949197265`
- job: `104315829990`
- conclusion: SUCCESS
- pre-mutation integration-contract regression: `76 passed`
- post-mutation adversarial regression: `166 passed`
- atomic integration commit: `99c2f38842a0c4ea66ba6ff90496380986d02e52`

Verdict:

**PASS — `BATCH05_ATOMIC_CALENDAR_ATTEMPT_PROGRESSION_INTEGRATION_COHERENT`**

The atomic commit:

- added exactly the five Batch 05 PASS records to executable calendar evidence;
- appended exactly five factual attempts as sequences `21..25`, all `PASS`;
- regenerated progression runtime;
- kept all six historical BLOCKED dates unresolved and same-capability execution-ineligible;
- registered no material capability change;
- admitted no negative-evidence promotion.

Post-integration persisted state:

- global: `111 / 42 resolved / 69 unresolved / 0 FAIL`;
- execution window: `68 / 19 resolved / 49 unresolved / 0 FAIL`;
- attempt ledger: `25`;
- attempted BLOCKED ineligible: `6`;
- execution-eligible unresolved: `43`.

## 6. INDEPENDENT PERSISTED-HEAD REBREAK — PASS

First attempt:

- run: `34949393807`
- job: `104316469582`
- `166 passed in 0.74s`;
- exact persisted calendar/ledger/progression assertion: PASS;
- overall run: FAIL only because the browser-free self-check contained the exact forbidden strings in its own search-list literals.

This was a self-referential guard false positive. It was not a data, calendar, ledger, progression, provenance or integration failure. The correction changed only the guard's string construction.

Corrected authoritative re-break:

- run: `34949499981`
- job: `104316813519`
- verified commit: `70428e536689793a74420d35c84744b8ad0f2f3d`
- conclusion: SUCCESS
- adversarial suite: `166 passed in 0.99s`
- exact persisted-state assertion: PASS
- no-browser/no-capture guard: PASS
- deterministic progression regeneration + `git diff --exit-code`: PASS
- permissions: `contents: read`, `metadata: read`

Final verdict:

**PASS — `BATCH05_ATOMIC_INTEGRATION_SURVIVES_INDEPENDENT_PERSISTED_HEAD_REBREAK`**

## 7. CURRENT ATTEMPT-AWARE PROGRESSION STATE

- unresolved candidates in execution window: `49`
- historical attempts: `25`
- material capability changes: `0`
- same-capability attempted BLOCKED / execution-ineligible: `6`
- execution-eligible unresolved: `43`

The six unresolved same-capability BLOCKED dates remain:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Each remains:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

The first current eligible unresolved progression entry is:

`2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

This fact does **not** freeze Batch 06.

## 8. WORKFLOW CLOSURE

Batch 05 browser execution and adjudication workflows were already manual-only.

Batch 05 persisted-head re-break archived to `workflow_dispatch` only:

`0946f2029c19b22cd34a4aa305076d0300eea357`

Batch 05 integration workflow archived to `workflow_dispatch` only:

`aeefca76a4d1b02c17bd07e825764ae232deb006`

No normal push may silently repeat completed Batch 05 execution, adjudication, integration or persisted-head re-break.

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
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 10. WHAT MUST NOT BE REPEATED OR BYPASSED

- do not rerun or rewrite historical Batch 05 membership;
- do not re-integrate Batch 05 merely because later batches are prepared;
- do not retry the six same-capability BLOCKED dates without a separately qualified material capability change addressing their blocker;
- do not manually choose Batch 06 members;
- do not move the execution window;
- do not acquire massive `.bi5` data;
- do not start a real backtest.

## 11. EXACTLY ONE NEXT GOVERNED ACTION

**Freeze and version Batch 06 from the persisted post-Batch05 `eligible_recovery_queue()`, then adversarially break its membership before any Chromium/browser observation.**

Batch 06 has **not** been frozen yet. Its membership must be derived mechanically from the persisted eligible queue with the same fixed-size, no-outcome-selection governance used previously. No substitution, skip, reorder, expansion or shortening is authorized.

No `.bi5`. No real backtest.
