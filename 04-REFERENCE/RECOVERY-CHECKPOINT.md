# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## 1. CURRENT STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Starting checkpoint:** `501a090afd09da1bcd30e9111c53147d682c5317`
- **Calendar evidence commit:** `2f0a088bc8f6aaafed9db9c1ed6966301271ac75`
- **Calendar test commit:** `df668b89b219cee8e72e20a10d5c307439a8046d`
- **Durable session backup commit:** `4e05e4f183a7653e28c086ec7864c41a2c30c26e`
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
  - contains 18 date-specific special-session evidence records in the coverage envelope.
- `tools/dukascopy_usatech_calendar_coverage.py`
  - `DUKASCOPY_USATECH_SPECIAL_SESSION_COVERAGE_V1`
- `tests/test_dukascopy_usatech_calendar.py`
  - 28 tests versioned after the 2019 additions.

## 5. LATEST OBSERVED TEST EXECUTION

Observed local execution after materializing the current GitHub test blob and current calendar classification/evidence logic:

```text
............................                                             [100%]
28 passed in 0.08s
```

There is no GitHub Actions workflow available for this branch. The local execution environment cannot directly reach `github.com`; GitHub state and writes were handled through the GitHub connector, while Python execution was performed locally from the versioned logic.

## 6. LATEST OBSERVED COVERAGE VERDICT

- `candidate_dates`: **111**
- `resolved_candidate_dates`: **18**
- `special_session_evidence_dates`: **18**
- `no_special_change_evidence_dates`: **0**
- `unresolved_candidate_dates`: **93**
- `contradictory_evidence_dates`: `[]`
- `evidence_shape_errors`: `[]`
- `orphan_special_evidence`: `[]`
- `verdict`: **BLOCKED**
- `reason`: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`
- coverage script exit code: `2`

This remains a clean BLOCKED, not FAIL.

## 7. RESOLVED DATES

All 2018 candidate dates inside the envelope remain resolved:

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

Newly resolved 2019 dates:

- 2019-01-01 New Year's Day
- 2019-01-21 Martin Luther King Jr. Day
- 2019-02-18 Presidents Day
- 2019-05-27 Memorial Day
- 2019-11-28 Thanksgiving Day
- 2019-11-29 Thanksgiving Friday

Other previously resolved dates:

- 2020-02-17 Presidents Day
- 2025-01-09 Carter National Day of Mourning

The first unresolved date is now `2019-04-19`.

## 8. REMAINING 2019 FRONTIER

Seven 2019 candidates remain unresolved because the currently available evidence does not yet meet the same exact broker/date-specific timing threshold without extrapolation:

- `2019-04-19` — GOOD_FRIDAY
- `2019-07-03` — INDEPENDENCE_PRE_HOLIDAY_SESSION
- `2019-07-04` — INDEPENDENCE_DAY_OBSERVED
- `2019-09-02` — LABOR_DAY
- `2019-12-24` — CHRISTMAS_PRE_HOLIDAY_SESSION
- `2019-12-25` — CHRISTMAS_OBSERVED
- `2019-12-31` — NEW_YEARS_EVE_CANDIDATE

Do not promote them from generic holiday names, exchange-only evidence that does not establish the Dukascopy treatment, missing BI5 files, or cross-year analogy.

## 9. EVIDENCE DISCIPLINE

- Only complete UTC hourly BI5 buckets proven closed enter `fully_closed_hours_utc`.
- A partially tradable hour remains EXPECTED_OPEN.
- Holiday name alone is not closure evidence.
- HTTP 403/404/503 or missing BI5 data is not closure evidence.
- Do not extrapolate one year's special hours to another year.
- Dukascopy establishes broker special-event context; precise equity-index timing may be supplied by CME evidence when necessary.
- Preserved third-party copies of historical CME tables/summaries must remain explicitly labelled mirror evidence.

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

**Resolve the remaining seven 2019 candidate dates (`2019-04-19`, `2019-07-03`, `2019-07-04`, `2019-09-02`, `2019-12-24`, `2019-12-25`, `2019-12-31`) using date-specific evidence at the same threshold; commit only dates that actually cross the threshold; then rerun the 28-test calendar suite and `tools/dukascopy_usatech_calendar_coverage.py`.**

Massive acquisition remains forbidden until coverage verdict is PASS with zero unresolved dates.
