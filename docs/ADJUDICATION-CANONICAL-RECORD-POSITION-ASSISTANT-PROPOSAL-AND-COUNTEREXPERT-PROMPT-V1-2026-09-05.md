# CANONICAL RECORD POSITION — ASSISTANT PROPOSAL & COUNTER-EXPERT PROMPT

## Status

**PROPOSAL ONLY — NO HUMAN ARCHITECTURE DECISION TAKEN**

This document records the assistant's current architectural proposal for the unresolved question of how to assign `CANONICAL_RECORD_POSITION` after the explicit selection of the positional identity family.

It must not be treated as a frozen decision or as a Master Plan requirement.

---

# 1. FROZEN CONTEXT

The following decisions are already explicit:

```text
OBSERVATION_IDENTITY
=
QUALIFIED_DATASET_DOMAIN
+
CANONICAL_RECORD_POSITION
```

The identity domain is acquisition/qualified-dataset scoped.

The identity of an observation is not the identity of a market event.

Strict duplicate primary observations retained by qualification must remain individually distinguishable.

`ordered_ticks` remains the unique normative authority for temporal relations.

`CANONICAL_RECORD_POSITION` must never itself establish temporal precedence and must never be used to construct `ordered_ticks`.

Runtime traversal order is not normative.

`1.1.2` consumes, preserves and propagates the upstream identity; it does not own the upstream identity-generation rule.

The following have NOT been decided merely by selecting the positional family:

- source-provided identity;
- physical row number as a universal rule;
- byte offset;
- file hash as identity;
- content-derived identity;
- temporal sorting;
- global multi-file ordinal;
- format-conversion identity continuity;
- inter-acquisition identity equivalence;
- collision policy;
- exact serialization/encoding of the identity.

---

# 2. QUESTION CURRENTLY OPEN

The exact rule for assigning `CANONICAL_RECORD_POSITION` is still open.

The corpus establishes that the position must be deterministic, stable after assignment, independent of runtime traversal, compatible with retained duplicates, and independent of temporal ordering.

The corpus does not yet establish the exact enumeration rule.

---

# 3. ASSISTANT'S PROPOSED ANSWER

## Proposed rule

The assistant's current proposal is:

> `CANONICAL_RECORD_POSITION` should be assigned once, upstream during qualification, by enumerating the **logical primary records of the qualified acquisition artifact in a deterministic canonical record order defined by the qualification contract**.

Conceptually:

```text
QUALIFIED ACQUISITION ARTIFACT
        ↓
DETERMINISTIC NORMATIVE PARSING
        ↓
LOGICAL PRIMARY RECORDS
        ↓
CANONICAL RECORD ENUMERATION
        ↓
CANONICAL_RECORD_POSITION
        ↓
OBSERVATION_IDENTITY
```

The critical property is that the canonical enumeration describes the identity of retained records **within the qualified dataset domain**. It is not a temporal ordering.

### Proposed normative properties

For a qualified dataset domain `D`, let the retained primary records be:

```text
R = {r1, r2, ..., rn}
```

The qualification contract would define a deterministic enumeration function:

```text
E(D) = [r(0), r(1), ..., r(n-1)]
```

and assign:

```text
CANONICAL_RECORD_POSITION(r(i)) = i
```

subject to:

1. every retained primary record appears exactly once;
2. no non-retained record receives a normative position;
3. retained duplicate records receive distinct positions when they are distinct records in the qualified dataset;
4. the result is independent of runtime traversal order;
5. the result is stable after qualification within the declared qualified dataset lineage;
6. the enumeration rule does not use temporal precedence as its meaning;
7. the resulting position cannot establish an `ordered_ticks` relation;
8. the enumeration is deterministic for every conforming implementation.

### Important qualification

The proposal deliberately does **not** yet select the physical mechanism used to realize the canonical enumeration.

In particular, this proposal does not yet declare that the canonical order is:

- raw file row order;
- byte offset order;
- provider sequence order;
- content sort order;
- timestamp order;
- hash order;
- filesystem order;
- runtime iteration order.

Those mechanisms must only become normative if independently justified and explicitly adjudicated.

---

# 4. WHY THIS IS MY CURRENT ANSWER

The key distinction is:

```text
RECORD MEMBERSHIP
≠
RECORD ENUMERATION
≠
OBSERVATION IDENTITY
≠
TEMPORAL ORDER
```

The positional identity decision already requires a coordinate for each retained record. Therefore some deterministic enumeration is a necessary consequence of the selected family.

However, assigning a position at qualification is not itself sufficient: it specifies **when the position becomes fixed**, not **how the records are enumerated**.

The proposed construction therefore places the missing rule upstream:

```text
qualified dataset
→ deterministic logical-record enumeration
→ position assigned once
→ position preserved downstream
```

This preserves duplicate observations without claiming that duplicates are different market events.

It also avoids using timestamp sorting as a surrogate for temporal order. Temporal order remains the responsibility of `ordered_ticks`, which can remain partial when the source does not establish a total physical order.

The proposal is intentionally conservative regarding artifact identity, format conversion, multi-file aggregation and physical storage. It does not infer that content hashes, byte offsets or global file order are mandatory.

---

# 5. MAIN RISK IN MY PROPOSAL

The principal unresolved issue is whether the phrase:

> "logical primary records of the qualified acquisition artifact in a deterministic canonical record order defined by the qualification contract"

is actually sufficient to define a unique normative construction, or whether it merely restates the problem.

The counter-expert must therefore attack this point directly.

In particular, determine whether the proposed rule still hides unresolved choices concerning:

- exact record boundaries;
- parsing determinism;
- multi-file acquisitions;
- physical artifact versus logical record sequence;
- source ordering;
- format conversion;
- duplicate record handling;
- acquisition lineage;
- insertion/reordering of records;
- reproducibility across conforming implementations.

No hidden architecture choice may be smuggled in under the word "canonical".

---

# 6. COUNTER-EXPERTISE REQUEST FOR CLAUDE / GROK

## Mandate

You are acting as an **independent adversarial architecture auditor**.

Do not attempt to validate the assistant's proposal by default.

Your objective is to determine whether the proposed rule is actually sufficient, whether it contains hidden assumptions, whether it contradicts the authoritative corpus, or whether a different rule is logically required.

The current proposal is **not a decision**. Do not treat it as normative.

Do not modify the repository.

Do not create commits.

Do not invent missing Master Plan requirements.

Do not silently promote an architecture proposal into a normative requirement.

---

## Question to audit

After the explicit decision:

```text
OBSERVATION_IDENTITY
=
QUALIFIED_DATASET_DOMAIN
+
CANONICAL_RECORD_POSITION
```

is the following rule a valid and sufficiently precise way to define the missing position?

> `CANONICAL_RECORD_POSITION` is assigned once during qualification by enumerating the logical primary records of the qualified acquisition artifact in a deterministic canonical record order defined by the qualification contract, independently of runtime traversal and without making the position a temporal relation.

---

## Required adversarial analysis

### A — Logical sufficiency

Does this rule actually define an enumeration, or does it merely say that an enumeration must exist?

Identify every remaining degree of freedom that could allow two conforming implementations to assign different positions.

### B — Record boundaries

Is a normative record-boundary rule logically required for deterministic enumeration?

If yes, explain whether this is:

- a necessary consequence;
- a separate human architecture decision;
- or simply an implementation detail that can remain inside the qualification contract.

Do not assume that a new D-1 decision is automatically required.

### C — Multi-file / partitioned acquisition

Does the rule require a single global sequence across multiple files/partitions?

Or can each artifact/domain have its own canonical enumeration without violating the selected identity family?

Do not invent a global ordinal unless the corpus requires it.

### D — Physical versus logical ordering

Can the canonical enumeration legitimately follow the deterministic order of logical records in the qualified acquisition artifact?

What exactly would make that order normative without confusing it with temporal order?

Do not assume that physical byte order, filesystem order, or row number is automatically normative.

### E — Duplicates

Does the rule preserve distinct positions for strict duplicate records that are distinct retained observations?

Can this be achieved without claiming that they are distinct market events?

### F — Temporal independence

Can any interpretation of the proposed canonical order accidentally imply:

```text
position(A) < position(B)
⇒
A temporally precedes B
```

If yes, specify the exact prohibition required.

### G — Reordering and qualification stability

Once qualification assigns positions, what exactly must remain invariant under:

- runtime traversal permutation;
- in-memory reorder;
- parallel processing;
- restart;
- downstream transformation;
- bar reconstruction;
- derived representations?

### H — Acquisition copy / re-acquisition

Given acquisition-scoped identity, must byte-identical copies of an artifact receive the same positions?

Must independent acquisitions receive the same positions?

Do not infer cross-acquisition identity unless the corpus requires it.

### I — Format conversion

Does identity need to survive conversion between representations of the same logical records?

If the corpus does not decide this, explicitly say so.

Do not invent a format-continuity rule.

### J — Hash / content identity

Does the proposed rule require a content hash, artifact hash, byte offset, or other physical locator?

If not, confirm that these remain architecture choices rather than normative requirements.

### K — Determinism across implementations

What is the minimum exact condition required so that two conforming implementations necessarily assign the same position to the same retained record?

Is the following sufficient?

```text
same qualified dataset
+
same qualification contract
+
same deterministic logical-record enumeration rule
⇒
same canonical position assignment
```

If not, identify the missing invariant.

### L — Relation to `ordered_ticks`

Confirm that canonical position and temporal order are separate relations.

Determine whether the contract needs an explicit structural prohibition against deriving `ordered_ticks` from position.

### M — Scope of the decision

Determine whether adopting this rule would accidentally decide any of the following without explicit adjudication:

- artifact hash identity;
- byte offset identity;
- source ID semantics;
- global multi-file ordinal;
- format-conversion continuity;
- inter-acquisition identity;
- record-boundary implementation;
- temporal ordering.

---

# 7. REQUIRED OUTPUT

Return exactly:

## 1. VERDICT

One of:

```text
ACCEPTABLE
PARTIAL
INSUFFICIENT
BLOCKED
```

## 2. What the assistant got right

Only claims supported by the authoritative corpus or logically necessary consequences.

## 3. What the assistant got wrong

Identify any reasoning error, hidden assumption, or unjustified architectural leap.

## 4. What remains unresolved

Separate:

- normative requirement;
- necessary consequence;
- architecture proposal;
- absence of proof;
- human decision required.

## 5. Minimal rule that survives adversarial scrutiny

Give the narrowest formulation that is actually defensible.

Do not add mechanisms that are not required.

## 6. Human decision required

If a human decision remains necessary, formulate exactly one precise decision question.

## 7. Impact on `1.1.2`

State whether any amendment to `1.1.2` is authorized at this stage.

Unless the rule has been explicitly adjudicated and decided, the default is:

```text
NO 1.1.2 AMENDMENT
```

---

# 8. FINAL DISCIPLINE

The project follows:

```text
ASSISTANT PROPOSAL
↓
CLAUDE/GROK COUNTER-EXPERTISE
↓
ADJUDICATION
↓
EXPLICIT HUMAN DECISION
↓
CONTRACT CORRECTION
↓
NEW ADVERSARIAL AUDIT
```

Do not collapse these stages.

The purpose of this request is to attack the assistant's answer before the project decides whether to adopt it.
