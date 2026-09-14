# SESSION BACKUP — 2026-09-14 — 2023 ANNUAL DUKASCOPY CALENDAR QUALIFICATION

## 0. Purpose

Authoritative durable recovery snapshot for completion of the 2023 annual Dukascopy USATECH calendar-qualification batch.

Do not reconstruct 2023 from conversation history. Recover from this file, the current Recovery Checkpoint, the annual protocol, and the versioned 2023 reports.

## 1. Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting verified checkpoint/HEAD: `ffc82a429e41f437df6894b3dfc2d8d3bde94175`
- Coverage envelope: `2018-05-01` through `2026-08-14`
- Instrument: Dukascopy `USATECH.IDX/USD` / internal `USATECHIDXUSD`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Real backtest: NOT authorized
- Global calendar coverage: BLOCKED
- Latest observed executable calendar state before/after 2023 batch: `34 tests PASS`
- Latest observed global counts: `111 candidates / 24 resolved / 87 unresolved`

## 2. Mandatory operating method

Calendar qualification follows:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

Permanent rule:

- **research batch = one complete calendar year**;
- **evidence verdict = one candidate date**;
- **audit = one complete calendar year**.

Annual batching never weakens date-specific evidence.

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

PASS routes only:

- PASS-A exact primary broker witness for target date + instrument + relevant hours;
- PASS-B exact archived broker witness with verified provenance;
- PASS-C exact-date broker event + explicit target instrument + explicit broker special-session mapping contract + exact verified exchange/reference timing.

Corroborative-only material cannot create PASS:

- another year;
- adjacent holiday date;
- exchange-only timing;
- generic broker holiday notice;
- current regular hours;
- missing `.bi5` / ticks;
- HTTP/archive failures;
- source-count majority.

## 4. 2023 candidate set freeze

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Candidate set frozen before 2023 outcome research in:

`reports/data-qualification/dukascopy_usatech_2023_calendar_qualification.md`

Freeze commit:

`c37468b58782b789aea289a6f5bd92813e1e7dcd`

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

Boundary facts:

- Jan 1 2023 is Sunday; observed date is Jan 2.
- Dec 31 2023 is Sunday; weekday guard excludes New Year's Eve candidate.
- Juneteenth falls directly on Monday Jun 19.

## 5. Pre-existing executable 2023 evidence

Current `SPECIAL_SESSION_EVIDENCE` contained no 2023 record before research.

No 2023 date was inherited as PASS.

## 6. Official Dukascopy 2023 evidence recovered

### Instrument-explicit regular schedule context

Official Dukascopy 2023 DST notice:

`https://www.dukascopy.com/europe/english/about/ournews/change-to-daylight-saving-time-2023-in-the-us`

This explicitly names `USATECH.IDX/USD` among CFDs affected by the U.S. summer schedule change.

It is regular/summer schedule context only, not a holiday special-session witness.

### New Year transition

Official end-2022 Christmas/New-Year notice:

`https://www.dukascopy.com/swiss/arabic/about/ournews/market-closures-during-x-mas-and-new-year`

Generic exact-period FX/Bullion/CFD context only; no exact Jan-2 USATECH hours.

### Juneteenth — Jun 19

Official notice:

`https://www.dukascopy.com/swiss/pt/about/ournews/juneteenth-national-independence-day-dbl202591/`

Exact-date broker holiday event; detailed closures delegated to Trading Breaks Calendar; no retrievable exact USATECH hours.

### Thanksgiving — Nov 23 / Nov 24

Official notice:

`https://www.dukascopy.com/swiss/english/about/ournews/thanksgiving-day-in-the-us-dbl202684`

Exact-date/period broker event; detailed Thursday/Friday closures delegated; no retrievable exact USATECH hours.

### Christmas — Dec 22 / Dec 25

Official notice:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-christmas-and-new-year-dbl202761`

Exact-period broker event; detailed schedules delegated; no retrievable exact USATECH hours.

## 7. Trading Breaks Calendar adversarial check

Official routes:

- `https://www.dukascopy.com/swiss/english/marketwatch/trading-breaks-calendar/`
- `https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks`

Current content identifies the calendar as the special-holiday schedule in GMT but does not expose an auditable historical `2023 + USATECH.IDX/USD + exact date hours` record.

This remains **absence of proof**, not historical open/closed evidence.

No PASS-A/PASS-B witness was created from the route limitation.

## 8. Targeted broker retrieval with no qualifying witness

No admissible exact/archived `2023 + USATECH.IDX/USD + target holiday hours` witness was recovered for:

- MLK Jan 16;
- Presidents Day Feb 20;
- Good Friday Apr 7;
- Memorial Day May 29;
- Independence pre-holiday Jul 3;
- Independence Day Jul 4;
- Labor Day Sep 4.

Other-year exact schedules remain corroborative-only.

Dukascopy research/market-news articles published on holiday dates were rejected as session evidence because content publication does not prove target-instrument tradability or broker hours.

## 9. Same-year exchange/reference side

Strong official CME evidence exists for several 2023 sessions, including Presidents Day, Memorial Day, Juneteenth, Labor Day, Thanksgiving and Christmas.

Examples:

- `https://www.cmegroup.com/tools-information/holiday-calendar/files/presidents-day-holiday-settlement-times-2023.pdf`
- `https://www.cmegroup.com/tools-information/holiday-calendar/files/2023-memorial-day-advisory.pdf`
- `https://www.cmegroup.com/trading-hours/files/juneteenth-2023.pdf`
- `https://www.cmegroup.com/trading-hours/files/labor-day-2023.pdf`
- `https://www.cmegroup.com/tools-information/holiday-calendar/files/2023-thanksgiving-advisory.pdf`
- `https://www.cmegroup.com/trading-hours/files/thanksgiving-day-2023.pdf`
- `https://www.cmegroup.com/trading-hours/files/christmas-day-2023.pdf`

Exchange/reference evidence was never promoted into broker truth.

Under strongest-favorable gate application, even granting exact verified exchange timing cannot complete PASS-C without explicit Dukascopy target instrument + special-session mapping contract.

## 10. Final 2023 qualification result

Completed annual qualification report:

`reports/data-qualification/dukascopy_usatech_2023_calendar_qualification.md`

Completion commit:

`295c8c2cfbddbd5bb31689e7623bdce4a8ab2aa0`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**

Every 2023 candidate remains:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2023 annual calendar coverage:

**BLOCKED — `2023_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 11. 2023 annual audit

Audit report:

`reports/data-qualification/dukascopy_usatech_2023_calendar_audit.md`

Audit commit:

`48adbc3b2c21f271e879c6fec7563539e13d25da`

Audit verdict:

**PASS**

Reason:

`ALL_2023_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

Audit checks include:

- 13/13 candidate completeness;
- frozen set preserved;
- one verdict per date;
- no cross-date inference;
- no cross-year substitution;
- no exchange-only promotion;
- no generic broker holiday event promoted to exact USATECH hours;
- Trading Breaks historical-route limitation preserved as absence of proof;
- no executable calendar record without date-level PASS;
- annual-audit PASS not confused with coverage PASS.

## 12. Executable state

No 2023 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` unchanged;
- no 2023 `SPECIAL_SESSION_EVIDENCE` record added;
- no test expectation changed;
- unchanged tests intentionally not rerun for timestamp freshness;
- latest observed calendar suite remains **34 PASS**;
- global special-session evidence remains **24 records**;
- latest observed global coverage remains **111 candidates / 24 resolved / 87 unresolved / BLOCKED**;
- no `.bi5` downloaded;
- no execution window frozen;
- no real backtest started.

## 13. Locked historical state

Do not reopen without materially new evidence:

- `2019-07-03` BLOCKED;
- 2020 annual matrix `1 PASS / 12 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2021 annual matrix `0 PASS / 13 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2022 annual matrix `0 PASS / 12 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2023 annual matrix `0 PASS / 13 BLOCKED`, annual audit PASS, coverage BLOCKED.

The transient false-PASS route from 2020-01-01 remains permanently rejected.

## 14. Boundaries

Still forbidden:

- global coverage PASS;
- execution-window freeze;
- massive native `.bi5` acquisition;
- real backtest;
- choosing a window merely to evade gaps.

## 15. Exactly one next governed action

**Begin and complete the 2024 annual calendar qualification batch.**

Required sequence:

1. verify branch == Recovery Checkpoint HEAD;
2. enumerate and freeze the complete 2024 candidate set before outcome research;
3. identify any already-qualified 2024 executable records;
4. research all remaining 2024 candidates together;
5. apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently date by date;
6. assign exactly one PASS / FAIL / BLOCKED verdict per candidate;
7. modify executable calendar only for admissible PASS dates;
8. rerun tests/coverage only if executable evidence changes;
9. create/complete `reports/data-qualification/dukascopy_usatech_2024_calendar_qualification.md`;
10. create `reports/data-qualification/dukascopy_usatech_2024_calendar_audit.md`;
11. update backup + Recovery Checkpoint.

Do not freeze an execution window, download `.bi5`, or start a real backtest.
