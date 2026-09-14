# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Global consolidation report:

`reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md`

## Current governed state

- Global research envelope: `2018-05-01` → `2026-08-14`
- Chronological qualification: complete to governed envelope end
- Candidate dates: **111**
- Resolved candidate dates: **24**
- Unresolved candidate dates: **87**
- Global FAIL dates: **0**
- Orphan special-evidence dates: **0**
- Contradictory evidence dates: **0**
- Evidence-shape errors: **0**
- Prior gaps preserved: **yes**
- Prior gaps hidden/reclassified: **no**
- Execution window frozen: **no**
- Massive acquisition authorized: **no**
- Real backtest authorized: **no**

## Global accounting audit

Decision:

**PASS**

Reason:

`ALL_111_CANDIDATES_RECONCILED_WITH_24_RESOLVED_87_UNRESOLVED_AND_NO_INTEGRITY_DEFECT`

This PASS certifies accounting integrity only. It does not certify coverage completeness.

## Action — Declare global coverage PASS

Decision:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

Eighty-seven candidate dates remain unresolved.

## Action — Execution-window feasibility / freeze

No exact execution window is currently versioned.

Executable freeze decision:

**BLOCKED — `EXECUTION_WINDOW_NOT_DEFINED`**

Cross-year feasibility conclusion:

**BLOCKED — `NO_ADMISSIBLE_FIVE_YEAR_ZERO_UNRESOLVED_WINDOW_UNDER_CURRENT_EVIDENCE`**

Reason:

- first unresolved candidate: `2019-07-03`;
- envelope start is only `2018-05-01`, so less than five years of resolved history exist before the first gap;
- every later annual/segment block through `2026-08-14` contains unresolved candidates;
- therefore every possible contiguous >=5-year window inside the current envelope intersects unresolved evidence.

This is BLOCKED because evidence could in principle be completed. No window is being proposed or cherry-picked.

## Action — Authorize massive `.bi5` acquisition

Decision:

**BLOCKED — `EXECUTION_WINDOW_NOT_FROZEN`**

The acquisition gate cannot be reached until an execution window first receives PASS under the boundary contract and all mandatory window/data gates pass.

Massive `.bi5` acquisition remains forbidden.

## Action — Start real backtest

Decision:

**BLOCKED — `UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`**

A real backtest remains downstream of a valid frozen >=5-year execution window and qualified native tick acquisition/reconciliation.

## Current boundary matrix

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `EXECUTION_WINDOW_FEASIBILITY = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`
- `REAL_BACKTEST = BLOCKED`

## Exactly one next governed action

**Define and version an execution-window selection rationale independent of known gaps, without freezing a window or acquiring data yet.**

Only after the rationale exists independently may its exact contiguous >=5-year candidate window be enumerated and its unresolved set measured.

Do not choose the window because it avoids a known gap. Do not download `.bi5`. Do not start a real backtest.