# SESSION BACKUP — 2026-09-14 — 2025 ANNUAL DUKASCOPY CALENDAR QUALIFICATION

## 0. Purpose

Authoritative durable recovery snapshot for completion of the 2025 annual Dukascopy USATECH calendar-qualification batch.

Do not reconstruct 2025 from conversation history. Recover from this file, the current Recovery Checkpoint, the annual protocol, and the versioned 2025 qualification/audit reports.

## 1. Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting verified checkpoint/HEAD: `3aee1d451122ad728c623ab9f786dc26262a4df1`
- Coverage envelope: `2018-05-01` through `2026-08-14`
- Instrument: Dukascopy `USATECH.IDX/USD` / internal `USATECHIDXUSD`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Real backtest: NOT authorized
- Global calendar coverage: BLOCKED
- Latest observed executable calendar suite before/after 2025 batch: `34 PASS`
- Latest observed global counts before/after 2025 batch: `111 candidates / 24 resolved / 87 unresolved`

## 2. Mandatory operating method

Calendar qualification follows:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

Permanent rule:

- **research batch = one bounded calendar year inside the global coverage envelope**;
- **evidence verdict = one candidate date**;
- **audit = one bounded annual batch**.

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

## 4. 2025 candidate-set freeze

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Freeze report:

`reports/data-qualification/dukascopy_usatech_2025_calendar_qualification.md`

Freeze commit:

`6571ee8b9458313137a09b1113698ffff2ca978a`

Exactly **15** candidates:

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

The candidate set was frozen before 2025 outcome research and was not altered afterward.

## 5. Pre-existing executable PASS

`2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025` existed in `SPECIAL_SESSION_EVIDENCE` before the annual batch.

Executable record:

- reason: `SPECIAL_US_NATIONAL_DAY_OF_MOURNING_2025`;
- `fully_closed_hours_utc = frozenset(range(15, 23))`;
- Dukascopy exact-date source:
  `https://www.dukascopy.com/europe/english/about/ournews/us-market-closure-on-9th-of-january-2025`;
- CME source:
  `https://www.cmegroup.com/trading-hours/files/day-of-mourning-january-9-2024.pdf`.

Important provenance check performed in this batch:

The CME filename contains `2024`, but direct PDF inspection proves the document itself states:

- `JANUARY 9, 2025`;
- `CME GROUP US EQUITIES CLOSE at 8:30 AM CT`;
- all Globex products reopen at their regularly scheduled time for the next trade date.

Therefore there is no newly discovered witness identity mismatch or provenance defect.

The Jan-9 verdict remains **PASS — pre-existing / locked**.

Do not reopen it merely to reconstruct chronology.

## 6. 2025 official Dukascopy evidence recovered

### Regular instrument identity / DST context

Official 2025 U.S. daylight-saving notice:

`https://www.dukascopy.com/swiss/english/about/ournews/daylight-saving-time-2025-in-the-us`

It explicitly names `USATECH.IDX/USD` among CFDs following U.S. summer trading time.

This is regular/summer schedule context only and is not a holiday special-session witness.

### Exact-date / exact-period holiday context

Recovered official Dukascopy material includes:

- New-Year transition into `2025-01-01` from the 2024-12-20 Christmas/New-Year notice;
- MLK `2025-01-20` exact CFD/Bullion special-break notice;
- Presidents Day `2025-02-17` exact CFD/Bullion special-break notice;
- Good Friday `2025-04-18` Easter-weekend notice;
- Memorial Day `2025-05-26` exact-date notice;
- Juneteenth `2025-06-19` exact-date notice;
- Independence Day `2025-07-04` exact-date notice;
- Labor Day `2025-09-01` exact-date notice;
- Thanksgiving `2025-11-27 / 2025-11-28` exact-period notice;
- Christmas/New Year `2025-12-24 / 2025-12-25 / 2025-12-31` exact-period notice.

These articles delegate detailed market hours to the Trading Breaks Calendar and do not expose retrievable exact `USATECH.IDX/USD` holiday hours.

No admissible exact broker witness was recovered for `2025-07-03` independently. The Jul-4 notice was not reused to prove Jul-3 treatment.

## 7. Trading Breaks Calendar adversarial check

Official route:

`https://www.dukascopy.com/swiss/english/marketwatch/trading-breaks-calendar/`

The current retrievable page states that it shows special holiday trading hours in GMT.

However, through the available route it exposes no auditable historical row satisfying:

`2025 + USATECH.IDX/USD + target date + exact special hours`.

This remained absence of proof, not evidence of historical session behavior.

No PASS-A/PASS-B witness was invented from the route limitation.

## 8. Exchange/reference side

Strong same-year official CME evidence was recovered and visually inspected where PDF material was used.

Important preserved examples:

### Jan-9 National Day of Mourning

`https://www.cmegroup.com/trading-hours/files/day-of-mourning-january-9-2024.pdf`

Content explicitly refers to Jan 9 2025 and U.S. equity close at 08:30 CT.

### Good Friday

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/2025-good-friday-clearing-advisory.pdf`

Exact Apr 18 2025 advisory.

### Juneteenth

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/juneteenth-day-settlement-times-2025.pdf`

Exact Jun 19 2025 material.

### Independence Day

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/2025-4th-of-july-clearing-advisory.pdf`

Exact Jul 4 2025 advisory.

### Thanksgiving

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/thanksgiving-holiday-settlement-times-2025.pdf`

No settlement prices on Thu Nov 27; Equity & Crypto settlement at 12:00 CT on Fri Nov 28.

### Christmas

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/christmas-holiday-settlement-times-2025.pdf`

Equity & Crypto settlement at 12:00 CT on Dec 24; no settlement prices on Dec 25.

Exchange evidence was never promoted directly into broker truth.

Strongest-favorable treatment of exact exchange timing still leaves PASS-C incomplete for the unresolved dates because explicit target-instrument Dukascopy holiday mapping is absent.

## 9. Final 2025 qualification result

Completed annual qualification report:

`reports/data-qualification/dukascopy_usatech_2025_calendar_qualification.md`

Completion commit:

`39d3a9e5c67a2d1f2294428273a1f5425b08e038`

Final matrix:

- PASS: **1**
- FAIL: **0**
- BLOCKED: **14**

Sole PASS:

- `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025` — pre-existing / locked.

All other 14 candidates:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2025 annual calendar coverage:

**BLOCKED — `2025_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 10. 2025 annual audit

Audit report:

`reports/data-qualification/dukascopy_usatech_2025_calendar_audit.md`

Audit commit:

`04dd7b59ab66f98a54073f812177ec7582e6d1b8`

Audit verdict:

**PASS**

Reason:

`ALL_2025_CANDIDATES_ACCOUNTED_FOR_WITH_LOCKED_PASS_PRESERVED_AND_NO_FALSE_PASS_BYPASS`

Audit checks include:

- 15/15 candidate completeness;
- frozen set preserved;
- one verdict per date;
- Jan-9 pre-existing PASS preserved and provenance checked;
- no cross-date inference;
- no cross-year substitution;
- no exchange-only promotion;
- no generic broker holiday notice promoted to exact USATECH hours;
- DST instrument identity not misused as holiday mapping;
- Trading Breaks historical-route limitation preserved as absence of proof;
- no executable calendar record without date-level PASS;
- annual-audit PASS not confused with coverage PASS.

## 11. Executable state

No **new** 2025 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- the pre-existing Jan-9 record remains unchanged;
- no new 2025 `SPECIAL_SESSION_EVIDENCE` record was added;
- no test expectation changed;
- unchanged tests intentionally not rerun for timestamp freshness;
- latest observed calendar suite remains **34 PASS**;
- global special-session evidence remains **24 records**;
- latest observed global coverage remains **111 candidates / 24 resolved / 87 unresolved / BLOCKED**;
- no `.bi5` downloaded;
- no execution window frozen;
- no real backtest started.

## 12. Locked historical state

Do not reopen without materially new evidence:

- `2019-07-03` BLOCKED;
- 2020 annual matrix `1 PASS / 12 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2021 annual matrix `0 PASS / 13 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2022 annual matrix `0 PASS / 12 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2023 annual matrix `0 PASS / 13 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2024 annual matrix `0 PASS / 14 BLOCKED`, annual audit PASS, coverage BLOCKED;
- 2025 annual matrix `1 PASS / 14 BLOCKED`, annual audit PASS, coverage BLOCKED.

The transient false-PASS route from `2020-01-01` remains permanently rejected.

## 13. Boundaries

Still forbidden:

- global coverage PASS;
- execution-window freeze;
- massive native `.bi5` acquisition;
- real backtest;
- choosing a future execution window merely to evade known gaps.

## 14. Exactly one next governed action

**Begin and complete the 2026 qualification batch bounded by the current global coverage end `2026-08-14`.**

This is **not** a full-calendar-year 2026 claim. Only candidate dates inside `2026-01-01` through `2026-08-14` belong to the current governed envelope.

Required sequence:

1. verify branch == Recovery Checkpoint HEAD;
2. enumerate and freeze the exact 2026 candidate set bounded by `end=date(2026,8,14)` before outcome research;
3. identify any already-qualified 2026 executable records;
4. research all remaining in-envelope 2026 candidates together;
5. apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently date by date;
6. assign exactly one PASS / FAIL / BLOCKED verdict per in-envelope candidate;
7. modify executable calendar only for admissible PASS dates;
8. rerun tests/coverage only if executable evidence changes;
9. create/complete `reports/data-qualification/dukascopy_usatech_2026_calendar_qualification.md` with an explicit `coverage_end = 2026-08-14` boundary;
10. create `reports/data-qualification/dukascopy_usatech_2026_calendar_audit.md` with the same bounded scope;
11. update backup + Recovery Checkpoint.

Do not freeze an execution window, download `.bi5`, or start a real backtest.
