# SESSION BACKUP — 2026-09-14 — 2024 ANNUAL DUKASCOPY CALENDAR QUALIFICATION

## 0. Purpose

Authoritative durable recovery snapshot for completion of the 2024 annual Dukascopy USATECH calendar-qualification batch.

Do not reconstruct 2024 from conversation history. Recover from this file, the current Recovery Checkpoint, the annual protocol and the versioned 2024 reports.

## 1. Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting verified checkpoint/HEAD: `b8e86286fd4057a9a1445d1943732d81ba4a2f63`
- Coverage envelope: `2018-05-01` through `2026-08-14`
- Instrument: Dukascopy `USATECH.IDX/USD` / internal `USATECHIDXUSD`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Real backtest: NOT authorized
- Global calendar coverage: BLOCKED
- Latest observed executable state before/after 2024 batch: `34 calendar tests PASS`
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

Gate implementation:

`tools/irreducible_historical_broker_evidence_gap.py`

Blob:

`1b152b9d1d3ac4c3da135db1528cfb1f687d3a05`

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

## 5. 2024 candidate set freeze

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Candidate set frozen before 2024 outcome research in:

`reports/data-qualification/dukascopy_usatech_2024_calendar_qualification.md`

Freeze commit:

`811976c584a0626e06d1012e9f90c9f9619c4ca2`

Exactly **14** candidates:

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

## 6. Pre-existing executable 2024 evidence

Current `SPECIAL_SESSION_EVIDENCE` had no 2024 record before research.

No 2024 date was inherited as PASS.

## 7. Official Dukascopy 2024 evidence recovered

### Instrument-explicit regular schedule context

Official 2024 U.S. daylight-saving notice:

`https://www.dukascopy.com/europe/english/about/ournews/daylight-saving-time-2024-in-the-us`

It explicitly names `USATECH.IDX/USD`, proving instrument identity and regular/summer schedule context only.

It is not a holiday special-session witness.

### Exact-date / exact-period broker context

Recovered official 2024 material includes:

- New Year transition from end-2023 Christmas/New-Year notice;
- MLK Jan 15 exact CFD/Bullion special-break notice;
- Easter / Good Friday Mar 29 exact-period notice;
- Memorial Day May 27 exact-date notice;
- Juneteenth Jun 19 exact-date notice;
- Labor Day Sep 2 exact-date notice;
- Thanksgiving Nov 28/29 exact-date/period notice;
- Christmas/New Year Dec 24/25/31 exact-period notice.

These notices delegate detailed closures to the Trading Breaks Calendar and do not expose retrievable exact `USATECH.IDX/USD` holiday hours.

No qualifying exact 2024 Dukascopy target-instrument witness was recovered for:

- Presidents Day Feb 19;
- Independence pre-holiday Jul 3;
- Independence Day Jul 4.

Other-year exact schedules remain corroborative-only.

## 8. Trading Breaks Calendar adversarial check

Official routes:

- `https://www.dukascopy.com/swiss/english/marketwatch/trading-breaks-calendar/`
- `https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks`

Current pages identify the calendar as Dukascopy's special-holiday-hours schedule in GMT.

No auditable historical `2024 + USATECH.IDX/USD + exact target-date hours` row was recoverable through the available route.

This is strictly absence of proof and was not treated as historical open/closed evidence.

## 9. Adversarial false lead — U.S. national holiday footnote

A Dukascopy Europe `General Features` page contains a U.S.-national-holiday footnote specifying non-tradable windows.

Official page:

`https://www.dukascopy.com/europe/english/forex/forex-trading-accounts/link/`

Inspection proved the footnote is attached only to:

- `XAU/USD`
- `XAG/USD`

It does not apply to `USATECH.IDX/USD`.

Therefore it was correctly rejected as a broker special-session mapping contract for USATECH.

This is an important anti-false-PASS lesson and must remain preserved.

## 10. Exchange/reference side

Strong same-year official CME material exists for the 2024 holiday calendar and multiple target sessions.

Examples preserved in the qualification report include:

- 2024 holiday-processing reference;
- Labor Day advisory;
- Independence Day settlement schedule;
- Thanksgiving settlement schedule;
- Christmas advisory.

The Independence PDF was visually checked and confirms July 3 Equity Index settlement treatment plus July 4 holiday treatment.

The Thanksgiving PDF was visually checked and confirms Nov 29 Equity & Crypto settlement treatment plus Nov 28 holiday treatment.

Christmas PDF text was retrievable and exact-date; screenshot access failed with cache miss. That screenshot failure is only an access limitation and was not treated as evidence.

Exchange/reference evidence was never promoted into broker truth.

Under strongest-favorable gate application, exact verified exchange timing may be granted and PASS-C still fails without explicit Dukascopy target-instrument + special-session mapping contract.

## 11. Final 2024 qualification result

Completed annual qualification report:

`reports/data-qualification/dukascopy_usatech_2024_calendar_qualification.md`

Completion commit:

`343e179254291192843c070ff2832d71eaded04b`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **14**

Every 2024 candidate remains:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2024 annual calendar coverage:

**BLOCKED — `2024_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 12. 2024 annual audit

Audit report:

`reports/data-qualification/dukascopy_usatech_2024_calendar_audit.md`

Audit commit:

`5392feec278e5edeec85cca5420ccd96737f9c1f`

Audit verdict:

**PASS**

Reason:

`ALL_2024_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

Audit checks include:

- 14/14 candidate completeness;
- frozen set preserved;
- one verdict per date;
- no cross-date inference;
- no cross-year substitution;
- no exchange-only promotion;
- no generic holiday event promoted to exact USATECH hours;
- U.S.-holiday footnote correctly rejected because it applies to metals only;
- Trading Breaks historical-route limitation preserved as absence of proof;
- no executable calendar record without date-level PASS;
- annual-audit PASS not confused with coverage PASS.

## 13. Executable state

No 2024 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` unchanged;
- no 2024 `SPECIAL_SESSION_EVIDENCE` record added;
- no test expectation changed;
- unchanged tests intentionally not rerun for timestamp freshness;
- latest observed calendar suite remains **34 PASS**;
- global special-session evidence remains **24 records**;
- latest observed global coverage remains **111 candidates / 24 resolved / 87 unresolved / BLOCKED**;
- no `.bi5` downloaded;
- no execution window frozen;
- no real backtest started.

## 14. Locked historical state

Do not reopen without materially new evidence:

- `2019-07-03` BLOCKED;
- 2020 annual matrix `1 PASS / 12 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2021 annual matrix `0 PASS / 13 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2022 annual matrix `0 PASS / 12 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2023 annual matrix `0 PASS / 13 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2024 annual matrix `0 PASS / 14 BLOCKED`, annual audit PASS, coverage BLOCKED.

The transient false-PASS route from 2020-01-01 remains permanently rejected.

## 15. Boundaries

Still forbidden:

- global coverage PASS;
- execution-window freeze;
- massive native `.bi5` acquisition;
- real backtest;
- choosing a window merely to evade gaps.

## 16. Exactly one next governed action

**Begin and complete the 2025 annual calendar qualification batch.**

Required sequence:

1. verify branch == Recovery Checkpoint HEAD;
2. enumerate and freeze complete 2025 candidate set before outcome research;
3. identify already-qualified 2025 executable records — especially the existing `2025-01-09` National Day of Mourning record — and preserve them unless materially new contradictory evidence appears;
4. research all remaining 2025 candidates together;
5. apply date-level PASS/FAIL/BLOCKED gate independently;
6. modify executable calendar only for admissible PASS dates;
7. rerun tests/coverage only if executable evidence changes;
8. create/complete `reports/data-qualification/dukascopy_usatech_2025_calendar_qualification.md`;
9. create `reports/data-qualification/dukascopy_usatech_2025_calendar_audit.md`;
10. update backup + Recovery Checkpoint.

Do not freeze an execution window, download `.bi5`, or start a real backtest.
