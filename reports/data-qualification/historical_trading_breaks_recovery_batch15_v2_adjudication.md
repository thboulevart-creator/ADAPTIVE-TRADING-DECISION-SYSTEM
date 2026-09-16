# Historical Trading Breaks Recovery — Batch 15 V2 independent adjudication

## Verdict

`PASS — BATCH15_V2_EVIDENCE_INDEPENDENTLY_ADJUDICATED_OFFLINE`

## Authoritative chain

- frozen membership baseline: `d6622e8da58e2d4218947ff3f2953fe8e19a2c96`
- freeze qualification HEAD: `8066e82607db1f8de0b406ec36684a6856e0646d`
- persisted-membership re-break run/job: `35067904056 / 104702309977`
- execution selector HEAD: `f73d31e645bdc1ad4081a7cf3c104e3f3bd4848b`
- execution run/job: `35068035246 / 104702726720`
- adjudication trigger HEAD: `6dc134aa53a0904cda6c08108377dd8be8dd718c`
- adjudication run/job: `35068120024 / 104702999768`
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- capability fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`

## Frozen results

1. `2021-12-24 — CHRISTMAS_OBSERVED` → PASS — source attempt `batch02:2021-12-24` — record `31532`
2. `2022-04-15 — GOOD_FRIDAY` → PASS — source attempt `batch02:2022-04-15` — record `34894`
3. `2022-12-26 — CHRISTMAS_OBSERVED` → PASS — source attempt `batch04:2022-12-26` — record `46756`
4. `2023-01-02 — NEW_YEARS_OBSERVED` → PASS — source attempt `batch04:2023-01-02` — record `48045`
5. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED` → PASS — source attempt `batch06:2023-07-04` — record `56233`

Accounting: `5 PASS / 0 BLOCKED / 0 FAIL`.

The adjudicator recalculated target-day overlap attribution from persisted historical Class-A evidence and compared the fresh result against the selected persisted execution evidence field-by-field. It did not use a browser, probe, network request, or new capture.

## Integration consequence

Atomic integration is now admissible for these five dates only. It must append retry attempts `69..73`, preserve all historical attempts `1..68`, add exactly the five PASS dates to executable calendar resolution, regenerate deterministic progression, and commit the state mutation only after post-mutation regression is PASS.

Batch 16 must not be frozen before the Batch 15 persisted-HEAD re-break passes.
