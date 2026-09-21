# B-PE-SEM-01 — C01-C07 SEMANTIC AUTHORITY ROUTE REVIEW — CORRECTION V0.2

**Date:** 2026-09-21  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Parent candidate HEAD:** `af0a078732d0ed02e747f83cc70a660af729ffc4`  
**Adversarial break HEAD:** `bd76b01985d4a0e05104226ce6c4be57d4413c23`  
**Status:** CORRECTED PERSISTED CANDIDATE — FINAL PERSISTED-HEAD RE-BREAK REQUIRED

This correction changes only defects BPESEM01-F01 through F08 demonstrated by the adversarial break.

No provider contact, provider GET, FULL_INTERVAL execution, D materialization, real Q/F/Q-RM-12 execution, backtest or paper/broker/live execution is authorized or performed.

## 1. F01/F04 correction — separate semantic-rule authority from later capture satisfaction

The successor route SHALL distinguish two non-substitutable objects.

### 1.1 OperationalSemanticRuleAdjudication

This is the pre-execution authority object.

It states exactly which semantic rules may be used as decisive invariants and why those rules have authority before exhaustive provider capture.

Minimum state:

```text
operational_semantic_rule_adjudication_id
schema_version
provider_identity
instrument_identity
representation_regime_identity

semantic_rule_records[]
  rule_id
  source_claim_id
  operational_dimension_id
  proposition
  applicability_scope
  evidence_bindings[]
  semantic_anchor_manifest_id_or_null
  semantic_hypothesis_set_id_or_null
  contradiction_rule
  failure_disposition
  status = PASS | FAIL | BLOCKED

evidence_set_digest
adjudication_seal
current_authority_status
reopen_state
```

A rule may be current authority before future provider objects are tested against it.

### 1.2 QualificationExecutionResult

This is later execution evidence.

It records whether the exact sealed FULL_INTERVAL capture set satisfies the already-authorized rules.

It SHALL NOT create, alter, or repair semantic rules after observation.

Therefore:

```text
OperationalSemanticRuleAdjudication
!= QualificationExecutionResult

semantic rule authority
!= observed satisfaction of that rule
```

B-FIQ may use only a current-authority OperationalSemanticRuleAdjudication as the source of decisive invariants.

FULL_INTERVAL later evaluates those invariants against each applicable captured object.

## 2. F01 correction — exact signedness behavioral-equivalence rule

The separately versioned operational successor may avoid claiming provider-declared signedness only through this predeclared conditional rule:

```text
SIGNEDNESS_EQUIVALENCE_RULE_V0_1

For a 32-bit field whose candidate signed and unsigned interpretations
would otherwise differ:

if high_bit == 0:
    signed_value == unsigned_value
    -> numeric interpretation ambiguity is behaviorally immaterial
       for that exact field instance

if high_bit == 1:
    -> SIGNEDNESS_SEMANTIC_AMBIGUITY
    -> BLOCKED unless exact signedness has independently acquired
       current semantic authority
```

Authority of this conditional rule is mathematical and may be adjudicated before FULL_INTERVAL execution.

Later FULL_INTERVAL execution supplies only the per-field satisfaction evidence.

No sampled low-value probe can establish full-domain satisfaction.

Application:

```text
C03-D3-OP:
first three 32-bit fields are decoded under the exact accepted numeric
interpretation; when provider-declared signedness is unresolved, every
material accepted instance must satisfy SIGNEDNESS_EQUIVALENCE_RULE_V0_1.

C05-D2-OP:
raw ask/bid numeric values use the same rule; any high-bit-one accepted
price field blocks qualification until signedness is independently resolved.
```

For timestamp offsets, the separately authorized timestamp-domain rule may imply high-bit zero when offset is constrained below 3,600,000; nevertheless the decisive timestamp semantics themselves remain subject to C04 operational authority.

This rule does not convert documentary BPE-C03/C05 signedness dimensions to PASS.

## 3. F02 correction — sealed SemanticAnchorManifest

Before any semantic-discrimination evidence is collected or reused, the successor contract SHALL require a sealed manifest:

```text
schema =
B_PE_SEM_OPERATIONAL_SEMANTIC_ANCHOR_MANIFEST_V0_1

semantic_anchor_manifest_id
contract_id
contract_version

anchors[]
  anchor_id
  evidence_class
  publisher_or_origin_identity
  source_locator
  source_version_or_commit
  exact_content_sha256
  immutable_materialization_ref
  provenance_status
  lineage_group_id
  lineage_resolution_ref
  project_origin_check

  target_operational_claim_id
  target_operational_dimension_id
  semantic_hypothesis_set_id
  semantic_hypothesis_set_seal

  expected_semantic_meaning
  expected_discriminating_observation
  contradiction_outcome
  ambiguity_outcome

  capture_or_retrieval_policy
  admissibility_status =
    ADMISSIBLE | REJECTED | BLOCKED
  reason_codes[]

created_at_utc
manifest_seal
```

Rules:

```text
unsealed anchor introduced after observation -> REJECTED
project I_A/I_B/F/O or direct derivative -> REJECTED as semantic anchor
unresolved lineage -> BLOCKED
non-immutable/unverifiable evidence identity -> BLOCKED
anchor scope not covering target dimension -> BLOCKED
material contradiction -> OPEN / BLOCKED
```

The manifest may contain a bounded provider-direct empirical anchor only when the proposition being tested is empirically discriminable without assuming the candidate semantic interpretation.

## 4. F03 correction — sealed SemanticHypothesisSet

Every material ambiguity used by the operational successor SHALL be frozen prospectively in:

```text
schema =
B_PE_SEM_SEMANTIC_HYPOTHESIS_SET_V0_1

semantic_hypothesis_set_id
target_operational_claim_id
target_operational_dimension_id

hypotheses[]
  hypothesis_id
  exact_normative_description
  interpretation_rule_identity_or_null
  interpretation_rule_sha256_or_null
  expected_discriminators[]
  contradiction_conditions[]

decision_rule
  exactly_one_survives -> eligible for adjudication
  zero_survive -> FAIL or BLOCKED according to declared cause
  multiple_material_hypotheses_survive -> BLOCKED

created_at_utc
hypothesis_set_seal
```

After evidence observation:

```text
add/remove/edit material hypothesis
-> adjudication reopen
-> old result historical only
```

No adaptive hypothesis repair is allowed.

## 5. F05 correction — bounded reuse of B-ERD-02 exact provider captures

Existing B-ERD-02 provider-direct evidence may be reused only as bounded evidence.

Named historical execution:

```text
execution_id = BERD02-GHA-35533153289-1
source HEAD = 2eb8350fb24c3043017c91475d202b5e0d6bb501
result seal = ab5c5bdf97ce3dcfa773ed555afa842443ef21b7a155057ab0e9517bb573f5ef
artifact digest = sha256:ec36b42f01116374ce017d1d00544a2862b83845d0066110d5d01c7d3bb62f61
probe set = PW + P0-P7
```

Reuse eligibility requires, before semantic use:

```text
exact evidence identities/hashes reverify
provider-origin binding reverify
capture provenance remains intact
successor SemanticAnchorManifest explicitly names each reused evidence object
target semantic dimension is within the declared bounded purpose
```

Hard prohibitions:

```text
9 probes -> no FULL_INTERVAL continuity inference
probe compatibility -> no representation-wide semantic truth by itself
B-PE-01R C08 operational authority -> no transfer to C01-C07
no new provider request is implied by reuse
```

If exact historical bytes required for a proposed discriminator are not durably available, that discriminator is BLOCKED rather than reconstructed from summaries.

## 6. F06 correction — exact operational replacements for evidence-method-coupled dimensions

The original documentary dimensions remain unchanged.

The separately versioned operational successor may define these distinct dimensions.

### C05-D3-OP — price-conversion prerequisite closure

```text
For the exact target representation regime, no unresolved prerequisite
semantic state exists between the qualified raw ask/bid fields and the
qualified logical price conversion.

PASS requires:
- ask/bid field-role authority PASS;
- numeric interpretation rule authority PASS;
- target price-scale rule authority PASS;
- every additional prerequisite explicitly enumerated and PASS;
- no hidden provider-metadata dependency whose unresolved value could
  change the decoded logical price.
```

This does not assert that original documentary C05-D3 has PASSed.

### C06-D3-OP — operational scale authority

```text
For USATECHIDXUSD in the exact governed representation regime,
logical ask/bid price = raw integer / 1000 is authorized by one
current OperationalSemanticRuleAdjudication that is:

- non-circular;
- identity-bound;
- scope-bound to USATECHIDXUSD and the exact regime;
- linked to a sealed SemanticAnchorManifest and, where ambiguity exists,
  a sealed SemanticHypothesisSet;
- contradiction-sensitive;
- subject to reopen semantics.
```

Explicitly insufficient:

```text
current CFD point value 0.01 alone
visual price plausibility
I_A/I_B agreement
chart resemblance
majority vote across independent parsers
```

This does not assert that original documentary C06-D3 has PASSed.

## 7. F08 correction — non-project reference implementation boundary

A non-project reference implementation can be used in two different roles.

### Physical-compatibility role

Allowed when exact version/content/provenance are pinned.

It may corroborate behavior such as byte order, record width, or parser acceptance.

### Semantic-anchor role

Allowed only when the implementation's expected semantic meaning is itself supported by a separately identified semantic source lineage.

Required:

```text
reference implementation identity
+
semantic source identity
+
relationship proof
+
lineage resolution showing semantic expectation was not derived
from I_A/I_B/F/O or from the candidate project's interpretation
```

Without that separately established semantic source lineage:

```text
reference implementation
-> physical compatibility evidence only
-> cannot solely authorize timestamp meaning
-> cannot solely authorize ask/bid orientation
-> cannot solely authorize USATECH scale
-> cannot solely authorize volume role/transform
```

Common-premise agreement therefore remains non-authoritative for semantic meaning.

## 8. F07 correction — exact B-FIQ reopen/rematerialization effect

The currently sealed B-FIQ-02 package remains historically valid evidence of what was materialized and tested, but its semantic authority state remains BLOCKED.

If a future B-PE-SEM successor creates a different semantic-authority identity:

```text
current evidence/bfiq02/semantic_invariant_manifest_v0_1.json
-> HISTORICAL_ONLY for new promotion

current B-FIQ-02 provisional authority_scope_tuple
-> HISTORICAL_ONLY for new promotion

current B-FIQ-02 pre-execution eligibility
-> remains BLOCKED
```

No in-place reinterpretation or seal inheritance is allowed.

A later governed refresh must create a new identity, e.g.:

```text
B-FIQ-02R — semantic-authority refresh of pre-execution package
```

and must at minimum:

```text
fresh HEAD
bind exact OperationalSemanticRuleAdjudication ID + seal
materialize a new SemanticInvariantManifest
recompute authority-scope tuple and digest
recompute any package seal transitively affected
adversarial break
persist corrections if demonstrated
persisted-head final re-break
PASS / FAIL / BLOCKED
```

Only after that separate refresh can pre-execution eligibility change.

## 9. Corrected route decision

The B-PE-SEM-01 review decision candidate is now:

```text
DECISION =
VERSIONED_OPERATIONAL_SEMANTIC_SUCCESSOR
```

Meaning:

```text
B-PE-01/BPE02 documentary C01-C07 authority
= UNCHANGED / BLOCKED

new operational semantic authority axis
= justified as a contract route
= NOT YET FORMALIZED
= NOT YET EXECUTED
= NOT YET PASS

B-FIQ-02 current pre-execution eligibility
= BLOCKED
```

This review qualifies only whether that route is logically admissible and sufficiently bounded.

It does not qualify any C01-C07 operational semantic proposition.

## 10. Required B-PE-SEM-02 boundary if this review later PASSes

Exactly one next governed block may be:

```text
B-PE-SEM-02 —
OPERATIONAL NATIVE-BI5 SEMANTIC AUTHORITY CONTRACT
```

Formalization only.

It must formalize, at minimum:

```text
OperationalSemanticRuleAdjudication schema
SemanticAnchorManifest schema
SemanticHypothesisSet schema
C01-C07 operational claim/dimension register
signedness conditional-equivalence rule
contradiction/reopen/current-authority rules
B-ERD-02 bounded evidence-reuse rule
exact PASS / FAIL / BLOCKED semantics
future B-FIQ-02R handoff contract
```

Still prohibited in B-PE-SEM-02 unless separately authorized later:

```text
provider contact
provider BI5 GET
new semantic discrimination execution
FULL_INTERVAL execution
D materialization
backtest
paper/broker/live
```

## 11. Correction status

```text
BPESEM01-F01 = CLOSED BY CORRECTION
BPESEM01-F02 = CLOSED BY CORRECTION
BPESEM01-F03 = CLOSED BY CORRECTION
BPESEM01-F04 = CLOSED BY CORRECTION
BPESEM01-F05 = CLOSED BY CORRECTION
BPESEM01-F06 = CLOSED BY CORRECTION
BPESEM01-F07 = CLOSED BY CORRECTION
BPESEM01-F08 = CLOSED BY CORRECTION
```

These closure claims are candidate claims only.

A persisted-HEAD final adversarial re-break is mandatory before any B-PE-SEM-01 PASS.

STOP.
