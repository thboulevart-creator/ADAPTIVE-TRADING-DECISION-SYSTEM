# HISTORICAL TRADING BREAKS RECOVERY — BATCH 02 QUALIFICATION

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02_POLICY_V1`

Parent adjudication boundary:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Final verdict

**PASS — `BATCH02_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

Batch 02 was frozen before outcome observation with `BATCH_SIZE = 5` and immutable membership:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
3. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
4. `2022-02-21 — PRESIDENTS_DAY`
5. `2022-04-15 — GOOD_FRIDAY`

## Authoritative runtime provenance

- workflow run: `34888022168`
- job: `104123381873`
- probe commit: `619a0200a9718827346d3c5458d1c1a290f3e5ce`
- artifact: `10364984459`
- artifact SHA-256: `ecd110649b1049d308171357ff0574aee4a8670c0d4f35c018854d7d3771ceab`
- instrument: `USATECH.IDX/USD`
- Dukascopy instrument ID: `9016`
- runtime conclusion: `SUCCESS`

Versioned compact runtime report:

`reports/data-qualification/historical_trading_breaks_recovery_batch02_runtime.json`

## Independent date-level adjudication

### 2021-12-24 — CHRISTMAS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

The historical query is honored and raw broker payload exists, but the only overlapping USATECH record is record `31532`, which starts on `2021-12-23T21:14:00Z`, not on the target date. The exact-date protocol explicitly rejects promotion of a neighboring-date start as target-date evidence. No exact target-date DOM witness was recovered.

This is not negative evidence and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

### 2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED

**BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`**

The historical date was honored, instrument identity was correct, and raw payload was retained. No positive USATECH break record was returned for the exact target date.

Absence is not proof of regular trading.

### 2022-01-17 — MARTIN_LUTHER_KING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

Broker record `32811`:

- start: `2022-01-17T17:59:00Z`
- final closed minute: `2022-01-17T22:59:00Z`
- calibrated reopen: `2022-01-17T23:00:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- broker reason: `Martin Luther King Day`

The DOM witness matches the exact instrument/date/start/end/reason. Raw payload and full artifact provenance are present.

### 2022-02-21 — PRESIDENTS_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

Broker record `33515`:

- start: `2022-02-21T17:59:00Z`
- final closed minute: `2022-02-21T22:59:00Z`
- calibrated reopen: `2022-02-21T23:00:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- broker reason: `Presidents Day and Washington's Birthday`

The DOM witness matches the exact instrument/date/start/end/reason. Raw payload and full artifact provenance are present.

### 2022-04-15 — GOOD_FRIDAY

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

The only overlapping record is record `34894`, reason `Easter`, beginning on `2022-04-14T20:14:00Z`. Because the protocol requires the positive broker record to begin on the exact target date, this neighboring-date start cannot be promoted as `2022-04-15` proof. No exact target-date DOM witness was recovered.

This outcome remains BLOCKED and MUST NOT be interpreted as negative evidence.

## Batch accounting

- attempted: `5`
- PASS: `2`
- BLOCKED: `3`
- FAIL: `0`

Only the two PASS dates are admissible for executable calendar integration.

The three BLOCKED dates remain unresolved. No absence or neighboring-date overlap is converted to `NO_SPECIAL_CHANGE_EVIDENCE`.

## Integration authorization

Authorized executable evidence additions:

- `2022-01-17 — SPECIAL_MARTIN_LUTHER_KING_DAY_2022`
- `2022-02-21 — SPECIAL_PRESIDENTS_DAY_2022`

Not authorized for integration:

- `2021-12-24`
- `2021-12-31`
- `2022-04-15`

No `.bi5` acquisition and no real backtest are authorized by this qualification.
