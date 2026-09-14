# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — 2023 ANNUAL DUKASCOPY CALENDAR QUALIFICATION COMPLETE

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Previous checkpoint / 2023 session start HEAD:** `ffc82a429e41f437df6894b3dfc2d8d3bde94175`
- **2023 durable backup:** `99-BACKUP/SESSION-2026-09-14-2023-CALENDAR.md`
  - commit `89231765605ccd2b5e026ba489de3a2ae431a6e8`
- **2023 annual qualification:** `reports/data-qualification/dukascopy_usatech_2023_calendar_qualification.md`
  - candidate freeze commit `c37468b58782b789aea289a6f5bd92813e1e7dcd`
  - completed qualification commit `295c8c2cfbddbd5bb31689e7623bdce4a8ab2aa0`
- **2023 annual audit:** `reports/data-qualification/dukascopy_usatech_2023_calendar_audit.md`
  - commit `48adbc3b2c21f271e879c6fec7563539e13d25da`
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
3. `99-BACKUP/SESSION-2026-09-14-2023-CALENDAR.md`
4. `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2023_calendar_qualification.md`
8. `reports/data-qualification/dukascopy_usatech_2023_calendar_audit.md`
9. compare active branch against this checkpoint final HEAD before writing anything.

Do not reconstruct 2019–2023 from conversation history.

## 3. LOCKED OPERATING METHOD

Calendar qualification follows:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

Permanent rule:

- **research batch = one complete calendar year**;
- **evidence verdict = one candidate date**;
- **audit = one complete calendar year**.

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

- continue annual qualification: **PASS**;
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

## 6. 2023 CANDIDATE SET — FROZEN BEFORE OUTCOME RESEARCH

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Freeze commit:

`c37468b58782b789aea289a6f5bd92813e1e7dcd`

Exactly **13** candidates were frozen before evidence research:

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

- Jan 1 2023 is Sunday; observed date Jan 2.
- Dec 31 2023 is Sunday; weekday guard excludes New Year's Eve candidate.
- Juneteenth is Monday Jun 19.

No 2023 date was pre-qualified in current `SPECIAL_SESSION_EVIDENCE`.

## 7. 2023 RESEARCH FINDINGS

The annual campaign searched exact dates, holiday names, `USATECH` / `USATECH.IDX/USD`, Dukascopy Bank / Europe news routes, multilingual variants, Trading Breaks routes and same-year CME evidence.

Important official Dukascopy material recovered:

- 2023 DST notice explicitly naming `USATECH.IDX/USD` for regular/summer schedule context;
- exact-date Juneteenth notice;
- exact-date/period Thanksgiving notice;
- exact-period Christmas/New-Year notice;
- generic New-Year transition context from end-2022 notice.

The holiday notices delegate detailed hours to the Trading Breaks Calendar and do not expose retrievable exact target-instrument holiday hours.

The Trading Breaks route was followed adversarially. The currently retrievable page/widget identifies the special-holiday schedule function but exposes no auditable historical `2023 + USATECH.IDX/USD + exact target-date hours` record.

This is absence of proof, not historical open/closed evidence.

No admissible exact/archived 2023 USATECH holiday witness was recovered for MLK, Presidents Day, Good Friday, Memorial Day, Independence pre-holiday/day or Labor Day.

Strong same-year CME material was recovered for several target dates, including Presidents Day, Memorial Day, Juneteenth, Labor Day, Thanksgiving and Christmas. It was not promoted into broker truth.

Even under strongest-favorable treatment granting exact verified exchange timing, PASS-C remains incomplete because no explicit Dukascopy target-instrument holiday witness + broker special-session mapping contract was recovered.

## 8. FINAL 2023 QUALIFICATION RESULT

Annual qualification report:

`reports/data-qualification/dukascopy_usatech_2023_calendar_qualification.md`

Completed qualification commit:

`295c8c2cfbddbd5bb31689e7623bdce4a8ab2aa0`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**

Every 2023 candidate remains:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2023 annual calendar coverage:

**BLOCKED — `2023_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 9. 2023 ANNUAL AUDIT

Audit report:

`reports/data-qualification/dukascopy_usatech_2023_calendar_audit.md`

Audit commit:

`48adbc3b2c21f271e879c6fec7563539e13d25da`

Audit verdict:

**PASS**

Reason:

`ALL_2023_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

Audit verified:

- 13/13 candidate completeness;
- frozen set preserved;
- exactly one verdict per date;
- no cross-year or adjacent-date substitution;
- no exchange-only promotion to broker truth;
- no generic broker holiday notice promoted to exact USATECH timing;
- Trading Breaks historical-route limitation kept as absence of proof;
- no hidden gaps;
- no executable record without date-level PASS;
- annual-audit PASS not confused with calendar-coverage PASS;
- no execution-window / acquisition bypass.

Critical distinction:

- `2023_ANNUAL_AUDIT = PASS`
- `2023_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

## 10. EXECUTABLE STATE

No 2023 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- no 2023 `SPECIAL_SESSION_EVIDENCE` record was added;
- no calendar test expectation changed;
- calendar tests were intentionally not rerun merely for timestamp freshness;
- latest observed calendar suite remains **34 PASS**;
- latest observed global `SPECIAL_SESSION_EVIDENCE` remains **24** records;
- latest observed global coverage remains **111 candidates / 24 resolved / 87 unresolved / BLOCKED**;
- no `.bi5` was downloaded;
- no execution window was frozen;
- no real backtest was started.

## 11. CLEANUP DEBT / DO NOT REPEAT

- accidental branch `__noop_should_not_exist__` MUST NOT be used;
- unavailable Wayback/archive routes or HTTP failures are not evidence of session behavior;
- do not rerun unchanged tests/audits only for freshness;
- do not reopen locked 2019/2020/2021/2022/2023 dates without materially new evidence;
- do not select an execution window to evade known gaps.

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Begin and complete the 2024 annual calendar qualification batch.**

Required sequence:

1. verify branch == this checkpoint final HEAD;
2. enumerate and freeze the complete 2024 candidate set from `candidate_special_dates()` before outcome research;
3. identify any already-qualified 2024 executable records and preserve them unless materially new contradictory evidence appears;
4. research all remaining 2024 candidates together;
5. apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently to every date;
6. assign exactly one PASS / FAIL / BLOCKED verdict per candidate;
7. modify executable calendar evidence only for admissible PASS dates;
8. rerun calendar tests/coverage only if executable evidence changes;
9. create/complete `reports/data-qualification/dukascopy_usatech_2024_calendar_qualification.md`;
10. create `reports/data-qualification/dukascopy_usatech_2024_calendar_audit.md`;
11. update backup + Recovery Checkpoint after the 2024 annual batch.

During this action, do NOT freeze an execution window, download massive `.bi5`, begin a real backtest, or infer broker truth from exchange-only / other-year / adjacent-date evidence.
