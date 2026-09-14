# DUKASCOPY USATECH — 2026 BOUNDED CALENDAR QUALIFICATION

## Status

Bounded annual batch: **OPEN — CANDIDATE SET FROZEN BEFORE OUTCOME RESEARCH**

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

Starting checkpoint / HEAD verified before batch:

`9586e983c3c0f45db683cb2031b5dd3d16bba076`

Global governed coverage envelope:

- start: `2018-05-01`
- end: `2026-08-14`

This 2026 batch is therefore **not a full calendar year**. It is explicitly bounded to:

`2026-01-01` → `2026-08-14`

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob SHA:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

## Frozen 2026 in-envelope candidate set

The candidate list below is derived from the versioned `candidate_special_dates(start=date(2026,1,1), end=date(2026,8,14))` behavior and is frozen **before any 2026 outcome/evidence research**.

Exactly **8** candidate dates:

1. `2026-01-01 — NEW_YEARS_OBSERVED`
2. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
3. `2026-02-16 — PRESIDENTS_DAY`
4. `2026-04-03 — GOOD_FRIDAY`
5. `2026-05-25 — MEMORIAL_DAY`
6. `2026-06-19 — JUNETEENTH_OBSERVED`
7. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
8. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

### Boundary facts

- `2026-07-04` is Saturday, therefore the observed Independence Day candidate is Friday `2026-07-03`.
- The generator's previous-business-day rule therefore adds Thursday `2026-07-02` as the independent pre-holiday candidate.
- Labor Day, Thanksgiving, Christmas and New Year's Eve 2026 fall **outside the governed coverage end `2026-08-14`** and are intentionally not part of this batch.
- The scope MUST NOT be extended beyond `2026-08-14` without a separately governed coverage-envelope change.

## Pre-existing executable evidence check

Current `SPECIAL_SESSION_EVIDENCE` contains no `date(2026, ...)` entries.

Therefore none of the 8 candidates is inherited as PASS before research.

## Freeze invariant

This candidate set MUST NOT be altered because a date is difficult to prove, appears to have normal hours, lacks broker evidence, or would be inconvenient for a future execution window.

Each candidate must receive exactly one independent verdict:

- `PASS`
- `FAIL`
- `BLOCKED`

No adjacent-date, same-holiday, same-year, other-year, exchange-only, missing-data, HTTP-error, or source-majority inference may substitute for the date-specific broker threshold.

## Next internal batch step

Research all 8 candidates as one bounded 2026 evidence campaign, apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently date by date, and modify executable calendar evidence only for admissible PASS outcomes.

No execution window may be frozen, no global coverage PASS may be declared, no `.bi5` acquisition may begin, and no real backtest is authorized by this batch.
