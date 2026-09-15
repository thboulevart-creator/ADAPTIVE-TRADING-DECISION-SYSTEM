# HISTORICAL TRADING BREAKS RECOVERY — BATCH 06 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Qualification status

**PASS — `BATCH06_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Authoritative qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch06_policy_qualification.md`

Authoritative corrected qualification:

- workflow run: `34951726033`
- job: `104324020570`
- trigger commit: `6a85c1c4c7d8c38861626b3eb8367274f015d118`
- adversarial/regression suite: `97 passed in 0.35s`
- exact governed eligible-prefix assertion: PASS
- no-browser/no-probe assertion: PASS
- read-only assertion: PASS

Batch 06 membership was mechanically derived from the persisted post-Batch05 attempt-aware execution state and frozen before any historical broker observation.

## 1. Freeze provenance

Authoritative pre-freeze checkpoint HEAD:

`289d7f4432efba4ad2bc1e97d5b23f14f587019e`

Source post-Batch05 atomic integration / progression-state commit:

`99c2f38842a0c4ea66ba6ff90496380986d02e52`

Independent persisted-HEAD re-break source:

`70428e536689793a74420d35c84744b8ad0f2f3d`

Governed progression state at freeze:

- calendar unresolved: `49`
- historical attempts: `25`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `6`
- execution-eligible unresolved: `43`
- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## 2. Frozen batch size

`BATCH_SIZE = 5`

The operational batch size is fixed. It MUST NOT be changed based on expected outcome, holiday type, source availability, apparent difficulty or convenience.

## 3. Deterministic selection rule

Batch 06 membership is exactly:

`eligible_recovery_queue()[:5]`

at the persisted post-Batch05 freeze state above.

Raw `recovery_queue()[:5]` is inadmissible because it contains unresolved dates that are execution-ineligible after same-capability BLOCKED attempts.

The production freeze module does not call either queue live. It stores only the already-derived immutable snapshot.

## 4. Frozen Batch 06 membership

The mechanically derived immutable membership is:

1. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
2. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
3. `2023-09-04 — LABOR_DAY`
4. `2023-11-23 — THANKSGIVING_DAY`
5. `2023-11-24 — THANKSGIVING_FRIDAY`

These identities and this order are frozen before any Batch 06 historical observation. They MUST NOT be inserted, skipped, substituted, expanded, shortened or reordered after outcomes become known.

## 5. Eligibility proof

Qualification proved that every frozen member:

- equals the corresponding entry of persisted post-Batch05 `eligible_recovery_queue()[:5]`;
- remains unresolved in calendar evidence state;
- is execution-eligible;
- is classified `ELIGIBLE — INITIAL_ATTEMPT`;
- has no prior factual attempt in the authoritative attempt ledger;
- is unique and chronologically ordered.

It also proved that all six same-capability attempted BLOCKED dates remain unresolved but excluded from Batch 06 execution membership:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`

Their exclusion is scheduling only. They remain unresolved calendar gaps.

## 6. Adversarial qualification and false-positive correction

The suite rejects:

- raw `recovery_queue()` substitution;
- skipping the first eligible member;
- reordering members;
- substituting a later eligible member;
- shortening or expanding batch cardinality;
- reinserting same-capability attempted BLOCKED dates;
- reintroducing already-resolved Batch 05 PASS dates;
- chronology/duplicate defects;
- prior-attempt contamination;
- caller mutation or caller selection surfaces;
- expected-outcome/manual-priority/holiday/source-availability selection surfaces;
- parent protocol/progression/calendar/boundary regressions.

First run:

- run: `34951530594`
- job: `104323377439`
- trigger commit: `0aec58ccab9222b0e86c401b156a9cb965e1c974`
- result: `96 passed / 1 failed`

The single failure was a guard false positive: it rejected the bare substring `eligible_recovery_queue`, which existed only inside the immutable metadata string `FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE`. No live queue call existed.

Minimal test-only correction:

`3ce94bb8c586fe4472ccf37d2a849f87bd9c03ef`

The corrected guard rejects actual call syntax while preserving the versioned selection-rule metadata. The corrected authoritative run then passed all `97` tests and every explicit gate.

## 7. Browser boundary

The Batch 06 freeze module contains no:

- Playwright;
- Chromium;
- `probe_candidate`;
- asyncio;
- live `eligible_recovery_queue()` call;
- live `recovery_queue()` call;
- browser/network observation path.

The qualification workflow installed pytest only. Therefore **no Batch 06 historical broker observation occurred during membership freeze or qualification**.

## 8. State mutation boundary

This freeze is scheduling/governance only. It did not:

- resolve any calendar candidate;
- modify executable calendar evidence;
- append any factual attempt;
- register any material capability change;
- alter progression runtime;
- alter global/window coverage counts.

Persisted accounting remains:

- global: `111 / 42 resolved / 69 unresolved / 0 FAIL`;
- execution window: `68 / 19 resolved / 49 unresolved / 0 FAIL`;
- attempt ledger: `25`;
- attempted BLOCKED / execution-ineligible: `6`;
- execution-eligible unresolved: `43`.

## 9. Workflow closure

The completed Batch 06 membership qualification workflow is archived to `workflow_dispatch` only.

No normal push may silently re-freeze or re-qualify historical Batch 06 membership.

## 10. Exactly one next governed action

**Execute exactly the already-frozen Batch 06 membership under the qualified Trading Breaks capture chain, with parent protocol/progression/Batch06 gates PASS before Chromium opens, then independently adjudicate all five results.**

At execution time membership MUST come from `batch06_targets()` / the immutable frozen tuple. It MUST NOT be recalculated from live `eligible_recovery_queue()` or raw `recovery_queue()`.

No `.bi5` acquisition. No real backtest.
