# AUDIT — OBSERVATION IDENTITY — CANONICAL QUALIFIED-RECORD SEQUENCE

**Date:** 4 September 2026  
**Reference HEAD:** `20f3197a268f6f4843af47008236306599f1046c`  
**Scope:** determine whether the current authoritative corpus contains an already-authorized rule capable of defining a canonical sequence of qualified primary records from which a stable positional identity could be assigned.  
**Status:** **BLOCKED FOR FREEZING**

---

## 1. QUESTION

The previous position-stability audit established:

```text
POSITIONAL IDENTITY FAMILY → ARCHITECTURALLY PLAUSIBLE
source_record_position AS NORMATIVE PRIMITIVE → NOT YET PROVEN
```

The present question is narrower:

> **Quelle règle amont peut définir une séquence canonique de records qualifiés permettant d'attribuer une position stable sans transformer cette position en ordre temporel ?**

The audit must determine whether such a rule already exists in the authoritative corpus, without creating a new architecture decision.

Three concepts are kept strictly separate:

```text
OBSERVATION IDENTITY
    = which primary record is being referred to

CANONICAL POSITION
    = deterministic coordinate assigned within a defined qualified dataset domain

TEMPORAL ORDER
    = independently established temporal relation between observations
```

In particular:

```text
position(A) < position(B)
```

must **not** imply:

```text
A precedes B
```

unless an independent normative temporal-order rule establishes that relation.

---

# 2. VERIFIED CORPUS CONSTRAINTS

The current repository state establishes the following:

1. `OI-01` assigns ownership of normative individual-observation identity to the upstream qualification/data-contract responsibility boundary; it does not define the identity mechanism.
2. Q-1 identity composition and Q-2 identity scope remain unresolved.
3. Q-3 is narrowed by necessary consequence: distinct observations retained by the qualified dataset must not be collapsed merely because visible content is identical.
4. `1.1.2` prohibits dependence on implicit runtime read order and requires deterministic transformation.
5. A-11 remains relevant because the corpus does not establish the complete upstream regime for observation order or source combination.
6. `09-DATASET-PROVENANCE-REGISTRY.md` is explicitly an architecture proposal / non-normative document and cannot supply a frozen sequence rule by itself.
7. `05-DATA-CONTRACT.md` is explicitly a proposal / non-validated and therefore cannot silently supply such a rule.
8. The current position-stability audit already established that a generic row number is insufficient and that the qualified sequence itself must be normatively defined.

**Classification of this section:**

```text
[NORMATIF — MASTER PLAN / DÉCISIONS DÉJÀ GELÉES]
[ABSENCE DE PREUVE — pour les éléments non établis dans le corpus]
```

---

# 3. CANDIDATE A — SOURCE-PROVIDED SEQUENCE

## Proposition audited

Use an ordering/record identifier supplied by the data provider as the canonical record sequence.

## Adversarial test

This is valid only if the upstream source contract establishes, for the relevant dataset:

- existence of a source-level sequence or stable record identifier;
- semantic meaning of that sequence;
- stability across acquisition;
- stability across provider reserialization;
- uniqueness within the required scope;
- preservation through qualification;
- behavior for duplicates and equal timestamps;
- behavior when the provider revises or republishes historical data.

## Finding

The current corpus does not establish such a provider guarantee.

A source field merely being present is not sufficient evidence that it is a stable identity primitive.

For the current concrete dataset, no normative provider guarantee has been established in the project corpus that would authorize this mechanism.

## Status

```text
NOT PROVEN
```

**Classification:** `[ABSENCE DE PREUVE]`

No source-provided identifier is promoted to normative status.

---

# 4. CANDIDATE B — PHYSICAL FILE / ROW ORDER

## Proposition audited

Use the order in which records physically occur in the source file(s), for example a row number.

## Adversarial tests

- different file traversal order;
- different concatenation order;
- provider re-export;
- insertion/removal before an existing record;
- equivalent content stored in another physical layout;
- multi-file acquisition;
- filtering before qualification.

## Finding

Physical position is relative to a physical representation. It is not intrinsically an attribute of the semantic primary observation.

Therefore:

```text
physical row number ≠ stable observation identity
```

unless the exact physical artifact and its record enumeration are themselves made normative and immutable.

The current corpus does not establish that regime.

## Status

```text
REJECTED AS GENERIC RULE
```

A future contract could explicitly make an immutable captured artifact and its enumeration normative, but that would be a separate adjudication, not an implication of the current corpus.

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]` for the rejection of generic physical row order; `[ARCHITECTURE PROPOSÉE]` for any future artifact-specific variant.

---

# 5. CANDIDATE C — QUALIFICATION-DEFINED CANONICAL SEQUENCE

## Proposition audited

The qualification layer establishes a deterministic sequence of the retained primary records before `1.1.2`, assigns the position once, and makes that position an immutable attribute of the qualified observation.

Conceptually:

```text
RAW
 ↓
QUALIFICATION
 ↓
IMMUTABLE QUALIFIED DATASET
 ↓
CANONICAL RECORD ENUMERATION
 ↓
POSITION ASSIGNED ONCE
 ↓
1.1.2
```

## Required properties

For this candidate to be normative, the upstream contract must define at minimum:

1. **Domain** — exactly which qualified dataset/version/lineage owns the sequence.
2. **Membership** — exactly which records are members of that sequence.
3. **Enumeration rule** — how every member receives one and only one position.
4. **Determinism** — same normative qualified dataset produces the same enumeration.
5. **Traversal independence** — runtime/file traversal order cannot alter assigned position.
6. **Qualification timing** — position assignment occurs at a defined stage and is not silently recomputed later.
7. **Duplicate preservation** — two distinct retained records may occupy distinct positions even with identical visible values.
8. **Equal timestamps** — equal timestamps do not require inventing temporal precedence.
9. **Multi-file/source combination** — combination semantics are explicitly defined.
10. **Dataset-version semantics** — a changed dataset is not silently treated as the same sequence.
11. **Cross-acquisition semantics** — whether equivalent acquisitions must reproduce the same identity is explicit rather than inferred.
12. **Serialization/comparison** — the assigned identity can be compared reproducibly across conforming implementations.

## Finding

This is the only candidate family that directly matches the requirement that identity be owned upstream while remaining independent of later runtime ordering and derived representations.

However, the actual canonical enumeration rule is absent from the current authoritative corpus.

Therefore the candidate is:

```text
ARCHITECTURALLY COMPATIBLE
BUT NOT NORMATIVELY DEFINED
```

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]` for the required properties; `[QUESTION NON RÉSOLUE]` for the actual enumeration rule.

---

# 6. CANDIDATE D — CONTENT SORT

## Proposition audited

Sort observations deterministically by their content fields, e.g. timestamp/bid/ask/volume.

## Adversarial test

Construct:

```text
O1 = (T, BID, ASK)
O2 = (T, BID, ASK)
```

where both records are distinct retained primary observations.

A content-only ordering cannot distinguish O1 from O2.

Adding an arbitrary tie-break based on collection position merely reintroduces the problem under another name.

Adding a runtime-generated tie-break would violate the requirement for deterministic, source-independent identity unless its source and stability are separately established.

## Finding

A pure content sort cannot define a unique canonical sequence while preserving strict duplicate individuality.

## Status

```text
REJECTED AS SUFFICIENT CANONICAL IDENTITY SEQUENCE
```

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

This does not prohibit content from being part of a future composite identity; it rejects content-only enumeration as sufficient for the present requirement.

---

# 7. CANDIDATE E — TEMPORAL SORT

## Proposition audited

Sort records by market timestamp and use the resulting sequence as the canonical positional sequence.

## Adversarial test

Consider multiple observations with the same timestamp or an upstream case where temporal precedence is unresolved.

A total sort requires a tie-break.

Any arbitrary tie-break creates an ordering relation not established by the source/corpus.

That would violate the separation:

```text
IDENTITY POSITION ≠ TEMPORAL ORDER
```

and conflicts with the established partial-order model for `ordered_ticks`, which explicitly forbids inventing an order relation that is not established.

## Finding

Temporal sorting is not a valid generic mechanism for defining canonical position when unresolved temporal relations exist.

Timestamp may be an input to an independently defined sequence rule, but timestamp ordering alone cannot manufacture missing physical order.

## Status

```text
REJECTED AS TEMPORAL-ORDER SUBSTITUTE
```

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

---

# 8. CANDIDATE F — SOURCE-STREAM + LOCAL ORDINAL

## Proposition audited

Define identity using a source stream identifier plus an ordinal assigned within that stream.

Conceptually:

```text
(source_stream, ordinal)
```

## Finding

This is a special case of an upstream-qualified positional/composite identity.

It can be valid only if the corpus defines:

- what constitutes one source stream;
- how streams are identified;
- how ordinals are assigned;
- whether the ordinal is source-defined or qualification-defined;
- stability under re-acquisition;
- multi-stream combination;
- duplicate semantics;
- scope and lineage.

The current corpus does not define these rules.

## Status

```text
PLAUSIBLE IDENTITY FAMILY
NOT PROVEN AS NORMATIVE
```

**Classification:** `[ARCHITECTURE PROPOSÉE]` as a candidate family; `[ABSENCE DE PREUVE]` for normative adoption.

---

# 9. CANDIDATE G — IMMUTABLE ARTIFACT OFFSET

## Proposition audited

Use an offset or exact physical locator inside an immutable captured artifact as part of identity.

## Finding

This can distinguish records within one exact immutable artifact, but it inherits the scope of that artifact.

It does not automatically establish:

```text
same logical dataset across two acquisitions
```

and it is sensitive to any transformation that changes physical representation.

It therefore may be a provenance locator, but it cannot be promoted automatically to semantic observation identity.

## Status

```text
INSUFFICIENT AS GENERIC IDENTITY RULE
```

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]` for the limitation; `[OPTION]` for using it as supplementary provenance metadata.

---

# 10. CROSS-CANDIDATE ADVERSARIAL MATRIX

| Candidate | Traversal independent | Preserves strict duplicates | Avoids artificial temporal order | Multi-file semantics defined | Cross-acquisition stability proven | Current corpus authorization |
|---|---:|---:|---:|---:|---:|---|
| A Source-provided sequence | ? | ? | ? | ? | ? | NOT PROVEN |
| B Physical file/row order | NO | YES | YES | NO | NO | REJECTED GENERICALLY |
| C Qualification-defined canonical sequence | YES* | YES* | YES* | ? | ? | ARCHITECTURALLY COMPATIBLE / UNDEFINED |
| D Content sort | YES | NO | YES | YES | ? | REJECTED AS SUFFICIENT |
| E Temporal sort | YES | YES* | NO | YES | ? | REJECTED AS ORDER SUBSTITUTE |
| F Source-stream + ordinal | YES* | YES* | YES* | ? | ? | NOT PROVEN |
| G Immutable artifact offset | YES within artifact | YES | YES | NO | NO | INSUFFICIENT GENERICALLY |

`*` only if the missing upstream contract explicitly defines the required semantics.

---

# 11. CRITICAL DISTINCTIONS PRESERVED

The audit confirms the following must not be collapsed:

### 11.1 Same qualified dataset vs new dataset version

A change to dataset membership/content may create a new normative dataset state. No identity-preservation requirement across different dataset versions is inferred automatically.

### 11.2 Same primary record vs same economic event

Two distinct retained source records may have identical visible values without proving whether they represent one or multiple economic events.

```text
observation identity ≠ market-event identity
```

### 11.3 Position vs temporal order

A position is an identity coordinate inside a domain. It is not itself a temporal relation.

### 11.4 Runtime index vs assigned position

A runtime collection index is not equivalent to an immutable position assigned upstream.

---

# 12. REQUIRED ADVERSARIAL TESTS FOR THE UPSTREAM CONTRACT

Before any positional identity is frozen, the eventual upstream contract must support tests for:

1. **Traversal invariance** — same qualified dataset, different file/read traversal.
2. **Runtime reorder invariance** — post-qualification in-memory reorder.
3. **Strict duplicate preservation** — identical visible records remain distinguishable when both are retained.
4. **Equal timestamp** — identity distinction without inferred temporal precedence.
5. **Multi-file combination** — equivalent source records under different file partitioning.
6. **Qualification boundary** — filtering before/after position assignment is not ambiguous.
7. **Dataset version change** — adding/removing/revising records produces explicitly distinguishable dataset state.
8. **Re-acquisition** — same logical dataset only requires same identities if cross-acquisition equivalence is explicitly defined.
9. **Source revision** — provider reserialization/revision does not silently preserve or destroy identity without a defined rule.
10. **No future dependence** — position assignment itself cannot depend on data occurring after the observation's admissible temporal boundary when that would violate the applicable point-in-time contract.
11. **No artificial total order** — unresolved temporal relations remain unresolved.
12. **BAR propagation** — identity remains unchanged from qualified primary observation through `BAR_IN_PROGRESS` and `BAR_CLOSED`.

---

# 13. RESULT

The audit does **not** authorize a positional identity implementation.

It establishes:

```text
GENERIC ROW / FILE ORDER
→ INSUFFICIENT

CONTENT-ONLY ORDER
→ INSUFFICIENT

TEMPORAL SORT
→ NOT ACCEPTABLE AS A SUBSTITUTE FOR PHYSICAL ORDER

SOURCE-PROVIDED SEQUENCE
→ NOT PROVEN BY CURRENT CORPUS

SOURCE-STREAM + ORDINAL
→ PLAUSIBLE FAMILY, NOT PROVEN

IMMUTABLE ARTIFACT OFFSET
→ PROVENANCE LOCATOR ONLY, NOT GENERIC SEMANTIC IDENTITY

QUALIFICATION-DEFINED CANONICAL SEQUENCE
→ ONLY ARCHITECTURALLY COMPATIBLE FAMILY IDENTIFIED,
   BUT ITS NORMATIVE ENUMERATION RULE IS ABSENT
```

Therefore:

```text
CANONICAL QUALIFIED-RECORD SEQUENCE
→ NOT YET ESTABLISHED

POSITIONAL IDENTITY FREEZE
→ BLOCKED

V12-01
→ STILL BLOCKED

1.1.2
→ NOT CLOSED
```

**Overall audit verdict:**

```text
BLOCKED
```

---

# 14. NO NEW DECISION

This audit does not decide:

- Q-1 identity composition;
- Q-2 identity scope;
- source ordering policy;
- source-combination regime;
- duplicate-event semantics;
- cross-acquisition equivalence;
- identity encoding;
- hash algorithm;
- serialization format;
- collision policy;
- late-tick policy;
- `event_time` / `availability_time` semantics.

No correction of `1.1.2` is authorized.

No Option B freeze is authorized.

---

# 15. NEXT BLOCK CONDITION

The blocker is now precisely identified:

```text
UPSTREAM CANONICAL RECORD SEQUENCE
        ↓
SCOPE + MEMBERSHIP + ENUMERATION + STABILITY RULES
        ↓
Q-1 / Q-2 EXPLICIT IDENTITY DECISION
        ↓
Q-4 → Q-7 DEPENDENT ADJUDICATION
        ↓
1.1.2 CORRECTION
        ↓
NEW ADVERSARIAL AUDIT
```

The next human/architectural adjudication is therefore **not** “position or no position”.

It is:

> **Can the upstream contract normatively define a canonical enumeration of qualified primary records, and if so, what exact rule determines that enumeration without creating temporal order?**

Until that question is explicitly answered, the implementation path remains blocked.

## FIN
