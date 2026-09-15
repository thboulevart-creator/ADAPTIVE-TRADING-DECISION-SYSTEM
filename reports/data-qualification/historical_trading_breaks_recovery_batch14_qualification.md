# HISTORICAL TRADING BREAKS RECOVERY — BATCH 14 TERMINAL INDEPENDENT ADJUDICATION

**PASS — `BATCH14_TERMINAL_RECORDS_INDEPENDENTLY_ADJUDICATED`**

## Authoritative runtime provenance

- workflow run: `35023845609`
- job: `104565948108`
- probe commit: `4194108c6c9e2c0308209b31cfa64ba8fb3b9f2b`
- artifact: `10418961548`
- artifact SHA-256: `00dd2044a76d926417779d22c7ce08b67318a9d00933b9cac1bc980f2a7c9910`
- browser/network acquisition during adjudication: `NONE`

## Independent date-level adjudication

### 2026-06-19 — JUNETEENTH_OBSERVED

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `101094`
- broker reason: `Juneteenth Holiday`
- start: `2026-06-19T16:59:59Z`
- final closed minute: `2026-06-21T21:59:59Z`
- calibrated reopen: `2026-06-21T22:00:59Z`
- fully closed UTC hours: `[17, 18, 19, 20, 21, 22, 23]`

### 2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION

**BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`**

- capture verdict: `BLOCKED`
- broker record: `None`
- unresolved evidence is retained and is not promoted into executable calendar evidence.

### 2026-07-03 — INDEPENDENCE_DAY_OBSERVED

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `101959`
- broker reason: `Independence Day`
- start: `2026-07-03T16:59:59Z`
- final closed minute: `2026-07-05T21:59:59Z`
- calibrated reopen: `2026-07-05T22:00:59Z`
- fully closed UTC hours: `[17, 18, 19, 20, 21, 22, 23]`

## Final accounting

- attempted: `3`
- PASS: `2`
- BLOCKED: `1`
- FAIL: `0`

Evidence-only adjudication: no calendar, ledger, progression, capability, or execution-window mutation.
