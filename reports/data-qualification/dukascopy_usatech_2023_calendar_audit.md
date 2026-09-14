# DUKASCOPY USATECH — 2023 ANNUAL CALENDAR AUDIT

## Status

Audit verdict: **PASS**

Reason:

`ALL_2023_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

This audit certifies the completeness and evidence discipline of the 2023 annual qualification batch. It does **not** certify complete 2023 broker-session coverage.

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

Starting checkpoint:

`ffc82a429e41f437df6894b3dfc2d8d3bde94175`

Qualification report:

`reports/data-qualification/dukascopy_usatech_2023_calendar_qualification.md`

Candidate freeze commit:

`c37468b58782b789aea289a6f5bd92813e1e7dcd`

Completed qualification commit:

`295c8c2cfbddbd5bb31689e7623bdce4a8ab2aa0`

## 1. Frozen candidate completeness

The 2023 candidate set was frozen before outcome research from the versioned `candidate_special_dates()` implementation.

Exactly **13** candidates:

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

Audit check: **PASS — 13/13 candidates accounted for.**

No candidate was added, removed, renamed or silently omitted after outcome research.

## 2. Exactly one verdict per date

Final 2023 matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**

Every candidate has exactly one explicit verdict.

Audit check: **PASS**.

## 3. Date-level independence

The qualification report does not infer one candidate from another.

Explicitly rejected shortcuts include:

- `2023-07-03` inferred from `2023-07-04`;
- Thanksgiving Friday inferred from Thanksgiving Thursday;
- Christmas pre-holiday inferred from Christmas Day;
- one 2023 holiday inferred from another 2023 holiday;
- any 2023 holiday inferred from an exact schedule in another year.

Audit check: **PASS**.

## 4. Cross-year substitution

Search recovered exact Dukascopy USATECH holiday schedules/notices from other years.

Those were kept corroborative-only and were not promoted into 2023 broker truth.

Audit check: **PASS**.

## 5. Exchange/reference separation

Strong same-year CME evidence exists for several 2023 holiday sessions, including Presidents Day, Memorial Day, Juneteenth, Labor Day, Thanksgiving and Christmas.

That evidence was used only as exchange/reference evidence and as the strongest-favorable input when testing whether PASS-C could be completed.

It was never treated as direct Dukascopy session truth.

Audit check: **PASS**.

## 6. Broker-event overreach check

Official Dukascopy 2023 material recovered includes:

- daylight-saving notice explicitly naming `USATECH.IDX/USD` for regular/summer schedule context;
- Juneteenth exact-date holiday notice;
- Thanksgiving exact-date/period holiday notice;
- Christmas/New-Year exact-period holiday notice.

The holiday notices delegate detailed hours to the Trading Breaks Calendar and do not expose retrievable exact target-instrument holiday hours.

The DST notice is instrument-explicit but is not a holiday special-session witness.

No combination of these materials was promoted into a false exact holiday witness.

Audit check: **PASS**.

## 7. Trading Breaks historical-route check

The official Dukascopy Trading Breaks routes were followed.

The currently retrievable page/widget describes the special-holiday schedule function but does not expose an auditable historical `2023 + USATECH.IDX/USD + exact target-date hours` record.

This limitation was preserved as **absence of proof**.

It was not converted into:

- evidence that the instrument was open;
- evidence that the instrument was closed;
- proof that no historical record ever existed;
- PASS-A or PASS-B.

Audit check: **PASS**.

## 8. PASS-route enforcement

### PASS-A

No candidate has an exact primary broker witness containing target date + `USATECH.IDX/USD` + relevant holiday hours.

### PASS-B

No candidate has an exact archived broker witness with verified provenance containing target date + instrument + relevant holiday hours.

### PASS-C

Some candidates have exact-date/period broker holiday context and strong exchange timing.

But no candidate has the complete required chain:

`exact-date broker event + target instrument explicit + explicit broker special-session mapping contract + exact verified exchange/reference timing`

Therefore no candidate was promoted to PASS.

Audit check: **PASS**.

## 9. FAIL-route check

No hard contradiction, witness identity mismatch, falsified archive provenance or bucket-conversion contradiction was established.

Therefore no date was artificially classified FAIL merely because evidence was unavailable.

Audit check: **PASS**.

## 10. Executable-calendar integrity

No 2023 candidate earned date-level PASS.

Therefore:

- no `SPECIAL_SESSION_EVIDENCE` entry was added for 2023;
- `tools/dukascopy_usatech_calendar.py` was not modified;
- no calendar-test expectation was modified;
- unchanged tests were not rerun merely to manufacture a newer timestamp.

Audit check: **PASS**.

Latest observed executable state remains:

- calendar tests: **34 PASS**;
- global special-session evidence records: **24**;
- global candidate dates: **111**;
- resolved: **24**;
- unresolved: **87**;
- global coverage: **BLOCKED**.

## 11. Coverage / execution / acquisition boundary

Completion of 2023 research does not authorize:

- global calendar coverage PASS;
- execution-window freeze;
- massive `.bi5` acquisition;
- a real backtest;
- selection of a window designed to evade historical gaps.

Audit check: **PASS**.

## 12. Final audit verdict

All adversarial accounting and anti-bypass checks above pass.

**PASS — `ALL_2023_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`**

Critical distinction:

- `2023_ANNUAL_AUDIT = PASS`
- `2023_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

The audit PASS means the annual qualification is complete and disciplined. It does not mean the missing historical broker-session evidence has been recovered.
