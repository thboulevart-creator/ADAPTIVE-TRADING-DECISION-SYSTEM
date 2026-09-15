# HISTORICAL TRADING BREAKS RECOVERY — BATCH 10 PERSISTED MEMBERSHIP RE-BREAK

**PASS — `BATCH10_PERSISTED_MEMBERSHIP_REBREAK_CONFIRMS_FROZEN_PREFIX`**

## Authoritative verifier

- freeze baseline checkpoint: `7264970e0be56f3eb379f6647f8c353885f6e521`
- mechanical freeze trigger: `7ddfeb9c7954abf3057c3cd1a6fa3d36287cd66c`
- persisted snapshot commit: `65b789f`
- freeze run/job: `35003111213` / `104496100100`
- independent verifier trigger: `865e962202c76de266bcdb6f18feb9bfe914e4d6`
- independent verifier run/job: `35003238287` / `104496526561`
- verifier permissions: `contents: read`
- full governed regression: `415 passed in 2.15s`
- deterministic progression regeneration: byte-stable
- final worktree: clean
- browser/probe/network observation: `NONE`
- governed calendar/ledger/progression mutation: `NONE`

## Immutable Batch 10 membership

The persisted snapshot independently equals the governed post-Batch09 `eligible_recovery_queue()[:5]` with fixed batch size `5`:

1. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`
2. `2025-01-01 — NEW_YEARS_OBSERVED`
3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
4. `2025-02-17 — PRESIDENTS_DAY`
5. `2025-04-18 — GOOD_FRIDAY`

All five are unresolved, execution-eligible, chronologically selected, `INITIAL_ATTEMPT`, without prior attempt history, and absent from resolving calendar evidence.

## Adversarial selection boundary

The freeze qualification rejected:

- first-member skip;
- reorder;
- later eligible substitution;
- batch shortening or expansion;
- duplicate target dates;
- raw recovery-queue bypass;
- same-capability BLOCKED reinsertion;
- resolved-date reinsertion;
- observation/outcome-dependent selection surfaces.

The generated frozen module has no live recovery-queue call, no progression scheduling call, and no browser/probe/network surface.

## Persisted pre-observation state

- raw unresolved queue: `34`
- execution-eligible unresolved: `23`
- historical attempts: `45`
- same-capability BLOCKED/ineligible: `11`
- material capability changes: `0`
- global accounting: `111 / 57 resolved / 54 unresolved / 0 FAIL`
- execution-window accounting: `68 / 34 resolved / 34 unresolved / 0 FAIL`

Batch 10 has **not** been executed. No Chromium or Playwright was opened during membership qualification or re-break.

No `.bi5`. No real backtest.
