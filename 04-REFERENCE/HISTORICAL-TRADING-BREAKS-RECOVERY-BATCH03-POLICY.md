# HISTORICAL TRADING BREAKS RECOVERY — BATCH 03 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Status before adversarial qualification

**CANDIDATE — NOT YET PASS**

This policy freezes Batch 03 membership before any Batch 03 historical observation. No browser execution is authorized until the membership contract has survived adversarial qualification.

## 1. Freeze provenance

Authoritative pre-freeze checkpoint HEAD:

`d4dab0a10ba6bc782186159899f7b8225e7aab59`

Source corrected progression runtime commit:

`b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`

Current semantic capability:

- capability ID: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- unresolved calendar candidates: `61`
- execution-eligible unresolved candidates: `58`
- registered material capability changes: `0`

## 2. Frozen batch size

`BATCH_SIZE = 5`

The size is inherited from the governed operational batch size used by Batch 01 and Batch 02. It is fixed for reproducibility, bounded runtime, bounded artifact volume, and date-level auditability only.

It MUST NOT be changed based on expected outcome, holiday type, apparent ease, source availability, or convenience.

## 3. Deterministic selection rule

Batch 03 membership is exactly:

`eligible_recovery_queue()[:5]`

at the freeze state identified above.

It MUST NOT be derived from raw `recovery_queue()[:5]`.

The attempt-aware progression layer is authoritative for execution eligibility. Calendar unresolved state remains separate and unchanged.

## 4. Frozen Batch 03 membership

The mechanically derived five entries are:

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

After this policy is versioned, these five identities and their order are immutable historical Batch 03 membership.

No date may be inserted, skipped, substituted, or reordered after outcomes become known.

## 5. Explicit exclusion of currently ineligible BLOCKED dates

The following dates remain unresolved calendar candidates but are execution-ineligible under the unchanged semantic capability and therefore MUST NOT enter Batch 03:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`

Their exclusion from Batch 03 is scheduling only. They remain unresolved and MUST NOT be reclassified, hidden from coverage accounting, or promoted to negative evidence.

## 6. Eligibility-state requirement

At freeze time, every Batch 03 member MUST be:

- present in the governed unresolved calendar queue;
- present in `eligible_recovery_queue()`;
- classified by the progression contract as `ELIGIBLE — INITIAL_ATTEMPT`;
- never previously attempted in the authoritative attempt ledger;
- ordered chronologically according to the governed eligible queue.

## 7. No outcome-dependent selection

Membership MUST be independent of:

- expected PASS/BLOCKED/FAIL result;
- holiday category;
- expected positive-record availability;
- apparent difficulty;
- convenience;
- manual preference;
- prior knowledge of likely broker behavior.

Only the governed attempt-aware eligibility queue and fixed batch size are admissible inputs.

## 8. Adversarial qualification obligations before Chromium

Before any Batch 03 browser execution, executable tests MUST reject at least:

1. batch-size drift;
2. membership mismatch from the first five governed eligible candidates at freeze time;
3. use of raw `recovery_queue()[:5]` instead of `eligible_recovery_queue()[:5]`;
4. reinsertion of any already-attempted BLOCKED/ineligible date;
5. chronology drift;
6. duplicate dates;
7. a Batch 03 member with prior attempt history;
8. a Batch 03 member whose progression reason is not `INITIAL_ATTEMPT`;
9. mutable membership returned by caller input or external priority parameters;
10. manual/expected-outcome selection paths;
11. mutation of the frozen Batch 03 membership after policy versioning.

The policy qualification workflow MUST NOT install/open Chromium or call any historical broker endpoint.

## 9. Post-qualification boundary

If the adversarial membership suite PASSes, this policy may be promoted to:

**PASS — `BATCH03_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

Only then may a separate Batch 03 execution workflow be created or run against these exact five dates.

No `.bi5` acquisition and no real backtest are authorized by this policy.
