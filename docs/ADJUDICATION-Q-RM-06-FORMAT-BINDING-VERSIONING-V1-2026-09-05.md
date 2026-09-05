# ADJUDICATION — Q-RM-06 FORMAT BINDING / VERSIONING

**Date:** 5 septembre 2026  
**Scope:** normative binding contract between declared physical acquisition representations and RB-A logical record semantics  
**Status:** **PASS — UNIVERSAL BINDING / VERSIONING POLICY CLOSED; CONCRETE FORMAT BINDINGS REMAIN BINDING-SPECIFIC WORK**  
**Reference:** Q-RM-01 RB-A, Q-RM-02 cardinality, Q-RM-03 non-observation material, Q-RM-04 failure-scope, Q-RM-05 acquisition domain  
**Exclusions:** no `CANONICAL_RECORD_POSITION`, no canonical enumeration, no temporal precedence, no physical identity primitive.

---

## 1. QUESTION

RB-A establishes a semantic logical record model with explicit bindings for declared representations. Q-RM-02 through Q-RM-05 establish the semantic constraints that the binding must satisfy.

The remaining question is:

> **What must a format binding declare and how must it be versioned so that two conforming implementations cannot silently interpret the same declared acquisition differently, especially when format, schema, framing, encoding, segmentation, anomaly handling, or interpretation changes?**

A binding is not an implementation adapter chosen for convenience. It is part of the normative input to the physical→logical mapping.

---

## 2. EXISTING NORMATIVE BASIS

RB-A already states that the logical model is abstract and that each declared representation requires an explicit, versioned binding. It also explicitly rejects treating a physical row, line, byte range, packet, provider identifier, or other primitive as the universal semantic definition of a record. fileciteturn32file0L2-L2

Q-RM-02 already requires physical→logical cardinality to be determined by the declared representation and versioned binding, rather than by runtime traversal or an implicit physical convention. Q-RM-03 similarly requires deterministic semantic classification of non-observation material. Q-RM-04 closes the failure-scope policy while leaving concrete anomaly matrices as a binding obligation. Q-RM-05 establishes that acquisition-domain membership is a normative declaration rather than an inference from physical file boundaries.

The existing `05-DATA-CONTRACT.md` is explicitly version `0.1 — PROPOSITION, non validée`; it cannot silently be used as a frozen binding specification. fileciteturn33file0L1-L2

Therefore this decision closes the **universal binding/versioning policy**, not the concrete CSV/JSON/binary/vendor bindings themselves.

---

## 3. FORMALISATION

Let:

```text
D  = declared acquisition domain
R  = declared physical representation
M  = versioned RB-A record-model version
B  = versioned format binding
Q  = applicable qualification contract/version
```

The normative mapping is:

```text
MAPPING(D, R, M, B, Q)
        → logical record interpretation
```

The binding `B` must determine every representation-specific rule capable of changing the logical universe, including where applicable:

```text
- physical representation / format family
- encoding and decoding semantics
- framing / container semantics
- record boundaries
- grouping / splitting rules
- field mapping and field types
- observation vs non-observation classification
- zero / one / N cardinality
- malformed / ambiguous anomaly classes
- constructive localisability conditions
- acquisition-fatal anomaly classes
- qualification interaction
- version applicability
```

If any such property is left to implementation behavior, the binding is incomplete for normative qualification.

---

## 4. ADOPTED UNIVERSAL RULE — BINDING CONTRACT

### R1 — Binding completeness

A format binding is **normatively applicable** only if it explicitly identifies the representation semantics necessary to determine the logical record universe.

At minimum, an applicable binding must make the following deterministic:

```text
representation identity
record boundaries
logical segmentation
cardinality
non-observation classification
field interpretation
malformed/ambiguous handling
qualification interaction
binding version
```

A binding may reference shared universal rules instead of repeating them, but the resulting normative closure must be unambiguous.

### R2 — Binding version as a semantic determinant

A binding version is part of the normative input whenever a change can alter any of:

```text
record boundaries
occurrence count
occurrence individuation
logical payload interpretation
non-observation classification
qualification membership
failure scope
```

Such a change **must not** be silently treated as an implementation update.

### R3 — Non-semantic implementation changes

An implementation/library/runtime change that is proven not to alter the normative semantics need not create a new binding version merely because the implementation changed.

However, the burden is on conformance evidence to establish semantic equivalence. Library behavior is never itself the normative rule.

### R4 — Unknown or missing binding

If the applicable binding cannot be uniquely identified, is unavailable, is unsupported, or is internally incomplete for a property affecting logical membership:

```text
→ no normative qualified universe may be produced.
```

The implementation must not select a “closest” binding, infer a version, fall back to parser defaults, or silently substitute another schema.

### R5 — Binding precedence

Where multiple normative layers apply, their relationship must be explicit. A lower-level format binding cannot silently override a higher-level RB-A invariant.

Therefore:

```text
RB-A universal invariants
        ↓
acquisition-domain declaration
        ↓
record-model version
        ↓
format binding version
        ↓
qualification-specific parameters
```

is interpreted as a dependency structure, not as permission for a lower layer to contradict an upstream invariant.

### R6 — Version identity is part of reproducibility

A qualified dataset must retain enough normative version information to reconstruct which semantic contract was applied.

At minimum, the reconstruction reference must identify:

```text
acquisition domain declaration
record-model version
binding identifier
binding version
qualification contract/version
```

This does not prescribe where those identifiers are physically stored.

---

## 5. ADVERSARIAL CASSAGE

### C-01 — Same bytes, two parser libraries

Two implementations use different CSV/JSON/binary libraries and obtain different segmentation or coercion behavior.

**Result:** library behavior is not normative. Both implementations must conform to the same binding. A divergence means at least one implementation is non-conforming.

**No break.**

### C-02 — Same format name, different schema versions

Two files are both called “CSV”, but one uses five fields and another six, with a changed field meaning.

**Result:** “CSV” is not sufficient binding identity. The declared binding/version must distinguish semantics capable of changing the logical universe.

**No break.**

### C-03 — Schema evolution without explicit version

A producer adds a field or changes a field's interpretation while keeping the same nominal format identifier.

If the change can alter boundaries, payload interpretation, cardinality, individuation, or qualification membership, silently retaining the old binding would make the same nominal identifier map to different logical universes.

**Result:** a new binding version is required.

**No break.**

### C-04 — Backward-compatible extension

A producer adds an optional field that the binding explicitly declares semantically irrelevant to the logical primary record.

**Result:** a new version is not logically required merely because physical bytes changed, provided the binding contract explicitly establishes semantic equivalence for the logical universe.

The physical artifact remains a new acquisition/transformation as required by upstream data-contract rules; the question here is specifically whether the record-binding semantics changed.

**No break.**

### C-05 — Encoding change

UTF-8, another character encoding, BOM handling, escape semantics, newline semantics, or byte decoding changes how boundaries or fields are interpreted.

**Result:** encoding behavior belongs to the applicable binding. If the change can alter logical interpretation, it requires a distinct binding version or an explicitly declared versioned compatibility rule.

**No break.**

### C-06 — Compression / envelope layer

A compressed archive or technical envelope wraps an otherwise identical observation stream.

**Result:** the envelope may be represented as a binding layer or explicit compositional binding, but the normative contract must uniquely determine how the underlying logical representation is obtained. Compression itself cannot silently define record boundaries or occurrence identity.

**No break.**

### C-07 — One physical object contains multiple observations

A single physical object contains multiple primary observations.

**Result:** the binding must explicitly define semantic segmentation/cardinality. The object is not automatically one logical record.

**No break.**

### C-08 — Several physical objects form one logical record

A record is split across chunks/files/segments.

**Result:** Q-RM-05 acquisition-domain semantics and the binding must define the grouping relation. Physical file boundaries do not automatically terminate a logical record.

**No break.**

### C-09 — Missing binding version

The implementation detects a supported format but cannot determine which binding version applies.

**Result:** no “best effort” version selection. Qualification is blocked.

**No break.**

### C-10 — Unknown anomaly class

A malformed input does not match any declared anomaly class in the binding.

Q-RM-04 prohibits turning this into `C=0` or silently repairing it.

**Result:** the binding is incomplete for that case; the acquisition cannot receive a normative qualified universe until the anomaly is normatively classified. This is not an implementation license to invent a local treatment.

**No break.**

### C-11 — Binding claims localisability incorrectly

The binding declares an anomaly localisable, but an admissible alternative interpretation changes the boundaries or membership of other occurrences.

**Result:** the binding is non-conforming. Q-RM-04's localisability condition is violated.

**No break.**

### C-12 — Parser silently repairs malformed content

A parser replaces a missing field, normalizes malformed framing, or guesses a delimiter.

**Result:** the implementation has introduced semantics not present in the binding. It cannot produce a normative qualified universe on that basis.

**No break.**

### C-13 — Binding version changes after qualification

A previously qualified dataset is reprocessed under a newer binding that changes logical membership.

**Result:** this is not an invisible refresh of the same logical universe. It produces a semantically different qualified dataset state that must be distinguishable by the applicable dataset/version contract.

**No break.**

### C-14 — Two conforming implementations

Given:

```text
same D
same R
same M
same B
same Q
```

both implementations must produce the same logical record universe.

If they do not, at least one implementation or the binding is non-conforming.

**No break.**

---

## 6. SECOND CASSAGE — POSSIBLE FAILURES OF THE RULE

### Attack A — “Version everything” becomes meaningless

If every implementation change automatically creates a new version, versioning ceases to identify semantic changes.

**Resolution:** versioning is required by semantic impact, not by implementation churn. Non-semantic changes may retain the same binding version only when semantic equivalence is established.

### Attack B — A binding can be internally contradictory

For example:

```text
boundary rule → fixed-length records
anomaly rule  → delimiter controls boundary
```

with no precedence relation.

**Resolution:** an internally contradictory or incomplete binding is not applicable. It cannot be resolved by parser preference.

### Attack C — Composite bindings create hidden version dependencies

A binding may depend on encoding, compression, schema and envelope sub-bindings whose versions are omitted.

**Resolution:** the normative binding identity must include or deterministically reference every versioned dependency capable of changing logical interpretation. A vague parent identifier is insufficient.

### Attack D — “Same logical output” hides different interpretation

Two bindings might happen to produce the same records on one dataset while having different semantics on another.

**Resolution:** binding equivalence cannot be established solely by observing equality on one corpus. The normative definitions must establish semantic equivalence for the declared domain, or the bindings remain distinct.

### Attack E — Version identifier is present but mutable

An identifier such as `v1` is reused while its content changes.

**Resolution:** a version identifier must refer to an immutable normative binding definition. Mutating its semantics without a new version destroys reproducibility and is non-conforming.

### Attack F — Binding chooses a physical primitive as identity

A binding declares “row number = observation identity”.

**Resolution:** Q-RM-06 cannot override the upstream acquisition-scoped occurrence identity architecture. A physical locator may be provenance, but it cannot silently become the universal semantic identity merely because a binding declares it convenient.

### Attack G — Qualification parameters alter record membership

A parameter changes whether a record is retained, while the binding version remains unchanged.

**Resolution:** the qualification contract/version is an independent normative determinant and must be included in the reconstruction tuple. Binding versioning cannot be used as a substitute for qualification versioning.

---

## 7. ROBUST FORMULATION

The adopted universal rule is:

> **For every declared acquisition representation, physical→logical interpretation shall be governed by an explicitly identifiable and immutable versioned format binding. The binding shall deterministically define every representation-specific property capable of changing record boundaries, cardinality, non-observation classification, logical field interpretation, occurrence individuation, qualification membership, or failure scope. Missing, unknown, unsupported, incomplete, contradictory, or non-conforming binding semantics cannot be resolved by implementation preference and prevent normative qualification. Changes capable of altering the logical universe require a distinct binding version. Changes proven semantically equivalent may retain the binding version.**

This closes the universal policy while deliberately leaving concrete format matrices to their own binding specifications.

---

## 8. CONFORMANCE MATRIX

| Property | Normative requirement | Failure if absent |
|---|---|---|
| Binding identity | Unambiguous | Qualification blocked |
| Binding version | Immutable / identifiable | Qualification blocked |
| Representation semantics | Explicit | Qualification blocked |
| Record boundary | Deterministic | Qualification blocked |
| Cardinality | Deterministic | Qualification blocked |
| Non-observation classification | Deterministic | Qualification blocked |
| Field interpretation | Deterministic | Qualification blocked |
| Malformed/ambiguous policy | Declared | Qualification blocked |
| Localisability criteria | Constructive where used | Qualification blocked |
| Acquisition-fatal classes | Explicit where used | Cannot infer acquisition rejection |
| Qualification interaction | Explicit | Qualification blocked |
| Version dependencies | Complete / reconstructable | Qualification blocked |
| Physical identity primitive | Not imposed | Any silent substitution = non-conformance |

---

## 9. IMPORTANT SCOPE DISTINCTION

Q-RM-06 closes the **normative contract for bindings and versioning**.

It does **not** claim that the project already possesses complete concrete bindings for every supported representation.

Therefore:

```text
UNIVERSAL BINDING POLICY              = PASS
CONCRETE FORMAT BINDING INVENTORY     = NOT YET CLOSED
CONCRETE ANOMALY MATRIX               = NOT YET CLOSED
CONCRETE CSV/JSON/BINARY CONTRACTS    = NOT YET CLOSED
```

A concrete binding that does not satisfy this policy is simply **not eligible for normative qualification**. The universal rule must not be weakened to accommodate an incomplete binding.

This distinction is essential because the existing data contract remains explicitly provisional/non-validé. fileciteturn33file0L1-L2

---

## 10. INVARIANTS PRESERVED

Q-RM-06 does not modify:

- RB-A;
- occurrence-based individuality;
- strict duplicate preservation;
- Q-RM-02 cardinality semantics;
- Q-RM-03 non-observation classification;
- Q-RM-04 failure-scope policy;
- Q-RM-05 acquisition-domain semantics;
- acquisition-scoped identity;
- qualification-before-canonical-enumeration;
- temporal authority of `ordered_ticks`;
- qualification freeze requirement.

It introduces no:

```text
CANONICAL_RECORD_POSITION
canonical order
row ordinal
byte-offset identity
provider identity
hash identity
new temporal rule
```

---

## 11. DETERMINISM GATE

For a conforming concrete binding, the following must hold:

```text
same acquisition domain
+ same declared representation
+ same record-model version
+ same binding identifier/version
+ same qualification contract/version
        ↓
same logical boundaries
        ↓
same logical occurrences
        ↓
same qualification membership
```

Any divergence between conforming implementations is evidence of either:

```text
implementation non-conformance
or
binding non-conformance
```

It is not an admissible third interpretation.

---

## 12. VERDICT

```text
Q-RM-06 UNIVERSAL FORMAT-BINDING POLICY = PASS
Q-RM-06 VERSIONING POLICY              = PASS
Q-RM-06 CONCRETE FORMAT BINDINGS       = BLOCKED
```

**Q-RM-06 is closed at the universal normative level.**

The remaining concrete binding work is a downstream implementation/specification obligation. It does not reopen RB-A or Q-RM-02..05.

---

## 13. NEXT LOGICAL BLOCK

Proceed to **Q-RM-07 — Qualification Freeze**.

Question:

> **At what exact normative point does the qualified logical record universe become immutable, and what versioned inputs must be sufficient to reproduce that exact universe after traversal, parallelism, cache, restart, serialization, or downstream reordering?**

Q-RM-07 must close immutability/reconstruction semantics without introducing canonical enumeration or a physical identity primitive.

Only after Q-RM-07 should the complete Record Model package be re-audited as a single closure gate before any work on `CANONICAL_RECORD_POSITION`.

## FIN
