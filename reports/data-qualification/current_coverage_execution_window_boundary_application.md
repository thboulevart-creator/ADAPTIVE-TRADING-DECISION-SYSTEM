# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

### Global calendar accounting after Trading Breaks Batch 01

- candidate dates: **111**
- resolved candidate dates: **28**
- unresolved candidate dates: **83**
- FAIL dates: **0**
- orphan special evidence: **0**
- contradictory evidence: **0**
- evidence-shape errors: **0**

Global coverage remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

### Candidate execution-window accounting

The independently selected window remains unchanged:

`2021-08-14` → `2026-08-14`

Current in-window state:

- candidates: **68**
- resolved: **5**
- unresolved: **63**
- FAIL: **0**

Resolved in-window candidates:

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

The window MUST NOT be shifted, shortened, or lengthened to avoid unresolved dates.

## Historical broker-evidence route

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

Route verdict:

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

The Trading Breaks route remains admissible only for **positive exact historical break records**. Empty/no-record responses are not negative evidence and MUST NOT become `NO_SPECIAL_CHANGE_EVIDENCE`.

## Systematic recovery protocol

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

Qualification:

**PASS — `SYSTEMATIC_TRADING_BREAKS_RECOVERY_PROTOCOL_REJECTS_KNOWN_BYPASSES`**

The protocol continues to reject queue/date/instrument drift, absent payloads, neighboring-date substitution, DOM/network contradiction, invalid provenance, reopen-semantic errors, and partial-hour rounding errors.

## Batch 01 policy and execution

Policy contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH_POLICY_V1`

Frozen operational batch size:

`BATCH_SIZE = 5`

Original immutable Batch 01 membership:

1. `2021-11-25 — THANKSGIVING_DAY`
2. `2021-11-26 — THANKSGIVING_FRIDAY`
3. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2021-12-24 — CHRISTMAS_OBSERVED`
5. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`

The size and membership were fixed before new outcome observation.

### Authoritative Batch 01 runtime provenance

- workflow run: `34885895206`
- job: `104116336235`
- probe commit: `479900e05eebc6e2c29e0f9f3bddfdfc78e78224`
- artifact ID: `10364872726`
- artifact SHA-256: `95d6d820393a358a5539f7959ffa06d240b344b1182a57b5b4f13bb43cb74a1f`
- workflow conclusion: `SUCCESS`
- instrument: `USATECH.IDX/USD` / ID `9016`

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch01_qualification.md`

### Independent Batch 01 adjudication

- `2021-11-25` → **PASS — exact positive broker break record**
- `2021-11-26` → **PASS — exact positive broker break record**
- `2021-12-23` → **PASS — exact positive broker break record**
- `2021-12-24` → **BLOCKED — no exact target-date positive record admissible**
- `2021-12-31` → **BLOCKED — no positive exact broker record recovered**

Batch result:

- PASS: **3**
- BLOCKED: **2**
- FAIL: **0**

Only the three PASS dates were integrated into executable calendar evidence.

## Executable evidence integrated

### 2021-11-25 — Thanksgiving Day

- broker record: `30449`
- break start: `17:59Z`
- final closed minute: `22:59Z`
- reopen: `23:00Z`
- governed fully closed UTC hours: `18,19,20,21,22`

### 2021-11-26 — Thanksgiving Friday

- broker record: `30450`
- break start: `18:14Z`
- interval continues through weekend to `2021-11-28 22:59Z`
- reopen: `2021-11-28 23:00Z`
- additional special-session whole closed UTC hours on target date: `19,20,21`
- Friday `22,23` remain classified by the existing regular weekly-close rule and were not reclassified as holiday hours.

### 2021-12-23 — Christmas pre-holiday session

- broker record: `31532`
- break start: `21:14Z`
- interval continues through Christmas/weekend to `2021-12-26 22:59Z`
- reopen: `2021-12-26 23:00Z`
- governed fully closed UTC hours on target date: `22,23`

## Post-integration regression

Validated integration workflow:

- run: `34887010102`
- result: **SUCCESS**
- combined regression before persistence: **91 passed**
- asserted global accounting: `111 / 28 resolved / 83 unresolved`
- asserted execution-window accounting: `68 / 5 resolved / 63 unresolved`

Persisted executable-evidence commit:

`18271cec8c07a96c2ea0fb348ab042d3c72d0c7d`

Independent calendar regression against persisted HEAD:

- workflow run: `34887061155`
- job: `104120211534`
- result: **SUCCESS**
- pytest: **67 passed**
- governed global accounting assertions: **PASS**

## Current recovery queue boundary

Current in-window unresolved queue size:

`63`

First unresolved candidate:

`2021-12-24 — CHRISTMAS_OBSERVED`

Last unresolved candidate:

`2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

The first five current queue entries, which are the deterministic candidates for the next fixed-size batch if the same batch policy is continued, are:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
3. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
4. `2022-02-21 — PRESIDENTS_DAY`
5. `2022-04-15 — GOOD_FRIDAY`

These entries are derived from the post-Batch-01 governed queue, not selected by expected ease or outcome.

## Current boundary decisions

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01 = PASS`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST = BLOCKED — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Freeze and version Batch 02 as the next five entries of the current governed recovery queue, preserving `BATCH_SIZE = 5`, before observing any new Batch 02 historical outcomes; then execute those five dates chronologically under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`.**

No date may be skipped, substituted, or reordered because it appears easy, difficult, likely positive, or likely empty.

After Batch 02: adjudicate each date independently; integrate only true positive-record PASS dates; retain no-record dates as BLOCKED; rerun calendar/boundary regression only if executable evidence changes; persist run/job/artifact/SHA/commit provenance; update backup and Recovery Checkpoint.

No `.bi5` acquisition. No real backtest.
