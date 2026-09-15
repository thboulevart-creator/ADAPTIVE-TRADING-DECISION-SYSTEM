# HISTORICAL TRADING BREAKS RECOVERY — BATCH 12 INDEPENDENT ADJUDICATION

**PASS — `BATCH12_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

## Authoritative runtime provenance

- workflow run: `35016454761`
- job: `104540999314`
- probe commit: `2c2fd6e2db2e0ab75a6b978d6cddad679dbda5b8`
- artifact: `10416410006`
- artifact SHA-256: `6649d976bb9d586cce591cd9b9a9e0e71ed8e5496a1e47e2e52bbdaa2de0297d`
- instrument: `USATECH.IDX/USD` / `9016`
- replay scope: immutable `batch12_targets()`
- browser/network acquisition during adjudication: `NONE`

## Independent date-level adjudication

### 2025-11-27 — THANKSGIVING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `87363`
- broker reason: `Thanksgiving Day`
- start: `2025-11-27T17:59:59Z`
- final closed minute: `2025-11-27T22:59:59Z`
- calibrated reopen: `2025-11-27T23:00:59Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22]`
- DOM witness: `True`

### 2025-11-28 — THANKSGIVING_FRIDAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `87364`
- broker reason: `Thanksgiving Day`
- start: `2025-11-28T18:14:59Z`
- final closed minute: `2025-11-30T22:59:59Z`
- calibrated reopen: `2025-11-30T23:00:59Z`
- fully closed UTC hours: `[19, 20, 21, 22, 23]`
- DOM witness: `True`

### 2025-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `91078`
- broker reason: `Christmas Day`
- start: `2025-12-24T18:14:59Z`
- final closed minute: `2025-12-25T22:59:59Z`
- calibrated reopen: `2025-12-25T23:00:59Z`
- fully closed UTC hours: `[19, 20, 21, 22, 23]`
- DOM witness: `True`

### 2025-12-25 — CHRISTMAS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- broker/overlap record: `91078`
- capture verdict: `CAPTURED`
- capture reason: `POSITIVE_RECORD_CAPTURED_PENDING_ARTIFACT_PROVENANCE_ADJUDICATION`
- no blocked/cross-date capture is promoted into executable date evidence.

### 2025-12-31 — NEW_YEARS_EVE_CANDIDATE

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `92491`
- broker reason: `New Year's Day`
- start: `2025-12-31T21:14:59Z`
- final closed minute: `2026-01-01T22:59:59Z`
- calibrated reopen: `2026-01-01T23:00:59Z`
- fully closed UTC hours: `[22, 23]`
- DOM witness: `True`

## Final accounting

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

This adjudicator is evidence-only. It does not mutate calendar evidence, the attempt ledger, progression state, the capability registry, or execution-window state.
