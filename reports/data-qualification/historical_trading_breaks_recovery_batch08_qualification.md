# HISTORICAL TRADING BREAKS RECOVERY — BATCH 08 QUALIFICATION

**PASS — `BATCH08_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**

## Authoritative runtime provenance

- workflow run: `34984538763`
- job: `104433139005`
- probe commit: `5cc4834af2c75de99f6e3427f31ab07b38b42611`
- artifact: `10402433119`
- artifact SHA-256: `644e6d6776792dac03e7cb87a3bd63af0be603c6efe951f44c8911ecd9defadd`
- instrument: `USATECH.IDX/USD` / `9016`
- replay scope: immutable frozen Batch 08 membership

## Independent date-level adjudication

### 2024-03-29 — GOOD_FRIDAY

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

- overlap broker record: `66555`
- capture reason: `EXPECTED_DOM_CROSSCHECK_MISSING`
- cross-date overlap is retained only as a blocker witness and is not promoted as exact-target evidence.

### 2024-05-27 — MEMORIAL_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `68242`
- broker reason: `Memorial Day`
- start: `2024-05-27T16:59:59Z`
- final closed minute: `2024-05-27T21:59:59Z`
- calibrated reopen: `2024-05-27T22:00:59Z`
- fully closed UTC hours: `[17, 18, 19, 20, 21]`
- DOM witness: `True`

### 2024-06-19 — JUNETEENTH_OBSERVED

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `69037`
- broker reason: `Juneteenth Holiday`
- start: `2024-06-19T17:00:00Z`
- final closed minute: `2024-06-19T21:59:59Z`
- calibrated reopen: `2024-06-19T22:00:59Z`
- fully closed UTC hours: `[17, 18, 19, 20, 21]`
- DOM witness: `True`

### 2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `69819`
- broker reason: `Independence Day`
- start: `2024-07-03T17:14:59Z`
- final closed minute: `2024-07-03T21:59:59Z`
- calibrated reopen: `2024-07-03T22:00:59Z`
- fully closed UTC hours: `[18, 19, 20, 21]`
- DOM witness: `True`

### 2024-07-04 — INDEPENDENCE_DAY_OBSERVED

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `69820`
- broker reason: `Independence Day`
- start: `2024-07-04T16:59:59Z`
- final closed minute: `2024-07-04T21:59:59Z`
- calibrated reopen: `2024-07-04T22:00:59Z`
- fully closed UTC hours: `[17, 18, 19, 20, 21]`
- DOM witness: `True`

## Final accounting

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

No calendar, attempt-ledger, capability-registry or progression mutation is performed by this adjudicator.
