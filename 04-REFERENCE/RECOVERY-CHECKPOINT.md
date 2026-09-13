# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — ANNUAL DUKASCOPY CALENDAR QUALIFICATION

## 1. CURRENT STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Prior checkpoint:** `501fed85bc8e41d3bf499c7270821e5c63778b2c`
- **Latest durable backup:** `99-BACKUP/SESSION-2026-09-13-2020-CALENDAR.md`
  - latest update commit `34a578afbde70ffbdd51bbf9aa6a012437171c1f`
- **Annual protocol:** `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
  - commit `4dec1dcd83259f219c2f6e1aadb0a2216a7315af`
- **2020 annual qualification:** `reports/data-qualification/dukascopy_usatech_2020_calendar_qualification.md`
  - commit `04a51fb509d73ed3ed3748fff539d78e9e54cc95`
- **2020 annual audit:** `reports/data-qualification/dukascopy_usatech_2020_calendar_audit.md`
  - commit `a5495e234d45263d98c9b15c6d004bf24b62537d`
- **Coverage envelope:** `2018-05-01` → `2026-08-14`
- **Execution/backtest window frozen:** no
- **Massive native `.bi5` acquisition:** forbidden
- **Global coverage verdict:** BLOCKED
- **Global unresolved candidates:** 87
- **First global unresolved:** `2019-07-03`

## 2. RECOVERY ORDER

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/README.md`
4. `99-BACKUP/SESSION-2026-09-13-2020-CALENDAR.md`
5. `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
6. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
7. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
8. `reports/data-qualification/dukascopy_usatech_2020_calendar_qualification.md`
9. `reports/data-qualification/dukascopy_usatech_2020_calendar_audit.md`
10. prior date-specific 2020 reports when forensic detail is needed
11. `tools/dukascopy_usatech_calendar.py`
12. `tools/dukascopy_usatech_calendar_coverage.py`
13. calendar/governance tests and actual GitHub state

## 3. NEW LOCKED OPERATING METHOD

Contract:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

From this checkpoint forward:

- **research batch = one full calendar year**;
- **evidence verdict = one candidate date**;
- **audit = one calendar year**.

Annual batching is only an efficiency improvement. It MUST NOT weaken the date-specific evidence threshold.

Every candidate date remains independent. No adjacent holiday date, same-year pattern, or other-year schedule may supply another date's broker verdict.

The annual audit is distinct from annual calendar coverage:

- annual audit PASS = complete accounting + evidence discipline;
- annual calendar coverage PASS = every candidate resolved with admissible evidence and no FAIL.

## 4. GOVERNANCE RULES — LOCKED

### `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Rule verdict: **PASS**.

Only three PASS routes exist:

- PASS-A exact primary broker witness;
- PASS-B exact archived broker witness with verified provenance;
- PASS-C exact-date broker event explicitly covering target instrument + official broker special-session mapping contract + exact same-date verified exchange/reference timing.

Exchange-only timing, generic broker holiday context, cross-year analogy, missing data, HTTP failures, or majority-of-sources reasoning do not create PASS.

### `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Rule verdict: **PASS**.

Current permission matrix:

- continue later annual qualification: **PASS**;
- declare global coverage PASS: **BLOCKED**;
- freeze execution window: **BLOCKED**;
- authorize massive acquisition: **BLOCKED**.

## 5. 2020 ANNUAL RESULT

Complete 2020 candidate set: **13**.

Final date-level verdicts:

- PASS: **1**
- FAIL: **0**
- BLOCKED: **12**

The sole PASS remains:

- `2020-02-17 — PRESIDENTS_DAY` → existing locked `SPECIAL_PRESIDENTS_DAY_2020` exact Dukascopy evidence.

BLOCKED dates:

- `2020-01-01`
- `2020-01-20`
- `2020-04-10`
- `2020-05-25`
- `2020-07-02`
- `2020-07-03`
- `2020-09-07`
- `2020-11-26`
- `2020-11-27`
- `2020-12-24`
- `2020-12-25`
- `2020-12-31`

2020 annual calendar coverage verdict:

**BLOCKED — `2020_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

## 6. 2020 ANNUAL AUDIT

Audit verdict:

**PASS**

Reason:

`ALL_2020_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

The audit verified:

- 13/13 candidate completeness;
- one explicit PASS/FAIL/BLOCKED verdict per date;
- preservation of earlier locked verdicts;
- no cross-date inference;
- no cross-year substitution;
- no exchange-only promotion to broker truth;
- no generic holiday notice promoted to exact USATECH hours;
- no executable calendar record without a date-level PASS;
- annual audit PASS not misrepresented as calendar coverage PASS.

## 7. 2020 RESEARCH FINDINGS

The annual batch recovered strong exact exchange/reference material for the remaining dates, including CME/Globex Independence Day, Labor Day, Thanksgiving, Christmas and New-Year schedules.

Dukascopy 2020 material recovered included:

- `Change to Daylight Saving Time 2020` explicitly naming `USATECH.IDX/USD` for regular summer-schedule context;
- `Market closures on Christmas and New Year 2020`, confirming generic CFD holiday closures but delegating exact hours to the Trading Breaks Calendar;
- `Weekend leverage at Christmas and New Year`, establishing leverage changes on Dec 24/31 but not exact USATECH session hours.

No new exact/archived 2020 Dukascopy witness explicitly naming `USATECH.IDX/USD` with target holiday hours was recovered for the eight previously unprocessed candidates.

## 8. EXECUTABLE CALENDAR STATE

No new 2020 date earned PASS during the annual batch.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- calendar tests remain unchanged;
- latest observed executable calendar state remains **34 tests PASS**;
- current calendar still contains **24** special-session evidence records globally;
- global coverage remains **111 candidates / 24 resolved / 87 unresolved / BLOCKED**;
- no test rerun was performed merely to create a newer timestamp.

## 9. HISTORICAL GAPS PRESERVED

`2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION` remains explicitly BLOCKED.

All 2020 BLOCKED dates remain visible and must remain part of global-envelope truth.

No gap was hidden, deleted, or reclassified merely to enable annual progression.

## 10. LOCKED UPSTREAM STATE — DO NOT REOPEN

- B02–B09 historical qualification remains locked.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- 3.1.2 actual execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution environment exist.
- No partial/synthetic/fabricated backtest is authorized.
- No OHLC M1, interpolation, synthetic ticks, or substituted ticks are authorized.

## 11. AUXILIARY BRANCH INCIDENT

The accidental branch `__noop_should_not_exist__` remains a tooling cleanup debt. It is not an authorized work branch and MUST NOT be used. Delete it only when a supported branch-deletion route is available.

## 12. ACQUISITION / WINDOW STATE

- Global coverage remains BLOCKED.
- Execution window remains undefined and unfrozen.
- No window may be selected merely to evade historical gaps.
- Massive native `.bi5` acquisition remains forbidden.
- No `.bi5` was downloaded during the 2020 annual batch.

## 13. EXACTLY ONE NEXT GOVERNED ACTION

**Begin the 2021 annual calendar qualification batch: enumerate and freeze the complete 2021 candidate set from `candidate_special_dates()`, preserve every 2020 verdict as locked historical state, research all 2021 candidates together, assign independent date-level PASS/FAIL/BLOCKED verdicts, then perform the 2021 annual audit. Do not freeze an execution window and do not download `.bi5`.**
