# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — TRADING BREAKS HISTORICAL ROUTE QUALIFIED

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Historical Trading Breaks route:** PASS for positive exact historical break recovery
- **Global calendar:** `111 candidates / 25 resolved / 86 unresolved / 0 FAIL`
- **Candidate window:** `68 candidates / 2 resolved / 66 unresolved / 0 FAIL`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized
- **Latest verified calendar/boundary regression:** `63 PASS`

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-WIDGET-ROUTE-PASS.md`
4. `04-REFERENCE/HISTORICAL-BROKER-EVIDENCE-ROUTE-QUALIFICATION.md`
5. `reports/data-qualification/historical_trading_breaks_widget_calibration_2020_02_17.md`
6. `reports/data-qualification/historical_trading_breaks_widget_pilot_2021_09_06.md`
7. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
8. `LOCAL-EVIDENCE/README.md`
9. `04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md`
10. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
11. compare active branch against this checkpoint final HEAD before writing anything.

Do not reconstruct the 2019–2026 annual work from chat history.

Do not repeat generic holiday searches already exhausted.

## 3. LOCKED WINDOW STATE

Window-selection rule:

`EXECUTION_WINDOW_SELECTION_RULE_V1`

Rule verdict:

**PASS — `WINDOW_SELECTION_RATIONALE_IS_VERSIONED_AND_GAP_INDEPENDENT`**

Mechanically selected candidate:

`2021-08-14` → `2026-08-14`

Current in-window accounting:

- candidates: **68**
- resolved: **2**
- unresolved/BLOCKED: **66**
- FAIL: **0**

Resolved in-window dates:

1. `2021-09-06 — LABOR_DAY`
2. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

The window MUST NOT be shifted, shortened or extended because evidence recovery is difficult.

## 4. HISTORICAL BROKER-EVIDENCE ROUTE — PASS

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

Final verdict:

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

The official Dukascopy Trading Breaks runtime is qualified for **positive historical special-session recovery** when a broker-native exact record exists.

### Gold-standard calibration

Date:

`2020-02-17 — PRESIDENTS_DAY`

Verdict:

**PASS — `HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS`**

Authoritative execution:

- workflow run: `34866241511`
- artifact ID: `10356927580`
- artifact SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`
- instrument: `USATECH.IDX/USD` / ID `9016`
- break: `18:00Z` → final closed minute `22:59Z`
- derived reopen: `23:00Z`

Calibrated representation rule:

`reopen = break_end_last_closed_minute + 60 seconds`

### First unresolved pilot

Date:

`2021-09-06 — LABOR_DAY`

Selection:

`EARLIEST_UNRESOLVED_IN_FROZEN_EXECUTION_WINDOW_CANDIDATE`

Verdict:

**PASS — `EXACT_PRIMARY_BROKER_USATECH_HISTORICAL_BREAK_WITNESS_RECOVERED`**

Date-level gate:

**PASS-A**

Authoritative execution:

- workflow run: `34866699952`
- job ID: `104052206522`
- artifact ID: `10357256669`
- artifact SHA-256: `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`
- break: `17:00Z` → final closed minute `21:59Z`
- derived reopen: `22:00Z`
- fully closed UTC hours: `17,18,19,20,21`

## 5. EXECUTABLE INTEGRATION

The executable calendar now includes exactly one newly recovered pilot record:

`2021-09-06 — SPECIAL_LABOR_DAY_2021`

Dedicated regression test:

`tests/test_dukascopy_usatech_calendar_2021_labor_day.py`

No other unresolved date was upgraded merely because the route passed.

## 6. REGRESSION STATUS

Initial post-integration regression:

- run ID: `34867320843`
- verdict: **FAIL**

Cause:

Two tests used `2018-09-03` as an unresolved witness even though that date was already qualified. This was a stale test fixture, not an executable calendar defect.

Correction:

- fixture changed only to genuinely unresolved `2021-11-25 — THANKSGIVING_DAY`;
- gate logic unchanged;
- commit: `ccb1f9fd6dd7eb5773564ca1759cfc6eb63522b4`.

Corrected regression:

- run ID: `34869158505`
- verdict: **PASS**
- pytest: **63 passed**
- global coverage assertions: PASS
- resulting counts: `111 candidates / 25 resolved / 86 unresolved`
- orphan evidence: 0
- contradictions: 0
- evidence-shape errors: 0

## 7. LOCAL RUNTIME EVIDENCE ARCHIVE

Repository policy:

`LOCAL-EVIDENCE/README.md`

Canonical workstation path:

`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM\LOCAL-EVIDENCE\dukascopy-trading-breaks-widget\2026-09-14\`

Raw ZIP destination:

`raw-zips\`

Rules:

- raw ZIP files remain local and are ignored by Git;
- a `manifest-sha256.csv` beside `raw-zips` records filename, size, relative path, timestamp and SHA-256;
- known calibration and pilot artifact identities/hashes are recorded in `LOCAL-EVIDENCE/README.md`;
- any third/local archive must be hashed in the manifest before durable use.

## 8. CURRENT BOUNDARY MATRIX

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST = BLOCKED — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 9. IMPORTANT NEGATIVE-EVIDENCE BOUNDARY

The Trading Breaks route is qualified only for **positive historical break records**.

An empty/no-record response does NOT prove normal trading hours and MUST NOT be promoted to `NO_SPECIAL_CHANGE_EVIDENCE` until a separate completeness/negative-evidence contract is qualified.

## 10. WHAT MUST NOT BE REPEATED

- do not reopen all 66 dates manually;
- do not repeat generic date-by-date searches already exhausted;
- do not use JForex offline domains for weekday holiday reconstruction;
- do not infer from empty widget/API responses;
- do not convert exchange-only timing into Dukascopy truth;
- do not use other-year or adjacent-date evidence;
- do not move the execution window;
- do not download `.bi5`;
- do not start a real backtest.

## 11. EXACTLY ONE NEXT GOVERNED ACTION

**Formalize and adversarially qualify a systematic historical Trading Breaks recovery protocol before applying the qualified route across the remaining 66 unresolved in-window candidates.**

Required protocol properties:

1. frozen candidate scope and deterministic ordering;
2. exact-date historical addressing;
3. explicit `USATECH.IDX/USD` / ID `9016` identity;
4. raw broker-native network payload capture;
5. DOM or equivalent rendered cross-check where available;
6. calibrated end-time semantics;
7. independent positive-record date-level PASS only;
8. no inference from empty/no-record responses;
9. deterministic workflow/run/artifact/hash provenance;
10. no execution-window movement based on outcomes;
11. calendar integration only after date-level evidence PASS;
12. regression and coverage audit after executable changes.

No `.bi5`. No real backtest.
