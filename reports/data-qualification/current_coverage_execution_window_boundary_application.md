# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 06 atomic integration + persisted-HEAD re-break PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 46 resolved / 65 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 23 resolved / 45 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Attempt-aware progression: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Recovery Batch 03: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — integrated**
- Recovery Batch 04: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL — atomically integrated + persisted-HEAD re-break PASS**
- Recovery Batch 05: **PASS — 5 PASS / 0 BLOCKED / 0 FAIL — atomically integrated + persisted-HEAD re-break PASS**
- Recovery Batch 06 membership: **PASS — frozen before observation**
- Recovery Batch 06 execution/adjudication: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL**
- Recovery Batch 06 atomic integration: **PASS**
- Recovery Batch 06 persisted-HEAD re-break: **PASS**
- Historical attempt ledger entries: **30**
- Registered material capability changes: **0**
- Attempted BLOCKED / execution-ineligible: **7**
- Execution-eligible unresolved: **38**
- Current semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- Capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- Batch 07 membership: **NOT FROZEN**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 06 immutable membership and final evidence

Frozen membership remained exactly:

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
3. `2023-09-04 — LABOR_DAY`
4. `2023-11-23 — THANKSGIVING_DAY`
5. `2023-11-24 — THANKSGIVING_FRIDAY`

Final independent adjudication remained:

- `2023-07-03`: PASS — record `56233`
- `2023-07-04`: BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`, overlap witness `56233` starts on `2023-07-03`
- `2023-09-04`: PASS — record `57462`
- `2023-11-23`: PASS — record `59358`
- `2023-11-24`: PASS — record `59359`

The cross-date July 4 overlap was never promoted to exact-target evidence.

Execution provenance:

- run: `34954308324`
- job: `104332522379`
- probe commit: `e968db2be1fbfd4d2c419f9dad717ca479b52edd`
- artifact: `10390926878`
- artifact SHA-256: `1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052`
- runtime persistence commit: `b50529991d9af6e27170090bd45b42eb751d0958`

Independent adjudication provenance:

- run: `34954764562`
- job: `104334032049`
- trigger commit: `44bac8e3ebb8c783d02295f052fe17c86c222049`
- adjudication persistence commit: `874f8fe2c809d1f3c1442ba61aaabb4056a03e3d`
- adversarial/regression suite: `114 passed in 0.36s`

## Batch 06 atomic integration — PASS

Authoritative corrected integration:

- workflow run: `34956127849`
- job: `104338497611`
- trigger commit: `0fd09cf0ac2083b32c97dafe090db0e7d5b82999`
- conclusion: **SUCCESS**
- pre-mutation contract/regression suite: `110 passed`
- post-mutation adversarial/regression suite: `206 passed in 0.77s`
- exact worktree accounting assertion: PASS
- no-negative-evidence/no-browser executable-surface guard: PASS
- atomic integration commit: `a2a59baefd7986f65efb4d625acd2c47c085ae31`

Atomic mutation performed:

- added executable calendar evidence only for:
  - `2023-07-03`
  - `2023-09-04`
  - `2023-11-23`
  - `2023-11-24`
- did **not** add `2023-07-04` to executable special-session evidence;
- appended all five factual attempts as sequences `26..30`;
- retained July 4 blocking reason `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`;
- regenerated progression after calendar + ledger mutation;
- registered no material capability change.

The persisted July 4 state is now exactly:

`UNRESOLVED + INELIGIBLE — SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

It remains absent from `SPECIAL_SESSION_EVIDENCE` and no `NO_SPECIAL_CHANGE_EVIDENCE` was created from the overlap.

Integration qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch06_integration_qualification.md`

## Fail-closed corrections before authoritative integration

Two qualification attempts stopped before any persistent state mutation:

1. run `34955611637` / job `104336823027`: the preparer assumed one Batch 05 attempt-count assertion but correctly encountered two legitimate assertions. The rewrite guard was minimally corrected; no calendar/ledger/progression commit occurred.
2. run `34956027482` / job `104338171283`: the simulated integration, regenerated progression, `206` regressions and exact accounting had all passed, but a whole-file lexical browser guard falsely matched tokens present only in generated test-source strings. The guard was minimally scoped to executable integration functions; no calendar/ledger/progression commit occurred.

Neither failed run produced a partial integration.

## Independent persisted-HEAD re-break — PASS

Authoritative re-break:

- workflow run: `34956317590`
- job: `104339111722`
- trigger commit: `3feb9f937bf74202f68642992ca3fe8b363398d9`
- authoritative integration ancestor: `a2a59baefd7986f65efb4d625acd2c47c085ae31`
- only file between atomic integration and re-break trigger: `.github/workflows/trading-breaks-recovery-batch06-persisted-head.yml`
- workflow permissions: `contents: read`
- adversarial/regression suite: **206 passed in 0.83s**
- exact persisted calendar/ledger/progression assertion: **PASS**
- no-browser/no-capture dependency guard: **PASS**
- deterministic progression regeneration followed by `git diff --exit-code`: **PASS**

Persisted state independently proven:

- global: `111 / 46 resolved / 65 unresolved / 0 FAIL`
- execution window: `68 / 23 resolved / 45 unresolved / 0 FAIL`
- attempt ledger: `30`
- material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `7`
- execution-eligible unresolved: `38`

The first currently eligible candidate is `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`. This is only a persisted-state observation; **Batch 07 has not been frozen**.

Persisted-head evidence report:

`reports/data-qualification/historical_trading_breaks_recovery_batch06_persisted_head_rebreak.md`

## Seven unresolved same-capability BLOCKED dates

The following dates remain calendar-unresolved and execution-ineligible under the unchanged capability:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`
- `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`

Each is explicitly `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`.

## Workflow closure

Completed Batch 06 browser execution and adjudication workflows were already manual-only.

Completed Batch 06 persisted-head re-break workflow is now `workflow_dispatch` only:

`6caa402c21a78faccb7ac3897c5b280f4dbdca6a`

Completed Batch 06 atomic integration workflow is now `workflow_dispatch` only:

`da6cff32eae7c8c863753aaff0875aeb0fe42774`

No normal push may silently repeat historical Batch 06 execution, adjudication, atomic integration or persisted-head re-break.

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_EXECUTION_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_EXECUTION_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_PERSISTED_HEAD_REBREAK`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Freeze Batch 07 membership from the freshly persisted post-Batch06 `eligible_recovery_queue()[:5]`, with fixed batch size and immutable membership versioned before any Batch 07 observation.**

This next action must be scheduling/governance only: no browser observation while freezing membership, no outcome-based selection, no raw `recovery_queue()` substitution, no `.bi5`, no real backtest.
