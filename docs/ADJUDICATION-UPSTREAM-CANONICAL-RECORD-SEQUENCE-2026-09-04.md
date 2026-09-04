# ADJUDICATION REQUIRED — UPSTREAM CANONICAL RECORD SEQUENCE

**Date:** 4 September 2026  
**Parent blocker:** `V12-01` / positional observation identity  
**Preceding audit:** `ADJUDICATION-OBSERVATION-IDENTITY-CANONICAL-SEQUENCE-AUDIT-V1-2026-09-04.md`  
**Status:** **ADJUDICATION REQUIRED — NO DECISION TAKEN**

---

# 1. DECISION QUESTION

The adversarial audit established that no currently authoritative rule defines a canonical enumeration of qualified primary records.

The question to adjudicate is therefore:

> **Can the upstream qualification contract define a canonical enumeration of qualified primary records, and if yes, what exact rule determines that enumeration without creating temporal order?**

This is **not** a decision between “position” and “no position”.

It is a decision about whether a deterministic record-enumeration rule can exist upstream and become an immutable attribute consumed by `1.1.2`.

---

# 2. CONSTRAINTS ALREADY ESTABLISHED

The adjudication must preserve:

1. Observation identity is distinct from market-event identity.
2. Canonical position is distinct from temporal order.
3. `ordered_ticks` remains the unique normative authority for established temporal relations.
4. No artificial total temporal order may be created merely to obtain unique identifiers.
5. Distinct primary observations retained by the qualified dataset must remain individually distinguishable, even when visible values are identical.
6. Runtime collection order cannot become normative identity.
7. `1.1.2` consumes and propagates observation identity; it does not silently invent the upstream identity mechanism.
8. No identity encoding, hash algorithm, collision policy, or implementation-specific identifier is pre-authorized by this document.

---

# 3. OPTION A — SOURCE-PROVIDED CANONICAL SEQUENCE

The provider supplies a sequence or stable record identifier that is contractually guaranteed to be:

- stable;
- unique within the required scope;
- preserved by qualification;
- deterministic across conforming acquisitions/reads where equivalence is required;
- semantically defined;
- compatible with duplicate and equal-timestamp cases.

**Decision implication:** If all guarantees are evidenced in the authoritative source/data contract, the upstream contract may consume that sequence as the identity primitive.

**Current evidence:** not established.

**Status:** AVAILABLE FOR ADJUDICATION, NOT PROVEN.

---

# 4. OPTION B — QUALIFICATION-ASSIGNED CANONICAL SEQUENCE

The qualification layer constructs an immutable qualified dataset and assigns each retained primary record a deterministic position according to an explicitly defined enumeration rule.

Minimum required rule components:

```text
scope
membership
enumeration
assignment stage
stability
duplicate treatment
multi-file/source combination
version semantics
cross-acquisition semantics
```

The assigned position is an identity coordinate only:

```text
position(A) < position(B)
```

does **not** imply:

```text
A temporally precedes B
```

unless an independent temporal-order relation establishes it.

**Current evidence:** architecture-compatible, but the actual enumeration rule is not defined by the corpus.

**Status:** AVAILABLE FOR ADJUDICATION, NOT YET NORMATIVE.

---

# 5. OPTION C — IMMUTABLE ARTIFACT ENUMERATION

The exact captured qualified artifact is normative, and its immutable record enumeration is the canonical coordinate system.

This may use a physical record locator internally, but only if the exact artifact, record boundaries, scope, and stability semantics are explicitly normative.

It does not automatically imply identity across distinct acquisitions or revised artifacts.

**Current evidence:** not established as a normative regime.

**Status:** AVAILABLE FOR ADJUDICATION, NOT PROVEN.

---

# 6. REJECTED AS SUFFICIENT GENERIC RULES

The following must not be selected as standalone canonical enumeration rules:

### 6.1 Runtime collection index

Not stable under traversal or in-memory reordering.

### 6.2 Generic physical row/file order

Not a semantic record attribute unless the exact immutable artifact and enumeration are made normative.

### 6.3 Content-only sort

Cannot distinguish strict duplicate records without an additional tie-break that introduces another unresolved identity mechanism.

### 6.4 Timestamp-only sort

Cannot resolve equal timestamps without inventing temporal precedence.

These are audit conclusions, not new architecture decisions.

---

# 7. REQUIRED ADJUDICATION QUESTIONS

The adjudication must answer explicitly:

### Q-S1 — Ownership

Which upstream normative boundary owns the canonical record-enumeration rule?

### Q-S2 — Scope

Is the canonical sequence scoped to:

- one qualified dataset version;
- one dataset lineage;
- one source stream;
- another explicitly defined domain?

### Q-S3 — Membership

At what exact point are records admitted to the sequence?

Before or after qualification filters, corrections, exclusions, or other admissibility decisions?

### Q-S4 — Enumeration

What deterministic rule assigns exactly one canonical coordinate to every retained primary record without relying on runtime traversal order?

### Q-S5 — Duplicate records

How are distinct retained records with identical visible values enumerated without collapsing them?

### Q-S6 — Equal timestamps

How is enumeration performed when temporal order is unresolved, without creating a false temporal relation?

### Q-S7 — Multi-file / multi-source combination

How are records combined into one qualified sequence when acquisition produces multiple files or source partitions?

### Q-S8 — Version change

What constitutes the same qualified dataset versus a new qualified dataset version, and what identity continuity is required across versions?

### Q-S9 — Re-acquisition

Must two acquisitions representing the same declared qualified dataset produce the same observation identities, or is identity acquisition-scoped?

### Q-S10 — Assignment stability

Once assigned, is the canonical coordinate immutable across:

```text
qualification
→ 1.1.2
→ BAR_IN_PROGRESS
→ BAR_CLOSED
→ derived representations
```

### Q-S11 — Temporal independence

What explicit rule guarantees that canonical enumeration does not become an artificial temporal ordering?

---

# 8. ACCEPTANCE CRITERIA FOR A FUTURE DECISION

A selected canonical sequence rule is acceptable only if the resulting contract makes all of the following mechanically decidable:

```text
same qualified dataset
        → same record membership
        → same canonical enumeration
        → same assigned identity
```

and simultaneously:

```text
canonical position
        ≠
        temporal order
```

The rule must survive at minimum:

- traversal permutation;
- runtime reorder;
- strict duplicate records;
- equal timestamps;
- multi-file partitioning;
- qualification filtering boundary;
- dataset-version change;
- re-acquisition semantics;
- BAR_IN_PROGRESS → BAR_CLOSED propagation.

If any of these remain unspecified, the identity freeze remains blocked.

---

# 9. CLASSIFICATION RULE

The following distinctions are mandatory during adjudication:

```text
[NORMATIF — MASTER PLAN / DECISION GELÉE]
[CONSÉQUENCE NÉCESSAIRE]
[ARCHITECTURE PROPOSÉE]
[QUESTION NON RÉSOLUE]
[ABSENCE DE PREUVE]
```

A technically attractive mechanism must not be promoted to `[NORMATIF]` merely because it is convenient to implement.

---

# 10. CURRENT STATE

```text
CANONICAL RECORD SEQUENCE → NOT ESTABLISHED
POSITIONAL IDENTITY → BLOCKED
V12-01 → BLOCKED
1.1.2 → NOT CLOSED
```

No implementation change is authorized by this document.

No identity format is selected.

No source-order rule is selected.

No cross-acquisition rule is selected.

No new Master Plan requirement is created.

## FIN
