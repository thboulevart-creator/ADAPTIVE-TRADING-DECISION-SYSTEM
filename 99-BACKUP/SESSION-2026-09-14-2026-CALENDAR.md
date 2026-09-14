# SESSION BACKUP — 2026-09-14 — 2026 BOUNDED DUKASCOPY CALENDAR QUALIFICATION

## 0. Purpose

Authoritative durable recovery snapshot for completion of the final chronological calendar-qualification segment inside the governed envelope.

Do not reconstruct this state from conversation history. Recover from this file, the current Recovery Checkpoint, the annual protocol, and the versioned 2026 reports.

## 1. Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting verified checkpoint/HEAD: `9586e983c3c0f45db683cb2031b5dd3d16bba076`
- Global coverage envelope: `2018-05-01` through `2026-08-14`
- Instrument: Dukascopy `USATECH.IDX/USD` / internal `USATECHIDXUSD`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Real backtest: NOT authorized
- Global calendar coverage: BLOCKED
- Latest observed executable calendar state before/after 2026 batch: `34 tests PASS`
- Latest observed global counts before/after 2026 batch: `111 candidates / 24 resolved / 87 unresolved`

## 2. Mandatory operating method

Calendar qualification follows:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

For a partial terminal year, the annual batch is bounded by the global envelope.

Permanent rule:

- research batch = one calendar year or governed partial-year segment inside the envelope;
- evidence verdict = one candidate date;
- audit = one bounded annual/partial-year batch.

Project-wide discipline remains:

`formalisation → candidate → adversarial break → correction → re-break → verdict`

Allowed verdicts only: PASS / FAIL / BLOCKED.

Never convert absence of proof into PASS.

## 3. Locked evidence gate

Contract:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

PASS routes only:

- PASS-A exact primary broker witness for target date + instrument + relevant hours;
- PASS-B exact archived broker witness with verified provenance;
- PASS-C exact-date broker event + explicit target instrument + explicit broker special-session mapping contract + exact verified exchange/reference timing.

Corroborative-only evidence cannot create PASS.

## 4. 2026 bounded candidate-set freeze

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Bounded call:

`candidate_special_dates(start=date(2026,1,1), end=date(2026,8,14))`

Freeze report:

`reports/data-qualification/dukascopy_usatech_2026_calendar_qualification.md`

Freeze commit:

`7c45defc80964123821181be339b8fba0fcbd547`

Exactly 8 candidates:

1. `2026-01-01 — NEW_YEARS_OBSERVED`
2. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
3. `2026-02-16 — PRESIDENTS_DAY`
4. `2026-04-03 — GOOD_FRIDAY`
5. `2026-05-25 — MEMORIAL_DAY`
6. `2026-06-19 — JUNETEENTH_OBSERVED`
7. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
8. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

No `date(2026, ...)` record existed in current `SPECIAL_SESSION_EVIDENCE` before research.

No candidate was inherited as PASS.

## 5. Broker evidence recovered

Official Dukascopy exact-date/period context recovered for:

- New Year transition into Jan 1;
- MLK Jan 19;
- Presidents Day Feb 16;
- Good Friday Apr 3;
- Memorial Day May 25;
- Juneteenth Jun 19;
- Independence observed Jul 3.

The Jul-3 notice was not reused for Jul-2.

All detailed-closure links lead to Dukascopy's Trading Breaks Calendar.

The currently retrievable Trading Breaks page states that it provides holiday-special hours in GMT but exposes no auditable historical row satisfying:

`2026 + USATECH.IDX/USD + target date + exact special hours`.

No exact target-instrument holiday witness was recovered for any of the 8 dates.

## 6. Juneteenth anomaly

Official Dukascopy Juneteenth notice says:

`Thursday, June 19th 2026`

but `2026-06-19` is Friday.

The numeric date and holiday match the candidate, while the weekday is inconsistent.

Treatment:

- preserved as a documentary anomaly;
- not silently corrected;
- not used as exact timing evidence;
- not promoted to standalone FAIL because it does not assert a contradictory exact USATECH session schedule.

## 7. Jul-2 / Jul-3 independence

Dukascopy Jul-1 notice explicitly announces special breaks on Friday Jul 3, ahead of Saturday Jul 4.

It does not prove Jul-2 treatment.

Official CME 2026 holiday material separately references Jul-2 early-close treatment and Jul-3 Independence Day observance.

Therefore both candidate dates remained independent evidence questions.

## 8. Exchange/reference side

Official CME source:

`https://www.cmegroup.com/trading-hours.html`

The 2026 page provides same-year holiday references and settlement-notice links for the target holidays.

Good Friday PDF:

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2026/good-friday-holiday-settlement-times-2026.pdf`

The PDF was opened and visually inspected; it explicitly identifies `Good Friday 4/3/2026 Settlement Times`.

Exchange evidence was given strongest-favorable treatment where appropriate and was never relabelled as Dukascopy truth.

PASS-C remained incomplete because the broker target-instrument + mapping chain was absent.

## 9. Final 2026 result

Completed qualification report:

`reports/data-qualification/dukascopy_usatech_2026_calendar_qualification.md`

Completion commit:

`481b25d0905b0b04079760965d98f78a6429a53b`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **8**

Every in-envelope 2026 candidate:

**BLOCKED — IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP**

Bounded 2026 coverage:

**BLOCKED — 2026_IN_ENVELOPE_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS**

## 10. 2026 bounded audit

Audit report:

`reports/data-qualification/dukascopy_usatech_2026_calendar_audit.md`

Audit commit:

`77cfcd9b6a05d0c1b974431e1e3149ebe064563c`

Audit verdict:

**PASS**

Reason:

`ALL_2026_IN_ENVELOPE_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

Critical distinction:

- `2026_BOUNDED_ANNUAL_AUDIT = PASS`
- `2026_BOUNDED_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_05_01_TO_2026_08_14_COVERAGE = BLOCKED`

## 11. Executable state

No 2026 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` unchanged;
- no 2026 `SPECIAL_SESSION_EVIDENCE` added;
- no test expectation changed;
- unchanged tests intentionally not rerun;
- latest observed suite remains `34 PASS`;
- latest observed global evidence remains `24 records`;
- latest observed global coverage remains `111 candidates / 24 resolved / 87 unresolved / BLOCKED`;
- no `.bi5` downloaded;
- no execution window frozen;
- no real backtest started;
- envelope not extended past `2026-08-14`.

## 12. Chronological research boundary reached

The annual/partial-year calendar qualification campaign has now reached the exact governed coverage end `2026-08-14`.

Do not start another annual batch.

Do not extend 2026 to Labor Day/Thanksgiving/Christmas unless the global envelope is separately changed under governance.

## 13. Locked historical state summary

Do not reopen without materially new evidence:

- first known unresolved global candidate: `2019-07-03` BLOCKED;
- 2020: `1 PASS / 12 BLOCKED`, audit PASS, coverage BLOCKED;
- 2021: `0 PASS / 13 BLOCKED`, audit PASS, coverage BLOCKED;
- 2022: `0 PASS / 12 BLOCKED`, audit PASS, coverage BLOCKED;
- 2023: `0 PASS / 13 BLOCKED`, audit PASS, coverage BLOCKED;
- 2024: `0 PASS / 14 BLOCKED`, audit PASS, coverage BLOCKED;
- 2025: `1 PASS / 14 BLOCKED`, audit PASS, coverage BLOCKED;
- bounded 2026: `0 PASS / 8 BLOCKED`, audit PASS, coverage BLOCKED.

Existing executable state includes the locked `2025-01-09` National Day of Mourning record and earlier validated records.

The transient 2020-01-01 false-PASS route remains permanently rejected.

## 14. Boundaries still in force

Still BLOCKED/FORBIDDEN:

- global coverage PASS;
- execution-window freeze;
- massive native `.bi5` acquisition;
- real backtest;
- selecting a window to evade known gaps.

## 15. Exactly one next governed action

**Perform the global cross-year calendar coverage-envelope consolidation/audit for `2018-05-01` → `2026-08-14`.**

Required goals:

1. verify current branch against the final 2026 checkpoint;
2. enumerate the executable global candidate/resolution state from the versioned coverage tool;
3. reconcile annual/segment audits against global counts without converting BLOCKED dates into PASS;
4. verify all unresolved gaps remain visible and no candidate is orphaned/contradictory/malformed;
5. apply `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1` to the completed chronological evidence state;
6. issue explicit PASS/FAIL/BLOCKED decisions for:
   - global coverage declaration;
   - execution-window feasibility/freeze;
   - massive acquisition authorization;
7. do not freeze a window merely to evade unresolved gaps;
8. preserve the global audit/conclusion and update Recovery Checkpoint.

Do not download `.bi5` or start a real backtest during this next action.
