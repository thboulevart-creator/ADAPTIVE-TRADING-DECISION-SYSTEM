# HISTORICAL TRADING BREAKS RECOVERY — BATCH 04 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Final status

**PASS — `BATCH04_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

This policy freezes Batch 04 membership before any Batch 04 historical observation. The membership contract survived adversarial qualification without opening Chromium or executing a historical broker probe.

## 1. Freeze provenance

Authoritative pre-freeze checkpoint HEAD:

`4d3c5db74ec31215b74799f27cdfe476d513014b`

Source post-Batch03 atomic integration / progression-state commit:

`d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

Current governed progression state at freeze:

- calendar unresolved: `57`
- historical attempts: `15`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `4`
- execution-eligible unresolved: `53`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## 2. Frozen batch size

`BATCH_SIZE = 5`

The operational batch size remains fixed for reproducibility, bounded runtime, bounded artifact volume and independent date-level adjudication. It MUST NOT be changed because of expected outcomes, holiday type, apparent ease, source availability or convenience.

## 3. Deterministic selection rule

Batch 04 membership is exactly the first five entries of the governed attempt-aware execution projection at the freeze state:

`eligible_recovery_queue()[:5]`

Raw `recovery_queue()[:5]` is not an admissible selection source because it includes already-attempted BLOCKED dates that remain unresolved but are execution-ineligible under the unchanged semantic capability.

## 4. Frozen Batch 04 membership

The mechanically derived immutable membership is:

1. `2022-11-24 — THANKSGIVING_DAY`
2. `2022-11-25 — THANKSGIVING_FRIDAY`
3. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2022-12-26 — CHRISTMAS_OBSERVED`
5. `2023-01-02 — NEW_YEARS_OBSERVED`

These identities and their order are frozen before any Batch 04 historical observation. They MUST NOT be inserted, skipped, substituted, expanded, shortened or reordered after outcomes become known.

## 5. Qualified eligibility proof

The authoritative qualification proved that every frozen member:

- equals the corresponding entry of current `eligible_recovery_queue()[:5]`;
- remains unresolved in calendar evidence state;
- is execution-eligible;
- is classified `ELIGIBLE — INITIAL_ATTEMPT`;
- has no prior factual attempt in the authoritative attempt ledger;
- is chronologically ordered and unique.

It also proved that the four same-capability attempted BLOCKED dates remain unresolved but are absent from Batch 04 execution membership:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Their exclusion is scheduling only and MUST NOT resolve, delete or promote them to negative evidence.

## 6. Forbidden selection inputs

Batch 04 membership remains independent of:

- expected PASS/BLOCKED/FAIL outcome;
- expected positive-record probability;
- holiday category/type;
- source availability;
- apparent difficulty;
- convenience;
- manual priority;
- manual skip/substitution;
- caller-supplied membership.

Only governed chronological execution eligibility plus fixed `BATCH_SIZE = 5` is admissible.

## 7. Adversarial qualification result

Authoritative qualification:

- workflow run: `34894947834`
- job: `104146491103`
- trigger commit: `641b0e0369ed5a47c4adb69370e2b166b8088c06`
- conclusion: **SUCCESS**
- adversarial/regression suite: **104 passed in 0.35s**
- exact frozen membership assertion against `eligible_recovery_queue()[:5]`: **PASS**
- no-browser/no-probe execution-path guard: **PASS**

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch04_policy_qualification.md`

The suite covers batch-size drift, eligible-prefix mismatch, raw-queue substitution, reinsertion of attempted BLOCKED dates, chronology drift, duplicates, prior-attempt contamination, non-initial eligibility, caller/manual selection surfaces, mutation of returned membership, semantic-capability drift and outcome/priority/holiday/source-selection surfaces.

## 8. Browser boundary

The qualified Batch 04 freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio.

Therefore no Batch 04 historical broker observation occurred during policy qualification.

The qualification workflow is archived to `workflow_dispatch` only after PASS.

## 9. Downstream boundary

This PASS does not resolve any Batch 04 date and does not authorize executable calendar integration by itself.

The next governed action may execute exactly these five frozen dates under the already-qualified Trading Breaks capture/adjudication chain, provided all parent/progression/Batch04 pre-browser gates pass before Chromium opens.

After observation, all five dates require independent adjudication. Membership MUST NOT be recalculated from the then-current queue.

No `.bi5` acquisition. No real backtest.
