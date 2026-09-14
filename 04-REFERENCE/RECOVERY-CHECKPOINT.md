# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — CHRONOLOGICAL CALENDAR QUALIFICATION REACHED ENVELOPE END

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Previous checkpoint / 2026 session start HEAD:** `9586e983c3c0f45db683cb2031b5dd3d16bba076`
- **2026 durable backup:** `99-BACKUP/SESSION-2026-09-14-2026-CALENDAR.md`
  - commit `dc281a739d983d33153a6a0e0a6f88ea58b0e2d5`
- **2026 bounded qualification:** `reports/data-qualification/dukascopy_usatech_2026_calendar_qualification.md`
  - candidate-freeze commit `7c45defc80964123821181be339b8fba0fcbd547`
  - completed qualification commit `481b25d0905b0b04079760965d98f78a6429a53b`
- **2026 bounded audit:** `reports/data-qualification/dukascopy_usatech_2026_calendar_audit.md`
  - commit `77cfcd9b6a05d0c1b974431e1e3149ebe064563c`
- **Annual protocol:** `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
- **Coverage envelope:** `2018-05-01` → `2026-08-14`
- **Chronological annual/segment calendar research:** REACHED GOVERNED ENVELOPE END
- **Execution/backtest window frozen:** NO
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized
- **Global coverage:** BLOCKED
- **Latest observed global coverage:** `111 candidates / 24 resolved / 87 unresolved`
- **Latest observed executable calendar tests:** `34 PASS`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-2026-CALENDAR.md`
4. `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2026_calendar_qualification.md`
8. `reports/data-qualification/dukascopy_usatech_2026_calendar_audit.md`
9. compare active branch against this checkpoint final HEAD before writing anything.

Do not reconstruct 2019–2026 from conversation history.

## 3. LOCKED OPERATING METHOD

Calendar qualification follows:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

Permanent rule:

- **research batch = one bounded calendar year/terminal segment inside the global envelope**;
- **evidence verdict = one candidate date**;
- **audit = one bounded annual/segment batch**.

Project-wide qualification discipline remains:

`formalisation → candidate → adversarial break → correction → re-break → verdict`

Allowed verdicts only: **PASS / FAIL / BLOCKED**.

Annual/segment audit PASS never converts unresolved date-level evidence gaps into coverage PASS.

## 4. LOCKED EVIDENCE GOVERNANCE

### `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Rule verdict: **PASS**.

PASS routes only:

- PASS-A exact primary broker witness for target date + instrument + relevant hours;
- PASS-B exact archived broker witness with verified provenance;
- PASS-C exact-date broker event + explicit target instrument + explicit broker special-session mapping contract + exact verified exchange/reference timing.

Cannot create PASS:

- other-year schedules;
- adjacent dates;
- exchange-only timing;
- generic broker holiday notices;
- current regular hours;
- missing `.bi5` / ticks;
- HTTP/archive failures;
- source-count majority.

### `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Rule verdict: **PASS**.

Current action matrix before global consolidation:

- chronological qualification research: **COMPLETE TO ENVELOPE END**;
- declare global coverage PASS: **BLOCKED**;
- freeze execution window: **BLOCKED**;
- authorize massive `.bi5` acquisition: **BLOCKED**;
- real backtest: **BLOCKED**.

## 5. LOCKED HISTORICAL STATE — DO NOT REOPEN WITHOUT MATERIALLY NEW EVIDENCE

### 2019

`2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Still the first known global unresolved candidate.

### 2020

- candidates: **13**
- PASS: **1**
- FAIL: **0**
- BLOCKED: **12**
- sole PASS: `2020-02-17 — PRESIDENTS_DAY`
- annual audit: **PASS**
- calendar coverage: **BLOCKED**

Transient false-PASS route for `2020-01-01` was adversarially broken and fully revoked.

### 2021

- candidates: **13**
- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**
- annual audit: **PASS**
- calendar coverage: **BLOCKED**

### 2022

- candidates: **12**
- PASS: **0**
- FAIL: **0**
- BLOCKED: **12**
- annual audit: **PASS**
- calendar coverage: **BLOCKED**

### 2023

- candidates: **13**
- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**
- annual audit: **PASS**
- calendar coverage: **BLOCKED**

### 2024

- candidates: **14**
- PASS: **0**
- FAIL: **0**
- BLOCKED: **14**
- annual audit: **PASS**
- calendar coverage: **BLOCKED**

Metal-only U.S.-holiday footnote remains inapplicable to `USATECH.IDX/USD`.

### 2025

- candidates: **15**
- PASS: **1**
- FAIL: **0**
- BLOCKED: **14**
- sole PASS: `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`
- annual audit: **PASS**
- calendar coverage: **BLOCKED**

Jan-9 CME filename includes `2024`, but direct PDF inspection confirms document body is explicitly Jan 9 2025; no provenance mismatch.

## 6. BOUNDED 2026 CANDIDATE SET — FROZEN BEFORE OUTCOME RESEARCH

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Bounded candidate call:

`candidate_special_dates(start=date(2026,1,1), end=date(2026,8,14))`

Freeze commit:

`7c45defc80964123821181be339b8fba0fcbd547`

Exactly **8** in-envelope candidates:

1. `2026-01-01 — NEW_YEARS_OBSERVED`
2. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
3. `2026-02-16 — PRESIDENTS_DAY`
4. `2026-04-03 — GOOD_FRIDAY`
5. `2026-05-25 — MEMORIAL_DAY`
6. `2026-06-19 — JUNETEENTH_OBSERVED`
7. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
8. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

No 2026 date was pre-qualified in current `SPECIAL_SESSION_EVIDENCE`.

Later 2026 dates are outside the governed envelope and were intentionally not researched in this batch.

## 7. BOUNDED 2026 RESEARCH FINDINGS

Official Dukascopy exact-date/period context recovered for:

- New Year transition into Jan 1;
- MLK Jan 19;
- Presidents Day Feb 16;
- Good Friday Apr 3;
- Memorial Day May 25;
- Juneteenth Jun 19;
- Independence observed Jul 3.

All relevant broker notices delegate detailed closures to Dukascopy's Trading Breaks Calendar and do not expose retrievable exact `USATECH.IDX/USD` target-date holiday hours.

Direct Trading Breaks route inspection showed no auditable historical `2026 + USATECH.IDX/USD + target date + exact hours` row.

No independent Jul-2 Dukascopy event/witness was recovered; Jul-3 evidence was not reused for Jul-2.

Official Dukascopy Juneteenth notice contains a documentary inconsistency: it says `Thursday, June 19th 2026`, while Jun 19 2026 is Friday. This was preserved as an anomaly, not silently corrected and not treated as exact timing evidence.

Official CME 2026 Holiday and Trading Hours material provides strong same-year reference evidence; Good Friday 2026 PDF was opened and visually inspected. Exchange evidence was not promoted into broker truth.

Under strongest-favorable exchange treatment, PASS-C still fails because explicit Dukascopy USATECH special-session mapping is absent.

## 8. FINAL BOUNDED 2026 RESULT

Qualification report:

`reports/data-qualification/dukascopy_usatech_2026_calendar_qualification.md`

Completion commit:

`481b25d0905b0b04079760965d98f78a6429a53b`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **8**

Every 2026 in-envelope candidate:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Bounded 2026 coverage:

**BLOCKED — `2026_IN_ENVELOPE_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 9. BOUNDED 2026 AUDIT

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

## 10. EXECUTABLE STATE

No new 2026 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- no 2026 `SPECIAL_SESSION_EVIDENCE` record added;
- no calendar test expectation changed;
- unchanged calendar tests intentionally not rerun for freshness;
- latest observed calendar suite remains **34 PASS**;
- latest observed global `SPECIAL_SESSION_EVIDENCE` remains **24 records**;
- latest observed global coverage remains **111 candidates / 24 resolved / 87 unresolved / BLOCKED**;
- no `.bi5` downloaded;
- no execution window frozen;
- no real backtest started;
- global coverage envelope remains exactly `2018-05-01` → `2026-08-14`.

## 11. CHRONOLOGICAL QUALIFICATION CAMPAIGN STATUS

The year-by-year / terminal-segment qualification campaign has now reached the governed envelope end.

Do **not** start a 2027 batch.

Do **not** continue 2026 beyond Aug 14 without a separately governed envelope change.

Do **not** interpret completion of chronological research as global coverage PASS.

## 12. CLEANUP DEBT / DO NOT REPEAT

- accidental branch `__noop_should_not_exist__` MUST NOT be used;
- unavailable Wayback/archive routes or HTTP failures are not evidence of session behavior;
- do not rerun unchanged tests/audits only for freshness;
- do not reopen locked 2019–2026 dates without materially new evidence;
- do not select an execution window to evade known gaps;
- do not apply metal-only U.S.-holiday rules to USATECH;
- do not reuse Jul-3 evidence for Jul-2;
- preserve the Juneteenth 2026 weekday/date anomaly as an evidence-quality warning.

## 13. EXACTLY ONE NEXT GOVERNED ACTION

**Perform the global cross-year calendar coverage-envelope consolidation/audit for `2018-05-01` → `2026-08-14`.**

Required sequence:

1. verify branch == this checkpoint final HEAD;
2. execute/read the versioned global calendar coverage state and reconcile it with annual/segment qualification reports;
3. confirm exact global candidate/resolved/unresolved counts and preserve all BLOCKED dates visibly;
4. verify no orphan, overlap, malformed evidence or contradiction exists;
5. audit that annual PASS reports were not confused with date/coverage PASS;
6. apply `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1` to the completed chronological state;
7. issue explicit PASS / FAIL / BLOCKED decisions for:
   - global coverage declaration;
   - execution-window feasibility/freeze;
   - massive `.bi5` acquisition authorization;
   - real-backtest authorization;
8. do not choose an execution window merely to evade unresolved gaps;
9. preserve a global coverage audit/conclusion report + backup + updated Recovery Checkpoint.

During this next action, do NOT download `.bi5`, start a real backtest, extend the envelope, or silently discard unresolved historical gaps.
