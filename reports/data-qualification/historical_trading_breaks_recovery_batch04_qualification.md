# HISTORICAL TRADING BREAKS RECOVERY — BATCH 04 QUALIFICATION

**PASS — `BATCH04_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

## Authoritative runtime provenance

- workflow run: `34895457466`
- job: `104148201341`
- probe commit: `11a81294720898802e49dd1131a64e20e7e7ae3a`
- artifact: `10369230708`
- artifact SHA-256: `3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc`
- instrument: `USATECH.IDX/USD` / `9016`
- replay scope: immutable frozen Batch 04 membership

## Independent date-level adjudication

### 2022-11-24 — THANKSGIVING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `45119`
- broker reason: `Thanksgiving Day`
- start: `2022-11-24T17:59:00Z`
- final closed minute: `2022-11-24T22:59:00Z`
- calibrated reopen: `2022-11-24T23:00:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- exact DOM witness present: `True`

### 2022-11-25 — THANKSGIVING_FRIDAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `45120`
- broker reason: `Thanksgiving Day`
- start: `2022-11-25T18:14:00Z`
- final closed minute: `2022-11-27T22:59:00Z`
- calibrated reopen: `2022-11-27T23:00:00Z`
- fully closed UTC hours: `19,20,21,22,23`
- exact DOM witness present: `True`

### 2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `46756`
- broker reason: `Christmas Day`
- start: `2022-12-23T21:14:00Z`
- final closed minute: `2022-12-26T22:59:00Z`
- calibrated reopen: `2022-12-26T23:00:00Z`
- fully closed UTC hours: `22,23`
- exact DOM witness present: `True`

### 2022-12-26 — CHRISTMAS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlapping broker record: `46756`
- broker reason: `Christmas Day`
- overlap starts: `2022-12-23T21:14:00Z`
- overlap final closed minute: `2022-12-26T22:59:00Z`
- the record starts on another date and cannot be promoted as exact-target evidence
- this remains unresolved/BLOCKED and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`

### 2023-01-02 — NEW_YEARS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlapping broker record: `48045`
- broker reason: `New Year's Day`
- overlap starts: `2022-12-30T21:14:00Z`
- overlap final closed minute: `2023-01-02T22:59:00Z`
- the record starts on another date and cannot be promoted as exact-target evidence
- this remains unresolved/BLOCKED and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`

## Batch accounting

- attempted: `5`
- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

Only genuine exact-target PASS dates are eligible for later executable calendar integration.
Cross-date overlaps remain BLOCKED and unresolved.
No absence or overlap is negative evidence.

No `.bi5` acquisition and no real backtest are authorized by this qualification.
