# DUKASCOPY USATECH — 2022 ANNUAL CALENDAR AUDIT

## Scope

Audit of the completed 2022 annual Dukascopy USATECH calendar-qualification batch.

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Qualification report:

`reports/data-qualification/dukascopy_usatech_2022_calendar_qualification.md`

Candidate-freeze commit:

`81a505df146c3bc09f5b68dec5dbef39e4e5caaf`

Completed qualification commit:

`4e2eeec5b37a679b6f8a9f9e0fa064b038d40e81`

## Audit question

Did the 2022 batch account for the complete frozen candidate set and preserve the date-specific evidence threshold without false-PASS bypasses?

This audit does **not** ask whether 2022 broker-session coverage is complete.

## 1. Candidate-set integrity

Frozen candidate count: **12**.

Audited candidates:

1. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
2. `2022-02-21 — PRESIDENTS_DAY`
3. `2022-04-15 — GOOD_FRIDAY`
4. `2022-05-30 — MEMORIAL_DAY`
5. `2022-06-20 — JUNETEENTH_OBSERVED`
6. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
7. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
8. `2022-09-05 — LABOR_DAY`
9. `2022-11-24 — THANKSGIVING_DAY`
10. `2022-11-25 — THANKSGIVING_FRIDAY`
11. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
12. `2022-12-26 — CHRISTMAS_OBSERVED`

Audit result: **PASS — 12/12 accounted for**.

Boundary behavior was preserved:

- no 2022 New Year's observed candidate because the observed day is `2021-12-31`, outside the bounded annual batch;
- no 2022 New Year's Eve candidate because `2022-12-31` is Saturday and the generator admits weekdays only;
- Juneteenth appears for the first time on `2022-06-20`, exactly as defined by the versioned generator.

## 2. One-verdict-per-date invariant

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **12**

Every frozen candidate has exactly one allowed verdict.

Audit result: **PASS**.

## 3. Evidence-threshold audit

Required PASS routes remained:

- PASS-A exact primary broker witness;
- PASS-B exact archived broker witness with verified provenance;
- PASS-C exact-date broker event + explicit target instrument + broker special-session mapping contract + exact verified exchange/reference timing.

Recovered exact-date/period Dukascopy notices for MLK, Memorial Day, Juneteenth, Independence Day and Christmas/New-Year were not promoted into PASS because retrievable text lacked the required explicit target-instrument exact-hours witness/mapping chain.

Audit result: **PASS — no weakened evidence threshold**.

## 4. Historical Trading Breaks bypass attack

The annual campaign followed the `Detailed market closures` / `Trading Breaks Calendar` links from exact-date 2022 Dukascopy notices.

The currently retrievable Trading Breaks Calendar identifies itself as the place where Dukascopy publishes special holiday trading hours, but no retrievable historical 2022 `USATECH.IDX/USD` row or exact 2022 instrument-hour witness was exposed.

This absence was kept as absence of proof, not converted into broker-session truth.

Audit result: **PASS**.

## 5. Exchange-only bypass audit

Official CME 2022 material provides strong same-year holiday/reference coverage, including:

- annual 2022 holiday windows;
- Juneteenth;
- Independence Day;
- Thanksgiving Thursday/Friday;
- Christmas.

No CME/reference schedule was silently promoted into Dukascopy truth.

The strongest-favorable PASS-C attack still fails when exact exchange timing is granted because the explicit broker target-instrument + mapping chain remains absent.

Audit result: **PASS**.

## 6. Cross-date audit

The batch did not infer:

- `2022-07-01` from `2022-07-04`;
- Thanksgiving Friday from Thanksgiving Thursday;
- Christmas pre-holiday from Christmas observed day;
- any unresolved date from another candidate in the same annual batch.

Audit result: **PASS**.

## 7. Cross-year audit

Older and later Dukascopy holiday schedules were retained only as corroborative context.

No 2018/2019/2020/2021 or 2023+ exact schedule was used to create a 2022 PASS.

Audit result: **PASS**.

## 8. Executable-artifact audit

Because no 2022 date earned PASS:

- no 2022 `SPECIAL_SESSION_EVIDENCE` record was created;
- `tools/dukascopy_usatech_calendar.py` was not modified;
- no calendar test expectation was changed;
- unchanged tests were not rerun solely for timestamp freshness.

Latest observed executable state remains:

- calendar tests: **34 PASS**;
- global special-session evidence records: **24**;
- global candidate count: **111**;
- resolved: **24**;
- unresolved: **87**;
- global coverage: **BLOCKED**.

Audit result: **PASS**.

## 9. Coverage / acquisition boundary audit

The 2022 batch did not:

- declare global coverage PASS;
- freeze an execution/backtest window;
- download massive native `.bi5` data;
- start a real backtest;
- choose a future window to evade known gaps.

Audit result: **PASS**.

## 10. Annual audit verdict

**PASS**

Reason:

`ALL_2022_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

Critical distinction:

- `2022_ANNUAL_AUDIT = PASS`
- `2022_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

The audit certifies process completeness and evidence discipline only. It does not certify complete 2022 broker-session coverage.
