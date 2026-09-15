# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 10 atomic integration PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 60 resolved / 51 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 37 resolved / 31 unresolved / 0 FAIL**
- Historical Trading Breaks broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Attempt-aware recovery progression: **PASS**
- Historical attempt ledger entries: **50**
- Registered material capability changes: **0**
- Attempted BLOCKED / same-capability execution-ineligible: **13**
- Execution-eligible unresolved: **18**
- Current semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- Capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- Batch 09: **FULLY CLOSED THROUGH PERSISTED-HEAD RE-BREAK PASS**
- Batch 10 membership: **FROZEN + ADVERSARIALLY QUALIFIED + PERSISTED-MEMBERSHIP RE-BREAK PASS**
- Batch 10 execution/capture: **PASS — CAPTURE ONLY**
- Batch 10 independent adjudication: **PASS — `3 PASS / 2 BLOCKED / 0 FAIL`**
- Batch 10 atomic integration: **PASS — `BATCH10_ATOMIC_CALENDAR_ATTEMPT_PROGRESSION_INTEGRATION_COHERENT`**
- Batch 10 persisted-HEAD re-break: **NOT YET RUN**
- Batch 11 membership: **NOT FROZEN**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 10 immutable membership and evidence chain

Frozen order:

1. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`
2. `2025-01-01 — NEW_YEARS_OBSERVED`
3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
4. `2025-02-17 — PRESIDENTS_DAY`
5. `2025-04-18 — GOOD_FRIDAY`

Frozen snapshot commit: `65b789f310c066f90b39cd9e1ed69d2bd0962b6c`.

Execution provenance:

- run/job: `35004172846` / `104499660140`
- probe commit: `443b3696e4e2740a54354787de231c886f90b26e`
- artifact: `10411022092`
- artifact SHA-256: `1572cc5a1c38998f59d32e107b1bcb006a74b288fe32c70ffe019726b3ad5f14`
- runtime persistence commit: `1134f96517157647d7663ce1ebaf045267e78bcb`

Independent adjudication:

- run/job: `35005525644` / `104504189641`
- persisted evidence commit: `77964da35adbff0e042061bbd977777df1ece0b8`
- result: `3 PASS / 2 BLOCKED / 0 FAIL`

Exact adjudicated PASS targets:

- `2024-12-31` — record `75799` — fully closed target-day UTC hours `[22,23]`;
- `2025-01-20` — record `76806` — `[18,19,20,21,22]`;
- `2025-02-17` — record `78513` — `[18,19,20,21,22]`.

Exact adjudicated BLOCKED targets:

- `2025-01-01` — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` — overlap record `75799` begins on `2024-12-31`;
- `2025-04-18` — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` — overlap record `80057` begins on `2025-04-17`; DOM witness also absent.

## Batch 10 atomic integration — PASS

Authoritative successful integration:

- trigger commit: `b720c7e6c357377b048245437d71d1015a9eee20`
- run/job: `35006738066` / `104508270149`
- pre-mutation contract/adjudication suite: **`40 passed in 0.12s`**
- exact worktree post-state assertion: PASS
- full governed + adversarial post-mutation regression: **`458 passed in 1.82s`**
- integration offline/no-live-selection guard: PASS
- atomic integration commit: `6d2f60525fed9a56fd4ebab587ce7ba699cedbda`
- integration qualification report: `reports/data-qualification/historical_trading_breaks_recovery_batch10_integration_qualification.md`
- completed integration workflow archive commit: `c9d847aea83131e20ecd3aef90c1b9c9e89b31f3`

Only the three adjudicated PASS targets entered executable special-session evidence. `2025-01-01` and `2025-04-18` entered neither resolving evidence surface.

Five factual attempts were appended in immutable frozen order:

- `46 — batch10:2024-12-31 — PASS`
- `47 — batch10:2025-01-01 — BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`
- `48 — batch10:2025-01-20 — PASS`
- `49 — batch10:2025-02-17 — PASS`
- `50 — batch10:2025-04-18 — BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

The two BLOCKED targets remain:

- calendar state: `UNRESOLVED`;
- absent from `SPECIAL_SESSION_EVIDENCE`;
- absent from `NO_SPECIAL_CHANGE_EVIDENCE`;
- latest attempt outcome: `BLOCKED`;
- eligibility: `false`;
- progression reason: `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`.

Current eligible queue contains `18` targets and begins at `2025-05-26 — MEMORIAL_DAY`. This is only a progression fact; it is **not** a Batch 11 freeze.

## Adversarial integration history

The first integration run `35006527120` / job `104507544123` failed before persistence after the exact worktree post-state had already passed. The full regression exposed only migration-harness defects: stale BLOCKED-count assertions (`11` instead of `13`), accidental rewriting of a historical Batch 09 integration contract, and a preintegration guard being rerun after worktree mutation. No governed state was committed by that failed run.

Those harness defects were corrected minimally, and the complete integration chain was rerun from the still-intact pre-integration persisted state. The authoritative second run passed all gates and alone produced the atomic integration commit.

## Current downstream boundary

PASS now includes:

- all completed Batch 01–09 recovery/integration gates;
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

## Exactly one next governed action

**Perform an independent read-only persisted-HEAD re-break of the Batch 10 atomic integration before any Batch 11 freeze.**

It must independently prove from the actually persisted branch state:

- exactly three Batch 10 calendar promotions and no blocked-date promotion;
- attempt sequences `46..50` and provenance are exact;
- global accounting `111/60/51`;
- execution-window accounting `68/37/31`;
- raw unresolved `31`;
- ledger `50`;
- same-capability BLOCKED/ineligible `13`;
- eligible unresolved `18`;
- capability changes `0`;
- `2025-01-01` and `2025-04-18` remain unresolved/ineligible;
- progression regeneration is byte-stable;
- verifier is strictly read-only and leaves a clean worktree.

**Batch 11 MUST NOT be frozen before this persisted-HEAD re-break PASS.**
