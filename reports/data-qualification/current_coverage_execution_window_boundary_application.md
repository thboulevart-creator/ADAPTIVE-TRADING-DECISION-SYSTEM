# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Global consolidation report:

`reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md`

Window-selection rule:

`04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md`

Rule qualification:

`reports/data-qualification/execution_window_selection_rule_qualification.md`

Window-candidate application:

`reports/data-qualification/execution_window_candidate_v1.md`

## Current governed state

- Global research envelope: `2018-05-01` → `2026-08-14`
- Chronological qualification: complete to governed envelope end
- Global candidate dates: **111**
- Global resolved candidate dates: **24**
- Global unresolved candidate dates: **87**
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

## Global coverage declaration

Decision:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

Eighty-seven candidate dates remain unresolved globally.

## Window-selection rationale

`EXECUTION_WINDOW_SELECTION_RULE_V1` is versioned and adversarially qualified before application.

Rule verdict:

**PASS — `WINDOW_SELECTION_RATIONALE_IS_VERSIONED_AND_GAP_INDEPENDENT`**

The rule uses only:

- the already-governed coverage end;
- the already-locked minimum five-calendar-year research horizon.

It does not use gap locations, gap counts, performance, or sub-period tick availability.

## Mechanically produced execution-window candidate

The qualified rule produces:

- `window_start = 2021-08-14`
- `window_end = 2026-08-14`
- duration = exactly 5 calendar years
- contiguous = YES
- manual exclusions = NO
- selection rationale versioned = YES
- selection independent of known gaps = YES
- shifted to avoid known gap = NO
- candidate set enumerated = YES

Candidate-calendar state inside this interval:

- candidates = **68**
- resolved = **1**
- unresolved = **67**
- FAIL = **0**

The sole resolved in-window candidate is:

`2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`.

All other 67 dates preserve their previously qualified BLOCKED state.

Global gaps outside the candidate window remain visible:

`87 - 67 = 20` outside-window unresolved candidates.

They are not reclassified or deleted.

## Freeze execution window

Boundary state now has an exact candidate window and known in-window counts.

Decision:

**BLOCKED — `EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`**

This supersedes the prior temporary reason `EXECUTION_WINDOW_NOT_DEFINED`.

The candidate has now been defined, but it cannot be frozen because 67 in-window candidates remain unresolved.

The rule MUST NOT be changed or the boundaries moved merely to reduce this count.

## Authorize massive `.bi5` acquisition

Decision:

**BLOCKED — `EXECUTION_WINDOW_NOT_FROZEN`**

The candidate is defined but has not received freeze PASS.

Massive native `.bi5` acquisition remains forbidden.

## Start real backtest

Decision:

**BLOCKED — `UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`**

A real backtest remains downstream of:

1. resolving all required in-window calendar evidence;
2. execution-window freeze PASS;
3. mandatory window/data gates PASS;
4. native tick acquisition/reconciliation;
5. fixed OOS split and execution/cost assumptions.

## Current boundary matrix

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`
- `REAL_BACKTEST = BLOCKED`

## Exactly one next governed action

**Do not repeat the already-exhausted date-by-date generic holiday searches. Determine whether a materially new admissible broker-evidence route exists that can resolve the 67 in-window BLOCKED candidates without changing the selected boundaries.**

The next investigation must target a genuinely new evidence class/route, such as an official historical Dukascopy Trading Breaks dataset/archive/API/export or equivalent broker-origin historical session record.

If no materially new route can be demonstrated, the candidate window remains BLOCKED; the selection rule must not be rewritten to escape that result.

Do not download `.bi5`. Do not start a real backtest.