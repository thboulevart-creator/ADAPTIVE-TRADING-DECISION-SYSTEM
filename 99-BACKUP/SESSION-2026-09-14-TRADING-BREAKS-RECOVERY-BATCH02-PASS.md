# SESSION BACKUP — 2026-09-14 — TRADING BREAKS RECOVERY BATCH 02 PASS

## Scope

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

This session started from verified checkpoint HEAD:

`787ab1e6a3a97b690af86050de26a4eae603da53`

The governed task was exactly one action: freeze/version Batch 02 at size five before observation, then execute the exact five deterministic queue candidates under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`.

## Batch 02 policy frozen before observation

Policy:

`04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH02-POLICY.md`

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02_POLICY_V1`

Batch size:

`BATCH_SIZE = 5`

Immutable membership:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
3. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
4. `2022-02-21 — PRESIDENTS_DAY`
5. `2022-04-15 — GOOD_FRIDAY`

Policy/tool/tests were committed before the browser workflow was allowed to observe outcomes. Pre-browser gates covered the parent protocol, immutable Batch 01 history, and Batch 02 membership/size/queue-prefix rules.

## Authoritative Batch 02 runtime

Workflow:

`.github/workflows/trading-breaks-recovery-batch02.yml`

Probe commit:

`619a0200a9718827346d3c5458d1c1a290f3e5ce`

Observed execution:

- run: `34888022168`
- job: `104123381873`
- conclusion: **SUCCESS**
- artifact: `10364984459`
- artifact SHA-256: `ecd110649b1049d308171357ff0574aee4a8670c0d4f35c018854d7d3771ceab`
- instrument: `USATECH.IDX/USD`
- instrument ID: `9016`
- read-only: true
- market data written: false

Runtime report:

`reports/data-qualification/historical_trading_breaks_recovery_batch02_runtime.json`

The execution workflow was archived to `workflow_dispatch` only after completion so Batch 02 cannot silently rerun due later code changes.

## Independent adjudication

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch02_qualification.md`

Final Batch 02 verdict:

**PASS — `BATCH02_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION`**

Date-level outcomes:

### 2021-12-24 — CHRISTMAS_OBSERVED

**BLOCKED — no exact target-date positive record admissible.**

The returned overlapping record `31532` starts on `2021-12-23T21:14:00Z`, not on the target date. It is not promoted into an exact-date PASS. No exact target-date DOM witness was recovered.

### 2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED

**BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`.**

Historical date addressing, instrument identity and raw payload retention were proven, but no exact positive USATECH break record was recovered. Absence was not converted into negative evidence.

### 2022-01-17 — MARTIN_LUTHER_KING_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`.**

- record: `32811`
- start: `17:59Z`
- final closed minute: `22:59Z`
- reopen: `23:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- DOM/network: concordant

### 2022-02-21 — PRESIDENTS_DAY

**PASS — `EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED`.**

- record: `33515`
- start: `17:59Z`
- final closed minute: `22:59Z`
- reopen: `23:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- broker reason: `Presidents Day and Washington's Birthday`
- DOM/network: concordant

### 2022-04-15 — GOOD_FRIDAY

**BLOCKED — no exact target-date positive record admissible.**

The overlapping record `34894` starts on `2022-04-14T20:14:00Z`, not on the target date. It is not promoted as exact 2022-04-15 evidence. No negative evidence was inferred.

Batch accounting:

- PASS: `2`
- BLOCKED: `3`
- FAIL: `0`

## Executable integration

Only the two PASS records were integrated:

- `2022-01-17 — SPECIAL_MARTIN_LUTHER_KING_DAY_2022`
- `2022-02-21 — SPECIAL_PRESIDENTS_DAY_2022`

Persisted executable-evidence commit:

`95c7275e1bb7b4abea611a674568441b2a4c52f7`

The three BLOCKED dates remain absent from `SPECIAL_SESSION_EVIDENCE` and remain unresolved.

Integration workflow validation:

- run: `34888531830`
- job: `104125107659`
- conclusion: **SUCCESS**
- pytest: **98 passed**
- global assertions: `111 / 30 resolved / 81 unresolved`
- in-window assertions: `68 / 7 resolved / 61 unresolved`

The integration workflow was archived to manual-only after successful persistence.

## Independent calendar regression

Workflow run:

`34888592937`

Job:

`104125313335`

Result:

**SUCCESS**

Pytest:

`70 passed in 0.57s`

Assertions:

- global candidates: `111`
- global resolved: `30`
- global unresolved: `81`
- window candidates: `68`
- window resolved: `7`
- window unresolved: `61`
- orphan special evidence: `0`
- contradictory evidence: `0`
- evidence-shape errors: `0`

Calendar regression workflow state commit:

`fd3f669f6bfe10936e97fb7dbd4185183586a71b`

## Current resolved in-window dates

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
6. `2022-02-21 — PRESIDENTS_DAY`
7. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

The fixed execution window remains `2021-08-14 → 2026-08-14` and is not frozen because 61 in-window candidates remain unresolved.

## Critical progression finding exposed by Batch 02

The post-Batch-02 unresolved queue still begins with dates already attempted and left BLOCKED:

- `2021-12-24`
- `2021-12-31`
- `2022-04-15`

This is correct for evidence accounting: **BLOCKED is unresolved**.

However, a future scheduler based naively on `recovery_queue()[:5]` would select these same already-attempted dates repeatedly under the unchanged evidence capability and could indefinitely starve later unresolved candidates.

Therefore calendar unresolved status and execution eligibility must now be separated.

A future progression mechanism MUST NOT solve this by:

- marking attempted BLOCKED dates resolved;
- converting empty/no-exact-record into `NO_SPECIAL_CHANGE_EVIDENCE`;
- hiding or excluding them from coverage accounting;
- shifting the execution window;
- discretionary/manual skipping.

It needs a governed attempt ledger / attempt identity and an explicit retry predicate. A blocked date remains unresolved but is not automatically eligible for identical-route re-execution unless a material route/protocol/runtime capability change justifies a deterministic retry.

## Current gates

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01 = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02 = PASS`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST = BLOCKED — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Accidental branch cleanup

During this session an auxiliary branch `__invalid_noop__` was accidentally created while probing connector write capability. It was not part of the workstream. A temporary, narrowly scoped GitHub Actions cleanup deleted exactly that branch, and the temporary cleanup workflow was then removed. No other branch was modified by this cleanup.

Cleanup-workflow removal commit:

`56a9349249768684e7dca4c73c0feb7a5f9d95c6`

## Exactly one next governed action

**Formalize and adversarially qualify an attempt-aware recovery progression contract before defining Batch 03.**

The contract must:

1. preserve BLOCKED dates as unresolved in calendar/coverage accounting;
2. persist recovery attempt identity including date, route/protocol capability identity and outcome;
3. derive batch execution eligibility deterministically from unresolved candidates minus already-attempted candidates under the unchanged capability;
4. permit retry only through an explicit deterministic predicate tied to a material route/protocol/runtime capability change;
5. reject silent skipping, hidden reclassification, queue starvation, and convenience-based retries;
6. remain independent of expected positive/negative outcome.

Only after that contract is PASS may Batch 03 membership be frozen and observed.

No `.bi5`. No real backtest.
