# DUKASCOPY USATECH — 2025 ANNUAL CALENDAR AUDIT

## Audit scope

This audit reviews the completed 2025 annual calendar-qualification batch under:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Qualification report:

`reports/data-qualification/dukascopy_usatech_2025_calendar_qualification.md`

Candidate-freeze commit:

`6571ee8b9458313137a09b1113698ffff2ca978a`

Completed qualification commit:

`39d3a9e5c67a2d1f2294428273a1f5425b08e038`

## 1. Candidate-set completeness

Frozen candidate count: **15**.

Audited dates:

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

Result: **PASS — 15/15 candidates accounted for.**

No candidate was removed after evidence research.

## 2. Verdict cardinality

Final matrix:

- PASS: **1**
- FAIL: **0**
- BLOCKED: **14**

Every frozen candidate has exactly one verdict.

Result: **PASS**.

## 3. Pre-existing Jan-9 PASS preservation

`2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025` existed in executable `SPECIAL_SESSION_EVIDENCE` before the annual batch.

Audit checks:

- it was included in the frozen candidate set;
- it was not silently omitted because already resolved;
- it was not re-qualified merely to reconstruct chronology;
- its Dukascopy exact-date source remains present;
- its CME source URL was directly inspected;
- although the CME filename contains `2024`, the document content explicitly states `JANUARY 9, 2025` and U.S. equity close `08:30 AM CT`;
- no new contradiction or provenance defect was found.

Result: **PASS — locked executable verdict preserved without chronology rewrite.**

## 4. Date independence

Audit confirms:

- Jul-4 broker notice was not reused to prove Jul-3 broker treatment;
- Thanksgiving event context was not allowed to collapse Thursday and Friday into one verdict;
- Christmas/New-Year period context was not allowed to collapse Dec-24, Dec-25 and Dec-31 into one verdict;
- other-year Dukascopy schedules were not substituted for 2025 witnesses.

Result: **PASS**.

## 5. Broker-event versus target-instrument proof

Official Dukascopy exact-date/period notices were recovered for many 2025 holidays, but their retrievable text delegates detailed hours to the Trading Breaks Calendar.

The 2025 DST notice explicitly names `USATECH.IDX/USD`, but only for regular/summer schedule context.

Audit confirms that the following prohibited inference was not used:

`generic exact-date holiday CFD notice + separate regular USATECH identity + exchange timing = PASS`

That route remains insufficient under PASS-C because the broker special-session mapping chain is absent.

Result: **PASS — no generic broker context promoted to exact target-instrument holiday timing.**

## 6. Trading Breaks historical-route check

The official Dukascopy Trading Breaks route was followed.

The retrievable page confirms its function as a special holiday-hours calendar in GMT, but does not expose an auditable historical `2025 + USATECH.IDX/USD + target-date exact hours` record through the available route.

Audit confirms this limitation remained classified as **absence of proof**, not evidence of open/closed behavior.

Result: **PASS**.

## 7. Exchange/reference evidence discipline

Strong same-year CME evidence was recovered, including exact materials for:

- Jan-9 National Day of Mourning;
- Good Friday;
- Juneteenth;
- Independence Day;
- Thanksgiving;
- Christmas.

PDF material used in the qualification was visually inspected where applicable.

Audit confirms exchange/reference timing was never promoted directly into Dukascopy broker truth.

For unresolved dates, strongest-favorable treatment of exact exchange timing still leaves PASS-C incomplete because explicit target-instrument broker holiday mapping is absent.

Result: **PASS**.

## 8. False-PASS resistance

The annual batch did **not** use any of the following as PASS-bearing evidence:

- other-year schedules;
- adjacent dates;
- generic holiday names;
- current regular hours;
- missing market data;
- HTTP/archive failure;
- source-count majority;
- exchange-only timing;
- a current Trading Breaks page without historical target-date rows.

The metal-only U.S.-national-holiday footnote rejected during the 2024 batch remains inapplicable to `USATECH.IDX/USD` and was not reused.

Result: **PASS**.

## 9. Executable-state audit

No new 2025 candidate earned PASS.

Therefore:

- the existing Jan-9 record remains unchanged;
- no new `SPECIAL_SESSION_EVIDENCE` record was added;
- `tools/dukascopy_usatech_calendar.py` was not modified;
- test expectations were not modified;
- unchanged tests were not rerun merely for timestamp freshness;
- no `.bi5` acquisition was started;
- no execution window was frozen;
- no real backtest was started.

Result: **PASS**.

## 10. Coverage-status distinction

The following are simultaneously true:

- `2025_ANNUAL_AUDIT = PASS`
- `2025_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

The annual audit PASS certifies completeness and evidence discipline. It does **not** certify complete broker-session coverage.

Result: **PASS**.

## Final audit verdict

**PASS**

Reason:

`ALL_2025_CANDIDATES_ACCOUNTED_FOR_WITH_LOCKED_PASS_PRESERVED_AND_NO_FALSE_PASS_BYPASS`

The 2025 annual batch is process-complete, date-complete and adversarially consistent with the locked evidence threshold.

The unresolved date-level evidence gaps remain visible and continue to block 2025 calendar coverage and global coverage.
