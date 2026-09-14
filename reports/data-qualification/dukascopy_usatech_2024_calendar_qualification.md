# DUKASCOPY USATECH — 2024 ANNUAL CALENDAR QUALIFICATION

## Status

Annual batch: **OPEN — CANDIDATE SET FROZEN BEFORE OUTCOME RESEARCH**

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

Starting checkpoint / HEAD verified before batch:

`b8e86286fd4057a9a1445d1943732d81ba4a2f63`

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob SHA:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

## Frozen 2024 candidate set

The candidate list below is derived from the versioned `candidate_special_dates(start=date(2024,1,1), end=date(2024,12,31))` behavior and is frozen **before any 2024 outcome/evidence research**.

Exactly **14** candidate dates:

1. `2024-01-01 — NEW_YEARS_OBSERVED`
2. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
3. `2024-02-19 — PRESIDENTS_DAY`
4. `2024-03-29 — GOOD_FRIDAY`
5. `2024-05-27 — MEMORIAL_DAY`
6. `2024-06-19 — JUNETEENTH_OBSERVED`
7. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
8. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`
9. `2024-09-02 — LABOR_DAY`
10. `2024-11-28 — THANKSGIVING_DAY`
11. `2024-11-29 — THANKSGIVING_FRIDAY`
12. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
13. `2024-12-25 — CHRISTMAS_OBSERVED`
14. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`

### Boundary facts

- `2024-01-01` is Monday and remains directly in-year.
- `2024-06-19` is Wednesday and is the generated Juneteenth candidate.
- `2024-07-04` is Thursday, so the previous business-day candidate is Wednesday `2024-07-03`.
- `2024-12-25` is Wednesday, so Christmas pre-holiday candidate is Tuesday `2024-12-24`.
- `2024-12-31` is Tuesday and therefore survives the weekday guard as a New Year's Eve candidate.

## Pre-existing executable evidence check

Current `SPECIAL_SESSION_EVIDENCE` contains no `date(2024, ...)` entries. Therefore none of the 14 candidates is inherited as PASS before research.

## Freeze invariant

This candidate set MUST NOT be altered because a date is difficult to prove, appears to have normal hours, lacks broker evidence, or would be inconvenient for a future execution window.

Each candidate must receive exactly one independent verdict:

- `PASS`
- `FAIL`
- `BLOCKED`

No adjacent-date, same-holiday, same-year, other-year, exchange-only, missing-data, HTTP-error, or source-majority inference may substitute for the date-specific broker threshold.

## Next internal batch step

Research all 14 candidates as one 2024 evidence campaign, apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently date by date, and modify executable calendar evidence only for admissible PASS outcomes.

No execution window may be frozen and no `.bi5` acquisition or real backtest is authorized by this batch.
