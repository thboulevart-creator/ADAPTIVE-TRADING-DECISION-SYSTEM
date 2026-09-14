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
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL**
- Attempt-aware recovery progression: **PASS**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14` and MUST NOT be moved to avoid unresolved dates.

## Batch 03 authoritative execution

Frozen immutable membership:

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

Authoritative runtime:

- workflow run: `34892253133`
- job: `104137558818`
- probe commit: `9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4`
- artifact ID: `10367930592`
- artifact SHA-256: `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`
- instrument: `USATECH.IDX/USD` / `9016`
- workflow conclusion: **SUCCESS**

Independent adjudication verdict:

**PASS — `BATCH03_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

Date-level outcomes:

- `2022-05-30` → **PASS** — broker record `37019`, Memorial Day, reopen `22:00Z`
- `2022-06-20` → **PASS** — broker record `38945`, Juneteenth Holiday, reopen `22:00Z`
- `2022-07-01` → **BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`**
- `2022-07-04` → **PASS** — broker record `41225`, Independence Day, reopen `22:00Z`
- `2022-09-05` → **PASS** — broker record `42569`, Labor Day, reopen `22:00Z`

Only the four PASS dates were integrated. `2022-07-01` remains unresolved and is not negative evidence.

## Batch 03 integration and persisted-state regression

Atomic integration workflow:

- run: `34893854678`
- trigger commit: `ea2a6ee39a2ab81eedca54157469c65143d387c6`
- persisted integration commit: `d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`
- conclusion: **SUCCESS**

Independent persisted-HEAD regression:

- run: `34893976903`
- job: `104143235284`
- HEAD under test: `30f6d11bb51473211b9576bde92e85b405ed5606`
- conclusion: **SUCCESS**
- regression suite: **104 passed in 0.60s**

Exact persisted accounting independently asserted:

- global calendar: `111 / 34 / 77`
- execution window: `68 / 11 / 57`
- evidence-shape errors: `0`
- orphan special evidence: `0`
- contradictory evidence dates: `0`
- attempt ledger entries: `15`
- recovery queue unresolved: `57`
- attempted BLOCKED / execution-ineligible: `4`
- execution-eligible unresolved: `53`
- registered material capability changes: `0`

## Attempt-aware progression after Batch 03

Current progression runtime verdict:

**PASS — `ATTEMPT_AWARE_PROGRESSION_STATE_IS_DETERMINISTIC_AND_NON_STARVING`**

Current state:

- calendar unresolved: `57`
- attempt ledger: `15`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `4`
- eligible initial/retry unresolved: `53`

Currently ineligible BLOCKED dates under unchanged capability:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Each remains unresolved in calendar accounting and is excluded only from `eligible_recovery_queue()` under the unchanged capability.

First five currently eligible unresolved candidates are:

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Freeze and version Batch 04 with `BATCH_SIZE = 5` as exactly the first five entries of the governed `eligible_recovery_queue()`, before any Batch 04 historical observation.**

Batch 04 membership MUST be derived mechanically from the current governed eligible queue and MUST NOT use raw `recovery_queue()[:5]`, expected outcome, holiday type, apparent ease, manual substitution, or convenience.

No `.bi5` acquisition. No real backtest.
