# NORMATIVE LOGICAL RECORD MODEL — DEFINITION & ADVERSARIAL AUDIT

**Date:** 5 September 2026
**Reference commit:** `d08ca301e7bcc0b906efa393dd6a6014a0bbc824`
**Scope:** upstream qualification contract — logical primary record model only
**Status:** **BLOCKED FOR FREEZE — CANDIDATE MODEL DEFINED, CRITICAL SEMANTICS STILL TO BE ADJUDICATED**

---

## 1. OBJECTIVE

Define the smallest normative logical model required before any canonical record-enumeration rule can be selected.

This block does **not** define:

- the canonical enumeration criterion;
- `CANONICAL_RECORD_POSITION` generation;
- a hash algorithm;
- a byte offset;
- a physical row number;
- a provider identifier;
- a global multi-file ordinal;
- temporal precedence;
- a new `1.1.2` rule.

The purpose is to make the universe of objects to be enumerated unambiguous.

---

## 2. VERIFIED CORPUS BASIS

`00-CORPUS-INDEX.md` identifies `05-DATA-CONTRACT.md` as a proposed data contract, not a frozen normative contract. `08-SYSTEM-REGISTRY.md` likewise records `05`, `09` and related details as provisional/non-normative. Therefore those documents can provide evidence of prior architectural thinking but cannot silently supply the missing frozen record model.

`OI-01` explicitly assigns ownership of individual primary-observation identity to the upstream qualification/data-contract responsibility boundary and states that identity composition remains unresolved. `1.1.2 V7 §4.1` consequently consumes an upstream identity rather than defining a local competing identity.

The canonical-enumeration audits establish that a deterministic position cannot exist until the logical record universe is itself determinable. They also establish that record-boundary treatment is a necessary dependency, but not automatically a separate architecture decision.

---

## 3. NORMATIVE LOGICAL RECORD MODEL — CANDIDATE DEFINITION

### 3.1 Logical primary record occurrence

A **logical primary record occurrence** is one individually retained occurrence in the qualified primary observation universe, obtained by applying the versioned record-model rules to the declared acquisition input.

For the tick-oriented primary dataset consumed by `1.1.2`, one retained logical primary record occurrence corresponds to exactly one primary market observation.

This correspondence is semantic, not a statement about physical file layout.

### 3.2 Occurrence individuality

Record individuality is occurrence-based, not content-based.

Therefore:

```text
R1.payload = R2.payload
```

does not imply:

```text
R1 = R2
```

when qualification has retained both occurrences as distinct primary records.

Strict duplicate records must therefore remain distinct logical occurrences.

This does not assert that they are distinct market events.

```text
observation identity ≠ market-event identity
```

### 3.3 Record boundary

The record model must define exactly what constitutes one logical record occurrence and where that occurrence begins and ends in the declared acquisition representation.

The boundary definition must be deterministic for the declared input representation and version of the record model.

A parser may not silently choose among multiple plausible interpretations.

If the declared representation cannot be parsed unambiguously under the applicable record model, the ambiguity must remain an explicit qualification failure/unknown state rather than being resolved by implementation preference.

### 3.4 Logical content

Each logical record occurrence has a logical payload resulting from the declared record-model interpretation.

The logical payload may contain the fields required to construct the primary observation, including the market timestamp and market values where applicable.

The logical payload is not itself the identity.

Equal logical payloads may belong to distinct retained occurrences.

### 3.5 Source representation

The model must preserve sufficient provenance to relate each logical record occurrence to the declared acquisition input from which it was obtained.

The exact physical provenance primitive is intentionally **not selected** here.

No conclusion is made here that provenance must be a byte offset, row number, file path, hash, provider ID, or other concrete locator.

### 3.6 Qualification membership

The logical-record model is evaluated before canonical enumeration.

The qualification contract must determine whether a parsed logical record occurrence belongs to the retained qualified primary universe.

Only retained occurrences enter the later canonical enumeration domain.

A rejected or excluded record must not receive a normative canonical observation position merely because it existed physically in the acquisition input.

### 3.7 No temporal meaning

The logical-record model does not establish temporal precedence between record occurrences.

Neither record boundary, source representation, occurrence identity, nor any later canonical position may be interpreted as:

```text
A precedes B
```

unless an independent normative temporal-order rule establishes that relation.

`ordered_ticks` remains the authority for established temporal relations.

### 3.8 Versioning

The record model is itself a versioned normative contract property.

A conforming implementation must be able to identify which record-model version was applied when producing the qualified primary dataset.

Changing the record model in a way that can change record membership, boundaries, logical payload interpretation, or occurrence individuation constitutes a materially different model version and cannot be treated as an invisible implementation update.

### 3.9 Qualification freeze point

The record model must become immutable for a qualified dataset at a defined qualification point.

After that point, downstream traversal, caching, parallel scheduling, restart, serialization choice, or collection reordering must not change which logical record occurrences exist in the qualified universe.

---

## 4. FORMAT-NEUTRALITY RULE

The normative logical model should remain semantic rather than silently selecting one physical storage representation.

A format-specific binding may define how a CSV, JSON, binary stream, vendor export, compressed object, or other representation is parsed into logical record occurrences.

However, the binding itself must be declared and versioned wherever its rules can affect:

- record boundaries;
- field interpretation;
- occurrence count;
- occurrence individuation;
- qualification membership.

The global logical model must not assume that a physical line, row, byte range, packet, or provider object is universally equivalent to one logical record.

**Classification:** `[ARCHITECTURE PROPOSÉE]` pending explicit upstream contract integration.

---

## 5. ADVERSARIAL TEST MATRIX

### RM-01 — Same input, different parser implementation

Two conforming implementations process the same declared acquisition representation using the same record-model version.

**Expected:** same logical record boundaries, same occurrence count, same retained membership.

### RM-02 — Runtime traversal permutation

The already-qualified logical records are delivered downstream in a different traversal order.

**Expected:** the logical record universe is unchanged.

### RM-03 — Strict duplicates

Two physically/logically distinct retained occurrences have identical visible payloads.

**Expected:** two distinct logical record occurrences; no content-based collapse.

### RM-04 — Equal timestamp

Two retained records share the same market timestamp.

**Expected:** they remain distinct occurrences if both are retained; the model establishes no temporal precedence.

### RM-05 — Boundary ambiguity

The same physical input admits two plausible record interpretations.

**Expected:** no implementation-specific choice; qualification cannot produce a normative qualified universe until the applicable model resolves the ambiguity.

### RM-06 — Header / metadata / non-observation material

The acquisition representation contains material that is not a primary observation.

**Expected:** the model deterministically classifies whether it is record content, metadata, or non-record material; it cannot silently enter the primary observation universe.

### RM-07 — Malformed record

A candidate record violates the declared record model.

**Expected:** deterministic qualification outcome; no silent repair or reinterpretation.

### RM-08 — Record containing multiple observations

One physical source object can encode more than one observation.

**Expected:** the model explicitly defines whether the physical object is split into multiple logical primary record occurrences. The tick-level primary universe must still be unambiguous.

### RM-09 — Qualification filtering

A physically present record is excluded by qualification.

**Expected:** it does not enter the retained logical-record universe and does not receive a later canonical position.

### RM-10 — Multi-file / partitioned acquisition

Equivalent acquisition content is physically partitioned across multiple files/objects.

**Expected:** the model explicitly identifies the acquisition domain and membership relation. It does not silently infer a global enumeration order.

### RM-11 — Re-acquisition

A second acquisition is produced independently.

**Expected:** no cross-acquisition identity continuity is inferred; behavior follows the already selected acquisition-scoped identity semantics.

### RM-12 — Format conversion

The same intended observations are converted into another physical representation.

**Expected:** no automatic identity continuity is inferred unless a future applicable contract explicitly requires it.

### RM-13 — Qualification restart

Qualification is interrupted and resumed.

**Expected:** same declared input + same record-model version + same qualification semantics produce the same logical record universe.

### RM-14 — Future data extension

Later observations are appended to the acquisition.

**Expected:** the prior qualified dataset is not silently rewritten. Any changed qualified dataset state must be distinguishable according to the applicable dataset/version contract.

---

## 6. CRITICAL FINDINGS

### RM-F01 — Record boundary is not optional

**Finding:** the enumeration problem cannot be made deterministic until the logical record universe is deterministic.

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

This does not decide the physical mechanism used to implement boundaries.

### RM-F02 — Content is not occurrence identity

**Finding:** strict duplicate retention prevents a pure content-only identity model from distinguishing all retained occurrences.

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

### RM-F03 — Physical representation is not automatically semantic

A physical row, line, byte range, packet, or source object can be used only if the applicable upstream contract explicitly makes it the relevant record representation.

**Classification:** `[ARCHITECTURE PROPOSÉE]` as a design constraint; no concrete primitive selected.

### RM-F04 — Record model and enumeration are distinct

The record model answers:

```text
WHAT IS ONE RETAINED OCCURRENCE?
```

Enumeration answers:

```text
HOW ARE THOSE OCCURRENCES ASSIGNED CANONICAL POSITIONS?
```

They must not be collapsed into one undefined phrase such as “canonical order”.

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

### RM-F05 — Record model and temporal order are distinct

The record model may define occurrence membership without establishing temporal precedence.

**Classification:** `[NORMATIF — CONSÉQUENCE DES CONTRAINTES GELÉES]`

### RM-F06 — Record model version is part of reproducibility

If changing the record interpretation can change the qualified observation universe, the model version is a determinant of the resulting dataset and must be identifiable.

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

### RM-F07 — Physical source order remains unselected

The model does not yet say that physical appearance order is normative.

Therefore the following remain open:

```text
physical row
byte offset
source ordinal
provider sequence
logical artifact order
composite non-temporal criterion
```

**Classification:** `[QUESTION NON RÉSOLUE]`

---

## 7. WHAT IS NOW DEFINED SUFFICIENTLY

The following semantic properties can be stated without selecting the enumeration mechanism:

```text
1. A logical record is an individual retained primary-observation occurrence.
2. Record individuality is occurrence-based, not content-based.
3. Strict retained duplicates remain distinct occurrences.
4. The logical record model is upstream of canonical enumeration.
5. Record membership is determined by qualification.
6. Record boundaries must be deterministic under the applicable versioned model.
7. Logical payload is distinct from identity.
8. Physical provenance is retained but its primitive is not selected here.
9. Record-model version is identifiable.
10. Qualification freezes the resulting logical record universe.
11. Record identity/boundaries do not establish temporal precedence.
12. `ordered_ticks` remains the temporal authority.
```

---

## 8. WHAT REMAINS BLOCKING

### BLOCKER B1 — Exact record boundary semantics

The corpus does not yet contain a frozen universal rule that determines the boundary of a logical record for every supported acquisition representation.

This is not necessarily a new architecture choice. It is a missing normative specification to be supplied by the upstream qualification contract and/or its format-specific binding.

### BLOCKER B2 — Physical-to-logical mapping

The model still needs a precise contract for how the declared acquisition representation is mapped into logical record occurrences.

This includes the case where one physical object may contain zero, one, or multiple primary observations.

### BLOCKER B3 — Multi-file acquisition-domain semantics

The existing corpus does not prove whether a multi-file acquisition is one logical acquisition domain or multiple domains for record-model purposes.

No global ordinal is inferred.

### BLOCKER B4 — Malformed / ambiguous record policy

The semantic requirement for deterministic treatment is established, but the exact admissibility outcome and transformation boundary remain to be specified by the upstream qualification contract.

### BLOCKER B5 — Format binding/version matrix

The corpus identifies a future format/schema contract but does not currently freeze the exact format-specific bindings.

---

## 9. NON-BLOCKING / NOT REQUIRED NOW

The following do **not** need to be decided in this record-model block:

- canonical enumeration criterion;
- canonical position encoding;
- hash algorithm;
- cross-acquisition identity;
- temporal order reconstruction;
- `ordered_ticks` structure;
- execution simulation;
- BAR_CLOSED provenance storage location.

These are separate concerns.

---

## 10. CLOSURE CRITERIA FOR THE RECORD MODEL

The `NORMATIVE LOGICAL RECORD MODEL` may be frozen only when the upstream qualification contract makes it possible for two conforming implementations to determine identically:

```text
same declared acquisition input
        ↓
same record-model version
        ↓
same logical record boundaries
        ↓
same logical record occurrences
        ↓
same retained qualification membership
```

and when the following invariants are mechanically testable:

1. no retained occurrence is silently duplicated or lost;
2. strict duplicate occurrences remain distinct;
3. malformed/ambiguous input cannot produce implementation-dependent membership;
4. record interpretation is independent of runtime traversal;
5. record interpretation is independent of downstream serialization;
6. record-model version is identifiable;
7. record occurrence semantics do not establish temporal precedence;
8. the model remains compatible with acquisition-scoped observation identity.

Only after this gate is passed may the canonical enumeration function be defined and audited.

---

## 11. CURRENT STATUS

```text
ARCHITECTURE FAMILY                         = RESOLVED
IDENTITY OWNERSHIP                          = RESOLVED UPSTREAM
IDENTITY SCOPE                              = ACQUISITION-SCOPED
NORMATIVE LOGICAL RECORD MODEL              = CANDIDATE DEFINED
RECORD MODEL FREEZE                         = BLOCKED
CANONICAL ENUMERATION                       = NOT YET TOUCHED
CANONICAL_RECORD_POSITION                   = NOT DEFINED
V12-01                                      = BLOCKED
1.1.2                                       = NOT CLOSED
```

No `1.1.2` amendment is authorized.

No enumeration rule is selected by this document.

No physical identity primitive is selected by this document.

## FIN
