# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — 2025 ANNUAL DUKASCOPY CALENDAR QUALIFICATION COMPLETE

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Previous checkpoint / 2025 session start HEAD:** `3aee1d451122ad728c623ab9f786dc26262a4df1`
- **2025 durable backup:** `99-BACKUP/SESSION-2026-09-14-2025-CALENDAR.md`
  - commit `8bdadc880f3f56e86bcbca3408555347b697cec3`
- **2025 annual qualification:** `reports/data-qualification/dukascopy_usatech_2025_calendar_qualification.md`
  - candidate freeze commit `6571ee8b9458313137a09b1113698ffff2ca978a`
  - completed qualification commit `39d3a9e5c67a2d1f2294428273a1f5425b08e038`
- **2025 annual audit:** `reports/data-qualification/dukascopy_usatech_2025_calendar_audit.md`
  - commit `04dd7b59ab66f98a54073f812177ec7582e6d1b8`
- **Annual protocol:** `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
- **Coverage envelope:** `2018-05-01` → `2026-08-14`
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
3. `99-BACKUP/SESSION-2026-09-14-2025-CALENDAR.md`
4. `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2025_calendar_qualification.md`
8. `reports/data-qualification/dukascopy_usatech_2025_calendar_audit.md`
9. compare active branch against this checkpoint final HEAD before writing anything.

Do not reconstruct 2019–2025 from conversation history.

## 3. LOCKED OPERATING METHOD

Calendar qualification follows:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

Permanent rule:

- **research batch = one calendar year bounded by the global coverage envelope**;
- **evidence verdict = one candidate date**;
- **audit = one bounded annual batch**.

Annual batching is an efficiency mechanism only. It MUST NOT weaken date-specific proof or allow cross-date / cross-year inference.

Project-wide qualification discipline remains:

`formalisation → candidate → adversarial break → correction → re-break → verdict`

Allowed verdicts only: **PASS / FAIL / BLOCKED**.

## 4. LOCKED EVIDENCE GOVERNANCE

### `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Rule verdict: **PASS**.

PASS routes only:

- PASS-A exact primary broker witness for target date + instrument + relevant hours;
- PASS-B exact archived broker witness with verified provenance;
- PASS-C exact-date broker event + explicit target instrument + explicit broker special-session mapping contract + exact verified exchange/reference timing.

The following cannot create PASS:

- other-year schedules;
- adjacent dates;
- exchange-only timing;
- generic broker holiday notices;
- current regular hours;
- missing `.bi5` / ticks;
- HTTP/archive failures;
- majority-of-sources reasoning.

### `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Rule verdict: **PASS**.

Current action matrix:

- continue bounded annual qualification: **PASS**;
- declare global coverage PASS: **BLOCKED**;
- freeze execution window: **BLOCKED**;
- authorize massive `.bi5` acquisition: **BLOCKED**;
- real backtest: **BLOCKED**.

## 5. LOCKED HISTORICAL STATE — DO NOT REOPEN WITHOUT MATERIALLY NEW EVIDENCE

### 2019

`2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Still the first global unresolved candidate.

### 2020

- candidates: **13**
- PASS: **1**
- FAIL: **0**
- BLOCKED: **12**
- sole PASS: `2020-02-17 — PRESIDENTS_DAY`
- annual audit: **PASS**
- calendar coverage: **BLOCKED**

The transient false-PASS route for `2020-01-01` was adversarially broken and fully revoked. Never resurrect `generic broker context + exact exchange timing + same holiday event = PASS`.

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

The metal-only U.S.-national-holiday footnote remains inapplicable to `USATECH.IDX/USD`.

## 6. 2025 CANDIDATE SET — FROZEN BEFORE OUTCOME RESEARCH

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Freeze commit:

`6571ee8b9458313137a09b1113698ffff2ca978a`

Exactly **15** candidates were frozen before evidence research:

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

One candidate was already executable PASS before the batch:

- `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`.

## 7. 2025 RESEARCH FINDINGS

The annual campaign searched exact dates, holiday names, `USATECH` / `USATECH.IDX/USD`, Dukascopy Bank / Europe news routes, multilingual variants, Trading Breaks routes and same-year CME evidence.

Important official Dukascopy material recovered:

- 2025 DST notice explicitly naming `USATECH.IDX/USD` for regular/summer schedule context;
- exact-date MLK notice;
- exact-date Presidents Day notice;
- exact-period Good Friday/Easter notice;
- exact-date Memorial Day notice;
- exact-date Juneteenth notice;
- exact-date Independence Day notice;
- exact-date Labor Day notice;
- exact-date/period Thanksgiving notice;
- exact-period Christmas/New-Year notices spanning Jan 1 and year-end 2025.

The holiday notices delegate detailed hours to the Trading Breaks Calendar and do not expose retrievable exact target-instrument holiday hours.

No admissible independent Jul-3 broker witness was recovered; the Jul-4 notice was not reused across dates.

The Trading Breaks route was followed adversarially. Its current retrievable page identifies its holiday-hours function in GMT but exposes no auditable historical `2025 + USATECH.IDX/USD + exact target-date hours` record.

This is absence of proof, not historical open/closed evidence.

Strong same-year CME evidence was recovered for several target dates and visually inspected where PDF evidence was used.

Under strongest-favorable treatment, exact exchange timing still cannot complete PASS-C without explicit Dukascopy target-instrument special-session mapping.

## 8. PRE-EXISTING JAN-9 PASS PROVENANCE CHECK

The current executable record references:

`https://www.cmegroup.com/trading-hours/files/day-of-mourning-january-9-2024.pdf`

The filename contains `2024`, but the actual PDF was directly opened and visually inspected.

Its content explicitly states:

- `JANUARY 9, 2025`;
- CME Group U.S. equities close at `08:30 AM CT`;
- U.S. Equity Index products close on Globex at `08:30 AM CT`;
- Globex products reopen at their regularly scheduled time for the next trade date.

No witness identity mismatch or provenance defect was found.

Therefore the pre-existing Jan-9 PASS remains locked and unchanged.

## 9. FINAL 2025 QUALIFICATION RESULT

Annual qualification report:

`reports/data-qualification/dukascopy_usatech_2025_calendar_qualification.md`

Completed qualification commit:

`39d3a9e5c67a2d1f2294428273a1f5425b08e038`

Final matrix:

- PASS: **1**
- FAIL: **0**
- BLOCKED: **14**

Sole PASS:

- `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025` — pre-existing / locked.

All remaining candidates:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2025 annual calendar coverage:

**BLOCKED — `2025_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 10. 2025 ANNUAL AUDIT

Audit report:

`reports/data-qualification/dukascopy_usatech_2025_calendar_audit.md`

Audit commit:

`04dd7b59ab66f98a54073f812177ec7582e6d1b8`

Audit verdict:

**PASS**

Reason:

`ALL_2025_CANDIDATES_ACCOUNTED_FOR_WITH_LOCKED_PASS_PRESERVED_AND_NO_FALSE_PASS_BYPASS`

Audit verified:

- 15/15 candidate completeness;
- frozen set preserved;
- exactly one verdict per date;
- Jan-9 pre-existing PASS preserved and provenance checked;
- no cross-year or adjacent-date substitution;
- no exchange-only promotion to broker truth;
- no generic broker holiday notice promoted to exact USATECH timing;
- DST instrument identity not misused as holiday mapping;
- Trading Breaks historical-route limitation kept as absence of proof;
- no hidden gaps;
- no executable record without admissible date-level PASS;
- annual-audit PASS not confused with calendar-coverage PASS;
- no execution-window / acquisition bypass.

Critical distinction:

- `2025_ANNUAL_AUDIT = PASS`
- `2025_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

## 11. EXECUTABLE STATE

No **new** 2025 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- the Jan-9 record remains unchanged;
- no new 2025 `SPECIAL_SESSION_EVIDENCE` record was added;
- no calendar test expectation changed;
- calendar tests were intentionally not rerun merely for timestamp freshness;
- latest observed calendar suite remains **34 PASS**;
- latest observed global `SPECIAL_SESSION_EVIDENCE` remains **24** records;
- latest observed global coverage remains **111 candidates / 24 resolved / 87 unresolved / BLOCKED**;
- no `.bi5` was downloaded;
- no execution window was frozen;
- no real backtest was started.

## 12. CLEANUP DEBT / DO NOT REPEAT

- accidental branch `__noop_should_not_exist__` MUST NOT be used;
- unavailable Wayback/archive routes or HTTP failures are not evidence of session behavior;
- do not rerun unchanged tests/audits only for freshness;
- do not reopen locked 2019–2025 dates without materially new evidence;
- do not select an execution window to evade known gaps;
- do not apply the metal-only U.S.-holiday footnote to USATECH;
- do not treat the `2024` token in the Jan-9 CME filename as a mismatch: the document body explicitly identifies Jan 9 2025.

## 13. EXACTLY ONE NEXT GOVERNED ACTION

**Begin and complete the 2026 calendar qualification batch bounded by the global coverage end `2026-08-14`.**

This is a **partial-calendar-year batch by design** because the governed coverage envelope ends on Aug 14 2026. Do not extend the scope to later 2026 dates without a separately governed envelope change.

Expected in-envelope candidate set from the current generator consists of **8 dates** to be formally frozen before outcome research:

1. `2026-01-01 — NEW_YEARS_OBSERVED`
2. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
3. `2026-02-16 — PRESIDENTS_DAY`
4. `2026-04-03 — GOOD_FRIDAY`
5. `2026-05-25 — MEMORIAL_DAY`
6. `2026-06-19 — JUNETEENTH_OBSERVED`
7. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
8. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

Required sequence:

1. verify branch == this checkpoint final HEAD;
2. formally enumerate and freeze the exact candidate set with `start=2026-01-01`, `end=2026-08-14` before outcome research;
3. identify any already-qualified in-envelope 2026 executable records;
4. research all remaining in-envelope 2026 candidates together;
5. apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently to every date;
6. assign exactly one PASS / FAIL / BLOCKED verdict per candidate;
7. modify executable calendar evidence only for admissible PASS dates;
8. rerun calendar tests/coverage only if executable evidence changes;
9. create/complete `reports/data-qualification/dukascopy_usatech_2026_calendar_qualification.md` with explicit `coverage_end = 2026-08-14`;
10. create `reports/data-qualification/dukascopy_usatech_2026_calendar_audit.md` with the same bounded scope;
11. update backup + Recovery Checkpoint after the bounded 2026 batch.

During this action, do NOT freeze an execution window, download massive `.bi5`, begin a real backtest, extend the global coverage envelope, or infer broker truth from exchange-only / other-year / adjacent-date evidence.
