# Historical Trading Breaks Recovery — Batch 01 Qualification

Contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH_POLICY_V1`

Parent protocol: `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Batch provenance

- workflow run: `34885895206`
- job: `104116336235`
- probe commit: `479900e05eebc6e2c29e0f9f3bddfdfc78e78224`
- artifact: `10364872726`
- artifact SHA-256: `95d6d820393a358a5539f7959ffa06d240b344b1182a57b5b4f13bb43cb74a1f`
- workflow conclusion: `SUCCESS`
- target instrument: `USATECH.IDX/USD`
- Dukascopy instrument ID: `9016`

The batch policy and parent-protocol tests passed before the browser probe executed. The five targets were the fixed chronological prefix `recovery_queue()[:5]`.

## Independent date adjudication

### 2021-11-25 — THANKSGIVING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

Observed broker record:

- record ID: `30449`
- start: `2021-11-25T17:59:00Z`
- final closed minute: `2021-11-25T22:59:00Z`
- calibrated reopen: `2021-11-25T23:00:00Z`
- broker reason: `Thanksgiving Day`
- whole closed UTC hours from the broker interval: `18,19,20,21,22`
- raw broker payload retained: yes
- exact DOM witness: `USATECH.IDX/USD — 25-Nov-21 17:59:00 → 25-Nov-21 22:59:00 — Thanksgiving Day`

The network record starts on the exact governed target date, instrument identity is exact, DOM and network agree, and run/artifact/hash/commit provenance is complete.

### 2021-11-26 — THANKSGIVING_FRIDAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

Observed broker record:

- record ID: `30450`
- start: `2021-11-26T18:14:00Z`
- final closed minute: `2021-11-28T22:59:00Z`
- calibrated reopen: `2021-11-28T23:00:00Z`
- broker reason: `Thanksgiving Day`
- whole closed UTC hours on the target date from the broker interval: `19,20,21,22,23`
- raw broker payload retained: yes
- exact DOM witness: `USATECH.IDX/USD — 26-Nov-21 18:14:00 → 28-Nov-21 22:59:00 — Thanksgiving Day`

The positive broker interval begins on the exact target date. For calendar integration, only the *additional special-session* whole-hour closures `19,20,21` are to be inserted: Friday hours `22,23` are already closed by the governed regular weekly-close rule and MUST NOT be reclassified as special-session closures.

### 2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`**

Observed broker record:

- record ID: `31532`
- start: `2021-12-23T21:14:00Z`
- final closed minute: `2021-12-26T22:59:00Z`
- calibrated reopen: `2021-12-26T23:00:00Z`
- broker reason: `Christmas Day`
- whole closed UTC hours on the target date: `22,23`
- raw broker payload retained: yes
- exact DOM witness: `USATECH.IDX/USD — 23-Dec-21 21:14:00 → 26-Dec-21 22:59:00 — Christmas Day`

The network record starts on the exact governed target date and the broker-native DOM cross-check agrees exactly.

### 2021-12-24 — CHRISTMAS_OBSERVED

**BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**

The target request is historically honored and the raw payload contains record `31532`, but that record begins on `2021-12-23`, not on the target date, and no exact `24-Dec-21` DOM witness was recovered.

The existing protocol deliberately rejects neighboring-date substitution. If record `31532` were submitted as a positive exact-date proof for 24 December, `validate_positive_recovery()` would return `FAIL — NETWORK_RECORD_DATE_MISMATCH`. We therefore do **not** promote that neighboring record; the date remains unresolved/BLOCKED and is not integrated.

This distinction preserves the rule: a rejected bypass is not itself evidence that the target date has no special change.

### 2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED

**BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`**

The historical widget loaded the exact requested date with HTTP 200 and the target instrument identity was recovered, but there was no matching positive `USATECH.IDX/USD` Trading Breaks record and no exact DOM witness.

Per the negative-evidence rule, this empty/no-record outcome MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE` and MUST NOT become PASS.

## Batch result

Date-level adjudication:

- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

The three PASS dates may be integrated into executable special-session evidence. The two BLOCKED dates remain in the governed recovery queue.

**PASS — `BATCH01_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

## Required post-adjudication action

Integrate only:

- `2021-11-25`
- `2021-11-26`
- `2021-12-23`

Then rerun calendar/coverage/boundary regression because executable evidence changes. Do not alter the execution window and do not authorize `.bi5` acquisition or real backtest.
