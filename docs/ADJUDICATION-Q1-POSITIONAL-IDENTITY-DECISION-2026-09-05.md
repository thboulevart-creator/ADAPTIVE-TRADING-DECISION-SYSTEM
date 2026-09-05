# ADJUDICATION — Q1 POSITIONAL OBSERVATION IDENTITY

**Date:** 5 September 2026  
**Parent:** `ADJUDICATION-OBSERVATION-IDENTITY-Q1-COMPOSITION-2026-09-04.md`  
**Status:** **DECISION TAKEN — POSITIONAL FAMILY SELECTED**

---

# 1. DECISION

The project explicitly selects the **acquisition-scoped positional identity family** for individual qualified primary observations.

Normative composition:

```text
OBSERVATION_IDENTITY
=
QUALIFIED_DATASET_DOMAIN
+
CANONICAL_RECORD_POSITION
```

This decision selects the identity family only.

It does **not** yet define how `CANONICAL_RECORD_POSITION` is generated.

Therefore:

```text
Q1 — COMPOSITION
→ POSITIONNELLE
→ OUI

CANONICAL_RECORD_POSITION
→ NOT YET DEFINED
```

---

# 2. SCOPE OF THE DECISION

The selected identity is the identity of an individual observation **within the qualified dataset domain**.

It is not a claim of identity of a real-world market event across independent acquisitions.

It is not a temporal-order identifier.

It is not an execution identifier.

It is not a content-only identity.

---

# 3. PRESERVED CONSTRAINTS

This decision preserves the constraints already established by the preceding audits and adjudications:

1. Observation identity is distinct from market-event identity.
2. Identity is acquisition/qualified-dataset scoped according to the previously adjudicated scope decision.
3. Distinct primary observations retained by the qualified dataset remain individually distinguishable, including strict duplicate visible values.
4. `ordered_ticks` remains the unique normative authority for established temporal relations.
5. `CANONICAL_RECORD_POSITION` must never itself establish temporal precedence.
6. Runtime traversal order must not become the identity mechanism.
7. `1.1.2` consumes, preserves, and propagates the upstream identity; it does not invent the upstream identity rule.

---

# 4. EXPLICITLY NOT DECIDED

This decision does **not** select or require any of the following:

- source-provided identifiers;
- physical row numbers;
- byte offsets;
- content hashes as artifact identity;
- any specific hash algorithm;
- any encoding or serialization;
- any collision policy;
- any global multi-file ordinal;
- any record-boundary convention;
- any format-conversion identity continuity rule;
- any inter-acquisition identity equivalence;
- any temporal sorting rule;
- any artificial total order;
- any implementation-specific runtime identifier.

These remain open unless separately adjudicated.

---

# 5. CONSEQUENCE FOR THE NEXT BLOCK

The next question is now legitimately narrower.

The project must determine how the upstream normative qualification contract generates a deterministic `CANONICAL_RECORD_POSITION` for every retained primary observation.

The rule must be sufficient to make the following mechanically decidable:

```text
same qualified dataset
        → same retained observation set
        → same canonical enumeration
        → same canonical record position
        → same observation identity
```

while preserving:

```text
CANONICAL_RECORD_POSITION
        ≠
TEMPORAL ORDER
```

The next adjudication must therefore focus on the **enumeration mechanism**, without silently deciding unrelated questions about hashes, physical storage, multi-file global ordering, format conversion, or event identity.

---

# 6. CURRENT STATE

```text
Q1 COMPOSITION
→ RESOLVED
→ POSITIONAL FAMILY SELECTED

CANONICAL RECORD ENUMERATION
→ OPEN

CANONICAL_RECORD_POSITION
→ NOT DEFINED

V12-01
→ STILL BLOCKED

1.1.2
→ NOT CLOSED
```

No modification to the `1.1.2` contract is authorized yet.

## FIN
