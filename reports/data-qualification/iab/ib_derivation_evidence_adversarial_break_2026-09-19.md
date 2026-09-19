# I_B — INDEPENDENT DERIVATION EVIDENCE PACKAGE — ADVERSARIAL BREAK

**Date:** 2026-09-19  
**Candidate evidence commit:** `17cd86ca0c943488fd5eea73feba7a557bafea97`  
**Evidence breaker/workflow commit:** `660754f81e85282cd9d8a0b19e58294d37c92808`

No I_B production source exists.

The I_A source was not used as derivation input for this evidence block.

## Candidate evidence blobs

```text
ib_semantic_source_provenance.json
8c9a6406275b653baa130127d8668ddae4b08581

ib_no_copy_declaration.json
8fc59ab9232e778abd08471e18a5ce5c98ede6af

ib_independent_stage_test_inventory.json
35aa65ab3a9646b897e2ad7f8e2a065de07f0ee2
```

## Executable break

Workflow:

`Native BI5 I_B Independent Derivation Evidence`

Run:

```text
run = 35443342072
job = 105897932321
```

Pre-break controls:

```text
exact persisted evidence blobs = PASS
I_B source absent              = PASS
qualification environment      = PASS
clean worktree                 = PASS
```

Breaker:

```text
4 failed
5 passed
```

---

## IBE-F01 — FROZEN_PAYLOAD_FINGERPRINT_MISMATCH

The three artifacts claim a `frozen_semantic_payload_sha256`.

At least the provenance artifact's declared fingerprint does not equal the canonical SHA-256 of the payload it is meant to freeze.

Attack:

mutate or incorrectly serialize semantic content while leaving the claimed fingerprint unchanged.

Current result:

the package cannot prove that its supposedly frozen semantic substance is the substance actually persisted.

Verdict:

```text
IBE-F01 = FAIL
```

Required correction:

recompute every frozen semantic payload digest canonically and verify all three.

---

## IBE-F02 — FUTURE_BREAKER_SHAPE_MISMATCH

The frozen future I_B breaker requires:

```python
provenance["derivation_basis"] == "PINNED_NORMATIVE_CONTRACTS"
```

The candidate places `derivation_basis` only inside `frozen_semantic_payload`.

Therefore a future independently implemented I_B could be correct while failing the already-qualified breaker because the pre-code evidence package was not shaped to its frozen interface.

Verdict:

```text
IBE-F02 = FAIL
```

Required correction:

expose the exact top-level breaker-required field while keeping the frozen copy inside the semantic payload.

---

## IBE-F03 — ANOMALY_TEST_INVENTORY_TOO_COARSE

The inventory currently uses one generic entry:

```text
A01-A13 targeted anomaly matrix
```

This does not independently enumerate the current A matrix.

Attack:

omit or misimplement one class such as:

```text
A02 undeclared component
A06 zero decompressed bytes
A07 partial without constructive proof
A08 partial with constructive proof
A11 ambiguous component role
A13 unknown anomaly
```

while claiming the generic A01-A13 test exists.

The inventory would not show which anomaly semantics are independently intended to be exercised.

Verdict:

```text
IBE-F03 = FAIL
```

Required correction:

enumerate A01 through A13 as explicit independent test inventory entries, including the A07/A08 constructive-completeness distinction.

---

## IBE-F04 — CROSS_ARTIFACT_PACKAGE_BINDING_MISSING

Each artifact has the same implementation identity/version and a locally frozen payload, but there is no shared immutable evidence-package identity or shared normative-source-set digest.

Attack:

combine:

- provenance artifact from derivation package X;
- no-copy declaration from derivation package Y;
- test inventory from derivation package Z;

where each artifact is individually self-consistent and targets the same I_B implementation version.

Without a common package binding, the set can masquerade as one coherent derivation package.

Verdict:

```text
IBE-F04 = FAIL
```

Required correction:

bind all three frozen payloads to the same:

```text
evidence_package_id
evidence_package_version
normative_source_set_sha256
```

and have the external breaker verify the common binding.

---

## Breaker finding that is NOT an evidence defect

One test failed because the breaker searched for the exact phrase:

`shared project-owned semantic helpers`

while the evidence says:

`sharing project-owned semantic helpers`.

The semantic prohibition is already present.

This is a brittle breaker matcher, not a proof defect.

Correction is authorized only in the evidence breaker:

match the semantic token `project-owned semantic helpers` rather than force one grammatical form.

No evidence wording needs to be weakened or cosmetically changed to obtain PASS.

---

## Two-phase source-digest binding — current adjudication

The pre-code package intentionally has:

```text
source_binding_state = PENDING_IMPLEMENTATION_SOURCE
source_digests = {}
```

This is not by itself a defect because no I_B source is permitted to exist yet.

The package instead freezes a one-way finalization rule:

```text
pre-code:
  freeze semantic provenance / no-copy constraints / test inventory

post-code:
  independently author I_B from those frozen inputs
  then bind only source_digests + source_binding_state
  never mutate frozen_semantic_payload
```

The final frozen I_B breaker will still require:

`evidence.source_digests == implementation_manifest.source_digests`.

Therefore pre-code evidence PASS can authorize only the next implementation block; it cannot qualify executable I_B.

The two-phase rule must survive the corrected persisted-head re-break.

---

## Initial verdict

```text
I_B INDEPENDENT DERIVATION EVIDENCE PACKAGE
FAIL
```

Demonstrated evidence defects:

```text
IBE-F01 — FROZEN_PAYLOAD_FINGERPRINT_MISMATCH
IBE-F02 — FUTURE_BREAKER_SHAPE_MISMATCH
IBE-F03 — ANOMALY_TEST_INVENTORY_TOO_COARSE
IBE-F04 — CROSS_ARTIFACT_PACKAGE_BINDING_MISSING
```

No I_B code is authorized until these defects are minimally corrected and the corrected evidence package survives persisted-head re-break.

No real BI5 acquisition, processing or backtest is authorized.
