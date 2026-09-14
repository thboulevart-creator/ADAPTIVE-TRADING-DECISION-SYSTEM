# HISTORICAL TRADING BREAKS RECOVERY — BATCH 03 QUALIFICATION

**PASS — `BATCH03_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

## Authoritative runtime provenance

- workflow run: `34892253133`
- job: `104137558818`
- probe commit: `9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4`
- artifact: `10367930592`
- artifact SHA-256: `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`
- instrument: `USATECH.IDX/USD` / `9016`
- replay scope: immutable frozen Batch 03 membership (not the current recovery queue)

## Independent date-level adjudication

### 2022-05-30 — MEMORIAL_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `37019`
- broker reason: `Memorial Day`
- start: `2022-05-30T16:59:00Z`
- final closed minute: `2022-05-30T21:59:00Z`
- calibrated reopen: `2022-05-30T22:00:00Z`
- fully closed UTC hours: `17,18,19,20,21`
- exact DOM witness: present and protocol-matched

### 2022-06-20 — JUNETEENTH_OBSERVED

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `38945`
- broker reason: `Juneteenth Holiday`
- start: `2022-06-20T16:59:00Z`
- final closed minute: `2022-06-20T21:59:00Z`
- calibrated reopen: `2022-06-20T22:00:00Z`
- fully closed UTC hours: `17,18,19,20,21`
- exact DOM witness: present and protocol-matched

### 2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION

**BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`**

No admissible exact positive broker record was recovered for this target date.
This remains unresolved/BLOCKED and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

### 2022-07-04 — INDEPENDENCE_DAY_OBSERVED

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `41225`
- broker reason: `Independence Day`
- start: `2022-07-04T16:59:00Z`
- final closed minute: `2022-07-04T21:59:00Z`
- calibrated reopen: `2022-07-04T22:00:00Z`
- fully closed UTC hours: `17,18,19,20,21`
- exact DOM witness: present and protocol-matched

### 2022-09-05 — LABOR_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

- broker record: `42569`
- broker reason: `Labor Day`
- start: `2022-09-05T16:59:00Z`
- final closed minute: `2022-09-05T21:59:00Z`
- calibrated reopen: `2022-09-05T22:00:00Z`
- fully closed UTC hours: `17,18,19,20,21`
- exact DOM witness: present and protocol-matched

## Batch accounting

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

Only PASS dates are authorized for executable calendar integration.
BLOCKED dates remain unresolved; absence is not negative evidence.
The frozen replay interface does not make resolved dates eligible for another recovery execution.

No `.bi5` acquisition and no real backtest are authorized by this qualification.
