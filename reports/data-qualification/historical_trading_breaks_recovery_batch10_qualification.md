# HISTORICAL TRADING BREAKS RECOVERY — BATCH 10 INDEPENDENT ADJUDICATION

**PASS — `BATCH10_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_OR_MISSING_DOM_PROMOTION`**

## Authoritative runtime provenance

- workflow run: `35004172846`
- job: `104499660140`
- probe commit: `443b3696e4e2740a54354787de231c886f90b26e`
- artifact: `10411022092`
- artifact SHA-256: `1572cc5a1c38998f59d32e107b1bcb006a74b288fe32c70ffe019726b3ad5f14`
- instrument: `USATECH.IDX/USD` / `9016`
- replay scope: immutable `batch10_targets()`
- browser/network acquisition during adjudication: `NONE`

## Independent date-level adjudication

### 2024-12-31 — NEW_YEARS_EVE_CANDIDATE

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `75799`
- broker reason: `New Year's Day`
- start: `2024-12-31T21:14:59Z`
- final closed minute: `2025-01-01T22:59:59Z`
- calibrated reopen: `2025-01-01T23:00:59Z`
- fully closed UTC hours: `[22, 23]`
- DOM witness: `True`

### 2025-01-01 — NEW_YEARS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- broker/overlap record: `75799`
- DOM witness: `True`
- capture verdict: `CAPTURED`
- capture reason: `POSITIVE_RECORD_CAPTURED_PENDING_ARTIFACT_PROVENANCE_ADJUDICATION`
- no blocked/cross-date/missing-DOM capture is promoted into executable date evidence.

### 2025-01-20 — MARTIN_LUTHER_KING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `76806`
- broker reason: `Martin Luther King Jr. Day`
- start: `2025-01-20T17:59:59Z`
- final closed minute: `2025-01-20T22:59:59Z`
- calibrated reopen: `2025-01-20T23:00:59Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22]`
- DOM witness: `True`

### 2025-02-17 — PRESIDENTS_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `78513`
- broker reason: `Presidents's Day`
- start: `2025-02-17T17:59:59Z`
- final closed minute: `2025-02-17T22:59:59Z`
- calibrated reopen: `2025-02-17T23:00:59Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22]`
- DOM witness: `True`

### 2025-04-18 — GOOD_FRIDAY

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- broker/overlap record: `80057`
- DOM witness: `False`
- capture verdict: `BLOCKED`
- capture reason: `EXPECTED_DOM_CROSSCHECK_MISSING`
- no blocked/cross-date/missing-DOM capture is promoted into executable date evidence.

## Final accounting

- attempted: `5`
- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

This adjudicator is evidence-only. It does not mutate calendar evidence, the attempt ledger, progression state, the capability registry, or execution-window state.
