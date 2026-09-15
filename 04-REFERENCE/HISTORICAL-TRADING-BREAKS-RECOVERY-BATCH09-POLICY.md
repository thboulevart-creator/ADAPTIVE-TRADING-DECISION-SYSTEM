# HISTORICAL TRADING BREAKS RECOVERY — BATCH 09 POLICY

Contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_POLICY_V1`

Parent progression contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

## Freeze status

**FROZEN — mechanically derived from persisted post-Batch08 `eligible_recovery_queue()[:5]`; adversarial qualification is mandatory before browser observation.**

## Freeze provenance

- pre-freeze checkpoint HEAD: `2e94b8bfa1459d300ee315d0754f84973be2dd1e`
- Batch 08 atomic integration commit: `aa85a2ade1fe9d9b1ade78f77b9b56c5310a6e74`
- Batch 08 persisted-HEAD re-break trigger: `d996d1e3573bfc36437710cc95510ca73b519650`
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- raw unresolved: `38`
- eligible unresolved: `28`
- historical attempts: `40`
- same-capability BLOCKED/ineligible: `10`
- material capability changes: `0`

## Fixed selection rule

`BATCH_SIZE = 5`

`eligible_recovery_queue()[:5]`

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Batch size and membership may not depend on expected outcome, holiday type, source availability, apparent difficulty, convenience, or manual priority.

## Frozen Batch 09 membership

1. `2024-09-02 — LABOR_DAY`
2. `2024-11-28 — THANKSGIVING_DAY`
3. `2024-11-29 — THANKSGIVING_FRIDAY`
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2024-12-25 — CHRISTMAS_OBSERVED`

These identities and this order were emitted by the freeze generator from the governed queue. No member was manually selected.

## Required qualification

The membership contract must reject skip, reorder, later-member substitution, cardinality change, duplication, same-capability BLOCKED reinsertion, already-resolved reinsertion, prior-attempt contamination, and any manual/outcome-based selection surface.

The frozen module must have no browser/probe/network path and no live call to either recovery queue.

No `.bi5`. No real backtest.
