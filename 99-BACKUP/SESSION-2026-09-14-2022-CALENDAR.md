# SESSION BACKUP — 2026-09-14 — 2022 ANNUAL DUKASCOPY CALENDAR QUALIFICATION

## 0. Purpose

Authoritative durable recovery snapshot for completion of the 2022 annual Dukascopy USATECH calendar-qualification batch.

Do not reconstruct 2022 from conversation history. Recover from this file, the current Recovery Checkpoint, the annual protocol, and the versioned 2022 reports.

## 1. Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting verified checkpoint/HEAD: `93896f7476ae27991b646b4ba2aa15c1f0aa79d9`
- Coverage envelope: `2018-05-01` through `2026-08-14`
- Instrument: Dukascopy `USATECH.IDX/USD` / internal `USATECHIDXUSD`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Real backtest: NOT authorized
- Global calendar coverage: BLOCKED
- Latest observed executable state before/after 2022 batch: `34 calendar tests PASS`
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

## 4. 2022 candidate set freeze

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Candidate set frozen before 2022 outcome research in:

`reports/data-qualification/dukascopy_usatech_2022_calendar_qualification.md`

Freeze commit:

`81a505df146c3bc09f5b68dec5dbef39e4e5caaf`

Exactly **12** candidates:

1. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
2. `2022-02-21 — PRESIDENTS_DAY`
3. `2022-04-15 — GOOD_FRIDAY`
4. `2022-05-30 — MEMORIAL_DAY`
5. `2022-06-20 — JUNETEENTH_OBSERVED`
6. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
7. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
8. `2022-09-05 — LABOR_DAY`
9. `2022-11-24 — THANKSGIVING_DAY`
10. `2022-11-25 — THANKSGIVING_FRIDAY`
11. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
12. `2022-12-26 — CHRISTMAS_OBSERVED`

Boundary facts:

- Jan 1 2022 is Saturday; observed date Dec 31 2021 falls outside bounded 2022 batch.
- Dec 31 2022 is Saturday; weekday guard excludes New Year's Eve candidate.
- Juneteenth first appears in generator in 2022, observed Monday June 20.

## 5. Pre-existing executable 2022 evidence

Current `SPECIAL_SESSION_EVIDENCE` had no 2022 record before research.

No 2022 date was inherited as PASS.

## 6. Official Dukascopy 2022 evidence recovered

Exact-date/period official broker context recovered included:

### MLK — Jan 17

Official notice published Jan 13 2022:

`https://www.dukascopy.com/swiss/pt/about/ournews/market-closures-on-martin-luther-king-day`

Exact-date CFD/Bullion special-break notice, but no retrievable explicit `USATECH.IDX/USD` hours.

### Memorial Day — May 30

Official Dukascopy Europe notice published May 27 2022:

`https://www.dukascopy.com/europe/arabic/about/ournews/market-closures-on-memorial-day-dbl202403/`

Exact-date special-break notice, but no retrievable target-instrument hours.

### Juneteenth — Jun 20

Official Dukascopy notice published Jun 16 2022:

`https://www.dukascopy.com/swiss/english/about/ournews/juneteenth-national-independence-day?p=DFT`

Exact-date broker event, but detailed schedule delegated to Trading Breaks Calendar and no retrievable target-instrument hours.

### Independence Day — Jul 4

Official notice published Jul 1 2022:

`https://www.dukascopy.com/swiss/english/about/ournews/market-closures-on-independence-day-in-the-us-dbl202410/`

Exact Jul-4 broker event, but no retrievable explicit target-instrument exact hours.

The same notice does not establish a Jul-1 Dukascopy special schedule, so Jul-1 remains independently unresolved.

### Christmas / New Year period

Official notice published Dec 9 2022:

`https://www.dukascopy.com/swiss/arabic/about/ournews/market-closures-during-x-mas-and-new-year`

Exact-period generic FX/Bullion/CFD context, but no retrievable Dec-23/Dec-26 USATECH exact-hours witness.

## 7. Trading Breaks Calendar attack

The `Detailed market closures` links from exact-date company notices were followed.

They resolve to Dukascopy's current `Trading Breaks Calendar`, which states that it publishes holiday special schedules in GMT.

However, the retrievable current page exposes no historical 2022 `USATECH.IDX/USD` row and no exact 2022 instrument-hour witness.

This did NOT become evidence of historical open/closed behavior.

Historical Trading Breaks witness route therefore remains unavailable for PASS-A/PASS-B.

## 8. Exchange/reference side

Strong same-year official CME evidence exists for the 2022 holiday calendar, including Globex windows for:

- MLK;
- Presidents Day;
- Good Friday;
- Memorial Day;
- Juneteenth;
- Independence Day;
- Labor Day;
- Thanksgiving;
- Christmas.

Official CME Thanksgiving settlement material also covers Nov 24-25 2022.

Exchange/reference evidence was not promoted into broker truth.

Under strongest-favorable gate application, exact verified exchange timing can be granted and PASS-C still fails without explicit Dukascopy target-instrument + special-session mapping contract.

## 9. Final 2022 qualification result

Completed annual qualification report:

`reports/data-qualification/dukascopy_usatech_2022_calendar_qualification.md`

Completion commit:

`4e2eeec5b37a679b6f8a9f9e0fa064b038d40e81`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **12**

Every 2022 candidate remains:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2022 annual calendar coverage:

**BLOCKED — `2022_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 10. 2022 annual audit

Audit report:

`reports/data-qualification/dukascopy_usatech_2022_calendar_audit.md`

Audit commit:

`b4b20a77dde86b2481d896d7ae5076451b4f6c13`

Audit verdict:

**PASS**

Reason:

`ALL_2022_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

Audit checks included:

- 12/12 candidate completeness;
- frozen set preserved;
- one verdict per date;
- no cross-date inference;
- no cross-year substitution;
- no exchange-only promotion;
- no generic broker notice promoted to exact USATECH hours;
- Trading Breaks historical-route failure preserved as absence of proof;
- no executable calendar record without date-level PASS;
- no annual-audit PASS confused with coverage PASS.

## 11. Executable state

No 2022 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` unchanged;
- no 2022 `SPECIAL_SESSION_EVIDENCE` record added;
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
- 2022 annual matrix `0 PASS / 12 BLOCKED`, annual audit PASS, coverage BLOCKED.

The transient false-PASS route from 2020-01-01 remains permanently rejected.

## 13. Boundaries

Still forbidden:

- global coverage PASS;
- execution-window freeze;
- massive native `.bi5` acquisition;
- real backtest;
- choosing a window merely to evade gaps.

## 14. Exactly one next governed action

**Begin and complete the 2023 annual calendar qualification batch.**

Required sequence:

1. verify branch == Recovery Checkpoint HEAD;
2. enumerate and freeze complete 2023 candidate set before outcome research;
3. identify any already-qualified 2023 executable records;
4. research all remaining 2023 candidates together;
5. apply date-level PASS/FAIL/BLOCKED gate independently;
6. modify executable calendar only for admissible PASS dates;
7. rerun tests/coverage only if executable evidence changes;
8. create/complete `dukascopy_usatech_2023_calendar_qualification.md`;
9. create `dukascopy_usatech_2023_calendar_audit.md`;
10. update backup + Recovery Checkpoint.

Do not freeze an execution window, download `.bi5`, or start a real backtest.
