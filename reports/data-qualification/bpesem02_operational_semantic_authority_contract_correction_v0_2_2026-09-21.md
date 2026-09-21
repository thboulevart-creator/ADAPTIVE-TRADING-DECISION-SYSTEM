# B-PE-SEM-02 — OPERATIONAL NATIVE-BI5 SEMANTIC AUTHORITY CONTRACT — CORRECTION V0.2

**Date:** 2026-09-21  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**Parent candidate commit:** b24b85740ed1d2a060ec3a9a2a254dbe332edccc  
**Parent candidate blob:** 092aae41821afb69d7fb84da095d1c8c0bfacb3d  
**Adversarial break commit:** e51eba617cab309b2f6f5d878d74ab506d7dc2fd  
**Correction scope:** BPESEM02-F01 through BPESEM02-F07 only

## 0. Composite identity

The corrected contract is the normative composite:

~~~text
candidate V0.1
+
this correction V0.2
~~~

Composite identity:

~~~text
B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_2_CORRECTED
~~~

Everything not explicitly changed below remains governed by the parent candidate.

This correction does not create any C01-C07 semantic PASS and performs no provider execution.

## 1. F01 correction — immutable ClaimDimensionRegister

A future adjudication may not supply its own mandatory-dimension universe.

Create and bind:

~~~text
ClaimDimensionRegister
  schema =
    B_PE_SEM_02_CLAIM_DIMENSION_REGISTER_V0_2
  register_id
  contract_id
  contract_version
  claims[]
    claim_id
    exact_claim_proposition
    mandatory_dimensions[]
      dimension_id
      exact_dimension_proposition
      dimension_class
      prerequisite_dimension_ids[]
      future_execution_obligation_allowed = true | false
  created_at_utc
  register_digest
~~~

The register content is exactly the C01-C07 operational register defined by the parent candidate, including:

~~~text
BPE-SEM-C01-OP
  C01-D1-OP
  C01-D2-OP
  C01-D3-OP
  C01-D4-OP

BPE-SEM-C02-OP
  C02-D1-OP
  C02-D2-OP
  C02-D3-OP
  C02-D4-OP

BPE-SEM-C03-OP
  C03-D1-OP
  C03-D2-OP
  C03-D3-OP
  C03-D4-OP

BPE-SEM-C04-OP
  C04-D1-OP
  C04-D2-OP
  C04-D3-OP
  C04-D4-OP

BPE-SEM-C05-OP
  C05-D1-OP
  C05-D2-OP
  C05-D3-OP

BPE-SEM-C06-OP
  C06-D1-OP
  C06-D2-OP
  C06-D3-OP
  C06-D4-OP

BPE-SEM-C07-OP
  C07-D1-OP
  C07-D2-OP
  C07-D3-OP
~~~

A future OperationalSemanticRuleAdjudication MUST contain:

~~~text
claim_dimension_register_id
claim_dimension_register_digest
~~~

and those values must exactly match the qualified register.

Claim status is derived from the register, not from adjudicator-supplied mandatory_dimension_ids.

Any:

~~~text
missing registered dimension
extra unregistered dimension
changed proposition
changed class
changed prerequisite set
changed obligation permission
register digest mismatch
~~~

makes the adjudication:

~~~text
BLOCKED — CLAIM_DIMENSION_REGISTER_MISMATCH
~~~

## 2. F02 correction — source admissibility and class-specific authority basis

### 2.1 OperationalSemanticEvidenceAdmissibilityDecision

Every OperationalSemanticEvidenceRecord must have exactly one separately sealed decision:

~~~text
OperationalSemanticEvidenceAdmissibilityDecision
  schema =
    B_PE_SEM_02_EVIDENCE_ADMISSIBILITY_DECISION_V0_2
  decision_id
  evidence_id
  evidence_exact_content_sha256
  contract_id
  contract_version
  scope_signature_id
  evidence_class
  immutability_status
  provenance_status
  project_origin_status
  semantic_source_lineage_status
  declared_scope_status
  decision_status = ADMISSIBLE | REJECTED | BLOCKED
  reason_codes[]
  reviewer_identity
  created_at_utc
  decision_seal
~~~

Rules:

~~~text
ADMISSIBLE
  only when exact bytes/version are pinned,
  provenance is sufficient,
  project-origin restrictions are satisfied,
  and the source can be mapped to the target authority problem

REJECTED
  when positively inadmissible

BLOCKED
  when admissibility cannot be established
~~~

An evidence record never self-authorizes.

Only ADMISSIBLE evidence may provide positive authority.

### 2.2 DimensionAuthorityBasis

Every registered dimension has exactly one persisted authority-basis record:

~~~text
DimensionAuthorityBasis
  basis_id
  claim_dimension_register_id + digest
  dimension_id
  dimension_class
  required_evidence_roles[]
  required_anchor_roles[]
  required_hypothesis_roles[]
  required_rule_roles[]
  required_scope_applicability = true
  required_prerequisite_ids[]
  insufficiency_disposition = BLOCKED
  basis_seal
~~~

Minimum semantics by class:

#### PHYSICAL_HYPOTHESIS

PASS eligibility requires:

~~~text
admissible exact physical evidence
+
pre-observation-eligible hypothesis/discriminator identity
+
all known material alternatives accounted for
+
exactly one material physical interpretation survives
+
no unresolved contradiction
+
scope applicability PASS
~~~

The result authorizes only the exact physical proposition in the register.

It cannot infer timestamp meaning, side meaning, price scale or volume meaning.

#### SEMANTIC_ANCHOR

PASS eligibility requires at least one ADMISSIBLE SemanticAnchorManifest whose:

~~~text
normalized semantic proposition entails the exact dimension
semantic-source lineage is established
project-origin status is non-project
scope applicability is PASS
source meaning is independently fixed rather than inferred from I_A/I_B/F/O
~~~

A reference implementation is insufficient unless its semantic-source relationship is separately established.

No fixed number of sources and no majority vote substitutes for entailment.

Any material contradictory admissible anchor => BLOCKED until resolved.

#### CONDITIONAL_RULE

PASS eligibility requires:

~~~text
sealed RuleRecord
exact mathematical/logical proposition
exact affected field set
exact condition
exact violation disposition
exact non-waivable ExecutionObligationRecord
scope applicability PASS
~~~

The rule may be authoritative before runtime satisfaction only when its semantics do not depend on the future observed values.

#### PREREQUISITE_CLOSURE

PASS eligibility requires the exact prerequisite IDs from the ClaimDimensionRegister and all of them current PASS under their own current-authority predicates.

No adjudicator may replace the prerequisite list.

#### SCOPE_APPLICABILITY

PASS eligibility requires a PASS SemanticScopeApplicabilityDecision defined below.

## 3. F03 correction — machine-closed scope and applicability

### 3.1 OperationalSemanticScopeSignature

Replace the free-text-only scope with:

~~~text
OperationalSemanticScopeSignature
  schema =
    B_PE_SEM_02_OPERATIONAL_SCOPE_SIGNATURE_V0_2
  scope_signature_id
  provider_identity = DUKASCOPY
  instrument_id = USATECHIDXUSD
  representation_identity = DUKASCOPY_NATIVE_BI5_HOURLY_TICKS
  representation_regime_id = K1_LEGACY_HOURLY_TICK_BI5
  native_object_family = HOURLY_HH_TICKS_BI5
  canonical_delivery_host = datafeed.dukascopy.com
  provider_delivery_identity_policy_id
  provider_delivery_identity_policy_seal
  representation_regime_manifest_id
  representation_regime_manifest_seal
  execution_window_freeze_path =
    04-REFERENCE/EXECUTION-WINDOW-FREEZE.json
  execution_window_freeze_blob =
    bf7c43e9d90d952dfa3715c28575fdf6cf379a89
  evaluation_first_open_slot_utc =
    2021-08-15T22:00:00+00:00
  evaluation_last_open_slot_utc =
    2026-08-14T20:00:00+00:00
  mandatory_warmup_h1_bars = 20
  intended_semantic_epoch =
    warmup prefix required by the frozen window
    plus the frozen evaluation domain
  contract_id
  contract_version
  scope_signature_digest
~~~

The exact current referenced identities are:

~~~text
provider_delivery_identity_policy_id =
BFIQ02-DUKASCOPY-PROVIDER-DELIVERY-V0_1

provider_delivery_identity_policy_seal =
302b3abe97a495cf173ae3561077fe59bbd8b71c3517220c115edcc82bf8387a

representation_regime_manifest_id =
BFIQ02-USATECH-K1-REGIME-MANIFEST-V0_1

representation_regime_manifest_seal =
368659c30c480673fea57030e63389d1d3950bb544de684d41120794389c90d5
~~~

These identities may be replaced only by a separately governed successor scope, never by in-place reinterpretation.

### 3.2 SemanticScopeApplicabilityDecision

Every dimension adjudication must bind exactly one scope decision:

~~~text
SemanticScopeApplicabilityDecision
  scope_decision_id
  dimension_id
  evidence_ids[]
  anchor_ids[]
  target_scope_signature_id + digest
  source_representation_scope
  source_instrument_scope
  source_temporal_scope
  continuity_or_equivalence_proof_refs[]
  uncovered_scope_segments[]
  contradictory_scope_evidence_ids[]
  status = PASS | FAIL | BLOCKED
  reason_codes[]
  reviewer_identity
  created_at_utc
  scope_decision_seal
~~~

PASS requires:

~~~text
exact provider/instrument/regime applicability
AND
the dimension's authority covers the complete intended semantic epoch
AND
no uncovered material regime/epoch segment exists
AND
no unresolved conflicting applicability evidence exists
~~~

A current daily provider source cannot authorize historical K1 merely because its physical layout is compatible.

Any uncovered segment:

~~~text
BLOCKED — SCOPE_APPLICABILITY_INCOMPLETE
~~~

## 4. F04 correction — historical observation eligibility

Historical target evidence may be reused decisively only through:

~~~text
HistoricalObservationEligibilityRecord
  schema =
    B_PE_SEM_02_HISTORICAL_OBSERVATION_ELIGIBILITY_V0_2
  eligibility_id
  historical_execution_id
  historical_source_head
  historical_observed_at_utc
  historical_evidence_ids[]
  target_dimension_id
  proposed_hypothesis_set_id
  proposed_discriminator_ids[]
  pre_observation_artifact_refs[]
  pre_observation_artifact_hashes[]
  pre_observation_commit_or_time
  equivalence_mapping_rationale
  post_hoc_broadening_check
  eligibility_role =
    DECISIVE_DISCRIMINATION |
    NONDECISIVE_COMPATIBILITY |
    CONTRADICTION_ONLY
  status = PASS | FAIL | BLOCKED
  reason_codes[]
  eligibility_seal
~~~

DECISIVE_DISCRIMINATION requires proof that, before the historical observation:

~~~text
the materially relevant interpretation alternatives were already fixed
AND
the discriminator behavior now relied upon was already fixed
AND
the current use does not broaden the old discriminator after seeing results
~~~

For BERD02-GHA-35533153289-1:

~~~text
historical source_head =
2eb8350fb24c3043017c91475d202b5e0d6bb501

historical exact result seal =
ab5c5bdf97ce3dcfa773ed555afa842443ef21b7a155057ab0e9517bb573f5ef
~~~

Its ProbePlan, locator manifests and source-head runner may be cited as pre-observation artifacts.

However:

~~~text
mere existence of FORMAT_ALONE or parser code before the run
does not automatically prove that a later, broader SemanticHypothesisSet
was precommitted
~~~

If exact pre-observation equivalence cannot be established:

~~~text
B-ERD-02 may support
  NONDECISIVE_COMPATIBILITY
  or CONTRADICTION_ONLY

but not DECISIVE_DISCRIMINATION
~~~

This removes retrospective hypothesis leakage.

## 5. F05 correction — KnownMaterialAlternativeRegistry

Every SemanticHypothesisSet must bind:

~~~text
KnownMaterialAlternativeRegistry
  schema =
    B_PE_SEM_02_KNOWN_MATERIAL_ALTERNATIVES_V0_2
  registry_id
  target_dimension_id
  evidence_review_cutoff_head
  evidence_review_cutoff_time
  reviewed_evidence_ids[]
  candidate_interpretations[]
    candidate_id
    normalized_interpretation
    material_effect_if_true
    evidence_refs[]
    disposition =
      INCLUDED_MATERIAL_HYPOTHESIS |
      EXCLUDED_NONMATERIAL |
      REJECTED_INADMISSIBLE |
      BLOCKED_UNRESOLVED
    disposition_rationale
  included_hypothesis_ids[]
  unresolved_candidate_ids[]
  registry_digest
~~~

Rules:

~~~text
every known material admissible alternative
-> must be INCLUDED_MATERIAL_HYPOTHESIS

known candidate excluded as non-material
-> requires explicit rationale showing no governed downstream effect

known unresolved material candidate
-> hypothesis set BLOCKED

candidate interpretation omitted from the registry despite being present
in reviewed admissible evidence
-> hypothesis set BLOCKED
~~~

SemanticHypothesisSet must bind:

~~~text
known_material_alternative_registry_id
known_material_alternative_registry_digest
~~~

The open-world rule remains active after sealing for genuinely new evidence.

## 6. F06 correction — exact digest and seal domains

All structured objects use the parent candidate canonical JSON rule.

Exact projections:

### 6.1 ClaimDimensionRegister

~~~text
register_digest =
SHA256(canonical_json(register_payload_without_register_digest))
~~~

### 6.2 Evidence admissibility decision

~~~text
decision_seal =
SHA256(canonical_json(decision_payload_without_decision_seal))
~~~

### 6.3 Evidence set

~~~text
evidence_set_digest =
SHA256(canonical_json(sorted [
  {
    evidence_id,
    evidence_exact_content_sha256,
    admissibility_decision_id,
    admissibility_decision_seal
  }
]))
~~~

### 6.4 Anchor set

~~~text
anchor_set_digest =
SHA256(canonical_json(sorted [
  {
    anchor_manifest_id,
    anchor_id,
    target_dimension_id,
    evidence_id,
    evidence_exact_sha256,
    anchor_manifest_seal
  }
]))
~~~

### 6.5 Known-alternative registry

~~~text
registry_digest =
SHA256(canonical_json(registry_payload_without_registry_digest))
~~~

### 6.6 Hypothesis set

~~~text
hypothesis_set_digest =
SHA256(canonical_json(sorted [
  {
    hypothesis_set_id,
    target_dimension_id,
    known_material_alternative_registry_id,
    known_material_alternative_registry_digest,
    hypothesis_set_seal
  }
]))
~~~

### 6.7 RuleRecord

Each conditional or deterministic rule is sealed:

~~~text
RuleRecord
  rule_id
  rule_type
  target_dimension_ids[]
  exact_proposition
  exact_condition
  affected_field_set[]
  violation_disposition
  created_at_utc
  rule_seal

rule_seal =
SHA256(canonical_json(rule_payload_without_rule_seal))
~~~

Then:

~~~text
rule_set_digest =
SHA256(canonical_json(sorted [
  {rule_id, rule_seal}
]))
~~~

### 6.8 Scope applicability set

~~~text
scope_applicability_set_digest =
SHA256(canonical_json(sorted [
  {
    scope_decision_id,
    dimension_id,
    target_scope_signature_id,
    scope_decision_seal
  }
]))
~~~

### 6.9 Historical eligibility set

~~~text
historical_eligibility_set_digest =
SHA256(canonical_json(sorted [
  {
    eligibility_id,
    historical_execution_id,
    target_dimension_id,
    eligibility_role,
    eligibility_seal
  }
]))
~~~

### 6.10 Lineage resolution set

~~~text
lineage_resolution_set_digest =
SHA256(canonical_json(sorted [
  {
    lineage_resolution_id,
    lineage_resolution_digest
  }
]))
~~~

### 6.11 Adjudication seal

OperationalSemanticRuleAdjudication must include:

~~~text
claim_dimension_register_id
claim_dimension_register_digest
scope_signature_id
scope_signature_digest
evidence_set_digest
anchor_set_digest
hypothesis_set_digest
rule_set_digest
scope_applicability_set_digest
historical_eligibility_set_digest
lineage_resolution_set_digest
obligation_set_digest
~~~

Then:

~~~text
adjudication_seal =
SHA256(canonical_json(adjudication_payload_without_adjudication_seal))
~~~

### 6.12 Reopen event

~~~text
reopen_event_seal =
SHA256(canonical_json(reopen_event_payload_without_reopen_event_seal))
~~~

Sorting for every set projection is lexicographic by each member's canonical JSON bytes.

Duplicate member identities are rejected before hashing.

Any digest/seal mismatch makes the containing object inadmissible.

## 7. F07 correction — exact execution-obligation closure

### 7.1 ExecutionObligationRecord

Every future runtime obligation is a closed record:

~~~text
ExecutionObligationRecord
  obligation_id
  source_claim_id
  source_dimension_id
  rule_id
  exact_predicate
  affected_field_set[]
  evaluation_scope
  evaluation_cardinality
  on_pass
  on_fail
  on_blocked
  nonwaivable = true
~~~

For SIGNEDNESS_EQUIVALENCE_RULE_V0_1 the required obligation is at minimum:

~~~text
obligation_id =
SIGNEDNESS_HIGH_BIT_ZERO_REQUIRED::<dimension_id>

exact_predicate =
high_bit == 0 for every affected target-domain field instance
unless exact signedness authority is separately current PASS

evaluation_cardinality =
EVERY_ACCEPTED_AFFECTED_FIELD_INSTANCE

on_fail =
BLOCKED — SIGNEDNESS_SEMANTIC_AMBIGUITY

nonwaivable =
true
~~~

### 7.2 Canonical obligation union

The global execution_obligation_set MUST equal the exact canonical union of every dimension_adjudication.execution_obligations[].

Rules:

~~~text
no missing obligation
no extra orphan obligation
no duplicate obligation_id
same obligation_id with differing bytes = invalid
every obligation source_dimension_id must exist in ClaimDimensionRegister
~~~

Digest:

~~~text
obligation_set_digest =
SHA256(canonical_json(sorted [
  canonical ExecutionObligationRecord objects
]))
~~~

A future adjudication with any union mismatch is:

~~~text
BLOCKED — EXECUTION_OBLIGATION_SET_MISMATCH
~~~

### 7.3 B-FIQ-02R binding

B-FIQ-02R must bind:

~~~text
OperationalSemanticRuleAdjudication ID + seal
claim_dimension_register_id + digest
scope_signature_id + digest
obligation_set_digest
exact ExecutionObligationRecord set
~~~

B-FIQ-02R may not drop, weaken, rename or reinterpret an obligation.

Any mismatch:

~~~text
B-FIQ-02R = BLOCKED
~~~

## 8. Corrected OperationalSemanticRuleAdjudication additions

The parent schema is amended to require:

~~~text
claim_dimension_register_id
claim_dimension_register_digest

scope_signature_id
scope_signature_digest

evidence_admissibility_decisions[]
dimension_authority_basis_records[]
semantic_scope_applicability_decisions[]
known_material_alternative_registries[]
historical_observation_eligibility_records[]

scope_applicability_set_digest
historical_eligibility_set_digest
lineage_resolution_set_digest
obligation_set_digest
~~~

Dimension adjudications may not self-select their required authority basis.

They must reference the exact DimensionAuthorityBasis bound to their registered dimension.

## 9. Corrected PASS predicate

Dimension PASS now requires all of:

~~~text
registered dimension identity exact
ClaimDimensionRegister exact
DimensionAuthorityBasis exact
all contributing evidence ADMISSIBLE
required anchor/hypothesis/rule roles satisfied
KnownMaterialAlternativeRegistry closed
historical decisive evidence eligible when used
SemanticScopeApplicabilityDecision PASS
all exact prerequisites current PASS
no unresolved material contradiction
execution obligations complete and non-waivable
all relevant digests/seals reverify
~~~

Claim PASS is derived only from the immutable register.

Overall PASS still requires all C01-C07 operational claims PASS and no unresolved material cross-claim contradiction.

## 10. Defect closure map

~~~text
BPESEM02-F01
-> CLOSED BY ClaimDimensionRegister + exact derivation

BPESEM02-F02
-> CLOSED BY source admissibility decision + DimensionAuthorityBasis

BPESEM02-F03
-> CLOSED BY machine-closed scope + per-dimension applicability decision

BPESEM02-F04
-> CLOSED BY HistoricalObservationEligibilityRecord

BPESEM02-F05
-> CLOSED BY KnownMaterialAlternativeRegistry

BPESEM02-F06
-> CLOSED BY exact digest/seal projections

BPESEM02-F07
-> CLOSED BY ExecutionObligationRecord + canonical union/digest
~~~

These closure statements remain candidate correction claims until persisted-HEAD final re-break.

## 11. Preserved prohibition boundary

Still no:

~~~text
provider contact
provider BI5 GET
new semantic-discrimination execution
FULL_INTERVAL execution
D materialization
real Q/F/Q-RM-12 full execution
backtest
paper/broker/live
~~~

No semantic proposition has been promoted.

## 12. Mandatory final re-break

The persisted corrected composite must now be attacked for at least:

~~~text
dimension omission
authority-basis bypass
current-daily -> historical-K1 scope leak
post-hoc B-ERD-02 discrimination
known-alternative omission
digest projection ambiguity
execution-obligation drop
C08 -> C01-C07 authority leak
project-decoder self-authority
plausibility-as-semantics
B-FIQ in-place reinterpretation
historical PASS after reopen
~~~

Only then may B-PE-SEM-02 receive PASS / FAIL / BLOCKED.

STOP.
