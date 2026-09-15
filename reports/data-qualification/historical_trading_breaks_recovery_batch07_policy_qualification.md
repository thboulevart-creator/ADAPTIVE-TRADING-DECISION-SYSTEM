# HISTORICAL TRADING BREAKS RECOVERY — BATCH 07 POLICY QUALIFICATION

## Final verdict

**PASS — `BATCH07_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Batch 07 membership was mechanically derived from the governed persisted post-Batch06 attempt-aware execution state and frozen before any Batch 07 historical broker observation.

## Freeze provenance

- repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- branch: `feat/multi-year-dukascopy-acquisition`
- pre-freeze checkpoint HEAD: `16c6288158985bb3ad68360401b6bdae60687e15`
- source post-Batch06 atomic integration / progression-state commit: `a2a59baefd7986f65efb4d625acd2c47c085ae31`
- independent post-Batch06 persisted-HEAD re-break trigger commit: `3feb9f937bf74202f68642992ca3fe8b363398d9`
- parent progression contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`
- Batch 07 policy contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_POLICY_V1`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

Persisted parent state at freeze:

- calendar unresolved in execution-window candidate: `45`
- historical attempts: `30`
- material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `7`
- execution-eligible unresolved: `38`

## Deterministic selection rule

`BATCH_SIZE = 5`

Selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

The authoritative assertion proved:

`batch07_targets() == eligible_recovery_queue()[:5]`

Raw `recovery_queue()[:5]` is inadmissible because it contains same-capability attempted BLOCKED dates that remain unresolved but execution-ineligible.

## Frozen Batch 07 membership

1. `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`
2. `2023-12-25 — CHRISTMAS_OBSERVED`
3. `2024-01-01 — NEW_YEARS_OBSERVED`
4. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
5. `2024-02-19 — PRESIDENTS_DAY`

All five are unresolved, chronologically ordered, unique, execution-eligible, classified `INITIAL_ATTEMPT`, and absent from the factual attempt ledger before freeze.

The seven same-capability attempted BLOCKED dates remain unresolved but excluded from Batch 07 execution membership:

- `2021-12-24`
- `2021-12-31`
- `2022-04-15`
- `2022-07-01`
- `2022-12-26`
- `2023-01-02`
- `2023-07-04`

Each remains `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED` under the unchanged semantic capability.

## Authoritative adversarial qualification

- workflow run: `34957479365`
- job: `104342908504`
- trigger commit: `2b3a2698f385b6c96003da61e1e59737ab48f3f2`
- conclusion: **SUCCESS**
- adversarial/regression suite: **`98 passed in 0.26s`**
- exact governed eligible-prefix assertion: **PASS**
- governed parent-state immutability since checkpoint `16c6288158985bb3ad68360401b6bdae60687e15`: **PASS**
- no-browser/no-probe/no-live-selection assertion: **PASS**
- read-only `git diff --exit-code`: **PASS**
- workflow token permissions: `contents: read`, `metadata: read`

The suite covers:

- batch-size drift;
- skipping the first eligible member;
- membership reorder;
- substitution with a later eligible member;
- batch shortening or expansion;
- raw-queue substitution;
- reinsertion of attempted BLOCKED dates;
- reintroduction of already-resolved Batch 06 PASS dates;
- chronology/duplicate defects;
- prior-attempt contamination;
- non-initial eligibility;
- caller-supplied selection surfaces;
- mutation of returned membership;
- semantic-capability/progression-state drift;
- expected-outcome/manual-priority/holiday/source-availability selection surfaces;
- parent protocol/progression/calendar/boundary regressions.

No correction was required: the first authoritative adversarial qualification passed all gates.

## Browser boundary

No Playwright or Chromium dependency was installed by the qualification run.

The Batch 07 freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio;
- live `eligible_recovery_queue()` call;
- live `recovery_queue()` call.

Therefore **no Batch 07 historical broker observation occurred during membership freeze or qualification**.

## State mutation boundary

This membership PASS is scheduling/governance only.

It did not:

- resolve any candidate date;
- modify executable calendar evidence;
- append any attempt to the ledger;
- change the semantic capability;
- alter progression runtime;
- change global/window coverage counts;
- freeze the execution window;
- authorize `.bi5` acquisition;
- authorize a real backtest.

Persisted accounting remains:

- global: `111 / 46 resolved / 65 unresolved / 0 FAIL`;
- execution window: `68 / 23 resolved / 45 unresolved / 0 FAIL`;
- attempt ledger: `30`;
- attempted BLOCKED ineligible: `7`;
- execution-eligible unresolved: `38`.

## Exactly one next governed action

**Execute exactly the already-frozen Batch 07 membership under the qualified Trading Breaks capture chain, with parent protocol/progression/Batch07 gates PASS before Chromium opens, then independently adjudicate all five results.**

At execution time, membership MUST come from `batch07_targets()` / the immutable frozen tuple. It MUST NOT be recalculated from live `eligible_recovery_queue()` or raw `recovery_queue()`.

No `.bi5`. No real backtest.
