# B-PE-01 — NATIVE BI5 PROVIDER-SENSITIVE PHYSICAL SEMANTICS EVIDENCE CONTRACT — CANDIDATE

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `a6e2206426b1229eb454dd224858b5934383d0e3`  
**Status:** PERSISTED FORMALIZATION CANDIDATE — NOT YET QUALIFIED  
**Scope:** evidence contract only. No provider evidence is accepted by this artifact, no BI5 is downloaded or processed, no D acquisition is materialized, no backtest is authorized.

---

## 0. Purpose

The concrete native-BI5 binding candidate and both Q-RM-12 V0.2 implementation paths currently share provider-sensitive physical premises.

Q-RM-12 proves that independently implemented paths conform to the governed contract and expose semantic divergence.

It does not prove that a shared external-provider premise is true.

This contract defines how provider-sensitive physical premises may later be qualified **without allowing V4.3, I_A, I_B, handoff, F or O to become their own normative evidence**.

Strict separation:

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
≠ proof that a later concrete acquisition is complete/correct
```

---

## 1. Contract identity

```text
evidence_contract_id =
B_PE_01_DUKASCOPY_NATIVE_BI5_PROVIDER_SENSITIVE_PHYSICAL_SEMANTICS_EVIDENCE

evidence_contract_version =
B_PE_01_DUKASCOPY_NATIVE_BI5_PROVIDER_SENSITIVE_PHYSICAL_SEMANTICS_EVIDENCE_V0_1_CANDIDATE
```

The contract is evidence-only.

It does not itself promote:

- B to PASS;
- R to PASS;
- D to PASS;
- any runtime implementation;
- any acquisition/backtest permission.

---

## 2. Exact provider-sensitive claim register

Every claim is independently adjudicated. Evidence supporting one claim does not silently support another.

### BPE-C01 — compression / envelope

Claim candidate:

```text
A native hourly Dukascopy BI5 tick payload admitted by the selected
representation is encoded as a single LZMA-Alone stream whose
decompressed payload is the physical slot byte stream.
```

Required proof dimensions:

- representation scope;
- compression family;
- exact envelope/container mode;
- whether concatenated streams, framing prefixes/suffixes or wrapper bytes are admitted;
- whether empty/decompression-failed payloads have defined representation meaning.

### BPE-C02 — fixed physical slot width / byte-zero framing

Claim candidate:

```text
After successful representation-level decompression, complete physical
records are framed from byte zero in fixed 20-byte slots; any remaining
terminal bytes are not a complete slot.
```

Required proof dimensions:

- exact slot width;
- frame origin;
- treatment of trailing bytes;
- no hidden per-record delimiter/header.

### BPE-C03 — field layout, byte order and primitive representation

Claim candidate:

```text
Each complete 20-byte slot has the exact big-endian primitive layout:

> I I I f f

millisecond_offset
ask_raw
bid_raw
ask_volume_raw
bid_volume_raw
```

Required proof dimensions:

- byte order;
- field order;
- field widths;
- integer signedness;
- IEEE-754 binary32 interpretation for each floating field.

A source proving only "20 bytes" cannot satisfy C03.

### BPE-C04 — timestamp offset semantics

Claim candidate:

```text
The first uint32 field is a millisecond offset within the represented
UTC hour; logical source timestamp reconstruction is:

declared_hour_utc + millisecond_offset milliseconds.
```

Required proof dimensions:

- unit = millisecond;
- reference origin = represented hour;
- UTC/hour basis;
- whether range [0, 3_600_000) is representation-valid;
- whether physical source order has any temporal authority.

Provider evidence may prove the encoded field meaning. The project contract separately remains owner of "physical traversal order is not canonical temporal authority."

### BPE-C05 — ask/bid integer role semantics

Claim candidate:

```text
The second and third uint32 fields encode raw ask and raw bid values,
respectively, in that order.
```

Required proof dimensions:

- ask versus bid role;
- field order;
- unsigned integer interpretation;
- whether any instrument-specific transformation is required before price scaling.

### BPE-C06 — USATECHIDXUSD price scaling

Claim candidate:

```text
For the selected Dukascopy USATECHIDXUSD native representation version,
logical ask/bid price is raw integer price divided by 1000.
```

This claim is deliberately instrument/symbol scoped.

A generic foreign-exchange BI5 rule does not automatically satisfy C06.

Required proof dimensions:

- exact symbol/instrument applicability;
- scale/point-value rule;
- representation/version applicability;
- whether scale is fixed by the representation, symbol metadata, or another provider-owned parameter.

### BPE-C07 — volume field primitive semantics

Claim candidate:

```text
The fourth and fifth fields are provider-native ask-volume and bid-volume
source values encoded as IEEE-754 binary32 values and are not implicitly
price-scaled by the BI5 decoder.
```

Required proof dimensions:

- ask-volume versus bid-volume role/order;
- binary32 primitive type;
- whether the encoded value is already the provider-native source value;
- any representation-level scale/conversion, if one exists.

This contract does **not** require B-PE-01 to prove an economic interpretation such as lots/contracts/notional unless that interpretation changes B physical decoding or Q membership.

### BPE-C08 — representation scope / applicability

Claim candidate:

```text
C01-C07 apply to the exact Dukascopy native hourly tick representation
selected by R for USATECHIDXUSD, rather than to an unrelated Dukascopy
API/product/file family.
```

C08 is a scope-binding claim. It prevents evidence about another Dukascopy format from being transplanted into this B contract.

---

## 3. Evidence record schema

Every future evidence item must be represented by a closed record containing at least:

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
representation_scope
instrument_scope
claim_ids_supported
claim_ids_contradicted
evidence_lineage_id
derived_from_lineage_ids
project_independence_status
scope_binding_rationale
notes_non_authoritative
```

Rules:

- `content_integrity_digest` binds the exact evidence bytes/snapshot used for adjudication;
- URL alone is not immutable evidence;
- repository default branch alone is not immutable evidence;
- `source_version_or_commit` must be exact when the source is versioned;
- evidence without an explicit representation/instrument scope mapping cannot silently support C08/C06;
- one evidence item may support several claims only when each mapping is explicit.

No evidence record may contain a caller-supplied claim verdict.

---

## 4. Admissible evidence classes

Evidence class controls admissibility, not automatic truth.

### EC-P1 — provider-primary normative documentation

Examples in principle:

- provider-owned format specification;
- provider-owned API/SDK documentation that explicitly defines the physical representation;
- provider-owned symbol metadata specification relevant to C06.

Strength:

highest documentary authority for the exact documented scope.

Limit:

provider ownership does not excuse missing version/scope/provenance.

### EC-P2 — provider-maintained reference implementation

Provider-owned source code may establish concrete encoded/decoded behavior when exact commit/version and relevant path are pinned.

It may support a claim only when the behavior is explicit enough to distinguish the competing interpretations.

A provider implementation with unexplained magic constants is evidence, but not automatically sufficient for all semantic meanings.

### EC-I1 — independent technical specification / documentation

A non-project, non-provider technical source may corroborate representation facts when:

- authorship/source is identifiable;
- exact version/snapshot is pinned;
- lineage is not merely copied from the project's V4.3/I_A/I_B;
- the source makes the relevant claim explicitly.

### EC-I2 — independent reference implementation

A non-project implementation may corroborate byte-level behavior when exact source revision and semantic path are pinned.

Its parser behavior cannot by itself prove an unstated economic meaning.

### EC-X1 — controlled external fixture evidence

A future controlled public/provider fixture may be used to test a documentary claim if its provenance and expected interpretation are independently known.

**Not authorized in this B-PE-01 formalization block.**

Use of EC-X1 later must not be confused with a project acquisition D materialization.

### EC-PROJECT — current project implementation/evidence

Includes:

- V4.3 compatibility probe;
- I_A V0.1/V0.2;
- I_B V0.1/V0.2;
- handoff;
- F/O implementation behavior;
- synthetic tests generated from the project contract.

Classification:

```text
INADMISSIBLE AS INDEPENDENT SUPPORT FOR C01-C08
```

These artifacts may be compared against independently qualified evidence later, but they cannot count toward qualifying the premise they implement.

---

## 5. Independence model

Independence is lineage-based, not hostname/count based.

Two sources count as one evidentiary lineage when one is:

- a fork;
- translation;
- mirror;
- generated documentation;
- wrapper;
- code port;
- article;
- example

derived materially from the other for the claim being adjudicated.

Required lineage semantics:

```text
same upstream semantic source
→ same evidence_lineage_id
→ no double counting
```

Project independence requires:

```text
not authored from V4.3 / I_A / I_B contract behavior
not generated from project tests
not inferred by executing project parsers
not a mirror of a project artifact
```

Provider P1/P2 documentation/code and an independently authored I1/I2 source may constitute distinct lineages.

Two independent-looking I1/I2 sources derived from the same historical parser are one lineage.

---

## 6. Claim-level evidence sufficiency

A claim may become `PASS` only if all of the following hold:

1. exact claim scope is bound;
2. all evidence records are immutable/version pinned;
3. no supporting evidence is project-circular;
4. no unresolved same-scope contradiction exists;
5. the evidence bundle contains at least one **provider-primary lineage (P1 or P2)**;
6. and the bundle contains at least one **distinct corroborating lineage** from:
   - P1/P2 independent provider artifact; or
   - I1/I2 independent non-provider artifact;
7. the two lineages independently support the material semantics of that exact claim.

Exception:

A single provider artifact may be sufficient only when it is itself a versioned normative specification explicitly and unambiguously defining the full claim **and** an adjudication record explains why no second lineage is necessary. Such a singleton PASS is classified:

`PASS_SINGLE_PROVIDER_NORMATIVE`

and remains eligible for later re-open if contradictory evidence appears.

Ordinary provider code plus project code is not two lineages.

Two non-provider sources without any provider-primary lineage cannot yield PASS under V0.1; they yield at most BLOCKED/PENDING_PROVIDER_CORROBORATION.

---

## 7. Claim verdicts

Exactly one adjudication verdict per claim:

### PASS

Used only when Section 6 sufficiency is met and no unresolved conflict remains.

### FAIL

Used only when evidence of adequate authority/scope establishes that the candidate claim is false for the exact target representation/version.

A FAIL requires an explicit contradicted candidate statement and the replacement fact, if known.

FAIL does not authorize silent mutation of B. It forces a distinct B correction/version decision.

### BLOCKED

Used when truth is not established either way, including:

- insufficient evidence;
- only project-circular evidence;
- only non-provider evidence;
- version ambiguity;
- representation/symbol scope ambiguity;
- unresolved conflict;
- stale evidence without scope mapping;
- evidence proving only part of the claim;
- evidence inaccessible/unpinned;
- empirical plausibility without authoritative expected semantics.

No UNKNOWN may be coerced to PASS.

---

## 8. Conflict semantics

Conflicts are adjudicated at claim + scope + version level.

### 8.1 Apparent conflict caused by different scope/version

If two sources refer to different:

- representation generations;
- provider APIs;
- symbol classes;
- versions;
- epochs;

they are not immediately contradictory.

The scope difference must be resolved before either can support the target claim.

### 8.2 Same-scope material contradiction

If admissible evidence disagrees materially on the same claim and target scope:

```text
claim = BLOCKED
```

until the conflict is resolved by additional authoritative evidence.

No automatic "provider always wins" shortcut is permitted if the provider artifact's applicability/version is itself ambiguous.

### 8.3 Confirmed authoritative contradiction

If exact-scope provider evidence unambiguously contradicts the B candidate and competing support is shown to be stale/wrong-scope/derived:

```text
claim = FAIL
```

The B candidate must later be corrected/version-forwarded before global B may pass.

---

## 9. Staleness and version binding

Evidence age alone is not staleness.

Evidence is stale for this contract when it cannot be shown to apply to the selected representation/version.

Mandatory rules:

- exact commits/releases preferred over moving branches/pages;
- undated/versionless pages require explicit target-scope justification;
- archived documentation may remain valid if representation continuity is established;
- latest documentation cannot be retroactively assumed to describe historical files;
- old documentation cannot be assumed to describe a later provider revision;
- instrument scaling evidence must bind USATECHIDXUSD or a provider rule demonstrably governing it.

Unresolved temporal/version applicability:

`BLOCKED`.

---

## 10. Representation-wide proof versus later acquisition-specific proof

### 10.1 Eligible for representation-wide qualification before project acquisition

B-PE-01 may, in principle, qualify without downloading project BI5 data:

```text
C01 compression/envelope
C02 slot width/framing
C03 primitive layout/order
C04 encoded timestamp-offset meaning
C05 ask/bid raw field roles
C06 provider-owned USATECHIDXUSD scaling rule
C07 encoded volume primitive/role semantics
C08 representation applicability
```

provided the documentary/reference evidence requirements are satisfied.

### 10.2 Explicitly deferred to a later bounded D acquisition

B-PE-01 cannot establish:

- that a concrete project component exists;
- exact component count;
- exact object/file hashes;
- whether expected components are missing/extra/repeated;
- completeness of a concrete acquisition;
- actual decompression success of project components;
- actual residual byte counts;
- actual anomaly incidence;
- actual observed millisecond ranges;
- actual price/volume value distributions;
- actual provider continuity for each acquired object;
- real Q outcome;
- real F universe;
- real I_A/I_B equality.

Those are later D/B/A/Q/F/Q-RM-12 execution evidence.

Representation truth must not be confused with acquisition truth.

---

## 11. Whole-contract result

The B-PE-01 evidence contract itself may receive:

- `PASS` — evidence-adjudication rules are complete enough to govern later evidence collection;
- `FAIL` — adversarial break demonstrates a contract defect;
- `BLOCKED` — required contract semantics cannot be specified without evidence/data not yet authorized.

This formalization candidate is not yet PASS.

Even a future:

`B-PE-01 EVIDENCE CONTRACT = PASS`

would mean only that the rules for judging evidence are qualified.

It would **not** mean C01-C08 are PASS.

---

## 12. Permission closure

B-PE-01 contract qualification permits no network/provider evidence gathering by itself and no data execution.

Still prohibited in this block:

```text
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

## 13. Pre-break verdict

```text
B-PE-01 EVIDENCE CONTRACT CANDIDATE = PERSISTED CANDIDATE
B-PE-01 EVIDENCE CONTRACT = NOT YET QUALIFIED

C01-C08 provider truth verdicts = NOT ADJUDICATED
B global executable gate = BLOCKED
```

Next within the current block:

```text
adversarially break this exact persisted evidence contract
```
