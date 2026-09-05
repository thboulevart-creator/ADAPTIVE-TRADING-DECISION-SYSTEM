# ADJUDICATION — OBSERVATION IDENTITY — Q1 COMPOSITION

**Date:** 4 September 2026  
**Scope:** normative composition of individual primary observation identity upstream of `1.1.2`  
**Status:** **BLOCKED — NO ARCHITECTURE DECISION TAKEN**  
**Reference basis:** `OI-01`, `OI-02`, Q1 candidate-elimination audit, canonical-sequence audit, Grok↔corpus audit, Claude and Grok counter-expertise.

---

# 1. QUESTION

The exact adjudication question is:

> **What composition shall the upstream normative contract use to identify one individual primary market observation within the acquisition-scoped domain already established by `OI-01` and `OI-02`?**

This adjudication must determine whether the corpus logically forces a positional identity, or merely makes positional identity the strongest currently identified architectural candidate.

It must not convert architectural convenience into a normative decision.

---

# 2. FROZEN CONSTRAINTS ENTERING THIS ADJUDICATION

The following are already established and are not reopened here:

1. Individual observation identity is owned upstream of `1.1.2` by the `1.1.1` / upstream data-contract responsibility boundary (`OI-01`).
2. Identity stability is acquisition/qualified-dataset scoped; no automatic inter-acquisition equivalence exists (`OI-02`).
3. Observation identity is distinct from market-event identity.
4. Distinct primary observations retained by the qualified dataset must remain individually distinguishable, including strict duplicate records.
5. `ordered_ticks` remains the unique normative authority for established temporal relations.
6. Identity or canonical position must never be used to invent a temporal relation.
7. Runtime traversal order/index cannot become normative identity.
8. No specific hash, encoding, serialization scheme, collision policy, provider guarantee, or implementation-generated identifier has been authorized.
9. `1.1.2` consumes, preserves and propagates the upstream identity; it does not invent a competing identity mechanism.

These constraints are supported by the existing adjudication and audit chain. `OI-01` explicitly leaves composition unresolved and forbids inferring a concrete identity mechanism from ownership alone. citeturn127file0 `OI-02` explicitly leaves the exact composition and canonical enumeration unresolved. citeturn134file0

---

# 3. CANDIDATE FAMILIES

## Q1-A — Source-defined identity

The source supplies an individual identifier with sufficient guarantees.

**Corpus finding:** no such normative source guarantee is currently proven.

**Classification:** `[ABSENCE DE PREUVE]`

This option is not logically impossible. It is simply not selectable as normative from the present corpus without evidence establishing the required guarantees.

---

## Q1-B — Upstream-qualified composite identity

The upstream qualification contract defines an individual identity from source-level information sufficient to distinguish every retained observation.

**Corpus finding:** this is a broad valid family, but it does not itself specify which information forms the identity.

It can therefore contain a positional construction, a source identifier plus provenance, or another deterministic upstream-defined composite.

**Classification:** `[ARCHITECTURE PROPOSÉE]` as a family; `[ABSENCE DE PREUVE]` for any particular composition.

---

## Q1-C — Dataset-position / provenance + local position

Candidate form:

```text
(observation_domain, canonical_local_position)
```

where the domain is acquisition-scoped and the local position is assigned deterministically upstream.

This family is the strongest surviving candidate in the existing audits because it can, in principle, distinguish retained strict duplicates, survive downstream runtime reordering, remain independent from temporal order, and fit acquisition-scoped identity.

However, its decisive primitive — `canonical_local_position` — is not currently defined by the authoritative corpus. The candidate-elimination audit explicitly classified this family as the strongest architectural family, not as a frozen normative primitive. citeturn137file0

**Classification:** `[ARCHITECTURE PROPOSÉE]`

The upstream canonical-sequence adjudication likewise remains explicitly decision-required and does not authorize a positional identity. citeturn129file0

---

## Q1-D — Content-derived identity

Identity is derived solely from observation content.

For the strict-duplicate case already preserved by the qualified dataset, a content-only function cannot distinguish two distinct retained records having identical content.

Therefore content-only identity is incompatible with the established requirement that retained distinct observations remain individually distinguishable.

**Classification:** `[CONSÉQUENCE NÉCESSAIRE]`

This eliminates content-only identity as a sufficient standalone primitive under the current constraints. It does not prohibit a future composite identity that contains content-derived information plus another distinguishing component.

---

# 4. WHAT THE CORPUS ELIMINATES

The evidence permits the following conclusions without creating new architecture:

### 4.1 Content alone is insufficient

A deterministic function of visible observation content alone cannot distinguish strict duplicate observations that the qualified dataset intentionally retains as distinct.

Therefore:

```text
content-only identity
→ insufficient
```

### 4.2 Runtime position alone is insufficient

An in-memory traversal index is not stable under runtime reorder and therefore cannot be normative identity.

### 4.3 Timestamp alone is insufficient

Equal timestamps do not establish a unique temporal precedence relation. Timestamp sorting cannot silently manufacture one merely to obtain unique identity coordinates.

### 4.4 Existing dataset-level identifiers are insufficient alone

Dataset identity/provenance values identify a dataset or lineage, not one individual observation within it.

### 4.5 Source-defined identity is not currently proven

No authoritative source guarantee sufficient to adopt a provider-supplied individual identifier has been established.

These are elimination/absence-of-proof findings. They do **not** prove that positional identity is the only possible remaining architecture.

---

# 5. WHAT THE CORPUS DOES NOT PROVE

The corpus does not currently prove any of the following:

```text
position must be the identity
hash must identify the artifact
byte-identical acquisitions must share identity
all files of an acquisition require one global ordinal
format conversion must preserve individual identity
physical row number is normative
source artifact byte offset is normative
```

The Grok↔corpus audit specifically rejected the attempt to derive these as necessary consequences, including the earlier inference that C11 implied a mandatory content hash. citeturn135file0

Therefore none of these may be inserted into the contract at this adjudication stage.

---

# 6. CAN POSITIONAL IDENTITY BE LOGICALLY FORCED?

**Answer: NO, not from the currently authoritative corpus.**

The corpus demonstrates that an individual identity must be:

- individually distinguishing within its normative domain;
- stable under the transformations and runtime reorderings for which stability is required;
- deterministic and comparable;
- independent from artificial temporal ordering.

But those properties do not logically entail one unique implementation-independent representation.

A source-defined identifier could satisfy them if the necessary guarantees were established.

An upstream-qualified composite could satisfy them if its exact composition were established.

A positional identity could satisfy them if a deterministic canonical enumeration were established.

Thus:

```text
POSITIONAL FAMILY
→ strongest currently demonstrated candidate

POSITIONAL FAMILY
≠
LOGICALLY FORCED DECISION
```

The distinction is essential. Selecting the positional family would therefore be an architecture decision, not a mere restatement of an already-proven Master Plan requirement.

**Classification:**

```text
[ARCHITECTURE PROPOSÉE]
```

for the positional family.

```text
[ABSENCE DE PREUVE]
```

for the proposition that the corpus uniquely forces it.

---

# 7. ADJUDICATION RESULT

The formal adjudication therefore cannot legitimately record:

```text
Q1 = POSITIONAL IDENTITY
```

as a corpus-forced decision.

It also cannot record:

```text
Q1 = SOURCE ID
```

or another concrete mechanism, because the corpus does not prove such a mechanism either.

The correct adjudication result is:

```text
Q1 COMPOSITION
→ NOT ADJUDICATED
→ ARCHITECTURE DECISION REQUIRED
```

This is not a failure of the audit. It is the result required by the project's non-invention rule.

---

# 8. EXACT HUMAN ARCHITECTURAL DECISION REQUIRED

The human decision is now narrowed to the following:

> **Do we explicitly choose an acquisition-scoped positional identity for individual qualified observations, i.e. an identity based on a normative domain plus a deterministic canonical local record position, or do we reject that family and require another explicitly specified upstream identity mechanism?**

If the positional family is selected, the next dependent adjudication is **not** “how do we code it?” but:

> **What exact upstream rule canonically enumerates the retained primary records and assigns their stable local positions without depending on runtime traversal, collapsing retained duplicates, or creating artificial temporal order?**

If the positional family is rejected, the alternative identity mechanism must itself be explicitly specified and subjected to the same adversarial tests.

---

# 9. NO IMPLICIT DECISIONS

This adjudication creates no decision on:

- hash algorithm;
- artifact content identity;
- file path identity;
- byte offset identity;
- source provider identifier;
- global multi-file ordering;
- record-boundary convention beyond whatever the applicable upstream contract already normatively defines;
- identity continuity across physical format conversion;
- inter-acquisition identity;
- market-event identity;
- temporal ordering;
- late-tick policy;
- `event_time` / `availability_time`.

No such point may be inferred from the fact that the positional family is currently the strongest candidate.

---

# 10. EFFECT ON 1.1.2

No modification to `1.1.2` is authorized by this adjudication.

`V12-01` remains blocked because the individual identity primitive is still not normatively defined.

The current V3 contract must therefore **not** be amended to encode a positional identity until the explicit architecture decision above is made and the dependent upstream identity contract is defined.

---

# 11. PIPELINE STATE

```text
Q1 QUESTION
   ↓
CORPUS AUDIT                         ✓
   ↓
POSITION-STABILITY AUDIT            ✓
   ↓
CANONICAL-SEQUENCE AUDIT             ✓
   ↓
CANDIDATE ELIMINATION                ✓
   ↓
CLAUDE COUNTER-EXPERTISE             ✓
   ↓
GROK COUNTER-EXPERTISE               ✓
   ↓
GROK ↔ CORPUS CONFRONTATION          ✓
   ↓
Q1 COMPOSITION ADJUDICATION          ✓ BLOCKED
   ↓
EXPLICIT ARCHITECTURE DECISION       ← REQUIRED
   ↓
UPSTREAM IDENTITY CONTRACT            ← DEPENDENT
   ↓
1.1.2 MINIMAL CORRECTION              ← LATER
   ↓
NEW ADVERSARIAL AUDIT                 ← LATER
```

---

# 12. CLOSURE CONDITION FOR Q1

Q1 may be considered adjudicated only when one of the following occurs:

### Path A — positional family selected

An explicit decision records that acquisition-scoped positional identity is the chosen composition family. The decision must then authorize a dependent upstream canonical-enumeration adjudication before any concrete position formula becomes normative.

### Path B — positional family rejected

An explicit decision records the alternative identity family and its required semantic guarantees. The alternative must then be audited against the same constraints before the upstream identity contract is frozen.

Until one of these occurs:

```text
Q1 = BLOCKED
V12-01 = BLOCKED
1.1.2 = NOT CLOSED
```

---

## FIN — Q1 COMPOSITION ADJUDICATION
