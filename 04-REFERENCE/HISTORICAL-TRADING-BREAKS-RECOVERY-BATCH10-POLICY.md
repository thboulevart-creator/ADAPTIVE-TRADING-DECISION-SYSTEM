# HISTORICAL TRADING BREAKS RECOVERY — BATCH 10 POLICY

Contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_POLICY_V1`

Parent progression contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

## Freeze status

**FROZEN — mechanically derived from persisted post-Batch09 `eligible_recovery_queue()[:5]`; no Batch 10 observation preceded this freeze.**

## Freeze provenance

- pre-freeze checkpoint HEAD: `7264970e0be56f3eb379f6647f8c353885f6e521`
- Batch 09 atomic integration commit: `126ff25129728dc9f5c26cfeff701c1e04270843`
- Batch 09 persisted-HEAD re-break trigger: `21965fd00fc92f606665b5db3c20c265b8ad83fe`
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- raw unresolved: `34`
- eligible unresolved: `23`
- historical attempts: `45`
- same-capability BLOCKED/ineligible: `11`
- material capability changes: `0`

## Fixed selection rule

`BATCH_SIZE = 5`

`eligible_recovery_queue()[:5]`

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Batch size and membership may not depend on expected outcome, holiday type, source availability, apparent difficulty, convenience, manual priority or browser observations.

## Frozen Batch 10 membership

1. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`
2. `2025-01-01 — NEW_YEARS_OBSERVED`
3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
4. `2025-02-17 — PRESIDENTS_DAY`
5. `2025-04-18 — GOOD_FRIDAY`

These identities and this order were emitted mechanically by the freeze generator from the governed eligible queue. No member was manually selected.

## Required qualification

The membership contract rejects skip, reorder, later-member substitution, cardinality change, duplication, raw-queue bypass, same-capability BLOCKED reinsertion, already-resolved reinsertion, prior-attempt contamination, manual selection and expected-outcome dependence.

The frozen module has no browser/probe/network path and no live call to either recovery queue.

No `.bi5`. No real backtest.
