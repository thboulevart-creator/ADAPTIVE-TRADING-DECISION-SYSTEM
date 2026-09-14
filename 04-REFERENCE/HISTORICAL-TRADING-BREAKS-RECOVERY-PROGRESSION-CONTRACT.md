# HISTORICAL TRADING BREAKS RECOVERY — ATTEMPT-AWARE PROGRESSION CONTRACT

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication boundary:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Status before adversarial qualification

**CANDIDATE — NOT YET PASS**

This contract exists to prevent unresolved dates that were already attempted under an unchanged evidence capability from starving later unresolved candidates, without ever converting `BLOCKED` into resolved evidence.

Batch 03 MUST NOT be frozen or observed until this contract has survived adversarial qualification.

## 1. Three states that MUST remain separate

### A. Calendar evidence state

Calendar evidence answers only whether a candidate is resolved by admissible evidence.

- `SPECIAL_SESSION_EVIDENCE` and admissible `NO_SPECIAL_CHANGE_EVIDENCE` may resolve a candidate.
- `BLOCKED` never resolves a candidate.
- An attempted-but-BLOCKED date MUST remain in `recovery_queue()` and in global/window unresolved accounting.

Attempt history MUST NOT write to or silently redefine calendar evidence state.

### B. Recovery attempt history

Recovery attempt history records factual executions independently from calendar resolution.

Every attempt identity MUST preserve at least:

- immutable `attempt_id`;
- monotonic `attempt_sequence`;
- exact target date and candidate reason;
- batch/policy identity when applicable;
- outcome `PASS`, `BLOCKED`, or `FAIL`;
- exact blocking reason for `BLOCKED`;
- semantic evidence-capability identity;
- workflow run/job/artifact/SHA/probe-commit provenance.

Historical attempts are facts and MUST NOT be deleted merely because a later attempt supersedes them.

### C. Execution eligibility

Execution eligibility answers whether an unresolved date is justified for another execution under the **current semantic capability**.

Eligibility is a scheduling property only. It MUST NOT alter calendar evidence accounting.

## 2. Semantic capability identity

A capability identity consists only of fields that can materially change what evidence the recovery route can obtain or admit:

- `route_contract`;
- `protocol_contract`;
- `capture_implementation`;
- explicit `proof_capabilities`.

Its fingerprint is the SHA-256 of a canonical serialization of those semantic fields.

The following are **attempt provenance**, not capability identity, and therefore MUST NOT authorize a retry by themselves:

- workflow run ID;
- job ID;
- artifact ID;
- artifact digest;
- probe commit SHA;
- wall-clock execution time;
- rerun number.

For the historical Batch 01 / Batch 02 route, the current semantic capability is the same because Batch 02 explicitly reuses `tools.trading_breaks_recovery_batch01.probe_candidate` under the same broker-evidence route and parent protocol.

## 3. Initial-attempt rule

For an unresolved date with no prior attempt in the ledger under any capability:

`ELIGIBLE — INITIAL_ATTEMPT`

No expected outcome, holiday type, convenience score, or source availability may influence this decision.

## 4. Identical-capability retry rule

If an unresolved date's latest attempt is `BLOCKED` and the current capability fingerprint equals the latest attempt's capability fingerprint:

`INELIGIBLE — SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

A new run/artifact/commit with the same semantic capability is still the same capability and MUST NOT bypass this rule.

This rule prevents indefinite replay and starvation while leaving the date unresolved.

## 5. Material-capability-change retry predicate

A previously `BLOCKED` date may become eligible again only if **all** of the following are true:

1. current semantic capability fingerprint differs from the latest attempted capability fingerprint;
2. an explicit versioned `MaterialCapabilityChange` binds the exact old fingerprint to the exact new fingerprint;
3. its declared changed dimensions exactly equal the dimensions that actually changed;
4. it adds at least one new semantic proof capability; metadata-only/version-label-only changes are insufficient;
5. the prior blocking reason is explicitly addressed;
6. at least one newly added proof capability belongs to the governed requirement set for that exact blocking reason.

If any condition fails:

`INELIGIBLE — RETRY_MATERIAL_CHANGE_NOT_PROVEN`

The initial governed retry-capability requirements are:

- `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED` requires at least one newly added capability from:
  - `ALTERNATE_BROKER_NATIVE_RECORD_ROUTE`
  - `BROKER_ARCHIVE_BACKFILL_ACCESS`
- `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` requires at least one newly added capability from:
  - `QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION`
  - `ALTERNATE_EXACT_TARGET_DATE_PRIMARY_RECORD_ROUTE`
- `EXPECTED_DOM_CROSSCHECK_MISSING` requires `DOM_CROSSCHECK_RECOVERY_PATH`.
- provenance/retention blockers require an explicit newly added provenance/retention repair capability appropriate to the blocker.

Adding an unrelated capability cannot authorize retry.

## 6. FAIL and inconsistent-state rule

A latest `FAIL` is not automatically retryable through this progression contract. It remains ineligible until a separately governed remediation proves that the violated invariant was corrected.

If an attempt ledger says `PASS` while the same date is still present in the unresolved calendar queue, the state is contradictory and progression MUST fail closed rather than schedule the date.

## 7. Non-silent progression plan

The progression layer MUST produce one decision for **every current unresolved date**, in the exact chronological order of `recovery_queue()`.

Each decision must expose:

- target date/reason;
- unresolved calendar state;
- latest attempt ID/outcome/capability fingerprint when present;
- `eligible` boolean;
- deterministic eligibility reason.

The execution-eligible queue is only a filtered projection of this complete decision list.

Therefore an already-attempted BLOCKED date may be bypassed for execution, but it cannot be hidden: it remains visible as unresolved + ineligible with an explicit reason.

## 8. Starvation rule

An ineligible attempted-BLOCKED prefix MUST NOT prevent later never-attempted unresolved candidates from becoming eligible.

The scheduler must scan the complete unresolved queue chronologically and select from dates whose eligibility is true. It MUST NOT stop merely because the earliest unresolved item is currently ineligible.

## 9. Outcome-independence rule

Eligibility MUST NOT accept or consume an `expected_outcome` input.

It MUST NOT select dates according to:

- expected positive record probability;
- expected empty/no-record probability;
- holiday type;
- apparent ease;
- manual preference;
- convenience.

Chronology, factual attempt history, semantic capability identity, and the material-retry predicate are the only admissible progression inputs.

## 10. Historical duplicate attempts

Batch 01 and Batch 02 predate this progression contract and contain repeated attempts of `2021-12-24` and `2021-12-31` under the same semantic capability.

Those executions MUST remain in the immutable ledger as historical facts. The new contract does not rewrite or retroactively delete them. It governs future eligibility from the latest factual attempt onward and therefore forbids a further identical-capability replay.

## 11. Adversarial qualification obligations

Before PASS, the executable contract MUST reject at least:

1. removing attempted BLOCKED dates from calendar unresolved accounting;
2. treating attempt completion as resolution;
3. retrying a BLOCKED date under unchanged semantic capability;
4. treating a new workflow run/artifact/probe commit as a capability change;
5. version-string-only capability changes with no added proof capability;
6. unrelated added capabilities falsely claimed to address the blocker;
7. wrong old/new fingerprints in a retry authorization;
8. lying about which semantic dimensions actually changed;
9. hidden skipping where the progression plan omits unresolved dates;
10. starvation where an ineligible unresolved prefix prevents later initial attempts;
11. expected-outcome/manual-priority selection paths;
12. ledger mutation/deletion of historical duplicate attempts;
13. `PASS`/unresolved contradictions.

Only after these attacks are executed and re-broken successfully may the verdict become PASS.

## 12. Current boundary

This contract authorizes **no Batch 03 membership yet**.

It authorizes no `.bi5` acquisition and no real backtest.
