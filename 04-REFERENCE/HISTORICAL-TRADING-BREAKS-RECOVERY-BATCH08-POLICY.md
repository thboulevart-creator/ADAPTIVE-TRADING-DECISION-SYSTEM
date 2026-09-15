# HISTORICAL TRADING BREAKS RECOVERY — BATCH 08 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Qualification status

**PASS — `BATCH08_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Authoritative qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch08_policy_qualification.md`

Authoritative qualification:

- workflow run: `34967834638`
- job: `104376461078`
- trigger commit: `7e0fc3268d6ec202267ecf71efe69b0e593be4ea`
- adversarial/regression suite: `307 passed in 1.46s`
- exact governed eligible-prefix assertion: PASS
- all frozen members `INITIAL_ATTEMPT`: PASS
- governed parent-state immutability: PASS
- no-browser/no-probe/no-live-selection assertion: PASS
- read-only assertion: PASS

Batch 08 membership was mechanically derived from the persisted post-Batch07 attempt-aware execution state and frozen before any historical broker observation.

## 1. Freeze provenance

Authoritative pre-freeze checkpoint HEAD:

`2e9e51cea8342c701eec14d8d86aca215c5b7b62`

Source post-Batch07 atomic integration / progression-state commit:

`616643e2bfd0b8a8ae3f21352554dc32fdbb503d`

Independent post-Batch07 persisted-HEAD re-break trigger commit:

`b4a2f3400b0629e7b1d0a715320735f74293b15a`

Governed progression state at freeze:

- calendar unresolved: `42`
- historical attempts: `35`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `9`
- execution-eligible unresolved: `33`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## 2. Frozen batch size

`BATCH_SIZE = 5`

The operational batch size is fixed. It MUST NOT be changed based on expected outcome, holiday type, source availability, apparent difficulty or convenience.

## 3. Deterministic selection rule

Batch 08 membership is exactly:

`eligible_recovery_queue()[:5]`

at the persisted post-Batch07 freeze state above.

Raw `recovery_queue()[:5]` is inadmissible because it contains unresolved dates that are execution-ineligible after same-capability BLOCKED attempts.

The production freeze module does not call either queue live. It stores only the already-derived immutable snapshot.

## 4. Frozen Batch 08 membership

The mechanically derived immutable membership is:

1. `2024-03-29 — GOOD_FRIDAY`
2. `2024-05-27 — MEMORIAL_DAY`
3. `2024-06-19 — JUNETEENTH_OBSERVED`
4. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
5. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`

These identities and this order are frozen before any Batch 08 historical observation. They MUST NOT be inserted, skipped, substituted, expanded, shortened or reordered after outcomes become known.

## 5. Eligibility proof

Qualification proved that every frozen member:

- equals the corresponding entry of persisted post-Batch07 `eligible_recovery_queue()[:5]`;
- remains unresolved in calendar evidence state;
- is execution-eligible;
- is classified `ELIGIBLE — INITIAL_ATTEMPT`;
- has no prior factual attempt in the authoritative attempt ledger;
- is unique and chronologically ordered.

It also proved that all nine same-capability attempted BLOCKED dates remain unresolved but excluded from Batch 08 execution membership:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`
- `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
- `2023-12-25 — CHRISTMAS_OBSERVED`
- `2024-01-01 — NEW_YEARS_OBSERVED`

Their exclusion is scheduling only. They remain unresolved calendar gaps.

The three Batch 07 PASS dates are already resolved and excluded:

- `2023-12-22`
- `2024-01-15`
- `2024-02-19`

## 6. Adversarial qualification

The suite rejects:

- raw `recovery_queue()` substitution;
- skipping the first eligible member;
- reordering members;
- substituting a later eligible member;
- shortening or expanding batch cardinality;
- reinserting same-capability attempted BLOCKED dates;
- reintroducing already-resolved Batch 07 PASS dates;
- chronology/duplicate defects;
- prior-attempt contamination;
- caller mutation or caller selection surfaces;
- expected-outcome/manual-priority/holiday/source-availability selection surfaces;
- semantic-capability/progression-state drift;
- parent protocol/progression/calendar/coverage regressions.

The first authoritative adversarial qualification passed all `307` tests; no corrective rerun was required.

## 7. Browser boundary

The Batch 08 freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio;
- live `eligible_recovery_queue()` call;
- live `recovery_queue()` call;
- browser/network observation path.

The qualification workflow installed pytest only. Therefore **no Batch 08 historical broker observation occurred during membership freeze or qualification**.

## 8. State mutation boundary

This freeze is scheduling/governance only. It did not:

- resolve any calendar candidate;
- modify executable calendar evidence;
- append any factual attempt;
- register any material capability change;
- alter progression runtime;
- alter global/window coverage counts.

Persisted accounting remains:

- global: `111 / 49 resolved / 62 unresolved / 0 FAIL`;
- execution window: `68 / 26 resolved / 42 unresolved / 0 FAIL`;
- attempt ledger: `35`;
- attempted BLOCKED / execution-ineligible: `9`;
- execution-eligible unresolved: `33`.

## 9. Workflow closure

The completed Batch 08 membership qualification workflow is archived to `workflow_dispatch` only after PASS evidence was persisted.

No normal push may silently re-freeze or re-qualify historical Batch 08 membership.

## 10. Exactly one next governed action

**Execute exactly the already-frozen Batch 08 membership under the qualified Trading Breaks capture chain, with parent protocol/progression/Batch08 gates PASS before Chromium opens, then independently adjudicate all five results.**

At execution time membership MUST come from `batch08_targets()` / the immutable frozen tuple. It MUST NOT be recalculated from live `eligible_recovery_queue()` or raw `recovery_queue()`.

No `.bi5` acquisition. No real backtest.
