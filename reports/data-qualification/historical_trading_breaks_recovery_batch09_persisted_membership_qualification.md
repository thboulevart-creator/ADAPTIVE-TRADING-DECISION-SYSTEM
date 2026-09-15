# HISTORICAL TRADING BREAKS RECOVERY — BATCH 09 PERSISTED MEMBERSHIP RE-BREAK

**PASS — `BATCH09_FROZEN_MEMBERSHIP_SURVIVES_INDEPENDENT_PERSISTED_HEAD_REBREAK`**

- mechanically frozen snapshot commit: `20a2c1722a2bc4798c0e5079ba51aa1f7bb5edb5`
- independent verifier trigger commit: `1a8953d0d589e904bb465f0206bfa97ea05f73b4`
- independent workflow run: `34992441792`
- independent job: `104460203391`
- permissions: `contents: read`
- governed regression: `351 passed in 1.55s`
- persisted selection invariant: `batch09_targets() == eligible_recovery_queue()[:5]`
- pre-execution state: raw unresolved `38`, eligible unresolved `28`, historical attempts `40`, same-capability BLOCKED/ineligible `10`, material capability changes `0`
- all five frozen members remain unresolved `INITIAL_ATTEMPT` candidates with no prior factual attempt
- frozen production module has no browser/probe/live-selection path
- progression regeneration produced no tracked diff
- independent verifier remained read-only with a clean worktree
- no Chromium opened; no `.bi5`; no real backtest

## Frozen Batch 09 membership

1. `2024-09-02 — LABOR_DAY`
2. `2024-11-28 — THANKSGIVING_DAY`
3. `2024-11-29 — THANKSGIVING_FRIDAY`
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2024-12-25 — CHRISTMAS_OBSERVED`

The five members above are the persisted result of the mechanical freeze. They were not manually selected; the freeze generator computed the fixed-size prefix of the governed attempt-aware eligible queue before any observation.