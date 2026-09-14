# SESSION BACKUP — 14 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY BATCH 03 PASS

## Final verdict

**PASS — `BATCH03_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

## Frozen membership executed

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

## Authoritative runtime

- run `34892253133`
- job `104137558818`
- probe commit `9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4`
- artifact `10367930592`
- SHA-256 `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`

## Independent adjudication

- 2022-05-30 PASS — record 37019
- 2022-06-20 PASS — record 38945
- 2022-07-01 BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`
- 2022-07-04 PASS — record 41225
- 2022-09-05 PASS — record 42569

Batch total: `4 PASS / 1 BLOCKED / 0 FAIL`.

Only PASS dates were integrated. BLOCKED remains unresolved and was not promoted to negative evidence.

## Integrated state

Persisted integration commit:

`d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Independent persisted-HEAD regression:

- run `34893976903`
- job `104143235284`
- tested HEAD `30f6d11bb51473211b9576bde92e85b405ed5606`
- `104 passed in 0.60s`

Exact state:

- global `111 / 34 / 77`
- execution window `68 / 11 / 57`
- attempts `15`
- BLOCKED ineligible `4`
- eligible unresolved `53`
- evidence-shape errors `0`
- orphan evidence `0`
- contradictory dates `0`

## Current next governed action

Freeze and version Batch 04 with `BATCH_SIZE = 5` from the first five entries of current governed `eligible_recovery_queue()` before any Batch 04 observation.

Projected first five:

1. 2022-11-24 THANKSGIVING_DAY
2. 2022-11-25 THANKSGIVING_FRIDAY
3. 2022-12-23 CHRISTMAS_PRE_HOLIDAY_SESSION
4. 2022-12-26 CHRISTMAS_OBSERVED
5. 2023-01-02 NEW_YEARS_OBSERVED

Do not use this projection as a substitute for the mechanical versioned freeze.

No `.bi5`. No real backtest.
