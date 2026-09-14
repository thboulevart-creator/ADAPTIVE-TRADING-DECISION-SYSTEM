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

Historical broker-evidence route gate:

`04-REFERENCE/HISTORICAL-BROKER-EVIDENCE-ROUTE-QUALIFICATION.md`

Route exploration:

`reports/data-qualification/historical_broker_evidence_route_exploration_v1.md`

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

## Historical broker-evidence route exploration

Overall route-exploration verdict:

**BLOCKED — `NO_NEW_HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFIED`**

Candidate mechanisms were evaluated as mechanisms before any systematic reuse across the 67 gaps.

### JForex offline-time-domain route

**FAIL — `OFFLINE_TIME_DOMAIN_DOES_NOT_COVER_WEEKDAY_HOLIDAY_SESSIONS`**

Authoritative Dukascopy API support explicitly states that a holiday in the middle of the week is not included by `getOfflineTimeDomains()`. This mechanism must not be promoted from weekend-offline data into holiday evidence.

### Official Trading Breaks widget historical-date route

**BLOCKED — `HISTORICAL_WIDGET_SEMANTICS_AND_PAYLOAD_NOT_VERIFIED`**

The official widget exposes a `date` parameter and is therefore a materially new technical route, but historical retrieval semantics, payload retention, exact `USATECH.IDX/USD` identity and historical special-session rows have not yet been captured reproducibly.

### Official Dukascopy Market News archive

**BLOCKED — `OFFICIAL_ARCHIVE_EXISTS_BUT_TARGET_INSTRUMENT_TIMING_NOT_RECOVERED`**

The archive preserves historical broker bulletins and supports historical search/date context. Tested in-window notices still delegate detailed hours to the Trading Breaks Calendar and do not yet provide exact `USATECH.IDX/USD` holiday timing.

### Archived Trading Breaks/widget snapshots

**BLOCKED — `NO_VERIFIED_ARCHIVED_TRADING_BREAKS_SNAPSHOT_RECOVERED`**

Failure to recover a snapshot is not evidence that no snapshot exists.

### Direct/archived Dukascopy support witness

**BLOCKED — `NO_TARGET_DATE_INSTRUMENT_SPECIFIC_SUPPORT_WITNESS_OBTAINED`**

No new exact target-date, target-instrument broker response has been collected.

No date-level calendar record changed as a result of this route exploration.

## Freeze execution window

Decision:

**BLOCKED — `EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`**

The execution-window candidate is defined but cannot be frozen because 67 in-window candidates remain unresolved.

The rule MUST NOT be changed or the boundaries moved merely to reduce this count.

Discovery of a plausible evidence mechanism does not change this verdict until admissible date-level evidence actually resolves the in-window gaps.

## Authorize massive `.bi5` acquisition

Decision:

**BLOCKED — `EXECUTION_WINDOW_NOT_FROZEN`**

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
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = BLOCKED`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`
- `REAL_BACKTEST = BLOCKED`

## Exactly one next governed action

**Technically qualify the official Dukascopy Trading Breaks widget historical-date route against the already-qualified `2020-02-17 — PRESIDENTS_DAY` gold-standard witness before using the route on any unresolved in-window date.**

Required calibration evidence:

1. execute the official widget in a JavaScript/network-capable environment;
2. record exact widget configuration;
3. capture actual endpoint/request path and parameters;
4. demonstrate historical-date semantics rather than infer them from the presence of a `date` field;
5. capture response payload or rendered historical row;
6. verify explicit `USATECH.IDX/USD` identity;
7. verify exact special-session timing against the locked 2020 witness;
8. issue PASS/FAIL/BLOCKED for the route;
9. only if calibration passes, probe one unresolved in-window date before considering systematic use.

Do not repeat generic date-by-date searches. Do not move the window. Do not download `.bi5`. Do not start a real backtest.