# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — TRADING BREAKS BATCH 10 ATOMIC INTEGRATION PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Persisted executable global calendar:** `111 candidates / 60 resolved / 51 unresolved / 0 FAIL`
- **Persisted executable candidate window:** `68 candidates / 37 resolved / 31 unresolved / 0 FAIL`
- **Historical Trading Breaks broker-evidence route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Attempt-aware recovery progression:** PASS
- **Recovery Batch 09:** fully closed through persisted-HEAD re-break PASS
- **Recovery Batch 10 membership:** frozen + adversarially qualified + persisted-membership re-break PASS
- **Recovery Batch 10 execution/capture:** PASS — capture only
- **Recovery Batch 10 independent adjudication:** PASS — `3 PASS / 2 BLOCKED / 0 FAIL`
- **Recovery Batch 10 atomic integration:** **PASS — `BATCH10_ATOMIC_CALENDAR_ATTEMPT_PROGRESSION_INTEGRATION_COHERENT`**
- **Recovery Batch 10 persisted-HEAD re-break:** NOT RUN
- **Batch 11 membership:** NOT FROZEN
- **Historical attempt ledger entries:** `50`
- **Registered material capability changes:** `0`
- **Attempted BLOCKED / same-capability execution-ineligible:** `13`
- **Execution-eligible unresolved:** `18`
- **Current semantic capability:** `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- **Capability fingerprint:** `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

Authoritative Batch 10 atomic integration commit:

`6d2f60525fed9a56fd4ebab587ce7ba699cedbda`

Authoritative integration run/job:

`35006738066` / `104508270149`

Latest durable backup:

`99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH10-INTEGRATION-PASS.md`

Backup commit:

`32974a43a9b28f77d0ea80a2aeef0983ea6af588`

Current boundary report commit:

`b03b87ae3fb87cfdaf006b3037e779d39f5baf5f`

Completed integration workflow archive commit:

`c9d847aea83131e20ecd3aef90c1b9c9e89b31f3`

## 2. MANDATORY RECOVERY ORDER

Before the next substantive write:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-15-TRADING-BREAKS-RECOVERY-BATCH10-INTEGRATION-PASS.md`
4. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
5. `reports/data-qualification/historical_trading_breaks_recovery_batch10_integration_qualification.md`
6. `tools/integrate_trading_breaks_recovery_batch10.py`
7. `tests/test_trading_breaks_recovery_batch10_integration_contract.py`
8. `tests/test_trading_breaks_recovery_batch10_integration.py`
9. `tests/test_dukascopy_usatech_calendar_2024_2025_batch10.py`
10. `reports/data-qualification/historical_trading_breaks_recovery_batch10_adjudication.json`
11. `reports/data-qualification/historical_trading_breaks_recovery_batch10_qualification.md`
12. `tools/trading_breaks_recovery_batch10_adjudication.py`
13. `tests/test_trading_breaks_recovery_batch10_adjudication.py`
14. `reports/data-qualification/historical_trading_breaks_recovery_batch10_runtime.json`
15. `reports/data-qualification/historical_trading_breaks_recovery_batch10_execution_qualification.md`
16. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH10-POLICY.md`
17. `tools/trading_breaks_recovery_batch10.py`
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

GitHub/checkpoint is source of truth. Do not reconstruct state from conversation memory.

## 3. BATCH 10 IMMUTABLE MEMBERSHIP

Frozen snapshot commit:

`65b789f310c066f90b39cd9e1ed69d2bd0962b6c`

Exact frozen order:

1. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`
2. `2025-01-01 — NEW_YEARS_OBSERVED`
3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
4. `2025-02-17 — PRESIDENTS_DAY`
5. `2025-04-18 — GOOD_FRIDAY`

## 4. AUTHORITATIVE BATCH 10 EXECUTION / ADJUDICATION

Execution:

- run/job: `35004172846` / `104499660140`
- probe commit: `443b3696e4e2740a54354787de231c886f90b26e`
- artifact: `10411022092`
- artifact SHA-256: `1572cc5a1c38998f59d32e107b1bcb006a74b288fe32c70ffe019726b3ad5f14`
- runtime persistence commit: `1134f96517157647d7663ce1ebaf045267e78bcb`

Independent adjudication:

- run/job: `35005525644` / `104504189641`
- persisted adjudication evidence: `77964da35adbff0e042061bbd977777df1ece0b8`
- verdict: `PASS — BATCH10_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_OR_MISSING_DOM_PROMOTION`
- result: `3 PASS / 2 BLOCKED / 0 FAIL`

Exact date-level outcomes:

1. `2024-12-31` → PASS — record `75799` — whole target-day UTC hours `[22,23]`.
2. `2025-01-01` → BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` — overlap `75799` starts `2024-12-31`.
3. `2025-01-20` → PASS — record `76806` — `[18,19,20,21,22]`.
4. `2025-02-17` → PASS — record `78513` — `[18,19,20,21,22]`.
5. `2025-04-18` → BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` — overlap `80057` starts `2025-04-17`; DOM absent.

## 5. BATCH 10 ATOMIC INTEGRATION — PASS

Authoritative successful trigger:

`b720c7e6c357377b048245437d71d1015a9eee20`

Authoritative run/job:

`35006738066` / `104508270149`

Observed gates:

- preparation-only delta from adjudication checkpoint: PASS;
- pre-mutation integration/adjudication suite: `40 passed in 0.12s`;
- worktree integration from persisted adjudication: PASS;
- deterministic progression regeneration: PASS;
- exact post-state assertion: PASS;
- full governed + adversarial post-mutation regression: **`458 passed in 1.82s`**;
- integration no-browser/no-probe/no-live-selection gate: PASS;
- atomic commit/push: PASS.

Atomic integration commit:

`6d2f60525fed9a56fd4ebab587ce7ba699cedbda`

Exactly three PASS dates entered executable calendar evidence:

- `2024-12-31`
- `2025-01-20`
- `2025-02-17`

`2025-01-01` and `2025-04-18` entered neither resolving evidence surface and remain unresolved.

Five factual attempts were appended in frozen order:

- `46 — batch10:2024-12-31 — PASS`
- `47 — batch10:2025-01-01 — BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`
- `48 — batch10:2025-01-20 — PASS`
- `49 — batch10:2025-02-17 — PASS`
- `50 — batch10:2025-04-18 — BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

For both Batch 10 BLOCKED targets:

- calendar state: `UNRESOLVED`;
- latest outcome: `BLOCKED`;
- eligible: `false`;
- reason: `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`;
- contract verdict: `PASS`.

## 6. ADVERSARIAL INTEGRATION HISTORY

First integration run:

`35006527120` / `104507544123`

It proved the exact requested worktree post-state before failing the full regression. No commit/push occurred.

Failure accounting:

`13 failed / 446 passed`

All failures were migration-harness defects, not data or governance-state defects:

- stale BLOCKED-count assertions expected `11` instead of `13`;
- an old Batch 09 integration contract was accidentally rewritten as if it were current-state evidence;
- the Batch 10 preintegration guard was rerun after worktree mutation and therefore correctly rejected the integrated worktree.

Minimal corrections:

- current-state BLOCKED assertions migrated to `13`;
- all historical `*_integration_contract.py` files excluded from state migration;
- the preintegration guard retained only as a pre-mutation gate.

The complete chain was then rerun from the untouched persisted pre-integration state and passed fully. Only that successful second run produced the atomic integration commit.

## 7. DETERMINISTIC POST-BATCH10 STATE

Persisted progression:

- calendar unresolved: `31`
- attempt ledger: `50`
- material capability changes: `0`
- same-capability attempted BLOCKED/ineligible: `13`
- execution-eligible unresolved: `18`

Persisted accounting:

- global: `111 / 60 resolved / 51 unresolved / 0 FAIL`
- execution window: `68 / 37 resolved / 31 unresolved / 0 FAIL`

First currently execution-eligible unresolved candidate:

`2025-05-26 — MEMORIAL_DAY`

This is a progression fact only. **Batch 11 has NOT been frozen.**

## 8. CURRENT DOWNSTREAM BOUNDARY

PASS now includes:

- all completed Batch 01–09 gates;
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_POLICY`;
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_PERSISTED_MEMBERSHIP_REBREAK`;
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_EXECUTION_CAPTURE`;
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_INDEPENDENT_ADJUDICATION`;
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_ATOMIC_INTEGRATION`.

Still pending/BLOCKED:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_PERSISTED_HEAD_REBREAK — NOT RUN`;
- `DECLARE_GLOBAL_COVERAGE_PASS — GLOBAL_UNRESOLVED_REMAINS_51`;
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_31_UNRESOLVED_DATES`;
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`;
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`.

No `.bi5`. No real backtest.

## 9. EXACTLY ONE NEXT GOVERNED ACTION

**Perform an independent read-only persisted-HEAD re-break of the Batch 10 atomic integration before any Batch 11 freeze.**

Mandatory persisted assertions:

- atomic integration commit `6d2f60525fed9a56fd4ebab587ce7ba699cedbda` is an ancestor;
- exactly three Batch 10 PASS dates exist in executable calendar evidence;
- `2025-01-01` and `2025-04-18` remain absent from both resolving evidence surfaces;
- ledger sequences `46..50` are contiguous, unique, in frozen order, and retain exact execution provenance;
- global accounting is exactly `111/60/51`;
- execution-window accounting is exactly `68/37/31`;
- raw unresolved is `31`;
- ledger is `50`;
- same-capability BLOCKED/ineligible is `13`;
- eligible unresolved is `18`;
- capability changes remain `0`;
- both Batch 10 BLOCKED targets remain `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`;
- progression regeneration is byte-stable;
- verifier has `contents: read`, performs no browser/probe/integration and leaves a clean worktree.

**Batch 11 MUST NOT be frozen before this persisted-HEAD re-break PASS.**

No `.bi5`. No real backtest.
