# HISTORICAL TRADING BREAKS RECOVERY — BATCH 05 POLICY QUALIFICATION

## Final verdict

**PASS — `BATCH05_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Batch 05 membership was mechanically derived from the governed post-Batch04 attempt-aware execution state and frozen before any historical broker observation.

## Freeze provenance

- repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- branch: `feat/multi-year-dukascopy-acquisition`
- pre-freeze checkpoint HEAD: `601310a55b64233ada9e481d3cb2f11dc20a30d5`
- source post-Batch04 atomic integration / progression-state commit: `6cafa5337f28c5424cbcc25280c690de702061d9`
- parent progression contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`
- Batch 05 policy contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY_V1`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

Persisted parent state at freeze:

- calendar unresolved: `54`
- historical attempts: `20`
- material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `6`
- execution-eligible unresolved: `48`

## Deterministic selection rule

`BATCH_SIZE = 5`

Selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

The authoritative assertion proved:

`batch05_targets() == eligible_recovery_queue()[:5]`

Raw `recovery_queue()[:5]` remains inadmissible because it includes same-capability attempted BLOCKED dates that remain unresolved but execution-ineligible.

## Frozen Batch 05 membership

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

All five are unresolved, chronologically ordered, unique, execution-eligible, classified `INITIAL_ATTEMPT`, and absent from the factual attempt ledger before freeze.

The six same-capability attempted BLOCKED dates remain unresolved but are excluded from Batch 05 execution membership:

- `2021-12-24`
- `2021-12-31`
- `2022-04-15`
- `2022-07-01`
- `2022-12-26`
- `2023-01-02`

Each remains `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED` under the unchanged semantic capability.

## Adversarial qualification

Authoritative GitHub Actions execution:

- workflow run: `34942590738`
- job: `104294478304`
- trigger commit: `71d33ea99b83a03f1ed916f447b95e24b9059b3b`
- conclusion: **SUCCESS**
- adversarial/regression suite: **`94 passed in 0.33s`**
- exact governed eligible-prefix assertion: **PASS**
- no-browser/no-probe execution-path assertion: **PASS**
- workflow token permissions: `contents: read`, `metadata: read`

The adversarial suite covers:

- batch-size drift;
- frozen membership substitution or reorder;
- raw-queue substitution;
- reinsertion of attempted BLOCKED dates;
- chronology/duplicate defects;
- prior-attempt contamination;
- non-initial eligibility;
- caller-supplied selection surfaces;
- mutation of returned membership;
- semantic-capability/progression-state drift;
- expected-outcome/manual-priority/holiday/source-availability selection surfaces;
- parent protocol/progression/calendar/boundary regressions.

## Browser boundary

No Playwright or Chromium dependency was installed by this qualification workflow.

The Batch 05 freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio.

Therefore **no Batch 05 historical broker observation occurred during membership freeze or qualification**.

## State mutation boundary

This membership PASS is scheduling/governance only.

It does not:

- resolve any candidate date;
- modify executable calendar evidence;
- append any attempt to the ledger;
- change the semantic capability;
- change global/window coverage counts;
- freeze the execution window;
- authorize `.bi5` acquisition;
- authorize a real backtest.

Current accounting therefore remains:

- global: `111 / 37 resolved / 74 unresolved / 0 FAIL`;
- execution window: `68 / 14 resolved / 54 unresolved / 0 FAIL`;
- attempt ledger: `20`;
- attempted BLOCKED ineligible: `6`;
- execution-eligible unresolved: `48`.

## Exactly one next governed action

**Execute exactly the already-frozen Batch 05 membership under the qualified Trading Breaks capture chain, with parent protocol/progression/Batch05 gates PASS before Chromium opens, then independently adjudicate all five results.**

At execution time, Batch 05 membership MUST come from the immutable frozen tuple. It MUST NOT be recalculated from the then-current `eligible_recovery_queue()` or raw `recovery_queue()`.

No `.bi5`. No real backtest.
