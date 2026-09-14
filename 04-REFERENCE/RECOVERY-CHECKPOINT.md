# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY PROTOCOL PASS

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Window frozen:** NO
- **Global calendar:** `111 candidates / 25 resolved / 86 unresolved / 0 FAIL`
- **Candidate window:** `68 candidates / 2 resolved / 66 unresolved / 0 FAIL`
- **Historical Trading Breaks positive-record route:** PASS
- **Systematic Trading Breaks recovery protocol:** PASS
- **Local runtime evidence archive:** COMPLETE / hash-verified on workstation
- **Latest calendar/boundary regression:** `63 PASS`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized

## 2. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-TRADING-BREAKS-RECOVERY-PROTOCOL-PASS.md`
4. `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
5. `reports/data-qualification/historical_trading_breaks_recovery_protocol_qualification.md`
6. `tools/trading_breaks_recovery_protocol.py`
7. `tests/test_trading_breaks_recovery_protocol.py`
8. `04-REFERENCE/HISTORICAL-BROKER-EVIDENCE-ROUTE-QUALIFICATION.md`
9. `reports/data-qualification/historical_trading_breaks_widget_calibration_2020_02_17.md`
10. `reports/data-qualification/historical_trading_breaks_widget_pilot_2021_09_06.md`
11. `LOCAL-EVIDENCE/README.md`
12. `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`
13. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
14. compare active branch against this checkpoint final HEAD before writing anything.

Do not reconstruct the 2019–2026 annual work from chat history.
Do not repeat generic holiday searches already exhausted.

## 3. LOCKED EXECUTION-WINDOW STATE

Window-selection contract:

`EXECUTION_WINDOW_SELECTION_RULE_V1`

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

The window MUST NOT be shifted, shortened or extended because recovery is difficult.

## 4. HISTORICAL BROKER-EVIDENCE ROUTE — PASS

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

Final verdict:

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

Calibration:

`2020-02-17 — PRESIDENTS_DAY`

- run `34866241511`
- artifact `10356927580`
- SHA-256 `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`
- `USATECH.IDX/USD` / ID `9016`
- break `18:00Z` → final closed minute `22:59Z`
- reopen `23:00Z`

First unresolved pilot:

`2021-09-06 — LABOR_DAY`

- PASS-A
- run `34866699952`
- artifact `10357256669`
- SHA-256 `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`
- break `17:00Z` → final closed minute `21:59Z`
- reopen `22:00Z`
- fully closed UTC hours `17,18,19,20,21`

## 5. SYSTEMATIC RECOVERY PROTOCOL — PASS

Protocol:

`04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

Executable validator:

`tools/trading_breaks_recovery_protocol.py`

Adversarial suite:

`tests/test_trading_breaks_recovery_protocol.py`

Workflow:

`.github/workflows/trading-breaks-recovery-protocol.yml`

Observed qualification:

- workflow head: `f699de1c9aa7b5726276f07d40c5fc8543bc9392`
- run: `34880921889`
- job: `104099717727`
- conclusion: **success**
- pytest: **20 passed in 0.05s**
- runtime queue count: **66**
- first queue item: `2021-11-25 — THANKSGIVING_DAY`
- last queue item: `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

Final verdict:

**PASS — `SYSTEMATIC_TRADING_BREAKS_RECOVERY_PROTOCOL_REJECTS_KNOWN_BYPASSES`**

The suite rejects/contains queue drift, out-of-window dates, resolved-date reintroduction, date/instrument mismatch, empty-response promotion, missing raw payload, malformed/negative intervals, adjacent-date evidence, DOM/network contradiction, missing provenance, invalid hashes/commit identity, wrong reopen semantics and partial-hour rounding.

## 6. NEGATIVE-EVIDENCE BOUNDARY

The Trading Breaks route remains qualified only for **positive historical break records**.

Empty/no-record outcomes remain:

`BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

They MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

A separate completeness/negative-evidence contract would be required before absence can prove normal trading.

## 7. LOCAL RUNTIME EVIDENCE ARCHIVE — COMPLETE

Canonical workstation root:

`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM\LOCAL-EVIDENCE\dukascopy-trading-breaks-widget\2026-09-14\`

Governed manifest:

`LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`

All three retained ZIPs were archived locally and independently re-hashed on the workstation after placement under `raw-zips/`.

Observed SHA-256 values:

- calibration authoritative: `F49FB3AA5B66C22127EDA3AC4593A387F6F83D3AB1D1D31EB742D44C49FB6A91`
- headed-browser technical trace: `AAF5341F3D7E10B60CC24622D6F16C2FFA3E3F31D6B108F69F53C6F3A2D48849`
- 2021-09-06 authoritative pilot: `8D8B568E17FD0E8D5D8C448742290313F78614CCD95C915AEF5B978ED7F90DDC`

All three match the governed manifest.

`tools/archive_local_trading_breaks_evidence.ps1` was restored locally from `origin/feat/multi-year-dukascopy-acquisition` after accidental removal.

Workstation verification:

- `Test-Path` → `True`
- local SHA-256 → `F8B5593EBB754A77A80728880B3FEDFD1F3FB750A2FEFAC00B3F4E48C5AF56B7`

Detailed local-verification persistence commit:

`b5b61961fcb4a0b8318ccd033601e8420dee843d`

Raw ZIPs remain local and ignored by Git. GitHub stores the governed manifest and reproducible tooling rather than duplicate binary evidence payloads.

## 8. CURRENT BOUNDARY MATRIX

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL = PASS`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST = BLOCKED — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 9. WHAT MUST NOT BE REPEATED

- do not reopen the 66 dates manually;
- do not repeat generic holiday searches already exhausted;
- do not infer from empty widget/API responses;
- do not convert exchange-only timing into Dukascopy truth;
- do not use other-year or adjacent-date evidence;
- do not move the execution window;
- do not download `.bi5`;
- do not start a real backtest.

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Fix and version the first deterministic recovery-batch policy/size BEFORE observing any new candidate outcomes, then execute that first batch in chronological order under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`.**

Batch size must be selected only for operational/reproducibility reasons and MUST NOT be altered because some dates look easier or harder.

After the batch:

1. adjudicate each date independently;
2. integrate only true positive-record PASS dates;
3. leave no-record outcomes BLOCKED;
4. rerun calendar/boundary regression only if executable evidence changes;
5. persist run/artifact/hash provenance and updated counts.

No `.bi5`. No real backtest.
