# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## 1. CURRENT STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Evidence-state HEAD before checkpoint persistence:** `e9b8aceba1e5690ea1ff9d71325afac1f3a769cd`
- **Durable session backup:** `99-BACKUP/SESSION-2026-09-13-MULTI-YEAR-DUKASCOPY-CALENDAR.md`
- **Backup commit:** `19ea4fe30d063baefe0336509558978f677ea7b9`
- **Active block:** complete special-session/calendar qualification for Dukascopy `USATECHIDXUSD` before multi-year native `.bi5` acquisition.
- **Coverage envelope:** `2018-05-01` → `2026-08-14`.
- **Execution/backtest window frozen:** no.

## 2. RECOVERY ORDER

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/README.md`
4. `99-BACKUP/SESSION-2026-09-13-MULTI-YEAR-DUKASCOPY-CALENDAR.md`
5. `tools/dukascopy_usatech_calendar.py`
6. `tools/dukascopy_usatech_calendar_coverage.py`
7. `tests/test_dukascopy_usatech_calendar.py`
8. actual GitHub/worktree state and current execution evidence

## 3. LOCKED UPSTREAM STATE — DO NOT REOPEN

- B02–B09 historical qualification remains locked; do not rerun merely to reconstruct history.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- 3.1.2 actual execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution environment exist.
- No partial/synthetic/fabricated backtest is authorized.

## 4. ACTIVE CALENDAR CONTRACTS

- `tools/dukascopy_usatech_calendar.py`
  - `DUKASCOPY_USATECH_SESSION_CALENDAR_V3`
  - evidence-state blob SHA `2b5a28c5d1eadbf651e784dbfcf5414f12ff7b8f`
- `tools/dukascopy_usatech_calendar_coverage.py`
  - `DUKASCOPY_USATECH_SPECIAL_SESSION_COVERAGE_V1`
  - blob SHA `dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`
- `tests/test_dukascopy_usatech_calendar.py`
  - blob SHA `826e6ece5d558d79b15642c91ac3b7a62b1136b5`
  - 22 tests versioned; do not claim 22/22 PASS without an observed current run.

## 5. LATEST OBSERVED COVERAGE VERDICT

Latest user-supplied execution:

- candidate dates: **111**
- resolved candidate dates: **12**
- special-session evidence dates: **12**
- no-special-change evidence dates: **0**
- unresolved candidate dates: **99**
- contradictory evidence dates: `[]`
- evidence shape errors: `[]`
- orphan special evidence: `[]`
- verdict: **BLOCKED**
- reason: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`

This is a clean BLOCKED, not FAIL.

## 6. RESOLVED DATES

All 2018 candidate dates inside the envelope are now resolved:

- 2018-05-28 Memorial Day
- 2018-07-03 Independence pre-holiday
- 2018-07-04 Independence Day
- 2018-09-03 Labor Day
- 2018-11-22 Thanksgiving Day
- 2018-11-23 Thanksgiving Friday
- 2018-12-05 GHWB National Day of Mourning
- 2018-12-24 Christmas Eve
- 2018-12-25 Christmas Day
- 2018-12-31 New Year's Eve

Other resolved dates:

- 2020-02-17 Presidents Day
- 2025-01-09 Carter National Day of Mourning

Therefore 2018 is complete and the first unresolved frontier is `2019-01-01`.

## 7. EVIDENCE DISCIPLINE

- Only complete UTC hourly BI5 buckets proven closed enter `fully_closed_hours_utc`.
- A partially tradable hour remains EXPECTED_OPEN.
- Holiday name alone is not closure evidence.
- HTTP 403/404/503 or missing BI5 data is not closure evidence.
- Do not extrapolate one year's special hours to another year.
- Dukascopy establishes broker special-event context; exact equity-index timing may be supplied by CME evidence when old Dukascopy pages no longer expose the detailed table.
- Preserved third-party copies of historical CME tables must remain explicitly labelled mirror evidence and must never be silently relabelled as primary-host CME evidence.

## 8. HISTORICAL WIDGET ROUTE — CLOSED

Do not restart the historical Trading Breaks widget path unless materially new evidence appears.

Reason:

- direct freeserv headless route returned 403;
- CDP/official-page route was built and hardened;
- one stale-frame false PASS showing Labor Day 2026 was detected and invalidated;
- strict exact-date frame for `2025-01-09` (`currentDate=false`, `date=1736424000000`) rendered empty (`dom_length=333`, visible text 0, table rows 0);
- repeated strict result remained BLOCKED.

The chosen path is now date-specific archived/primary evidence, not widget recovery.

## 9. MULTI-YEAR ACQUISITION GATE

Massive acquisition is still forbidden.

Before acquisition:

1. calendar coverage must reach zero unresolved candidate dates;
2. verdict must be PASS;
3. then freeze the exact >=5-year execution window;
4. only then download native Dukascopy `.bi5` real ticks with manifest/hash/reconciliation;
5. no OHLC M1, interpolation, synthetic or substituted ticks.

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Consolidate date-specific evidence for the 13 unresolved 2019 candidate sessions, commit only dates that actually meet the same evidence threshold used for 2018, then rerun `tests/test_dukascopy_usatech_calendar.py` and `tools/dukascopy_usatech_calendar_coverage.py`.**

The objective is to reduce `unresolved_candidate_dates` below 99 without any false PASS. Do not begin massive acquisition before coverage reaches PASS with zero unresolved dates.
