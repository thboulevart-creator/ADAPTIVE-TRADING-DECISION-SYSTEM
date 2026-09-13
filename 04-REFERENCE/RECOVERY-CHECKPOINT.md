# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## 1. CURRENT STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Prior checkpoint:** `25545ced686e06188c2e860d9355da478889ab82`
- **Late-2019 calendar evidence commit:** `6dbe69cc3a4d7a1fe023e7274945bfe147b6aeeb`
- **Late-2019 supplementary-test commit:** `82ede6465f9fa006cc49868b663d0fd67c9824fc`
- **Durable session backup commit:** `4970041870c7c252f3fddc3ef2db16cb6b59aeb8`
- **Durable session backup:** `99-BACKUP/SESSION-2026-09-13-MULTI-YEAR-DUKASCOPY-CALENDAR.md`
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
8. `tests/test_dukascopy_usatech_calendar_2019_remaining.py`
9. actual GitHub/worktree state and current execution evidence

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
  - now contains **24** date-specific special-session evidence records inside the coverage envelope.
- `tools/dukascopy_usatech_calendar_coverage.py`
  - `DUKASCOPY_USATECH_SPECIAL_SESSION_COVERAGE_V1`
- `tests/test_dukascopy_usatech_calendar.py`
  - **28** historical/current calendar tests.
- `tests/test_dukascopy_usatech_calendar_2019_remaining.py`
  - **6** targeted tests for the newly-qualified late-2019 sessions.

## 5. LATEST OBSERVED TEST EXECUTION

The pre-existing 28-test suite was rerun after the new evidence was versioned:

```text
............................                                             [100%]
28 passed in 0.04s
```

The six new targeted tests were also executed:

```text
......                                                                   [100%]
6 passed in 0.02s
```

Combined observed execution: **34 passed in 0.04s**.

Execution caveat: the container has no direct network route to GitHub. GitHub state/writes/blob verification were handled through the GitHub connector; Python execution used a local materialisation of the versioned calendar classification/evidence logic and tests. This is not a GitHub Actions run or network checkout.

## 6. LATEST OBSERVED COVERAGE VERDICT

- `candidate_dates`: **111**
- `resolved_candidate_dates`: **24**
- `special_session_evidence_dates`: **24**
- `no_special_change_evidence_dates`: **0**
- `unresolved_candidate_dates`: **87**
- `contradictory_evidence_dates`: `[]`
- `evidence_shape_errors`: `[]`
- `orphan_special_evidence`: `[]`
- `verdict`: **BLOCKED**
- `reason`: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`
- coverage script exit code: `2`

This is a clean BLOCKED, not FAIL.

## 7. 2019 RESOLUTION STATE

Resolved 2019 candidate dates now include:

- `2019-01-01` New Year's Day
- `2019-01-21` Martin Luther King Jr. Day
- `2019-02-18` Presidents Day
- `2019-04-19` Good Friday
- `2019-05-27` Memorial Day
- `2019-07-04` Independence Day
- `2019-09-02` Labor Day
- `2019-11-28` Thanksgiving Day
- `2019-11-29` Thanksgiving Friday
- `2019-12-24` Christmas Eve
- `2019-12-25` Christmas Day
- `2019-12-31` New Year's Eve

The **only unresolved 2019 candidate** is now:

- `2019-07-03` — `INDEPENDENCE_PRE_HOLIDAY_SESSION`

The first unresolved coverage date is therefore still `2019-07-03`.

## 8. WHY 2019-07-03 IS STILL BLOCKED

Exact 2019 CME-derived evidence shows ES/NQ/YM closing early at 12:15 Chicago time on Wednesday 3 July 2019, which would imply a partial 17 UTC hour and fully closed `18-21 UTC` exchange buckets.

However, the broker-specific side of the proof is missing:

- the recovered Dukascopy 2019 Independence announcement explicitly identifies special CFD breaks on **4 July 2019**;
- no date-specific Dukascopy/USATECH witness was found for a 3 July early close;
- targeted searches for `USATECH.IDX/USD`, `3 July 2019`, `17:15`, and historical Dukascopy Trading Breaks produced no qualifying witness;
- the exact 2018 Dukascopy July-3 schedule is not extrapolated into 2019.

Therefore CME-only evidence is insufficient under the current threshold. No special record was created for `2019-07-03`.

## 9. EVIDENCE DISCIPLINE

- Only complete UTC hourly BI5 buckets proven closed enter `fully_closed_hours_utc`.
- A partially tradable hour remains EXPECTED_OPEN.
- Holiday name alone is not closure evidence.
- HTTP 403/404/503 or missing BI5 data is not closure evidence.
- Do not extrapolate one year's special hours to another year.
- Dukascopy establishes broker special-event context; precise equity-index timing may be supplied by CME evidence when necessary.
- Preserved third-party historical CME schedules remain explicitly labelled mirror evidence.
- Exchange-only evidence does not silently become Dukascopy broker truth where broker treatment is materially uncertain.

## 10. HISTORICAL WIDGET ROUTE — CLOSED

Do not restart the historical Trading Breaks widget path unless materially new evidence appears.

The prior route reached the exact historical frame but returned an empty DOM/table after the stale-frame false PASS was detected and corrected. The chosen path remains date-specific archived/primary evidence.

## 11. MULTI-YEAR ACQUISITION GATE

Massive acquisition is still forbidden.

Before acquisition:

1. calendar coverage must reach zero unresolved candidate dates;
2. verdict must be PASS;
3. then freeze the exact >=5-year execution window;
4. only then download native Dukascopy `.bi5` real ticks with manifest/hash/reconciliation;
5. no OHLC M1, interpolation, synthetic or substituted ticks.

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Resolve `2019-07-03` only if a materially new, date-specific Dukascopy/USATECH broker witness closes the current proof gap. Do not reuse the 2018 rule and do not promote CME-only evidence. If such evidence is found, version the exact whole-hour classification and rerun the 28 historical tests, the 6 late-2019 tests, and coverage. Until then the calendar remains BLOCKED and massive `.bi5` acquisition remains forbidden.**
