# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — 2024 ANNUAL DUKASCOPY CALENDAR QUALIFICATION COMPLETE

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Previous checkpoint / 2024 session start HEAD:** `b8e86286fd4057a9a1445d1943732d81ba4a2f63`
- **2024 durable backup:** `99-BACKUP/SESSION-2026-09-14-2024-CALENDAR.md`
  - commit `085a0e470a382fe47c9499eecc725ce5cebddf08`
- **2024 annual qualification:** `reports/data-qualification/dukascopy_usatech_2024_calendar_qualification.md`
  - candidate freeze commit `811976c584a0626e06d1012e9f90c9f9619c4ca2`
  - completed qualification commit `343e179254291192843c070ff2832d71eaded04b`
- **2024 annual audit:** `reports/data-qualification/dukascopy_usatech_2024_calendar_audit.md`
  - commit `5392feec278e5edeec85cca5420ccd96737f9c1f`
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
3. `99-BACKUP/SESSION-2026-09-14-2024-CALENDAR.md`
4. `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2024_calendar_qualification.md`
8. `reports/data-qualification/dukascopy_usatech_2024_calendar_audit.md`
9. compare active branch against this checkpoint final HEAD before writing anything.

Do not reconstruct 2019–2024 from conversation history.

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

### 2023

- candidates: **13**
- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**
- annual audit: **PASS**
- calendar coverage: **BLOCKED**

## 6. 2024 CANDIDATE SET — FROZEN BEFORE OUTCOME RESEARCH

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Freeze commit:

`811976c584a0626e06d1012e9f90c9f9619c4ca2`

Exactly **14** candidates were frozen before evidence research:

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

No 2024 date was pre-qualified in current `SPECIAL_SESSION_EVIDENCE`.

## 7. 2024 RESEARCH FINDINGS

The annual campaign searched exact dates, holiday names, `USATECH` / `USATECH.IDX/USD`, Dukascopy Bank / Europe news routes, multilingual variants, Trading Breaks routes and same-year CME evidence.

Important official Dukascopy material recovered:

- 2024 DST notice explicitly naming `USATECH.IDX/USD` for regular/summer schedule context;
- exact-date MLK notice;
- exact-period Easter / Good Friday notice;
- exact-date Memorial Day notice;
- exact-date Juneteenth notice;
- exact-date Labor Day notice;
- exact-date/period Thanksgiving notice;
- exact-period Christmas/New-Year notice.

The holiday notices delegate detailed hours to the Trading Breaks Calendar and do not expose retrievable exact target-instrument holiday hours.

No admissible exact 2024 target-instrument holiday witness was recovered for Presidents Day or the Independence pre-holiday/day pair.

The Trading Breaks route was followed adversarially. The current page/widget identifies the holiday-special schedule function but exposes no auditable historical `2024 + USATECH.IDX/USD + exact target-date hours` record.

This is absence of proof, not historical open/closed evidence.

### Important false-lead correction

A Dukascopy Europe `General Features` page was found with a rule stating an instrument is non-tradable during specified windows on U.S. national holidays.

Inspection of the actual table proved the footnote applies only to:

- `XAU/USD`
- `XAG/USD`

It does **not** apply to `USATECH.IDX/USD`.

Therefore this rule cannot serve as the missing broker special-session mapping contract for USATECH and cannot complete PASS-C.

This anti-false-PASS finding must be preserved.

Strong same-year official CME material was recovered for the 2024 holiday calendar and multiple target dates, including Independence, Labor Day, Thanksgiving and Christmas.

The exchange side was given the strongest favorable treatment where appropriate, but it was never promoted into broker truth. PASS-C still fails without explicit Dukascopy USATECH holiday mapping evidence.

## 8. FINAL 2024 QUALIFICATION RESULT

Annual qualification report:

`reports/data-qualification/dukascopy_usatech_2024_calendar_qualification.md`

Completed qualification commit:

`343e179254291192843c070ff2832d71eaded04b`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **14**

Every 2024 candidate remains:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2024 annual calendar coverage:

**BLOCKED — `2024_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 9. 2024 ANNUAL AUDIT

Audit report:

`reports/data-qualification/dukascopy_usatech_2024_calendar_audit.md`

Audit commit:

`5392feec278e5edeec85cca5420ccd96737f9c1f`

Audit verdict:

**PASS**

Reason:

`ALL_2024_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

Audit verified:

- 14/14 candidate completeness;
- frozen set preserved;
- exactly one verdict per date;
- no cross-year or adjacent-date substitution;
- no exchange-only promotion to broker truth;
- no generic broker holiday notice promoted to exact USATECH timing;
- metal-only U.S.-holiday footnote correctly rejected for USATECH;
- Trading Breaks historical-route limitation kept as absence of proof;
- no hidden gaps;
- no executable record without date-level PASS;
- annual-audit PASS not confused with calendar-coverage PASS;
- no execution-window / acquisition bypass.

Critical distinction:

- `2024_ANNUAL_AUDIT = PASS`
- `2024_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

## 10. EXECUTABLE STATE

No 2024 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- no 2024 `SPECIAL_SESSION_EVIDENCE` record was added;
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
- do not reopen locked 2019/2020/2021/2022/2023/2024 dates without materially new evidence;
- do not select an execution window to evade known gaps;
- do not apply the metal-only U.S.-national-holiday footnote to USATECH.

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Begin and complete the 2025 annual calendar qualification batch.**

Required sequence:

1. verify branch == this checkpoint final HEAD;
2. enumerate and freeze the complete 2025 candidate set from `candidate_special_dates()` before outcome research;
3. identify already-qualified 2025 executable records, especially the existing `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025` record, and preserve them unless materially new contradictory evidence appears;
4. research all remaining 2025 candidates together;
5. apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently to every date;
6. assign exactly one PASS / FAIL / BLOCKED verdict per candidate;
7. modify executable calendar evidence only for admissible PASS dates;
8. rerun calendar tests/coverage only if executable evidence changes;
9. create/complete `reports/data-qualification/dukascopy_usatech_2025_calendar_qualification.md`;
10. create `reports/data-qualification/dukascopy_usatech_2025_calendar_audit.md`;
11. update backup + Recovery Checkpoint after the 2025 annual batch.

During this action, do NOT freeze an execution window, download massive `.bi5`, begin a real backtest, or infer broker truth from exchange-only / other-year / adjacent-date evidence.
