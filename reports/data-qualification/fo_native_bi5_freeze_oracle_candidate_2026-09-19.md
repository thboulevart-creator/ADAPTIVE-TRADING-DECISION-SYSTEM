# F + O — FIRST CONCRETE NATIVE-BI5 QUALIFICATION FREEZE / SEMANTIC ORACLE CANDIDATE

**Date:** 2026-09-19  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `f204cb5eb81b02711c1df30af8d5d2994ccc4c50`  
**Scope:** formalization only — no acquisition, no real BI5 processing, no backtest, no permission increase.

## 0. Status and strict separations

This artifact creates the first concrete candidate for:

```text
F — qualification-freeze artifact / persistence contract
+
O — deterministic semantic comparison oracle
```

It consumes the corrected/re-broken candidate package:

```text
D/R/M candidate blob
2249bea6dbf6b5a8e0d49b99a93bf16248f9c0e9

B/A candidate blob
25400abcc3a2a24438954ff27b970bd934313ae3

Q candidate blob
9e15cfb86716894131485a15a180cc170a230287
```

and preserves the Q-RM-07 / Q-RM-11 / Q-RM-12 universal contracts.

Official gates remain:

```text
F = BLOCKED
O = BLOCKED
```

until the concrete contract is adversarially qualified and an executable persistence/oracle implementation exists on materialized concrete inputs.

Strict separations:

```text
freeze artifact integrity
≠ occurrence identity

serialization order
≠ semantic order
≠ temporal order

physical source witness
≠ canonical occurrence identity

content hash
≠ semantic universe equality

terminal qualification evidence
≠ frozen qualified universe

candidate
≠ PASS

F/O formalization
≠ acquisition authorization
≠ backtest authorization
```

---

# 1. Upstream candidate boundary

F/O MUST NOT reinterpret any upstream candidate semantics.

In particular:

- D owns acquisition membership and the mandatory deterministic warmup prefix plus frozen five-year evaluation window;
- R selects native Dukascopy BI5 as the first representation candidate;
- M defines occurrence-based, strict-duplicate-preserving, pre-Q logical primary market-tick candidates;
- B owns fixed BI5 physical interpretation for the selected candidate binding;
- A owns versioned anomaly classification/outcome;
- Q owns final qualification outcome and retained membership.

F/O may prove, persist and compare those semantics. F/O may not repair or replace them.

---

# 2. F candidate identity

```text
freeze_contract_id =
F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE

freeze_contract_version =
F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE_V0_1_CANDIDATE
```

The persistence envelope candidate is:

```text
UTF-8 JSON object
schema family:
QUALIFICATION_FREEZE_ARTIFACT_V0_1_CANDIDATE
```

JSON is only the selected persistence container.

JSON array/object textual order is not semantic occurrence order.

---

# 3. Two distinct terminal artifact classes

A qualification execution may end in one of Q's exact outcomes:

```text
QUALIFIED
QUALIFICATION_BLOCKED
ACQUISITION_REJECTED
```

F MUST distinguish two artifact classes.

## 3.1 Qualified freeze artifact

Created only when:

```text
Q outcome = QUALIFIED
+
all F construction invariants succeed
```

Then:

```text
artifact_class = QUALIFIED_UNIVERSE_FREEZE
freeze_state = FROZEN
```

A qualified occurrence universe is present.

## 3.2 Terminal non-freeze evidence

Created when:

```text
Q outcome = QUALIFICATION_BLOCKED
or
Q outcome = ACQUISITION_REJECTED
or
F construction itself cannot prove completeness
```

Then:

```text
artifact_class = QUALIFICATION_TERMINAL_EVIDENCE
freeze_state = NOT_CREATED
qualified_universe = null
qualified_occurrence_count = null
```

A blocked/rejected run MUST NOT emit:

- a partial qualified occurrence list;
- a prefix count presented as the qualified universe;
- a zero count that could be misread as a valid empty universe;
- a freeze identifier that claims semantic freeze occurred.

Diagnostic prefix information may be retained only in a clearly non-normative execution-diagnostic section.

---

# 4. Exact reconstruction tuple

Every qualified freeze artifact MUST bind the complete normative tuple:

```text
D
R
M
B
A
Q
F
```

For each determinant the artifact must store at minimum:

```text
normative_id
normative_version
immutable artifact reference
integrity digest/reference
```

The complete tuple includes:

```text
acquisition_domain_id
acquisition_declaration_version

representation_id
representation_version

record_model_version

format_binding_id
format_binding_version
binding semantic dependency references

anomaly_matrix_id
anomaly_matrix_version

qualification_contract_id
qualification_contract_version
qualification parameters

freeze_contract_id
freeze_contract_version
```

Integrity digests are provenance/integrity evidence only.

They are not occurrence identity and are not by themselves semantic-equality proof.

Any missing, contradictory or unresolved determinant prevents `FROZEN`.

---

# 5. Acquisition / component snapshot

A qualified freeze MUST contain or immutably bind a complete snapshot of the materialized D membership sufficient to reconstruct the exact acquisition.

For each declared component:

```text
component_manifest_entry_id
declared role
instrument/source identity
declared_hour_bucket_utc
immutable payload/provenance reference
payload integrity reference
materialization status
```

The snapshot must also bind D's completeness evidence and the exact acquisition-domain identity.

Filename/path syntax is not normative membership or hour authority.

Manifest entry order is non-semantic.

---

# 6. Complete physical accounting snapshot

For every deterministically framed non-blocked B component, F MUST preserve Q's complete-slot accounting proof.

For component `c`:

```text
S_all(c)
=
{0 .. complete_slot_count(c)-1}

S_candidate(c) ∩ S_rejected(c) = ∅

S_candidate(c) ∪ S_rejected(c) = S_all(c)
```

F persists the semantic relation, not traversal order.

For each complete slot, exactly one disposition exists:

```text
CANDIDATE_RETAINED
REJECT_RECORD
```

A candidate slot cannot disappear.

A rejected slot cannot also be retained.

Terminal fragments are represented separately and never inserted into complete-slot cardinality.

The exact source witness:

```text
(component_manifest_entry_id, component_local_slot_index)
```

remains a physical provenance/conformance locator only.

It does not become canonical occurrence identity.

---

# 7. Anomaly outcome snapshot

F MUST preserve the complete normative anomaly outcome relation required to reproduce Q.

Each semantic anomaly entry contains at minimum:

```text
anomaly_class_id
anomaly_matrix_version
exact normative target shape
mandatory outcome
acquisition_fatal flag where declared
qualification_evidence_bindings where classification/localisability/outcome depends on evidence
```

For every evidence-dependent anomaly decision, F MUST freeze enough immutable evidence binding to independently revalidate the decision:

```text
qualification_evidence_bindings[]
- evidence_role
- immutable_reference
- integrity_digest_or_reference
- exact_anomaly_target_binding
```

In particular:

```text
BI5-A08 TERMINAL_PARTIAL_SLOT_WITH_CONSTRUCTIVE_COMPLETENESS_PROOF
→ exact constructive completeness-proof binding is mandatory
```

A decision label without its required qualification evidence is not reconstructibly frozen.

Permitted target shapes remain exactly those frozen by Q:

```text
COMPLETE_SLOT
→ component_manifest_entry_id
 + component_local_slot_index

TERMINAL_FRAGMENT
→ component_manifest_entry_id
 + terminal_fragment_start_offset
 + terminal_fragment_length

COMPONENT
→ component_manifest_entry_id

ACQUISITION
→ acquisition_domain_id
```

Diagnostic paths, diagnostic list order, worker IDs and free text may be persisted as provenance but are not semantic comparison keys.

---

# 8. Qualified occurrence snapshot

A `QUALIFIED_UNIVERSE_FREEZE` persists every retained occurrence exactly once.

Each persisted occurrence consists of two separated projections:

```text
1. logical semantic payload
2. source/conformance witness
```

## 8.1 Logical semantic payload

For the current B/M candidate, semantic storage MUST avoid implementation-dependent binary floating JSON numbers.

Candidate exact normal form:

```text
market_timestamp_utc
  = exact RFC3339 UTC timestamp
  = YYYY-MM-DDTHH:MM:SS.mmmZ

ask_price
  = exact rational numerator / 1000

bid_price
  = exact rational numerator / 1000

ask_volume
  = exact finite binary32 numeric value normalized as
    integer_coefficient * 2^exponent2

bid_volume
  = same exact finite numeric normal form
```

The binary32 numeric normal form MUST be unique.

For every finite non-zero value:

```text
value = integer_coefficient * 2^exponent2

integer_coefficient
= signed odd integer

exponent2
= integer

all removable factors of two
= factored into exponent2
```

For finite binary32 zero:

```text
integer_coefficient = 0
exponent2 = 0
```

Therefore forms such as:

```text
1 * 2^0
2 * 2^-1
```

cannot both be emitted for the same non-zero logical value; only the unique odd-coefficient form is conforming.

Textual/container differences and signed-zero source representation do not create two logical numeric values.

The artifact may additionally preserve raw source bits as provenance, but raw bit patterns are not substituted for the M logical numeric value.

## 8.2 Source/conformance witness

Each retained occurrence also carries:

```text
component_manifest_entry_id
component_local_slot_index
```

This proves which B candidate slot was retained and allows independent reconstruction of the physical→logical relation.

The witness is not:

```text
canonical record position
global row id
market-event identity
temporal precedence
cross-acquisition identity
```

---

# 9. Strict duplicates and occurrence individuality

F MUST preserve occurrence multiplicity.

If two distinct B source slots produce the same normalized logical payload:

```text
same payload
+
distinct complete source slots
→ two retained occurrences
```

No content hash, payload equality, timestamp equality or serialization deduplication may collapse them.

The qualified universe is therefore modeled semantically as an unordered finite bag/multiset of retained logical occurrences plus the separately persisted source→logical conformance relation.

This does not introduce canonical enumeration.

---

# 10. Serialization semantics

The physical JSON file may contain arrays because JSON needs a container representation.

Array position is explicitly non-normative.

The following MUST NOT change the frozen semantic state:

```text
object-key order
array order for components
array order for anomaly outcomes
array order for occurrences
pretty-printing
whitespace
equivalent container traversal
```

Any implementation using array index as occurrence identity or temporal order is non-conforming.

---

# 11. Persistence, immutability and integrity

Candidate persistence path family:

```text
artifacts/data-qualification/freezes/<qualification-run-scope>/
```

The exact future run-specific filename is not yet instantiated because no materialized D/Q execution exists.

A future persisted artifact MUST be immutable once committed.

Candidate integrity evidence may include:

```text
Git commit SHA
Git blob SHA
SHA-256 of exact artifact bytes
```

These values authenticate a physical artifact instance.

They do not define semantic occurrence identity.

Two semantically equal freeze artifacts may have different byte hashes because non-semantic serialization order/whitespace may differ.

Therefore byte-hash equality is never the O semantic oracle.

---

# 12. F construction rule

Conceptually:

```text
validate exact D/R/M/B/A/Q tuple
→ validate D materialization/completeness
→ validate B/A/Q complete slot accounting
→ require Q outcome
→ if Q != QUALIFIED:
     emit terminal non-freeze evidence only
→ if Q == QUALIFIED:
     build complete reconstruction tuple
     build complete component snapshot
     build complete anomaly relation
     build complete source→logical retained relation
     build unordered retained logical-occurrence bag
     self-check all counts/relations
     persist immutable artifact
     mark FROZEN
```

If any F self-check is incomplete or contradictory:

```text
freeze_state = NOT_CREATED
qualification terminal state = BLOCKED at F
```

F may not repair upstream values or drop inconsistent entries.

---

# 13. O candidate identity

```text
oracle_id =
O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR

oracle_version =
O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR_V0_1_CANDIDATE
```

O compares semantic freeze meaning, not file bytes.

---

# 14. O pre-comparison validity gate

Before semantic comparison, each input must independently satisfy the F schema and integrity rules.

If either input is malformed, incomplete, contradictory or not actually frozen:

```text
oracle_result = BLOCKED
```

If either terminal outcome is not `QUALIFIED`, no qualified universe exists to compare.

O may report whether terminal outcomes agree, but MUST return:

```text
qualified_universe_comparison = BLOCKED
```

It must not compare diagnostic prefixes as if they were frozen universes.

---

# 15. Same-state comparability gate

For a Q-RM-12 same-state determinism comparison, both F artifacts must bind the same normative determinant set:

```text
D/R/M/B/A/Q/F semantic versions + parameters
+
the same immutable determinant-content bindings
```

and the same materialized acquisition identity/input state.

For every normative determinant, O MUST compare:

```text
normative_id
normative_version
bound immutable content/integrity reference
```

Rules:

```text
different legitimate qualification-relevant version
→ comparison_scope = DISTINCT_QUALIFICATION_STATE
→ qualified_universe_comparison = BLOCKED

same normative_id + same normative_version
but different bound determinant content/integrity digest
→ oracle_result = BLOCKED
→ reason = NORMATIVE_VERSION_INTEGRITY_CONFLICT
```

The second case is not a legitimate distinct state under the same version and must never be treated as semantically comparable.

A semantic contract change requires a new version.

This determinant-integrity rule is separate from the byte digest of the produced freeze artifact itself.

---

# 16. O semantic comparison projection

For two valid comparable `QUALIFIED_UNIVERSE_FREEZE` artifacts, O compares all of the following.

## 16.1 Reconstruction tuple

Exact semantic identities/versions/parameters must match.

## 16.2 Acquisition membership

Compare the complete D component membership as an unordered semantic relation.

Manifest listing order is ignored.

## 16.3 Physical→logical accounting relation

For the current B version, compare for every exact declared component and complete slot:

```text
source witness
→ exact disposition
→ if retained, exact normalized logical payload
→ if rejected, exact normative A class/outcome target
```

This relation is a conformance proof.

It does not make source witness the final logical occurrence identity.

## 16.4 Anomaly semantic relation

Compare normalized semantic anomaly tuples:

```text
(class_id, exact normative target, mandatory outcome, acquisition_fatal flag)
```

Ignore non-semantic diagnostic path/list order/worker metadata.

## 16.5 Qualified logical occurrence bag

Compare the unordered multiset of normalized logical payloads.

Multiplicity is normative.

Thus:

```text
[A, A, B] != [A, B]
```

even though strict duplicates have identical payload.

## 16.6 Cardinality / individuality

The total retained multiplicity and all source→logical retained relations must agree.

---

# 17. O result semantics

For same-state comparable qualified inputs:

```text
all semantic projections agree
→ oracle_result = SEMANTIC_EQUAL

any required semantic projection differs
→ oracle_result = SEMANTIC_DIFFERENT

required proof missing / non-qualified / non-comparable
→ oracle_result = BLOCKED
```

For Q-RM-12:

```text
SEMANTIC_EQUAL
→ determinism comparison may PASS for that test instance

SEMANTIC_DIFFERENT
→ determinism test FAIL

BLOCKED
→ determinism test BLOCKED
```

No byte hash or file ordering may override this result.

---

# 18. Explicit non-semantic differences

The following alone MUST NOT cause `SEMANTIC_DIFFERENT`:

```text
JSON whitespace
object-key order
array/list order
diagnostic list order
worker id
worker partition
runtime traversal order
cache layout
temporary path
artifact filename
Git blob identity
freeze-output artifact byte SHA-256
pretty-printing
```

provided the validated semantic projections are equal.

---

# 19. Physical repartitioning boundary

Q-RM-12 T06 applies only:

```text
where the applicable binding explicitly declares
two physical partitions semantically equivalent
```

The current B V0.1 candidate does not define a general repartitioning equivalence transform.

Therefore O V0.1 MUST NOT invent one.

For this concrete binding, same-state comparison uses the exact materialized D/B source-accounting relation.

A future B version may define a different semantic projection for explicitly equivalent repartitioning; that requires a new compatible O version.

---

# 20. No temporal authority

Neither F nor O sorts the universe into normative chronology.

Timestamp is part of each logical payload.

The following remains forbidden:

```text
physical slot order
→ temporal authority

JSON array order
→ temporal authority

oracle normalization order
→ temporal authority
```

An implementation may internally sort temporary comparison keys, but such sorting is only an algorithmic technique and never a semantic order exposed by F/O.

---

# 21. Permission boundary

Nothing in F/O changes:

```text
real data acquisition       = NOT AUTHORIZED
native BI5 download         = NOT AUTHORIZED
real BI5 processing         = NOT AUTHORIZED
real backtest               = NOT AUTHORIZED
positive P1.1 AUTHORIZED    = BLOCKED
paper / broker / live       = NOT AUTHORIZED
```

---

# 22. Pre-break verdict state

```text
F/O candidate formalization
= PERSISTED CANDIDATE once committed

F official gate
= BLOCKED

O official gate
= BLOCKED
```

Reasons include:

1. no materialized D acquisition/manifest/completeness evidence;
2. B/A provider-sensitive facts remain officially BLOCKED;
3. no executable Q implementation has been qualified;
4. no concrete F artifact has been emitted from a real qualified run;
5. no executable O implementation has been qualified;
6. no independent I_A / I_B determinism run exists.

---

# 23. Next governed action

Adversarially break this exact persisted F/O candidate before any F/O implementation.

Attack at minimum:

- blocked Q emitting a partial/list/count universe;
- acquisition-rejected Q emitting a freeze;
- missing normative determinant in F;
- semantic determinant changed but same freeze reused;
- strict duplicate collapse;
- same payload with different multiplicity;
- source slot swapped to another payload while payload bag stays equal;
- component list order change;
- occurrence list order change;
- anomaly diagnostic order/path change;
- file/hash equality used as semantic oracle;
- equal semantics with different byte hashes;
- source witness promoted to canonical identity;
- array index promoted to occurrence identity;
- hidden timestamp sorting;
- float/JSON numeric normalization ambiguity;
- signed-zero source-bit difference;
- terminal fragment inserted into complete-slot accounting;
- candidate/reject overlap;
- late upstream non-conformance mutating old freeze;
- distinct B/Q version incorrectly compared as same state;
- physical repartitioning equivalence invented without binding authority;
- permission leakage.

No acquisition or real backtest is permitted during the break.
