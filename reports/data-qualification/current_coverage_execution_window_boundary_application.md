# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 07 membership qualification PASS

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
- Recovery Batch 04: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL — integrated + persisted-HEAD re-break PASS**
- Recovery Batch 05: **PASS — 5 PASS / 0 BLOCKED / 0 FAIL — integrated + persisted-HEAD re-break PASS**
- Recovery Batch 06: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL — integrated + persisted-HEAD re-break PASS**
- Recovery Batch 07 membership: **PASS — frozen before observation**
- Historical attempt ledger entries: **30**
- Registered material capability changes: **0**
- Attempted BLOCKED / execution-ineligible: **7**
- Execution-eligible unresolved: **38**
- Current semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- Capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 06 closed persisted state

Authoritative Batch 06 atomic integration:

- run: `34956127849`
- job: `104338497611`
- atomic commit: `a2a59baefd7986f65efb4d625acd2c47c085ae31`
- post-mutation regression: `206 passed in 0.77s`

Independent persisted-HEAD re-break:

- run: `34956317590`
- job: `104339111722`
- trigger commit: `3feb9f937bf74202f68642992ca3fe8b363398d9`
- regression: `206 passed in 0.83s`
- deterministic progression regeneration + `git diff --exit-code`: PASS

Persisted state independently proven:

- global: `111 / 46 resolved / 65 unresolved / 0 FAIL`
- execution window: `68 / 23 resolved / 45 unresolved / 0 FAIL`
- attempt ledger: `30`
- material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `7`
- execution-eligible unresolved: `38`

## Batch 07 immutable membership — PASS

Policy contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_POLICY_V1`

Selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

Frozen size:

`BATCH_SIZE = 5`

Authoritative frozen membership:

1. `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`
2. `2023-12-25 — CHRISTMAS_OBSERVED`
3. `2024-01-01 — NEW_YEARS_OBSERVED`
4. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
5. `2024-02-19 — PRESIDENTS_DAY`

The membership was mechanically derived from persisted post-Batch06:

`eligible_recovery_queue()[:5]`

before any Batch 07 observation.

Freeze provenance:

- pre-freeze checkpoint HEAD: `16c6288158985bb3ad68360401b6bdae60687e15`
- source progression-state commit: `a2a59baefd7986f65efb4d625acd2c47c085ae31`
- source independent persisted-head re-break trigger: `3feb9f937bf74202f68642992ca3fe8b363398d9`

Authoritative adversarial qualification:

- run: `34957479365`
- job: `104342908504`
- trigger commit: `2b3a2698f385b6c96003da61e1e59737ab48f3f2`
- adversarial/regression suite: `98 passed in 0.26s`
- exact governed eligible-prefix assertion: PASS
- parent-state immutability since pre-freeze checkpoint: PASS
- no-browser/no-probe/no-live-selection assertion: PASS
- read-only `git diff --exit-code`: PASS

Final verdict:

**PASS — `BATCH07_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch07_policy_qualification.md`

Policy:

`04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH07-POLICY.md`

Frozen membership implementation:

`tools/trading_breaks_recovery_batch07.py`

Adversarial tests:

`tests/test_trading_breaks_recovery_batch07.py`

## Adversarial boundaries proven

Batch 07 qualification rejects:

- raw `recovery_queue()` substitution;
- skip of the first governed eligible member;
- reorder;
- substitution with a later eligible candidate;
- batch shortening or expansion;
- reinsertion of same-capability attempted BLOCKED dates;
- reintroduction of already-resolved Batch 06 PASS dates;
- prior-attempt contamination;
- duplicate or non-chronological membership;
- caller-supplied selection arguments;
- caller mutation of returned membership;
- expected-outcome/manual-priority/holiday/source-availability selection surfaces;
- parent calendar/protocol/progression/boundary regression.

The freeze module contains no live `eligible_recovery_queue()` call, raw `recovery_queue()` call, Playwright, Chromium, `probe_candidate`, asyncio or browser/network path.

## State mutation boundary

The Batch 07 membership freeze did not mutate execution evidence or progression state.

Counts remain exactly:

- global: `111 / 46 resolved / 65 unresolved / 0 FAIL`
- execution window: `68 / 23 resolved / 45 unresolved / 0 FAIL`
- ledger: `30`
- material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `7`
- eligible unresolved: `38`

## Seven unresolved same-capability BLOCKED dates

These remain unresolved and execution-ineligible:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`
- `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`

Each remains `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED` under unchanged semantic capability.

## Workflow closure

The completed Batch 07 membership qualification workflow is archived to `workflow_dispatch` only.

No normal push may silently re-freeze or re-qualify Batch 07 membership.

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_POLICY`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Execute exactly the already-frozen Batch 07 membership under the qualified Trading Breaks capture chain, with parent protocol/progression/Batch07 gates PASS before Chromium opens, then independently adjudicate all five results.**

At execution time membership MUST come from `batch07_targets()` / the immutable frozen tuple. It MUST NOT be recalculated from live `eligible_recovery_queue()` or raw `recovery_queue()`.

No `.bi5`. No real backtest.
