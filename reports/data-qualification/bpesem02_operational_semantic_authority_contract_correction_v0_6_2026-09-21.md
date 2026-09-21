# B-PE-SEM-02 — OPERATIONAL NATIVE-BI5 SEMANTIC AUTHORITY CONTRACT — CORRECTION V0.6

**Date:** 2026-09-21  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**V0.5 corrected HEAD:** da809cc02526f4ef1a61483220f94629fdcc968a  
**V0.5 final re-break commit:** 859a9fb70d9248a57a495bdc95dd48f889800ca2  
**Correction scope:** BPESEM02-R13 only

## 0. Composite identity

Normative composite:

~~~text
V0.1 candidate
+ V0.2 correction
+ V0.3 correction
+ V0.4 correction
+ V0.5 correction
+ V0.6 correction
~~~

Composite identity:

~~~text
B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_6_CORRECTED
~~~

No C01-C07 proposition is adjudicated by this correction.

## 1. R13 correction — forward-closed governed semantic discovery

The V0.5 direct-root predicates are superseded by family predicates.

Contract-fixed discovery policy identity becomes:

~~~text
discovery_policy_id =
BPESEM02-GOVERNED-SEMANTIC-DISCOVERY-V0_6
~~~

All V0.5 Git-tree enumeration, case-sensitivity, fixed-point reference closure,
cycle handling, baseline-set equation, race checks and digest rules remain unchanged.

### 1.1 Forward family predicates

A repository blob is directly discovered when its exact path satisfies ANY:

~~~text
path starts with "evidence/bpe"
path starts with "reports/data-qualification/bpe"

path starts with "evidence/berd"
path starts with "reports/data-qualification/berd"

path starts with "evidence/bfiq"
path starts with "reports/data-qualification/bfiq"
~~~

These are exact case-sensitive prefix predicates over repository-relative Git paths.

Consequences include automatic direct discovery of future families such as:

~~~text
evidence/bpe05/...
reports/data-qualification/bpe05_...

evidence/bpesem03/...
reports/data-qualification/bpesem03_...

evidence/bfiq02r/...
reports/data-qualification/bfiq02r_...
~~~

without changing the discovery policy version.

The prefix itself does not grant evidentiary authority.

Every discovered artifact still receives the qualified relevance/admissibility/scope/lineage treatment required by V0.4/V0.5.

## 2. SemanticEvidenceRegistry for evidence outside discovered families

Some future evidence may legitimately need to live outside the direct family prefixes.

Define a contract-discovered registry family:

~~~text
registry_path_prefix =
evidence/bpesem/registry/
~~~

This prefix is already directly discovered by:

~~~text
path starts with "evidence/bpe"
~~~

### 2.1 Registry schema

~~~text
SemanticEvidenceRegistry
  schema =
    B_PE_SEM_02_SEMANTIC_EVIDENCE_REGISTRY_V0_6

  registry_id
  governed_branch
  registry_parent_id
  registered_items[]
    registry_item_id
    artifact_path
    artifact_git_blob
    artifact_role =
      POSITIVE_EVIDENCE |
      CONTRADICTORY_EVIDENCE |
      ALTERNATIVE_INTERPRETATION_EVIDENCE |
      SCOPE_EVIDENCE |
      LINEAGE_EVIDENCE |
      REOPEN_TRIGGER_EVIDENCE |
      GOVERNANCE_CONSTRAINT
    target_claim_ids[]
    target_dimension_ids[]
    registration_reason
  created_at_utc
  registry_digest
~~~

Digest:

~~~text
registry_digest =
SHA256(canonical_json(registry_payload_without_registry_digest))
~~~

Exact artifact identity is:

~~~text
{artifact_path, artifact_git_blob}
~~~

A registry item whose path/blob does not exist at the registry's governed HEAD is invalid.

### 2.2 Registry reference closure

Every registered artifact is inserted into the discovery set before relevance classification.

Its explicit repository references are then followed transitively under the V0.5 fixed-point rules.

Therefore an evidence artifact outside direct prefixes is still included in:

~~~text
baseline discovery
evidence horizon
delta review
visibility analysis
positive-authority analysis
~~~

when registered.

## 3. Registration rule

Any newly created repository artifact intended to do any of the following for operational C01-C07 authority:

~~~text
provide positive evidence
provide a competing material interpretation
contradict a current proposition
change semantic source lineage
change target scope applicability
trigger reopen
change a governing semantic-authority constraint
~~~

MUST satisfy at least one:

~~~text
A. artifact path is directly discovered by the V0.6 family predicates

OR

B. exact {path, git_blob} is registered in a V0.6 SemanticEvidenceRegistry
   that is itself directly discovered
~~~

If neither is true:

~~~text
artifact_status =
UNREGISTERED_GOVERNED_SEMANTIC_EVIDENCE

positive authority =
FORBIDDEN
~~~

If such an artifact becomes known to a governed review through an explicit reference,
manual audit or adversarial break:

~~~text
current operational semantic authority =
BLOCKED

until:
  artifact is registered
  discovery horizon is refreshed
  delta review is completed
  contradiction/reopen rules are applied
~~~

This rule governs repository evidence after it becomes known/versioned.

It does not claim omniscient discovery of external evidence that has never entered the governed repository.

## 4. Forward freshness invariant

A CurrentAuthorityEvidenceDeltaReview MUST use the SAME V0.6 family predicates and registered-artifact expansion at both:

~~~text
prior horizon
current consumer-parent horizon
~~~

A future BPE / B-ERD / B-FIQ generation therefore changes the discovered artifact map automatically.

Example:

~~~text
H0:
no evidence/bpe05/*

H1:
evidence/bpe05/provider_clarification.json added

V0.6 current map includes it
-> exact added set includes it
-> one delta disposition mandatory
-> material alternative/contradiction/authority change
   creates reopen and blocks stale PASS
~~~

No numeric-generation update to the discovery policy is required.

## 5. Discovery-policy digest amendment

The V0.6 discovery-policy payload MUST bind exactly:

~~~text
policy_id
case_sensitive = true
git_tree_recursive_enumeration = true
direct_prefixes = [
  "evidence/bpe",
  "reports/data-qualification/bpe",
  "evidence/berd",
  "reports/data-qualification/berd",
  "evidence/bfiq",
  "reports/data-qualification/bfiq"
]
registry_path_prefix = "evidence/bpesem/registry/"
reference_closure = TRANSITIVE_FIXED_POINT
visited_identity = {path, git_blob}
unresolved_required_reference_disposition = BLOCKED
~~~

Then:

~~~text
discovery_policy_digest =
SHA256(canonical_json(discovery_policy_payload))
~~~

No implementation may narrow these prefixes while retaining the same policy identity.

## 6. R13 closure claim

~~~text
R13
-> CLOSED BY:
   forward family prefixes
   +
   SemanticEvidenceRegistry for out-of-family governed evidence
   +
   same policy at baseline and every future delta review
~~~

This closure claim remains unqualified until persisted-HEAD final re-break.

## 7. Preserved authority boundaries

Still:

~~~text
BPE-C01..C07 documentary = BLOCKED

BPE-SEM-C01-OP..C07-OP =
NOT YET ADJUDICATED / NOT YET PASS

OperationalSemanticRuleAdjudication =
ABSENT

B-FIQ-02 pre-execution eligibility =
BLOCKED

FULL_INTERVAL =
NOT AUTHORIZED / NOT RUN

C08-D4-OP / C08-D5-OP =
NOT YET PASS

D =
NO

backtest =
NO
~~~

No provider contact, provider GET or semantic-discrimination execution occurred.

## 8. Mandatory final persisted-head re-break

Attack the entire V0.6 composite, including at least:

~~~text
future bpeNN evidence
future bfiqNN semantic artifact
out-of-family registered evidence
out-of-family unregistered evidence
prefix narrowing
registry path/blob mismatch
registry omission from delta
stale baseline
discovery/reference closure
materiality laundering
visibility/positive-authority collapse
delta omission/race
reopen bypass
C01-C07/C08 leakage
signedness conditional-rule misuse
B-ERD post-hoc discrimination
project self-authority
execution-obligation loss
B-FIQ in-place reinterpretation
~~~

Only zero demonstrated material contract defects may produce PASS.

STOP.
