# DUKASCOPY USATECH — 2025 ANNUAL CALENDAR QUALIFICATION

## Status

Annual batch: **COMPLETE**

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

Candidate-freeze commit:

`6571ee8b9458313137a09b1113698ffff2ca978a`

## 1. Frozen 2025 candidate set

The candidate set was frozen before outcome research.

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

The set was not altered after evidence retrieval.

## 2. Pre-existing executable PASS preserved

Current `SPECIAL_SESSION_EVIDENCE` already contains:

`2025-01-09 — SPECIAL_US_NATIONAL_DAY_OF_MOURNING_2025`

with:

- `fully_closed_hours_utc = frozenset(range(15, 23))`;
- Dukascopy exact-date context:
  `https://www.dukascopy.com/europe/english/about/ournews/us-market-closure-on-9th-of-january-2025`;
- CME exact schedule source:
  `https://www.cmegroup.com/trading-hours/files/day-of-mourning-january-9-2024.pdf`.

The CME filename contains `2024`, but direct inspection of the document confirms the schedule itself is explicitly for **January 9, 2025** and states that CME Group U.S. equities close at `08:30 CT`, with Globex reopening at the regularly scheduled time for the next trade date.

Therefore no new provenance defect or contradiction was found. The pre-existing Jan-9 verdict remains:

**PASS — LOCKED PRE-EXISTING EXECUTABLE EVIDENCE**

It was not re-qualified from scratch merely to reconstruct chronology.

## 3. 2025 broker-side research campaign

The annual campaign searched exact dates, holiday names, `USATECH` / `USATECH.IDX/USD`, Dukascopy Bank and Dukascopy Europe company-news routes, multilingual variants, exact-year formulations, and the linked Trading Breaks route.

### Instrument-explicit regular-schedule context

Official Dukascopy 2025 daylight-saving notice:

`https://www.dukascopy.com/swiss/english/about/ournews/daylight-saving-time-2025-in-the-us`

This explicitly names `USATECH.IDX/USD` among the CFDs to which U.S. summer trading time applies.

This proves instrument identity and regular/summer schedule context only. It is **not** a holiday special-session witness and cannot be combined silently with generic holiday notices to manufacture PASS-C.

### New Year — 2025-01-01

Official exact-period broker notice, published 2024-12-20:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-during-x-mas-and-new-year-dbl203022`

It warns of Christmas/New-Year closures and points to detailed FX/Bullion/CFD closures, but the retrievable text does not provide exact `USATECH.IDX/USD` hours for Jan 1.

### MLK — 2025-01-20

Official exact-date broker notice:

`https://www.dukascopy.com/europe/english/about/ournews/market-closures-on-martin-luther-king-day-dbl203039`

It states special trading breaks for CFDs and Bullion on Jan 20 and delegates details to the Trading Breaks Calendar. No exact target-instrument hours are exposed in retrievable text.

### Presidents Day — 2025-02-17

Official exact-date broker notice:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-president-s-day-in-the-usa-dbl203069`

It states reduced liquidity and special CFD/Bullion breaks on Feb 17, but delegates detailed hours and does not expose exact `USATECH.IDX/USD` hours.

### Good Friday — 2025-04-18

Official exact-date/period broker notice:

`https://www.dukascopy.com/swiss/english/about/ournews/easter-weekend-market-closures-2025`

It explicitly identifies Friday Apr 18 as an Easter closure period and delegates trading schedules. No exact USATECH-hour witness is present in retrievable text.

### Memorial Day — 2025-05-26

Official exact-date broker notice:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-monday-26-may`

It states trading breaks for CFDs and Bullion and U.S. market closure for Memorial Day. Detailed schedules are delegated; no exact target-instrument hours are exposed.

### Juneteenth — 2025-06-19

Official exact-date broker notice:

`https://www.dukascopy.com/swiss/english/about/ournews/juneteenth-national-independence-day-dbl203146`

It identifies Juneteenth on Jun 19 and explicitly sends clients to the Trading Breaks Calendar for special closures. No exact USATECH-hour witness is present in the article text.

### Independence pre-holiday — 2025-07-03

No admissible exact broker witness was recovered proving a Jul-3 special `USATECH.IDX/USD` session.

The Jul-4 notice below does not independently prove Jul-3 broker treatment and was not reused across dates.

### Independence Day — 2025-07-04

Official exact-date broker notice:

`https://www.dukascopy.com/europe/french/about/ournews/market-closures-on-independence-day-in-the-us-dbl203154`

It states special CFD and Bullion trading breaks on Jul 4 and delegates detailed closures. No exact `USATECH.IDX/USD` hours are exposed in retrievable text.

### Labor Day — 2025-09-01

Official exact-date broker notice:

`https://www.dukascopy.com/europe/english/about/ournews/market-closures-on-labor-day-in-the-united-states-dbl203195`

It states special CFD/Bullion breaks on Sep 1 and delegates detailed closures. No exact target-instrument hours are exposed.

### Thanksgiving — 2025-11-27 / 2025-11-28

Official exact-date/period broker notice:

`https://www.dukascopy.com/swiss/english/about/ournews/thanksgiving-day-in-the-us-dbl203236`

It explicitly identifies Thursday Nov 27 and special closures on Thursday **and Friday**, but sends clients to the Trading Breaks Calendar rather than publishing exact `USATECH.IDX/USD` hours.

The two candidate dates remain independent and neither receives a PASS from the generic event notice alone.

### Christmas / year-end — 2025-12-24 / 12-25 / 12-31

Official exact-period broker notice:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-during-x-mas-and-new-year-dbl203256`

It confirms Christmas/New-Year market closures and delegates detailed FX/Bullion/CFD hours. The retrievable text does not expose exact USATECH hours for Dec 24, Dec 25 or Dec 31.

## 4. Trading Breaks Calendar adversarial check

Official route:

`https://www.dukascopy.com/swiss/english/marketwatch/trading-breaks-calendar/`

The currently retrievable page explicitly describes itself as the special holiday-hours schedule in GMT, but it exposes no auditable historical `2025 + USATECH.IDX/USD + exact target-date hours` row through the available route.

This remains **absence of proof**, not evidence that a historical session was open or closed.

No PASS-A or PASS-B witness was created from the route limitation.

## 5. Exchange/reference side

Strong same-year official CME evidence was recovered and visually inspected where PDF evidence was used.

Examples:

### Jan 9 National Day of Mourning

`https://www.cmegroup.com/trading-hours/files/day-of-mourning-january-9-2024.pdf`

Despite the filename, the document explicitly states `JANUARY 9, 2025` and `CME GROUP US EQUITIES CLOSE at 8:30 AM CT`.

### Good Friday

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/2025-good-friday-clearing-advisory.pdf`

Exact Good Friday Apr 18 2025 advisory.

### Juneteenth

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/juneteenth-day-settlement-times-2025.pdf`

Exact Jun 19 2025 holiday material.

### Independence Day

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/2025-4th-of-july-clearing-advisory.pdf`

Exact Jul 4 2025 clearing advisory.

### Thanksgiving

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/thanksgiving-holiday-settlement-times-2025.pdf`

The document records no settlement-price dissemination on Thu Nov 27 and a `12:00 CT` Equity & Crypto settlement on Fri Nov 28.

### Christmas

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/christmas-holiday-settlement-times-2025.pdf`

The document records a `12:00 CT` Equity & Crypto settlement on Dec 24 and no settlement-price dissemination on Dec 25.

Exchange/reference evidence was **never promoted into broker truth**.

Under the strongest-favorable application of the historical-gap gate, even granting exact verified exchange timing cannot complete PASS-C for the unresolved dates because the required explicit Dukascopy target-instrument holiday witness plus broker special-session mapping contract remains absent.

## 6. Date-level gate result

Final matrix:

| Date | Candidate reason | Verdict | Reason |
|---|---|---|---|
| 2025-01-01 | NEW_YEARS_OBSERVED | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-01-09 | NATIONAL_DAY_OF_MOURNING_CARTER_2025 | **PASS** | pre-existing locked executable evidence |
| 2025-01-20 | MARTIN_LUTHER_KING_DAY | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-02-17 | PRESIDENTS_DAY | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-04-18 | GOOD_FRIDAY | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-05-26 | MEMORIAL_DAY | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-06-19 | JUNETEENTH_OBSERVED | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-07-03 | INDEPENDENCE_PRE_HOLIDAY_SESSION | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-07-04 | INDEPENDENCE_DAY_OBSERVED | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-09-01 | LABOR_DAY | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-11-27 | THANKSGIVING_DAY | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-11-28 | THANKSGIVING_FRIDAY | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-12-24 | CHRISTMAS_PRE_HOLIDAY_SESSION | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-12-25 | CHRISTMAS_OBSERVED | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |
| 2025-12-31 | NEW_YEARS_EVE_CANDIDATE | **BLOCKED** | `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` |

Totals:

- PASS: **1**
- FAIL: **0**
- BLOCKED: **14**
- total candidates: **15**

## 7. Annual coverage verdict

**BLOCKED — `2025_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

The existing Jan-9 PASS is preserved, but fourteen date-level broker-session facts remain unresolved under the locked evidence threshold.

## 8. Executable impact

No **new** 2025 candidate earned PASS.

Therefore:

- the existing Jan-9 executable record remains unchanged;
- `tools/dukascopy_usatech_calendar.py` requires no modification;
- no new `SPECIAL_SESSION_EVIDENCE` record is added;
- no test expectation changes;
- calendar tests/coverage must not be rerun merely to manufacture a newer timestamp;
- no `.bi5` acquisition is authorized;
- no execution window is frozen;
- no real backtest is authorized.

The latest observed executable state therefore remains the previously locked state until an executable change justifies a rerun.
