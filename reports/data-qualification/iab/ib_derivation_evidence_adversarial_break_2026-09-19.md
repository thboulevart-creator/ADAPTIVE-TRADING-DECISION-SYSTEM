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


---

## Residual persisted-head re-break after first correction

First correction commit:

`506e0b17c537250059e27b8ebad82ef31a1a250e`

Corrected evidence blobs:

```text
provenance
446de56a83d442861d130d7cab2054790dd3c6a3

no-copy
2540a86155a2806543f62a039661c28ed5c77eda

test inventory
bbcba195b2b47600d11b7badf4b30482cef99030
```

Corrected evidence breaker blob:

`9461bcfbc2b81b688c03d6084c5911ddff4a460a`

Executable re-break:

```text
run = 35443500490
job = 105898365713
9 passed
```

All persisted-blob locks, I_B-source-absence proof, qualification-environment checks and clean-worktree checks passed.

The four initial defects are materially improved, but full adversarial inspection still demonstrates the following residuals.

### IBE-R01 — POSITIVE_A08_TEST_WITHOUT_QUALIFIED_PROOF_VERIFIER

The inventory now explicitly lists A08, but it currently promises a positive test:

```text
terminal partial with independently valid constructive completeness proof
→ REJECT_RECORD
```

No independently qualified constructive-completeness proof verifier/schema currently exists in the pinned allowed derivation inputs.

Therefore future I_B code cannot implement the positive A08 branch without either:

- inventing proof-validation semantics;
- trusting a self-described proof reference;
- or importing an unqualified external authority.

All three violate the fail-closed boundary.

Current I_A independently reached the same architectural limitation and fails closed, but I_A source is not used as derivation authority here.

Verdict:

```text
IBE-R01 = FAIL
```

Required correction:

the pre-code inventory must mark positive A08 execution as an unresolved dependency and test the currently implementable fail-closed rule:

```text
claimed/unverified constructive proof
→ do not promote A08
→ A07 / QUALIFICATION_BLOCKED
```

A future separately qualified verifier may reopen positive A08 semantics.

### IBE-R02 — CROSS_CUTTING_BOUNDARY_TEST_INVENTORY_GAPS

The stage inventory now covers D/R/M/B/A/Q/F and A01-A13, but it still lacks explicit independent tests for several cross-cutting I_A/I_B-boundary invariants:

- component traversal-order invariance;
- exact execution/semantic/freeze status-axis contradictions;
- result-seal mutation/integrity;
- pre-seal environment/read/network/IPC isolation;
- missing normative input/default prohibition as a cross-cutting invariant;
- source→logical relation corruption.

These are not implementation details; they are explicit boundary obligations.

Verdict:

```text
IBE-R02 = FAIL
```

Required correction:

add independent inventory entries for those boundary attacks without using I_A or O expected answers.

### IBE-R03 — EXACT_SIBLING_PAYLOAD_BINDING_NOT_CLOSED

The first correction added a common package ID/version and a common normative-source-set digest.

That prevents many mix-and-match attacks, but it does not bind the exact three frozen semantic payload revisions to one another.

Attack:

combine two individually valid artifacts produced under different corrected revisions that share:

```text
same evidence_package_id
same evidence_package_version
same normative_source_set_sha256
```

Each artifact can pass its local fingerprint while the trio did not exist as one exact reviewed package.

Verdict:

```text
IBE-R03 = FAIL
```

Required correction:

all three artifacts must carry the same top-level exact sibling map:

```text
frozen_payload_set = {
  provenance path: exact provenance frozen_semantic_payload_sha256,
  no-copy path: exact no-copy frozen_semantic_payload_sha256,
  inventory path: exact inventory frozen_semantic_payload_sha256
}
```

This binding must remain outside the payloads themselves to avoid a hash cycle, and the external breaker must verify it against the three actual frozen payload fingerprints.

---

## Second authorized correction

Correct only IBE-R01..R03:

1. mark positive A08 proof validation as unresolved/fail-closed in the pre-code evidence semantics;
2. add the missing cross-cutting boundary test inventory entries;
3. bind the exact three frozen payload fingerprints together;
4. extend the evidence breaker to validate these exact conditions;
5. update workflow hash locks;
6. perform a fresh persisted-head re-break.

No I_B production code is authorized during this correction.
