# ANNUAL CALENDAR QUALIFICATION PROTOCOL

## Status

Contract: `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

This protocol changes the operating unit of calendar research from one-date-at-a-time sessions to annual research batches while preserving date-level evidence verdicts.

## Core rule

**Research batch = one calendar year.**

**Evidence verdict = one candidate date.**

**Audit = one calendar year.**

Annual batching is an efficiency mechanism only. It MUST NOT weaken the evidence threshold, merge distinct dates, infer one holiday session from another, or promote exchange/reference evidence into broker truth.

## Annual workflow

For each year in chronological order:

1. Enumerate the complete candidate set from `candidate_special_dates()` for that year.
2. Freeze that candidate list for the annual research batch.
3. Preserve already-qualified and already-BLOCKED dates without reopening them unless materially new evidence appears.
4. Research all remaining candidate dates in a single annual evidence campaign.
5. Apply the existing governing evidence rule independently to every date.
6. Record each date as exactly one of:
   - `PASS` — date resolved by admissible broker evidence;
   - `FAIL` — contradiction, invalid witness identity, falsified provenance, or other hard invalidation;
   - `BLOCKED` — required proof remains unavailable.
7. Update executable calendar evidence only for dates that actually earn PASS.
8. After all annual candidates have an explicit verdict, run an annual audit.
9. Only after the annual audit is complete move to the next year.

## Date-level evidence threshold

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` remains authoritative.

PASS requires one of:

- PASS-A: exact primary broker witness for target date + target instrument + relevant hours;
- PASS-B: exact archived broker witness with verified provenance;
- PASS-C: exact-date broker event explicitly covering target instrument + explicit broker special-session mapping contract + exact same-date verified exchange/reference timing.

Corroborative-only evidence remains non-PASS-bearing, including:

- another year with the same holiday;
- another date in the same holiday period;
- exchange-only timing;
- generic broker holiday notices that do not identify the target instrument;
- current regular hours;
- missing `.bi5` / missing ticks;
- HTTP errors or unavailable pages;
- majority-of-sources reasoning.

## Independence invariant

Every candidate date is independent for verdict purposes.

Examples:

- `2020-07-02` MUST NOT be inferred from `2020-07-03`.
- Thanksgiving Thursday MUST NOT automatically validate Thanksgiving Friday.
- Christmas Eve MUST NOT automatically validate Christmas Day or New Year's Eve.
- A PASS for one date does not change any other candidate's verdict.

## Annual audit

The annual audit answers a different question from calendar coverage.

### Annual audit may PASS when

- the complete candidate set for the year is enumerated;
- every candidate has an explicit PASS / FAIL / BLOCKED verdict;
- no candidate was silently omitted;
- prior locked verdicts were preserved unless materially new evidence justified reopening;
- no cross-date or cross-year inference was used as PASS evidence;
- no exchange-only evidence was promoted to broker truth;
- every executable calendar change corresponds to a date-level PASS;
- unresolved/FAIL dates remain visible;
- contradictions and provenance issues are surfaced explicitly.

### Important separation

`ANNUAL_AUDIT = PASS` means the year's qualification accounting and evidence discipline are complete.

It does **not** mean `ANNUAL_CALENDAR_COVERAGE = PASS`.

If one or more dates remain BLOCKED, the annual calendar coverage remains BLOCKED even when the annual audit itself passes.

If any date is FAIL, annual calendar coverage is FAIL until that contradiction is governed.

## Artifact strategy

Prefer one living annual qualification report per year:

`reports/data-qualification/dukascopy_usatech_<YEAR>_calendar_qualification.md`

and one annual audit report:

`reports/data-qualification/dukascopy_usatech_<YEAR>_calendar_audit.md`

Previously created date-specific reports remain authoritative historical evidence and should be referenced rather than rewritten.

## Execution discipline

- Do not rerun unchanged test suites merely to create a newer timestamp.
- If executable calendar data changes, rerun the relevant calendar tests and coverage checks before the annual audit verdict.
- If no executable calendar data changes, preserve the latest observed executable test state and state explicitly that no rerun was necessary.

## Acquisition and execution-window boundary

This protocol changes only research batching.

It does not authorize:

- freezing an execution/backtest window;
- declaring global 2018–2026 coverage PASS;
- downloading massive native `.bi5` data;
- beginning a real backtest.

Those actions remain governed by `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1` and their separate gates.

## Anti-bypass rules

Forbidden:

- declaring an annual PASS because most dates passed;
- hiding BLOCKED dates from the annual report;
- treating an annual audit PASS as calendar coverage PASS;
- using a known holiday pattern from another year as broker evidence;
- merging adjacent holiday dates into one broker verdict;
- changing the execution window to avoid annual gaps;
- starting `.bi5` acquisition because an annual research batch is complete.
