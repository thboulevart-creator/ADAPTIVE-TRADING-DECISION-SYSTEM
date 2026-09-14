# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — 2021 ANNUAL DUKASCOPY CALENDAR QUALIFICATION COMPLETE

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Previous checkpoint / session start HEAD:** `f4938f2823412aef3df65d6fd30408f2036d2b88`
- **2021 durable backup:** `99-BACKUP/SESSION-2026-09-14-2021-CALENDAR.md`
  - commit `918cb4ad97331b8a2644e82821883444bbce1e2d`
- **2021 annual qualification:** `reports/data-qualification/dukascopy_usatech_2021_calendar_qualification.md`
  - candidate freeze commit `d8083da25951d1f506179c39bfba1691ef53c60c`
  - completed qualification commit `2f6531a72e85a91382564305193d67985fe544ac`
- **2021 annual audit:** `reports/data-qualification/dukascopy_usatech_2021_calendar_audit.md`
  - commit `43a080f7456c9a557527e1f9b8cff9eec27bff74`
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
3. `99-BACKUP/SESSION-2026-09-14-2021-CALENDAR.md`
4. `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2021_calendar_qualification.md`
8. `reports/data-qualification/dukascopy_usatech_2021_calendar_audit.md`
9. compare the active branch against this checkpoint's final HEAD before writing anything.

Do not reconstruct 2019, 2020 or 2021 from conversation history.

## 3. LOCKED OPERATING METHOD

Calendar qualification follows:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

Permanent rule:

- **research batch = one complete calendar year**;
- **evidence verdict = one candidate date**;
- **audit = one complete calendar year**.

Annual batching is only an efficiency mechanism. It MUST NOT weaken date-specific proof or allow cross-date / cross-year inference.

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

It remains the first global unresolved candidate.

### 2020

Complete candidate set: **13**.

Final matrix:

- PASS: **1**
- FAIL: **0**
- BLOCKED: **12**

Sole PASS:

- `2020-02-17 — PRESIDENTS_DAY`

2020 annual audit:

**PASS — `ALL_2020_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`**

2020 calendar coverage:

**BLOCKED — `2020_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

The transient false-PASS route for `2020-01-01` was adversarially broken and fully revoked. Never resurrect `generic broker context + exact exchange timing + same holiday event = PASS`.

## 6. 2021 CANDIDATE SET — FROZEN BEFORE OUTCOME RESEARCH

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Freeze commit:

`d8083da25951d1f506179c39bfba1691ef53c60c`

Exactly **13** candidates were frozen before evidence research:

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

No Juneteenth candidate exists for 2021 under the versioned generator; Juneteenth begins in 2022.

No 2021 date was pre-qualified in current `SPECIAL_SESSION_EVIDENCE`.

## 7. 2021 RESEARCH FINDINGS

The annual campaign searched exact dates, holiday names, `USATECH` / `USATECH.IDX/USD`, Dukascopy Bank / Dukascopy Europe company-news routes, multilingual variants and exact-year formulations.

Exact-date/period official Dukascopy context recovered included:

- New Year 2021 period via the 2020 Christmas/New-Year notice;
- `2021-02-15 — Presidents Day` official notice;
- `2021-04-02 — Good Friday` official Easter notice;
- `2021-05-31 — Memorial Day` official notice;
- end-2021 Christmas/New-Year official notice.

These notices establish exact-date/period broker context but, in retrievable text, do not provide the full target-instrument exact-hours witness or explicit special-session mapping chain required for PASS.

No qualifying exact/archived 2021 Dukascopy USATECH witness was recovered for MLK, Independence pre-holiday/observed, Labor Day or Thanksgiving Thursday/Friday.

Exact same-year external CME/Nasdaq/reference evidence exists for several dates but was not promoted into broker truth.

Under the strongest-favorable adversarial check, granting exact verified exchange timing still does not complete PASS-C because the required Dukascopy target-instrument + mapping chain remains absent.

## 8. FINAL 2021 QUALIFICATION RESULT

Annual qualification report:

`reports/data-qualification/dukascopy_usatech_2021_calendar_qualification.md`

Completed qualification commit:

`2f6531a72e85a91382564305193d67985fe544ac`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**

Every 2021 candidate remains:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2021 annual calendar coverage:

**BLOCKED — `2021_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 9. 2021 ANNUAL AUDIT

Audit report:

`reports/data-qualification/dukascopy_usatech_2021_calendar_audit.md`

Audit commit:

`43a080f7456c9a557527e1f9b8cff9eec27bff74`

Audit verdict:

**PASS**

Reason:

`ALL_2021_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

The audit verified:

- 13/13 candidate completeness;
- frozen candidate set preserved;
- exactly one verdict per date;
- no cross-year or adjacent-date substitution;
- no exchange-only promotion to broker truth;
- no generic broker notice promoted to exact USATECH timing;
- no hidden gaps;
- no executable record without date-level PASS;
- annual-audit PASS not confused with calendar-coverage PASS;
- no execution-window / acquisition bypass.

Critical distinction:

- `2021_ANNUAL_AUDIT = PASS`
- `2021_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

## 10. EXECUTABLE STATE

No 2021 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- no 2021 `SPECIAL_SESSION_EVIDENCE` record was added;
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
- do not reopen locked 2019/2020/2021 dates without materially new evidence;
- do not select an execution window to evade known gaps.

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Begin and complete the 2022 annual calendar qualification batch.**

Required sequence:

1. verify branch == this checkpoint final HEAD;
2. enumerate and freeze the complete 2022 candidate set from `candidate_special_dates()` before outcome research;
3. note that 2022 is the first generator year including `JUNETEENTH_OBSERVED`;
4. identify any already-qualified 2022 executable records and preserve them unless materially new contradictory evidence appears;
5. research all remaining 2022 candidates together;
6. apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently to every date;
7. assign exactly one PASS / FAIL / BLOCKED verdict per candidate;
8. modify executable calendar evidence only for admissible PASS dates;
9. rerun calendar tests/coverage only if executable evidence changes;
10. create/complete `reports/data-qualification/dukascopy_usatech_2022_calendar_qualification.md`;
11. create `reports/data-qualification/dukascopy_usatech_2022_calendar_audit.md`;
12. update backup + Recovery Checkpoint after the 2022 annual batch.

During this action, do NOT freeze an execution window, download massive `.bi5`, begin a real backtest, or infer broker truth from exchange-only / other-year / adjacent-date evidence.
