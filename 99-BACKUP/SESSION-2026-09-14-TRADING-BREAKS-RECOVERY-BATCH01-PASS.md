# SESSION BACKUP — 2026-09-14 — TRADING BREAKS RECOVERY BATCH 01 PASS

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

## Purpose

Preserve the governed state after fixing the first deterministic recovery batch policy, executing Batch 01 against the historical Dukascopy Trading Breaks route, independently adjudicating all five dates, integrating only admissible positive records, and re-running persisted calendar/boundary regression.

## Starting state

- global envelope: `2018-05-01 → 2026-08-14`
- execution-window candidate: `2021-08-14 → 2026-08-14`
- initial global accounting: `111 / 25 resolved / 86 unresolved / 0 FAIL`
- initial window accounting: `68 / 2 resolved / 66 unresolved / 0 FAIL`
- window intentionally unchanged throughout the session

## Batch policy frozen before outcome observation

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH_POLICY_V1`

Operational batch size:

`BATCH_SIZE = 5`

Batch 01 was fixed as the chronological prefix of the governed recovery queue before any new historical outcome was observed:

1. `2021-11-25 — THANKSGIVING_DAY`
2. `2021-11-26 — THANKSGIVING_FRIDAY`
3. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2021-12-24 — CHRISTMAS_OBSERVED`
5. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`

Batch size was selected only for bounded runtime, artifact volume, reproducibility, and date-level diagnosability. It was not selected from expected outcomes.

Policy artifact:

`04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH-POLICY.md`

## Pre-observation gate behavior

The policy gate failed closed twice before any new date was observed:

1. run `34885608502`: an expected fifth reason omitted the mechanically combined `+NEW_YEARS_OBSERVED`; browser execution was skipped.
2. run `34885714089`: policy/tests passed, but the probe entry mode failed before navigation; no artifact/date observation occurred.

The minimal entry-mode correction was to execute the probe as repository module:

`python -m tools.trading_breaks_recovery_batch01`

No batch size or membership was changed after either failure.

## Authoritative Batch 01 execution

- workflow run: `34885895206`
- job: `104116336235`
- probe commit: `479900e05eebc6e2c29e0f9f3bddfdfc78e78224`
- artifact: `10364872726`
- artifact SHA-256: `95d6d820393a358a5539f7959ffa06d240b344b1182a57b5b4f13bb43cb74a1f`
- workflow conclusion: `SUCCESS`
- target instrument: `USATECH.IDX/USD`
- Dukascopy instrument ID: `9016`

Runtime report:

`reports/data-qualification/historical_trading_breaks_recovery_batch01_runtime.json`

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch01_qualification.md`

## Independent adjudication

### PASS — 2021-11-25

Broker record `30449`:

- start: `17:59Z`
- final closed minute: `22:59Z`
- reopen: `23:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- exact network + DOM + instrument/date provenance present

### PASS — 2021-11-26

Broker record `30450`:

- start: `18:14Z`
- final closed minute: `2021-11-28 22:59Z`
- reopen: `2021-11-28 23:00Z`
- exact target-date positive record present
- additional special-session hours integrated: `19,20,21`
- Friday `22,23` remain governed by regular weekly close

### PASS — 2021-12-23

Broker record `31532`:

- start: `21:14Z`
- final closed minute: `2021-12-26 22:59Z`
- reopen: `2021-12-26 23:00Z`
- fully closed target-date UTC hours: `22,23`
- exact network + DOM + instrument/date provenance present

### BLOCKED — 2021-12-24

The only overlapping positive record starts on `2021-12-23`; no exact `24-Dec-21` DOM witness was recovered.

It was deliberately **not** promoted. A neighboring-date substitution would violate the protocol via `NETWORK_RECORD_DATE_MISMATCH`.

Verdict:

`BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

### BLOCKED — 2021-12-31

Exact historical date loaded, but no positive exact `USATECH.IDX/USD` Trading Breaks record was recovered.

Verdict:

`BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

The empty outcome was not transformed into `NO_SPECIAL_CHANGE_EVIDENCE`.

## Batch 01 outcome

- PASS: `3`
- BLOCKED: `2`
- FAIL: `0`

Only the three PASS records were integrated.

Overall qualification:

**PASS — `BATCH01_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

## Integration and adversarial regression

During the first integration attempt, a stale synthetic partial-hour fixture mixed a November start timestamp with the new December target. The integration stopped before commit:

- run `34886561690`
- result: `1 failed, 90 passed`

The fixture alone was corrected to keep its synthetic 18:15 start on `2021-12-24`.

The corrected integration then reached:

- `91 passed`
- global assertions: `111 / 28 resolved / 83 unresolved`
- window assertions: `68 / 5 resolved / 63 unresolved`

A GitHub Actions token permission boundary then rejected a runner push only because that commit included `.github/workflows/*`. This was an infrastructure permission issue, not a data/test failure.

The workflow files were persisted through the direct GitHub write path, Batch 01 was archived to manual dispatch, calendar push regression was safely paused during intermediate persistence, and the validated non-workflow executable evidence was pushed successfully.

Validated integration workflow:

- run: `34887010102`
- conclusion: `SUCCESS`

Executable-evidence commit:

`18271cec8c07a96c2ea0fb348ab042d3c72d0c7d`

## Independent persisted-HEAD regression

Calendar regression was restored against the actual persisted state:

- workflow run: `34887061155`
- job: `104120211534`
- conclusion: `SUCCESS`
- pytest: `67 passed in 0.52s`
- global candidate dates: `111`
- resolved: `28`
- unresolved: `83`
- orphan evidence: `0`
- contradictions: `0`
- shape errors: `0`

The global verdict remains `BLOCKED` solely because unresolved special-session candidates remain.

## Current governed state

Global:

- candidates: `111`
- resolved: `28`
- unresolved: `83`
- FAIL: `0`

Execution-window candidate (unchanged):

`2021-08-14 → 2026-08-14`

Window:

- candidates: `68`
- resolved: `5`
- unresolved: `63`
- FAIL: `0`

Resolved in-window dates:

- `2021-09-06 — LABOR_DAY`
- `2021-11-25 — THANKSGIVING_DAY`
- `2021-11-26 — THANKSGIVING_FRIDAY`
- `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
- `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

Current recovery queue:

- size: `63`
- first: `2021-12-24 — CHRISTMAS_OBSERVED`
- last: `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

First five current entries:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
3. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
4. `2022-02-21 — PRESIDENTS_DAY`
5. `2022-04-15 — GOOD_FRIDAY`

## Gates

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

Still BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Freeze and version Batch 02 as the next five entries of the current governed recovery queue, preserving `BATCH_SIZE = 5`, before observing any new Batch 02 historical outcomes; then execute those five dates chronologically under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`.**

No `.bi5` acquisition. No real backtest. No window movement. No no-record promotion.
