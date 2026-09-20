# B-PE-01 — NATIVE BI5 PROVIDER-SENSITIVE PHYSICAL SEMANTICS EVIDENCE CONTRACT — CANDIDATE

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Initial candidate commit:** `9d2a7bbb5e42af5261e2881c050f9442b998c5cb`  
**Initial candidate blob:** `d21ce35fe9acdcdc1b3b0828bb2525f75c15054a`  
**Adversarial break commit:** `47bd9055ba42a2bfe810d7c7e6d40a35cb9248c4`  
**Status:** CORRECTED PERSISTED CANDIDATE — NOT YET QUALIFIED  
**Scope:** evidence contract only. No provider evidence is accepted by this artifact, no BI5 is downloaded or processed, no D acquisition is materialized, no backtest is authorized.

---

## 0. Purpose and strict separations

The native-BI5 binding candidate and both Q-RM-12 V0.2 paths share provider-sensitive physical premises.

This contract governs future proof of those premises without allowing the implementations that consume them to become their own normative evidence.

```text
implementation agreement
≠ provider truth

working decoder
≠ representation specification

plausible decoded values
≠ physical semantic proof

project acquisition evidence
≠ representation-wide provider evidence

representation-wide provider evidence
≠ concrete-acquisition completeness

source digest
≠ semantic entailment

two URLs
≠ two independent lineages
```

---

## 1. Contract identity

```text
evidence_contract_id =
B_PE_01_DUKASCOPY_NATIVE_BI5_PROVIDER_SENSITIVE_PHYSICAL_SEMANTICS_EVIDENCE

evidence_contract_version =
B_PE_01_DUKASCOPY_NATIVE_BI5_PROVIDER_SENSITIVE_PHYSICAL_SEMANTICS_EVIDENCE_V0_1_CANDIDATE
```

Candidate correction does not itself promote any global gate.

---

## 2. Closed target representation scope signature

Evidence applicability is judged against the following target signature, which is distinct from any source's own version label:

```text
provider_identity =
DUKASCOPY

representation_family =
NATIVE_HOURLY_TICK_BI5

native_object_family =
HOURLY_TICK_PAYLOAD

project_representation_id =
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS

project_representation_version =
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE

instrument_scope =
USATECHIDXUSD where a claim is instrument-specific;
family-wide only when provider evidence proves family-wide applicability

intended_temporal_applicability =
the already-governed first research acquisition temporal domain:
mandatory 20-H1 warmup prefix + frozen 2021-08-14 → 2026-08-14 evaluation window
```

No provider format version is fabricated.

A source must instead prove or justify how its own version/epoch applies to this target signature.

If temporal/representation continuity cannot be established:

`BLOCKED`.

---

## 3. Provider-sensitive claim and mandatory-dimension register

Every claim is decomposed into mandatory dimensions. A claim PASS requires **every mandatory dimension PASS**.

### BPE-C01 — compression / envelope

Candidate proposition:

```text
A target native hourly BI5 payload uses LZMA-Alone representation-level
compression/envelope semantics and successful decompression yields the
physical slot byte stream.
```

Mandatory dimensions:

```text
C01-D1 compression family = LZMA
C01-D2 envelope/container mode = LZMA-Alone
C01-D3 stream/wrapper semantics = exact admission rule for one/multiple streams,
        prefixes/suffixes or wrapper bytes
C01-D4 decompressed output role = physical slot byte stream
```

### BPE-C02 — physical framing

Candidate proposition:

```text
Successful decompressed payload bytes are framed from byte zero into
fixed 20-byte complete slots; a terminal residual is not a complete slot.
```

Mandatory dimensions:

```text
C02-D1 complete slot width = 20 bytes
C02-D2 frame origin = byte zero
C02-D3 residual/trailing-byte semantics
C02-D4 presence/absence and semantics of any per-record delimiter/header
```

### BPE-C03 — primitive field layout

Candidate proposition:

```text
Each complete slot uses big-endian >IIIff primitive layout:
millisecond_offset, ask_raw, bid_raw, ask_volume_raw, bid_volume_raw.
```

Mandatory dimensions:

```text
C03-D1 byte order = big-endian
C03-D2 field count/order = five fields in exact stated order
C03-D3 first three fields = unsigned 32-bit integers
C03-D4 final two fields = IEEE-754 binary32
```

### BPE-C04 — timestamp offset meaning

Candidate proposition:

```text
The first uint32 is a millisecond offset relative to the represented UTC hour.
```

Mandatory dimensions:

```text
C04-D1 unit = millisecond
C04-D2 reference origin = represented hour
C04-D3 hour/time basis = UTC or exact provider-equivalent mapping
C04-D4 valid representation-level offset domain/range
```

Physical traversal-order authority is **not** a provider claim here; the project contract separately declares that physical slot order is not canonical temporal authority.

### BPE-C05 — ask/bid raw integer roles

Candidate proposition:

```text
The second uint32 is raw ask and the third uint32 is raw bid.
```

Mandatory dimensions:

```text
C05-D1 second/third field roles = ask then bid
C05-D2 integer interpretation = unsigned raw price integers
C05-D3 any provider-owned prerequisite metadata needed before price conversion
```

### BPE-C06 — USATECHIDXUSD price scaling

Candidate proposition:

```text
For target USATECHIDXUSD material, logical ask/bid price is raw integer / 1000.
```

Mandatory dimensions:

```text
C06-D1 evidence applies to USATECHIDXUSD or a proven provider rule governing it
C06-D2 numeric scaling = /1000
C06-D3 scale authority = exact provider rule/metadata source
C06-D4 temporal/version applicability to the target research epoch
```

Generic FX evidence is insufficient unless a provider rule proves the same scaling model applies.

### BPE-C07 — volume primitive / role / representation transform

Corrected candidate proposition:

```text
The fourth and fifth fields encode provider-native ask-volume and bid-volume
source fields, respectively, as IEEE-754 binary32 values; any representation-
level numeric transform or scale is exactly the one established by provider
evidence.
```

Mandatory dimensions:

```text
C07-D1 field roles/order = ask-volume then bid-volume
C07-D2 primitive encoding = IEEE-754 binary32
C07-D3 representation-level transform/scale = exact provider-defined rule,
        including explicit no-additional-scale if that is the rule
```

Project decoder behavior is outside this provider-truth claim and is checked later for conformance.

Economic interpretation such as lots/contracts/notional is required here only if it changes B decoding or Q membership.

### BPE-C08 — applicability to target representation

Candidate proposition:

```text
The evidence used for C01-C07 applies to the target Dukascopy native hourly
tick BI5 representation and not merely to another Dukascopy product/API/file family.
```

Mandatory dimensions:

```text
C08-D1 provider identity applicability
C08-D2 native hourly tick BI5 family applicability
C08-D3 native object/product family applicability
C08-D4 instrument applicability where claim-specific
C08-D5 temporal/version continuity to target research epoch
```

---

## 4. Source evidence record — closed schema

A source record identifies immutable evidence bytes. It does **not** self-assert which claims it proves.

Required fields:

```text
evidence_id
evidence_class
publisher_identity
source_title_or_repository
source_locator
source_version_or_commit
publication_or_commit_time
retrieved_at_utc
content_integrity_digest
declared_representation_scope
declared_instrument_scope
declared_temporal_scope
evidence_lineage_candidate_id
project_origin_check
notes_non_authoritative
```

Rules:

- exact evidence bytes/snapshot are hash-bound;
- moving branch/page alone is insufficient;
- exact commit/release preferred where available;
- source record contains no claim verdict and no `claim_ids_supported` shortcut.

### 4.1 Fixed integrity primitive

All contract integrity digests use:

```text
algorithm = SHA-256
encoding  = lowercase 64-character hexadecimal
```

For raw source/snapshot/anchor bytes:

```text
digest = SHA256(exact_bytes)
```

No text normalization, newline rewriting, decompression, Unicode normalization, or content transformation occurs before a raw-byte digest unless that transformed representation is itself separately persisted and identified.

### 4.2 EvidenceAdmissibilityDecision

Every source record must have exactly one persisted source-level admissibility decision:

```text
schema =
B_PE_01_EVIDENCE_ADMISSIBILITY_DECISION_V0_1_CANDIDATE

decision_id
evidence_id
evidence_content_integrity_digest
evidence_contract_id
evidence_contract_version
target_scope_signature
evidence_class
immutability_status
provenance_status
scope_status
project_origin_status
lineage_precheck_status
decision_status = ADMISSIBLE | REJECTED | BLOCKED
reason_codes
reviewer_identity
created_at_utc
decision_seal
```

Rules:

- `ADMISSIBLE` only when evidence bytes are pinned, provenance is sufficient, target-scope mapping is possible, and no project-origin disqualification is present;
- `REJECTED` when the source is positively inadmissible for this contract;
- `BLOCKED` when admissibility cannot yet be resolved;
- only `ADMISSIBLE` sources may contribute SUPPORT/CONTRADICT assertions to dimension PASS/FAIL;
- REJECTED/BLOCKED sources remain auditable but have zero positive evidentiary weight.

The admissibility decision is sealed under Section 12 canonicalization rules.

---

## 5. Claim evidence assertion — separate adjudicator-owned schema

Semantic support/contradiction mapping is a separate object:

```text
assertion_id
evidence_id
claim_id
dimension_id
stance = SUPPORT | CONTRADICT
anchor_type
anchor_locator
anchor_integrity_digest
normalized_proposition
scope_mapping
scope_mapping_rationale
adjudicator_identity
assertion_created_at_utc
```

Examples of acceptable anchors:

- documentation section + page/fragment locator;
- repository commit + path + symbol + exact line/range;
- immutable API/reference section;
- exact fixture expectation only when EC-X1 is later authorized.

A document/repository digest without a claim-specific anchor cannot support a dimension.

The assertion's normalized proposition must state **what the source actually establishes**, not merely repeat the candidate claim ID.

---

## 6. Evidence classes

### EC-P1 — provider-primary normative documentation

Provider-owned specification/API/SDK documentation explicitly defining target representation semantics.

### EC-P2 — provider-maintained reference implementation

Provider-owned source code pinned to an exact revision, usable when behavior is explicit enough to distinguish competing interpretations.

### EC-I1 — independent non-project technical specification/documentation

Must be identifiable, immutable/version-pinned and lineage-resolved.

### EC-I2 — independent non-project reference implementation

May corroborate byte-level behavior. Parser behavior cannot prove unstated economic semantics.

### EC-X1 — controlled external fixture evidence

Future controlled public/provider fixture with independently known expected interpretation.

`NOT AUTHORIZED FOR EXECUTION IN THIS CONTRACT-FORMALIZATION BLOCK`.

### EC-PROJECT — project implementation/evidence

Includes V4.3, I_A, I_B, F/O, handoff and project-generated synthetic tests.

```text
INADMISSIBLE AS INDEPENDENT SUPPORT FOR C01-C08
```

May later be checked for conformance against qualified provider truth.

---

## 7. Auditable lineage-resolution record

Independence cannot be self-declared by evidence submitters.

Each evidence set must have a lineage-resolution record:

```text
lineage_resolution_id
evidence_ids
lineage_groups
relationship_basis_refs
relationship_basis_rationale
project_origin_checks
independence_status_per_pair =
    INDEPENDENT | COMMON_LINEAGE | UNRESOLVED
reviewer_identity
created_at_utc
lineage_resolution_integrity_digest
```

Rules:

- fork/translation/mirror/wrapper/port/generated docs derived from one semantic source count as one lineage;
- same upstream semantic source → one lineage;
- different hostname/author/repository does not imply independence;
- unresolved material lineage relationship cannot be counted as independent;
- if the required second lineage is UNRESOLVED, the affected dimension remains BLOCKED.

Project independence requires evidence that the source did not derive its claim from V4.3/I_A/I_B/project tests.

---

## 8. Dimension-level evidence sufficiency

Every mandatory dimension is adjudicated independently.

A dimension may become PASS only when:

1. exact target-scope mapping is established;
2. source bytes/snapshot and anchors are immutable;
3. no project-circular evidence is counted;
4. lineage resolution is complete enough to count independence;
5. no unresolved same-scope contradiction exists;
6. at least one provider-primary lineage (EC-P1 or EC-P2) supports the dimension;
7. at least one **distinct** corroborating lineage supports the same material dimension, from:
   - another independently originated EC-P1/P2 artifact; or
   - EC-I1/I2;
8. both lineages' anchored propositions entail the dimension rather than merely being compatible with it.

There is **no single-provider PASS exception** in V0.1.

If only one provider lineage exists:

`BLOCKED — INSUFFICIENT_INDEPENDENT_CORROBORATION`.

If two non-provider lineages exist but no provider-primary lineage exists:

`BLOCKED — PROVIDER_PRIMARY_EVIDENCE_ABSENT`.

---

## 9. Claim-level verdict

A claim verdict is a pure projection of its mandatory dimensions plus conflict state.

### PASS

```text
all mandatory dimensions = PASS
AND no unresolved material contradiction
AND exact target scope bound
```

### FAIL

Used only when adequate exact-scope authoritative evidence establishes that the candidate proposition or a mandatory dimension is false.

FAIL must identify the contradicted dimension and replacement fact if known.

FAIL forces later B correction/version adjudication; it never silently mutates B.

### BLOCKED

Any other state, including:

- one dimension unresolved;
- insufficient source lineages;
- only project evidence;
- provider-primary evidence absent;
- unproven independence;
- scope/version ambiguity;
- stale applicability;
- unresolved contradiction;
- unanchored evidence;
- partial proposition support.

No majority vote exists.

---

## 10. Conflict semantics

### 10.1 Different scope/version

Potentially different representation generations, symbol classes, APIs or epochs are not automatically conflicting.

Applicability must be resolved first.

### 10.2 Same-scope contradiction

Any admissible material contradiction on the same dimension and target scope makes that dimension:

`BLOCKED — CONFLICT_UNRESOLVED`

until adjudicated.

### 10.3 Confirmed authoritative contradiction

If target-scope provider evidence unambiguously contradicts the candidate and competing support is proven stale/wrong-scope/derived:

`dimension = FAIL`

and therefore the parent claim cannot PASS.

No "provider always wins" shortcut applies when provider scope/version is itself ambiguous.

---

## 11. Staleness / temporal applicability

Evidence age alone is not staleness.

Evidence is stale when applicability to the target signature cannot be established.

Rules:

- exact commits/releases preferred;
- undated/versionless source requires explicit continuity proof;
- latest docs cannot be assumed to describe historical material;
- old docs cannot be assumed to describe later revisions;
- archived evidence may remain valid if continuity is established;
- C06 must bind USATECHIDXUSD or a provider rule demonstrably governing it.

Unresolved applicability:

`BLOCKED`.

---

## 12. Closed persisted adjudication record

Every future claim adjudication must be persisted in a closed object:

```text
adjudication_schema
adjudication_id
evidence_contract_id
evidence_contract_version
target_scope_signature
evidence_records
evidence_admissibility_decisions
evidence_set_digest
claim_assertions
assertion_set_digest
lineage_resolution_id
lineage_resolution_integrity_digest
dimension_adjudications
claim_adjudications
overall_provider_evidence_status
supersedes_adjudication_id
adjudication_status
adjudicator_identity
created_at_utc
adjudication_seal
```

`evidence_records` binds exact `evidence_id + content_integrity_digest` tuples.

`evidence_admissibility_decisions` binds each evidence ID to exactly one sealed ADMISSIBLE/REJECTED/BLOCKED source decision.

`dimension_adjudications` contain exact supporting/contradicting assertion IDs and one of:

`PASS | FAIL | BLOCKED`.

`claim_adjudications` are derived from mandatory dimensions.

`overall_provider_evidence_status` is exactly:

```text
PASS
FAIL
BLOCKED
```

and may be PASS only when C01-C08 are all PASS.

### 12.1 Canonical JSON normalization

All structured integrity objects in B-PE-01 use the same canonical JSON byte rule:

```text
UTF-8
sorted object keys
compact separators "," and ":"
ensure_ascii = false
allow_nan = false
JSON types preserved exactly
duplicate object keys rejected at serialized ingress
```

Arrays are semantically ordered unless the schema explicitly defines a set projection.

Where a field is semantically a set, the contract defines the hashed projection as the lexicographically sorted array of each member's own canonical JSON bytes.

### 12.2 Digest domains

```text
evidence_set_digest =
SHA256(canonical_json(sorted [
  {evidence_id, content_integrity_digest, admissibility_decision_id, admissibility_decision_seal}
]))

assertion_set_digest =
SHA256(canonical_json(sorted [
  {assertion_id, evidence_id, claim_id, dimension_id, stance, anchor_integrity_digest}
]))

lineage_resolution_integrity_digest =
SHA256(canonical_json(lineage_resolution_payload_without_its_digest))

decision_seal =
SHA256(canonical_json(admissibility_decision_payload_without_decision_seal))

adjudication_seal =
SHA256(canonical_json(adjudication_payload_without_adjudication_seal))
```

Sorting for set projections is by canonical JSON byte sequence, not insertion/traversal order.

All seal/digest fields use the SHA-256/lowercase-hex primitive from Section 4.1.

A record whose recomputed seal differs from the persisted seal is invalid and cannot contribute authority.

---

## 13. Supersession / newly discovered conflict

Historical adjudications are immutable.

New evidence never mutates an old sealed record.

### 13.1 ProviderEvidenceReopenEvent — closed schema

A material post-PASS trigger is persisted as:

```text
schema =
B_PE_01_PROVIDER_EVIDENCE_REOPEN_EVENT_V0_1_CANDIDATE

reopen_event_id
evidence_contract_id
evidence_contract_version
target_scope_signature
prior_adjudication_id
prior_adjudication_seal
trigger_evidence_ids
trigger_admissibility_decision_ids
affected_claim_ids
affected_dimension_ids
trigger_reason_codes
event_status = OPEN | CLOSED
opened_at_utc
closed_by_adjudication_id
reviewer_identity
reopen_event_seal
```

Seal:

```text
reopen_event_seal =
SHA256(canonical_json(reopen_event_payload_without_reopen_event_seal))
```

An OPEN event must have `closed_by_adjudication_id = null`.

A CLOSED event must bind the exact superseding adjudication that resolved it.

### 13.2 Trigger rule

If newly admitted target-scope evidence materially contradicts a current PASS:

```text
persist OPEN ProviderEvidenceReopenEvent
→ previous PASS remains immutable historical evidence
→ previous adjudication becomes NON_AUTHORITATIVE_FOR_NEW_PROMOTION
→ current provider-evidence authority = BLOCKED
→ produce a new adjudication
→ new adjudication explicitly supersedes the old one
→ only that new adjudication may close the event
```

### 13.3 Current-authority predicate

A B-PE-01 adjudication is current provider-evidence authority iff all are true:

```text
adjudication seal valid
adjudication_status = PASS
overall_provider_evidence_status = PASS
target_scope_signature exact
not superseded by a later valid adjudication
no OPEN reopen event binds its adjudication_id/seal
all bound evidence admissibility decisions remain exact and sealed
```

Downstream B promotion must pin the exact adjudication ID + seal and prove the current-authority predicate at promotion time.

Thus a historical PASS cannot silently remain current authority after a material conflict.

---

## 14. Representation-wide proof versus later acquisition proof

### 14.1 Eligible before project acquisition

Documentary/reference evidence may establish C01-C08 without downloading project BI5 if all dimension-level requirements are met.

### 14.2 Deferred to bounded real D acquisition

B-PE-01 cannot establish:

- existence/count/hash of project components;
- missing/extra/repeated project components;
- project acquisition completeness;
- actual decompression success/residual lengths;
- actual anomaly incidence;
- actual observed offsets/price/volume distributions;
- per-object provider continuity;
- real Q outcome;
- real F universe;
- real I_A/I_B equality.

Those remain later D/B/A/Q/F/Q-RM-12 execution evidence.

---

## 15. Whole-contract qualification result

The **evidence contract** may eventually receive:

- PASS — rules for later evidence collection/adjudication survived adversarial qualification;
- FAIL — contract defect demonstrated;
- BLOCKED — contract semantics cannot be closed without prohibited evidence/data.

Contract PASS is distinct from provider-truth PASS:

```text
B-PE-01 EVIDENCE CONTRACT = PASS
≠ C01-C08 = PASS
≠ B GLOBAL PASS
```

---

## 16. Permission closure

Still prohibited:

```text
provider evidence gathering during this formalization block
native BI5 download
real BI5 payload processing
real project acquisition
D materialization
real Q execution
real F emission
real Q-RM-12 comparison
real backtest
paper/broker/live execution
positive P1.1 authorization
```

---

## 17. Correction record

Initial adversarial break demonstrated:

```text
BPE-F01 — SINGLE_PROVIDER_ESCAPE_UNDERCUTS_INDEPENDENCE_REQUIREMENT
BPE-F02 — CLAIM_SUPPORT_CAN_BE_SELF_ASSERTED_WITHOUT_EXACT_SOURCE_ANCHOR
BPE-F03 — LINEAGE_INDEPENDENCE_IS_SELF_ASSERTED
BPE-F04 — TARGET_PROVIDER_SCOPE_VERSION_BINDING_NOT_CONCRETE_ENOUGH
BPE-F05 — C07_MIXES_PROVIDER_FACT_WITH_PROJECT_DECODER_BEHAVIOR
BPE-F06 — BROAD_CLAIM_CAN_PASS_WITH_UNPROVEN_REQUIRED_DIMENSION
BPE-F07 — NO_CLOSED_PERSISTED_ADJUDICATION_OUTPUT_EVIDENCE_SET_BINDING
BPE-F08 — POST_PASS_CONFLICT_SUPERSESSION_SEMANTICS_INCOMPLETE
```

First persisted-head re-break demonstrated residuals:

```text
BPE-R01 — INTEGRITY_DIGEST_AND_SEAL_CANONICALIZATION_DEFERRED
BPE-R02 — SOURCE_ADMISSIBILITY_IS_NOT_A_PERSISTED_DECISION
BPE-R03 — REOPEN_REQUIRED_EVENT_HAS_NO_CLOSED_SCHEMA_CURRENT_AUTHORITY_RULE
```

Corrections are limited to F01-F08 and R01-R03.

---

## 18. Corrected candidate pre-rebreak verdict

```text
B-PE-01 EVIDENCE CONTRACT = CORRECTED CANDIDATE / NOT YET QUALIFIED

C01-C08 provider truth = NOT ADJUDICATED
B global executable gate = BLOCKED
```

Next:

`persisted-HEAD adversarial re-break of this corrected contract only`.
