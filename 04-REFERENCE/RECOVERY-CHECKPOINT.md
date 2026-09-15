# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 06 MEMBERSHIP PASS

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
- **Recovery Batch 06 execution/adjudication:** NOT YET PERFORMED
- **Historical attempt ledger entries:** `25`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `6`
- **Execution-eligible unresolved:** `43`
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Authoritative post-Batch05 atomic integration commit:

`99c2f38842a0c4ea66ba6ff90496380986d02e52`

Authoritative post-Batch05 persisted-HEAD verification commit:

`70428e536689793a74420d35c84744b8ad0f2f3d`

Batch 06 pre-freeze checkpoint:

`289d7f4432efba4ad2bc1e97d5b23f14f587019e`

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH06-MEMBERSHIP-PASS.md`

Backup commit:

`b90b03f83b7f282b2814291b074a28206b3fffd0`

Current boundary report update commit:

`8c7fbb7adf5597894708af0cdb5f08775b11c69c`

Final Batch 06 policy commit:

`ec38cb44d36a579fc8a7d995a2099a3bef337c58`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH06-MEMBERSHIP-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH06-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch06_policy_qualification.md`
7. `tools/trading_breaks_recovery_batch06.py`
8. `tests/test_trading_breaks_recovery_batch06.py`
9. `reports/data-qualification/historical_trading_breaks_recovery_batch05_integration_qualification.md`
10. `reports/data-qualification/historical_trading_breaks_recovery_batch05_adjudication.json`
11. `reports/data-qualification/historical_trading_breaks_recovery_batch05_runtime.json`
12. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH05-POLICY.md`
13. `tools/trading_breaks_recovery_batch05.py`
14. `tools/trading_breaks_recovery_batch05_adjudication.py`
15. `tools/integrate_trading_breaks_recovery_batch05.py`
16. `tests/test_trading_breaks_recovery_batch05.py`
17. `tests/test_trading_breaks_recovery_batch05_adjudication.py`
18. `tests/test_trading_breaks_recovery_batch05_integration_contract.py`
19. `tests/test_trading_breaks_recovery_batch05_integration.py`
20. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
21. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
22. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
23. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
24. `tools/trading_breaks_recovery_progression.py`
25. `tests/test_trading_breaks_recovery_progression.py`
26. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
27. `tools/trading_breaks_recovery_protocol.py`
28. `tests/test_trading_breaks_recovery_protocol.py`
29. `tools/dukascopy_usatech_calendar.py`
30. `tools/dukascopy_usatech_calendar_coverage.py`
31. `tests/test_dukascopy_usatech_calendar_coverage.py`
32. `tests/test_coverage_execution_window_boundary.py`
33. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct state from conversation.

## 3. BATCH 06 MEMBERSHIP IS NOW IMMUTABLE

Fixed size:

`BATCH_SIZE = 5`

Selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Historical freeze-time assertion:

`batch06_targets() == eligible_recovery_queue()[:5]`

Frozen membership:

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
3. `2023-09-04 — LABOR_DAY`
4. `2023-11-23 — THANKSGIVING_DAY`
5. `2023-11-24 — THANKSGIVING_FRIDAY`

These identities and this order MUST NOT be recalculated, substituted, reordered, expanded, shortened or rewritten after outcomes become knowable.

At execution time the target set MUST come only from immutable `batch06_targets()` / `FROZEN_BATCH06_TARGETS`, never from a live queue recomputation.

## 4. BATCH 06 FREEZE PROVENANCE

Freeze module:

`tools/trading_breaks_recovery_batch06.py`

Creation commit:

`2cfd7d8c82cc12ce5904a60ed0720cd17ec15efd`

Policy contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_POLICY_V1`

Pre-freeze checkpoint:

`289d7f4432efba4ad2bc1e97d5b23f14f587019e`

Source post-Batch05 progression/integration state:

`99c2f38842a0c4ea66ba6ff90496380986d02e52`

Source persisted-HEAD proof:

`70428e536689793a74420d35c84744b8ad0f2f3d`

Parent persisted state at freeze:

- recovery queue / unresolved window candidates: `49`;
- attempt ledger: `25`;
- material capability changes: `0`;
- same-capability BLOCKED / execution-ineligible: `6`;
- execution-eligible unresolved: `43`.

Every Batch 06 member was proven:

- unresolved;
- execution-eligible;
- `INITIAL_ATTEMPT`;
- absent from prior attempt ledger;
- unique;
- chronological.

## 5. BATCH 06 ADVERSARIAL MEMBERSHIP QUALIFICATION — PASS

First qualification run:

- run: `34951530594`
- job: `104323377439`
- trigger commit: `0aec58ccab9222b0e86c401b156a9cb965e1c974`
- result: `96 passed / 1 failed`

The single failure was a source-guard false positive, not a membership failure. The guard rejected the bare substring `eligible_recovery_queue`, which occurred only inside the immutable metadata constant:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

No live `eligible_recovery_queue()` or `recovery_queue()` call existed in the Batch 06 freeze module.

Minimal test-only correction:

`3ce94bb8c586fe4472ccf37d2a849f87bd9c03ef`

Corrected authoritative qualification:

- run: `34951726033`
- job: `104324020570`
- trigger commit: `6a85c1c4c7d8c38861626b3eb8367274f015d118`
- conclusion: SUCCESS
- adversarial/regression suite: `97 passed in 0.35s`
- baseline ancestry and governed-state immutability: PASS
- exact mechanically frozen membership assertion: PASS
- no-browser/no-probe path assertion: PASS
- read-only `git diff --exit-code`: PASS
- workflow permissions: `contents: read`, `metadata: read`

Final verdict:

**PASS — `BATCH06_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch06_policy_qualification.md`

The attacks cover at least:

- raw-queue substitution;
- skip;
- reorder;
- substitution with a later candidate;
- shortening/expansion;
- reinsertion of attempted BLOCKED dates;
- re-entry of already-resolved Batch 05 dates;
- duplicate/chronology defects;
- prior-attempt contamination;
- non-initial eligibility;
- caller mutation/selection surfaces;
- expected-outcome/manual-priority/manual-skip/holiday/source-availability paths;
- live queue selection in the frozen module;
- parent progression/protocol/calendar/boundary regressions.

## 6. BROWSER BOUNDARY — NO OBSERVATION YET

No Batch 06 historical broker observation occurred during membership freeze or qualification.

The freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio;
- live `eligible_recovery_queue()` call;
- live `recovery_queue()` call.

The qualification workflow installed pytest only.

Therefore no Batch 06 outcome is known or versioned yet.

## 7. STATE MUTATION BOUNDARY

Batch 06 membership PASS is scheduling/governance only.

It did not:

- resolve any calendar candidate;
- modify executable calendar evidence;
- populate negative evidence;
- append attempts;
- change capability identity;
- register capability changes;
- alter progression runtime;
- change global/window coverage counts.

Persisted executable state remains:

- global `111 / 42 resolved / 69 unresolved / 0 FAIL`;
- window `68 / 19 resolved / 49 unresolved / 0 FAIL`;
- ledger `25`;
- material changes `0`;
- attempted BLOCKED/ineligible `6`;
- eligible unresolved `43`.

The six unresolved same-capability BLOCKED dates remain:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Each remains `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`.

## 8. WORKFLOW CLOSURE

Completed Batch 06 membership qualification workflow is manual-only:

`.github/workflows/trading-breaks-recovery-batch06-policy.yml`

Archive commit:

`ee6dd4c12f07a0212241cd5e3826d14d956207ef`

No normal push may silently re-freeze or re-qualify historical Batch 06 membership.

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
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 10. WHAT MUST NOT BE REPEATED OR BYPASSED

- do not recalculate or rewrite frozen Batch 06 membership;
- do not substitute, skip, reorder, expand or shorten Batch 06;
- do not manually select Batch 06 members;
- do not retry the six same-capability BLOCKED dates without a separately qualified material capability change addressing their blocker;
- do not move the execution window;
- do not acquire massive `.bi5` data;
- do not start a real backtest.

## 11. EXACTLY ONE NEXT GOVERNED ACTION

**Execute exactly the five already-frozen Batch 06 dates under the qualified Trading Breaks capture chain, with parent protocol/progression/Batch06 gates PASS before Chromium opens, then independently adjudicate all five results.**

At execution time membership MUST come only from immutable `batch06_targets()` / `FROZEN_BATCH06_TARGETS`. It MUST NOT be recalculated from live `eligible_recovery_queue()` or raw `recovery_queue()`.

No `.bi5`. No real backtest.
