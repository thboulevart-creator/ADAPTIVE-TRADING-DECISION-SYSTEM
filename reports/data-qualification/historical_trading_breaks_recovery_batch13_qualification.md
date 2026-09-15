# HISTORICAL TRADING BREAKS RECOVERY — BATCH 13 INDEPENDENT ADJUDICATION

**PASS — `BATCH13_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

## Authoritative runtime provenance

- workflow run: `35020650564`
- job: `104555157264`
- probe commit: `a974275d06ff45b0a78ad6558a6480e25cfe0f73`
- artifact: `10416898441`
- artifact SHA-256: `59c93ab69bb1484fa0578bb8704aea76f15d67765e9a27ec0416c615d83faec8`
- browser/network acquisition during adjudication: `NONE`

## Independent date-level adjudication

### 2026-01-01 — NEW_YEARS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- broker/overlap record: `92491`
- cross-date overlap is retained as evidence but is not promoted into exact target-date evidence.

### 2026-01-19 — MARTIN_LUTHER_KING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `93608`
- broker reason: `Martin Luther King Jr. Day`
- start: `2026-01-19T17:59:59Z`
- final closed minute: `2026-01-19T22:59:59Z`
- calibrated reopen: `2026-01-19T23:00:59Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22]`

### 2026-02-16 — PRESIDENTS_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `94467`
- broker reason: `President's Day`
- start: `2026-02-16T17:59:59Z`
- final closed minute: `2026-02-16T22:59:59Z`
- calibrated reopen: `2026-02-16T23:00:59Z`
- fully closed UTC hours: `[18, 19, 20, 21, 22]`

### 2026-04-03 — GOOD_FRIDAY

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- broker/overlap record: `98541`
- cross-date overlap is retained as evidence but is not promoted into exact target-date evidence.

### 2026-05-25 — MEMORIAL_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `100253`
- broker reason: `Memorial Day`
- start: `2026-05-25T16:59:59Z`
- final closed minute: `2026-05-25T21:59:59Z`
- calibrated reopen: `2026-05-25T22:00:59Z`
- fully closed UTC hours: `[17, 18, 19, 20, 21]`

## Final accounting

- attempted: `5`
- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

Evidence-only adjudication: no calendar, ledger, progression, capability, or execution-window mutation.
