# HISTORICAL TRADING BREAKS RECOVERY — BATCH 02 POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02_POLICY_V1`

Parent protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

Inherited operational batch contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH_POLICY_V1`

## Verdict before execution

**PASS — `BATCH02_POLICY_FIXED_BEFORE_OUTCOME_OBSERVATION`**

This document freezes Batch 02 before any new Batch 02 historical outcome is observed.

## 1. Frozen batch size

`BATCH_SIZE = 5`

The size is inherited unchanged from the already governed Batch 01 operational policy. It remains fixed solely for reproducibility, bounded runtime, bounded artifact volume, and date-level auditability. It MUST NOT be changed because any Batch 02 target appears easy, difficult, likely positive, likely empty, or otherwise convenient.

## 2. Deterministic membership rule

Batch 02 membership is exactly the first five entries of the governed post-Batch-01 recovery queue at policy-version time:

`recovery_queue()[:5]`

Expected mechanically derived membership:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
3. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
4. `2022-02-21 — PRESIDENTS_DAY`
5. `2022-04-15 — GOOD_FRIDAY`

These five identities are regression assertions, not discretionary choices. After this policy is versioned, the Batch 02 membership MUST remain immutable even if one or more dates later become PASS, BLOCKED, or FAIL.

No date may be skipped, substituted, inserted, or reordered according to holiday type, prior source availability, expected result, or apparent difficulty.

## 3. Execution order

The five candidates MUST be executed and adjudicated in strict ascending date order.

A shared browser runtime is allowed. Each date retains independent request/response/DOM/screenshot capture and independent protocol adjudication.

A no-record outcome on one date MUST NOT stop later governed dates. Execution may stop only if the shared runtime itself becomes untrustworthy.

## 4. Evidence boundary

For every Batch 02 target:

- exact historical date must be addressed;
- target instrument remains `USATECH.IDX/USD` / Dukascopy ID `9016`;
- raw broker response payload must be retained;
- DOM/equivalent broker-native rendering must be retained where available;
- positive records are only capture candidates until artifact provenance exists and `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1` independently adjudicates them;
- empty/no-record remains `BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`;
- adjacent-date or overlapping records MUST NOT be promoted as exact-target proof;
- absence MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`;
- wrong-date, wrong-instrument, malformed, provenance-deficient, or contradictory evidence is not promotable.

## 5. Artifact/provenance rule

Batch 02 must preserve:

- protocol and Batch 02 policy versions;
- exact frozen membership/order;
- workflow run ID;
- numeric job ID where available;
- probe commit SHA;
- uploaded artifact ID;
- GitHub artifact SHA-256 digest;
- per-date network request/response capture;
- per-date DOM/equivalent capture;
- per-date screenshot where runtime permits;
- compact versioned runtime summary for independent adjudication.

## 6. Adversarial gates before browser execution

Before opening Chromium, the workflow MUST execute:

1. the parent recovery-protocol adversarial suite;
2. the frozen Batch 01 regression, proving Batch 01 history was not rewritten;
3. the Batch 02 policy suite.

The Batch 02 tests MUST reject at least:

- batch-size drift;
- mismatch from the first five current governed unresolved candidates;
- chronology drift;
- duplicates;
- resolved-date reintroduction;
- mutation of the frozen Batch 02 membership.

If those gates fail, no Batch 02 historical browser observation is allowed.

## 7. Post-batch rule

After Batch 02 execution:

1. adjudicate all five dates independently under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`;
2. integrate only genuine positive-record PASS dates;
3. leave no-record / inadmissible exact-date outcomes BLOCKED;
4. rerun calendar/coverage/boundary regression only if executable evidence changes;
5. preserve run/job/artifact/hash/probe-commit provenance and updated counts;
6. archive Batch 02 membership against later queue drift;
7. update session backup and Recovery Checkpoint.

No `.bi5` acquisition and no real backtest are authorized by this policy.
