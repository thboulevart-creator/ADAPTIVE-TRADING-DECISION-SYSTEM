# HISTORICAL TRADING BREAKS RECOVERY — BATCH 06 QUALIFICATION

**PASS — `BATCH06_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

## Authoritative runtime provenance

- workflow run: `34954308324`
- job: `104332522379`
- probe commit: `e968db2be1fbfd4d2c419f9dad717ca479b52edd`
- artifact: `10390926878`
- artifact SHA-256: `1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052`
- instrument: `USATECH.IDX/USD` / `9016`
- replay scope: immutable frozen Batch 06 membership

## Independent date-level adjudication

### 2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `56233`
- broker reason: `Independence Day`
- start: `2023-07-03T17:14:00Z`
- final closed minute: `2023-07-04T21:59:00Z`
- calibrated reopen: `2023-07-04T22:00:00Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22, 23]`
- DOM witness: `True`

### 2023-07-04 — INDEPENDENCE_DAY_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlap broker record: `56233`
- cross-date overlap is retained only as a blocker witness and is not promoted as exact-target evidence.

### 2023-09-04 — LABOR_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `57462`
- broker reason: `Labor Day`
- start: `2023-09-04T16:59:00Z`
- final closed minute: `2023-09-04T21:59:00Z`
- calibrated reopen: `2023-09-04T22:00:00Z`
- fully closed UTC hours: `[17, 18, 19, 20, 21]`
- DOM witness: `True`

### 2023-11-23 — THANKSGIVING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `59358`
- broker reason: `Thanksgiving Day`
- start: `2023-11-23T16:59:00Z`
- final closed minute: `2023-11-23T22:59:00Z`
- calibrated reopen: `2023-11-23T23:00:00Z`
- fully closed UTC hours: `[17, 18, 19, 20, 21, 22]`
- DOM witness: `True`

### 2023-11-24 — THANKSGIVING_FRIDAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `59359`
- broker reason: `Thanksgiving Day`
- start: `2023-11-24T17:14:00Z`
- final closed minute: `2023-11-26T22:59:00Z`
- calibrated reopen: `2023-11-26T23:00:00Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22, 23]`
- DOM witness: `True`

## Final accounting

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

No calendar integration is performed by this adjudicator.
