# B-PE-SEM-02 — OPERATIONAL NATIVE-BI5 SEMANTIC AUTHORITY CONTRACT — CANDIDATE

**Date:** 2026-09-21  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting live HEAD:** `7c493bc8c095211cfeb7db9aadb1825407a5bb76`  
**Status:** PERSISTED FORMALIZATION CANDIDATE — NOT YET QUALIFIED

## 0. Permission boundary

This block formalizes an operational semantic-authority contract only.

Explicitly prohibited in B-PE-SEM-02:

```text
provider contact
provider BI5 GET
new semantic-discrimination execution
FULL_INTERVAL execution
D materialization
real Q/F/Q-RM-12 full execution
backtest
paper/broker/live
```

No existing documentary adjudication is rewritten. No operational semantic proposition is declared PASS by this candidate.

## 1. Authoritative inputs preserved

This contract is downstream of and must preserve:

```text
B-PE-01 V0.1 provider-sensitive semantics contract
BPE02-ADJ-2026-09-20-V0_2
B-PE-01R PASS / VERSIONED_EMPIRICAL_SUPERSESSION
B-FIQ-01 V0.2 corrected contract
B-FIQ-02 current SemanticInvariantManifest
B-PE-SEM-01 PASS / VERSIONED_OPERATIONAL_SEMANTIC_SUCCESSOR
B-ERD-02 supported bounded run BERD02-GHA-35533153289-1
```

Current documentary truth remains:

```text
BPE-C01..C07 = BLOCKED
BPE-C08 documentary = BLOCKED
```

Current operational truth remains:

```text
OperationalSemanticRuleAdjudication = ABSENT
BPE-SEM-C01-OP..C07-OP = NOT YET PASS
B-FIQ-02 pre-execution eligibility = BLOCKED
FULL_INTERVAL execution = NOT AUTHORIZED / NOT RUN
```

B-PE-01R remains C08-only and cannot authorize C01-C07.

## 2. Contract identity and target scope

```text
contract_id =
B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY

contract_version =
B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_1_CANDIDATE
```

Target operational representation scope:

```text
provider_identity = DUKASCOPY
instrument_id = USATECHIDXUSD
representation_identity = DUKASCOPY_NATIVE_BI5_HOURLY_TICKS
representation_regime_id = K1_LEGACY_HOURLY_TICK_BI5
provider_delivery_host = datafeed.dukascopy.com
object_family = hourly {HH}h_ticks.bi5
intended_research_epoch =
  governed warmup + 2021-08-14 -> 2026-08-14 evaluation domain
```

The scope does not claim provider-canonical exhaustiveness or provider documentary truth.

Any future adjudication must bind an exact `OperationalSemanticScopeSignature` containing at minimum:

```text
provider_identity
instrument_id
representation_identity
representation_regime_id
locator_family_identity
provider_delivery_identity_policy_id + seal
temporal_applicability_statement
contract_id + contract_version
```

Scope changes require a new adjudication identity.

## 3. Governing separations

The following are hard invariants:

```text
provider normative truth
!= operational semantic authority

operational semantic authority
!= later capture satisfaction

provider-served bytes
!= semantic meaning by themselves

two project decoders agree
!= independent semantic truth

physical compatibility
!= semantic role

bounded probe support
!= full-interval continuity

rule authority
!= observation satisfying the rule

B-PE-SEM-02 PASS
!= any C01-C07 operational PASS
```

The contract therefore separates:

```text
OperationalSemanticRuleAdjudication
from
QualificationExecutionResult
```

A later execution may satisfy pre-authorized obligations. It may not create, repair, reinterpret, or expand semantic authority after observing the data.

## 4. Operational claim and dimension register

Every operational claim is a new identity. None is an alias for documentary `BPE-C01..C07`.

Dimension classes:

```text
PHYSICAL_HYPOTHESIS
SEMANTIC_ANCHOR
CONDITIONAL_RULE
PREREQUISITE_CLOSURE
SCOPE_APPLICABILITY
```

### BPE-SEM-C01-OP — compression / envelope

Operational proposition:

```text
For the target K1 object family, admitted provider object bytes are decoded
under an exact LZMA-family envelope rule whose successful output is the
physical slot byte stream.
```

Mandatory dimensions:

```text
C01-D1-OP compression family = LZMA
C01-D2-OP exact envelope/container mode used for the target K1 object family
C01-D3-OP exact stream/wrapper admission rule, including prefix/suffix and
          multi-stream disposition
C01-D4-OP decompressed output role = physical slot byte stream
```

Class: `PHYSICAL_HYPOTHESIS` for D1-D3, `SEMANTIC_ANCHOR` for D4 unless independently entailed by the exact qualified representation definition.

Successful decompression alone is insufficient. Competing materially distinct envelope hypotheses must be presealed.

### BPE-SEM-C02-OP — physical framing

Operational proposition:

```text
Qualified decompressed bytes are framed from byte zero into fixed complete
records of the authorized width, with exact residual/header/delimiter rules.
```

Mandatory dimensions:

```text
C02-D1-OP complete record width = 20 bytes
C02-D2-OP frame origin = byte zero
C02-D3-OP terminal residual/trailing-byte disposition
C02-D4-OP per-record header/delimiter presence and semantics
```

Class: `PHYSICAL_HYPOTHESIS`.

### BPE-SEM-C03-OP — primitive field layout

Operational proposition:

```text
Each complete physical record contains five fields in the qualified order,
using big-endian integer bit patterns for the first three fields and
IEEE-754 binary32 for the final two fields.
```

Mandatory dimensions:

```text
C03-D1-OP byte order = big-endian
C03-D2-OP exact five-field physical order
C03-D3-OP first three fields obey SIGNEDNESS_EQUIVALENCE_RULE_V0_1 or have
          separately qualified exact signedness authority
C03-D4-OP final two fields = IEEE-754 binary32
```

D1/D2/D4 class: `PHYSICAL_HYPOTHESIS`.

D3 class: `CONDITIONAL_RULE`.

This contract does not relabel documentary C03-D3 as PASS.

### BPE-SEM-C04-OP — timestamp semantics

Operational proposition:

```text
The first physical integer field denotes a millisecond offset from the
represented UTC H1 origin, under the exact qualified target regime.
```

Mandatory dimensions:

```text
C04-D1-OP timestamp offset unit = millisecond
C04-D2-OP reference origin = represented provider H1 object hour
C04-D3-OP hour/time basis = UTC or exact provider-equivalent mapping
C04-D4-OP valid offset domain = exact authorized domain for one H1
```

D1-D3 class: `SEMANTIC_ANCHOR`.

D4 class: `SEMANTIC_ANCHOR` plus later execution-domain satisfaction.

Range plausibility alone cannot establish D1-D3.

### BPE-SEM-C05-OP — ask/bid raw field roles

Operational proposition:

```text
The second and third integer fields represent raw ask and raw bid
respectively, and all prerequisites for qualified logical price conversion
are closed.
```

Mandatory dimensions:

```text
C05-D1-OP field roles/order = ask_raw then bid_raw
C05-D2-OP raw price integers obey SIGNEDNESS_EQUIVALENCE_RULE_V0_1 or have
          separately qualified exact signedness authority
C05-D3-OP no unresolved prerequisite semantic state exists between raw
          ask/bid fields and qualified logical price conversion
```

D1 class: `SEMANTIC_ANCHOR`.

D2 class: `CONDITIONAL_RULE`.

D3 class: `PREREQUISITE_CLOSURE`.

C05-D3-OP PASS requires current authority for all semantic prerequisites actually consumed by price conversion, including C05-D1-OP, C05-D2-OP and C06-D1-OP..D4-OP, plus any additional declared prerequisite. It cannot be satisfied by asserting that no metadata is needed.

Positive spread alone is not evidence for C05-D1-OP.

### BPE-SEM-C06-OP — USATECHIDXUSD logical price scale

Operational proposition:

```text
For the exact target instrument and authorized K1 regime,
logical ask/bid price = raw ask/bid integer / 1000.
```

Mandatory dimensions:

```text
C06-D1-OP exact applicability to USATECHIDXUSD and target K1 representation
C06-D2-OP numeric divisor = 1000
C06-D3-OP scale authority is non-circular, identity-bound, scope-bound,
          contradiction-sensitive and linked to sealed semantic evidence
C06-D4-OP temporal/version applicability covers the intended research epoch
```

D1/D2/D4 class: `SEMANTIC_ANCHOR` plus `SCOPE_APPLICABILITY`.

D3 class: `PREREQUISITE_CLOSURE`.

Explicitly insufficient:

```text
current CFD point value 0.01 alone
visual price plausibility
I_A/I_B agreement
chart resemblance
majority vote
```

### BPE-SEM-C07-OP — volume primitive / role / representation transform

Operational proposition:

```text
The fourth and fifth fields are provider-native ask-volume and bid-volume
source values encoded as IEEE-754 binary32, with the exact authorized
representation-level transform/scale.
```

Mandatory dimensions:

```text
C07-D1-OP field roles/order = ask_volume_raw then bid_volume_raw
C07-D2-OP primitive encoding = IEEE-754 binary32
C07-D3-OP exact representation-level transform/scale, including explicit
          no-additional-scale when that is the qualified rule
```

D1/D3 class: `SEMANTIC_ANCHOR`.

D2 class: `PHYSICAL_HYPOTHESIS`.

C07 remains mandatory because the current logical record carries both volume fields and O compares the complete logical payload.

Economic lots/contracts/notional interpretation is outside this contract unless it changes decoding, Q membership or governed downstream semantics.

## 5. Semantic evidence record

Every source used by this operational axis must be persisted as:

```text
OperationalSemanticEvidenceRecord
  evidence_id
  evidence_class
  publisher_or_origin_identity
  title_or_repository
  exact_locator
  source_version_or_commit
  exact_content_sha256
  retrieval_or_materialization_time
  declared_representation_scope
  declared_instrument_scope
  declared_temporal_scope
  project_origin_status
  semantic_source_lineage_id
  immutability_status
  notes_non_authoritative
```

Allowed evidence classes:

```text
OS-E-P1  provider-primary normative/documentary source
OS-E-P2  provider-maintained exact-version reference implementation
OS-E-P3  provider-direct empirical bytes/capture
OS-E-I1  independent non-project documentation/specification
OS-E-I2  independent non-project reference implementation
OS-E-X1  controlled fixture with independently established expected meaning
```

Project implementation artifacts including I_A, I_B, F, O and their direct derivatives are:

```text
INADMISSIBLE AS SEMANTIC ANCHORS
```

They may be tested later for conformance against qualified authority.

## 6. SemanticAnchorManifest

Every semantic anchor used for a `SEMANTIC_ANCHOR` or `SCOPE_APPLICABILITY` dimension must be presealed before the observation it is intended to discriminate.

Required schema:

```text
SemanticAnchorManifest
  schema
  anchor_manifest_id
  contract_id + contract_version
  scope_signature
  anchor_id
  anchor_class
  evidence_id
  evidence_exact_sha256
  source_version_or_commit
  immutable_materialization_ref
  provenance_status
  project_origin_status
  semantic_source_lineage_id
  semantic_source_identity
  semantic_source_relationship_proof_refs
  target_claim_id
  target_dimension_id
  normalized_semantic_proposition
  hypothesis_set_id_if_applicable
  expected_discriminator
  contradiction_condition
  ambiguity_condition
  failure_disposition
  admissibility_status = ADMISSIBLE | REJECTED | BLOCKED
  created_at_utc
  anchor_manifest_seal
```

Admissibility rules:

- exact source bytes must be hash-bound;
- source/version/provenance must be resolvable;
- project-origin anchors are REJECTED;
- an implementation used as semantic anchor must have separately established semantic-source lineage;
- unresolved semantic-source lineage => BLOCKED;
- an anchor created or materially modified after observing discriminating target data => REJECTED for that lineage;
- anchor scope must entail the target dimension, not merely be compatible with it.

A non-project implementation without separately established semantic-source lineage may support physical compatibility only.

## 7. SemanticHypothesisSet

Any dimension with more than one materially plausible interpretation must bind a presealed hypothesis set.

Required schema:

```text
SemanticHypothesisSet
  schema
  hypothesis_set_id
  contract_id + contract_version
  scope_signature
  target_claim_id
  target_dimension_id
  hypothesis_records[]
    hypothesis_id
    exact_interpretation
    material_effect_if_true
    discriminator_ids[]
    required_anchor_ids[]
    contradiction_condition
  completeness_rationale
  open_world_rule
  decision_rule
  created_at_utc
  hypothesis_set_seal
```

Decision rule:

```text
exactly one material hypothesis survives all authorized discriminators
  -> dimension may be eligible for PASS

zero survive
  -> FAIL when adequate authoritative evidence positively contradicts the
     candidate proposition
  -> otherwise BLOCKED

more than one material hypothesis survives
  -> BLOCKED
```

The hypothesis set is not assumed epistemically exhaustive merely because it is sealed.

Its `open_world_rule` must state:

```text
positive evidence of a materially distinct unregistered interpretation
-> OPEN reopen event
-> current authority BLOCKED
```

Post-observation material change to hypotheses/discriminators/anchors requires a new adjudication lineage.

## 8. SIGNEDNESS_EQUIVALENCE_RULE_V0_1

Rule identity:

```text
rule_id = SIGNEDNESS_EQUIVALENCE_RULE_V0_1
rule_type = CONDITIONAL_MATHEMATICAL_EQUIVALENCE
```

For an exact 32-bit field instance:

```text
if high_bit == 0:
  signed_int32(bit_pattern) == unsigned_uint32(bit_pattern)
  -> signed/unsigned ambiguity is behaviorally immaterial for that instance

if high_bit == 1:
  signed_int32(bit_pattern) != unsigned_uint32(bit_pattern)
  -> SIGNEDNESS_SEMANTIC_AMBIGUITY
  -> BLOCKED unless exact signedness has separate current authority
```

Pre-execution rule authority may be PASS if the mathematical rule, affected fields and failure behavior are correctly bound.

This does NOT prove that future or historical target records satisfy `high_bit == 0`.

Therefore every adjudication using this rule must emit an execution obligation:

```text
SIGNEDNESS_HIGH_BIT_ZERO_REQUIRED
affected_field_set
obligation_scope
on_violation = BLOCKED
```

No sampled-probe extrapolation is allowed.

The later QualificationExecutionResult may satisfy or violate the obligation. It may not change the rule.

## 9. OperationalSemanticRuleAdjudication

The authoritative pre-execution semantic object is:

```text
OperationalSemanticRuleAdjudication
  schema
  adjudication_id
  contract_id + contract_version
  scope_signature
  evidence_records[]
  semantic_anchor_manifests[]
  semantic_hypothesis_sets[]
  rule_records[]
  dimension_adjudications[]
    dimension_id
    dimension_class
    proposition
    evidence_ids[]
    anchor_ids[]
    hypothesis_set_ids[]
    rule_ids[]
    scope_mapping
    contradiction_state
    execution_obligations[]
    status = PASS | FAIL | BLOCKED
    reason_codes[]
  claim_adjudications[]
    claim_id
    mandatory_dimension_ids[]
    status = PASS | FAIL | BLOCKED
    reason_codes[]
  overall_operational_semantic_status = PASS | FAIL | BLOCKED
  execution_obligation_set[]
  evidence_set_digest
  anchor_set_digest
  hypothesis_set_digest
  rule_set_digest
  supersedes_adjudication_id
  adjudication_status
  created_at_utc
  adjudicator_identity
  adjudication_seal
```

Hard separation:

```text
OperationalSemanticRuleAdjudication.status
!= QualificationExecutionResult.status
```

A current PASS adjudication can contain unsatisfied future execution obligations only when those obligations are explicitly conditional runtime checks whose semantics are already authorized, such as signedness high-bit zero.

A dimension whose meaning itself depends on observing future data cannot be pre-authorized by converting that missing meaning into an execution obligation.

## 10. B-ERD-02 bounded evidence reuse

Only the exact persisted supported run may be considered for reuse:

```text
execution_id = BERD02-GHA-35533153289-1
source_head = 2eb8350fb24c3043017c91475d202b5e0d6bb501
workflow_run_id = 35533153289
artifact_digest =
sha256:ec36b42f01116374ce017d1d00544a2862b83845d0066110d5d01c7d3bb62f61
result_seal =
ab5c5bdf97ce3dcfa773ed555afa842443ef21b7a155057ab0e9517bb573f5ef
probe_set = PW + P0-P7
K1_supported = 9/9
```

Reuse prerequisites:

```text
exact PROVENANCE.json reverified
exact execution_result.json reverified
exact raw-body SHA256 values reverified
exact diagnostic A/B identities reverified
exact source-head and artifact digest reverified
```

Allowed reuse:

```text
bounded provider-direct physical compatibility evidence
bounded hypothesis-discrimination evidence
bounded contradiction evidence
```

Forbidden inference:

```text
FULL_INTERVAL continuity
provider documentary truth
provider-canonical representation truth
C08 supersession transfer into C01-C07
timestamp semantic meaning from range alone
ask/bid meaning from spread sign alone
/1000 scale from plausible prices alone
volume meaning from finite values alone
semantic independence merely because diagnostics A and B agree
```

Any future use must name the exact B-ERD-02 evidence record and the exact dimension for which it is used.

## 11. Semantic-source lineage and independence

Every anchor/evidence pair that contributes independent semantic authority must have a persisted lineage-resolution record:

```text
OperationalSemanticLineageResolution
  lineage_resolution_id
  evidence_ids[]
  semantic_source_lineage_ids[]
  relationship_proof_refs[]
  project_origin_checks[]
  pairwise_relationships =
    INDEPENDENT | COMMON_LINEAGE | UNRESOLVED
  reviewer_identity
  created_at_utc
  lineage_resolution_digest
```

Rules:

- fork, translation, mirror, wrapper or port of one semantic source = common lineage;
- different repositories/authors/hostnames do not prove independence;
- two implementations sharing one unstated premise do not create semantic corroboration;
- UNRESOLVED material lineage cannot be counted as independent support;
- no fixed number of lineages creates PASS by majority vote;
- evidence sufficiency is proposition-specific and must establish the targeted operational dimension under its exact scope.

## 12. Contradiction, reopen and current-authority semantics

Historical adjudications are immutable.

A material new contradiction creates:

```text
OperationalSemanticReopenEvent
  reopen_event_id
  prior_adjudication_id + seal
  trigger_evidence_ids[]
  affected_claim_ids[]
  affected_dimension_ids[]
  trigger_reason_codes[]
  status = OPEN | CLOSED
  opened_at_utc
  closed_by_adjudication_id
  reopen_event_seal
```

While a material reopen event is OPEN:

```text
prior PASS = historical evidence only
current operational semantic authority = BLOCKED
new promotion relying on prior PASS = forbidden
```

Current-authority predicate:

An OperationalSemanticRuleAdjudication is current authority only if all are true:

```text
adjudication integrity re-verifies
contract_id/version matches required consumer
scope_signature exactly matches consumer scope
all referenced evidence/anchor/hypothesis/rule identities re-verify
all PASS dimensions remain internally valid
no superseding adjudication exists
no OPEN material reopen event exists
no referenced semantic-source lineage has become unresolved/materially contradicted
all prerequisite adjudications it depends on remain current authority
```

A downstream consumer must evaluate this predicate at use time; a historical PASS label alone is insufficient.

## 13. Exact PASS / FAIL / BLOCKED semantics

### Dimension PASS

Allowed only when:

```text
exact proposition is fixed
exact target scope is bound
required evidence/anchor/hypothesis/rule objects are admissible
no unresolved material contradiction exists
all mandatory semantic prerequisites are current authority
and any future runtime obligation is only a pre-authorized conditional
satisfaction check, not a substitute for missing meaning
```

### Dimension FAIL

Used only when adequate exact-scope authoritative evidence positively establishes that the operational proposition is false or incompatible with the target regime.

FAIL must identify the contradicted proposition and evidence.

### Dimension BLOCKED

Any unresolved state, including:

```text
missing semantic anchor
unresolved lineage
scope ambiguity
temporal applicability ambiguity
multiple surviving material hypotheses
unresolved contradiction
post-hoc anchor
project-circular semantic evidence
missing prerequisite authority
integrity mismatch
unregistered material interpretation
conditional rule violation without exact fallback authority
```

### Claim PASS

```text
all mandatory dimensions PASS
AND no OPEN claim/dimension reopen event
AND exact scope/current-authority predicate passes
```

### Overall operational semantic PASS

```text
BPE-SEM-C01-OP PASS
BPE-SEM-C02-OP PASS
BPE-SEM-C03-OP PASS
BPE-SEM-C04-OP PASS
BPE-SEM-C05-OP PASS
BPE-SEM-C06-OP PASS
BPE-SEM-C07-OP PASS
AND no unresolved material cross-claim contradiction
```

No partial-majority PASS exists.

## 14. Canonical integrity rules

Structured objects use:

```text
UTF-8
sorted object keys
compact separators "," and ":"
ensure_ascii = false
allow_nan = false
duplicate object keys rejected at serialized ingress
SHA-256 lowercase hex
```

Raw evidence:

```text
SHA256(exact_bytes)
```

Set projections are sorted by canonical member bytes before hashing.

Required digests:

```text
evidence_set_digest
anchor_set_digest
hypothesis_set_digest
rule_set_digest
lineage_resolution_digest
```

Each sealed object hashes the canonical object excluding only its own seal field.

Any integrity mismatch makes the object inadmissible for authority.

## 15. QualificationExecutionResult boundary

A future execution result is a distinct object.

It may record:

```text
which pre-authorized execution obligations were evaluated
exact capture-set identity
per-obligation PASS/FAIL/BLOCKED
contradictions newly observed
integrity and provenance
```

It may NOT:

```text
add a new semantic hypothesis
invent a new anchor
change a semantic proposition
weaken a failure rule
repair a failed obligation by changing interpretation
promote plausibility into meaning
```

Any such required semantic change reopens the semantic adjudication and requires a new lineage before execution can continue.

## 16. B-FIQ-02R handoff contract

The current B-FIQ-02 package remains historical and BLOCKED.

If a future OperationalSemanticRuleAdjudication becomes current PASS, no in-place edit or seal inheritance is allowed.

A separate governed block must create:

```text
B-FIQ-02R —
SEMANTIC-AUTHORITY REFRESH OF PRE-EXECUTION PACKAGE
```

B-FIQ-02R must at minimum:

```text
fresh HEAD
bind exact OperationalSemanticRuleAdjudication ID + seal
verify current-authority predicate
materialize a NEW SemanticInvariantManifest identity
copy only explicitly authorized execution obligations
bind exact claim/dimension statuses
recompute authority_scope_tuple and digest
recompute all transitively affected package seals
preserve previous B-FIQ-02 artifacts as historical-only
adversarial break
minimal correction only if demonstrated
persisted-head final re-break
PASS / FAIL / BLOCKED
```

B-FIQ-02R PASS may establish pre-execution semantic eligibility only.

It still does not equal `FULL_INTERVAL_QUALIFIED`.

## 17. Candidate qualification boundary

B-PE-SEM-02 itself is a contract-formalization block.

A B-PE-SEM-02 PASS would prove only:

```text
the operational semantic-authority contract is sufficiently closed,
fail-closed and non-circular to govern a later semantic adjudication
```

It would NOT prove:

```text
any C01-C07 operational semantic proposition
any SemanticAnchorManifest admissible in fact
any SemanticHypothesisSet discriminated in fact
SIGNEDNESS_HIGH_BIT_ZERO over the full domain
FULL_INTERVAL_QUALIFIED
B-FIQ-02R PASS
D admissibility
backtest authorization
```

## 18. Mandatory adversarial attacks before qualification

Attack at minimum:

```text
A01 conditional execution obligation used to hide missing semantic meaning
A02 post-hoc semantic anchor laundering
A03 independent implementation with common semantic-source lineage
A04 incomplete hypothesis set treated as closed-world truth
A05 B-ERD-02 9/9 probes extrapolated to five years
A06 CFD point value / visual plausibility promoted to /1000 authority
A07 ask/bid inferred from positive spread
A08 timestamp semantics inferred from hourly range alone
A09 volume semantics bypassed or downgraded
A10 C08 empirical supersession leaked into C01-C07
A11 historical PASS reused after contradiction/reopen
A12 B-FIQ-02 current package silently reinterpreted instead of rematerialized
A13 signedness high-bit violation repaired after observation
A14 scope drift across provider/instrument/regime/epoch
A15 integrity-valid but semantically irrelevant anchor accepted
A16 majority vote across non-authoritative sources
```

No final PASS before persisted-HEAD final re-break.

STOP.
