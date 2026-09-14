# SESSION BACKUP — 2026-09-14 — TRADING BREAKS WIDGET ROUTE PASS

## Purpose

Durable recovery snapshot after technical qualification of the Dukascopy Trading Breaks historical widget route, one unresolved-date pilot recovery, executable calendar integration, regression repair, and completion of the workstation-side runtime-evidence archive.

## Authoritative branch

`feat/multi-year-dukascopy-acquisition`

## Locked execution-window candidate

`2021-08-14` → `2026-08-14`

The window-selection rationale remains independent of gap locations and MUST NOT be moved to escape unresolved dates.

Current in-window accounting:

- candidates: **68**
- resolved: **2**
- unresolved: **66**
- FAIL: **0**

Resolved in-window dates:

1. `2021-09-06 — LABOR_DAY`
2. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

## Global calendar accounting

After integration of `2021-09-06`:

- candidates: **111**
- resolved: **25**
- unresolved: **86**
- FAIL: **0**
- orphan evidence: **0**
- contradictory evidence: **0**
- evidence-shape errors: **0**

Global coverage remains BLOCKED.

## Historical widget route qualification

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

Final verdict:

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

### Calibration witness — 2020-02-17 PRESIDENTS_DAY

Report:

`reports/data-qualification/historical_trading_breaks_widget_calibration_2020_02_17.md`

Verdict:

**PASS — `HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS`**

Authoritative execution:

- run ID: `34866241511`
- artifact ID: `10356927580`
- artifact SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`
- target instrument ID: `9016`
- target instrument: `USATECH.IDX/USD`
- break start: `2020-02-17T18:00:00Z`
- final closed minute: `2020-02-17T22:59:00Z`
- derived reopen: `2020-02-17T23:00:00Z`

Calibrated representation invariant:

`reopen = break_end_last_closed_minute + 60 seconds`

### First unresolved in-window pilot — 2021-09-06 LABOR_DAY

Selection rule:

`EARLIEST_UNRESOLVED_IN_FROZEN_EXECUTION_WINDOW_CANDIDATE`

Report:

`reports/data-qualification/historical_trading_breaks_widget_pilot_2021_09_06.md`

Verdict:

**PASS — `EXACT_PRIMARY_BROKER_USATECH_HISTORICAL_BREAK_WITNESS_RECOVERED`**

Date-level gate:

**PASS-A**

Authoritative execution:

- run ID: `34866699952`
- job ID: `104052206522`
- artifact ID: `10357256669`
- artifact SHA-256: `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`
- break start: `2021-09-06T17:00:00Z`
- final closed minute: `2021-09-06T21:59:00Z`
- derived reopen: `2021-09-06T22:00:00Z`
- fully closed UTC hours: `17,18,19,20,21`

## Executable integration and regression

`tools/dukascopy_usatech_calendar.py` contains:

`2021-09-06 — SPECIAL_LABOR_DAY_2021`

Dedicated test:

`tests/test_dukascopy_usatech_calendar_2021_labor_day.py`

Initial post-integration regression run `34867320843` failed because two tests used stale unresolved fixture `2018-09-03`. Only the fixture was corrected to genuinely unresolved `2021-11-25`; gate logic was unchanged.

Correction commit:

`ccb1f9fd6dd7eb5773564ca1759cfc6eb63522b4`

Corrected regression:

- run ID: `34869158505`
- verdict: **PASS**
- pytest: **63 passed**
- global counts: `111 candidates / 25 resolved / 86 unresolved`

## Local runtime evidence archive — COMPLETED

Canonical workstation root:

`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM\LOCAL-EVIDENCE\dukascopy-trading-breaks-widget\2026-09-14\`

Raw ZIP destination:

`raw-zips\`

Governed manifest:

`LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`

The PowerShell helper was executed successfully on the workstation on `2026-09-14` and archived all three retained ZIPs. The generated manifest was displayed, and all three archived ZIPs were re-hashed independently with PowerShell `Get-FileHash -Algorithm SHA256`.

### Local archive verification

1. `dukascopy-trading-breaks-widget-2020-02-17-authoritative.zip`
   - size: `810965`
   - SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`
   - role: `AUTHORITATIVE_CALIBRATION`
   - artifact ID: `10356927580`
   - run: `34866241511`

2. `dukascopy-trading-breaks-widget-2020-02-17-headed-browser.zip`
   - size: `709841`
   - SHA-256: `aaf5341f3d7e10b60cc24622d6f16c2ffa3e3f31d6b108f69f53c6f3a2d48849`
   - role: `TECHNICAL_TRACE_NON_AUTHORITATIVE`
   - artifact ID: `10356971957`
   - run: `34865846126`

3. `dukascopy-trading-breaks-widget-pilot-2021-09-06-authoritative.zip`
   - size: `797338`
   - SHA-256: `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`
   - role: `AUTHORITATIVE_PILOT_PASS_A`
   - artifact ID: `10357256669`
   - run: `34866699952`

All three locally recomputed hashes matched the governed expected values.

The exact generated CSV manifest is now versioned in Git. Raw ZIPs remain local and ignored by Git.

The archival helper remains versioned in GitHub for reproducibility even if removed from the local working tree after use.

## Boundary matrix

- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`
- `REAL_BACKTEST = BLOCKED`

## Important remaining limitation

The calibrated route is qualified for **positive historical break recovery** only.

Empty/no-record responses are NOT qualified as proof of normal trading hours. They remain non-evidence unless a separate negative-evidence/completeness contract is formally qualified.

## Exactly one next governed action

**Formalize and adversarially qualify a systematic historical Trading Breaks recovery protocol before applying the route across the remaining 66 unresolved in-window candidates.**

Required properties:

- frozen candidate scope and deterministic ordering;
- exact-date historical addressing;
- explicit `USATECH.IDX/USD` / instrument ID `9016` identity;
- raw broker-native network payload capture;
- rendered/DOM cross-check where available;
- calibrated end-time semantics;
- independent positive-record date-level PASS only;
- no inference from empty/no-record responses;
- reproducible workflow/run/artifact/hash provenance;
- no execution-window movement based on outcomes;
- calendar integration only after date-level PASS;
- regression and coverage audit after executable changes.

No `.bi5`. No real backtest.
