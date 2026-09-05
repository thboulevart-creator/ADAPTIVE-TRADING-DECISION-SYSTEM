# ADJUDICATION — Q-RM-05 ACQUISITION DOMAIN

**Date:** 5 septembre 2026  
**Scope:** normative acquisition-domain semantics for the logical record model under RB-A / Q-RM-01..04  
**Status:** **PASS — UNIVERSAL DOMAIN RULE CLOSED; CONCRETE ACQUISITION DECLARATION REMAINS BINDING-SCOPED**  
**Exclusions:** no `CANONICAL_RECORD_POSITION`, no canonical enumeration, no temporal ordering, no new physical identity primitive.

---

## 1. QUESTION

When the physical input for one qualification operation is distributed across multiple files, objects, partitions, chunks, streams, or independently delivered units, what constitutes one logical acquisition domain?

The decision must distinguish:

```text
acquisition domain
≠ physical container
≠ physical order
≠ temporal order
≠ canonical enumeration
```

It must also remain compatible with the already established **acquisition-scoped identity** semantics.

---

## 2. STARTING INVARIANTS

The following are not reopened:

1. RB-A is the semantic logical record-model architecture.
2. Logical record boundaries and cardinality are governed by the applicable versioned model/binding.
3. Strict duplicate observations remain distinct retained occurrences.
4. Q-RM-04 forbids silent repair and makes failure scope normative.
5. Qualification membership precedes canonical enumeration.
6. No canonical position is created at record-model stage.
7. The record model does not establish temporal precedence.
8. Observation identity is acquisition-scoped; no cross-acquisition continuity is inferred.

The Q-RM-05 question is therefore **scope**, not identity implementation.

---

## 3. FORMALISATION

Let an acquisition declaration be:

```text
A = (domain declaration, representation set, record-model version,
     applicable bindings, qualification contract)
```

Let the physical input units supplied to that declared acquisition be:

```text
U(A) = {u1, u2, ..., un}
```

The acquisition domain is the **normatively declared qualification scope** to which the same acquisition-level record-model and qualification semantics apply.

Physical subdivision is merely a representation of that domain unless the applicable contract explicitly declares the subdivision itself to define separate acquisition domains.

Therefore:

```text
one file            may be one acquisition domain
many files           may be one acquisition domain
one partition        may be one acquisition domain
many partitions      may be one acquisition domain
one stream            may be one acquisition domain
many chunks           may be one acquisition domain
```

No physical cardinality convention determines the domain by itself.

---

## 4. RULE CANDIDATE R1

### R1 — Declared qualification scope owns the acquisition boundary

An acquisition domain is determined by an explicit, versioned acquisition declaration that identifies which physical representation units are jointly submitted to one qualification operation under one applicable record-model/qualification contract.

A physical subdivision does **not** create a new acquisition domain merely because it is:

- a different file;
- a different object;
- a different partition;
- a different chunk;
- a different stream segment;
- delivered at a different time;
- processed by a different worker.

Conversely, physical units must not be merged into one acquisition domain merely because they:

- have the same filename pattern;
- contain adjacent timestamps;
- come from the same provider;
- look like continuation files;
- contain similar observations;
- happen to be available in the same runtime operation.

The declaration, not runtime convenience, determines the domain.

---

## 5. FIRST ADVERSARIAL CASSAGE

### C-01 — One acquisition split into ten files

The acquisition declaration explicitly identifies all ten files as components of one acquisition.

**Result:** one acquisition domain.

The ten files do not become ten acquisition identities merely because they are physically separate.

### C-02 — Ten files happen to look related

No acquisition declaration joins them.

**Result:** no implementation may silently merge them into one acquisition domain based on filename, timestamp continuity, provider, or directory layout.

If qualification requires a declared domain and none exists, the input is not eligible for normative qualification under this contract.

### C-03 — One logical stream split into chunks

Chunk boundaries are transport/storage boundaries only if the acquisition declaration says the chunks jointly belong to the same acquisition.

**Result:** chunking alone has no semantic domain effect.

### C-04 — Same observations re-acquired separately

Two independent acquisitions contain identical observations.

**Result:** they remain distinct acquisition domains. Acquisition-scoped identity does not create cross-acquisition identity continuity.

Content equality does not merge domains.

### C-05 — Same file processed twice

The same physical artifact is submitted in two independent acquisition operations.

**Result:** two acquisition domains, unless a higher-level contract explicitly identifies the second operation as a continuation/replay of the first acquisition rather than a new acquisition.

This document does not invent such a continuation mechanism.

### C-06 — Same acquisition processed by multiple workers

Parallel processing divides the physical input into worker subsets.

**Result:** worker partitions do not become acquisition domains. They are execution partitions inside the declared domain.

### C-07 — File order differs between implementations

Two conforming implementations receive the same declared acquisition membership but traverse its physical components in different orders.

**Result:** acquisition-domain membership is unchanged.

This decision establishes scope, not enumeration order.

### C-08 — Missing component from a declared multi-file acquisition

The acquisition declaration requires files A, B, and C; only A and B are present.

The domain is still the declared A+B+C acquisition scope, but qualification cannot silently pretend that C was never required.

The missing-component condition must be classified by the applicable acquisition/format binding and Q-RM-04 failure policy. If the missing component affects determinability of the qualified universe and no local treatment is normatively proven, qualification is blocked.

### C-09 — Duplicate physical delivery of the same component

The same artifact is delivered twice as part of one declared acquisition.

Physical duplication does not automatically mean two logical observations and does not automatically mean two domains.

The applicable binding must determine whether the repeated delivery is the same physical component, an independent occurrence, or an acquisition anomaly. No content-based deduplication is introduced here.

### C-10 — Cross-file record boundary

A format binding permits one logical record to span physical files/chunks.

If the acquisition declaration places those components in the same domain, the format binding must define the cross-unit boundary semantics.

If the required boundary cannot be determined, Q-RM-04 applies. The physical file boundary cannot be used as a silent logical record boundary.

### C-11 — Partition boundaries correlate with time

Partition 1 contains earlier timestamps and partition 2 later timestamps.

**Result:** this does not establish temporal precedence as part of Q-RM-05.

`ordered_ticks` remains the temporal authority.

### C-12 — Equivalent repartitioning

The same declared acquisition is physically represented once as one file and once as four partitions.

**Result:** partitioning alone must not change the acquisition-domain semantics.

Whether the resulting logical observations are equivalent still depends on the applicable format binding and record-model rules; Q-RM-05 does not invent cross-format identity continuity.

---

## 6. SECOND CASSAGE — FAILURE-SCOPE INTERACTION

Q-RM-04 established that failure scope depends on whether the affected logical universe remains determinable.

Q-RM-05 therefore adds the following constraint:

> Failure scope is evaluated against the **declared acquisition domain**, not against whichever physical file, worker partition, or chunk happened to expose the anomaly first.

Consequences:

```text
local anomaly in one file
≠ automatically acquisition-local

anomaly in one chunk
≠ automatically chunk-local

worker-local detection
≠ worker-local qualification scope
```

The scope is semantic and acquisition-level.

For example, if one chunk contains a corrupt framing header whose effect can alter interpretation of subsequent chunks in the same declared domain, Q-RM-04 cannot be bypassed by rejecting only the physical chunk.

Conversely, if a malformed record is constructively proven local under the binding, Q-RM-04 may permit `REJECT RECORD` without rejecting the whole declared domain.

---

## 7. THIRD CASSAGE — IDENTITY INTERACTION

The domain boundary is upstream of acquisition-scoped occurrence identity.

Therefore:

```text
same payload + different acquisition domain
→ no automatic identity continuity

same acquisition domain + strict duplicate occurrences
→ distinct occurrences remain distinct

same acquisition domain + multiple physical partitions
→ no identity multiplication merely from partition count
```

This avoids two opposite errors:

1. **over-merging:** treating independent acquisitions as one because content matches;
2. **over-splitting:** treating physical partitions of one acquisition as independent identities.

No physical identity primitive is selected by this rule.

---

## 8. DETERMINISM TEST — TWO CONFORMING IMPLEMENTATIONS

Given:

```text
same acquisition declaration
same physical component membership
same record-model version
same format-binding versions
same qualification contract
```

Implementation A may process:

```text
A → B → C
```

while implementation B processes:

```text
C → A → B
```

or uses parallel workers.

Both must nevertheless operate on the same declared acquisition domain.

Therefore domain membership cannot depend on:

- traversal order;
- thread scheduling;
- cache state;
- worker allocation;
- restart point;
- serialization order.

This is a direct prerequisite for qualification freeze, but does not itself define the freeze mechanism.

---

## 9. FAILURE / MISSING DECLARATION CASES

A crucial distinction is required:

### Domain declared and valid

Proceed with the declared acquisition domain.

### Domain declared but incompletely materialised

Do not silently redefine the domain to the subset that happens to be present. Apply the applicable missing-input/anomaly binding and Q-RM-04.

### Domain not declared

No implementation may infer one from physical adjacency, naming, timestamps, provider, directory, or runtime grouping.

The acquisition cannot be treated as normatively qualified until the domain is established by the applicable contract.

### Domain declaration itself ambiguous

The acquisition boundary is not uniquely determined.

This is a qualification-level ambiguity, not a parser preference.

The result is therefore `QUALIFICATION BLOCKED` unless another already-established normative contract uniquely resolves the declaration.

---

## 10. WHAT Q-RM-05 DOES NOT DECIDE

Q-RM-05 does **not** decide:

- canonical enumeration order;
- `CANONICAL_RECORD_POSITION`;
- physical row/offset/ordinal identity;
- temporal precedence;
- cross-acquisition identity;
- a universal file ordering;
- whether a particular provider's files form one acquisition;
- concrete CSV/JSON/binary framing;
- restart implementation;
- deduplication policy.

Those remain separate normative concerns.

---

## 11. CONCRETE BINDING OBLIGATION

The universal domain rule is closed, but every supported acquisition binding must still declare, in a versioned and auditable manner:

1. what constitutes an acquisition declaration;
2. which physical components belong to that declaration;
3. whether component membership is complete or optional;
4. whether any logical record may cross component boundaries;
5. how missing, duplicated, or extra components are classified;
6. which component-level anomalies are acquisition-fatal;
7. what evidence establishes that the declared domain is complete.

A binding that cannot answer these questions is not eligible for deterministic qualification.

This distinction is mandatory:

```text
UNIVERSAL ACQUISITION-DOMAIN POLICY = CLOSED
≠
ALL CONCRETE ACQUISITION BINDINGS = CLOSED
```

---

## 12. CLOSURE CRITERIA

Q-RM-05 is closed at the semantic policy level when the following invariant holds:

```text
same acquisition declaration
        ↓
same declared component membership
        ↓
same acquisition domain
```

independently of physical traversal, partitioning, worker allocation, serialization, or restart.

A conforming implementation must never create or destroy acquisition-domain boundaries as a side effect of runtime execution.

---

## 13. VERDICT

```text
Q-RM-05 UNIVERSAL ACQUISITION-DOMAIN RULE = PASS
Q-RM-05 CONCRETE ACQUISITION BINDINGS       = BLOCKED
```

The universal semantic rule is sufficiently determined and survives the adversarial cases.

The remaining binding obligation is not a reason to reopen Q-RM-01..04. It is carried forward to the format/acquisition binding closure work under Q-RM-06.

---

## 14. NEXT LOGICAL BLOCK

Proceed to **Q-RM-06 — Format Binding / Versioning**.

Q-RM-06 must now determine whether every supported physical representation has a sufficiently precise, versioned binding to make the already-closed universal rules executable, including:

```text
record boundaries
cardinality
non-observation material
failure classes
acquisition component membership
cross-component framing
binding/version compatibility
```

The key gate is no longer architectural invention. It is **binding completeness and determinism**.

Canonical enumeration remains untouched.

## FIN
