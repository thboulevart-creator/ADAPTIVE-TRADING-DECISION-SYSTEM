# B-FIQ-01 — FULL-INTERVAL CONTRACT — ADVERSARIAL BREAK

Date: 2026-09-21  
Candidate HEAD: d77ee1546570dd6e6056868110d8ebb9516ed48c  
Candidate blob: 171caf891e6943d27cd8b612cf01acc5ffb34d43

## 1. Attack objective

Attempt to make a future exhaustive run appear FULL_INTERVAL_QUALIFIED while changing request membership, sharing hidden diagnostic logic, losing raw evidence, or selectively admitting only favorable evidence.

## 2. Attacks already resisted

The candidate already closes:

- sample-to-five-year extrapolation;
- omission of wall-clock closed intervals from the inventory;
- 404/zero-byte as automatic empty data;
- hidden runtime addition of K2 or another regime;
- automatic retries;
- unsealed sharding;
- transport failure as refutation;
- C01-C07 semantic bootstrapping;
- provider-atomic snapshot overclaim;
- current-authority reopening after archive mutation;
- D use of different bytes without exact hash equality.

## 3. Demonstrated defects

### BFIQ01-F01 — EXACT REQUEST MEMBERSHIP IS DERIVED AT RUNTIME, NOT SEALED

The candidate seals an IntervalInventory and RepresentationRegimeManifest, and states that every EXPECTED_OPEN interval must render one locator.

But it does not persist the complete rendered mapping before execution.

Attack:

Two implementations use the same sealed inventory and the same textual rendering rule but differ on:

- zero-indexed month handling;
- URL escaping;
- endpoint canonicalization;
- hour formatting;
- regime assignment at a boundary.

Both can claim conformance while requesting different provider objects.

The RequestBudget count still matches, so completeness can falsely PASS for the wrong object set.

Verdict:

DEMONSTRATED DEFECT.

Required correction:

Introduce a sealed pre-request RequestManifest containing exactly one row for every REQUIRED interval:

~~~text
interval_id
interval_ordinal
regime_id
exact_request_locator
provider_delivery_endpoint_identity
request_expected = true
~~~

and one explicit no-request row for every CLOSED interval.

The RequestManifest root must be included in RequestBudget, shard plan, execution result, capture-set leaves and authority_scope_tuple.

No runtime locator rendering may be authoritative after the RequestManifest is sealed.

---

### BFIQ01-F02 — DIAGNOSTIC INDEPENDENCE IS ASSERTED, NOT EVIDENTIALLY CLOSED

The candidate requires two independent paths and exact executable identities/versions, but it defines no artifact proving code-level separation.

Attack:

Diagnostic A and B use different decompressors but share:

- the same parser helper;
- the same field projection helper;
- the same invariant evaluator;
- or generated/copied code.

Their outputs agree perfectly while one common defect survives both.

Version strings do not establish independence.

Verdict:

DEMONSTRATED DEFECT.

Required correction:

Introduce a sealed DiagnosticIndependenceManifest that binds:

- exact source/runtime blob hashes for each path;
- decompressor identity/version/hash;
- parser implementation identity/hash;
- invariant-evaluator identity/hash;
- forbidden shared semantic helper inventory;
- relationship analysis;
- independence verdict per material stage.

Allowed shared material must be limited to immutable schemas/constants whose semantics are already current-authority qualified and explicitly listed.

If parser/projection/invariant logic shares a material implementation lineage:

~~~text
INDEPENDENCE = BLOCKED
~~~

and FULL_INTERVAL_QUALIFIED cannot PASS.

---

### BFIQ01-F03 — DURABLE STORAGE POLICY HAS NO CLOSED IDENTITY OR SCOPE BINDING

The candidate says durable storage classes must be declared before execution and that durable storage is immutable after first request.

But no DurableEvidencePolicy schema/seal exists, and authority_scope_tuple does not bind one.

Attack:

Qualification runs under storage policy A.

After execution, body references are migrated to policy B with different retention/retrievability semantics.

The same operational adjudication and tuple still appear valid.

A later audit cannot recover exact bytes, but the policy change itself is not scope-detectable until retrieval fails.

Verdict:

DEMONSTRATED DEFECT.

Required correction:

Define sealed DurableEvidencePolicy with:

- policy ID/version;
- allowed storage classes;
- content-addressing rule;
- immutability/versioning rule;
- retention requirement;
- recovery verification method;
- access/audit requirement;
- object-reference encoding rule;
- credential non-persistence rule.

Bind policy ID/seal into:

- every evidence-object record;
- QualificationExecutionResult;
- CompletenessProof;
- authority_scope_tuple.

Policy change requires new adjudication lineage.

---

### BFIQ01-F04 — NO CLOSED EXECUTION EVIDENCE-SET MEMBERSHIP OBJECT

The candidate defines captures, diagnostics, leaves, CompletenessProof and adjudication, but no single sealed object states exactly which evidence records constitute the exhaustive execution.

Attack:

A failing DiagnosticResult exists for interval X.

A favorable duplicate/recomputed result is used in the capture-set leaf.

The CompletenessProof re-verifies the selected leaf/root but there is no closed evidence-set membership digest proving that all execution-produced captures/diagnostics were admitted exactly once.

Selective evidence admission can therefore be hidden.

Verdict:

DEMONSTRATED DEFECT.

Required correction:

Introduce sealed QualificationExecutionResult containing:

- all pre-request artifact IDs/seals;
- exact execution lineage identity;
- exact set of all TransportCapture IDs/seals;
- exact set of all Diagnostic A IDs/seals;
- exact set of all Diagnostic B IDs/seals;
- per-interval terminal record IDs/seals;
- durable evidence object IDs/seals;
- request count;
- shard completion state;
- evidence_set_digest;
- capture-set root;
- overall FULL_INTERVAL verdict candidate.

The evidence_set_digest must be canonical over every produced execution evidence identity, not only favorable/admitted records.

CompletenessProof and adjudication must bind the exact QualificationExecutionResult ID/seal/digest.

Duplicate, omitted or unbound execution evidence blocks qualification.

## 4. Break verdict

~~~text
B-FIQ-01 CONTRACT CANDIDATE = FAIL
~~~

Only BFIQ01-F01 through F04 are authorized for correction.

No provider request, exhaustive qualification, D materialization or backtest occurred.
