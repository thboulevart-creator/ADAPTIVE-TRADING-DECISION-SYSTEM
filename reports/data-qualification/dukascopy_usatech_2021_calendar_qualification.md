# DUKASCOPY USATECH — 2021 ANNUAL CALENDAR QUALIFICATION

## Status

Annual batch: **OPEN — CANDIDATE SET FROZEN BEFORE OUTCOME RESEARCH**

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

Starting checkpoint / HEAD verified before batch:

`f4938f2823412aef3df65d6fd30408f2036d2b88`

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob SHA:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

## Frozen 2021 candidate set

The candidate list below is derived from the versioned `candidate_special_dates()` implementation and is frozen **before any 2021 outcome/evidence research**.

Exactly **13** candidate dates:

1. `2021-01-01 — NEW_YEARS_OBSERVED`
2. `2021-01-18 — MARTIN_LUTHER_KING_DAY`
3. `2021-02-15 — PRESIDENTS_DAY`
4. `2021-04-02 — GOOD_FRIDAY`
5. `2021-05-31 — MEMORIAL_DAY`
6. `2021-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
7. `2021-07-05 — INDEPENDENCE_DAY_OBSERVED`
8. `2021-09-06 — LABOR_DAY`
9. `2021-11-25 — THANKSGIVING_DAY`
10. `2021-11-26 — THANKSGIVING_FRIDAY`
11. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
12. `2021-12-24 — CHRISTMAS_OBSERVED`
13. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE`

No Juneteenth candidate exists for 2021 under the current versioned generator; the generator intentionally adds Juneteenth only from 2022 onward.

## Freeze invariant

This candidate set MUST NOT be altered merely because a date is difficult to prove, lacks broker evidence, appears to have normal hours, or would be inconvenient for a future execution window.

Each candidate must receive exactly one independent verdict:

- `PASS`
- `FAIL`
- `BLOCKED`

No adjacent-date, same-holiday, same-year, other-year, exchange-only, missing-data, or source-majority inference may substitute for the date-specific broker threshold.

## Next internal batch step

Identify which of these 13 dates are already represented by admissible current `SPECIAL_SESSION_EVIDENCE`, preserve such locked dates unless materially new contradictory evidence appears, then research the remaining candidates as one 2021 evidence campaign.

No execution window may be frozen and no `.bi5` acquisition or real backtest is authorized by this batch.
