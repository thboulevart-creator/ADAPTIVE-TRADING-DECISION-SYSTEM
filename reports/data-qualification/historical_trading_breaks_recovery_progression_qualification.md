# HISTORICAL TRADING BREAKS RECOVERY — ATTEMPT-AWARE PROGRESSION QUALIFICATION

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Final verdict:

**PASS — `ATTEMPT_AWARE_RECOVERY_PROGRESSION_REJECTS_RETRY_BYPASSES_AND_PREVENTS_STARVATION`**

## 1. Purpose

This qualification addresses the progression defect exposed after Batch 02: calendar-unresolved dates that were already attempted and remained `BLOCKED` must remain unresolved, but they must not be replayed indefinitely under an unchanged evidence capability and starve later unresolved candidates.

The qualified boundary separates:

1. calendar evidence state;
2. immutable recovery attempt history;
3. execution eligibility.

It does not alter the historical broker-evidence adjudication contract and does not define Batch 03 membership.

## 2. Historical state preserved

The versioned attempt ledger contains all ten factual Batch 01 / Batch 02 executions.

In particular, the duplicated historical attempts of:

- `2021-12-24 — CHRISTMAS_OBSERVED`;
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`;

are retained rather than rewritten, even though Batch 01 and Batch 02 used the same semantic capture capability.

Current semantic capability:

`TRADING_BREAKS_PRIMARY_WIDGET_V1`

Fingerprint:

`82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

Batch 02 explicitly reused `tools.trading_breaks_recovery_batch01.probe_candidate`; new run/job/artifact/probe-commit provenance therefore does not constitute a new semantic capability.

## 3. First adversarial execution

Workflow:

- run: `34890138036`
- job: `104130467209`
- trigger commit: `fe09849451c868a9abb624d9d1525539e0b49d25`
- result: **SUCCESS**
- regression/adversarial suite: **67 passed**

The candidate runtime state was internally coherent:

- calendar unresolved: `61`
- attempt ledger entries: `10`
- attempted BLOCKED and execution-ineligible: `3`
- execution-eligible unresolved: `58`
- registered material capability changes: not yet governed by an external registry in this first implementation.

However, the nominal test PASS was **not accepted as the final contract verdict**. A second adversarial design review found two real bypasses not covered by the first suite.

## 4. Bypasses found after the first nominal PASS

### Bypass A — declarative capability-token promotion

The first implementation could treat addition of a relevant `proof_capability` token as a material capability change even when `route_contract`, `protocol_contract`, and `capture_implementation` were unchanged.

That meant metadata could masquerade as an actual new evidence capability.

This was unacceptable.

### Bypass B — caller-injected retry authorization

The first production scheduling interface accepted caller-provided `attempts`, `current capability`, or `changes` inputs.

A future consumer could therefore inject an unversioned retry authorization rather than deriving it exclusively from governed repository state.

This was unacceptable.

## 5. Minimal corrections

The corrections were deliberately limited to the progression boundary.

A material retry change now requires all of the following:

- exact old/new semantic capability fingerprints;
- exact declared-versus-actual changed dimensions;
- at least one real executable semantic change in `route_contract`, `protocol_contract`, or `capture_implementation`;
- at least one newly added proof capability relevant to the exact blocker;
- no removal of previously qualified proof capabilities;
- explicit blocker coverage;
- versioned qualification contract;
- exact 40-hex qualification commit.

A proof-capability token alone now fails with:

`NO_ROUTE_PROTOCOL_OR_RUNTIME_CHANGE`

Production progression now loads its own authoritative state from:

- `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
- `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`

`progression_decisions()` and `eligible_recovery_queue()` accept no caller-provided scheduling or retry-authorization inputs.

The material-capability-change registry is currently empty.

## 6. Final adversarial re-break

Authoritative corrected workflow:

- run: `34890560172`
- job: `104131879994`
- trigger commit: `c020a5132d053011f517007b9562b5257bbf9aaf`
- result: **SUCCESS**
- adversarial/regression suite: **72 passed in 0.51s**
- persisted corrected runtime commit: `b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`

The corrected suite rejects, among other attacks:

- BLOCKED-to-resolved promotion;
- identical-capability replay;
- new-run/new-artifact/new-probe-commit masquerading as capability change;
- version-label-only change;
- proof-token-only change;
- unrelated proof capability;
- false old/new fingerprints;
- false changed-dimension declarations;
- proof-capability regression;
- missing/invalid material-change qualification identity;
- caller-injected retry/scheduling state;
- hidden unresolved-date omission;
- starvation behind an ineligible unresolved prefix;
- PASS/unresolved contradiction;
- silent retry after FAIL.

## 7. Authoritative current progression state

Runtime schema:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Runtime verdict:

**PASS — `ATTEMPT_AWARE_PROGRESSION_STATE_IS_DETERMINISTIC_AND_NON_STARVING`**

Current values:

- calendar unresolved: `61`
- attempt ledger entries: `10`
- registered material capability changes: `0`
- attempted BLOCKED / currently execution-ineligible: `3`
- execution-eligible unresolved initial/retry candidates: `58`

The three already-attempted BLOCKED dates remain calendar-unresolved and are explicitly execution-ineligible under the unchanged current capability:

- `2021-12-24` → `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`
- `2021-12-31` → `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`
- `2022-04-15` → `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

Later never-attempted unresolved dates remain eligible, proving that this ineligible prefix no longer starves progression.

## 8. Calendar/boundary state remains unchanged

This qualification changes scheduling eligibility only; it does not add or remove calendar evidence.

Therefore the governed accounting remains:

- global: `111 candidates / 30 resolved / 81 unresolved / 0 FAIL`
- execution-window candidate: `68 candidates / 7 resolved / 61 unresolved / 0 FAIL`

The execution window remains unfrozen.

No `.bi5` acquisition is authorized.

No real backtest is authorized.

## 9. Final boundary decision

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION = PASS`

The starvation/retry frontier is now qualified strongly enough for the next action to use `eligible_recovery_queue()` rather than raw `recovery_queue()` when freezing the next execution batch.

This report itself does **not** freeze or execute Batch 03.
