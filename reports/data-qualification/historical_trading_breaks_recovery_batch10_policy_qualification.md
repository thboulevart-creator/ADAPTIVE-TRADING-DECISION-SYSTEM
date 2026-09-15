# HISTORICAL TRADING BREAKS RECOVERY — BATCH 10 MEMBERSHIP QUALIFICATION

**PASS — `BATCH10_MEMBERSHIP_MECHANICALLY_FROZEN_AND_ADVERSARIALLY_QUALIFIED`**

- workflow run: `35003111213`
- job: `104496100100`
- trigger commit: `7ddfeb9c7954abf3057c3cd1a6fa3d36287cd66c`
- freeze baseline checkpoint: `7264970e0be56f3eb379f6647f8c353885f6e521`
- selection: `eligible_recovery_queue()[:5]`
- fixed batch size: `5`
- pre-freeze state: raw `34`, eligible `23`, attempts `45`, BLOCKED/ineligible `11`, capability changes `0`
- browser/probe/network observation during freeze: `NONE`
- governed calendar/ledger/progression mutation: `NONE`

## Frozen membership

1. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`
2. `2025-01-01 — NEW_YEARS_OBSERVED`
3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
4. `2025-02-17 — PRESIDENTS_DAY`
5. `2025-04-18 — GOOD_FRIDAY`

Adversarial rejection includes skip, reorder, later-member substitution, cardinality change, duplication, raw-queue bypass, same-capability BLOCKED reinsertion, resolved-date reinsertion and observation/outcome-dependent selection surfaces.

No `.bi5`. No real backtest.
