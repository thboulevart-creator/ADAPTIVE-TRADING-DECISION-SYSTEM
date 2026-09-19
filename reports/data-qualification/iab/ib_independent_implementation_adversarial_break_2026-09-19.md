# I_B — INDEPENDENT IMPLEMENTATION CANDIDATE — ADVERSARIAL BREAK

**Date:** 2026-09-19

Initial I_B source commit:

`ac37dc2157659ecbfe6190a6e970245be89ff1de`

Initial I_B source Git blob:

`1b3fbcd4ac084eedc27a008c959025c02b71a95a`

Initial I_B raw-source SHA-256:

`1179ffda54f568e8c7f3fc94887137a9442ba28787ea4dcdf052c4fcbcfb1285`

Evidence binding commit:

`fcd2eceb84850c2bac618b71bb0e1c8323a662b7`

Candidate qualification runner commit:

`699bd501b63d44c6bba7ab3bffe35621302e107a`

No I_A source was used as derivation input.

## Initial qualification result

Candidate workflow:

```text
run = 35444348136
job = 105900601241
```

Results:

```text
qualified evidence breaker = 11 passed
frozen I_B breaker         = 23 passed
```

All exact source/evidence/breaker locks, qualification-environment checks and clean-worktree checks passed.

A green frozen breaker was not treated as sufficient for PASS.

---

## Executable adversarial break

Supplemental adversarial breaker:

`breakers/native_bi5_ib_independent_qualifier_adversarial.py`

Breaker commit:

`a26518b35d48ecbcdc856b5fafdb6b5c4cb738e3`

Breaker blob:

`b60aa0e0e70b1c6864ed0682536d5169038726c0`

Workflow:

`Native BI5 I_B Independent Qualifier Adversarial`

Run:

```text
run = 35444439482
job = 105900841148
4 failed
2 passed
```

All pre-break controls and clean-worktree checks passed.

---

## IB-F01 — RESEALED_MANIFEST_DIGEST_SUBSTITUTION_ACCEPTED

### Attack

Produce a valid qualified I_B result.

Replace:

`implementation_manifest_digest`

with an arbitrary 64-hex digest.

Recompute the public deterministic result seal over the forged payload.

### Observed behavior

`is_sealed_implementation_result(...)`

returns true.

The current structural validator checks result identity/status invariants but does not require the embedded manifest digest to equal the manifest generated from the actually executing I_B source.

### Consequence

A digest-consistent result can falsely claim another implementation manifest while still being accepted as a sealed I_B result.

This violates the boundary requirement that the result seal bind the actual implementation manifest digest.

### Verdict

```text
IB-F01 = FAIL
```

Minimal correction:

`_validate_shape` must require:

```text
result.implementation_manifest_digest
==
SHA256(canonical current build_implementation_manifest())
```

before seal validity can be true.

---

## IB-F02 — RESEALED_INCOMPLETE_DETERMINANT_BINDING_ACCEPTED

### Attack

Produce a valid qualified I_B result.

Remove determinant `Q` from:

`input_determinant_digests`.

Recompute the deterministic result seal.

### Observed behavior

The resealed result is accepted as a valid sealed result.

### Consequence

The public result validator does not prove that a sealed result still binds the complete normative determinant set:

```text
D R M B A Q F O
```

This weakens the exact-input-state binding required by the I_A/I_B boundary.

### Verdict

```text
IB-F02 = FAIL
```

Minimal correction:

result structural validation must require:

- exact determinant key set;
- every determinant digest to be a valid 64-hex digest.

The validator does not need to rediscover the original input package; it must at least reject a structurally incomplete claimed determinant binding.

---

## IB-F03 — MALFORMED_EXECUTION_CONTEXT_ESCAPES_STATUS_MODEL

### Attack

Call:

`qualify_native_bi5(...)`

with otherwise valid synthetic input and:

```text
execution_context = None
execution_context = "not-a-context"
```

### Observed behavior

The implementation raises raw:

`AttributeError`

from isolation-context access.

### Boundary consequence

The implementation boundary defines explicit nonsemantic execution statuses:

```text
ENVIRONMENT_BLOCKED
IMPLEMENTATION_ERROR
```

A malformed/unavailable pre-seal execution context must not accidentally become semantic `QUALIFICATION_BLOCKED`, but it also must not escape the governed status model as an unclassified exception.

### Verdict

```text
IB-F03 = FAIL
```

Minimal correction:

normalize a non-mapping execution context into a closed environment snapshot and return:

```text
execution_status = ENVIRONMENT_BLOCKED
semantic_status = NOT_REACHED
freeze_status = NOT_REACHED
```

An empty mapping already behaves this way and passed the attack.

---

## Attack that already survives

The supplemental breaker confirmed that an unverified claimed constructive-completeness proof does not activate A08.

Current behavior remains:

```text
unverified A08 claim
→ A07
→ QUALIFICATION_BLOCKED
```

This is the required fail-closed behavior while the constructive-proof verifier remains unqualified.

---

## Initial adversarial verdict

```text
I_B INDEPENDENT IMPLEMENTATION CANDIDATE
FAIL
```

Demonstrated defects:

```text
IB-F01 — RESEALED_MANIFEST_DIGEST_SUBSTITUTION_ACCEPTED
IB-F02 — RESEALED_INCOMPLETE_DETERMINANT_BINDING_ACCEPTED
IB-F03 — MALFORMED_EXECUTION_CONTEXT_ESCAPES_STATUS_MODEL
```

The qualified evidence breaker remains immutable:

`231f9daa343f95baa4b747ec2b89166833255958`

The frozen I_B breaker remains unchanged:

`d1a305e3b9ae813e891b34522e3a12bb6bc8ac34`

No upstream D/R/M/B/A/Q/F semantics may be modified.

No I_A source may be used as a correction input.

---

## Authorized minimal correction

Correct only IB-F01..IB-F03 in:

`src/native_bi5_independent_qualifier.py`.

After source bytes change:

1. compute the new raw-source SHA-256;
2. update only `source_digests` in all three derivation evidence JSON files;
3. keep `source_binding_state = BOUND_TO_IMPLEMENTATION_SOURCE`;
4. modify no frozen semantic payload or frozen payload hash;
5. update only source hash locks in candidate/adversarial runners;
6. rerun the immutable evidence breaker;
7. rerun the frozen I_B breaker;
8. rerun the supplemental adversarial breaker;
9. perform final persisted-head re-break before any PASS.

No real BI5 acquisition, processing or backtest is authorized.

---

## Residual persisted-head re-break — IB-R01

First minimal correction source commit:

`36d916a02951736c0122d62b79e27295db0834f2`

Corrected source Git blob:

`051acc40a6368d9159de720eacbd1e6e778a9776`

Corrected raw-source SHA-256:

`06461c72e4a5dd96f7c0dd6758759d3a5d60faaaeb447d5ea635d027a467a429`

Rebinding commit:

`721adb43a01e3f6ecd5a084771b029b65ea94ce1`

Post-correction results:

```text
candidate workflow
run = 35444604586
evidence breaker = 11 passed
frozen I_B breaker = 23 passed

supplemental adversarial workflow
run = 35444604463
6 passed
```

The initial IB-F01..IB-F03 attacks survive the first correction.

A new persisted-head attack was then added.

Run:

```text
run = 35444686972
job = 105901479082
1 failed
6 passed
```

### IB-R01 — BLOCKED_MISSING_DETERMINANT_RESULT_LOSES_PRESENT_INPUT_BINDINGS

Attack:

Remove only determinant `Q` from an otherwise valid input package.

Expected governed outcome:

```text
execution_status = COMPLETED
semantic_status = QUALIFICATION_BLOCKED
freeze_status = NOT_CREATED
```

The result should remain a valid sealed terminal result and should bind the seven determinant digests that were actually supplied.

Observed current behavior:

```text
semantic status is correctly blocked
but
input_determinant_digests = {}
```

The implementation copies determinant bindings only after exact-set validation succeeds.

The first correction also made exact determinant completeness a universal sealed-result invariant, so the blocked result cannot be recognized as validly sealed.

This conflates:

```text
qualified result
→ must bind complete D/R/M/B/A/Q/F/O set

blocked due missing determinant
→ must accurately bind the provided valid subset
```

### Verdict

```text
IB-R01 = FAIL
```

Minimal correction:

1. preserve every provided determinant binding that is structurally a valid required-key/64-hex pair before completeness adjudication;
2. for a `QUALIFIED` result, require the exact complete determinant set;
3. for a non-qualified terminal result, allow a valid subset of required determinant bindings so the result can faithfully bind the incomplete input state that caused blocking;
4. continue rejecting unknown determinant keys or malformed claimed digests from sealed result validation.

No evidence semantics, frozen breaker or I_A source may be changed.


---

## Final persisted-head I_B re-break and verdict

Second minimal correction source commit:

`a988da503651451df7801ddec6dec26cc04d5801`

Final I_B source Git blob:

`25fadd36761616e89a21964201b3bfa3c7349ea4`

Final I_B raw-source SHA-256:

`a2b155d23a3a66968ba5bc35586bc7a9b9318655053121066676d6db1d7addb9`

Final post-code evidence binding/workflow transition commit:

`2d9ad088bb9ada9a289f63307df2e2c0ab7a0182`

Final bound evidence blobs:

```text
provenance
f78025f5e8ad9bf9a66f8ceef3995eddecdc0cf3

no-copy
b62df24e695c925ab440b826b5100c84e9072468

stage inventory
b822f48bbdca3c9580374a7170b493f7f684e1b0
```

The qualified evidence breaker remained unchanged:

`231f9daa343f95baa4b747ec2b89166833255958`

The frozen I_B breaker remained unchanged:

`d1a305e3b9ae813e891b34522e3a12bb6bc8ac34`

Final supplemental adversarial breaker blob:

`e0fd8b6c8b946945ad91d772fc0505edbc7f79f5`

### Final same-HEAD re-break

Persisted code/evidence/harness HEAD:

`5f79f77951c8563d7a4cc193e1fdca9b8aa7a09a`

Workflow:

`Native BI5 I_B Independent Qualifier Persisted-HEAD Rebreak`

Run:

```text
run = 35444927844
job = 105902106261
```

Results:

```text
qualified derivation evidence breaker = 11 passed
frozen I_B breaker                    = 23 passed
supplemental adversarial breaker      = 7 passed
```

All exact source/evidence/breaker blob locks, raw source SHA-256 lock, qualification-environment checks and clean-worktree checks passed.

### Defect closure

```text
IB-F01 — RESEALED_MANIFEST_DIGEST_SUBSTITUTION_ACCEPTED
→ SURVIVES CORRECTION

IB-F02 — RESEALED_INCOMPLETE_DETERMINANT_BINDING_ACCEPTED
→ SURVIVES CORRECTION

IB-F03 — MALFORMED_EXECUTION_CONTEXT_ESCAPES_STATUS_MODEL
→ SURVIVES CORRECTION

IB-R01 — BLOCKED_MISSING_DETERMINANT_RESULT_LOSES_PRESENT_INPUT_BINDINGS
→ SURVIVES CORRECTION
```

No additional internal I_B implementation defect was demonstrated after the second minimal correction and final same-HEAD re-break.

### Independence / pair evidence that also passed

The frozen I_B breaker additionally demonstrated on the qualified synthetic fixture:

- I_B source and I_A source are not identical;
- structural clone detector remains below its forbidden threshold;
- no I_A import/shared semantic shortcut is admitted by the checked source/dependency surface;
- cold-import and runtime channel audits remain closed;
- I_B source digests match all three bound independent-derivation evidence artifacts;
- I_A and I_B independently sealed semantic projections agree on the same immutable synthetic input;
- I_A-only semantic mutation is detected;
- I_B-only semantic mutation is detected;
- result-byte/seal inequality is not mistaken for semantic inequality;
- strict duplicates, zero/crossed prices, finite negative volume and timestamp regression remain preserved;
- local A09 rejection/accounting remains exact;
- late semantic blocking emits no partial qualified universe;
- missing normative input fails closed.

The I_A source was not used as a derivation input for I_B. It is touched only by the already-qualified external pair breaker after independently sealed I_B execution, as permitted by the boundary.

### Known scope limitation retained

Positive A08 constructive-completeness proof validation remains unavailable because its independent verifier/schema is not qualified.

I_B therefore deliberately remains fail-closed:

```text
unverified claimed constructive-completeness proof
→ no A08 promotion
→ A07
→ QUALIFICATION_BLOCKED
```

This does not authorize real-data B/A closure.

## Final implementation-layer verdict

```text
I_B INDEPENDENT IMPLEMENTATION CANDIDATE
PASS
```

Scope of this PASS:

- independent I_B source exists;
- source digest is bound to the already-qualified derivation evidence package;
- no frozen evidence semantics changed after source creation;
- qualified evidence breaker remains unchanged and passes;
- frozen I_B breaker remains unchanged and passes;
- demonstrated implementation defects are encoded in the supplemental breaker and pass;
- pair semantic agreement and one-sided mutant detection pass on synthetic/in-memory fixtures;
- final qualification is from one persisted HEAD.

This PASS does **not** imply:

```text
D = PASS
R = PASS
M = PASS
B = PASS
A = PASS
Q = PASS
F = PASS
O = PASS
I_B global executable gate = PASS
real BI5 acquisition authorized
real BI5 processing authorized
real backtest authorized
```

The correct two-level state is:

```text
I_B implementation candidate qualification = PASS
I_B global executable gate                  = BLOCKED
```

because the complete concrete D/R/M/B/A/Q/F/O chain remains officially BLOCKED and has not been materially instantiated against real acquisition evidence.

No permission increase is created.
