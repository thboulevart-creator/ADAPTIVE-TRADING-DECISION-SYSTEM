# ADJUDICATION — Q-RM-03 NON-OBSERVATION MATERIAL

**Date:** 5 septembre 2026  
**Scope:** semantic classification of non-observation material under validated RB-A / Q-RM-01 / Q-RM-02  
**Status:** **PASS — SEMANTIC RULE RESOLVED; CONCRETE FORMAT CLASSIFICATIONS REMAIN OPEN**  
**Exclusions:** no `CANONICAL_RECORD_POSITION`, no canonical enumeration, no temporal ordering, no physical identity primitive.

---

## 1. QUESTION

For a declared acquisition representation and its applicable versioned RB-A binding, how must the system classify:

- headers;
- metadata;
- comments;
- separators;
- technical envelopes;
- empty material;
- mixed material containing both non-observation content and primary observations;

so that non-observation material cannot silently enter the primary logical-record universe, while genuine observation payload is not silently discarded?

The rule must remain compatible with Q-RM-02: valid absence of primary observation may yield `C = 0`, but malformed or ambiguous input must never be disguised as zero cardinality.

---

## 2. BASE NORMATIVE STATE

RB-A has already been validated: the logical record model is semantic and is bound explicitly and versionedly to each declared acquisition representation.

Q-RM-02 has already resolved the cardinality semantics:

```text
VALID + no primary observation     → C = 0
VALID + one primary observation    → C = 1
VALID + multiple observations      → C = N
INVALID                            → qualification outcome distinct
AMBIGUOUS                          → qualification outcome distinct
```

The current question therefore does **not** reopen whether `0 / 1 / N` exists. It determines how material is classified before that cardinality is established.

The existing normative record-model candidate already requires deterministic treatment of headers/metadata/non-observation material and states that such material cannot silently enter the primary observation universe. cite-not-used-in-repo-document

---

## 3. FORMALIZATION

Let `u` be a physical unit interpreted under representation `R` and versioned binding `B`.

The binding induces a deterministic semantic classification:

```text
K_B(u) → classification / interpretation
```

The classification must distinguish at least:

```text
PRIMARY_OBSERVATION_MATERIAL
NON_OBSERVATION_MATERIAL
MIXED_MATERIAL
INVALID
AMBIGUOUS
```

`NON_OBSERVATION_MATERIAL` is material which, under the applicable binding, has no primary-observation role.

`PRIMARY_OBSERVATION_MATERIAL` is material which contributes to one or more primary observations.

`MIXED_MATERIAL` contains both roles and must be semantically partitioned by the binding before cardinality is determined.

`INVALID` means the unit violates the applicable binding and cannot be validly interpreted.

`AMBIGUOUS` means the applicable binding does not determine one unique semantic classification/partition.

The classification is semantic, not heuristic.

---

## 4. CANDIDATE RULE

> **Under RB-A, non-observation material is material that the applicable declared and versioned binding explicitly classifies as having no primary-observation role. It contributes no primary occurrence by itself. Mixed units are partitioned according to the same binding, and only the semantically identified primary-observation portions participate in cardinality. A parser may not infer semantic role from superficial syntax, field count, position, naming, or implementation convenience when the binding does not establish that inference.**

Therefore:

```text
header only                  → valid non-observation → C = 0
comment only                 → valid non-observation → C = 0
metadata only                → valid non-observation → C = 0
technical envelope only      → valid non-observation → C = 0
header + observation         → mixed → classify/partition → observation contributes to C
metadata + 3 observations    → mixed → classify/partition → C = 3
malformed material           → INVALID, not C = 0
ambiguous role               → AMBIGUOUS, not C = 0
```

These examples are semantic illustrations, not concrete format bindings.

---

## 5. NECESSARY DISTINCTIONS

### 5.1 Material is not automatically a record

A physical unit may contain material which exists for transport, schema description, commentary, provenance, or other technical purposes without representing a primary market observation.

Physical presence therefore does not imply primary-record membership.

### 5.2 Non-observation material is not discarded by arbitrary parser choice

The rule is not:

```text
"anything I cannot map to an observation is metadata"
```

That would turn malformed data into non-observation material and could silently erase observations.

Instead:

```text
binding says non-observation → NON_OBSERVATION
binding cannot determine role → AMBIGUOUS / INVALID as applicable
```

### 5.3 Mixed content is first-class

A unit may contain both non-observation and observation material.

The binding must define how the two are separated semantically.

The presence of a header, metadata block, separator, or technical envelope must not force the entire unit to be classified as non-observation when valid primary observations are also present.

Conversely, the presence of observation-looking fields must not force technical material into the primary universe.

### 5.4 Metadata can be structurally similar to observations

A metadata object may contain fields that resemble observation fields.

Therefore lexical similarity, field names, numeric shape, or parseability alone cannot establish primary-observation status.

The binding must supply the semantic role.

### 5.5 Comments and separators are contextual

A comment marker or separator may be universally obvious in some representation, but the normative rule cannot assume a syntax that has not been declared by the applicable binding.

The general model defines the semantic category; the binding defines how that category is recognized for the representation/version.

---

## 6. MIXED CONTENT RULE

For mixed material:

```text
u = M_nonobs + M_primary
```

The binding must produce a deterministic partition:

```text
partition_B(u) = (M_nonobs, M_primary)
```

The non-observation component contributes zero primary observations unless the binding explicitly defines that material as part of the payload of an observation.

The primary component is then segmented into observations under Q-RM-02.

Thus:

```text
header + 1 observation      → C = 1
metadata + 3 observations   → C = 3
comments + 0 observations   → C = 0
technical envelope + 2 obs → C = 2
```

The phrase "part of the payload" is important: material can be non-independent of an observation without itself being an additional occurrence.

---

## 7. ENVELOPE VS PAYLOAD

A technical envelope may surround, precede, or follow observation payload.

The model must distinguish:

```text
transport/container structure
            ≠
primary observation occurrence
```

An envelope does not create an occurrence merely because it is physically present.

However, an envelope field may legitimately belong to the logical payload of an observation if the binding explicitly defines that semantic role.

This does not make the envelope itself a separate occurrence.

---

## 8. ADVERSARIAL CASSAGE

### C-01 — "Anything not parsed as observation is metadata"

**Failure:** malformed or unsupported observation data could disappear silently.

**Correction:** non-observation status requires positive normative classification by the applicable binding. Failure to classify is not proof of non-observation.

### C-02 — "Header is always non-observation"

**Failure:** a representation could encode a legitimate first observation in a structure that superficially resembles a header.

**Correction:** header status is binding-defined, not a universal lexical heuristic.

### C-03 — "Metadata-looking object is never an observation"

**Failure:** semantic role cannot be established from appearance alone.

**Correction:** declared binding controls role; ambiguity remains explicit.

### C-04 — "Mixed unit becomes one record"

**Failure:** container/envelope granularity would incorrectly determine logical cardinality.

**Correction:** mixed material is partitioned semantically; observations are then segmented under Q-RM-02.

### C-05 — "Every separator creates a zero-record unit"

**Failure:** technical separators may not constitute independently meaningful acquisition units at all.

**Correction:** `C = 0` is a semantic result for a valid interpreted unit; it does not require inventing a separate logical record/unit merely because bytes exist.

### C-06 — "Discard comments before parsing and therefore avoid ambiguity"

**Failure:** preprocessing could alter the semantic input before the binding has established what the material means.

**Correction:** classification is part of the normative interpretation, not an implementation-specific preprocessing shortcut.

### C-07 — "Field names determine role"

**Failure:** metadata and observations can share field names.

**Correction:** field names alone are insufficient unless the binding explicitly makes them normative.

### C-08 — "Non-observation material can be attached to any nearby observation"

**Failure:** proximity is not semantic association and can differ under traversal/chunking.

**Correction:** attachment rules must be explicitly specified by the binding where association affects payload interpretation.

---

## 9. RE-CASSAGE

### RC-01 — Universal taxonomy without binding

A global taxonomy such as `header/comment/metadata/separator` is insufficient to make concrete classification executable across all formats.

**Result:** retain a universal semantic distinction but defer recognition rules to explicit versioned bindings.

### RC-02 — Binding says "ignore metadata"

This wording is insufficient if "metadata" is itself not normatively identifiable.

**Result:** a conforming binding must define the recognition/classification boundary, not merely instruct an implementation to ignore a named category.

### RC-03 — Mixed material with ambiguous boundary

If the binding cannot uniquely determine which material is observation payload and which is non-observation material, the implementation may not choose the most convenient partition.

**Result:** classification remains AMBIGUOUS and proceeds to Q-RM-04; no qualified universe is produced from an arbitrary choice.

### RC-04 — Empty physical material

An empty physical unit does not automatically imply either invalidity or a logical zero-occurrence unit.

**Result:** the applicable binding must define whether empty input is valid and, if valid, whether it yields `C = 0`.

### RC-05 — Non-observation material carrying provenance

A provenance field can be important without being a primary observation field.

**Result:** logical importance does not imply primary-observation membership. Its role must be specified by the binding/model.

### RC-06 — Observation payload contains technical fields

A technical field may legitimately be part of an observation payload.

**Result:** "technical" is not synonymous with "non-observation". Semantic role, not naming, controls classification.

---

## 10. ROBUST ANSWER

The robust rule is:

```text
For declared representation R and versioned binding B:

1. B defines the semantic classification of material.
2. B distinguishes primary-observation material from non-observation material.
3. Non-observation material contributes no primary occurrence by itself.
4. Mixed material is deterministically partitioned when the binding permits it.
5. Only primary-observation material enters the Q-RM-02 segmentation/cardinality process.
6. Technical/envelope material may contribute fields to an observation only when B explicitly defines that role; it does not create an occurrence by itself.
7. Failure to recognize material is not evidence that it is non-observation.
8. INVALID and AMBIGUOUS are never silently converted to C = 0.
9. Classification must be independent of traversal, parallelism, caching and downstream serialization.
10. Concrete recognition rules are part of the declared, versioned format binding.
```

This yields the invariant:

```text
No primary observation can enter the qualified primary universe merely because
its physical material was parseable or located inside an acquisition object.

No valid primary observation can disappear merely because its material was
conveniently classified as metadata, comment, separator, or envelope.
```

---

## 11. VERDICT

```text
Q-RM-03 SEMANTIC RULE = PASS
CONCRETE FORMAT CLASSIFICATION RULES = BLOCKED
```

The semantic architecture is sufficiently determined: non-observation status is a binding-governed semantic classification; mixed material is explicitly supported; non-observation does not create primary occurrences; malformed/ambiguous material remains distinct from valid zero cardinality.

The concrete classification tables for supported representations are still required before the overall record model can be frozen.

---

## 12. GOVERNANCE

This block does not authorize:

- `CANONICAL_RECORD_POSITION`;
- canonical enumeration;
- temporal precedence;
- physical identity primitives;
- modification of `1.1.2`;
- silent parser heuristics;
- global assumptions about CSV/JSON/binary/etc. syntax.

Next dependency: Q-RM-04 — malformed / ambiguous input policy.

## FIN
