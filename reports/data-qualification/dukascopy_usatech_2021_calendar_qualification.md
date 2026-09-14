# DUKASCOPY USATECH — 2021 ANNUAL CALENDAR QUALIFICATION

## 1. Final status

Annual qualification verdict:

**BLOCKED — `2021_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

Annual batch accounting:

- candidates: **13**
- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

Starting checkpoint / HEAD verified before batch:

`f4938f2823412aef3df65d6fd30408f2036d2b88`

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob SHA:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

## 2. Candidate-set freeze — performed before outcome research

The 2021 list was derived from the versioned `candidate_special_dates()` implementation and committed before 2021 outcome research.

Freeze commit:

`d8083da25951d1f506179c39bfba1691ef53c60c`

Exactly **13** candidate dates were frozen:

1. `2021-01-01 — NEW_YEARS_OBSERVED`
2. `2021-01-18 — MARTIN_LUTHER_KING_DAY`
3. `2021-02-15 — PRESIDENTS_DAY`
4. `2021-04-02 — GOOD_FRIDAY`
5. `2021-05-31 — MEMORIAL_DAY`
6. `2021-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
7. `2021-07-05 — INDEPENDENCE_DAY_OBSERVED`
8. `2021-09-06 — LABOR_DAY`
9. `2021-11-25 — THANKSGIVING_DAY`
10. `2021-11-26 — THANKSGIVING_FRIDAY`
11. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
12. `2021-12-24 — CHRISTMAS_OBSERVED`
13. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE`

No Juneteenth candidate exists for 2021 under the current generator; the code intentionally starts Juneteenth candidate generation in 2022.

## 3. Existing executable evidence before research

The current `SPECIAL_SESSION_EVIDENCE` contains no 2021 record.

The last pre-2021 record is:

- `2020-02-17 — SPECIAL_PRESIDENTS_DAY_2020`

and the next later record is:

- `2025-01-09 — SPECIAL_US_NATIONAL_DAY_OF_MOURNING_2025`

Therefore no 2021 candidate was pre-qualified or allowed to inherit a prior verdict.

## 4. 2021 annual evidence campaign

The campaign searched exact dates, holiday names, `USATECH` / `USATECH.IDX/USD`, Dukascopy Bank / Dukascopy Europe `about/ournews` routes, multilingual variants and exact-year formulations.

### Exact-date Dukascopy context recovered

The following official Dukascopy material was recovered for the correct 2021 date/period:

#### New Year 2021 context

Dukascopy's 2020 Christmas/New-Year notice covers the period entering 2021 but only states generic CFD holiday closures and delegates exact schedules to the Trading Breaks Calendar:

`https://www.dukascopy.com/swiss/pt/about/ournews/market-closures-on-christmas-and-new-year-2020`

It does not provide a retrievable exact `USATECH.IDX/USD` session witness for `2021-01-01`.

#### Presidents Day — 2021-02-15

Official Dukascopy notice published `2021-02-10`:

`https://www.dukascopy.com/swiss/pt/about/ournews/market-closures-on-president-s-day-in-usa/`

The notice explicitly identifies Monday `15 February 2021` and special CFD/Bullion trading breaks, but the retrievable notice delegates detailed closures through its linked calendar and does not itself name `USATECH.IDX/USD` with exact hours.

#### Good Friday — 2021-04-02

Official Dukascopy notice published `2021-03-31`:

`https://www.dukascopy.com/swiss/english/about/ournews/easter-weekend-market-closures-2021`

It explicitly identifies Friday `2 April 2021` as an Easter closure period and points to detailed trading schedules, but the retrievable notice does not itself provide exact `USATECH.IDX/USD` hours.

#### Memorial Day — 2021-05-31

Official Dukascopy notice published `2021-05-28`:

`https://www.dukascopy.com/swiss/deutsch/about/ournews/market-closures-on-memorial-day-dbl202104`

It explicitly identifies Monday `31 May 2021` and trading breaks for CFDs/Bullion, but the retrievable notice does not itself name `USATECH.IDX/USD` with exact hours.

#### Christmas / New Year period at end of 2021

Official Dukascopy notice published `2021-12-22`:

`https://www.dukascopy.com/swiss/pt/about/ournews/market-closures-on-christmas-and-new-year-2022`

It confirms market closures during the Christmas/New-Year period and again delegates detailed FX/Bullion/CFD schedules to the Trading Breaks Calendar. The retrievable text does not provide exact `USATECH.IDX/USD` hours for `2021-12-23`, `2021-12-24`, or `2021-12-31`.

### Targeted searches that did not recover PASS-bearing broker evidence

No qualifying exact/archived Dukascopy USATECH witness was recovered for:

- `2021-01-18 — MARTIN_LUTHER_KING_DAY`
- `2021-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2021-07-05 — INDEPENDENCE_DAY_OBSERVED`
- `2021-09-06 — LABOR_DAY`
- `2021-11-25 — THANKSGIVING_DAY`
- `2021-11-26 — THANKSGIVING_FRIDAY`

Searches also recovered exact Dukascopy USATECH schedules for other years, but these remain corroborative-only and are inadmissible as substitutes for 2021.

## 5. Exchange/reference side

Exact same-year exchange/reference material exists for multiple 2021 holidays. Examples include:

- CME Good Friday advisory for `2021-04-02`:
  `https://www.cmegroup.com/tools-information/holiday-calendar/files/2021-good-friday-advisory.pdf`
- CME 2021 holiday-processing notice:
  `https://www.cmegroup.com/notices/market-regulation/2021/01/MSN01-14-21.html`
- CME Thanksgiving-related notice for `2021-11-25`:
  `https://www.cmegroup.com/notices/clearing/2021/10/Chadv21-386.html`
- Nasdaq UTP Thanksgiving notice confirming closed Thursday `2021-11-25` and early close Friday `2021-11-26`:
  `https://www.nasdaqtrader.com/TraderNews.aspx?id=UTP2021-15`
- CME Christmas advisory for the `2021-12-24` holiday-processing period:
  `https://www.cmegroup.com/tools-information/holiday-calendar/files/2021-christmas-advisory.pdf`

These sources can corroborate the holiday/reference side. They do not constitute Dukascopy broker truth.

## 6. Gate application

Authoritative gate implementation:

`tools/irreducible_historical_broker_evidence_gap.py`

Blob SHA:

`1b152b9d1d3ac4c3da135db1528cfb1f687d3a05`

Across the 13 candidates, no date satisfies PASS-A or PASS-B:

- exact primary broker witness for target date + `USATECH.IDX/USD` + relevant hours: **not recovered**;
- exact archived broker witness with verified provenance: **not recovered**.

PASS-C also cannot succeed because the research did not recover an explicit Dukascopy special-session mapping contract that would convert external exchange timing into broker timing. Where an exact-date broker notice exists, the retrievable notice still does not provide the complete target-instrument/mapping chain required by PASS-C.

Adversarial strongest-favorable check:

even if `exact_exchange_schedule=True` and `exchange_provenance_verified=True` are granted for a candidate, the missing broker target-instrument/mapping chain still prevents PASS-C.

With retrieval materially exhausted for this annual campaign and no hard contradiction found, the gate outcome for every 2021 candidate is:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

## 7. Final date-level matrix

| Date | Candidate reason | Verdict | Decisive reason |
|---|---|---|---|
| 2021-01-01 | NEW_YEARS_OBSERVED | BLOCKED | No exact Dukascopy USATECH hours recovered |
| 2021-01-18 | MARTIN_LUTHER_KING_DAY | BLOCKED | No exact Dukascopy USATECH 2021 witness recovered |
| 2021-02-15 | PRESIDENTS_DAY | BLOCKED | Exact-date broker notice exists, but no retrievable USATECH exact-hours witness / mapping chain |
| 2021-04-02 | GOOD_FRIDAY | BLOCKED | Exact-date broker notice exists, but no retrievable USATECH exact-hours witness / mapping chain |
| 2021-05-31 | MEMORIAL_DAY | BLOCKED | Exact-date broker notice exists, but no retrievable USATECH exact-hours witness / mapping chain |
| 2021-07-02 | INDEPENDENCE_PRE_HOLIDAY_SESSION | BLOCKED | No exact Dukascopy USATECH 2021 witness recovered |
| 2021-07-05 | INDEPENDENCE_DAY_OBSERVED | BLOCKED | No exact Dukascopy USATECH 2021 witness recovered |
| 2021-09-06 | LABOR_DAY | BLOCKED | No exact Dukascopy USATECH 2021 witness recovered |
| 2021-11-25 | THANKSGIVING_DAY | BLOCKED | No exact Dukascopy USATECH 2021 witness recovered |
| 2021-11-26 | THANKSGIVING_FRIDAY | BLOCKED | No exact Dukascopy USATECH 2021 witness recovered |
| 2021-12-23 | CHRISTMAS_PRE_HOLIDAY_SESSION | BLOCKED | Generic exact-period broker notice does not provide target-instrument exact hours |
| 2021-12-24 | CHRISTMAS_OBSERVED | BLOCKED | Generic exact-period broker notice does not provide target-instrument exact hours |
| 2021-12-31 | NEW_YEARS_EVE_CANDIDATE | BLOCKED | Generic exact-period broker notice does not provide target-instrument exact hours |

Totals:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**

## 8. Executable consequence

No 2021 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` is **not modified**;
- no 2021 `SPECIAL_SESSION_EVIDENCE` record is added;
- no calendar test expectation is changed;
- the calendar test suite is **not rerun merely for timestamp freshness**;
- latest observed executable calendar state remains **34 tests PASS**;
- global calendar state remains **111 candidates / 24 resolved / 87 unresolved / BLOCKED** until executable evidence changes.

## 9. Boundaries preserved

This annual qualification does not authorize:

- global coverage PASS;
- execution-window freeze;
- massive native `.bi5` acquisition;
- real backtest execution.

Every 2019/2020 locked verdict remains unchanged.
