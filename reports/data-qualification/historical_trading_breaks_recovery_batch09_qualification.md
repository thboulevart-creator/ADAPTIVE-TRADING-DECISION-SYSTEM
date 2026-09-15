# HISTORICAL TRADING BREAKS RECOVERY — BATCH 09 INDEPENDENT ADJUDICATION

**PASS — `BATCH09_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

## Authoritative runtime provenance

- workflow run: `34993614373`
- job: `104464228483`
- probe commit: `0b5dedf6028add27040af112d0bceef76be25827`
- artifact: `10406357435`
- artifact SHA-256: `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`
- instrument: `USATECH.IDX/USD` / `9016`
- replay scope: immutable `batch09_targets()`
- browser/network acquisition during adjudication: `NONE`

## Independent date-level adjudication

### 2024-09-02 — LABOR_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `70878`
- broker reason: `Labor Day`
- start: `2024-09-02T16:59:59Z`
- final closed minute: `2024-09-02T21:59:59Z`
- calibrated reopen: `2024-09-02T22:00:59Z`
- fully closed UTC hours: `[17, 18, 19, 20, 21]`
- DOM witness: `True`

### 2024-11-28 — THANKSGIVING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `72887`
- broker reason: `Thanksgiving Day`
- start: `2024-11-28T17:59:59Z`
- final closed minute: `2024-11-28T22:59:59Z`
- calibrated reopen: `2024-11-28T23:00:59Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22]`
- DOM witness: `True`

### 2024-11-29 — THANKSGIVING_FRIDAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `72888`
- broker reason: `Thanksgiving Day`
- start: `2024-11-29T18:14:59Z`
- final closed minute: `2024-12-01T22:59:59Z`
- calibrated reopen: `2024-12-01T23:00:59Z`
- fully closed UTC hours: `[19, 20, 21, 22, 23]`
- DOM witness: `True`

### 2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `74339`
- broker reason: `Christmas`
- start: `2024-12-24T18:14:59Z`
- final closed minute: `2024-12-25T22:59:59Z`
- calibrated reopen: `2024-12-25T23:00:59Z`
- fully closed UTC hours: `[19, 20, 21, 22, 23]`
- DOM witness: `True`

### 2024-12-25 — CHRISTMAS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- broker/overlap record: `74339`
- capture verdict: `CAPTURED`
- capture reason: `POSITIVE_RECORD_CAPTURED_PENDING_ARTIFACT_PROVENANCE_ADJUDICATION`
- no blocked/cross-date capture is promoted into executable date evidence.

## Final accounting

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

This adjudicator is evidence-only. It does not mutate calendar evidence, the attempt ledger, progression state, the capability registry, or execution-window state.
