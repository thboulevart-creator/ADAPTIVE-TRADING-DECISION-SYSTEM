# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

### Global calendar accounting

- candidate dates: **111**
- resolved candidate dates: **25**
- unresolved candidate dates: **86**
- FAIL dates: **0**
- orphan special evidence: **0**
- contradictory evidence: **0**
- evidence-shape errors: **0**

Global coverage remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

### Candidate execution-window accounting

The independently selected five-year candidate remains unchanged:

`2021-08-14` → `2026-08-14`

Current in-window state:

- candidates: **68**
- resolved: **2**
- unresolved: **66**
- FAIL: **0**

Resolved in-window candidates:

1. `2021-09-06 — LABOR_DAY`
2. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

The window MUST NOT be shifted or shortened because unresolved dates remain.

## Historical broker-evidence route

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

Final route verdict:

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

### Gold-standard calibration

Witness:

`2020-02-17 — PRESIDENTS_DAY`

Report:

`reports/data-qualification/historical_trading_breaks_widget_calibration_2020_02_17.md`

Verdict:

**PASS — `HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS`**

Authoritative runtime evidence:

- workflow run: `34866241511`
- artifact ID: `10356927580`
- artifact SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`
- explicit instrument: `USATECH.IDX/USD` / ID `9016`
- break: `2020-02-17T18:00:00Z` → final closed minute `22:59:00Z`
- derived reopen: `23:00:00Z`

### First unresolved in-window pilot

Pilot:

`2021-09-06 — LABOR_DAY`

Report:

`reports/data-qualification/historical_trading_breaks_widget_pilot_2021_09_06.md`

Verdict:

**PASS — `EXACT_PRIMARY_BROKER_USATECH_HISTORICAL_BREAK_WITNESS_RECOVERED`**

Date-level gate:

**PASS-A — exact primary broker date/instrument/timing witness.**

Authoritative runtime evidence:

- workflow run: `34866699952`
- artifact ID: `10357256669`
- artifact SHA-256: `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`
- break: `2021-09-06T17:00:00Z` → final closed minute `21:59:00Z`
- derived reopen: `22:00:00Z`
- governed fully closed UTC hours: `17,18,19,20,21`

The executable calendar now contains exactly this recovered pilot record as `SPECIAL_LABOR_DAY_2021`.

## Regression status after pilot integration

Initial regression workflow run `34867320843` failed because two downloader-gate tests still used `2018-09-03` as an allegedly unresolved witness even though that date was already qualified. This was a stale test fixture, not a calendar regression.

The fixture was corrected to use genuinely unresolved `2021-11-25 — THANKSGIVING_DAY` without changing gate logic.

Corrected regression:

- commit: `ccb1f9fd6dd7eb5773564ca1759cfc6eb63522b4`
- workflow run: `34869158505`
- verdict: **PASS**
- pytest: **63 passed**
- governed coverage assertions: **PASS**
- resulting global counts: `111 / 25 resolved / 86 unresolved`

## Current boundary decisions

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST = BLOCKED — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Negative-evidence boundary

The qualified widget route is currently admissible for **positive historical break records**.

An empty/no-record response MUST NOT be promoted to `NO_SPECIAL_CHANGE_EVIDENCE` until a separate completeness/negative-evidence contract is qualified.

## Local runtime evidence archive

Governed workstation location:

`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM\LOCAL-EVIDENCE\dukascopy-trading-breaks-widget\2026-09-14\`

Raw ZIP archives are local-only and ignored by Git. Their filenames/hashes are to be recorded in `manifest-sha256.csv`.

Repository policy:

`LOCAL-EVIDENCE/README.md`

## Exactly one next governed action

**Formalize and qualify a systematic historical Trading Breaks recovery protocol before applying the route across the remaining 66 unresolved in-window candidates.**

The protocol must preserve exact-date addressing, explicit broker instrument identity, positive-record evidence capture, calibrated end-time semantics, deterministic provenance, independent date-level verdicts, fixed candidate-window boundaries, and the prohibition on interpreting empty responses as regular-hours proof.

No `.bi5` acquisition. No real backtest.
