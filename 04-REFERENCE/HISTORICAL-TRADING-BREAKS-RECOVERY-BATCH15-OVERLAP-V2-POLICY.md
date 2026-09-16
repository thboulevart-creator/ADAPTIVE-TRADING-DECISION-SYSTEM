# Historical Trading Breaks Recovery — Batch 15 overlap-V2 retry policy

## Purpose

Batch 15 is the first bounded retry batch opened by the qualified material capability change `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`.

It is **not** a browser/probe batch and must not recapture broker evidence. Its admissible evidence is the already persisted Class-A offline readjudication produced under the qualified target-day-overlap attribution contract.

## Immutable selection rule

The membership is exactly:

`eligible_recovery_queue()[:5]`

at freeze baseline HEAD:

`d6622e8da58e2d4218947ff3f2953fe8e19a2c96`

Frozen order:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2022-04-15 — GOOD_FRIDAY`
3. `2022-12-26 — CHRISTMAS_OBSERVED`
4. `2023-01-02 — NEW_YEARS_OBSERVED`
5. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`

No skip, reorder, substitution, shrink, expansion, result-based selection, raw-queue bypass, browser observation, probe, or live recapture is admissible.

## Governing capability

- capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`
- qualification: `TARGET_DAY_OVERLAP_ATTRIBUTION_ADVERSARIALLY_QUALIFIED`
- persisted Class-A readjudication: `14 PASS / 0 BLOCKED / 0 FAIL`

Each frozen row must be a previously BLOCKED V1 attempt with blocker `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`, now eligible only because the persisted material capability change proves the exact missing semantic capability.

## Next gate

Before any integration, the persisted freeze must be adversarially re-broken read-only. Integration may consume only the matching five persisted readjudication PASS rows and must append retry attempts without mutating historical attempts.
