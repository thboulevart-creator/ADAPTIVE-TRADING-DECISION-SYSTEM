# HISTORICAL TRADING BREAKS RECOVERY — BATCH 03 POLICY QUALIFICATION

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

## Final verdict

**PASS — `BATCH03_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Batch 03 was frozen before any Batch 03 historical broker observation with:

`BATCH_SIZE = 5`

Frozen membership:

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

## Freeze provenance

Pre-freeze checkpoint HEAD:

`d4dab0a10ba6bc782186159899f7b8225e7aab59`

Source corrected progression runtime commit:

`b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`

Current semantic capability:

- ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- calendar unresolved: `61`
- execution eligible: `58`
- registered material capability changes: `0`

## Deterministic membership proof

The final qualification run mechanically asserted:

`batch03_targets() == eligible_recovery_queue()[:5]`

and recovered exactly the five frozen members above.

The raw unresolved prefix is intentionally not the selection source because it still begins with already-attempted BLOCKED dates. The attempt-aware progression layer excludes those dates from execution eligibility without removing them from calendar unresolved accounting.

The following three dates therefore remain unresolved but are not Batch 03 members:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`

## Adversarial coverage

The Batch 03 membership suite rejects or proves against at least:

- batch-size drift;
- membership drift from the governed eligible prefix;
- use of raw `recovery_queue()[:5]`;
- reinsertion of already-attempted BLOCKED dates;
- chronology drift;
- duplicate members;
- members with prior attempt history;
- members whose progression reason is not `INITIAL_ATTEMPT`;
- caller-supplied/manual membership inputs;
- mutation of returned membership;
- expected-outcome / priority / holiday-type selection surfaces;
- mismatch from the qualified progression capability identity.

Parent progression, recovery protocol, Batch 01, Batch 02, calendar coverage and execution-window boundary tests were executed in the same qualification suite.

## First run — guard false positive, not membership failure

Initial workflow run:

- run: `34891254793`
- job: `104134235510`
- trigger commit: `3fa23b7027d722ce474d2a7dc9034a79233e5176`
- membership/regression suite: **84 passed in 0.59s**
- exact frozen membership assertion: **PASS**
- final browser-boundary guard: **FALSE POSITIVE / workflow step failure**

The guard searched for the literal string `playwright install` inside the workflow file while that same literal existed in the guard assertion itself. The failure therefore did not expose browser execution or membership drift. The control was corrected minimally rather than ignored.

## Corrected authoritative re-break

Final workflow run:

- run: `34891341634`
- job: `104134524746`
- trigger commit: `4260fd7c91fe855aeb0ff99c70ceb7458d593993`
- conclusion: **SUCCESS**
- adversarial/regression suite: **84 passed in 0.39s**
- exact frozen membership assertion: **PASS**
- browser/probe execution-path guard: **PASS**

The corrected guard inspected the Batch 03 freeze tool itself and proved absence of:

- `playwright`;
- `probe_candidate`;
- `asyncio`;
- `chromium`.

Therefore no Batch 03 historical observation occurred during policy qualification.

## Boundary after PASS

Batch 03 membership is now historically frozen and must not be changed according to future outcomes.

This PASS authorizes only the next governed step: a separate execution workflow may execute these exact five dates under the already-qualified historical Trading Breaks capture/adjudication chain, with all pre-browser gates preserved.

It does not resolve any of the five dates by itself.

Calendar accounting remains unchanged until actual evidence is observed and independently adjudicated.

No `.bi5` acquisition and no real backtest are authorized by this qualification.
