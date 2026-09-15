# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 08 MEMBERSHIP PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Persisted executable global calendar:** `111 candidates / 49 resolved / 62 unresolved / 0 FAIL`
- **Persisted executable candidate window:** `68 candidates / 26 resolved / 42 unresolved / 0 FAIL`
- **Historical Trading Breaks broker-evidence route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Attempt-aware recovery progression:** PASS
- **Recovery Batch 01:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`)
- **Recovery Batch 02:** PASS (`2 PASS / 3 BLOCKED / 0 FAIL`)
- **Recovery Batch 03:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) and integrated
- **Recovery Batch 04:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 05:** PASS (`5 PASS / 0 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 06:** PASS (`4 PASS / 1 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 07:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`) and integrated + persisted-HEAD re-break PASS
- **Recovery Batch 08 membership:** PASS — immutable and frozen before observation
- **Historical attempt ledger entries:** `35`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `9`
- **Execution-eligible unresolved:** `33`
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH08-MEMBERSHIP-PASS.md`

Backup commit:

`c6f8be6732f30747f241406f3fdfced888e2bb5f`

Current boundary report commit:

`09a742c630aa8e33e3285860d369520dbb7ba3f4`

## 2. MANDATORY RECOVERY ORDER

Before the next substantive write:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH08-MEMBERSHIP-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH08-POLICY.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch08_policy_qualification.md`
7. `tools/trading_breaks_recovery_batch08.py`
8. `tests/test_trading_breaks_recovery_batch08.py`
9. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`
10. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
11. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`
12. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`
13. `tools/trading_breaks_recovery_progression.py`
14. `tests/test_trading_breaks_recovery_progression.py`
15. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
16. `tools/trading_breaks_recovery_protocol.py`
17. `tests/test_trading_breaks_recovery_protocol.py`
18. `tools/dukascopy_usatech_calendar.py`
19. `tools/dukascopy_usatech_calendar_coverage.py`
20. `tests/test_dukascopy_usatech_calendar_coverage.py`
21. `tests/test_coverage_execution_window_boundary.py`
22. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is source of truth. Do not reconstruct state from conversation memory.

## 3. POST-BATCH07 SOURCE STATE

Authoritative Batch 07 atomic integration commit:

`616643e2bfd0b8a8ae3f21352554dc32fdbb503d`

Independent Batch 07 persisted-HEAD proof trigger commit:

`b4a2f3400b0629e7b1d0a715320735f74293b15a`

Batch 07 final state remains:

- global `111 / 49 resolved / 62 unresolved / 0 FAIL`
- execution window `68 / 26 resolved / 42 unresolved / 0 FAIL`
- ledger `35`
- material capability changes `0`
- BLOCKED/ineligible `9`
- eligible unresolved `33`

No post-Batch07 governed parent state was changed during Batch 08 membership freeze.

## 4. BATCH 08 FROZEN MEMBERSHIP

Freeze baseline checkpoint:

`2e9e51cea8342c701eec14d8d86aca215c5b7b62`

Batch size:

`5`

Selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Equivalent freeze assertion:

`batch08_targets() == eligible_recovery_queue()[:5]`

Frozen immutable membership:

1. `2024-03-29 — GOOD_FRIDAY`
2. `2024-05-27 — MEMORIAL_DAY`
3. `2024-06-19 — JUNETEENTH_OBSERVED`
4. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
5. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`

Production freeze module:

`tools/trading_breaks_recovery_batch08.py`

The production module stores the immutable snapshot and contains no live `eligible_recovery_queue()` or raw `recovery_queue()` selection call.

## 5. BATCH 08 ADVERSARIAL MEMBERSHIP QUALIFICATION — PASS

Authoritative qualification:

- run `34967834638`
- job `104376461078`
- trigger commit `7e0fc3268d6ec202267ecf71efe69b0e593be4ea`
- conclusion `SUCCESS`
- `307 passed in 1.46s`
- token permissions `contents: read`, `metadata: read`
- final `git diff --exit-code` PASS

Proven controls:

- exact governed eligible prefix PASS;
- all five frozen members are unresolved `INITIAL_ATTEMPT` targets;
- none has a prior factual attempt;
- chronology and uniqueness PASS;
- raw unresolved queue substitution rejected;
- skip/reorder/later-substitution/shorten/expand variants rejected;
- all nine same-capability attempted BLOCKED dates remain unresolved but excluded;
- Batch 07 resolved PASS dates remain excluded;
- parent protocol/progression/calendar/coverage regressions PASS;
- no browser/probe/live-selection/manual-priority path in the freeze module;
- read-only qualification PASS.

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch08_policy_qualification.md`

Policy:

`04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH08-POLICY.md`

## 6. BROWSER / MUTATION BOUNDARY

No Batch 08 historical broker observation occurred during freeze or qualification.

The membership block did not:

- change executable calendar evidence;
- append a factual attempt;
- change the capability registry;
- mutate progression runtime;
- alter coverage counts;
- freeze the execution window;
- authorize `.bi5` acquisition;
- authorize a real backtest.

## 7. WORKFLOW CLOSURE

`.github/workflows/trading-breaks-recovery-batch08-policy.yml` is archived to `workflow_dispatch` only.

Normal pushes cannot silently re-freeze or re-qualify Batch 08 membership.

## 8. CURRENT DOWNSTREAM BOUNDARY

PASS now includes:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY`

Still BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 9. EXACTLY ONE NEXT GOVERNED ACTION

**Execute exactly the already-frozen Batch 08 membership under the qualified Trading Breaks capture chain, with parent protocol/progression/Batch08 gates PASS before Chromium opens, then independently adjudicate all five results.**

At execution time:

- membership MUST come from `batch08_targets()` / `FROZEN_BATCH08_TARGETS`;
- do not recalculate membership from live `eligible_recovery_queue()`;
- do not use raw `recovery_queue()`;
- do not substitute, reorder, skip, expand or shorten dates;
- do not alter the execution window;
- no `.bi5`;
- no real backtest.
