# SESSION BACKUP — 2026-09-13 — 2020 ANNUAL CALENDAR QUALIFICATION

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting checkpoint for annual batching transition: `501fed85bc8e41d3bf499c7270821e5c63778b2c`
- Global coverage envelope: `2018-05-01` through `2026-08-14`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Historical-gap rule: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- Annual protocol: `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

## Operating-method change

The calendar workstream no longer advances through one-date-per-session checkpoints.

From this point forward:

- **research batch = one full calendar year**;
- **evidence verdict = one candidate date**;
- **audit = one calendar year**.

The efficiency gain does not weaken any date-specific evidence rule.

Protocol artifact:

`04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`

Protocol commit:

`4dec1dcd83259f219c2f6e1aadb0a2216a7315af`

## 2020 candidate set

`candidate_special_dates()` produces exactly 13 candidates for 2020:

1. `2020-01-01` NEW_YEARS_OBSERVED
2. `2020-01-20` MARTIN_LUTHER_KING_DAY
3. `2020-02-17` PRESIDENTS_DAY
4. `2020-04-10` GOOD_FRIDAY
5. `2020-05-25` MEMORIAL_DAY
6. `2020-07-02` INDEPENDENCE_PRE_HOLIDAY_SESSION
7. `2020-07-03` INDEPENDENCE_DAY_OBSERVED
8. `2020-09-07` LABOR_DAY
9. `2020-11-26` THANKSGIVING_DAY
10. `2020-11-27` THANKSGIVING_FRIDAY
11. `2020-12-24` CHRISTMAS_PRE_HOLIDAY_SESSION
12. `2020-12-25` CHRISTMAS_OBSERVED
13. `2020-12-31` NEW_YEARS_EVE_CANDIDATE

## Annual qualification result

Durable annual report:

`reports/data-qualification/dukascopy_usatech_2020_calendar_qualification.md`

Commit:

`04a51fb509d73ed3ed3748fff539d78e9e54cc95`

Final 2020 matrix:

- PASS: **1**
- FAIL: **0**
- BLOCKED: **12**
- total: **13**

### PASS

- `2020-02-17 — PRESIDENTS_DAY`
  - remains the existing locked `SPECIAL_PRESIDENTS_DAY_2020` record with exact Dukascopy evidence.

### BLOCKED

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

All BLOCKED dates remain `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` outcomes or equivalent unresolved broker-proof states under the same gate.

## Remaining-date annual research campaign

The eight previously unprocessed 2020 dates were researched together.

Strong exchange/reference evidence was recovered across the annual set, including:

- official CME Independence-Day 2020 settlement schedule;
- preserved CME Globex Independence-Day 2020 summary;
- preserved CME Globex Labor-Day 2020 summary;
- official CME Thanksgiving 2020 settlement schedule;
- official CME Christmas 2020 advisory;
- preserved CME Globex Christmas 2020 summary;
- preserved CME Globex New-Year 2020/2021 summary.

Dukascopy-specific 2020 context recovered included:

- `Change to Daylight Saving Time 2020`, explicitly naming `USATECH.IDX/USD` for regular summer-schedule context;
- `Market closures on Christmas and New Year 2020`, which confirms generic CFD holiday closures but delegates exact details to the Trading Breaks Calendar;
- `Weekend leverage at Christmas and New Year`, which proves leverage changes on Dec 24/31 but not USATECH session hours.

No new exact/archived 2020 Dukascopy witness explicitly naming `USATECH.IDX/USD` with target holiday hours was recovered for the eight remaining candidates.

Other-year Dukascopy USATECH holiday schedules remain corroborative-only.

## Annual audit

Durable audit report:

`reports/data-qualification/dukascopy_usatech_2020_calendar_audit.md`

Commit:

`a5495e234d45263d98c9b15c6d004bf24b62537d`

Audit verdict:

**PASS**

Reason:

`ALL_2020_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

The audit verified:

- exact candidate-set completeness: 13/13;
- one allowed verdict per date;
- locked prior verdict preservation;
- no cross-date inference;
- no cross-year substitution;
- no exchange-only promotion to broker truth;
- no generic holiday notice promoted to exact USATECH hours;
- no executable calendar record created without date-level PASS;
- no annual-audit PASS misrepresented as calendar-coverage PASS.

## Critical distinction

These statements are simultaneously true:

- `2020_ANNUAL_AUDIT`: **PASS**
- `2020_CALENDAR_COVERAGE`: **BLOCKED**
- `GLOBAL_2018_2026_COVERAGE`: **BLOCKED**
- `EXECUTION_WINDOW_FREEZE`: **BLOCKED**
- `MASSIVE_BI5_ACQUISITION`: **BLOCKED**

Annual audit PASS certifies process completeness and evidence discipline, not broker-session coverage completeness.

## Executable state

No new 2020 date earned PASS during the annual batch.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- calendar tests remain unchanged;
- the latest observed executable calendar state remains **34 tests PASS**;
- global coverage remains **111 candidates / 24 resolved / 87 unresolved / BLOCKED**;
- no rerun was performed merely to create a newer timestamp.

## Historical gaps preserved

`2019-07-03` remains explicitly BLOCKED and was not reopened.

All 2020 BLOCKED dates remain visible and must not be silently removed from future coverage reasoning.

## Auxiliary branch incident

The accidental branch `__noop_should_not_exist__` remains a tooling cleanup debt and MUST NOT be used. Delete it only when a supported branch-deletion route is available.

## Exactly one next governed action

**Begin the 2021 annual calendar qualification batch: enumerate and freeze the complete 2021 candidate set from `candidate_special_dates()`, preserve all 2020 verdicts as locked historical state, research all 2021 candidates as a batch, apply independent date-level PASS/FAIL/BLOCKED verdicts, then finish with a 2021 annual audit. Do not freeze an execution window and do not download `.bi5`.**
