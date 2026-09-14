# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — TRADING BREAKS BATCH 04 INTEGRATION PASS

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

Authoritative independent persisted-state verification commit:

`9ad19ede0052f37ce8aa2ccd30a117cd0525bc10`

Session backup immediately preceding this checkpoint:

`99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH04-INTEGRATION-PASS.md`

Backup commit:

`797fcef1f1df92eb8c6b8b7f29aa09d881d90bb5`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-BATCH04-INTEGRATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `reports/data-qualification/historical_trading_breaks_recovery_batch04_integration_qualification.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch04_qualification.md`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch04_adjudication.json`
8. `reports/data-qualification/historical_trading_breaks_recovery_batch04_runtime.json`
9. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH04-POLICY.md`
10. `tools/trading_breaks_recovery_batch04.py`
11. `tools/trading_breaks_recovery_batch04_execute.py`
12. `tools/trading_breaks_recovery_batch04_adjudication.py`
13. `tools/integrate_trading_breaks_recovery_batch04.py`
14. `tests/test_trading_breaks_recovery_batch04.py`
15. `tests/test_trading_breaks_recovery_batch04_adjudication.py`
16. `tests/test_trading_breaks_recovery_batch04_integration_contract.py`
17. `tests/test_trading_breaks_recovery_batch04_integration.py`
18. `tests/test_dukascopy_usatech_calendar_2022_batch04.py`
19. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
20. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
21. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
22. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
23. `tools/trading_breaks_recovery_progression.py`
24. `tests/test_trading_breaks_recovery_progression.py`
25. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
26. `tools/trading_breaks_recovery_protocol.py`
27. `tests/test_trading_breaks_recovery_protocol.py`
28. `tools/dukascopy_usatech_calendar.py`
29. `tools/dukascopy_usatech_calendar_coverage.py`
30. `tests/test_dukascopy_usatech_calendar_coverage.py`
31. `tests/test_coverage_execution_window_boundary.py`
32. `LOCAL-EVIDENCE/README.md`
33. `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`
34. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is the source of truth. Do not reconstruct this work from conversational memory.

## 3. BATCH 04 HISTORICAL MEMBERSHIP REMAINS IMMUTABLE

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1`

Frozen membership:

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

This membership was frozen before observation and MUST NOT be recalculated, replaced, reordered, expanded, shortened, or rewritten by later batches.

## 4. BATCH 04 AUTHORITATIVE EVIDENCE CHAIN

Browser execution:
- run: `34895457466`
- job: `104148201341`
- probe commit: `11a81294720898802e49dd1131a64e20e7e7ae3a`
- artifact: `10369230708`
- artifact SHA-256: `3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc`
- pre-browser suite: `110 passed in 0.59s`

Independent adjudication:
- run: `34895985689`
- job: `104149952523`
- adversarial suite: `81 passed in 0.27s`
- verdict: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**

PASS records:
- `2022-11-24` → record `45119`, fully closed UTC hours `18–22`;
- `2022-11-25` → record `45120`, fully closed target-day UTC hours `19–23`;
- `2022-12-23` → record `46756`, fully closed target-day UTC hours `22–23`.

BLOCKED records:
- `2022-12-26` → `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`;
- `2023-01-02` → `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`.

The two BLOCKED dates remain unresolved. Cross-date overlap is not exact-target proof and is not negative evidence.

## 5. BATCH 04 ATOMIC INTEGRATION

Final contract verdict:

**PASS — `BATCH04_ATOMIC_CALENDAR_ATTEMPT_PROGRESSION_INTEGRATION_COHERENT`**

The first integration attempt:
- run: `34896890735`
- job: `104153120649`
- stopped before mutation;
- cause: self-referential false-positive guard finding the literal `playwright` only inside generated future test text;
- no calendar, ledger, progression, or integration commit was produced.

Minimal correction:
- commit: `7dd9a0dcc938d13b018be14436a35b6b79ed5146`;
- guard scoped to callable integration runtime;
- no integration semantic rule weakened.

Authoritative corrected integration:
- run: `34896951616`
- job: `104153317098`
- pre-mutation adversarial suite: `79 passed in 0.35s`
- post-mutation adversarial/regression suite: `139 passed in 1.23s`
- exact worktree accounting assertion: PASS
- atomic integration commit: `6cafa5337f28c5424cbcc25280c690de702061d9`

That single atomic commit persisted together:
- only the three independently adjudicated PASS calendar records;
- all five factual Batch 04 attempts as attempt sequences `16..20`;
- regenerated progression runtime;
- updated state-sensitive regressions and Batch 04 integration proofs.

No partial calendar/ledger state was accepted.

## 6. ATTEMPT-AWARE PROGRESSION AFTER BATCH 04

Persisted deterministic state:
- calendar unresolved: `54`
- historical attempts: `20`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `6`
- execution-eligible unresolved: `48`

The six same-capability attempted BLOCKED dates remain unresolved but are not execution-eligible:
- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Each is classified:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

No retry is authorized under the unchanged capability.

## 7. INDEPENDENT PERSISTED-HEAD RE-BREAK

The integration push was produced by GitHub Actions using `GITHUB_TOKEN`; GitHub therefore correctly suppressed recursive workflow execution. An evidence-only trigger commit changed no executable state and provoked the separately versioned read-only verifier.

Authoritative proof:
- exact verified commit: `9ad19ede0052f37ce8aa2ccd30a117cd0525bc10`
- run: `34897126921`
- job: `104153918828`
- conclusion: **SUCCESS**
- regression suite: `139 passed in 0.73s`
- exact persisted calendar / ledger / progression assertion: PASS
- read-only proof `git diff --exit-code`: PASS
- verifier token permissions: `contents: read`

The persisted-HEAD proof independently confirms:
- global `111 / 37 / 74`;
- execution window `68 / 14 / 54`;
- ledger `20`;
- six same-capability attempted BLOCKED dates ineligible;
- `48` eligible unresolved dates;
- no Batch 04 BLOCKED promotion;
- no worktree mutation by the verifier.

## 8. WORKFLOW CLOSURE

Completed Batch 04 workflows are archived/manual-only. In particular:
- `.github/workflows/trading-breaks-recovery-batch04-integration.yml` → `workflow_dispatch` only;
- `.github/workflows/trading-breaks-recovery-batch04-persisted-head.yml` → `workflow_dispatch` only.

No normal push can silently repeat the completed Batch 04 integration or its fixed-state verifier.

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
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 10. WHAT MUST NOT BE REPEATED

- do not rerun Batch 04 browser execution or integration merely because a new batch will be prepared;
- do not recalculate or rewrite historical Batch 04 membership;
- do not promote `2022-12-26` or `2023-01-02` from cross-date overlap;
- do not make any of the six attempted BLOCKED dates retryable without a qualified material capability change;
- do not derive Batch 05 from conversational memory or raw `recovery_queue()`;
- do not move the execution window;
- do not acquire massive `.bi5` data;
- do not start a real backtest.

## 11. EXACTLY ONE NEXT GOVERNED ACTION

**Freeze and version Batch 05 membership from the governed post-Batch04 `eligible_recovery_queue()`, then adversarially qualify that immutable membership before any browser observation.**

At that next action, membership must be mechanically derived from the persisted repository state and frozen before any outcome observation. Do not preselect dates from conversational memory. Raw `recovery_queue()`, expected outcomes, source availability, holiday type preference, or manual convenience are inadmissible selection surfaces.

No Chromium belongs to the membership-freeze step. No `.bi5`. No real backtest.
