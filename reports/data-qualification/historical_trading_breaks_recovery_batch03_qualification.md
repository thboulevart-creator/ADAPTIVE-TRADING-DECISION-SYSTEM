# HISTORICAL TRADING BREAKS RECOVERY — BATCH 03 QUALIFICATION

**PASS — `BATCH03_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

## Frozen membership

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

This membership was frozen before observation from the governed attempt-aware eligible queue and was not recalculated during execution, adjudication, or integration.

## Authoritative browser execution

- workflow run: `34892253133`
- job: `104137558818`
- probe commit: `9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4`
- artifact: `10367930592`
- artifact SHA-256: `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`
- instrument: `USATECH.IDX/USD` / `9016`
- pre-browser gate suite: `84 passed`
- runtime report: `reports/data-qualification/historical_trading_breaks_recovery_batch03_runtime.json`

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

No admissible exact positive broker record was recovered for this target date. It remains unresolved/BLOCKED and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

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

## Adversarial adjudication history

The first independent adjudication run was **not accepted**:

- run: `34892773715`
- job: `104139273746`
- verdict: FAIL during adversarial validation

It exposed a representation defect in the adjudication adapter: the DOM carries the human broker name `USATECH.IDX/USD`, while the network payload carries Dukascopy instrument ID `9016`. The first adapter compared the two representations directly and therefore generated a false `DOM_NETWORK_CONTRADICTION`.

Minimal correction:

1. require the DOM instrument name to match exactly `USATECH.IDX/USD`;
2. only after that validation, normalize it to governed instrument ID `9016` for comparison with the network record;
3. add an adversarial attack proving that an incorrect DOM instrument name is rejected before normalization.

Corrected independent re-break:

- run: `34893116066`
- job: `104140394051`
- conclusion: SUCCESS
- suite: `62 passed`
- adjudication: `4 PASS / 1 BLOCKED / 0 FAIL`
- persisted adjudication commit: `a46e48ee4e4b1828e28418bfca1a0f84fd795b19`

## Adversarial integration history

The first atomic integration run was also **not accepted**:

- run: `34893471211`
- job: `104141565466`
- conclusion: FAIL before any integration commit was pushed

It exposed two issues:

1. one historical Batch 02 regression still asserted the pre-Batch03 current unresolved count `61` instead of the post-integration count `57`;
2. more importantly, historical Batch 03 adjudication was tied to the mutable live `recovery_queue()`. Once PASS dates were integrated and therefore left the unresolved queue, replaying the historical adjudication incorrectly rejected them as no longer eligible.

The second issue was corrected by separating two boundaries:

- live recovery validation still uses the current `recovery_queue()` and therefore cannot make a resolved date eligible again;
- historical replay uses only the immutable frozen Batch 03 scope and validates its uniqueness, chronology, target membership, exact candidate reason, and evidence semantics.

This replay correction is a reproducibility boundary only. It did **not** change the semantic broker evidence capability, did not register a material capability change, and did not trigger a new broker observation.

Final atomic integration:

- run: `34893854678`
- job: `104142824703`
- conclusion: SUCCESS
- regression: `104 passed`
- integration commit: `d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

The same atomic commit integrated only the four PASS dates into executable calendar evidence and recorded all five factual attempts in the attempt ledger. `2022-07-01` remained unresolved/BLOCKED.

## Independent persisted-HEAD re-break

After the integration commit was already persisted, the governed branch was independently re-read and re-broken:

- run: `34893976903`
- job: `104143235284`
- conclusion: SUCCESS
- suite: `104 passed in 0.60s`

Persisted accounting independently confirmed:

- global calendar: `111 / 34 resolved / 77 unresolved / 0 FAIL`
- execution-window candidate: `68 / 11 resolved / 57 unresolved / 0 FAIL`
- attempt ledger: `15`
- attempted BLOCKED / currently ineligible: `4`
- currently execution-eligible unresolved: `53`
- registered material capability changes: `0`
- first currently eligible candidate: `2022-11-24 — THANKSGIVING_DAY`

## Batch accounting and closure

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

The Batch 03 execution, adjudication, atomic integration, persisted-HEAD regression, and membership-policy workflows are archived to `workflow_dispatch` only after PASS.

Only PASS dates were integrated. BLOCKED dates remain unresolved; absence is not negative evidence. The frozen replay interface does not make resolved dates eligible for another recovery execution.

No `.bi5` acquisition and no real backtest are authorized by this qualification.
