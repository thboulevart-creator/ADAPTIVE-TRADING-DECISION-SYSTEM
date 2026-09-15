# SESSION BACKUP — 15 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY BATCH 10 ATOMIC INTEGRATION PASS

## Final verdict

**PASS — `BATCH10_ATOMIC_CALENDAR_ATTEMPT_PROGRESSION_INTEGRATION_COHERENT`**

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

## Authoritative evidence chain

Batch 10 immutable membership:

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
- persisted adjudication evidence: `77964da35adbff0e042061bbd977777df1ece0b8`
- result: `3 PASS / 2 BLOCKED / 0 FAIL`

## Atomic integration

Authoritative successful run/job:

`35006738066` / `104508270149`

Trigger commit:

`b720c7e6c357377b048245437d71d1015a9eee20`

Observed gates:

- preparation-only delta from adjudication checkpoint: PASS;
- pre-mutation contract/adjudication suite: `40 passed in 0.12s`;
- worktree integration prepared from persisted adjudication only: PASS;
- deterministic progression regeneration: PASS;
- exact post-state assertion: PASS;
- full governed/adversarial post-mutation regression: `458 passed in 1.82s`;
- no browser/probe/live-selection integration path: PASS;
- atomic persistence: PASS.

Atomic integration commit:

`6d2f60525fed9a56fd4ebab587ce7ba699cedbda`

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch10_integration_qualification.md`

Completed integration workflow archive:

`c9d847aea83131e20ecd3aef90c1b9c9e89b31f3`

## Persisted Batch 10 calendar truth

Exactly three Batch 10 targets entered executable special-session evidence:

1. `2024-12-31` — record `75799` — target-day whole closed UTC hours `[22,23]`.
2. `2025-01-20` — record `76806` — `[18,19,20,21,22]`.
3. `2025-02-17` — record `78513` — `[18,19,20,21,22]`.

The following two targets remain absent from both resolving evidence surfaces:

- `2025-01-01 — NEW_YEARS_OBSERVED` — overlap record `75799` starts on `2024-12-31`.
- `2025-04-18 — GOOD_FRIDAY` — overlap record `80057` starts on `2025-04-17`; DOM witness was absent.

They remain unresolved. No cross-date or missing-DOM evidence was promoted.

## Persisted Batch 10 attempt truth

Ledger total: `50` contiguous attempts.

Batch 10 tail, exact frozen order:

- `46 — batch10:2024-12-31 — PASS`
- `47 — batch10:2025-01-01 — BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`
- `48 — batch10:2025-01-20 — PASS`
- `49 — batch10:2025-02-17 — PASS`
- `50 — batch10:2025-04-18 — BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

All five retain the authoritative Batch 10 execution provenance.

## Deterministic post-state

- global coverage: `111 candidates / 60 resolved / 51 unresolved / 0 FAIL`
- execution-window candidate: `68 candidates / 37 resolved / 31 unresolved / 0 FAIL`
- raw unresolved queue: `31`
- attempt ledger: `50`
- material capability changes: `0`
- same-capability attempted BLOCKED/ineligible: `13`
- execution-eligible unresolved: `18`
- first eligible unresolved: `2025-05-26 — MEMORIAL_DAY`

Both Batch 10 BLOCKED dates have progression reason:

`SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

## Adversarial failure caught safely before authoritative integration

First integration run:

- run/job: `35006527120` / `104507544123`
- exact worktree post-state assertion: PASS
- full regression: `13 failed / 446 passed`
- persistence step: SKIPPED
- governed-state commit: NONE

The failures were migration-harness defects only:

1. stale historical/current-state BLOCKED count assertions still expected `11` instead of `13`;
2. an old Batch 09 integration contract was accidentally treated as mutable current-state assertion;
3. the preintegration guard was rerun after worktree integration and therefore correctly rejected an already-integrated worktree.

Corrections were minimal: migrate current-state BLOCKED counts, exclude historical `*_integration_contract.py` from state rewriting, and keep the preintegration guard as a pre-mutation workflow gate only. Then the whole integration was rerun from the untouched persisted pre-integration state and passed.

## Current downstream boundary

- Batch 10 membership: PASS.
- Batch 10 execution/capture: PASS.
- Batch 10 independent adjudication: PASS.
- Batch 10 atomic integration: PASS.
- Batch 10 independent persisted-HEAD re-break: **NOT YET RUN**.
- Batch 11 membership: **NOT FROZEN**.
- execution window frozen: NO.
- `.bi5`: FORBIDDEN.
- real backtest: NOT AUTHORIZED.

## Exactly one next governed action

**Perform an independent read-only persisted-HEAD re-break of Batch 10 atomic integration before any Batch 11 freeze.**

Required persisted invariants:

- exactly three Batch 10 calendar promotions;
- the two BLOCKED dates remain unresolved and absent from resolving evidence;
- ledger sequences `46..50` exact and provenance preserved;
- global `111/60/51`;
- window `68/37/31`;
- raw unresolved `31`;
- ledger `50`;
- BLOCKED/ineligible `13`;
- eligible `18`;
- capability changes `0`;
- progression regeneration byte-stable;
- verifier read-only and final worktree clean.

**Do not freeze Batch 11 before this persisted-HEAD re-break PASS.**

No `.bi5`. No real backtest.
