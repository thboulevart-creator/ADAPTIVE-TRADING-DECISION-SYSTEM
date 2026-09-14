# HISTORICAL TRADING BREAKS RECOVERY — FIRST BATCH POLICY

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH_POLICY_V1`

Parent protocol:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Verdict before execution

**PASS — `FIRST_RECOVERY_BATCH_POLICY_FIXED_BEFORE_OUTCOME_OBSERVATION`**

This document fixes the first systematic recovery batch before any new candidate outcome is observed.

## 1. Frozen batch size

`BATCH_SIZE = 5`

The size is selected only for operational and reproducibility reasons:

- one browser workflow remains a bounded, reviewable execution unit;
- five independent date captures keep runtime and artifact volume limited;
- one artifact can retain complete request/response/DOM/screenshot evidence for all dates while preserving date-level directories;
- five dates materially reduce workflow overhead compared with one run per date without turning the first run into a large opaque bulk operation;
- a failure or runtime issue remains diagnosable without contaminating the remaining 61 unresolved dates.

The size was **not** selected from holiday type, expected break behavior, apparent ease, prior source availability, or any observed result for the five dates.

Once this policy is versioned, Batch 01 size MUST NOT be changed because its dates prove easy, difficult, positive, empty, blocked, or failing.

## 2. Deterministic membership rule

Batch 01 membership is exactly:

`recovery_queue()[:5]`

where `recovery_queue()` is the governed queue from:

`tools/trading_breaks_recovery_protocol.py`

No date is manually inserted, excluded, substituted, reordered, or selected by holiday name.

At policy-version time the expected mechanically derived membership is:

1. `2021-11-25 — THANKSGIVING_DAY`
2. `2021-11-26 — THANKSGIVING_FRIDAY`
3. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2021-12-24 — CHRISTMAS_OBSERVED`
5. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE`

These identities are regression assertions, not discretionary target choices.

## 3. Execution order

The five candidates MUST be executed and adjudicated in strict ascending date order.

Technical reuse of one workflow or browser installation is allowed. Evidence capture and adjudication remain independent per date.

A failure or no-record result on one candidate MUST NOT stop the other governed candidates from being attempted unless the shared runtime itself is no longer trustworthy.

## 4. Evidence boundary

For every candidate:

- exact historical date must be addressed;
- target instrument remains `USATECH.IDX/USD` / Dukascopy ID `9016`;
- raw broker response payload must be retained;
- DOM/equivalent broker-native rendering is retained where available;
- exact positive record may proceed to date-level PASS adjudication only after workflow/artifact/hash/commit provenance exists;
- no-record remains `BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`;
- absence MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`;
- malformed, wrong-date, wrong-instrument, or contradictory evidence is not promotable.

The capture probe itself MUST NOT declare a calendar PASS before artifact provenance exists. It may only report that a positive record was captured and is pending protocol adjudication.

## 5. Artifact/provenance rule

Batch 01 must preserve:

- protocol and batch-policy versions;
- exact batch membership/order;
- workflow run ID;
- numeric job ID where available;
- probe commit SHA;
- uploaded artifact ID;
- GitHub-provided artifact SHA-256 digest;
- per-date request/response capture;
- per-date DOM/equivalent capture;
- per-date screenshot where runtime permits;
- compact versioned runtime summary for adjudication.

## 6. Adversarial gates before browser execution

The workflow MUST run the existing recovery-protocol adversarial suite and the Batch 01 policy tests before opening the historical browser probe.

At minimum the batch tests reject:

- batch-size drift;
- queue-prefix drift;
- chronology drift;
- resolved-date reintroduction;
- manual divergence from the first five governed unresolved candidates.

If these gates fail, the historical probe MUST NOT execute.

## 7. Post-batch rule

After Batch 01 completes:

1. adjudicate all five dates independently under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`;
2. integrate only true positive-record PASS dates;
3. leave no-record outcomes BLOCKED;
4. rerun calendar/coverage/boundary regression only if executable calendar evidence changes;
5. persist run/artifact/hash/job/commit provenance and updated counts;
6. update session backup and Recovery Checkpoint.

No `.bi5` acquisition and no real backtest are authorized by this policy.
