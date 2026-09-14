# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — GLOBAL CROSS-YEAR CALENDAR AUDIT COMPLETE

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Previous checkpoint / global-audit start HEAD:** `3e1324199b4e8ab8c2c2534d264d3dea6b859193`
- **Global audit report:** `reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md`
  - creation commit `ce7d0869efeddcf27e496f3bb9410aa08534c957`
- **Current boundary application:** `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
  - update commit `a8a64c3c15e7fbf4699f5c496fa3a0d9d2392d4c`
- **Durable global-audit backup:** `99-BACKUP/SESSION-2026-09-14-GLOBAL-CALENDAR-COVERAGE-AUDIT.md`
  - commit `d4f89eb8350dca66faf844e3ba8bdc5020eede20`
- **Coverage envelope:** `2018-05-01` → `2026-08-14`
- **Chronological annual/segment research:** COMPLETE TO ENVELOPE END
- **Execution/backtest window frozen:** NO
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized
- **Latest observed executable calendar tests:** `34 PASS`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-GLOBAL-CALENDAR-COVERAGE-AUDIT.md`
4. `reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md`
5. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `tools/coverage_execution_window_boundary.py`
8. `tools/dukascopy_usatech_calendar_coverage.py`
9. compare active branch against this checkpoint final HEAD before writing anything.

Do not reconstruct the annual 2019–2026 work from conversation history.

## 3. GLOBAL CROSS-YEAR AUDIT VERDICT

Global accounting audit:

**PASS**

Reason:

`ALL_111_CANDIDATES_RECONCILED_WITH_24_RESOLVED_87_UNRESOLVED_AND_NO_INTEGRITY_DEFECT`

This PASS means only that the global candidate/evidence accounting is complete and internally consistent.

It does **not** mean global calendar coverage is complete.

## 4. GLOBAL RECONCILIATION

| Period | Candidates | Resolved | Unresolved |
|---|---:|---:|---:|
| 2018-05-01 → 2018-12-31 | 10 | 10 | 0 |
| 2019 | 13 | 12 | 1 |
| 2020 | 13 | 1 | 12 |
| 2021 | 13 | 0 | 13 |
| 2022 | 12 | 0 | 12 |
| 2023 | 13 | 0 | 13 |
| 2024 | 14 | 0 | 14 |
| 2025 | 15 | 1 | 14 |
| 2026-01-01 → 2026-08-14 | 8 | 0 | 8 |
| **TOTAL** | **111** | **24** | **87** |

Arithmetic is exact:

- candidates = `111`;
- resolved = `24`;
- unresolved = `87`;
- `24 + 87 = 111`.

## 5. EXECUTABLE CALENDAR INTEGRITY

Current executable source:

`tools/dukascopy_usatech_calendar.py`

Current `SPECIAL_SESSION_EVIDENCE` distribution:

- 2018: 10
- 2019: 12
- 2020: 1
- 2021: 0
- 2022: 0
- 2023: 0
- 2024: 0
- 2025: 1
- 2026 bounded: 0

Total: **24**.

`NO_SPECIAL_CHANGE_EVIDENCE`: **0**.

Integrity state:

- orphan special evidence: **0**;
- contradictory overlap: **0**;
- evidence-shape errors: **0**;
- hidden/reclassified prior gaps: **0**;
- prior gaps preserved: **YES**.

First unresolved remains:

`2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**.

## 6. LOCKED BOUNDARY DECISIONS

Contract:

`COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

### Global coverage declaration

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

Reason: unresolved = **87**; PASS requires unresolved = 0.

### Execution-window feasibility

**BLOCKED — `NO_ADMISSIBLE_FIVE_YEAR_ZERO_UNRESOLVED_WINDOW_UNDER_CURRENT_EVIDENCE`**

Proof:

- first unresolved occurs `2019-07-03`;
- the envelope starts `2018-05-01`, leaving far less than five years before the first gap;
- every later annual/segment block through `2026-08-14` contains unresolved dates;
- therefore every possible contiguous >=5-year subset inside the current envelope intersects unresolved evidence.

This is BLOCKED rather than FAIL because evidence could in principle be completed later.

### Execution-window freeze

**BLOCKED — `EXECUTION_WINDOW_NOT_DEFINED`**

No exact independently justified >=5-year execution window is currently versioned.

### Massive native `.bi5` acquisition

**BLOCKED — `EXECUTION_WINDOW_NOT_FROZEN`**

Massive acquisition remains forbidden.

### Real backtest

**BLOCKED — `UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`**

No real backtest may begin.

## 7. CURRENT ACTION MATRIX

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `EXECUTION_WINDOW_FEASIBILITY = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`
- `REAL_BACKTEST = BLOCKED`

No executable calendar file changed during the global audit, so unchanged calendar tests were intentionally not rerun merely for timestamp freshness.

## 8. LOCKED METHODOLOGICAL CONCLUSIONS

- The 87 BLOCKED dates are not an audit failure; hiding or reclassifying them would be a failure.
- Annual/segment audit PASS never implies calendar coverage PASS.
- Global audit PASS never implies global coverage PASS.
- A future execution window may be narrower than the envelope, but it must be contiguous, >=5 years, independently justified, versioned, and contain zero unresolved/FAIL candidates before freeze PASS.
- A window MUST NOT be moved or shortened merely to avoid a known gap.
- Global gaps outside a future admissible window remain globally BLOCKED and visible.
- Massive `.bi5` acquisition remains a separate downstream authorization.
- No OHLC M1, synthetic ticks, interpolation, or substituted data may bypass the native-tick gate.

## 9. EXACTLY ONE NEXT GOVERNED ACTION

**Define and version an execution-window selection rationale that is independent of known gaps, without freezing a window or acquiring data yet.**

Required sequence:

1. verify branch == this checkpoint final HEAD;
2. formalize the window-selection policy **before** using unresolved dates to choose boundaries;
3. require the resulting window to be contiguous and at least five calendar years;
4. version the independent research rationale;
5. derive the exact candidate window mechanically from that rationale;
6. enumerate its in-window calendar candidates and exact unresolved set;
7. apply `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1` to that candidate;
8. do not claim freeze PASS while any in-window unresolved remains;
9. use the resulting unresolved set only as a targeted future evidence-recovery frontier;
10. do not download `.bi5` and do not start a real backtest.

The selection rationale must not be reverse-engineered from which dates are easiest to qualify.