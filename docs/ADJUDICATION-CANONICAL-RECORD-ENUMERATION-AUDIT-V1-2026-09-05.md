# ADVERSARIAL AUDIT — CANONICAL RECORD ENUMERATION

**Date:** 5 September 2026  
**Parent decision:** Q1 positional identity family selected  
**Status:** **BLOCKED — NO ENUMERATION RULE SELECTED**

---

# 1. AUDIT OBJECTIVE

Determine what the upstream qualification contract must specify in order to assign a deterministic `CANONICAL_RECORD_POSITION` to every retained primary observation, without introducing an artificial temporal order and without silently deciding unrelated architecture questions.

The selected identity family is:

```text
OBSERVATION_IDENTITY
=
QUALIFIED_DATASET_DOMAIN
+
CANONICAL_RECORD_POSITION
```

Only the second component is under examination here.

---

# 2. FROZEN CONSTRAINTS

The audit must preserve:

1. `ordered_ticks` is the unique normative authority for established temporal relations.
2. Canonical position is an identity coordinate, not temporal precedence.
3. Strict duplicate observations retained by qualification remain individually distinguishable.
4. Runtime traversal or in-memory collection order is not normative.
5. Identity is acquisition/qualified-dataset scoped; it is not market-event identity.
6. No hash algorithm, source identifier, byte offset, physical row number, serialization, or global multi-file order is preselected.
7. `1.1.2` does not own the upstream identity-generation rule.

---

# 3. CENTRAL QUESTION

> **What exact normative rule can enumerate every retained primary record exactly once and deterministically within the already-defined qualified dataset domain, such that two conforming implementations assign the same canonical position to the same retained record, while the position itself establishes no temporal relation?**

This question does not assume that the answer must be physical row order, byte offset, source order, content sorting, or a single global ordinal.

---

# 4. CANDIDATE FAMILIES TO ATTACK

## E1 — Physical artifact enumeration

Potential mechanism: enumerate records according to a normative immutable acquisition artifact.

Audit questions:
- Is the artifact itself normatively identified?
- Are record boundaries normatively defined?
- Is the enumeration deterministic?
- Does physical storage order carry any unintended temporal meaning?
- Does the mechanism survive strict duplicates?

Status before adjudication: **ARCHITECTURE PROPOSAL**.

## E2 — Qualification-created enumeration

Potential mechanism: qualification constructs the retained record set and assigns positions according to a deterministic rule.

Audit question:
- Does “assigned at qualification” define an enumeration rule, or merely the point at which a rule becomes immutable?

Status: **ARCHITECTURE PROPOSAL / INCOMPLETE**.

## E3 — Source-provided sequence or identifier

Potential mechanism: use provider sequence/ID.

Audit question:
- Is contractual stability, uniqueness, preservation, and duplicate semantics actually proven?

Status: **ABSENCE DE PREUVE** under current corpus unless upstream evidence changes.

## E4 — Content-derived ordering

Potential mechanisms include lexical sorting, hashes, timestamp sorting, or other value-derived ordering.

Audit questions:
- Can strict duplicates receive distinct positions?
- Does timestamp sorting invent temporal precedence where `ordered_ticks` remains unresolved?

Generic standalone forms are already strongly constrained/rejected by prior audits, but this audit must verify rather than assume.

## E5 — Multi-domain enumeration

Potential mechanism: maintain independent canonical enumeration domains rather than forcing one global sequence across all files/source partitions.

Audit question:
- Is a single global sequence actually required by the selected identity family?

Status: **QUESTION NON RÉSOLUE**.

---

# 5. ADVERSARIAL CASE MATRIX

The selected rule must be challenged against at least:

### C1 — Runtime traversal permutation

Same qualified dataset, records delivered to the implementation in a different traversal order.

Expected property: canonical positions unchanged.

### C2 — Strict duplicate records

Two distinct retained primary records have identical visible values.

Expected property: both receive distinct identity coordinates without asserting they are distinct market events.

### C3 — Equal timestamps

Multiple retained observations share the same timestamp and their temporal relation is unresolved.

Expected property: position assignment does not establish temporal precedence.

### C4 — Qualification filtering

Records are removed before admission to the qualified dataset.

Expected property: the enumeration domain is unambiguously defined relative to the retained qualified dataset.

### C5 — Multiple files / partitions

One acquisition is physically partitioned across multiple files or source partitions.

Expected property: behavior is deterministic, but no global sequence may be invented unless required and explicitly selected.

### C6 — Re-acquisition

Two independent acquisitions contain equivalent-looking data.

Expected property: behavior follows acquisition-scoped identity; no cross-acquisition identity requirement may be invented.

### C7 — Artifact copy

The same acquisition artifact is copied without changing its content.

Expected property: no conclusion about identity equality may be inferred unless the corpus explicitly requires it.

### C8 — Format conversion

An artifact is transformed into another representation without changing the intended logical records.

Expected property: no identity-continuity requirement may be invented unless explicitly required.

### C9 — Record-boundary ambiguity

A parser or format can admit multiple plausible record boundaries.

Expected property: enumeration cannot be deterministic until the normative record model resolves membership/boundaries; however, this must not be confused with a new architecture decision unless the corpus requires one.

### C10 — Insertion / modified acquisition

A changed acquisition contains an inserted, removed, or modified record.

Expected property: behavior follows the defined qualified-dataset domain; no cross-lineage stability requirement may be invented.

### C11 — Physical reorder without content change

Same records are physically rearranged.

Expected property: if physical order is normative, this must be explicit; otherwise positions must not silently depend on runtime/storage traversal.

### C12 — Temporal-order trap

A candidate enumeration sorts by timestamp and uses a tie-breaker.

Expected property: the tie-breaker must not manufacture `ordered_ticks` relations.

---

# 6. KEY AUDIT DISTINCTIONS

The following must remain separate:

```text
RECORD MEMBERSHIP
≠
RECORD ENUMERATION
≠
OBSERVATION IDENTITY
≠
TEMPORAL ORDER
```

A rule can identify records without determining when one record occurred before another.

Likewise, a rule can define when a position becomes immutable without defining how records are enumerated.

---

# 7. REQUIRED OUTPUT OF THIS AUDIT

The final adjudication must identify:

1. what the corpus actually proves;
2. what remains merely an architecture proposal;
3. which candidate mechanisms are eliminated and why;
4. whether one exact enumeration rule can be derived from existing corpus material;
5. whether further human architecture choice is required;
6. whether record boundary, multi-file handling, artifact identity, or format conversion are genuinely blocking dimensions or merely conditional dependencies.

No implementation change is authorized by this audit.

No new Master Plan requirement is created.

No hash, byte offset, physical row, source ID, format continuity, or global sequence decision is created implicitly.

## FIN
