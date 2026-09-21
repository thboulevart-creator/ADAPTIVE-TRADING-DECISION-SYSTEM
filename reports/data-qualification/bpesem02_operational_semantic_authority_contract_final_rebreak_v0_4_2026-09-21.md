# B-PE-SEM-02 — FINAL PERSISTED-HEAD RE-BREAK OF V0.4 COMPOSITE

**Date:** 2026-09-21  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**Persisted corrected HEAD attacked:** 15ffd1da84d41cd3c2b2346d8da7e296d1948192

## 1. Persisted state re-broken

The V0.4 correction closes the direct R05-R08 exploits:

~~~text
R05 governed-evidence omission
-> materially closed by mandatory baseline + discovery horizon

R06 positive-authority / visibility conflation
-> closed by separate VisibilityUniverse and PositiveAuthorityUniverse

R07 reopen-event existence as sole freshness proof
-> closed in principle by mandatory evidence horizon + delta review

R08 C01-C07 semantic scope / C08 representation-presence conflation
-> closed by explicit non-interchangeable predicates and zero C08 effect
~~~

The following extended attacks still demonstrate four material contract defects.

## 2. BPESEM02-R09 — BASELINE HEAD CAN BE STALE BY CONSTRUCTION

GovernedSemanticEvidenceBaseline contains:

~~~text
baseline_head
baseline_tree_sha
~~~

but V0.4 does not require baseline_head to equal the freshly verified live governed-branch HEAD at the opening of the semantic-adjudication block.

Exploit:

~~~text
live branch HEAD = H2
material evidence introduced at H2

future adjudicator chooses baseline_head = H1
where H1 is an ancestor before that evidence

repository discovery is perfectly complete relative to H1
baseline digest is internally exact
-> H2 evidence is absent before adjudication even starts
~~~

A later delta review is not guaranteed to repair this because the first adjudication can itself be created from the stale horizon.

Required correction:

~~~text
baseline_head MUST equal fresh live branch HEAD observed immediately before
baseline materialization

baseline branch ref MUST equal integration/system-v1

baseline materialization commit MUST descend directly from or be created
against that verified parent without an intervening unreviewed branch movement

branch movement before baseline persistence
-> restart fresh-HEAD verification
~~~

The exact observed branch-head identity must be persisted as part of the baseline provenance.

## 3. BPESEM02-R10 — DISCOVERY POLICY SEMANTICS ARE NOT CANONICAL

V0.4 names minimum discovery roots using patterns such as:

~~~text
evidence/bpe02/**
reports/data-qualification/bpesem*
~~~

but does not define:

~~~text
path matching semantics
recursive tree enumeration semantics
case sensitivity
how referenced artifacts are followed
whether reference following is transitive
cycle handling
what counts as an artifact reference
the exact relation between discovered_repository_artifacts[]
and baseline_member_refs[]
~~~

Exploit:

Two implementations use the same discovery-policy text/digest but different matcher/reference-following semantics and produce different baselines.

Or:

~~~text
artifact A references B
B references material C
implementation follows one hop only
-> C omitted
~~~

Required correction:

Define a contract-fixed Git-tree discovery algorithm.

At minimum:

~~~text
enumerate every blob path at exact baseline tree
UTF-8 path comparison, case-sensitive
prefix roots recurse over all descendant blobs
filename-prefix rules use exact defined basename/prefix predicate
parse explicit versioned artifact references from discovered governance/evidence
follow references transitively until fixed point
cycle-safe by exact {path, blob} identity
unresolved referenced artifact -> BLOCKED
baseline_member_refs =
exact canonical union of mandatory lineage members
+ all discovered MATERIAL_VISIBLE / GOVERNANCE_VISIBLE /
  BLOCKED_RELEVANCE_UNRESOLVED members
~~~

A discovery implementation/version identity and digest must be bound.

## 4. BPESEM02-R11 — NONMATERIAL_PROVEN HAS NO CLOSED MATERIALITY TEST

VisibilityUniverse permits:

~~~text
NONMATERIAL_PROVEN
~~~

and known alternatives can disappear from the hypothesis set after such a disposition.

But V0.4 does not define what "material" means for this pipeline.

Exploit:

~~~text
competing interpretation changes raw field meaning
-> reviewer asserts downstream strategy probably unaffected
-> NONMATERIAL_PROVEN
-> interpretation removed from material hypotheses
~~~

That can turn a real semantic ambiguity into a reviewer judgment.

Required correction:

A competing interpretation is MATERIAL if it can change any governed observable or decision input, including at least:

~~~text
physical record boundary/admission
logical-record cardinality
timestamp value/order/session/warmup/evaluation membership
ask/bid role or logical price
price numeric value
volume role/value retained in current logical payload
Q retained/rejected/blocked membership
F/O semantic comparison payload
downstream research input identity
~~~

NONMATERIAL_PROVEN is allowed only with a persisted equivalence proof showing
that the competing interpretation is invariant with respect to every applicable
governed observable above over its declared domain.

Absence of a demonstrated downstream difference is not such proof.

If equivalence cannot be proved:

~~~text
MATERIAL_ALTERNATIVE or BLOCKED_UNRESOLVED
~~~

## 5. BPESEM02-R12 — DELTA REVIEW DOES NOT FORMALLY PROVE COMPLETE SET DIFFERENCE OR CLOSE THE HANDOFF RACE

CurrentAuthorityEvidenceDeltaReview contains prior/current artifact refs plus:

~~~text
added_items[]
modified_items[]
deleted_bound_items[]
per_delta_item_dispositions[]
~~~

but V0.4 does not require these arrays to be the exact mathematical diff of the two horizons.

Exploit:

~~~text
new artifact X exists in current_discovered_semantic_artifact_refs
-> omit X from added_items
-> all declared delta items are harmless
-> status PASS
~~~

Additionally, "PASS for the exact consumer HEAD" is under-specified operationally because the delta-review artifact itself must be persisted after observing a HEAD.

Required correction:

### Exact diff equations

For canonical artifact identity:

~~~text
artifact_key = path

prior_map[path] = prior blob/content identity
current_map[path] = current blob/content identity

added =
  current keys - prior keys

deleted =
  prior keys - current keys

modified =
  intersection keys whose exact content identity differs

unchanged =
  intersection keys whose exact content identity is identical
~~~

Persisted arrays MUST equal those exact sets.

Every added/deleted/modified member has exactly one delta disposition.

Any omission/duplicate/orphan:

~~~text
BLOCKED — DELTA_SET_MISMATCH
~~~

### Consumer-parent binding

Define:

~~~text
reviewed_consumer_parent_head
~~~

as the freshly verified branch HEAD whose tree is scanned.

The delta review is then persisted as a child of that reviewed parent.

A consumer block such as B-FIQ-02R may rely on the review only if:

~~~text
its starting parent lineage contains that delta-review commit
AND
no intervening commit between the reviewed parent/delta-review persistence
and consumer start changes a governed semantic-evidence artifact
~~~

If an intervening relevant change exists:

~~~text
new delta review required
~~~

This closes the check/use race without requiring a review to predict its own future commit SHA.

## 6. Attacks that remain closed in V0.4

No defect was demonstrated for:

~~~text
BPE03 omission from mandatory inherited evidence
visibility collapsed into positive authority
inadmissible evidence automatically disappearing as a hypothesis
absence of reopen event treated as freshness proof
C01-C07 semantic PASS promoted to C08
C08 empirical supersession promoted to C01-C07
runtime semantic deferral outside signedness
historical B-ERD-02 post-hoc reuse without eligibility record
project-decoder self-authority
plausibility-as-semantics
execution-obligation dropping
B-FIQ-02 in-place reinterpretation
~~~

## 7. V0.4 re-break verdict

~~~text
B-PE-SEM-02 V0.4 CORRECTED COMPOSITE = FAIL

demonstrated material residual/new defects =
R09
R10
R11
R12
~~~

No semantic proposition is promoted.

Required next movement:

~~~text
minimal correction V0.5 for R09-R12 only
-> persist
-> final persisted-head re-break
-> PASS / FAIL / BLOCKED
~~~

STOP.
