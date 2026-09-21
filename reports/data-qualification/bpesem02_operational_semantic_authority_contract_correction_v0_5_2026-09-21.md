# B-PE-SEM-02 — OPERATIONAL NATIVE-BI5 SEMANTIC AUTHORITY CONTRACT — CORRECTION V0.5

**Date:** 2026-09-21  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**V0.4 corrected HEAD:** 15ffd1da84d41cd3c2b2346d8da7e296d1948192  
**V0.4 final re-break commit:** f0202c00728d640c2808be3fb3b1d3b414363d6a  
**Correction scope:** BPESEM02-R09 through BPESEM02-R12 only

## 0. Composite identity

Normative composite:

~~~text
V0.1 candidate
+ V0.2 correction
+ V0.3 correction
+ V0.4 correction
+ V0.5 correction
~~~

Composite identity:

~~~text
B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_5_CORRECTED
~~~

No operational semantic proposition is adjudicated by this correction.

## 1. R09 correction — fresh live baseline parent is mandatory

GovernedSemanticEvidenceBaseline is amended with:

~~~text
governed_branch = integration/system-v1
fresh_live_head
fresh_live_tree_sha
fresh_head_observed_at_utc
baseline_materialization_parent_head
baseline_materialization_commit
parent_relation_status
~~~

Hard rules:

~~~text
fresh_live_head =
the exact branch HEAD returned by GitHub immediately before baseline construction

baseline_head =
fresh_live_head

baseline_tree_sha =
fresh_live_tree_sha

baseline_materialization_parent_head =
fresh_live_head
~~~

The baseline must be persisted from that exact parent.

Before baseline persistence, the branch HEAD is re-read.

If:

~~~text
current branch HEAD != fresh_live_head
~~~

then:

~~~text
BASELINE_RACE_DETECTED
-> discard the unpersisted baseline candidate
-> restart from fresh live HEAD
~~~

After persistence:

~~~text
baseline_materialization_commit
must have baseline_materialization_parent_head in its direct parent set
~~~

Otherwise:

~~~text
BLOCKED — BASELINE_PARENT_RELATION_INVALID
~~~

A baseline derived from an arbitrary ancestor is forbidden.

## 2. R10 correction — canonical repository discovery algorithm

Contract-fixed discovery algorithm identity:

~~~text
discovery_policy_id =
BPESEM02-GOVERNED-SEMANTIC-DISCOVERY-V0_5
~~~

### 2.1 Path enumeration

Input:

~~~text
exact Git tree identified by baseline_tree_sha
~~~

Rules:

1. Enumerate all Git tree entries recursively.
2. Only blob entries are candidate artifacts.
3. Paths are compared as exact UTF-8 byte sequences represented by GitHub path strings.
4. Matching is case-sensitive.
5. No filesystem locale, OS glob implementation or symlink traversal is used.
6. The repository Git tree is the only enumeration authority.

### 2.2 Exact root predicates

A blob is directly discovered when its path satisfies any exact predicate:

~~~text
path starts with "evidence/bpe02/"
path starts with "evidence/bpe03/"
path starts with "evidence/bpe04/"
path starts with "evidence/berd02/"

path equals
"evidence/bfiq02/semantic_invariant_manifest_v0_1.json"

path starts with "reports/data-qualification/bpe01"
path starts with "reports/data-qualification/bpe02"
path starts with "reports/data-qualification/bpe03"
path starts with "reports/data-qualification/bpe04"
path starts with "reports/data-qualification/bpesem"
path starts with "reports/data-qualification/berd02"
~~~

The report predicates apply only under the exact reports/data-qualification/ prefix.

### 2.3 Reference closure

For every directly discovered UTF-8 structured/text artifact, extract only explicit repository references that are syntactically exact repository paths.

Accepted reference forms:

~~~text
a full repository-relative path beginning with:
evidence/
reports/
04-REFERENCE/
src/
tools/
breakers/
.github/
~~~

A referenced path is followed only when that exact blob path exists in the same baseline tree.

Reference following is transitive:

~~~text
direct set
-> referenced set
-> references of referenced set
-> repeat until fixed point
~~~

Visited identity:

~~~text
{path, git_blob}
~~~

prevents cycles.

If an explicit referenced path required by an evidence/adjudication identity cannot be resolved in the baseline tree:

~~~text
BLOCKED — REFERENCED_ARTIFACT_UNRESOLVED
~~~

Free prose that merely resembles a filename but is not an exact repository-relative path does not create authority.

### 2.4 Baseline membership equation

Let:

~~~text
M = exact mandatory-lineage artifact identities
D = all directly discovered artifact identities
R = transitive exact referenced artifact identities
~~~

Each member of D union R receives exactly one relevance disposition:

~~~text
MATERIAL_VISIBLE
GOVERNANCE_VISIBLE
WRONG_SCOPE_PROVEN
DUPLICATE_EXACT_BYTES
BLOCKED_RELEVANCE_UNRESOLVED
~~~

Then:

~~~text
baseline_member_refs =
canonical unique union(
  M,
  all D/R members whose disposition is
    MATERIAL_VISIBLE
    GOVERNANCE_VISIBLE
    BLOCKED_RELEVANCE_UNRESOLVED
)
~~~

No other construction is allowed.

Duplicates are collapsed only on exact:

~~~text
{path, git_blob}
~~~

not on semantic similarity.

Any mismatch between the computed union and persisted baseline_member_refs:

~~~text
BLOCKED — BASELINE_MEMBER_SET_MISMATCH
~~~

### 2.5 Discovery implementation binding

The baseline records:

~~~text
discovery_policy_id
discovery_policy_digest
discovery_result_digest
~~~

where:

~~~text
discovery_policy_digest =
SHA256(canonical_json(the complete V0.5 discovery policy parameters))

discovery_result_digest =
SHA256(canonical_json(sorted [
  {
    path,
    git_blob,
    discovery_origin,
    relevance_disposition,
    controlling_decision_refs
  }
]))
~~~

The baseline seal/digest binds both.

## 3. R11 correction — closed materiality predicate

Materiality is defined relative to the currently governed logical/data pipeline.

A competing interpretation is MATERIAL if there exists any admissible input domain
or unresolved target-domain instance for which the interpretation can change at least one of:

~~~text
M01 physical decompression/admission outcome
M02 physical record boundary or complete-record cardinality
M03 primitive decoded bit/value interpretation
M04 logical-record cardinality
M05 market_timestamp_utc value
M06 temporal ordering
M07 session membership
M08 warmup versus evaluation membership
M09 ask/bid role
M10 ask/bid logical numeric price
M11 ask_volume/bid_volume role
M12 volume numeric value retained in logical payload
M13 B/A anomaly classification
M14 Q retained/rejected/blocked membership
M15 F frozen-universe identity/content
M16 O semantic payload equality/divergence
M17 downstream research input identity/content
~~~

If any M01-M17 effect is possible and not disproven:

~~~text
MATERIAL_ALTERNATIVE
or
BLOCKED_UNRESOLVED
~~~

### 3.1 NonMaterialityEquivalenceProof

NONMATERIAL_PROVEN requires:

~~~text
NonMaterialityEquivalenceProof
  proof_id
  target_dimension_id
  candidate_interpretation_id
  reference_interpretation_id
  exact_domain_definition
  applicable_materiality_axes[]
  proof_method
  proof_artifacts[]
  per_axis_result[]
    materiality_axis_id
    result = EQUIVALENT | NOT_APPLICABLE | BLOCKED
    evidence_refs[]
  overall_result = PASS | FAIL | BLOCKED
  proof_seal
~~~

PASS requires every M01-M17 axis to be either:

~~~text
EQUIVALENT
or
NOT_APPLICABLE with a proved structural reason
~~~

No sampled empirical absence of divergence proves universal equivalence unless the declared domain itself is exactly that finite sampled domain and the downstream authority is also restricted to it.

For full target semantic authority, a finite sample cannot prove nonmateriality outside the sample.

If the proof is missing or any axis is BLOCKED:

~~~text
NONMATERIAL_PROVEN is forbidden
~~~

Seal:

~~~text
proof_seal =
SHA256(canonical_json(proof_payload_without_proof_seal))
~~~

VisibilityUniverse items using NONMATERIAL_PROVEN must bind the exact PASS proof ID + seal.

## 4. R12 correction — exact horizon diff and race-free consumer binding

### 4.1 Canonical artifact map

For both prior and current horizons:

~~~text
artifact_key = exact repository-relative path
artifact_value = exact git_blob
~~~

Duplicate keys are invalid.

Let:

~~~text
P = prior artifact map
C = current artifact map
~~~

The exact sets are:

~~~text
added_paths =
keys(C) - keys(P)

deleted_paths =
keys(P) - keys(C)

common_paths =
keys(P) intersection keys(C)

modified_paths =
{p in common_paths where P[p] != C[p]}

unchanged_paths =
{p in common_paths where P[p] == C[p]}
~~~

Persisted CurrentAuthorityEvidenceDeltaReview arrays MUST equal these sets exactly.

For each added path persist:

~~~text
{path, current_git_blob}
~~~

For each deleted path:

~~~text
{path, prior_git_blob}
~~~

For each modified path:

~~~text
{path, prior_git_blob, current_git_blob}
~~~

No duplicate path is allowed.

Every added/deleted/modified member must have exactly one disposition record.

No disposition may exist for an unchanged or absent member.

Any inequality:

~~~text
BLOCKED — DELTA_SET_MISMATCH
~~~

### 4.2 Delta coverage invariant

~~~text
count(per_delta_item_dispositions)
=
count(added) + count(deleted) + count(modified)
~~~

and the keyed joins must be bijective.

A count match without key equality is insufficient.

### 4.3 Reviewed consumer parent

The delta review records:

~~~text
reviewed_consumer_parent_head
reviewed_consumer_parent_tree_sha
delta_review_persistence_commit
~~~

Before scanning:

~~~text
reviewed_consumer_parent_head =
fresh live integration/system-v1 HEAD
~~~

Immediately before persisting the delta review, branch HEAD is re-read.

If it moved:

~~~text
DELTA_REVIEW_RACE_DETECTED
-> restart delta review
~~~

The persisted delta-review commit must have the reviewed parent in its direct parent set.

### 4.4 Consumer-start validity

A consumer block relying on that delta review must begin from a fresh HEAD Hc.

The review is valid for Hc only when all are true:

1. the delta-review persistence commit is an ancestor of Hc;
2. every commit after the delta-review persistence commit through Hc is examined;
3. the contract-fixed semantic discovery algorithm finds no added/modified/deleted governed semantic-evidence artifact in that intervening range;
4. any commit that only persists the delta review itself is classified governance-only and does not alter a governed evidence input.

If any relevant evidence artifact changed:

~~~text
STALE_DELTA_REVIEW
-> new CurrentAuthorityEvidenceDeltaReview required
~~~

This check is called:

~~~text
ConsumerStartFreshnessCheck
~~~

and is persisted by the consumer block.

### 4.5 ConsumerStartFreshnessCheck

~~~text
ConsumerStartFreshnessCheck
  check_id
  delta_review_id + seal
  delta_review_persistence_commit
  consumer_start_head
  consumer_start_tree_sha
  intervening_commits[]
  semantic_evidence_changes[]
  status = PASS | BLOCKED
  check_seal
~~~

PASS only when semantic_evidence_changes is empty.

~~~text
check_seal =
SHA256(canonical_json(check_payload_without_check_seal))
~~~

B-FIQ-02R must bind a PASS ConsumerStartFreshnessCheck.

## 5. Adjudication / handoff amendments

OperationalSemanticRuleAdjudication must bind:

~~~text
discovery_policy_id + digest
discovery_result_digest
~~~

in addition to prior V0.4 fields.

Any NONMATERIAL_PROVEN visibility item must transitively bind its
NonMaterialityEquivalenceProof ID + seal.

Current authority requires:

~~~text
PASS CurrentAuthorityEvidenceDeltaReview
+
when used by a later consumer,
PASS ConsumerStartFreshnessCheck
~~~

## 6. Closure map

~~~text
R09
-> CLOSED BY baseline_head == freshly observed live branch HEAD
   + pre-persist branch race check + direct parent binding

R10
-> CLOSED BY contract-fixed exact Git-tree discovery and transitive reference closure
   + baseline set equation

R11
-> CLOSED BY M01-M17 materiality predicate
   + NonMaterialityEquivalenceProof

R12
-> CLOSED BY exact map-difference equations
   + bijective disposition coverage
   + delta-review race check
   + ConsumerStartFreshnessCheck
~~~

These closure claims remain unqualified until persisted-HEAD final re-break.

## 7. Preserved boundaries

Still no:

~~~text
provider contact
provider BI5 GET
new semantic discrimination execution
FULL_INTERVAL execution
D materialization
backtest
paper/broker/live
~~~

Current states remain:

~~~text
BPE-C01..C07 documentary = BLOCKED
BPE-SEM-C01-OP..C07-OP = NOT YET ADJUDICATED
OperationalSemanticRuleAdjudication = ABSENT
B-FIQ-02 pre-execution eligibility = BLOCKED
C08-D4-OP / C08-D5-OP = NOT YET PASS
FULL_INTERVAL = NOT RUN
~~~

## 8. Mandatory final persisted-head re-break

Attack at minimum:

~~~text
stale baseline ancestor
baseline persistence race
discovery matcher divergence
one-hop-only reference discovery
baseline set omission
material alternative labeled nonmaterial
sample-based false equivalence
delta-item omission
delta orphan/duplicate disposition
delta persistence race
consumer check/use race
visibility/positive-authority conflation
C01-C07/C08 cross-authority leakage
historical B-ERD-02 post-hoc reuse
project self-authority
execution-obligation dropping
reopen bypass
~~~

No PASS before the persisted V0.5 composite survives the final re-break.

STOP.
