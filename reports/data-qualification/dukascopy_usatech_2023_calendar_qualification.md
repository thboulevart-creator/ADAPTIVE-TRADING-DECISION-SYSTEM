# DUKASCOPY USATECH — 2023 ANNUAL CALENDAR QUALIFICATION

## Status

Annual batch: **OPEN — CANDIDATE SET FROZEN BEFORE OUTCOME RESEARCH**

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

Starting checkpoint / HEAD verified before batch:

`ffc82a429e41f437df6894b3dfc2d8d3bde94175`

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob SHA:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

## Frozen 2023 candidate set

The candidate list below is derived from the versioned `candidate_special_dates(start=date(2023,1,1), end=date(2023,12,31))` behavior and is frozen **before any 2023 outcome/evidence research**.

Exactly **13** candidate dates:

1. `2023-01-02 — NEW_YEARS_OBSERVED`
2. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
3. `2023-02-20 — PRESIDENTS_DAY`
4. `2023-04-07 — GOOD_FRIDAY`
5. `2023-05-29 — MEMORIAL_DAY`
6. `2023-06-19 — JUNETEENTH_OBSERVED`
7. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
8. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
9. `2023-09-04 — LABOR_DAY`
10. `2023-11-23 — THANKSGIVING_DAY`
11. `2023-11-24 — THANKSGIVING_FRIDAY`
12. `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`
13. `2023-12-25 — CHRISTMAS_OBSERVED`

### Boundary note

- `2023-01-01` is Sunday, so `NEW_YEARS_OBSERVED` is Monday `2023-01-02`.
- `2023-12-31` is Sunday, so the generator's weekday guard excludes the `NEW_YEARS_EVE_CANDIDATE` from the bounded 2023 annual batch.
- Juneteenth is generated because the current implementation includes it for `year >= 2022`; in 2023 it falls directly on Monday `2023-06-19`.

## Pre-existing executable evidence check

Current `SPECIAL_SESSION_EVIDENCE` contains no `date(2023, ...)` entries. Therefore none of the 13 candidates is inherited as PASS before research.

## Freeze invariant

This candidate set MUST NOT be altered merely because a date is difficult to prove, lacks broker evidence, appears to have normal hours, or would be inconvenient for a future execution window.

Each candidate must receive exactly one independent verdict:

- `PASS`
- `FAIL`
- `BLOCKED`

No adjacent-date, same-holiday, same-year, other-year, exchange-only, missing-data, or source-majority inference may substitute for the date-specific broker threshold.

## Next internal batch step

Research all 13 candidates as one 2023 evidence campaign, apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently date by date, and modify executable calendar evidence only for admissible PASS outcomes.

No execution window may be frozen and no `.bi5` acquisition or real backtest is authorized by this batch.
