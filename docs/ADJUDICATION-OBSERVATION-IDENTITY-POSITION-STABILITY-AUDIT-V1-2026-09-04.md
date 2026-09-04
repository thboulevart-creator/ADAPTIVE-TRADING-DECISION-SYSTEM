# AUDIT — OBSERVATION IDENTITY — SOURCE RECORD POSITION STABILITY

**Date:** 4 September 2026

**Reference HEAD:** `3c4509d233f3b248a2d36de9ade1be8bb8505faf`

**Scope:** determine whether `source_record_position` can be used as a normative primitive for individual observation identity before any Q1/Q2 identity decision is frozen.

**Status:** AUDIT RESULT — BLOCKED FOR FREEZING

---

# 1. QUESTION

Can a `source_record_position` be a normative primitive for individual observation identity while satisfying the already established requirements of:

```text
stability
individuality
reproducibility
comparability
independence from derived representations
```

without silently creating a new assumption about source ordering or dataset semantics?

---

# 2. VERIFIED CORPUS STATE

The current repository HEAD is:

```text
3c4509d233f3b248a2d36de9ade1be8bb8505faf
```

`OI-01` explicitly assigns ownership of normative individual observation identity to the upstream qualification/data-contract responsibility boundary and does not itself define the identity composition, scope, encoding, serialization or collision policy.

The Q1→Q3 preliminary resolution establishes preservation of individuality for distinct observations retained by the qualified dataset, while exact identity composition and scope remain unresolved.

`1.1.2 V12` already requires deterministic results and prohibits dependence on implicit read order. `V7 §4.1` refers to an applicable upstream identity contract but the current corpus does not establish a normative source-record-position rule.

A-11 remains relevant because the corpus does not currently establish the complete upstream regime for observation order or source combination.

---

# 3. FINDING P-01 — POSITION IS NOT INHERENTLY STABLE

A position is stable only relative to a precisely defined and immutable ordered domain.

A generic statement such as:

```text
source_record_position = row number
```

is insufficient.

The position changes under operations such as:

- insertion of a preceding record;
- removal of a preceding record;
- concatenation of source files;
- filtering before qualification;
- source re-export with a different record order;
- provider-side reserialization;
- different file traversal order;
- reconstruction from equivalent source content using a different physical layout.

Therefore:

```text
position alone ≠ stable identity
```

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

This follows from the definition of a relative position and from the existing prohibition on implicit read order.

---

# 4. FINDING P-02 — POSITION CAN BECOME STABLE AFTER QUALIFICATION, BUT ONLY UNDER AN UNRESOLVED UPSTREAM CONTRACT

A positional identity could be made stable if the upstream contract first defines a canonical, deterministic sequence of qualified primary records and assigns the position exactly once within that immutable qualified dataset.

Conceptually:

```text
RAW SOURCE
   ↓
QUALIFICATION
   ↓
CANONICAL QUALIFIED RECORD SEQUENCE
   ↓
POSITION ASSIGNED ONCE
   ↓
OBSERVATION IDENTITY
```

Under this model, later reordering of collections does not change identity because the position is already an attribute of the qualified record rather than a runtime collection index.

However, the current authoritative corpus does not establish:

- the canonical source-record sequence;
- the rule by which that sequence is determined;
- whether the sequence is source-defined or qualification-defined;
- how multiple source files are combined;
- how ties in timestamp/order are handled without inventing physical order;
- whether the position is assigned before or after filtering/qualification transformations;
- whether the same logical dataset reacquired from the source must reproduce the same positions.

**Classification:** `[ABSENCE DE PREUVE]`

This is the decisive blocker.

---

# 5. FINDING P-03 — POSITION MUST NOT BE CONFUSED WITH TEMPORAL ORDER

A position used for identity must not itself become evidence of temporal precedence.

In particular:

```text
position(O17) < position(O18)
```

must not imply:

```text
O17 < O18
```

unless the applicable normative order rule independently establishes that relation.

This is especially important for equal timestamps or otherwise unresolved ordering.

The identity coordinate may distinguish records without establishing an order relation between them.

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

---

# 6. FINDING P-04 — DUPLICATE RECORDS ARE NOT A POSITIONAL COLLISION

If the qualified dataset retains two distinct primary records with identical visible values:

```text
O17 = (T, BID, ASK)
O18 = (T, BID, ASK)
```

then a positional scheme can distinguish them structurally, provided the qualification layer has already established that they are two distinct retained records.

This does not establish that they represent two distinct market events.

Therefore the following distinction must remain explicit:

```text
observation identity
        ≠
market-event identity
```

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

The semantic question of whether source duplicates represent one or multiple market events remains upstream and is not solved by positional identity.

---

# 7. FINDING P-05 — DATASET SCOPE IS STILL REQUIRED

A position without its normative domain is not an identity.

For example:

```text
position = 18427
```

does not identify anything without knowing the dataset/qualified sequence to which that position belongs.

Therefore any positional mechanism requires an explicitly defined identity scope.

Conceptually:

```text
QUALIFIED_DATASET_SCOPE + STABLE_POSITION
```

The exact scope remains unresolved by the current Q1/Q2 adjudication.

**Classification:** `[QUESTION NON RÉSOLUE]`

---

# 8. FINDING P-06 — RE-ACQUISITION STABILITY IS NOT AUTOMATIC

Two acquisitions can contain identical visible market records while having different physical record positions because of source packaging, ordering or filtering differences.

Conversely, two datasets can have the same positions while containing different records.

Therefore:

```text
same position ≠ same observation
```

and:

```text
same visible content + different position
```

does not by itself establish whether the observations denote the same market event.

If cross-acquisition comparability is required, the upstream contract must define the exact dataset identity/scope and the conditions under which record correspondence is preserved.

**Classification:** `[QUESTION NON RÉSOLUE]`

No cross-acquisition identity guarantee is inferred here.

---

# 9. TESTS REQUIRED BEFORE POSITION CAN BE FROZEN

The following tests are required to establish whether a positional primitive is actually stable under the intended upstream contract:

### P-TEST-1 — Same qualified dataset, different traversal

Read the same qualified dataset through different physical/file traversal orders.

**Expected:** assigned observation identities remain identical.

### P-TEST-2 — Runtime collection reorder

Reorder the in-memory collection after qualification.

**Expected:** observation identities remain identical.

### P-TEST-3 — Duplicate retained records

Use two distinct retained records with identical visible content.

**Expected:** identities remain distinct.

### P-TEST-4 — Preceding insertion

Insert a record before an existing record in a mutable pre-qualification representation.

**Expected:** this test is meaningful only after the contract defines whether the dataset itself has changed. It must not silently be interpreted as an identity-preservation requirement across different dataset versions.

### P-TEST-5 — Re-acquisition

Acquire the same declared dataset again.

**Expected:** only if the normative dataset identity/scope explicitly requires cross-acquisition correspondence, the same observations must receive the same identities.

### P-TEST-6 — Multi-file combination

Present equivalent records through different file partitioning/concatenation arrangements.

**Expected:** no identity change if and only if the qualified dataset contract defines those arrangements as the same normative dataset/lineage.

### P-TEST-7 — Equal timestamp

Provide multiple records with identical timestamps.

**Expected:** identities distinguish retained records without turning positional identity into temporal order.

---

# 10. RESULT

The audit does **not** reject positional identity as an architecture family.

It establishes a stricter result:

> `source_record_position` can be a normative identity component only if it is an immutable attribute assigned within a normatively defined qualified record sequence whose scope and stability rules are themselves explicit.

The current corpus does not yet establish that sequence or those stability rules.

Therefore:

```text
POSITIONAL IDENTITY FAMILY
→ ARCHITECTURALLY PLAUSIBLE

source_record_position AS NORMATIVE PRIMITIVE
→ NOT YET PROVEN

FREEZE OF OPTION B
→ BLOCKED
```

---

# 11. NO NEW ARCHITECTURE CREATED

This audit does not decide:

- the exact identity formula;
- the exact dataset scope;
- cross-acquisition equivalence;
- duplicate-event semantics;
- canonical serialization format;
- hash algorithm;
- collision-resolution mechanism;
- source ordering policy;
- late-tick policy;
- `event_time` / `availability_time` semantics.

No modification of `1.1.2` is authorized.

---

# 12. PIPELINE STATE

```text
Q1/Q2 identity semantics
        ↓
POSITION STABILITY AUDIT       ✓ COMPLETED
        ↓
POSITION AS NORMATIVE PRIMITIVE
        ↓
UPSTREAM SEQUENCE CONTRACT     ✗ NOT ESTABLISHED
        ↓
EXPLICIT IDENTITY DECISION     ✗
        ↓
1.1.2 CORRECTION               ✗
        ↓
NEW ADVERSARIAL AUDIT          ✗
```

**Global status:**

```text
V12-01          = BLOCKED
1.1.2           = NOT CLOSED
POSITION FREEZE = NOT AUTHORIZED
```

## FIN
