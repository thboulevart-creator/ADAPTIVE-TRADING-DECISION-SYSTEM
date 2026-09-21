# B-PE-SEM-02 — OPERATIONAL NATIVE-BI5 SEMANTIC AUTHORITY CONTRACT — CORRECTION V0.4

**Date:** 2026-09-21  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**V0.3 corrected HEAD:** 5c0eaf700cb2b550ed9b4efbb0b4e42b743af4ef  
**V0.3 final re-break commit:** e6983a6bfa9504280107ea8884d9bdd5198cf5bf  
**Correction scope:** BPESEM02-R05 through BPESEM02-R08 only

## 0. Composite identity

The corrected normative composite becomes:

~~~text
V0.1 candidate
+
V0.2 correction
+
V0.3 correction
+
V0.4 correction
~~~

Composite identity:

~~~text
B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_4_CORRECTED
~~~

No C01-C07 semantic proposition is adjudicated or promoted by this correction.

## 1. R05 correction — governed evidence baseline and discovery horizon

A SemanticEvidenceReviewUniverse may no longer define its own inherited baseline.

Create first:

~~~text
GovernedSemanticEvidenceBaseline
  schema =
    B_PE_SEM_02_GOVERNED_SEMANTIC_EVIDENCE_BASELINE_V0_4

  baseline_id
  contract_id
  contract_version
  baseline_head
  baseline_tree_sha

  discovery_policy_id
  discovery_policy_digest

  mandatory_lineages[]
    lineage_role
    artifact_refs[]
      path
      git_blob
      sealed_identity_if_any
      sealed_digest_or_seal_if_any

  discovered_repository_artifacts[]
    path
    git_blob
    discovery_reason
    relevance_disposition
    controlling_decision_refs[]

  baseline_member_refs[]
  baseline_digest
~~~

### 1.1 Exact mandatory inherited lineages

The baseline MUST include at least these already-governed lineages when constructing the first B-PE-SEM-02 operational adjudication:

#### BPE02 documentary C01-C07 evidence/adjudication

~~~text
adjudication_id =
BPE02-ADJ-2026-09-20-V0_2

adjudication_seal =
d27771bc8c2023571b4fbbe66238dbc28b29ca69949a1db114480346f1c90a76

evidence_set_digest =
d2c9cd9a62c7f000f6821a3b04898400dbb28a363c161c0c398228aa79b6ba98

evidence bundle path =
evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json

evidence bundle git blob =
df22332709377591d73571a4940c1fda39565867
~~~

#### BPE03 legacy-hourly scope/version continuity evidence

~~~text
final adjudication seal =
90c240c2aea78fed5fd1509daecf390fd439b38376e3c3a4fc4368d19d6af2be

evidence_set_digest =
5cdf41debc110d5b5de0cedd552643300e75b2a03b305cfb9220f18c62fdf30c

evidence bundle path =
evidence/bpe03/legacy_hourly_scope_version_evidence_bundle_v0_1.json

evidence bundle git blob =
f934df8ea93018ee0c22b2d69575f15fc8f2c72f
~~~

Its C08-D4/D5 BLOCKED state is not imported as C01-C07 authority, but its provider-family / temporal-continuity evidence and limitations are mandatory visibility inputs for semantic scope applicability.

#### B-PE-01R scope firewall

~~~text
final re-break path =
reports/data-qualification/
bpe01r_empirical_evidence_sufficiency_final_rebreak_2026-09-21.md

git blob =
291841d22c6b6fabcd3c008ea67731552a5f560a
~~~

This lineage is governance authority for the C08-only supersession boundary, not semantic evidence supporting C01-C07.

#### B-PE-SEM-01 route review

~~~text
final re-break path =
reports/data-qualification/
bpesem01_semantic_authority_route_review_final_rebreak_2026-09-21.md

git blob =
dd14e843cd03e7e8fc41803a325e5a0a7636d686
~~~

The route review's identified conflicts, insufficiencies and anti-circularity constraints are mandatory inherited governance inputs.

#### Current B-FIQ semantic-block state

~~~text
path =
evidence/bfiq02/semantic_invariant_manifest_v0_1.json

git blob =
9ce3b711da6568fb412cdad116284c9300920223

manifest seal =
e0181475e7b0213eba625182b3556c39b2a4790b5491173de3dec92e60ca9f6b
~~~

This is inherited as blocked-state/governance context only. It contributes no positive C01-C07 semantic authority.

#### B-ERD-02 supported evidence when reused

If any B-ERD-02 evidence contributes to a dimension, the baseline/review universe MUST include:

~~~text
execution_id =
BERD02-GHA-35533153289-1

source_head =
2eb8350fb24c3043017c91475d202b5e0d6bb501

result_seal =
ab5c5bdf97ce3dcfa773ed555afa842443ef21b7a155057ab0e9517bb573f5ef

artifact_digest =
sha256:ec36b42f01116374ce017d1d00544a2862b83845d0066110d5d01c7d3bb62f61
~~~

### 1.2 Governed evidence discovery policy

The baseline must also execute and persist a repository discovery pass at its exact baseline HEAD.

Minimum discovery roots:

~~~text
evidence/bpe02/**
evidence/bpe03/**
evidence/bpe04/**
evidence/berd02/**
evidence/bfiq02/semantic_invariant_manifest*
reports/data-qualification/bpe01*
reports/data-qualification/bpe02*
reports/data-qualification/bpe03*
reports/data-qualification/bpe04*
reports/data-qualification/bpesem*
reports/data-qualification/berd02*
~~~

Discovery also includes any artifact explicitly referenced by a discovered artifact as:

~~~text
evidence
claim assertion
semantic source
lineage proof
scope proof
contradiction
reopen trigger
~~~

The discovery pass is not allowed to infer positive authority from filename/path membership.

Each discovered artifact receives one of:

~~~text
MATERIAL_VISIBLE
GOVERNANCE_VISIBLE
WRONG_SCOPE_PROVEN
DUPLICATE_EXACT_BYTES
BLOCKED_RELEVANCE_UNRESOLVED
~~~

A potentially C01-C07 or target-scope-relevant artifact may not be silently omitted.

If relevance cannot be resolved:

~~~text
BLOCKED_RELEVANCE_UNRESOLVED
-> semantic adjudication cannot PASS
~~~

### 1.3 Baseline integrity

~~~text
discovery_policy_digest =
SHA256(canonical_json(discovery_policy_payload_without_discovery_policy_digest))

baseline_digest =
SHA256(canonical_json(baseline_payload_without_baseline_digest))
~~~

SemanticEvidenceReviewUniverse MUST bind:

~~~text
governed_semantic_evidence_baseline_id
governed_semantic_evidence_baseline_digest
~~~

A baseline member missing from the review universe without an allowed, sealed visibility disposition makes the dimension:

~~~text
BLOCKED — GOVERNED_EVIDENCE_BASELINE_INCOMPLETE
~~~

## 2. R06 correction — visibility is separate from positive evidentiary authority

The phrase "effective review universe" is replaced by two non-interchangeable projections.

### 2.1 VisibilityUniverse

~~~text
VisibilityUniverse
  visibility_universe_id
  baseline_id + baseline_digest
  target_dimension_id

  visible_items[]
    visible_item_id
    evidence_or_assertion_ref
    exact_content_identity
    normalized_interpretation_if_any
    visibility_disposition =
      SUPPORTING_SAME_PROPOSITION |
      MATERIAL_ALTERNATIVE |
      MATERIAL_CONTRADICTION |
      GOVERNANCE_CONSTRAINT |
      WRONG_SCOPE_PROVEN |
      NONMATERIAL_PROVEN |
      BLOCKED_UNRESOLVED

    controlling_decision_refs[]

  visibility_universe_digest
~~~

Rules:

1. Every mandatory baseline item relevant to the dimension is represented.
2. Every current-adjudication evidence item is represented.
3. Evidence with zero positive authority can still be MATERIAL_ALTERNATIVE or MATERIAL_CONTRADICTION.
4. INADMISSIBLE / COMMON_LINEAGE / HISTORICAL_ONLY / NONDECISIVE do not by themselves erase the interpretation from visibility.
5. A material interpretation disappears from visibility only when a controlling sealed decision positively establishes WRONG_SCOPE_PROVEN or NONMATERIAL_PROVEN.
6. BLOCKED_UNRESOLVED keeps the dimension BLOCKED.

Digest:

~~~text
visibility_universe_digest =
SHA256(canonical_json(
  visibility_universe_payload_without_visibility_universe_digest
))
~~~

### 2.2 PositiveAuthorityUniverse

~~~text
PositiveAuthorityUniverse
  positive_authority_universe_id
  target_dimension_id
  visibility_universe_id + digest

  positive_authority_items[]
    evidence_id
    evidence_admissibility_decision_id + seal
    semantic_anchor_id_if_any
    scope_decision_id + seal
    lineage_resolution_id_if_required + digest

  positive_authority_universe_digest
~~~

Only this projection may support a PASS.

Every positive item must have:

~~~text
OperationalSemanticEvidenceAdmissibilityDecision = ADMISSIBLE
required SemanticScopeApplicabilityDecision = PASS
required lineage resolution complete
required semantic anchor/hypothesis/rule role satisfied
~~~

Digest:

~~~text
positive_authority_universe_digest =
SHA256(canonical_json(
  positive_authority_universe_payload_without_positive_authority_universe_digest
))
~~~

### 2.3 Exclusion decisions become projections, not discretionary erasure

ReviewUniverseExclusionDecision may not independently declare INADMISSIBLE, WRONG_SCOPE, COMMON_LINEAGE or NONMATERIAL.

It must reference the exact already-sealed controlling decision that establishes the disposition.

A ReviewUniverseExclusionDecision whose disposition contradicts a controlling decision is invalid.

For example:

~~~text
source admissibility = ADMISSIBLE
+
exclusion says INADMISSIBLE
-> INVALID

scope decision = PASS for same target scope
+
exclusion says WRONG_SCOPE
-> INVALID
~~~

### 2.4 KnownMaterialAlternativeRegistry input

KnownMaterialAlternativeRegistry MUST derive candidate interpretations from:

~~~text
VisibilityUniverse
~~~

not from PositiveAuthorityUniverse.

Therefore:

~~~text
zero positive authority
!=
interpretation disappears
~~~

Every MATERIAL_ALTERNATIVE becomes an included material hypothesis unless a separately sealed non-materiality/wrong-scope decision later changes its visibility disposition.

Every MATERIAL_CONTRADICTION blocks PASS until resolved.

## 3. R07 correction — evidence horizon and mandatory use-time delta review

### 3.1 SemanticEvidenceHorizon

Every OperationalSemanticRuleAdjudication must bind an evidence horizon:

~~~text
SemanticEvidenceHorizon
  horizon_id
  adjudication_id
  cutoff_head
  cutoff_tree_sha
  discovery_policy_id + digest
  governed_baseline_id + digest
  discovered_semantic_artifact_refs[]
  horizon_digest
~~~

~~~text
horizon_digest =
SHA256(canonical_json(horizon_payload_without_horizon_digest))
~~~

The adjudication seal binds horizon_id + horizon_digest.

### 3.2 CurrentAuthorityEvidenceDeltaReview

A historical PASS may be used for new promotion only after:

~~~text
CurrentAuthorityEvidenceDeltaReview
  delta_review_id
  adjudication_id + seal
  prior_horizon_id + digest
  consumer_head
  consumer_tree_sha
  descendant_relation_status
  current_discovery_policy_id + digest
  current_discovered_semantic_artifact_refs[]
  added_items[]
  modified_items[]
  deleted_bound_items[]
  per_delta_item_dispositions[]
  created_reopen_event_ids[]
  status = PASS | BLOCKED
  reviewer_identity
  created_at_utc
  delta_review_seal
~~~

Required history relation:

~~~text
consumer_head must descend from adjudication cutoff_head
under the governed branch history
~~~

If ancestry cannot be established, or relevant history was rewritten:

~~~text
BLOCKED — EVIDENCE_HISTORY_RELATION_UNRESOLVED
~~~

### 3.3 Delta dispositions

Every added/modified discovered item with plausible semantic/scope relevance must be assigned exactly one:

~~~text
WRONG_SCOPE_PROVEN
NONMATERIAL_PROVEN
DUPLICATE_EXACT_BYTES_NO_EFFECT
COMMON_LINEAGE_NO_NEW_AUTHORITY
CORROBORATING_NO_AUTHORITY_CHANGE
MATERIAL_AUTHORITY_CHANGE
MATERIAL_ALTERNATIVE
MATERIAL_CONTRADICTION
BLOCKED_UNRESOLVED
~~~

Rules:

~~~text
MATERIAL_AUTHORITY_CHANGE
MATERIAL_ALTERNATIVE
MATERIAL_CONTRADICTION
-> create OPEN OperationalSemanticReopenEvent
-> prior adjudication NON_AUTHORITATIVE_FOR_NEW_PROMOTION
-> delta review BLOCKED until superseding adjudication closes the event

BLOCKED_UNRESOLVED
-> delta review BLOCKED

deleted or byte-modified bound authority evidence
-> CAPTURE_OR_EVIDENCE_INTEGRITY_FAILURE
-> delta review BLOCKED

all items resolved with no authority-changing material state
-> delta review may PASS
~~~

No reopen event is required merely for unrelated/nonmaterial repository changes.

### 3.4 Revised current-authority predicate

Current authority now requires BOTH:

~~~text
no OPEN material reopen event
AND
PASS CurrentAuthorityEvidenceDeltaReview
for the exact consumer HEAD
~~~

Thus:

~~~text
absence of a reopen event
!= proof no reopen trigger exists
~~~

The delta review is mandatory evidence that post-adjudication changes were actually checked.

## 4. R08 correction — conditional semantic-rule scope versus representation presence

Two predicates are now formally separate.

### 4.1 SEMANTIC_RULE_SCOPE_APPLICABILITY

This is the only scope predicate B-PE-SEM-02 may adjudicate for C01-C07.

Exact meaning:

~~~text
For an object that has ALREADY been independently classified by the
later governed representation-membership process as belonging to the
exact target K1 representation/regime, the qualified semantic rule is
applicable to that object's provider/instrument/regime/temporal scope.
~~~

It answers:

~~~text
IF object/regime = K1,
which semantic rule governs interpretation?
~~~

It does NOT answer whether K1 is actually present, served, complete or continuous for any H1.

SemanticScopeApplicabilityDecision is renamed normatively to:

~~~text
SemanticRuleScopeApplicabilityDecision
~~~

and must contain:

~~~text
representation_presence_authority =
NOT_ADJUDICATED_IN_B_PE_SEM_02

c08_authority_effect =
NONE
~~~

Any other value makes the decision invalid.

### 4.2 REPRESENTATION_PRESENCE_CONTINUITY

Exact meaning:

~~~text
whether the provider actually serves/uses the target representation
for the governed interval/membership universe
~~~

This predicate is outside B-PE-SEM-02.

Its state remains governed by:

~~~text
C08-D4-OP
C08-D5-OP
BPE-C08-OP-V0.2
FULL_INTERVAL_QUALIFIED
~~~

A BPE-SEM C01-C07 PASS:

~~~text
MUST NOT
set
support directly
satisfy
or substitute for

C08-D4-OP
C08-D5-OP
BPE-C08-OP-V0.2
~~~

It may only provide the semantic-rule authority that FULL_INTERVAL later consumes when interpreting objects already observed/classified in that execution.

### 4.3 No circular prerequisite

C01-C07 semantic-rule PASS therefore requires:

~~~text
semantic rule applicability conditional on K1 classification
~~~

but does NOT require:

~~~text
FULL_INTERVAL proof that K1 is present in every required H1
~~~

Conversely, FULL_INTERVAL may not execute its semantic interpretation until the required C01-C07 semantic rule authority and B-FIQ-02R handoff are current PASS.

This yields the non-circular order:

~~~text
semantic rule authority
-> B-FIQ-02R pre-execution semantic refresh
-> FULL_INTERVAL observes/classifies actual provider objects
-> runtime obligations evaluated
-> C08 operational representation-presence/continuity adjudication
~~~

## 5. New object digest/seal domains

All new structured objects use the already-qualified canonical JSON rule.

Explicitly:

~~~text
VisibilityUniverse.visibility_universe_digest
= SHA256(canonical payload excluding only visibility_universe_digest)

PositiveAuthorityUniverse.positive_authority_universe_digest
= SHA256(canonical payload excluding only positive_authority_universe_digest)

SemanticEvidenceHorizon.horizon_digest
= SHA256(canonical payload excluding only horizon_digest)

CurrentAuthorityEvidenceDeltaReview.delta_review_seal
= SHA256(canonical payload excluding only delta_review_seal)
~~~

GovernedSemanticEvidenceBaseline and discovery-policy digest formulas are defined in Section 1.3.

All exact object IDs/digests/seals referenced by an adjudication are transitively bound by the adjudication seal.

## 6. OperationalSemanticRuleAdjudication additions

The adjudication MUST now bind:

~~~text
governed_semantic_evidence_baseline_id + digest

visibility_universe_ids[] + digests[]
positive_authority_universe_ids[] + digests[]

semantic_evidence_horizon_id + digest
~~~

Its PASS derivation uses:

~~~text
VisibilityUniverse
for known alternatives / contradictions / governance constraints

PositiveAuthorityUniverse
for positive evidence sufficiency
~~~

These roles are non-interchangeable.

## 7. B-FIQ-02R handoff amendment

B-FIQ-02R must verify current semantic authority at its own consumer HEAD through:

~~~text
OperationalSemanticRuleAdjudication ID + seal
+
PASS CurrentAuthorityEvidenceDeltaReview
for the exact B-FIQ-02R consumer HEAD
~~~

It binds only:

~~~text
C01-C07 semantic rule authority
execution obligations
semantic-rule scope
~~~

It MUST set:

~~~text
C08 operational representation-presence authority =
UNCHANGED / NOT YET PASS
~~~

No C08 promotion is possible in B-FIQ-02R.

## 8. R05-R08 closure map

~~~text
R05
-> CLOSED BY governed baseline + repository discovery horizon
   + mandatory BPE03 scope/version lineage

R06
-> CLOSED BY VisibilityUniverse / PositiveAuthorityUniverse separation
   + controlling-decision-bound exclusions
   + alternatives derived from visibility

R07
-> CLOSED BY SemanticEvidenceHorizon
   + mandatory consumer-HEAD CurrentAuthorityEvidenceDeltaReview

R08
-> CLOSED BY explicit SEMANTIC_RULE_SCOPE_APPLICABILITY
   != REPRESENTATION_PRESENCE_CONTINUITY
   + zero C08 authority effect
~~~

These are correction claims only until persisted-HEAD final re-break.

## 9. Preserved current state

Still:

~~~text
BPE-C01..C07 documentary = BLOCKED

BPE-SEM-C01-OP..C07-OP =
NOT YET ADJUDICATED / NOT YET PASS

OperationalSemanticRuleAdjudication =
ABSENT

B-FIQ-02 pre-execution eligibility =
BLOCKED

FULL_INTERVAL execution =
NOT AUTHORIZED / NOT RUN

C08-D4-OP =
NOT YET PASS

C08-D5-OP =
NOT YET PASS

BPE-C08-OP-V0.2 =
NOT YET PASS

D materialization =
NO

backtest =
NO
~~~

No provider contact, provider GET or new semantic execution occurred.

## 10. Mandatory final persisted-head re-break

Attack at minimum:

~~~text
baseline-member omission
discovery-policy shrinkage
visibility -> positive-authority collapse
free-form exclusion laundering
known-alternative disappearance
unreviewed post-adjudication evidence
fake no-reopen state
non-descendant consumer HEAD
bound-evidence deletion/mutation
C01-C07 semantic scope -> C08 leakage
C08 -> C01-C07 leakage
conditional semantic runtime deferral outside signedness
historical B-ERD-02 post-hoc decisive reuse
project-decoder self-authority
plausibility-as-semantics
execution-obligation dropping
B-FIQ in-place reinterpretation
~~~

No PASS before the persisted V0.4 composite survives that re-break.

STOP.
