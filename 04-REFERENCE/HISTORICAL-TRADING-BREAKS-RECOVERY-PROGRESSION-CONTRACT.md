# HISTORICAL TRADING BREAKS RECOVERY — ATTEMPT-AWARE PROGRESSION CONTRACT

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Parent adjudication boundary:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Final status

**PASS — `ATTEMPT_AWARE_RECOVERY_PROGRESSION_REJECTS_RETRY_BYPASSES_AND_PREVENTS_STARVATION`**

Authoritative qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_progression_qualification.md`

Authoritative final re-break:

- workflow run: `34890560172`
- job: `104131879994`
- trigger commit: `c020a5132d053011f517007b9562b5257bbf9aaf`
- adversarial/regression suite: `72 passed in 0.51s`
- corrected runtime commit: `b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`

This contract prevents unresolved dates already attempted under an unchanged evidence capability from starving later unresolved candidates, without ever converting `BLOCKED` into resolved evidence.

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

The authoritative attempt ledger is:

`reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`

### C. Execution eligibility

Execution eligibility answers whether an unresolved date is justified for another execution under the **current semantic capability**.

Eligibility is a scheduling property only. It MUST NOT alter calendar evidence accounting.

## 2. Semantic capability identity

A capability identity consists of fields that describe what evidence the recovery route can actually obtain or admit:

- `route_contract`;
- `protocol_contract`;
- `capture_implementation`;
- explicit `proof_capabilities`.

Its fingerprint is the SHA-256 of a canonical serialization of those semantic fields.

The following are **attempt provenance**, not capability identity, and MUST NOT authorize retry by themselves:

- workflow run ID;
- job ID;
- artifact ID;
- artifact digest;
- probe commit SHA;
- wall-clock execution time;
- rerun number.

For historical Batch 01 / Batch 02, the semantic capability is the same because Batch 02 explicitly reuses `tools.trading_breaks_recovery_batch01.probe_candidate` under the same broker-evidence route and parent protocol.

Current capability:

`TRADING_BREAKS_PRIMARY_WIDGET_V1`

Current fingerprint:

`82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## 3. Initial-attempt rule

For an unresolved date with no prior attempt in the ledger:

`ELIGIBLE — INITIAL_ATTEMPT`

No expected outcome, holiday type, convenience score, source availability, or manual preference may influence this decision.

## 4. Identical-capability retry rule

If an unresolved date's latest attempt is `BLOCKED` and the current capability fingerprint equals the latest attempt's capability fingerprint:

`INELIGIBLE — SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

A new run/artifact/probe commit with the same semantic capability is still the same capability and MUST NOT bypass this rule.

This prevents indefinite replay and starvation while leaving the date unresolved.

## 5. Material-capability-change retry predicate

A previously `BLOCKED` date may become execution-eligible again only if **all** of the following are true:

1. current semantic capability fingerprint differs from the latest attempted capability fingerprint;
2. an explicit **versioned registry entry** binds the exact old fingerprint to the exact new fingerprint;
3. its declared changed dimensions exactly equal the dimensions that actually changed;
4. **at least one executable semantic dimension changes**: `route_contract`, `protocol_contract`, or `capture_implementation`;
5. at least one genuinely new proof capability is added, and no previously qualified proof capability is removed;
6. the change has its own versioned qualification contract and exact qualification commit;
7. the prior blocking reason is explicitly addressed;
8. at least one newly added proof capability belongs to the governed requirement set for that exact blocking reason.

A new `proof_capabilities` token by itself is **declarative metadata**, not proof of a material capability change. It cannot authorize retry unless accompanied by a real route/protocol/capture change and a versioned qualification.

The only authoritative retry-change registry is:

`reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`

Production scheduling MUST load this registry itself. A caller MUST NOT be able to inject an unversioned `changes`, `attempts`, `current capability`, manual skip, expected outcome, or priority override into `progression_decisions()` or `eligible_recovery_queue()`.

If any predicate fails:

`INELIGIBLE — RETRY_MATERIAL_CHANGE_NOT_PROVEN`

The initial governed retry-capability requirements are:

- `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED` requires at least one newly added capability from:
  - `ALTERNATE_BROKER_NATIVE_RECORD_ROUTE`
  - `BROKER_ARCHIVE_BACKFILL_ACCESS`
- `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` requires at least one newly added capability from:
  - `QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION`
  - `ALTERNATE_EXACT_TARGET_DATE_PRIMARY_RECORD_ROUTE`
- `EXPECTED_DOM_CROSSCHECK_MISSING` requires `DOM_CROSSCHECK_RECOVERY_PATH`.
- provenance/retention blockers require a newly qualified provenance/retention repair capability appropriate to that blocker.

Adding an unrelated capability cannot authorize retry.

## 6. FAIL and inconsistent-state rule

A latest `FAIL` is not automatically retryable through this progression contract. It remains ineligible until a separately governed remediation proves that the violated invariant was corrected.

If an attempt ledger says `PASS` while the same date is still in the unresolved calendar queue, the state is contradictory and progression MUST fail closed rather than schedule the date.

## 7. Non-silent progression plan

The progression layer MUST produce one decision for **every current unresolved date**, in the exact chronological order of `recovery_queue()`.

Each decision exposes:

- target date/reason;
- unresolved calendar state;
- latest attempt ID/outcome/capability fingerprint when present;
- `eligible` boolean;
- deterministic eligibility reason.

The execution-eligible queue is only a filtered projection of this complete decision list.

Therefore an already-attempted BLOCKED date may be bypassed for execution, but it cannot be hidden: it remains visible as unresolved + ineligible with an explicit reason.

## 8. Starvation rule

An ineligible attempted-BLOCKED prefix MUST NOT prevent later never-attempted unresolved candidates from becoming eligible.

The scheduler scans the complete unresolved queue chronologically and selects only dates whose deterministic eligibility is true. It MUST NOT stop merely because the earliest unresolved item is ineligible.

## 9. Outcome-independence and injection boundary

Production eligibility MUST NOT accept or consume:

- `expected_outcome`;
- manual priority;
- manual skip lists;
- caller-provided attempt history;
- caller-provided current capability;
- caller-provided material-change authorizations.

It MUST NOT select dates according to expected positive/empty probability, holiday type, apparent ease, or convenience.

Chronology plus versioned calendar state, attempt ledger, semantic capability identity, and material-change registry are the only admissible production progression inputs.

## 10. Historical duplicate attempts

Batch 01 and Batch 02 predate this progression contract and contain repeated attempts of `2021-12-24` and `2021-12-31` under the same semantic capability.

Those executions remain in the immutable ledger as historical facts. The contract does not rewrite or retroactively delete them. It governs future eligibility from the latest factual attempt onward and therefore forbids another identical-capability replay.

## 11. Adversarial qualification result

The final executable boundary rejects at least:

1. removing attempted BLOCKED dates from calendar unresolved accounting;
2. treating attempt completion as resolution;
3. retrying a BLOCKED date under unchanged semantic capability;
4. treating a new workflow run/artifact/probe commit as a capability change;
5. version-string-only changes with no new proof capability;
6. proof-capability-token-only changes with no real route/protocol/capture change;
7. unrelated added capabilities falsely claimed to address the blocker;
8. wrong old/new fingerprints;
9. lying about which semantic dimensions actually changed;
10. removal/regression of previously qualified proof capabilities;
11. missing/invalid material-change qualification identity;
12. caller-injected retry authorizations or scheduling state;
13. hidden skipping where the progression plan omits unresolved dates;
14. starvation where an ineligible unresolved prefix prevents later initial attempts;
15. expected-outcome/manual-priority selection paths;
16. ledger mutation/deletion of historical duplicate attempts;
17. `PASS`/unresolved contradictions.

The first nominal adversarial execution passed its then-current suite but a second design review exposed two genuine bypasses: declarative proof-token-only retry and caller-injected change authorization. Those were minimally corrected and the corrected boundary then passed the 72-test re-break.

## 12. Current qualified state

The material capability-change registry is currently empty.

Current progression state:

- calendar unresolved: `61`
- historical attempts: `10`
- registered material capability changes: `0`
- attempted BLOCKED and execution-ineligible: `3`
- execution-eligible unresolved initial/retry candidates: `58`

The three BLOCKED dates remain unresolved but are not currently retry-eligible:

- `2021-12-24`
- `2021-12-31`
- `2022-04-15`

This contract authorizes the next batch-freezing step to use `eligible_recovery_queue()` rather than raw `recovery_queue()`.

It does **not** itself freeze Batch 03.

No `.bi5` acquisition and no real backtest are authorized by this PASS.
