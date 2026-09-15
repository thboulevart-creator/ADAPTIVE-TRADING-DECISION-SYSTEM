# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 05 MEMBERSHIP PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Persisted executable global calendar:** `111 candidates / 37 resolved / 74 unresolved / 0 FAIL`
- **Persisted executable candidate window:** `68 candidates / 14 resolved / 54 unresolved / 0 FAIL`
- **Historical Trading Breaks positive-record route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Recovery Batch 01:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Recovery Batch 02:** PASS (`2 PASS / 3 BLOCKED / 0 FAIL`)
- **Recovery Batch 03:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) and integrated
- **Recovery Batch 04:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`) and atomically integrated
- **Recovery Batch 05 membership policy:** PASS — frozen before observation
- **Attempt-aware recovery progression:** PASS
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Current capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Historical attempt ledger entries:** `20`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `6`
- **Execution-eligible unresolved:** `48`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Authoritative Batch 04 atomic integration commit:

`6cafa5337f28c5424cbcc25280c690de702061d9`

Authoritative Batch 04 persisted-state verification commit:

`9ad19ede0052f37ce8aa2ccd30a117cd0525bc10`

Authoritative Batch 05 pre-freeze baseline/checkpoint HEAD:

`601310a55b64233ada9e481d3cb2f11dc20a30d5`

Batch 05 membership backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH05-MEMBERSHIP-PASS.md`

Backup commit:

`99243ca4aad2571a941eb03637ea38eb1458346f`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH05-MEMBERSHIP-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH05-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch05_policy_qualification.md`
7. `tools/trading_breaks_recovery_batch05.py`
8. `tests/test_trading_breaks_recovery_batch05.py`
9. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
10. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
11. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
12. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
13. `tools/trading_breaks_recovery_progression.py`
14. `tests/test_trading_breaks_recovery_progression.py`
15. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
16. `tools/trading_breaks_recovery_protocol.py`
17. `tests/test_trading_breaks_recovery_protocol.py`
18. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH04-INTEGRATION-PASS.md`
19. `reports/data-qualification/historical_trading_breaks_recovery_batch04_integration_qualification.md`
20. `reports/data-qualification/historical_trading_breaks_recovery_batch04_qualification.md`
21. `reports/data-qualification/historical_trading_breaks_recovery_batch04_adjudication.json`
22. `reports/data-qualification/historical_trading_breaks_recovery_batch04_runtime.json`
23. `tools/trading_breaks_recovery_batch04_execute.py`
24. `tools/trading_breaks_recovery_batch04_adjudication.py`
25. `tests/test_trading_breaks_recovery_batch04_adjudication.py`
26. `tools/dukascopy_usatech_calendar.py`
27. `tools/dukascopy_usatech_calendar_coverage.py`
28. `tests/test_dukascopy_usatech_calendar_coverage.py`
29. `tests/test_coverage_execution_window_boundary.py`
30. `LOCAL-EVIDENCE/README.md`
31. `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`
32. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct Batch 05 membership from conversational memory or from a newly calculated execution queue.

## 3. BATCH 05 MEMBERSHIP IS NOW IMMUTABLE

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY_V1`

Selection rule at freeze:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Fixed batch size:

`BATCH_SIZE = 5`

Authoritative frozen membership:

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

This membership was frozen before any Batch 05 observation and MUST NOT be recalculated, replaced, reordered, expanded, shortened, or rewritten by execution/adjudication or future batches.

At execution time the source of membership is the immutable `FROZEN_BATCH05_TARGETS` / `batch05_targets()` from:

`tools/trading_breaks_recovery_batch05.py`

The live `eligible_recovery_queue()` may be used only as a parent-state consistency gate, not to select a new Batch 05 membership.

## 4. BATCH 05 FREEZE PROVENANCE

Pre-freeze checkpoint HEAD:

`601310a55b64233ada9e481d3cb2f11dc20a30d5`

Source post-Batch04 progression-state commit:

`6cafa5337f28c5424cbcc25280c690de702061d9`

Freeze module commit:

`0a1208fa485759982d56d9167c860af8afb7a397`

Initial policy commit:

`8b304470c1c0d43dd727deaeadda71b09e0fb3f4`

Adversarial-test commit:

`d55ee57c3cb89268f13c33a1ac6c3e23ee8df2ab`

Qualification-workflow trigger commit:

`71d33ea99b83a03f1ed916f447b95e24b9059b3b`

Qualification report commit:

`c9592f2f7e64672269395e0b55c51933b6a064da`

Workflow archive commit:

`36066d1ac5200c752b59734d1487df14423b650c`

Final policy PASS commit:

`fff22a18d013cbdf196ae94b8653f1cf9ab8c953`

Current boundary report update commit:

`4f3f1e4c04d3d5b74e590cc77ddd6600e90f062d`

## 5. AUTHORITATIVE BATCH 05 MEMBERSHIP QUALIFICATION

Final verdict:

**PASS — `BATCH05_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Authoritative GitHub Actions proof:

- workflow run: `34942590738`
- job: `104294478304`
- trigger commit: `71d33ea99b83a03f1ed916f447b95e24b9059b3b`
- conclusion: **SUCCESS**
- adversarial/regression suite: **94 passed in 0.33s**
- exact assertion `batch05_targets() == eligible_recovery_queue()[:5]`: **PASS**
- exact five members printed in governed order: **PASS**
- no-browser/no-probe freeze guard: **PASS**
- workflow token permissions: `contents: read`, `metadata: read`

The workflow installed pytest only. It did not install Playwright or Chromium.

No historical broker observation occurred during Batch 05 freeze or membership qualification.

## 6. PARENT PROGRESSION STATE AT FREEZE

Persisted state:

- unresolved in execution window: `54`
- historical attempts: `20`
- material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `6`
- execution-eligible unresolved: `48`

The six same-capability attempted BLOCKED dates remain unresolved but execution-ineligible:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Each is:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

No retry is authorized under the unchanged capability.

Every frozen Batch 05 member had no prior ledger attempt and was classified:

`ELIGIBLE — INITIAL_ATTEMPT`

## 7. BROWSER / OBSERVATION BOUNDARY

Batch 05 membership qualification contains no browser execution path.

The freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio.

The completed policy workflow is archived to `workflow_dispatch` only.

Therefore no normal push can silently repeat completed Batch 05 membership qualification.

## 8. CURRENT EXECUTABLE ACCOUNTING REMAINS UNCHANGED

Membership freeze does not resolve dates.

No calendar evidence was modified.

No attempt ledger entry was appended.

No material capability change was registered.

Current persisted state therefore remains:

- global: `111 candidates / 37 resolved / 74 unresolved / 0 FAIL`
- execution window: `68 candidates / 14 resolved / 54 unresolved / 0 FAIL`
- attempt ledger: `20`
- attempted BLOCKED ineligible: `6`
- execution-eligible unresolved: `48`

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 10. WHAT MUST NOT BE REPEATED OR BYPASSED

- do not recompute Batch 05 membership at execution time;
- do not use raw `recovery_queue()` as execution membership;
- do not insert/skip/reorder Batch 05 members after outcomes are observed;
- do not rerun the Batch 05 membership freeze merely because execution will be prepared;
- do not retry any of the six same-capability BLOCKED dates without a qualified material capability change;
- do not move the execution window;
- do not acquire massive `.bi5` data;
- do not start a real backtest.

## 11. EXACTLY ONE NEXT GOVERNED ACTION

**Execute the already-frozen Batch 05 membership under the qualified Trading Breaks capture chain, with all parent protocol/progression/Batch05 gates PASS before Chromium opens, then independently adjudicate all five results.**

Execution MUST use exactly:

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

Before Chromium opens, prove at minimum:

- parent recovery protocol remains PASS;
- attempt-aware progression state remains coherent with the freeze state;
- Batch 05 frozen tuple is exact and immutable;
- all five members correspond to the qualified frozen identities;
- no membership substitution/reorder/expansion path exists;
- the execution runner consumes `batch05_targets()` rather than calculating a new live prefix.

Then execute the five frozen dates using the already-qualified semantic capture implementation and persist run/job/artifact/hash/probe-commit provenance.

Only after that, perform a separate independent adjudication of all five results under the parent protocol and immutable Batch 05 scope.

No `.bi5`. No real backtest.
