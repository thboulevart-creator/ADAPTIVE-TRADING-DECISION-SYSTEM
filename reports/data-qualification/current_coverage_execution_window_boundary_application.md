# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 08 execution + independent adjudication PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 49 resolved / 62 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 26 resolved / 42 unresolved / 0 FAIL**
- Historical Trading Breaks broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Attempt-aware recovery progression: **PASS**
- Historical attempt ledger entries: **35**
- Registered material capability changes: **0**
- Attempted BLOCKED / same-capability execution-ineligible: **9**
- Persisted execution-eligible unresolved: **33 — STALE FOR ANY BATCH 09 SCHEDULING UNTIL BATCH 08 INTEGRATION**
- Current semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- Capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- Batch 08 membership: **FROZEN + ADVERSARIALLY QUALIFIED PASS**
- Batch 08 execution/adjudication: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — NOT YET INTEGRATED**
- Batch 09 membership: **NOT FROZEN**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 07 final closed state

Batch 07 is atomically integrated and independently re-broken from persisted HEAD.

- authoritative integration commit: `616643e2bfd0b8a8ae3f21352554dc32fdbb503d`
- integration run/job: `34962174847` / `104358082938`
- full integration regression: `297 passed in 1.43s`
- persisted-HEAD verifier run/job: `34962331347` / `104358587801`
- persisted regression: `297 passed in 1.47s`
- global persisted state after Batch 07: `111 / 49 resolved / 62 unresolved / 0 FAIL`
- execution window: `68 / 26 resolved / 42 unresolved / 0 FAIL`
- ledger: `35`
- same-capability BLOCKED/ineligible: `9`
- eligible unresolved at that persisted state: `33`

## Batch 08 membership freeze — PASS

Freeze baseline checkpoint:

`2e9e51cea8342c701eec14d8d86aca215c5b7b62`

Mechanically frozen membership:

1. `2024-03-29 — GOOD_FRIDAY`
2. `2024-05-27 — MEMORIAL_DAY`
3. `2024-06-19 — JUNETEENTH_OBSERVED`
4. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
5. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`

Selection rule:

`eligible_recovery_queue()[:5]`

Authoritative membership qualification:

- workflow run: `34967834638`
- job: `104376461078`
- trigger commit: `7e0fc3268d6ec202267ecf71efe69b0e593be4ea`
- full governed adversarial/regression suite: `307 passed in 1.46s`
- exact eligible-prefix assertion: PASS
- all five targets `INITIAL_ATTEMPT`: PASS
- parent governed-state immutability: PASS
- no browser/probe/live-selection/manual-priority path: PASS
- read-only assertion: PASS

## Batch 08 browser execution — PASS

Authoritative execution:

- workflow run: `34984538763`
- job: `104433139005`
- probe/trigger commit: `5cc4834af2c75de99f6e3427f31ab07b38b42611`
- runtime persistence commit: `6136243c2fbe906a242546d3014a6ee78d30beeb`
- artifact: `10402433119`
- artifact SHA-256: `644e6d6776792dac03e7cb87a3bd63af0be603c6efe951f44c8911ecd9defadd`
- pre-Chromium governed regression: `307 passed in 1.47s`
- exact frozen identity gate: PASS
- no-live-membership-recalculation gate: PASS
- Chromium installed only after all pre-browser gates PASS

Execution consumed only `batch08_targets()`; it did not select from a live eligible or raw recovery queue.

## Batch 08 independent adjudication — PASS

Authoritative successful adjudication rerun:

- run: `34985341285`
- job: `104435886156`
- trigger commit: `cb5d281b2097c751066dc08dd591e7384dc14376`
- adversarial/parent suite: `117 passed in 0.40s`
- final evidence persistence commit: `c2c0ae3`
- final accounting: `4 PASS / 1 BLOCKED / 0 FAIL`
- no browser/probe/live-queue path: PASS

Date-level results:

- `2024-03-29 — GOOD_FRIDAY` — **BLOCKED** — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`; overlap record `66555` starts `2024-03-28T20:14:59Z` and is not promoted.
- `2024-05-27 — MEMORIAL_DAY` — **PASS** — record `68242`, exact target-date primary record.
- `2024-06-19 — JUNETEENTH_OBSERVED` — **PASS** — record `69037`, exact target-date primary record.
- `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION` — **PASS** — record `69819`; start `17:14:59Z`, so hour 17 remains partial and only `[18,19,20,21]` are projected fully closed.
- `2024-07-04 — INDEPENDENCE_DAY_OBSERVED` — **PASS** — record `69820`, exact target-date primary record.

The Good Friday overlap is retained only as blocker evidence. It does not authorize any exact-target PASS or any negative calendar evidence.

### Adjudication persistence correction

The first independent adjudication run `34985087276` / job `104435014275` passed all substantive gates, including `117 passed in 0.36s` and exact `4 PASS / 1 BLOCKED / 0 FAIL`, but its final persistence step failed because `git diff --cached --check` detected one blank line at EOF in the generated Markdown report.

No governed calendar/ledger/progression state was mutated. A minimal persistence-only normalization was applied at commit `cb5d281b2097c751066dc08dd591e7384dc14376`, then the entire independent adjudication chain was rerun and passed.

## State mutation boundary — Batch 08 NOT YET INTEGRATED

Batch 08 execution/adjudication has not yet mutated executable calendar evidence or attempt-aware progression.

Therefore the persisted executable state remains mechanically pre-integration:

- global: `111 / 49 resolved / 62 unresolved / 0 FAIL`
- execution window: `68 / 26 resolved / 42 unresolved / 0 FAIL`
- attempt ledger: `35`
- capability changes: `0`
- same-capability attempted BLOCKED/ineligible: `9`
- persisted eligible unresolved: `33`

The five Batch 08 observations are factual execution evidence but are not yet ledger attempts in the persisted progression state. Consequently `33` MUST NOT be used to freeze Batch 09.

## Workflow closure

The following completed Batch 08 workflows are archived to `workflow_dispatch` only:

- `.github/workflows/trading-breaks-recovery-batch08-policy.yml`
- `.github/workflows/trading-breaks-recovery-batch08.yml`
- `.github/workflows/trading-breaks-recovery-batch08-adjudication.yml`

Normal pushes cannot silently re-freeze, re-execute or re-adjudicate Batch 08.

## Current boundary decisions

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_CONTRACT`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_EXECUTION_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_EXECUTION_ADJUDICATION`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_ATOMIC_INTEGRATION — NOT YET EXECUTED`
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Integrate Batch 08 atomically: add only the four independently adjudicated PASS dates to executable calendar evidence, append all five factual Batch 08 attempts to the ledger, keep `2024-03-29` unresolved and make it same-capability BLOCKED/ineligible, regenerate progression, adversarially re-break calendar/coverage/progression, then independently verify the persisted HEAD before any Batch 09 membership freeze.**

Do not recalculate historical Batch 08 membership. No Batch 09 before Batch 08 integration + persisted-HEAD re-break PASS. No `.bi5`. No real backtest.
