# HISTORICAL TRADING BREAKS RECOVERY — BATCH 06 POLICY QUALIFICATION

## Final verdict

**PASS — `BATCH06_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Batch 06 membership was mechanically derived from the governed persisted post-Batch05 attempt-aware execution state and frozen before any historical broker observation.

## Freeze provenance

- repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- branch: `feat/multi-year-dukascopy-acquisition`
- pre-freeze checkpoint HEAD: `289d7f4432efba4ad2bc1e97d5b23f14f587019e`
- source post-Batch05 atomic integration / progression-state commit: `99c2f38842a0c4ea66ba6ff90496380986d02e52`
- independent post-Batch05 persisted-HEAD re-break commit: `70428e536689793a74420d35c84744b8ad0f2f3d`
- parent progression contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`
- Batch 06 policy contract: `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_POLICY_V1`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

Persisted parent state at freeze:

- calendar unresolved in execution-window candidate: `49`
- historical attempts: `25`
- material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `6`
- execution-eligible unresolved: `43`

## Deterministic selection rule

`BATCH_SIZE = 5`

Selection rule:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

The authoritative assertion proved:

`batch06_targets() == eligible_recovery_queue()[:5]`

Raw `recovery_queue()[:5]` remains inadmissible because it contains same-capability attempted BLOCKED dates that remain unresolved but execution-ineligible.

## Frozen Batch 06 membership

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
3. `2023-09-04 — LABOR_DAY`
4. `2023-11-23 — THANKSGIVING_DAY`
5. `2023-11-24 — THANKSGIVING_FRIDAY`

All five are unresolved, chronologically ordered, unique, execution-eligible, classified `INITIAL_ATTEMPT`, and absent from the factual attempt ledger before freeze.

The six same-capability attempted BLOCKED dates remain unresolved but are excluded from Batch 06 execution membership:

- `2021-12-24`
- `2021-12-31`
- `2022-04-15`
- `2022-07-01`
- `2022-12-26`
- `2023-01-02`

Each remains `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED` under the unchanged semantic capability.

## First adversarial execution — guard false positive

Initial qualification:

- workflow run: `34951530594`
- job: `104323377439`
- trigger commit: `0aec58ccab9222b0e86c401b156a9cb965e1c974`
- result: `96 passed / 1 failed`

The only failure was the no-live-selection source guard. It searched for the bare substring `eligible_recovery_queue`, which appears legitimately inside the versioned metadata value:

`FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`

No live call to `eligible_recovery_queue()` or `recovery_queue()` existed in the Batch 06 freeze module. This was therefore a test-guard false positive, not a membership, progression, calendar, ledger or browser-boundary failure.

Minimal correction commit:

`3ce94bb8c586fe4472ccf37d2a849f87bd9c03ef`

The correction changed only the guard to reject actual call syntax (`eligible_recovery_queue(` / `recovery_queue(`) while permitting immutable selection-rule metadata.

## Corrected authoritative adversarial qualification

- workflow run: `34951726033`
- job: `104324020570`
- trigger commit: `6a85c1c4c7d8c38861626b3eb8367274f015d118`
- conclusion: **SUCCESS**
- adversarial/regression suite: **`97 passed in 0.35s`**
- exact governed eligible-prefix assertion: **PASS**
- governed-state immutability since checkpoint `289d7f44...`: **PASS**
- no-browser/no-probe execution-path assertion: **PASS**
- read-only `git diff --exit-code`: **PASS**
- workflow token permissions: `contents: read`, `metadata: read`

The suite covers:

- batch-size drift;
- frozen membership substitution or reorder;
- skipping the first eligible member;
- substitution with a later eligible date;
- batch shortening or expansion;
- raw-queue substitution;
- reinsertion of attempted BLOCKED dates;
- reintroduction of already-resolved Batch 05 PASS dates;
- chronology/duplicate defects;
- prior-attempt contamination;
- non-initial eligibility;
- caller-supplied selection surfaces;
- mutation of returned membership;
- semantic-capability/progression-state drift;
- expected-outcome/manual-priority/holiday/source-availability selection surfaces;
- parent protocol/progression/calendar/boundary regressions.

## Browser boundary

No Playwright or Chromium dependency was installed by either qualification run.

The Batch 06 freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio;
- live `eligible_recovery_queue()` call;
- live `recovery_queue()` call.

Therefore **no Batch 06 historical broker observation occurred during membership freeze or qualification**.

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

- global: `111 / 42 resolved / 69 unresolved / 0 FAIL`;
- execution window: `68 / 19 resolved / 49 unresolved / 0 FAIL`;
- attempt ledger: `25`;
- attempted BLOCKED ineligible: `6`;
- execution-eligible unresolved: `43`.

## Exactly one next governed action

**Execute exactly the already-frozen Batch 06 membership under the qualified Trading Breaks capture chain, with parent protocol/progression/Batch06 gates PASS before Chromium opens, then independently adjudicate all five results.**

At execution time, membership MUST come from `batch06_targets()` / the immutable frozen tuple. It MUST NOT be recalculated from live `eligible_recovery_queue()` or raw `recovery_queue()`.

No `.bi5`. No real backtest.
