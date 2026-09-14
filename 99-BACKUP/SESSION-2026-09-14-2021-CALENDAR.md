# SESSION BACKUP — 2026-09-14 — 2021 ANNUAL DUKASCOPY CALENDAR QUALIFICATION

## 0. Purpose

Authoritative durable recovery snapshot for completion of the 2021 annual Dukascopy USATECH calendar-qualification batch.

Do not reconstruct this state from conversation history. Recover from this file, the current Recovery Checkpoint, the annual protocol, and the versioned 2021 reports.

## 1. Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting verified checkpoint/HEAD: `f4938f2823412aef3df65d6fd30408f2036d2b88`
- Coverage envelope: `2018-05-01` through `2026-08-14`
- Instrument: Dukascopy `USATECH.IDX/USD` / internal `USATECHIDXUSD`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Real backtest: NOT authorized
- Global calendar coverage: BLOCKED
- Latest observed executable state before/after 2021 batch: `34 calendar tests PASS`
- Latest observed global counts: `111 candidates / 24 resolved / 87 unresolved`

## 2. Mandatory operating method

Calendar qualification follows:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

Permanent rule:

- **research batch = one complete calendar year**;
- **evidence verdict = one candidate date**;
- **audit = one complete calendar year**.

Annual batching is an efficiency mechanism only. It never weakens date-specific evidence.

Project-wide qualification discipline remains:

`formalisation → candidate → adversarial break → correction → re-break → verdict`

Allowed verdicts only:

- PASS
- FAIL
- BLOCKED

Never convert absence of proof into PASS.

## 3. Locked evidence gate

Contract:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Gate implementation:

`tools/irreducible_historical_broker_evidence_gap.py`

Blob:

`1b152b9d1d3ac4c3da135db1528cfb1f687d3a05`

PASS routes only:

- PASS-A exact primary broker witness for target date + instrument + relevant hours;
- PASS-B exact archived broker witness with verified provenance;
- PASS-C exact-date broker event + explicit target instrument + explicit broker special-session mapping contract + exact verified exchange/reference timing.

Corroborative-only material cannot create PASS:

- other-year schedules;
- adjacent holiday dates;
- exchange-only timing;
- generic broker holiday notices;
- missing `.bi5` / ticks;
- HTTP/archive failures;
- regular-session similarity;
- source-count majority.

## 4. Coverage / execution / acquisition boundary

Contract:

`COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Current permission matrix:

- continue annual qualification: PASS
- global coverage PASS: BLOCKED
- execution-window freeze: BLOCKED
- massive `.bi5` acquisition: BLOCKED
- real backtest: BLOCKED

No annual research completion may bypass these boundaries.

## 5. 2021 candidate set freeze

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Candidate set was frozen before 2021 outcome research in:

`reports/data-qualification/dukascopy_usatech_2021_calendar_qualification.md`

Freeze commit:

`d8083da25951d1f506179c39bfba1691ef53c60c`

Exactly 13 candidates:

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

No Juneteenth candidate exists for 2021 under the versioned generator; generation begins in 2022.

## 6. Pre-existing executable 2021 evidence

Current `SPECIAL_SESSION_EVIDENCE` had no 2021 record before research.

The calendar jumped from:

- `2020-02-17 — SPECIAL_PRESIDENTS_DAY_2020`

to:

- `2025-01-09 — SPECIAL_US_NATIONAL_DAY_OF_MOURNING_2025`

Therefore no 2021 date was inherited as PASS.

## 7. 2021 annual research findings

The annual campaign searched exact dates, holiday names, `USATECH` / `USATECH.IDX/USD`, Dukascopy Bank and Dukascopy Europe company-news routes, multilingual variants and exact-year formulations.

Exact-date/period official Dukascopy context recovered included:

### New Year 2021

2020 Christmas/New-Year notice covering the transition into 2021:

`https://www.dukascopy.com/swiss/pt/about/ournews/market-closures-on-christmas-and-new-year-2020`

Generic CFD holiday context only; no retrievable exact USATECH session witness for Jan 1.

### Presidents Day — 2021-02-15

Official notice published 2021-02-10:

`https://www.dukascopy.com/swiss/pt/about/ournews/market-closures-on-president-s-day-in-usa/`

Exact-date broker event exists, but retrievable text delegates detailed closures and does not itself provide `USATECH.IDX/USD` exact hours.

### Good Friday — 2021-04-02

Official notice published 2021-03-31:

`https://www.dukascopy.com/swiss/english/about/ournews/easter-weekend-market-closures-2021`

Exact-date broker event exists, but retrievable text does not provide exact USATECH hours.

### Memorial Day — 2021-05-31

Official notice published 2021-05-28:

`https://www.dukascopy.com/swiss/deutsch/about/ournews/market-closures-on-memorial-day-dbl202104`

Exact-date broker event exists, but retrievable text does not provide exact USATECH hours.

### Christmas/New-Year end-2021 period

Official notice published 2021-12-22:

`https://www.dukascopy.com/swiss/pt/about/ournews/market-closures-on-christmas-and-new-year-2022`

Exact period context exists, but detailed FX/Bullion/CFD schedules are delegated to the Trading Breaks Calendar and no exact USATECH hours are present in the retrievable text for Dec 23, Dec 24 or Dec 31.

No qualifying exact/archived Dukascopy USATECH witness was recovered for MLK, Independence pre-holiday/observed, Labor Day or Thanksgiving Thursday/Friday 2021.

Other-year exact Dukascopy USATECH schedules were recovered during search but were kept strictly corroborative-only.

## 8. Exchange/reference side

Exact same-year external holiday/reference material exists for several 2021 candidates, including CME Good Friday, Thanksgiving-related, Christmas and annual holiday-processing material, plus Nasdaq Thanksgiving closure/early-close material.

This external evidence was not promoted into broker truth.

Strongest-favorable adversarial check:

even granting exact/verified exchange timing cannot create PASS-C without the required Dukascopy target-instrument + explicit broker special-session mapping chain.

## 9. Final 2021 qualification result

Completed annual qualification report:

`reports/data-qualification/dukascopy_usatech_2021_calendar_qualification.md`

Completion commit:

`2f6531a72e85a91382564305193d67985fe544ac`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**

Every candidate returned the governed outcome:

`BLOCKED — IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

Annual coverage verdict:

**BLOCKED — `2021_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 10. 2021 annual audit

Audit report:

`reports/data-qualification/dukascopy_usatech_2021_calendar_audit.md`

Audit commit:

`43a080f7456c9a557527e1f9b8cff9eec27bff74`

Audit verdict:

**PASS**

Reason:

`ALL_2021_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

Audit verified:

- 13/13 candidate completeness;
- exact frozen candidate set preserved;
- one verdict per candidate;
- no cross-year substitution;
- no adjacent-date substitution;
- no exchange-only promotion;
- no generic broker notice promoted to exact USATECH timing;
- no hidden gaps;
- no executable record without date-level PASS;
- no annual-audit PASS confused with calendar-coverage PASS;
- no execution-window or acquisition bypass.

Critical distinction:

- `2021_ANNUAL_AUDIT = PASS`
- `2021_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

## 11. Executable state

No 2021 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` was not modified;
- no 2021 `SPECIAL_SESSION_EVIDENCE` record was added;
- no test expectation changed;
- tests were intentionally not rerun merely for timestamp freshness;
- latest observed calendar suite remains `34 PASS`;
- latest observed global state remains `111 candidates / 24 resolved / 87 unresolved / BLOCKED`.

## 12. Historical state preserved

Do not reopen without materially new evidence:

- `2019-07-03` remains BLOCKED;
- all 12 BLOCKED 2020 candidates remain BLOCKED;
- `2020-02-17 — PRESIDENTS_DAY` remains the sole locked 2020 PASS;
- 2020 annual audit remains PASS;
- 2020 annual coverage remains BLOCKED;
- all 13 2021 candidates remain BLOCKED;
- 2021 annual audit remains PASS;
- 2021 annual coverage remains BLOCKED.

## 13. Known cleanup debt / prohibited mistakes

- accidental branch `__noop_should_not_exist__` MUST NOT be used;
- never resurrect the rejected 2020-01-01 false-PASS logic;
- unavailable archives / HTTP failures are not evidence of session behavior;
- do not rerun unchanged annual audits/tests just for freshness;
- do not select an execution window to evade known gaps.

## 14. Exactly one next governed action

**Begin and complete the 2022 annual calendar qualification batch.**

Required sequence:

1. verify active branch against current Recovery Checkpoint HEAD;
2. enumerate and freeze the complete 2022 candidate set from `candidate_special_dates()` before outcome research;
3. note that 2022 is the first year in the generator where `JUNETEENTH_OBSERVED` is included;
4. identify any already-qualified 2022 executable records and preserve them unless materially new contradictory evidence appears;
5. research all remaining 2022 candidates together;
6. apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently date by date;
7. assign exactly one PASS / FAIL / BLOCKED verdict to every candidate;
8. modify executable calendar evidence only for admissible PASS dates;
9. rerun calendar tests/coverage only if executable evidence changes;
10. create/complete `reports/data-qualification/dukascopy_usatech_2022_calendar_qualification.md`;
11. create `reports/data-qualification/dukascopy_usatech_2022_calendar_audit.md`;
12. update backup + Recovery Checkpoint after the 2022 annual batch.

Do NOT freeze an execution window, download massive `.bi5`, begin a real backtest, or infer broker truth from exchange-only/other-year/adjacent-date evidence.
