# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — 2022 ANNUAL DUKASCOPY CALENDAR QUALIFICATION COMPLETE

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Previous checkpoint / session start HEAD:** `93896f7476ae27991b646b4ba2aa15c1f0aa79d9`
- **2022 durable backup:** `99-BACKUP/SESSION-2026-09-14-2022-CALENDAR.md`
  - commit `82c4203d57555df95c38299d0fee326337b20513`
- **2022 annual qualification:** `reports/data-qualification/dukascopy_usatech_2022_calendar_qualification.md`
  - candidate freeze commit `81a505df146c3bc09f5b68dec5dbef39e4e5caaf`
  - completed qualification commit `4e2eeec5b37a679b6f8a9f9e0fa064b038d40e81`
- **2022 annual audit:** `reports/data-qualification/dukascopy_usatech_2022_calendar_audit.md`
  - commit `b4b20a77dde86b2481d896d7ae5076451b4f6c13`
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
3. `99-BACKUP/SESSION-2026-09-14-2022-CALENDAR.md`
4. `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2022_calendar_qualification.md`
8. `reports/data-qualification/dukascopy_usatech_2022_calendar_audit.md`
9. compare active branch against this checkpoint final HEAD before writing anything.

Do not reconstruct 2019, 2020, 2021 or 2022 from conversation history.

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

Still the first global unresolved candidate.

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

### 2021

Complete candidate set: **13**.

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**

2021 annual audit:

**PASS — `ALL_2021_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`**

2021 calendar coverage:

**BLOCKED — `2021_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 6. 2022 CANDIDATE SET — FROZEN BEFORE OUTCOME RESEARCH

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Freeze commit:

`81a505df146c3bc09f5b68dec5dbef39e4e5caaf`

Exactly **12** candidates were frozen before evidence research:

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

- Jan 1 2022 is Saturday; observed date `2021-12-31` is outside bounded 2022 batch.
- Dec 31 2022 is Saturday, so weekday guard excludes New Year's Eve candidate.
- Juneteenth first appears in current generator in 2022, observed Monday `2022-06-20`.

No 2022 date was pre-qualified in current `SPECIAL_SESSION_EVIDENCE`.

## 7. 2022 RESEARCH FINDINGS

The annual campaign searched exact dates, holiday names, `USATECH` / `USATECH.IDX/USD`, Dukascopy Bank / Dukascopy Europe news routes, multilingual variants, exact-year formulations, CME 2022 holiday material and the linked Dukascopy Trading Breaks route.

Exact-date/period official Dukascopy context recovered included:

- `2022-01-17 — MLK`: exact broker special-break notice;
- `2022-05-30 — Memorial Day`: exact broker special-break notice;
- `2022-06-20 — Juneteenth`: exact broker event and first Juneteenth candidate;
- `2022-07-04 — Independence Day`: exact broker special-break notice;
- `2022-12-23 / 2022-12-26 — Christmas period`: exact-period broker notice.

The retrievable text for these notices delegates detailed schedules to Dukascopy's Trading Breaks Calendar and does not itself provide the required explicit `USATECH.IDX/USD` exact-hours witness.

The linked Trading Breaks Calendar was followed adversarially. The currently retrievable page identifies itself as the special-holiday schedule but does not expose a retrievable historical 2022 `USATECH.IDX/USD` row or exact-hours witness.

This remains absence of proof, not evidence of historical open/closed behavior.

No admissible exact/archived target-instrument witness was recovered for Presidents Day, Good Friday, July 1 pre-holiday, Labor Day, Thanksgiving Thursday or Thanksgiving Friday.

Official CME same-year evidence provides strong holiday/reference context for the 2022 calendar, including Juneteenth, Independence, Thanksgiving and Christmas. It was never promoted into broker truth.

Under strongest-favorable gate application, even granting exact verified exchange timing cannot complete PASS-C without explicit Dukascopy target instrument + special-session mapping chain.

## 8. FINAL 2022 QUALIFICATION RESULT

Annual qualification report:

`reports/data-qualification/dukascopy_usatech_2022_calendar_qualification.md`

Completed qualification commit:

`4e2eeec5b37a679b6f8a9f9e0fa064b038d40e81`

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **12**

Every 2022 candidate remains:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

2022 annual calendar coverage:

**BLOCKED — `2022_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 9. 2022 ANNUAL AUDIT

Audit report:

`reports/data-qualification/dukascopy_usatech_2022_calendar_audit.md`

Audit commit:

`b4b20a77dde86b2481d896d7ae5076451b4f6c13`

Audit verdict:

**PASS**

Reason:

`ALL_2022_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

The audit verified:

- 12/12 candidate completeness;
- frozen candidate set preserved;
- exactly one verdict per date;
- no cross-year or adjacent-date substitution;
- no exchange-only promotion to broker truth;
- no generic broker notice promoted to exact USATECH timing;
- Trading Breaks historical-route limitation kept as absence of proof;
- no hidden gaps;
- no executable record without date-level PASS;
- annual-audit PASS not confused with calendar-coverage PASS;
- no execution-window / acquisition bypass.

Critical distinction:

- `2022_ANNUAL_AUDIT = PASS`
- `2022_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

## 10. EXECUTABLE STATE

No 2022 candidate earned PASS.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- no 2022 `SPECIAL_SESSION_EVIDENCE` record was added;
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
- do not reopen locked 2019/2020/2021/2022 dates without materially new evidence;
- do not select an execution window to evade known gaps.

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Begin and complete the 2023 annual calendar qualification batch.**

Required sequence:

1. verify branch == this checkpoint final HEAD;
2. enumerate and freeze the complete 2023 candidate set from `candidate_special_dates()` before outcome research;
3. identify any already-qualified 2023 executable records and preserve them unless materially new contradictory evidence appears;
4. research all remaining 2023 candidates together;
5. apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently to every date;
6. assign exactly one PASS / FAIL / BLOCKED verdict per candidate;
7. modify executable calendar evidence only for admissible PASS dates;
8. rerun calendar tests/coverage only if executable evidence changes;
9. create/complete `reports/data-qualification/dukascopy_usatech_2023_calendar_qualification.md`;
10. create `reports/data-qualification/dukascopy_usatech_2023_calendar_audit.md`;
11. update backup + Recovery Checkpoint after the 2023 annual batch.

During this action, do NOT freeze an execution window, download massive `.bi5`, begin a real backtest, or infer broker truth from exchange-only / other-year / adjacent-date evidence.
