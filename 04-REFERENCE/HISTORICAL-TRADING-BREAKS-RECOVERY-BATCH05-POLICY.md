# HISTORICAL TRADING BREAKS RECOVERY — BATCH 05 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Final status

**PASS — `BATCH05_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

This policy freezes Batch 05 membership from the persisted post-Batch04 attempt-aware execution state. The membership contract survived adversarial qualification without opening Chromium or executing a historical broker probe.

## 1. Freeze provenance

Authoritative pre-freeze checkpoint HEAD:

`601310a55b64233ada9e481d3cb2f11dc20a30d5`

Source post-Batch04 atomic integration / progression-state commit:

`6cafa5337f28c5424cbcc25280c690de702061d9`

Governed progression state at freeze:

- calendar unresolved: `54`
- historical attempts: `20`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `6`
- execution-eligible unresolved: `48`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## 2. Frozen batch size

`BATCH_SIZE = 5`

The operational batch size remains fixed. It MUST NOT be changed based on expected outcome, holiday type, source availability, apparent difficulty or convenience.

## 3. Deterministic selection rule

Batch 05 membership is exactly:

`eligible_recovery_queue()[:5]`

at the freeze state above.

Raw `recovery_queue()[:5]` is inadmissible because it contains unresolved dates that are execution-ineligible after same-capability BLOCKED attempts.

## 4. Frozen Batch 05 membership

The mechanically derived immutable membership is:

1. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
2. `2023-02-20 — PRESIDENTS_DAY`
3. `2023-04-07 — GOOD_FRIDAY`
4. `2023-05-29 — MEMORIAL_DAY`
5. `2023-06-19 — JUNETEENTH_OBSERVED`

These identities and this order are frozen before any Batch 05 historical observation. They MUST NOT be inserted, skipped, substituted, expanded, shortened or reordered after outcomes become known.

## 5. Qualified eligibility proof

The authoritative qualification proved that each frozen member:

- equals the corresponding entry of persisted post-Batch04 `eligible_recovery_queue()[:5]`;
- remains unresolved in calendar evidence state;
- is execution-eligible;
- is classified `ELIGIBLE — INITIAL_ATTEMPT`;
- has no prior factual attempt in the authoritative attempt ledger;
- is unique and chronologically ordered.

It also proved that all six same-capability attempted BLOCKED dates remain unresolved but excluded from Batch 05 execution membership:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Their exclusion is scheduling only. They remain unresolved calendar gaps.

## 6. Forbidden selection inputs

Batch 05 membership remains independent of:

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

- workflow run: `34942590738`
- job: `104294478304`
- trigger commit: `71d33ea99b83a03f1ed916f447b95e24b9059b3b`
- conclusion: **SUCCESS**
- adversarial/regression suite: **`94 passed in 0.33s`**
- exact frozen membership assertion against `eligible_recovery_queue()[:5]`: **PASS**
- no-browser/no-probe execution-path guard: **PASS**

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch05_policy_qualification.md`

The suite covers batch-size drift, eligible-prefix mismatch, raw-queue substitution, reinsertion of attempted BLOCKED dates, chronology drift, duplicates, prior-attempt contamination, non-initial eligibility, caller/manual selection surfaces, mutation of returned membership, semantic-capability/progression-state drift and outcome/priority/holiday/source-selection surfaces.

## 8. Browser boundary

The qualified Batch 05 freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio.

The workflow installed only pytest; no Playwright/Chromium dependency was installed or opened.

Therefore no Batch 05 historical broker observation occurred during policy qualification.

The qualification workflow is archived to `workflow_dispatch` only after PASS.

## 9. State boundary

This policy PASS changes only scheduling/governance state. It does not resolve any calendar candidate, append an attempt, register a capability change, or alter coverage counts.

Persisted accounting remains:

- global: `111 / 37 resolved / 74 unresolved / 0 FAIL`;
- execution window: `68 / 14 resolved / 54 unresolved / 0 FAIL`;
- attempt ledger: `20`;
- attempted BLOCKED / execution-ineligible: `6`;
- execution-eligible unresolved: `48`.

## 10. Downstream boundary

This PASS does not resolve any Batch 05 date and does not authorize executable calendar integration by itself.

The next governed action may execute exactly these five frozen dates under the already-qualified Trading Breaks capture/adjudication chain, provided all parent/progression/Batch05 pre-browser gates pass before Chromium opens.

At execution time membership MUST come from `batch05_targets()` / the immutable frozen tuple. It MUST NOT be recalculated from live `eligible_recovery_queue()` or raw `recovery_queue()`.

After observation, all five dates require independent adjudication.

No `.bi5` acquisition. No real backtest.
