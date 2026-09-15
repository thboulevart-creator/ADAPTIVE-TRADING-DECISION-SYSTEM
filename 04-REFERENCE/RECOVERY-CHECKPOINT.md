# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 07 ATOMIC INTEGRATION + PERSISTED-HEAD RE-BREAK PASS

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
- **Recovery Batch 07:** PASS (`3 PASS / 2 BLOCKED / 0 FAIL`) and atomically integrated + persisted-HEAD re-break PASS
- **Historical attempt ledger entries:** `35`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / execution-ineligible:** `9`
- **Execution-eligible unresolved:** `33`
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Batch 08 membership:** NOT FROZEN
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH07-INTEGRATION-PASS.md`

Backup commit:

`4365d10607730b667f582c3d2e8eb09a2a95fd98`

Current boundary report commit:

`dd27f51e37db447234f76bbab88b4dbbe2c0ad06`

## 2. MANDATORY RECOVERY ORDER

Before the next substantive write:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH07-INTEGRATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `reports/data-qualification/historical_trading_breaks_recovery_batch07_integration_qualification.md`
6. `reports/data-qualification/historical_trading_breaks_recovery_batch07_adjudication.json`
7. `reports/data-qualification/historical_trading_breaks_recovery_batch07_qualification.md`
8. `reports/data-qualification/historical_trading_breaks_recovery_batch07_runtime.json`
9. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH07-POLICY.md`
10. `tools/trading_breaks_recovery_batch07.py`
11. `tools/trading_breaks_recovery_batch07_execute.py`
12. `tools/trading_breaks_recovery_batch07_adjudication.py`
13. `tools/integrate_trading_breaks_recovery_batch07.py`
14. `tests/test_trading_breaks_recovery_batch07.py`
15. `tests/test_trading_breaks_recovery_batch07_adjudication.py`
16. `tests/test_trading_breaks_recovery_batch07_integration_contract.py`
17. `tests/test_trading_breaks_recovery_batch07_integration.py`
18. `tests/test_dukascopy_usatech_calendar_2023_2024_batch07.py`
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
32. compare active branch HEAD against the commit containing this checkpoint before any write.

GitHub/checkpoint is source of truth. Do not reconstruct state from conversation memory.

## 3. BATCH 07 AUTHORITATIVE EVIDENCE

Frozen membership:

1. `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`
2. `2023-12-25 — CHRISTMAS_OBSERVED`
3. `2024-01-01 — NEW_YEARS_OBSERVED`
4. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
5. `2024-02-19 — PRESIDENTS_DAY`

Browser execution:

- run `34958083459`
- job `104344855871`
- artifact `10392510730`
- artifact SHA-256 `0df18b4bfcae04c0bf5e3670e789fc1253fde7317a50d108b35e10dd1cc2676a`
- probe commit `3d434dda9bd293d48cbe2f35df3d464abd5938a4`

Independent adjudication:

- run `34958613649`
- job `104346566865`
- result `3 PASS / 2 BLOCKED / 0 FAIL`
- final adjudication persistence commit `2551595485923931cd47028cbc741f2f5580b6c3`

Date-level outcomes:

- `2023-12-22` — PASS — record `63023`
- `2023-12-25` — BLOCKED `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` — overlap record `63023` starts `2023-12-22`
- `2024-01-01` — BLOCKED `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` — overlap record `63024` starts `2023-12-29`
- `2024-01-15` — PASS — record `63883`
- `2024-02-19` — PASS — record `65120`

Cross-date overlaps were not promoted to exact-target PASS.

## 4. BATCH 07 ATOMIC INTEGRATION — PASS

Final authoritative integration run:

- run `34962174847`
- job `104358082938`
- atomic integration commit `616643e2bfd0b8a8ae3f21352554dc32fdbb503d`
- full regression `297 passed in 1.43s`
- exact integrated-state assertion PASS
- forbidden negative-evidence/browser/capture integration-path assertion PASS

Atomic mutation:

- added only these PASS dates to executable calendar evidence:
  - `2023-12-22`
  - `2024-01-15`
  - `2024-02-19`
- appended all five Batch 07 factual attempts as sequences `31..35`;
- retained `2023-12-25` and `2024-01-01` unresolved;
- added neither BLOCKED date to `SPECIAL_SESSION_EVIDENCE`;
- added neither BLOCKED date to `NO_SPECIAL_CHANGE_EVIDENCE`;
- regenerated progression;
- registered no material semantic capability change.

Post-integration progression:

- unresolved calendar candidates `42`
- attempt ledger `35`
- material capability changes `0`
- attempted BLOCKED/ineligible `9`
- eligible unresolved `33`
- first eligible unresolved `2024-03-29 — GOOD_FRIDAY`

Both Batch 07 BLOCKED dates are now:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

under unchanged capability.

## 5. ADVERSARIAL INTEGRATION CORRECTIONS CAUGHT SAFELY

Two migration defects were exposed before the governed atomic commit:

1. The preparatory correction originally assumed one historical Batch05 ledger assertion; two existed. Run stopped with `BATCH05_OLD_TUPLE_COUNT:2` before governed mutation.
2. After that minimal correction, full regression reached `296 PASS / 1 FAIL` because `tests/test_trading_breaks_recovery_batch05_integration.py` retained one stale `len(attempts) == 30` assertion. Again, no governed atomic integration commit was produced.

Minimal source corrections:

- `56ae3fea6ff24e42feeb80f621729e6949f83251`
- `f4af31c41f38d2d53478b6954c56997519df1d99`

They affected test/state-migration mechanics only and did not weaken evidence semantics. Each correction was re-broken before governed mutation.

## 6. INDEPENDENT PERSISTED-HEAD RE-BREAK — PASS

Verifier trigger commit:

`b4a2f3400b0629e7b1d0a715320735f74293b15a`

Authoritative verifier:

- run `34962331347`
- job `104358587801`
- `contents: read`
- exact detached persisted HEAD checkout
- integrated commit `616643e2...` ancestry PASS
- governed-state immutability since integration commit PASS
- full regression `297 passed in 1.47s`
- exact persisted-state accounting PASS
- deterministic progression regeneration PASS
- progression-runtime `git diff --exit-code` PASS
- final read-only worktree `git diff --exit-code` PASS

Independent persisted proof:

**PASS — `BATCH07_ATOMIC_INTEGRATION_PERSISTED_HEAD_REBREAK_COHERENT`**

The verifier independently confirmed:

- global `111 / 49 resolved / 62 unresolved / 0 FAIL`
- execution window `68 / 26 resolved / 42 unresolved / 0 FAIL`
- ledger `35`
- capability changes `0`
- BLOCKED/ineligible `9`
- eligible unresolved `33`
- three Batch 07 PASS dates resolved
- two Batch 07 BLOCKED dates unresolved and execution-ineligible
- no negative evidence for either Batch 07 BLOCKED date.

## 7. WORKFLOW CLOSURE

The following Batch 07 workflow paths are archived to `workflow_dispatch` only:

- `.github/workflows/trading-breaks-recovery-batch07-integration.yml`
- `.github/workflows/trading-breaks-recovery-batch07-integration-resume.yml`
- `.github/workflows/trading-breaks-recovery-batch07-persisted-head.yml`

Normal pushes cannot silently replay Batch 07 integration or its persisted verifier.

## 8. CURRENT DOWNSTREAM BOUNDARY

Still BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

No `.bi5` acquisition has been authorized or performed by this workstream. No real backtest has been authorized or performed.

## 9. EXACTLY ONE NEXT GOVERNED ACTION

**Freeze and version Batch 08 membership mechanically from the governed post-Batch07 `eligible_recovery_queue()`, then adversarially qualify that immutable membership before any browser observation.**

Rules:

- derive membership from persisted post-Batch07 state only;
- do not preselect dates from conversation memory;
- do not use raw `recovery_queue()`;
- do not use expected outcomes, source availability, holiday preference or manual convenience;
- freeze/version membership before observation;
- no Chromium in membership-freeze qualification;
- do not execute Batch 08 browser observation until membership qualification PASS;
- no `.bi5`;
- no real backtest;
- same branch; no auxiliary branch proliferation.
