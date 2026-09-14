# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 03

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Global calendar: **111 candidates / 34 resolved / 77 unresolved / 0 FAIL**
- Execution-window candidate: **68 candidates / 11 resolved / 57 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Attempt-aware recovery progression: **PASS**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL**
- Historical attempt ledger entries: **15**
- Registered material capability changes: **0**
- Attempted BLOCKED / currently execution-ineligible: **4**
- Currently execution-eligible unresolved: **53**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened, or lengthened to avoid unresolved dates.

## Resolved in-window dates

The execution-window candidate now contains exactly **11** resolved dates:

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
6. `2022-02-21 — PRESIDENTS_DAY`
7. `2022-05-30 — MEMORIAL_DAY`
8. `2022-06-20 — JUNETEENTH_OBSERVED`
9. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
10. `2022-09-05 — LABOR_DAY`
11. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

Global coverage remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

The positive-record boundary is unchanged: empty/no-record responses and neighboring-date overlaps do not prove regular trading and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Batch 03 authoritative execution and adjudication

Frozen membership:

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

Authoritative browser runtime:

- workflow run: `34892253133`
- job: `104137558818`
- probe commit: `9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4`
- artifact ID: `10367930592`
- artifact SHA-256: `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`
- conclusion: **SUCCESS**

Independent adjudication:

- `2022-05-30` → **PASS** — record `37019`, Memorial Day
- `2022-06-20` → **PASS** — record `38945`, Juneteenth Holiday
- `2022-07-01` → **BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED**
- `2022-07-04` → **PASS** — record `41225`, Independence Day
- `2022-09-05` → **PASS** — record `42569`, Labor Day

Only the four PASS dates were integrated into executable calendar evidence. `2022-07-01` remains unresolved/BLOCKED and MUST NOT be interpreted as evidence of a normal session.

## Batch 03 adversarial closure

The first adjudication run (`34892773715`, job `104139273746`) deliberately failed because a representation adapter compared DOM human instrument name `USATECH.IDX/USD` directly with network instrument ID `9016`. The adapter was corrected to validate the exact DOM name before normalizing to governed ID `9016`. Corrected adjudication run `34893116066`, job `104140394051`, passed with **62 tests** and final `4 PASS / 1 BLOCKED / 0 FAIL`.

The first integration run (`34893471211`, job `104141565466`) also failed safely before pushing an integration commit. It exposed a stale Batch 02 current-count assertion and, more importantly, that historical adjudication replay was incorrectly tied to the mutable live recovery queue. The replay boundary was separated from live execution eligibility without changing the broker evidence capability or observing new broker data.

Final atomic integration:

- run: `34893854678`
- job: `104142824703`
- regression: **104 passed**
- integration commit: `d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Independent persisted-HEAD regression:

- run: `34893976903`
- job: `104143235284`
- conclusion: **SUCCESS**
- regression: **104 passed in 0.60s**

All operational Batch 03 workflows are archived to `workflow_dispatch` only.

## Attempt-aware progression after Batch 03

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Current deterministic state:

- calendar unresolved dates: **57**
- historical attempts: **15**
- registered material capability changes: **0**
- attempted BLOCKED / currently execution-ineligible: **4**
- unresolved currently execution-eligible: **53**

The four already-attempted BLOCKED dates remain unresolved but are not replay-eligible under the unchanged capability:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Each is governed by `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED` until a versioned, qualified material evidence-capability change explicitly addresses its blocker.

The first currently eligible unresolved candidate is:

`2022-11-24 — THANKSGIVING_DAY`

This does **not** define Batch 04 membership. The complete Batch 04 membership may only be derived mechanically and versioned during the next governed freeze action.

## Current boundary decisions

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Freeze and version Batch 04 with `BATCH_SIZE = 5` as exactly the first five entries of the current governed `eligible_recovery_queue()`, BEFORE any Batch 04 historical observation.**

The membership MUST be derived mechanically at freeze time and versioned before Chromium. No candidate may be inserted, skipped, substituted, or reordered based on expected outcome, holiday type, apparent ease, source availability, manual preference, or convenience.

This document does **not** define or freeze Batch 04 membership.

No `.bi5` acquisition. No real backtest.
