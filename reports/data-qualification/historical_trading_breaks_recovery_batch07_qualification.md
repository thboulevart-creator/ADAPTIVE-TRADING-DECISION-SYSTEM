# HISTORICAL TRADING BREAKS RECOVERY — BATCH 07 QUALIFICATION

**PASS — `BATCH07_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

## Authoritative runtime provenance

- workflow run: `34958083459`
- job: `104344855871`
- probe commit: `3d434dda9bd293d48cbe2f35df3d464abd5938a4`
- artifact: `10392510730`
- artifact SHA-256: `0df18b4bfcae04c0bf5e3670e789fc1253fde7317a50d108b35e10dd1cc2676a`
- instrument: `USATECH.IDX/USD` / `9016`
- replay scope: immutable frozen Batch 07 membership

## Independent date-level adjudication

### 2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `63023`
- broker reason: `Christmas Day`
- start: `2023-12-22T21:14:00Z`
- final closed minute: `2023-12-25T22:59:00Z`
- calibrated reopen: `2023-12-25T23:00:00Z`
- fully closed UTC hours: `[22, 23]`
- DOM witness: `True`

### 2023-12-25 — CHRISTMAS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlap broker record: `63023`
- cross-date overlap is retained only as a blocker witness and is not promoted as exact-target evidence.

### 2024-01-01 — NEW_YEARS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlap broker record: `63024`
- cross-date overlap is retained only as a blocker witness and is not promoted as exact-target evidence.

### 2024-01-15 — MARTIN_LUTHER_KING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `63883`
- broker reason: `Martin Luther King Jr. Day`
- start: `2024-01-15T18:00:00Z`
- final closed minute: `2024-01-15T22:59:00Z`
- calibrated reopen: `2024-01-15T23:00:00Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22]`
- DOM witness: `True`

### 2024-02-19 — PRESIDENTS_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `65120`
- broker reason: `Presidents's Day`
- start: `2024-02-19T18:00:00Z`
- final closed minute: `2024-02-19T22:59:59Z`
- calibrated reopen: `2024-02-19T23:00:59Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22]`
- DOM witness: `True`

## Final accounting

- attempted: `5`
- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

This adjudication does not mutate calendar evidence, attempt ledger, progression state, or capability registry.
No `.bi5` acquisition and no real backtest are authorized by this report.
