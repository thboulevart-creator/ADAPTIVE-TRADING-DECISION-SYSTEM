# SESSION BACKUP — 2026-09-14 — TRADING BREAKS WIDGET ROUTE PASS

## Purpose

Durable recovery snapshot after technical qualification of the Dukascopy Trading Breaks historical widget route, one unresolved-date pilot recovery, executable calendar integration, regression repair, and local runtime-evidence archival policy.

## Authoritative branch

`feat/multi-year-dukascopy-acquisition`

## Locked execution-window candidate

`2021-08-14` → `2026-08-14`

The window-selection rationale remains independent of gap locations and MUST NOT be moved to escape unresolved dates.

Current in-window accounting after the first recovered pilot:

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

### Calibration witness

`2020-02-17 — PRESIDENTS_DAY`

Report:

`reports/data-qualification/historical_trading_breaks_widget_calibration_2020_02_17.md`

Calibration verdict:

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

### First unresolved in-window pilot

`2021-09-06 — LABOR_DAY`

Selection rule:

`EARLIEST_UNRESOLVED_IN_FROZEN_EXECUTION_WINDOW_CANDIDATE`

Report:

`reports/data-qualification/historical_trading_breaks_widget_pilot_2021_09_06.md`

Pilot verdict:

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

## Executable integration

`tools/dukascopy_usatech_calendar.py` now contains:

`2021-09-06 — SPECIAL_LABOR_DAY_2021`

A dedicated test exists:

`tests/test_dukascopy_usatech_calendar_2021_labor_day.py`

## Regression history

First post-integration workflow:

- run ID: `34867320843`
- result: **FAIL**

Cause:

Two downloader gate tests still used `2018-09-03` as an allegedly unresolved date. That fixture had become stale because 2018 Labor Day was already qualified.

This was not a calendar regression and did not invalidate the recovered 2021 witness.

Correction:

- replace only the stale unresolved fixture with `2021-11-25 — THANKSGIVING_DAY`;
- no gate logic change;
- correction commit: `ccb1f9fd6dd7eb5773564ca1759cfc6eb63522b4`.

Corrected regression workflow:

- run ID: `34869158505`
- result: **PASS**
- tests: **63 passed**
- coverage assertions: PASS
- global counts asserted: `111 candidates / 25 resolved / 86 unresolved`

## Local runtime evidence retention

Canonical workstation root:

`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM\LOCAL-EVIDENCE\dukascopy-trading-breaks-widget\2026-09-14\`

Raw archives:

`raw-zips\`

Rules:

- raw ZIPs remain local;
- `.gitignore` excludes `LOCAL-EVIDENCE/**/raw-zips/*.zip`;
- a `manifest-sha256.csv` beside `raw-zips` identifies each local archive by filename, size, timestamp, relative path and SHA-256;
- `LOCAL-EVIDENCE/README.md` records the policy and retained artifact identities.

Do not treat presence of a ZIP as evidence by itself. Reports, artifact identities, hashes and governed verdicts remain authoritative.

## Artifact recovery after chat-link expiry — 2026-09-14

The temporary download links previously surfaced in chat expired. The runtime evidence was **not lost** because the underlying GitHub Actions artifacts remained available.

Three archives were re-downloaded directly from GitHub Actions and their SHA-256 values were recomputed locally in the assistant runtime. All three matched the GitHub digests exactly:

1. `dukascopy-trading-breaks-widget-2020-02-17-authoritative.zip`
   - artifact ID: `10356927580`
   - run: `34866241511`
   - size: `810965` bytes
   - SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`
   - status: authoritative calibration evidence archive.

2. `dukascopy-trading-breaks-widget-2020-02-17-headed-browser.zip`
   - artifact ID: `10356971957`
   - run: `34865846126`
   - size: `709841` bytes
   - SHA-256: `aaf5341f3d7e10b60cc24622d6f16c2ffa3e3f31d6b108f69f53c6f3a2d48849`
   - status: technical headed-browser predecessor retained for auditability; **non-authoritative** for date promotion.

3. `dukascopy-trading-breaks-widget-pilot-2021-09-06-authoritative.zip`
   - artifact ID: `10357256669`
   - run: `34866699952`
   - size: `797338` bytes
   - SHA-256: `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`
   - status: authoritative pilot PASS-A evidence archive.

Workstation placement is intentionally a separate local action. It must be performed by the versioned helper:

`tools/archive_local_trading_breaks_evidence.ps1`

The helper:

- reads the three exact filenames from the user's Downloads directory by default;
- verifies SHA-256 **before** moving anything;
- refuses mismatched or conflicting files;
- stores them under the canonical `raw-zips\` path;
- regenerates `manifest-sha256.csv` with filename, size, relative path, timestamp, SHA-256, role, artifact ID and workflow run.

This preserves a clean separation between Git-tracked governance/provenance and opaque local binary evidence.

## Boundary matrix

- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`
- `REAL_BACKTEST = BLOCKED`

## Important remaining limitation

The calibrated route is qualified for **positive historical break recovery**.

Empty/no-record responses are NOT qualified as proof of normal trading hours. They must remain non-evidence unless a separate negative-evidence/completeness contract is formally qualified.

## Exactly one next governed action

**Formalize and adversarially qualify a systematic historical Trading Breaks recovery protocol before applying the route across the remaining 66 unresolved in-window candidates.**

The protocol must preserve:

- frozen candidate window and deterministic ordering;
- exact-date addressing;
- explicit `USATECH.IDX/USD` / instrument ID mapping;
- raw network payload and rendered evidence capture;
- calibrated end-time semantics;
- independent date-level PASS only from positive exact broker records;
- no upgrade from empty/no-record responses;
- reproducible artifact identity/hash/run provenance;
- no window movement based on recovery outcomes.

No `.bi5`. No real backtest.
