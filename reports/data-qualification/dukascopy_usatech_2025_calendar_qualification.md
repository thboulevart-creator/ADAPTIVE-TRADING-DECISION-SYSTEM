# DUKASCOPY USATECH — 2025 ANNUAL CALENDAR QUALIFICATION

## Status

Annual batch: **OPEN — CANDIDATE SET FROZEN BEFORE OUTCOME RESEARCH**

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

Starting checkpoint / HEAD verified before batch:

`3aee1d451122ad728c623ab9f786dc26262a4df1`

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob SHA:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

## Frozen 2025 candidate set

The candidate list below is derived from the versioned `candidate_special_dates(start=date(2025,1,1), end=date(2025,12,31))` behavior and is frozen **before any 2025 outcome/evidence research**.

Exactly **15** candidate dates:

1. `2025-01-01 — NEW_YEARS_OBSERVED`
2. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`
3. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
4. `2025-02-17 — PRESIDENTS_DAY`
5. `2025-04-18 — GOOD_FRIDAY`
6. `2025-05-26 — MEMORIAL_DAY`
7. `2025-06-19 — JUNETEENTH_OBSERVED`
8. `2025-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
9. `2025-07-04 — INDEPENDENCE_DAY_OBSERVED`
10. `2025-09-01 — LABOR_DAY`
11. `2025-11-27 — THANKSGIVING_DAY`
12. `2025-11-28 — THANKSGIVING_FRIDAY`
13. `2025-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
14. `2025-12-25 — CHRISTMAS_OBSERVED`
15. `2025-12-31 — NEW_YEARS_EVE_CANDIDATE`

## Pre-existing executable evidence check

One 2025 candidate is already represented in the current executable `SPECIAL_SESSION_EVIDENCE` and is preserved as locked historical state:

- `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025` — **PASS (pre-existing / locked)**

This record MUST NOT be reopened merely to rebuild chronology. It may be revisited only if materially new contradictory evidence or a provenance defect appears.

The remaining **14** candidates begin this annual campaign unresolved.

## Freeze invariant

This candidate set MUST NOT be altered because a date is difficult to prove, appears to have normal hours, lacks broker evidence, or would be inconvenient for a future execution window.

Each candidate must end with exactly one independent verdict:

- `PASS`
- `FAIL`
- `BLOCKED`

The pre-existing Jan-9 PASS counts as one date-level verdict and remains part of the annual completeness audit.

No adjacent-date, same-holiday, same-year, other-year, exchange-only, missing-data, HTTP-error, or source-majority inference may substitute for the date-specific broker threshold.

## Next internal batch step

Research the remaining 14 candidates as one 2025 evidence campaign, apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently date by date, preserve the locked Jan-9 PASS, and modify executable calendar evidence only for additional admissible PASS outcomes.

No execution window may be frozen and no `.bi5` acquisition or real backtest is authorized by this batch.
