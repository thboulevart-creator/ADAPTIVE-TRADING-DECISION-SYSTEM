# DUKASCOPY USATECH — 2023 ANNUAL CALENDAR QUALIFICATION

## Status

Annual batch: **COMPLETE**

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

Candidate freeze commit:

`c37468b58782b789aea289a6f5bd92813e1e7dcd`

## Frozen 2023 candidate set

The candidate list below was frozen before any 2023 outcome/evidence research.

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

Boundary facts:

- `2023-01-01` is Sunday, therefore `NEW_YEARS_OBSERVED` is Monday `2023-01-02`.
- `2023-12-31` is Sunday, therefore the weekday guard excludes the bounded 2023 `NEW_YEARS_EVE_CANDIDATE`.
- Juneteenth is included because the current generator adds it for `year >= 2022`; in 2023 it falls directly on Monday `2023-06-19`.

## Pre-existing executable evidence

Current `SPECIAL_SESSION_EVIDENCE` contains no `date(2023, ...)` entries.

Therefore no 2023 candidate was inherited as PASS before research.

## Research campaign

The annual campaign searched the complete frozen set using:

- exact target dates and holiday names;
- `USATECH` and `USATECH.IDX/USD`;
- Dukascopy Bank and Dukascopy Europe company-news routes;
- English and multilingual indexed variants;
- exact-year formulations;
- Dukascopy Trading Breaks Calendar routes;
- same-year official CME holiday schedules and settlement/advisory material.

No 2019/2020/2021/2022 verdict was reopened.

## Official Dukascopy 2023 material recovered

### Regular/summer schedule context — instrument explicit

Official Dukascopy 2023 daylight-saving notice:

`https://www.dukascopy.com/europe/english/about/ournews/change-to-daylight-saving-time-2023-in-the-us`

This exact-year notice explicitly names:

`USATECH.IDX/USD`

among the CFDs to which the 2023 U.S. summer trading-time change applies.

This is useful instrument identity and regular/summer-schedule context only. It is **not** a holiday-session witness for any candidate date.

### New Year 2023 period

Official end-2022 notice:

`https://www.dukascopy.com/swiss/arabic/about/ournews/market-closures-during-x-mas-and-new-year`

This establishes generic Christmas/New-Year FX/Bullion/CFD context spanning the transition into 2023, but delegates detailed schedules and does not publish an exact `2023-01-02 + USATECH.IDX/USD + hours` witness.

### Juneteenth — `2023-06-19`

Official Dukascopy Bank notice:

`https://www.dukascopy.com/swiss/pt/about/ournews/juneteenth-national-independence-day-dbl202591/`

The notice explicitly identifies Monday 19 June 2023 as Juneteenth and directs clients to the Trading Breaks Calendar for special market closures.

It does **not** expose in retrievable text an exact `USATECH.IDX/USD` row or exact hours.

### Thanksgiving — `2023-11-23` and `2023-11-24`

Official Dukascopy Bank notice:

`https://www.dukascopy.com/swiss/english/about/ournews/thanksgiving-day-in-the-us-dbl202684`

The notice explicitly identifies Thanksgiving Thursday 23 November 2023 and special closures on Thursday and Friday, but delegates the detailed schedule to the Trading Breaks Calendar.

It does **not** expose in retrievable text an exact `USATECH.IDX/USD` row or exact hours for either date.

### Christmas / New Year period — `2023-12-22` and `2023-12-25`

Official Dukascopy Bank notice:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-christmas-and-new-year-dbl202761`

Published 22 December 2023, it confirms Christmas/New-Year FX/Bullion/CFD closure context and warns specifically about 25 December, but delegates exact details to the Trading Breaks Calendar.

It does **not** publish exact `USATECH.IDX/USD` hours for 22 or 25 December.

## Trading Breaks Calendar adversarial check

Current official routes:

- `https://www.dukascopy.com/swiss/english/marketwatch/trading-breaks-calendar/`
- `https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks`

The page states that the Trading Breaks Calendar shows special holiday trading hours in GMT.

However, the currently retrievable page/widget does not expose an auditable historical 2023 `USATECH.IDX/USD` row with target-date hours.

This access limitation is preserved as **absence of proof**. It is not evidence that Dukascopy was open or closed at any specific hour.

## Targeted broker retrieval with no qualifying witness

Materially targeted searches did not recover an admissible exact/archived `2023 + USATECH.IDX/USD + target holiday hours` witness for:

- `2023-01-16 — MARTIN_LUTHER_KING_DAY`;
- `2023-02-20 — PRESIDENTS_DAY`;
- `2023-04-07 — GOOD_FRIDAY`;
- `2023-05-29 — MEMORIAL_DAY`;
- `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`;
- `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`;
- `2023-09-04 — LABOR_DAY`.

Dukascopy market-news/analysis pages published on some holiday dates were deliberately rejected as session evidence: publication of analysis content does not prove `USATECH.IDX/USD` tradability or exact broker hours.

Other-year instrument-specific Dukascopy holiday schedules were also rejected as corroborative-only.

## Same-year exchange/reference evidence

Strong official same-year exchange/reference material exists and was used only as corroboration / strongest-favorable PASS-C input, never as broker truth.

Examples include:

- CME Presidents' Day settlement material:
  `https://www.cmegroup.com/tools-information/holiday-calendar/files/presidents-day-holiday-settlement-times-2023.pdf`
- CME Memorial Day advisory:
  `https://www.cmegroup.com/tools-information/holiday-calendar/files/2023-memorial-day-advisory.pdf`
- CME Juneteenth Globex schedule:
  `https://www.cmegroup.com/trading-hours/files/juneteenth-2023.pdf`
- CME Labor Day Globex schedule:
  `https://www.cmegroup.com/trading-hours/files/labor-day-2023.pdf`
- CME Thanksgiving advisory and Globex schedule:
  `https://www.cmegroup.com/tools-information/holiday-calendar/files/2023-thanksgiving-advisory.pdf`
  `https://www.cmegroup.com/trading-hours/files/thanksgiving-day-2023.pdf`
- CME Christmas Globex schedule:
  `https://www.cmegroup.com/trading-hours/files/christmas-day-2023.pdf`
- CME 2023 holiday-processing reference:
  `https://www.cmegroup.com/notices/market-regulation/2022/12/MSN12-13-22.html`

The CME schedules confirm real 2023 holiday session modifications for equity products on several target dates. This never substitutes for the broker-side instrument witness.

## Strongest-favorable gate application

For every candidate, the broker-side PASS-bearing routes remain incomplete.

### PASS-A

Exact primary Dukascopy witness for target date + `USATECH.IDX/USD` + relevant hours:

**absent for all 13 candidates**.

### PASS-B

Exact archived Dukascopy witness with verified provenance for target date + instrument + relevant hours:

**absent for all 13 candidates**.

### PASS-C

Some dates have exact-date/period Dukascopy holiday events and strong same-date CME timing.

However PASS-C additionally requires:

- target instrument explicit in the broker holiday event; and
- an explicit broker special-session mapping contract to the exchange/reference schedule.

Those links were not recovered for any 2023 candidate.

Even when exact verified CME timing is granted under the strongest favorable assumption, PASS-C remains false.

No hard contradiction, witness-identity mismatch, falsified archive provenance or bucket-conversion contradiction was established.

Retrieval was materially exhausted for this annual batch under the governed research method.

## Final date-level verdict matrix

| Date | Candidate reason | Broker evidence summary | Verdict |
|---|---|---|---|
| `2023-01-02` | `NEW_YEARS_OBSERVED` | Generic Christmas/New-Year broker context only; no exact USATECH hours | **BLOCKED** |
| `2023-01-16` | `MARTIN_LUTHER_KING_DAY` | No qualifying exact/archived 2023 USATECH holiday witness recovered | **BLOCKED** |
| `2023-02-20` | `PRESIDENTS_DAY` | No qualifying exact/archived 2023 USATECH holiday witness recovered | **BLOCKED** |
| `2023-04-07` | `GOOD_FRIDAY` | No qualifying exact/archived 2023 USATECH holiday witness recovered | **BLOCKED** |
| `2023-05-29` | `MEMORIAL_DAY` | No qualifying exact/archived 2023 USATECH holiday witness recovered | **BLOCKED** |
| `2023-06-19` | `JUNETEENTH_OBSERVED` | Exact-date Dukascopy event, but detailed schedule delegated; no USATECH exact hours | **BLOCKED** |
| `2023-07-03` | `INDEPENDENCE_PRE_HOLIDAY_SESSION` | No qualifying exact broker pre-holiday USATECH witness recovered | **BLOCKED** |
| `2023-07-04` | `INDEPENDENCE_DAY_OBSERVED` | No qualifying exact/archived 2023 USATECH holiday witness recovered | **BLOCKED** |
| `2023-09-04` | `LABOR_DAY` | No qualifying exact/archived 2023 USATECH holiday witness recovered | **BLOCKED** |
| `2023-11-23` | `THANKSGIVING_DAY` | Exact-date Dukascopy event covering Thursday/Friday; no USATECH exact hours | **BLOCKED** |
| `2023-11-24` | `THANKSGIVING_FRIDAY` | Exact-date-period Dukascopy event; no USATECH exact hours | **BLOCKED** |
| `2023-12-22` | `CHRISTMAS_PRE_HOLIDAY_SESSION` | Exact-period Dukascopy notice; no target-instrument exact hours | **BLOCKED** |
| `2023-12-25` | `CHRISTMAS_OBSERVED` | Exact-period Dukascopy notice; no target-instrument exact hours | **BLOCKED** |

Every BLOCKED row is governed by:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

This is an absence-of-proof verdict, not a claim about actual open/closed hours.

## Final 2023 result

- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**
- total: **13**

2023 annual calendar coverage verdict:

**BLOCKED — `2023_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## Executable impact

No 2023 candidate earned an admissible PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- no 2023 `SPECIAL_SESSION_EVIDENCE` record is added;
- no calendar test expectation is changed;
- calendar tests/coverage are not rerun merely for timestamp freshness;
- latest observed executable calendar suite remains `34 PASS`;
- latest observed global coverage remains `111 candidates / 24 resolved / 87 unresolved / BLOCKED`;
- no execution window is frozen;
- no `.bi5` is downloaded;
- no real backtest is started.

## Next step

Perform the separate 2023 annual audit. The audit may PASS if all 13 candidates are accounted for with disciplined date-level verdicts, while 2023 calendar coverage remains BLOCKED.
