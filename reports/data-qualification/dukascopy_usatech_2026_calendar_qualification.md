# DUKASCOPY USATECH — 2026 BOUNDED CALENDAR QUALIFICATION

## Status

Bounded annual batch: **COMPLETE**

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

Starting checkpoint / HEAD verified before batch:

`9586e983c3c0f45db683cb2031b5dd3d16bba076`

Candidate-freeze commit:

`7c45defc80964123821181be339b8fba0fcbd547`

Global governed coverage envelope:

- start: `2018-05-01`
- end: `2026-08-14`

This 2026 batch is therefore **not a full calendar year**. It is explicitly bounded to:

`2026-01-01` → `2026-08-14`

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob SHA:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

## 1. Frozen 2026 in-envelope candidate set

The candidate list below was derived from the versioned `candidate_special_dates(start=date(2026,1,1), end=date(2026,8,14))` behavior and frozen **before any 2026 outcome/evidence research**.

Exactly **8** candidate dates:

1. `2026-01-01 — NEW_YEARS_OBSERVED`
2. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
3. `2026-02-16 — PRESIDENTS_DAY`
4. `2026-04-03 — GOOD_FRIDAY`
5. `2026-05-25 — MEMORIAL_DAY`
6. `2026-06-19 — JUNETEENTH_OBSERVED`
7. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
8. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

Boundary facts:

- `2026-07-04` is Saturday, therefore the observed Independence Day candidate is Friday `2026-07-03`.
- The generator's previous-business-day rule independently adds Thursday `2026-07-02`.
- Labor Day, Thanksgiving, Christmas and New Year's Eve 2026 are outside the governed coverage end `2026-08-14` and were not researched as part of this batch.
- The scope was not extended beyond `2026-08-14`.

## 2. Pre-existing executable evidence check

Current `tools/dukascopy_usatech_calendar.py` contains no `date(2026, ...)` entry in `SPECIAL_SESSION_EVIDENCE`.

Therefore none of the 8 candidates was inherited as PASS.

## 3. Evidence threshold

Date-level qualification uses `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`.

PASS routes only:

- PASS-A: exact primary broker witness for target date + instrument + relevant hours;
- PASS-B: exact archived broker witness with verified provenance;
- PASS-C: exact-date broker event + explicit target instrument + explicit broker special-session mapping contract + exact verified exchange/reference timing.

The following remain corroborative-only and cannot create PASS:

- regular/current USATECH hours;
- another date or year;
- a generic CFD holiday notice;
- an exchange-only schedule;
- missing ticks/data;
- an inaccessible historical widget;
- source-count majority.

## 4. Official Dukascopy 2026 evidence recovered

### 2026-01-01 — New Year

Official exact-period Dukascopy notice published 2025-12-19:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-during-x-mas-and-new-year-dbl203256`

It warns of Christmas/New-Year market closures and points to detailed FX/Bullion/CFD closures, but the retrievable notice does not provide exact `USATECH.IDX/USD` Jan-1 hours.

### 2026-01-19 — Martin Luther King Day

Official exact-date Dukascopy notice published 2026-01-15:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-martin-luther-king-day-dbl203263`

It explicitly states special trading breaks for CFDs and Bullion on Monday Jan 19 and delegates detailed closures to the Trading Breaks Calendar. The retrievable notice does not name `USATECH.IDX/USD` or exact hours.

Historical search also surfaced an older Dukascopy MLK page that explicitly names `USATECH.IDX/USD`, but its calendar wording refers to a different year/date configuration. It was rejected as cross-year evidence and was not used to qualify 2026.

### 2026-02-16 — Presidents Day

Official exact-date notice published 2026-02-12:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-president-s-day-in-the-usa-dbl203350`

It states reduced liquidity and special trading breaks for CFDs and Bullion on Feb 16 and delegates detailed closures. No exact retrievable USATECH hours are present.

### 2026-04-03 — Good Friday

Official exact-period notice published 2026-04-02:

`https://www.dukascopy.com/swiss/english/full-news/easter-weekend-market-closures-2026/`

It states that multiple markets will be closed Friday Apr 3 and Monday Apr 6 and delegates detailed schedules. It does not expose exact USATECH Apr-3 hours.

### 2026-05-25 — Memorial Day

Official exact-date notice published 2026-05-20:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-monday-25-may`

It warns of trading breaks for CFDs and Bullion on May 25 and says U.S. markets remain closed for Memorial Day. Exact `USATECH.IDX/USD` hours are not present in the retrievable text.

### 2026-06-19 — Juneteenth

Official exact-date notice published 2026-06-15:

`https://www.dukascopy.com/europe/english/about/ournews/juneteenth-national-independence-day-dbl203536`

It directs clients to the Trading Breaks Calendar for special closures.

Adversarial anomaly: the notice text says `Thursday, June 19th 2026`, whereas calendar date `2026-06-19` is Friday. The numeric date and holiday identity still point to the in-scope candidate, but the weekday/date inconsistency makes the notice unsuitable as a precise timing witness. It is recorded as a broker-document inconsistency, **not** promoted to session evidence and **not** treated as a standalone FAIL because it does not establish a contradictory USATECH session schedule.

### 2026-07-02 — Independence pre-holiday candidate

No admissible exact-date Dukascopy event/witness was recovered for Jul 2 independently.

The Jul-3 broker notice was not reused to prove Jul-2 behavior.

### 2026-07-03 — Independence Day observed

Official Dukascopy notice published 2026-07-01:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-independence-day-in-the-us-dbl203546`

It explicitly states reduced liquidity and special trading breaks for CFD and Bullion instruments on Friday Jul 3 2026, ahead of U.S. Independence Day on Saturday Jul 4. It delegates exact closures to the Trading Breaks Calendar and does not expose exact USATECH hours.

## 5. Trading Breaks Calendar adversarial check

The `Detailed market closures` links from 2026 MLK, Presidents Day and Independence notices were followed directly.

They resolve to:

`https://www.dukascopy.com/swiss/english/marketwatch/trading-breaks-calendar/`

The page states that the Trading Breaks Calendar provides special holiday trading hours in GMT.

However, the retrievable page exposes no auditable row satisfying:

`2026 + USATECH.IDX/USD + target date + exact special hours`

Targeted page checks found no retrievable `USATECH` entry and no historical Jul/May row.

This remains an **absence of proof**, not historical open/closed evidence.

No PASS-A or PASS-B witness was invented from the route limitation.

## 6. Regular instrument context

Current official Dukascopy Range of Markets identifies `USATECH.IDX/USD` and its regular summer/winter session:

`https://www.dukascopy.com/swiss/french/cfd/range-of-markets/`

This proves instrument identity and regular schedule context only. It does not establish holiday-special treatment and therefore cannot serve as PASS-A/B/C by itself.

## 7. Same-year official CME/reference evidence

Official CME 2026 Holiday and Trading Hours page:

`https://www.cmegroup.com/trading-hours.html`

It provides 2026 holiday references for the in-scope dates and lists 2026 settlement notices for MLK, Presidents Day, Good Friday, Memorial Day, Juneteenth and Independence Day.

Important boundary evidence on that official page includes Independence Day observed Friday Jul 3 and an early-close reference for Thursday Jul 2, confirming that Jul 2 and Jul 3 merit independent treatment on the exchange side.

Good Friday exact-date CME PDF:

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2026/good-friday-holiday-settlement-times-2026.pdf`

The one-page PDF was opened and visually inspected. It is explicitly titled `Good Friday 4/3/2026 Settlement Times`; it states that most CME/CBT/NYMEX/COMEX settlements are carried from Apr 2 to Apr 3, with specific FX/Crypto/Interest Rate treatment.

Official CME same-year evidence was given the strongest favorable treatment where appropriate. It was never promoted into Dukascopy broker truth.

## 8. Date-level gate matrix

| Date | Candidate | Exact broker event/context | Exact target-instrument holiday hours | Explicit broker special-session mapping | Same-year exchange/reference | Verdict |
|---|---|---:|---:|---:|---:|---|
| 2026-01-01 | NEW_YEARS_OBSERVED | YES, exact period | NO | NO | YES | BLOCKED |
| 2026-01-19 | MARTIN_LUTHER_KING_DAY | YES | NO | NO | YES | BLOCKED |
| 2026-02-16 | PRESIDENTS_DAY | YES | NO | NO | YES | BLOCKED |
| 2026-04-03 | GOOD_FRIDAY | YES | NO | NO | YES | BLOCKED |
| 2026-05-25 | MEMORIAL_DAY | YES | NO | NO | YES | BLOCKED |
| 2026-06-19 | JUNETEENTH_OBSERVED | YES, with weekday/date anomaly | NO | NO | YES | BLOCKED |
| 2026-07-02 | INDEPENDENCE_PRE_HOLIDAY_SESSION | NO | NO | NO | YES | BLOCKED |
| 2026-07-03 | INDEPENDENCE_DAY_OBSERVED | YES | NO | NO | YES | BLOCKED |

Under the strongest-favorable application, even setting exact exchange/reference timing to verified does not complete PASS-C because the broker target-instrument + explicit special-session mapping chain is absent.

No exact primary broker witness or verified archived broker witness was recovered for any of the 8 dates.

Normal and available historical retrieval routes were materially exhausted for this batch.

## 9. Final bounded-2026 qualification result

Final matrix:

- candidate dates: **8**
- PASS: **0**
- FAIL: **0**
- BLOCKED: **8**

Every in-envelope 2026 candidate is:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Bounded 2026 calendar coverage:

**BLOCKED — `2026_IN_ENVELOPE_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

The batch itself is complete; `BLOCKED` describes the unresolved evidence state, not incomplete research execution.

## 10. Executable effect

No 2026 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- no 2026 `SPECIAL_SESSION_EVIDENCE` record is added;
- no calendar test expectation changes;
- unchanged tests are not rerun merely for timestamp freshness;
- no `.bi5` is downloaded;
- no execution window is frozen;
- no real backtest begins;
- the global coverage envelope is not extended beyond `2026-08-14`.

Latest previously observed executable state remains:

- calendar suite: **34 PASS**;
- global `SPECIAL_SESSION_EVIDENCE`: **24 records**;
- global coverage: **111 candidates / 24 resolved / 87 unresolved / BLOCKED**.

## 11. Scope conclusion

The chronological calendar-qualification research campaign has now reached the governed envelope end `2026-08-14`.

This does **not** imply global coverage PASS. The global envelope still contains unresolved candidate dates and remains BLOCKED.

A separate cross-year/global envelope audit is required before any later decision concerning execution-window feasibility or acquisition authorization.
