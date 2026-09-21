# B-PE-SEM-02 — OPERATIONAL NATIVE-BI5 SEMANTIC AUTHORITY CONTRACT — CORRECTION V0.3

**Date:** 2026-09-21  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**Parent corrected HEAD:** d6e35d6f5fb56c4a082e79d98f23c2afe356cc40  
**Persisted re-break commit:** c3c27c5cf24bd749d595da61cc2b66de9ee416e4  
**Correction scope:** BPESEM02-R01 through BPESEM02-R04 only

## 0. Composite identity

The corrected normative composite becomes:

~~~text
V0.1 candidate
+
V0.2 correction
+
V0.3 correction
~~~

Composite identity:

~~~text
B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_3_CORRECTED
~~~

No semantic proposition is promoted by this correction.

## 1. R01 correction — contract-locked DimensionAuthorityBasisRegister

Create:

~~~text
DimensionAuthorityBasisRegister
  schema =
    B_PE_SEM_02_DIMENSION_AUTHORITY_BASIS_REGISTER_V0_3
  basis_register_id
  claim_dimension_register_id
  claim_dimension_register_digest
  dimension_bases[]
    dimension_id
    primary_authority_class
    required_scope_applicability = true
    exact_prerequisite_dimension_ids[]
    allowed_conditional_semantic_rule_ids[]
    allowed_obligation_modes[]
    required_authority_roles[]
  created_at_utc
  basis_register_digest
~~~

Digest:

~~~text
basis_register_digest =
SHA256(canonical_json(basis_register_payload_without_basis_register_digest))
~~~

Every OperationalSemanticRuleAdjudication MUST bind:

~~~text
dimension_authority_basis_register_id
dimension_authority_basis_register_digest
~~~

and must use the exact basis for every registered dimension.

### 1.1 Exact primary-class map

~~~text
C01-D1-OP  PHYSICAL_HYPOTHESIS
C01-D2-OP  PHYSICAL_HYPOTHESIS
C01-D3-OP  PHYSICAL_HYPOTHESIS
C01-D4-OP  SEMANTIC_ANCHOR

C02-D1-OP  PHYSICAL_HYPOTHESIS
C02-D2-OP  PHYSICAL_HYPOTHESIS
C02-D3-OP  PHYSICAL_HYPOTHESIS
C02-D4-OP  PHYSICAL_HYPOTHESIS

C03-D1-OP  PHYSICAL_HYPOTHESIS
C03-D2-OP  PHYSICAL_HYPOTHESIS
C03-D3-OP  CONDITIONAL_RULE
C03-D4-OP  PHYSICAL_HYPOTHESIS

C04-D1-OP  SEMANTIC_ANCHOR
C04-D2-OP  SEMANTIC_ANCHOR
C04-D3-OP  SEMANTIC_ANCHOR
C04-D4-OP  SEMANTIC_ANCHOR

C05-D1-OP  SEMANTIC_ANCHOR
C05-D2-OP  CONDITIONAL_RULE
C05-D3-OP  PREREQUISITE_CLOSURE

C06-D1-OP  SEMANTIC_ANCHOR
C06-D2-OP  SEMANTIC_ANCHOR
C06-D3-OP  PREREQUISITE_CLOSURE
C06-D4-OP  SEMANTIC_ANCHOR

C07-D1-OP  SEMANTIC_ANCHOR
C07-D2-OP  PHYSICAL_HYPOTHESIS
C07-D3-OP  SEMANTIC_ANCHOR
~~~

### 1.2 Exact prerequisite map

All dimensions have no cross-dimension prerequisite unless listed here.

~~~text
C05-D3-OP prerequisites =
  C05-D1-OP
  C05-D2-OP
  C06-D1-OP
  C06-D2-OP
  C06-D3-OP
  C06-D4-OP
~~~

C06-D3-OP has no cross-dimension shortcut. Its PREREQUISITE_CLOSURE role is satisfied only by its required authority roles:

~~~text
admissible exact semantic evidence
sealed SemanticAnchorManifest
resolved semantic-source lineage
PASS SemanticScopeApplicabilityDecision
no unresolved material contradiction
~~~

### 1.3 Exact conditional-semantic obligation policy

For all dimensions except C03-D3-OP and C05-D2-OP:

~~~text
allowed_conditional_semantic_rule_ids = []
allowed_obligation_modes =
  CONFORMANCE_ONLY
~~~

For:

~~~text
C03-D3-OP
C05-D2-OP
~~~

the exact rule allowance is:

~~~text
allowed_conditional_semantic_rule_ids =
  SIGNEDNESS_EQUIVALENCE_RULE_V0_1

allowed_obligation_modes =
  CONFORMANCE_ONLY
  CONDITIONAL_SEMANTIC_SIGNEDNESS
~~~

No other dimension may defer missing semantic meaning into a runtime obligation under V0.3.

CONFORMANCE_ONLY means:

~~~text
runtime may test observed bytes against meaning already independently authorized
runtime may not create or choose that meaning
~~~

Any adjudication whose basis differs from this register is:

~~~text
BLOCKED — DIMENSION_AUTHORITY_BASIS_REGISTER_MISMATCH
~~~

## 2. R02 correction — exact full-domain scope identity

OperationalSemanticScopeSignature V0.2 is amended with:

~~~text
session_calendar_contract =
DUKASCOPY_USATECH_SESSION_CALENDAR_V3

session_calendar_path =
tools/dukascopy_usatech_calendar.py

session_calendar_git_blob =
fab634aab7b8c299b0139c3c43bf5b89a2aa03d0

full_domain_first_h1 =
2021-08-13T01:00:00Z

full_domain_last_h1 =
2026-08-14T20:00:00Z

wall_clock_interval_count =
43868

expected_open_interval_count =
29543

expected_closed_interval_count =
14325

warmup_open_interval_count =
20

evaluation_open_interval_count =
29523

interval_inventory_path =
evidence/bfiq02/interval_inventory_v0_1.json

interval_inventory_git_blob =
8c02972228941d8b6f1aacaf9ac6bf75fb0f2029

interval_inventory_sha256_raw_bytes =
7f55d600d9bfcab804283d668a9f74b555e55cc6c98a99919e0012c08f038f5d

interval_inventory_root =
26d86a34a00e6697208a6481867f6338f21c1deae26e5be74b52cc8ba83eced8
~~~

These imported identities use only the B-FIQ-02 structural/integrity-qualified domain.

They do NOT import:

~~~text
B-FIQ-02 SemanticInvariantManifest authority
B-FIQ-02 pre-execution eligibility
FULL_INTERVAL_QUALIFIED
~~~

Any change to the calendar, full-domain bounds, counts, inventory bytes or inventory root requires a new OperationalSemanticScopeSignature and therefore a new semantic adjudication.

## 3. R03 correction — SemanticEvidenceReviewUniverse

KnownMaterialAlternativeRegistry may not choose its own evidence universe.

Create:

~~~text
SemanticEvidenceReviewUniverse
  schema =
    B_PE_SEM_02_SEMANTIC_EVIDENCE_REVIEW_UNIVERSE_V0_3
  review_universe_id
  target_dimension_id
  cutoff_head
  cutoff_time
  mandatory_inherited_evidence_refs[]
  current_adjudication_evidence_ids[]
  reopen_or_contradiction_evidence_ids[]
  exclusion_decisions[]
  effective_review_evidence_ids[]
  review_universe_digest
~~~

Mandatory inherited evidence for every relevant C01-C07 dimension includes, when dimension-relevant:

~~~text
BPE02-ADJ-2026-09-20-V0_2
adjudication seal =
d27771bc8c2023571b4fbbe66238dbc28b29ca69949a1db114480346f1c90a76

BPE02 evidence_set_digest =
d2c9cd9a62c7f000f6821a3b04898400dbb28a363c161c0c398228aa79b6ba98

B-PE-SEM-01 final route review / correction / re-break
including already-identified signedness, timestamp, side,
USATECH-scale and volume limitations/conflicts

BERD02-GHA-35533153289-1
whenever any B-ERD-02 evidence is reused in the current dimension
~~~

Rules:

1. Every current-adjudication evidence record is included.
2. Every evidence/assertion from BPE02 already mapped to the same documentary claim/dimension is inherited into the review universe, even if it is not positive authority under this operational contract.
3. Existing governed contradictory or alternative evidence cannot be silently omitted.
4. A mandatory inherited item may be excluded from effective positive authority only through a separately sealed exclusion decision.
5. Exclusion as IRRELEVANT is forbidden when the inherited artifact contains an assertion mapped to the same underlying C01-C07 dimension and target proposition; it may instead be classified as INADMISSIBLE, WRONG_SCOPE, HISTORICAL_ONLY, COMMON_LINEAGE or NONDECISIVE, with reasons.
6. BLOCKED exclusion status keeps the KnownMaterialAlternativeRegistry BLOCKED.

Exclusion decision:

~~~text
ReviewUniverseExclusionDecision
  exclusion_id
  target_dimension_id
  evidence_or_assertion_ref
  disposition =
    INADMISSIBLE |
    WRONG_SCOPE |
    HISTORICAL_ONLY |
    COMMON_LINEAGE |
    NONDECISIVE |
    BLOCKED_UNRESOLVED
  reason_codes[]
  evidence_refs[]
  reviewer_identity
  exclusion_seal
~~~

Digest:

~~~text
review_universe_digest =
SHA256(canonical_json(review_universe_payload_without_review_universe_digest))
~~~

KnownMaterialAlternativeRegistry MUST bind:

~~~text
semantic_evidence_review_universe_id
semantic_evidence_review_universe_digest
~~~

and MUST derive its candidate interpretations from the complete effective review universe.

If a dimension-relevant mandatory inherited item is absent without a valid exclusion decision:

~~~text
BLOCKED — REVIEW_UNIVERSE_INCOMPLETE
~~~

This does not claim omniscience about unknown future external evidence.

The existing open-world/reopen rule remains mandatory for genuinely new evidence.

## 4. R04 correction — remaining exact digest domains

### 4.1 Scope signature

~~~text
scope_signature_digest =
SHA256(canonical_json(
  scope_signature_payload_without_scope_signature_digest
))
~~~

### 4.2 Lineage resolution

OperationalSemanticLineageResolution is amended to require:

~~~text
covered_evidence_ids[]
covered_semantic_source_ids[]
pairwise_relationships[]
relationship_proof_refs[]
project_origin_checks[]
reviewer_identity
created_at_utc
lineage_resolution_digest
~~~

Digest:

~~~text
lineage_resolution_digest =
SHA256(canonical_json(
  lineage_resolution_payload_without_lineage_resolution_digest
))
~~~

Every evidence ID or semantic source relied upon for independent semantic authority must appear in at least one applicable lineage-resolution record.

An uncovered required lineage:

~~~text
BLOCKED — SEMANTIC_LINEAGE_RESOLUTION_INCOMPLETE
~~~

## 5. Adjudication schema additions

OperationalSemanticRuleAdjudication must now also bind:

~~~text
dimension_authority_basis_register_id
dimension_authority_basis_register_digest

semantic_evidence_review_universe_ids[]
semantic_evidence_review_universe_digests[]
~~~

Its adjudication seal transitively binds these fields.

The current-authority predicate must reverify:

~~~text
ClaimDimensionRegister
DimensionAuthorityBasisRegister
OperationalSemanticScopeSignature
all evidence admissibility decisions
all SemanticEvidenceReviewUniverse objects
all KnownMaterialAlternativeRegistry objects
all anchors/hypotheses/rules
all scope decisions
all historical eligibility records
all lineage records
all execution obligations
all set digests
adjudication seal
reopen state
~~~

## 6. Corrected defect map

~~~text
R01
-> CLOSED BY contract-locked DimensionAuthorityBasisRegister
   and exact conditional-semantic obligation policy

R02
-> CLOSED BY session-calendar + exact full-domain + IntervalInventory binding

R03
-> CLOSED BY mandatory inherited SemanticEvidenceReviewUniverse

R04
-> CLOSED BY exact scope-signature and lineage digest formulas
~~~

These closure claims remain unqualified until final persisted-head re-break.

## 7. No authority promotion

Still:

~~~text
BPE-C01..C07 documentary = BLOCKED
BPE-SEM-C01-OP..C07-OP = NOT YET ADJUDICATED
OperationalSemanticRuleAdjudication = ABSENT
B-FIQ-02 pre-execution eligibility = BLOCKED
FULL_INTERVAL execution = NOT AUTHORIZED / NOT RUN
~~~

No provider contact or provider GET occurred.

## 8. Mandatory final re-break

Attack the persisted V0.3 composite for at least:

~~~text
dimension omission
basis weakening
semantic meaning deferred as runtime obligation
calendar/warmup scope drift
review-universe shrinking
known-alternative omission
historical B-ERD-02 post-hoc reuse
digest/seal ambiguity
lineage omission
execution-obligation dropping
C08 authority leakage
project self-authority
plausibility-as-semantics
B-FIQ in-place reinterpretation
reopen bypass
~~~

Only a persisted-HEAD re-break with zero demonstrated material defects may qualify the contract.

STOP.
