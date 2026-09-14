# HISTORICAL TRADING BREAKS RECOVERY — BATCH 03 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_POLICY_V1`

Parent progression contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Final status

**PASS — `BATCH03_MEMBERSHIP_FROZEN_FROM_ATTEMPT_AWARE_ELIGIBLE_QUEUE_BEFORE_OBSERVATION`**

This policy freezes Batch 03 membership before any Batch 03 historical observation. The membership contract survived adversarial qualification without opening Chromium or executing a historical broker probe.

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

These five identities and their order are immutable historical Batch 03 membership.

No date may be inserted, skipped, substituted, or reordered after outcomes become known.

## 5. Explicit exclusion of currently ineligible BLOCKED dates

The following dates remain unresolved calendar candidates but are execution-ineligible under the unchanged semantic capability and therefore MUST NOT enter Batch 03:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`

Their exclusion from Batch 03 is scheduling only. They remain unresolved and MUST NOT be reclassified, hidden from coverage accounting, or promoted to negative evidence.

## 6. Eligibility-state requirement

At freeze time, every Batch 03 member is proven to be:

- present in the governed unresolved calendar queue;
- present in `eligible_recovery_queue()`;
- classified by the progression contract as `ELIGIBLE — INITIAL_ATTEMPT`;
- never previously attempted in the authoritative attempt ledger;
- ordered chronologically according to the governed eligible queue.

## 7. No outcome-dependent selection

Membership is independent of:

- expected PASS/BLOCKED/FAIL result;
- holiday category;
- expected positive-record availability;
- apparent difficulty;
- convenience;
- manual preference;
- prior knowledge of likely broker behavior.

Only the governed attempt-aware eligibility queue and fixed batch size are admissible inputs.

## 8. Adversarial qualification result

Authoritative corrected re-break:

- workflow run: `34891341634`
- job: `104134524746`
- trigger commit: `4260fd7c91fe855aeb0ff99c70ceb7458d593993`
- conclusion: **SUCCESS**
- adversarial/regression suite: **84 passed in 0.39s**
- exact frozen membership assertion: **PASS**
- no-browser/probe execution-path guard: **PASS**

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch03_policy_qualification.md`

The suite covers batch-size drift, eligible-prefix mismatch, raw-queue substitution, reinsertion of attempted BLOCKED dates, chronology drift, duplicates, prior-attempt contamination, non-initial eligibility, caller/manual selection surfaces, mutable return values and outcome/priority selection surfaces.

The first qualification run `34891254793` already had `84 passed` and exact membership PASS, but its final browser guard produced a false positive because it searched the workflow for a literal string present in its own assertion. The guard was corrected minimally and the full suite was re-run rather than accepting the first run.

## 9. Browser boundary

The qualified Batch 03 freeze tool contains membership only and no execution path using:

- Playwright;
- Chromium;
- `probe_candidate`;
- `asyncio`.

Therefore no Batch 03 historical broker observation occurred before this policy PASS.

A separate execution workflow may now be created for these exact five dates, provided the pre-browser gates remain mandatory.

No `.bi5` acquisition and no real backtest are authorized by this policy.
