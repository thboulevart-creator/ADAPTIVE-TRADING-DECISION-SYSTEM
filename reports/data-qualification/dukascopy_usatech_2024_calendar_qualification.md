# DUKASCOPY USATECH — 2024 ANNUAL CALENDAR QUALIFICATION

## Status

Annual batch: **COMPLETE**

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

Candidate freeze commit:

`811976c584a0626e06d1012e9f90c9f9619c4ca2`

## Frozen 2024 candidate set

The candidate set was frozen before outcome research.

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

Boundary facts:

- `2024-01-01` is Monday and remains directly in-year.
- `2024-06-19` is Wednesday and is the generated Juneteenth candidate.
- `2024-07-04` is Thursday, so pre-holiday candidate is Wednesday `2024-07-03`.
- `2024-12-25` is Wednesday, so Christmas pre-holiday candidate is Tuesday `2024-12-24`.
- `2024-12-31` is Tuesday and remains an in-year New Year's Eve candidate.

## Pre-existing executable evidence check

Current `SPECIAL_SESSION_EVIDENCE` contained no `date(2024, ...)` entry before the annual campaign.

Therefore no 2024 candidate was inherited as PASS.

## Official Dukascopy 2024 evidence recovered

### Instrument-explicit regular schedule context

Official 2024 U.S. daylight-saving notice:

`https://www.dukascopy.com/europe/english/about/ournews/daylight-saving-time-2024-in-the-us`

The notice explicitly names `USATECH.IDX/USD` among instruments moving to Dukascopy's U.S. summer schedule.

This is valuable instrument-identity and regular-schedule context only. It does **not** identify any 2024 holiday special-session hours.

Current instrument schedule page:

`https://www.dukascopy.com/europe/english/cfd/range-of-markets/`

It confirms the normal `USATECH.IDX/USD` summer/winter trading-hours model, but current regular hours cannot prove historical holiday exceptions.

### New Year — `2024-01-01`

Official end-2023 Christmas/New-Year notice:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-christmas-and-new-year-dbl202761`

Exact-period broker context exists, but detailed FX/Bullion/CFD closures are delegated to the Trading Breaks Calendar. No retrievable exact `2024-01-01 + USATECH.IDX/USD + hours` witness was recovered.

### MLK — `2024-01-15`

Official 2024 notice:

`https://www.dukascopy.com/europe/spanish/about/ournews/market-closures-on-martin-luther-king-day-dbl202768`

It explicitly warns of special CFD/Bullion trading breaks on Monday 15 January 2024 and delegates the detailed closures. The retrievable notice does not itself identify `USATECH.IDX/USD` exact hours.

### Presidents Day — `2024-02-19`

Targeted exact-date/title searches across Dukascopy Bank / Dukascopy Europe, multiple languages and publication-date formulations did **not** recover an admissible exact 2024 broker witness.

Exact Dukascopy Presidents-Day material from other years exists, including 2020, 2023, 2025 and 2026, but those records remain corroborative-only and cannot substitute for 2024.

### Good Friday — `2024-03-29`

Official 2024 Easter notice:

`https://www.dukascopy.com/swiss/pt/about/ournews/easter-weekend-market-closures-2024`

It identifies Friday 29 March 2024 as a market-closure date and links to detailed trading schedules. The retrievable notice does not itself publish the target-instrument exact hours.

### Memorial Day — `2024-05-27`

Official 2024 notice:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-monday-27-may`

It warns of CFD/Bullion trading breaks on Monday 27 May and links to detailed market closures. No exact `USATECH.IDX/USD` hours are present in retrievable notice text.

### Juneteenth — `2024-06-19`

Official 2024 notice:

`https://www.dukascopy.com/swiss/french/about/ournews/juneteenth-national-independence-day-dbl202861`

It identifies Wednesday 19 June 2024 and directs users to the Trading Breaks Calendar for special market closures. No target-instrument exact hours are present in the retrievable notice.

### Independence pre-holiday / Independence Day — `2024-07-03` / `2024-07-04`

Targeted exact-year/date searches did **not** recover an admissible exact 2024 Dukascopy holiday witness for either July 3 or July 4.

Exact Dukascopy Independence schedules from other years exist, including older instrument-explicit schedules and later 2025/2026 notices. They remain cross-year corroboration only.

### Labor Day — `2024-09-02`

Official 2024 notice:

`https://www.dukascopy.com/europe/cz/about/ournews/market-closures-on-labor-day-in-the-united-states-dbl202910`

It identifies special CFD/Bullion breaks on Monday 2 September 2024 and delegates detailed closures. No exact `USATECH.IDX/USD` holiday hours are present in retrievable text.

### Thanksgiving — `2024-11-28` / `2024-11-29`

Official 2024 notice:

`https://www.dukascopy.com/swiss/english/about/ournews/thanksgiving-day-in-the-us-dbl202994`

It explicitly identifies Thanksgiving Thursday 28 November and special closures on both Thursday and Friday, but directs users to the Trading Breaks Calendar. No retrievable target-instrument exact-hours witness was recovered.

### Christmas / New Year — `2024-12-24`, `2024-12-25`, `2024-12-31`

Official 2024 notice:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-during-x-mas-and-new-year-dbl203022`

It warns of market closures throughout the Christmas/New-Year period, especially 25 December, and delegates exact FX/Bullion/CFD schedules. It does not publish retrievable exact `USATECH.IDX/USD` hours for Dec 24, Dec 25 or Dec 31.

## Trading Breaks Calendar adversarial check

Official routes:

- `https://www.dukascopy.com/swiss/english/marketwatch/trading-breaks-calendar/`
- `https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks`

The current pages identify the Trading Breaks Calendar as Dukascopy's holiday-special-hours schedule in GMT.

However, the retrievable current route exposes no auditable historical `2024 + USATECH.IDX/USD + exact target-date hours` record.

This is preserved strictly as **absence of proof**. It is not evidence that historical sessions were open or closed.

No PASS-A or PASS-B witness is created from an inaccessible/non-retrievable historical widget state.

## Adversarial false-lead check — generic U.S. holiday rule

A Dukascopy Europe `General Features` page was found with the footnote:

`Instrument is not tradable from 17:00 till 21:00 during Summer Time (from 18:00 till 22:00 during Winter Time) on US national holidays`.

Official page:

`https://www.dukascopy.com/europe/english/forex/forex-trading-accounts/link/`

Inspection of the table proves that this footnote applies only to `XAU/USD` and `XAG/USD` entries. `USATECH.IDX/USD` is not present in that table and is not covered by the footnote.

Therefore this material **cannot** serve as a `USATECH` special-session mapping contract and cannot complete PASS-C.

## Exchange/reference side — strongest favorable treatment

Strong exact same-year official CME evidence was recovered for the 2024 U.S. holiday calendar and several target sessions.

Examples:

- 2024 U.S. holiday-processing reference:
  `https://www.cmegroup.com/notices/market-regulation/2023/12/MSN12-04-23.html`
- Labor Day advisory:
  `https://www.cmegroup.com/tools-information/holiday-calendar/files/2024-labor-day-advisory.pdf`
- Independence Day settlement schedule:
  `https://www.cmegroup.com/tools-information/holiday-calendar/files/us-independence-day-settlement-times-2024.pdf`
- Thanksgiving settlement schedule:
  `https://www.cmegroup.com/content/dam/cmegroup/tools-information/holiday-calendar/files/thanksgiving-holiday-settlement-times-2024.pdf`
- Christmas advisory:
  `https://www.cmegroup.com/tools-information/holiday-calendar/files/2024-christmas-advisory.pdf`

The Independence schedule explicitly identifies July 3 Equity Index settlement treatment and July 4 holiday treatment. The Thanksgiving schedule identifies Nov 29 Equity & Crypto settlement treatment and Nov 28 holiday treatment. Christmas material identifies the Dec 25 holiday and related processing.

CME material remains exchange/reference evidence only.

For the strongest-favorable application of `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`, the exchange-side fields may be granted as satisfied where exact official same-date material exists. PASS-C still fails because no explicit Dukascopy `USATECH` holiday witness + broker special-session mapping contract was recovered.

## Date-level evidence matrix

| Date | Candidate | Exact 2024 broker event/context | Exact broker USATECH hours | Explicit broker special-session mapping contract | Strong same-year exchange/reference | Verdict |
|---|---|---:|---:|---:|---:|---|
| 2024-01-01 | NEW_YEARS_OBSERVED | yes, exact period | no | no | favorable/external | BLOCKED |
| 2024-01-15 | MARTIN_LUTHER_KING_DAY | yes | no | no | favorable/external | BLOCKED |
| 2024-02-19 | PRESIDENTS_DAY | no qualifying witness recovered | no | no | favorable/external | BLOCKED |
| 2024-03-29 | GOOD_FRIDAY | yes | no | no | favorable/external | BLOCKED |
| 2024-05-27 | MEMORIAL_DAY | yes | no | no | favorable/external | BLOCKED |
| 2024-06-19 | JUNETEENTH_OBSERVED | yes | no | no | favorable/external | BLOCKED |
| 2024-07-03 | INDEPENDENCE_PRE_HOLIDAY_SESSION | no qualifying witness recovered | no | no | yes | BLOCKED |
| 2024-07-04 | INDEPENDENCE_DAY_OBSERVED | no qualifying witness recovered | no | no | yes | BLOCKED |
| 2024-09-02 | LABOR_DAY | yes | no | no | yes | BLOCKED |
| 2024-11-28 | THANKSGIVING_DAY | yes | no | no | yes | BLOCKED |
| 2024-11-29 | THANKSGIVING_FRIDAY | yes | no | no | yes | BLOCKED |
| 2024-12-24 | CHRISTMAS_PRE_HOLIDAY_SESSION | yes, exact period | no | no | yes | BLOCKED |
| 2024-12-25 | CHRISTMAS_OBSERVED | yes, exact period | no | no | yes | BLOCKED |
| 2024-12-31 | NEW_YEARS_EVE_CANDIDATE | yes, exact period | no | no | favorable/external | BLOCKED |

## Gate application

For every 2024 candidate:

- no `strong_broker_contradiction` was found;
- no witness-identity/provenance falsification requiring FAIL was found;
- PASS-A is absent because no exact primary `date + USATECH + relevant hours` witness was recovered;
- PASS-B is absent because no exact archived `date + USATECH + relevant hours` broker witness with verified provenance was recovered;
- PASS-C is absent because the broker side never supplies the complete `target instrument explicit + explicit broker special-session mapping contract` chain, even when exchange-side evidence is treated maximally favorably;
- targeted normal, multilingual, exact-date and linked Trading-Breaks retrieval routes were materially exhausted for this batch.

Therefore the gate outcome for each date is:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

## Final 2024 qualification result

- candidates: **14**
- PASS: **0**
- FAIL: **0**
- BLOCKED: **14**

Every 2024 candidate remains:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2024 annual calendar coverage:

**BLOCKED — `2024_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

This is absence-of-proof governance, not a claim that Dukascopy was historically open or closed at any unproven hour.

## Executable-calendar consequence

No 2024 candidate earned an admissible PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- no `2024` `SPECIAL_SESSION_EVIDENCE` record is added;
- no calendar test expectation is changed;
- no calendar/coverage suite rerun is required merely to manufacture a fresh timestamp;
- latest observed executable state remains `34 calendar tests PASS`;
- latest observed global state remains `111 candidates / 24 resolved / 87 unresolved / BLOCKED` until executable evidence actually changes.

No `.bi5` acquisition, execution-window freeze or real backtest is authorized by this qualification.
