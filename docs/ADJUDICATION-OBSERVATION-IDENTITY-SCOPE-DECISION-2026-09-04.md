# ADJUDICATION — OBSERVATION IDENTITY SCOPE

**Date:** 4 September 2026

**Reference HEAD:** `79a5c648e902331e07c4ab999b733ea6cd9b52e4`

**Parent decision:** `OI-01` — normative ownership of individual observation identity

**Supporting analysis:** `ADJUDICATION-OBSERVATION-IDENTITY-POSITION-STABILITY-AUDIT-V1-2026-09-04.md` and independent Claude counter-expertise on canonical qualified-record sequencing.

**Status:** **DECISION EXPLICIT — SCOPE ADJUDICATED**

---

## 1. QUESTION

What is the required stability scope of the normative identity of an individual primary market observation?

The alternatives examined were:

```text
A — acquisition / qualified-artifact scope
B — instrument / inter-acquisition scope
```

The decision must not be confused with the semantic identity of a market event.

---

## 2. CORPUS AND AUDIT BASIS

The verified corpus establishes that:

- individual observation identity is owned upstream of `1.1.2` by `OI-01`;
- strict duplicate primary records retained by the qualified dataset must remain individually distinguishable;
- a generic runtime row number is not a stable identity primitive;
- a positional identity requires a defined normative domain and an assigned position within that domain;
- the current corpus does not establish a source guarantee sufficient to require identity stability across independent acquisitions;
- the current corpus does not establish an intrinsic content-only key capable of distinguishing strict duplicates.

The independent counter-expertise further established that, without an external guarantee, simultaneous requirements of strict-duplicate individuality and universal inter-acquisition stability cannot be satisfied by a generic positional sequence.

---

## 3. EXPLICIT DECISION — OI-02

### DECISION

> **The normative individual observation identity has acquisition-scoped stability. It is stable within the declared qualified dataset artifact/lignée to which the observation belongs, and no inter-acquisition identity equivalence is implied unless a separate normative decision explicitly establishes such equivalence.**

For the purpose of this decision, an acquisition-scoped identity denotes an individual retained primary record within its declared qualified dataset domain.

The decision therefore selects:

```text
Q-2 = ACQUISITION / QUALIFIED-DATASET SCOPE
```

and rejects the implicit requirement:

```text
Q-2 = UNIVERSAL / INSTRUMENT-WIDE INTER-ACQUISITION SCOPE
```

**Classification:**

```text
[DECISION EXPLICITE — ARCHITECTURAL SEMANTICS]
```

---

## 4. REQUIRED SEMANTIC CONSEQUENCES

The following are consequences of OI-02 and are not additional architecture choices:

### 4.1 Identity is domain-relative

An individual observation identity is meaningful only together with the normative qualified-dataset domain in which it is defined.

Conceptually:

```text
OBSERVATION IDENTITY
    = identity within declared qualified-dataset scope
```

A bare positional value such as:

```text
18427
```

is not a complete observation identity.

---

### 4.2 No automatic cross-acquisition equivalence

Two acquisitions may contain observations with identical visible market values without those observations receiving the same normative identity.

Therefore:

```text
same visible observation content
        ≠
identical normative observation identity
```

across independent acquisitions.

Cross-acquisition correspondence, if ever required, requires a separate explicit decision.

---

### 4.3 Derived artifacts remain inside the same lineage semantics

A transformation of a qualified dataset does not silently create a new identity for an already identified primary observation merely because the observation is represented in another structure.

Within the same declared lineage, the primary observation identity must remain referentially stable when propagated into derived representations.

---

### 4.4 Reordering does not alter identity

Once an observation has received its normative identity within the qualified dataset domain, reordering the runtime collection does not alter that identity.

In particular:

```text
runtime_index != normative_observation_identity
```

---

### 4.5 Position is not temporal order

The acquisition-scoped identity does not establish physical or temporal precedence.

In particular:

```text
position(A) < position(B)
```

does not imply:

```text
A temporally precedes B
```

unless an independent temporal-order rule establishes that relation.

This preserves the distinction required by the existing partial-order treatment of ambiguous temporal relationships.

---

### 4.6 Strict duplicates remain distinct when both are retained

If the qualified dataset retains two distinct primary records with identical visible values, they remain distinct observations and must receive distinct identities within that qualified dataset domain.

This decision does not claim that the records represent two distinct economic events.

Therefore:

```text
observation identity
        ≠
market-event identity
```

---

## 5. WHAT OI-02 DOES NOT DECIDE

OI-02 deliberately does **not** decide:

- the exact identity composition;
- whether the composition is positional, source-defined, composite or another mechanism;
- the exact canonical qualified-record enumeration rule;
- the exact encoding of the identity;
- the hash algorithm, if any;
- collision handling;
- provider-specific identity guarantees;
- late-tick policy;
- event identity;
- temporal ordering;
- serialization syntax for `ordered_ticks`.

In particular, OI-02 does not by itself authorize:

```text
(dataset_lineage, source_record_position)
```

as the final identity formula. It establishes the **scope semantics** within which a future identity composition may be adjudicated.

---

## 6. COMPATIBILITY CHECK

### H-04 / A-09

Compatible in principle because canonicalization may operate on a stable identity within a defined acquisition-scoped domain, while the resulting representation order remains purely representational.

The exact identity primitive remains separately unresolved.

### V7 strict-duplicate preservation

Compatible: two retained distinct records remain individually distinguishable within the same qualified dataset domain.

### V12 identity correspondence

Compatible in scope: correspondence between primary observations and derived representations is evaluated within the declared qualified dataset/lineage domain rather than across unrelated acquisitions.

The identity function itself remains undefined, so `V12-01` remains blocked.

### Causal / temporal constraints

Compatible: acquisition scope does not authorize using future information to define a past observation identity where the applicable point-in-time contract forbids such dependence.

---

## 7. STATUS OF THE POSITION QUESTION

After OI-02:

```text
POSITIONAL IDENTITY FAMILY
→ SCOPE RESOLVED

source_record_position
→ NOT YET FROZEN AS IDENTITY PRIMITIVE

CANONICAL QUALIFIED-RECORD SEQUENCE
→ STILL REQUIRES EXPLICIT DEFINITION

V12-01
→ STILL BLOCKED

1.1.2
→ NOT CLOSED
```

OI-02 removes one ambiguity identified by the position-stability audit: the identity is **not required to be stable across independent acquisitions** unless a later decision explicitly says otherwise.

It does not remove the remaining requirement that the sequence/position itself be deterministically defined within the selected acquisition scope.

---

## 8. PIPELINE STATE

```text
QUESTION
   ↓
CORPUS AUDIT                         ✓
   ↓
COUNTER-EXPERTISE                    ✓
   ↓
Q-2 SCOPE ADJUDICATION               ✓ OI-02
   ↓
Q-1 EXACT COMPOSITION                 ← NEXT
   ↓
Q-3 DUPLICATE SEMANTICS               ← DEPENDENT
   ↓
Q-4 / Q-5 / Q-6 / Q-7                ← DEPENDENT
   ↓
UPSTREAM IDENTITY CONTRACT            ← REQUIRED
   ↓
1.1.2 MINIMAL CORRECTION              ← LATER
   ↓
NEW ADVERSARIAL AUDIT                 ← LATER
```

---

## 9. NON-DÉRIVE GUARD

This decision:

- does not modify V8 or any `1.1.2` contract;
- does not create V9/V10/V11/V12/V13/V14;
- does not define a source-record ordering rule;
- does not turn position into temporal order;
- does not infer a provider guarantee;
- does not define event identity;
- does not define late-tick behavior;
- does not close `V12-01`;
- does not authorize an implementation.

Any future rule requiring inter-acquisition correspondence must be introduced through a separate explicit decision.

---

## FIN — OI-02
