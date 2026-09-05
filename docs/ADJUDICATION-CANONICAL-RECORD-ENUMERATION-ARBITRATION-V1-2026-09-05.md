# CANONICAL RECORD ENUMERATION — ARBITRAGE ARCHITECTURAL V1

**Date:** 5 September 2026  
**Scope:** canonical generation of `CANONICAL_RECORD_POSITION` only  
**Status:** **ARCHITECTURE DECISION REQUIRED — NO DECISION TAKEN**

---

## 1. OBJECTIVE

Determine the smallest set of genuine architectural candidate families capable of generating `CANONICAL_RECORD_POSITION` within the already-resolved identity family:

```text
OBSERVATION_IDENTITY
=
QUALIFIED_DATASET_DOMAIN
+
CANONICAL_RECORD_POSITION
```

This artifact does **not** select a candidate, modify `1.1.2`, reopen H-04, or create a new normative rule.

---

## 2. FROZEN CONSTRAINTS

The arbitration preserves:

- `ordered_ticks` as the unique normative authority for established temporal relations;
- canonical position as identity coordinate, never temporal precedence;
- strict retained duplicate records as individually distinguishable observations;
- runtime traversal, memory layout and parallel scheduling as non-normative;
- acquisition/qualified-dataset-scoped identity;
- no assumed cross-acquisition identity equality;
- no implicit hash, byte offset, physical row number, source identifier or global ordinal decision;
- `1.1.2` consumes and propagates upstream identity rather than owning its generation rule.

---

## 3. REDUCTION OF THE CANDIDATE SPACE

The previous broad candidate space can be reduced to four materially different families.

### C1 — SOURCE-DECLARED RECORD SEQUENCE / IDENTIFIER

Use an identity or sequence supplied by the upstream source, provided the upstream contract normatively guarantees its uniqueness, preservation and stability within the declared acquisition scope.

**Current assessment:** not adoptable as a normative rule from the current corpus because the required source guarantees are not established.

**Adversarial failures if guarantees are absent:**

- duplicate semantics remain ambiguous;
- source IDs may be unstable across acquisition;
- source sequence may be absent or non-unique;
- source ordering may be implementation/provider specific;
- `1.1.2` would inherit an unproven property.

**Status:** `ELIMINATED FOR CURRENT DECISION` due to absence of proof, not because the family is theoretically impossible.

---

### C2 — DETERMINISTIC ORDER OF LOGICAL RECORDS IN AN IMMUTABLE ACQUISITION ARTIFACT

The qualified acquisition artifact is identified as part of the acquisition scope. Its logical primary records are individuated by a normative parsing/record-boundary rule. A deterministic enumeration of those records assigns positions once during qualification.

Conceptually:

```text
IMMUTABLE ACQUISITION ARTIFACT
        ↓
NORMATIVE RECORD MODEL / BOUNDARIES
        ↓
DETERMINISTIC RECORD ENUMERATION
        ↓
CANONICAL_RECORD_POSITION
```

The critical point is that the criterion is the **declared logical record enumeration of the acquisition artifact**, not runtime traversal.

**Strengths:**

- naturally preserves strict duplicates as separate occurrences;
- can be independent of runtime traversal;
- can remain independent of temporal order;
- naturally supports acquisition-scoped identity;
- can be deterministic across implementations if parser and enumeration rules are normative;
- can support traceability back to the acquisition artifact.

**Blocking dependencies:**

- record individuation/boundaries;
- exact deterministic enumeration rule;
- multi-file/partition aggregation rule;
- point at which enumeration becomes immutable.

**Status:** `STRONGEST ARCHITECTURAL FAMILY — INCOMPLETE`

---

### C3 — QUALIFICATION-DEFINED ENUMERATION

Qualification creates the retained primary-record universe and applies an explicit deterministic enumeration function to that universe. The resulting position is assigned once and then propagated downstream.

Conceptually:

```text
QUALIFIED RECORD UNIVERSE
        ↓
NORMATIVE ENUMERATION FUNCTION
        ↓
CANONICAL_RECORD_POSITION
```

**Strengths:**

- directly aligned with the resolved ownership boundary;
- naturally excludes records not admitted into the qualified dataset;
- allows deterministic assignment before downstream transformation;
- preserves duplicate individuality if the enumeration operates on record occurrences rather than content equality;
- cleanly separates membership from enumeration.

**Critical weakness:**

“assigned at qualification” is not itself an enumeration criterion. A concrete deterministic function is still required.

**Status:** `ARCHITECTURALLY VALID FAMILY — INCOMPLETE`

---

### C4 — DETERMINISTIC EXTRINSIC RECORD COORDINATE / LOCATOR

Use a coordinate that identifies the individual record occurrence through an immutable acquisition representation, for example a structured artifact/partition/local-coordinate tuple. The exact physical primitive is intentionally not selected here.

Conceptually:

```text
ACQUISITION DOMAIN
+
IMMUTABLE RECORD OCCURRENCE COORDINATE
        ↓
CANONICAL_RECORD_POSITION
```

**Strengths:**

- distinguishes strict duplicate occurrences without semantic deduplication;
- does not require content uniqueness;
- can be independent of temporal ordering;
- can provide direct provenance.

**Critical weakness:**

A locator is not automatically a canonical enumeration rule. It becomes sufficient only if the coordinate itself is produced by a deterministic normative enumeration/record-boundary rule.

**Status:** `VALID ARCHITECTURAL SUB-FAMILY — DEPENDENT ON C2/C3`

---

## 4. CANDIDATES ELIMINATED AS STANDALONE RULES

The following are not viable as standalone normative enumeration criteria under the frozen constraints.

### E1 — Runtime collection order

**ELIMINATED.** Different traversal order can assign different positions to the same qualified dataset.

### E2 — Generic in-memory index

**ELIMINATED.** It is a runtime artifact, not an acquisition/qualification property.

### E3 — Timestamp sort as temporal sequence

**ELIMINATED.** It risks manufacturing temporal precedence where `ordered_ticks` deliberately leaves relations unresolved.

A timestamp may be an input to an enumeration function only if the resulting position is explicitly prevented from acquiring temporal semantics; timestamp-only ordering is nevertheless insufficient for strict duplicates and equal timestamps without additional non-temporal tie-breaking.

### E4 — Content-only sort / content hash

**ELIMINATED AS STANDALONE RULE.** Strict duplicate records can have identical content and therefore cannot be assigned distinct positions without an additional occurrence discriminator.

### E5 — Global ordinal across all files/sources

**NOT REQUIRED BY THE RESOLVED IDENTITY FAMILY.** It would introduce a global ordering decision not established by the current corpus.

### E6 — Physical row number without a normative artifact contract

**ELIMINATED AS GENERIC RULE.** Physical row order can only become normative if the exact immutable artifact, record boundaries and enumeration semantics are themselves normatively defined. Otherwise it is storage-dependent.

---

## 5. ADVERSARIAL EVALUATION MATRIX

| Criterion | C1 Source sequence | C2 Artifact logical enumeration | C3 Qualification enumeration | C4 Extrinsic coordinate |
|---|---|---|---|---|
| Determinism | **UNPROVEN** | **POSSIBLE** if rule frozen | **POSSIBLE** if function frozen | **POSSIBLE** if generation frozen |
| Strict duplicates | **UNPROVEN** | **PASSABLE** | **PASSABLE** | **PASSABLE** |
| Runtime-traversal independence | **UNKNOWN** | **PASS** if normative | **PASS** if normative | **PASS** if normative |
| Temporal independence | **UNKNOWN** | **PASS** if explicitly separated | **PASS** | **PASS** |
| Acquisition-scoped stability | **POSSIBLE** | **NATURAL** | **NATURAL** | **NATURAL** |
| Multi-file behavior | **UNKNOWN** | **MUST BE DEFINED** | **MUST BE DEFINED** | **MUST BE DEFINED** |
| Record boundaries | **SOURCE-DEPENDENT** | **MUST BE DEFINED** | **MUST BE DEFINED** | **MUST BE DEFINED** |
| Reproducibility | **UNPROVEN** | **STRONG IF RULE FROZEN** | **STRONG IF FUNCTION FROZEN** | **STRONG IF GENERATION FROZEN** |
| Traceability | **STRONG IF SOURCE GUARANTEE EXISTS** | **STRONG** | **STRONG** | **STRONG** |
| Compatibility with `ordered_ticks` | **UNKNOWN** | **PASS** if prohibited from temporal use | **PASS** | **PASS** |
| Current corpus support | **NO** | **PARTIAL** | **PARTIAL** | **DERIVED FROM C2/C3** |

---

## 6. CRITICAL OBSERVATION — C2 AND C3 ARE NOT FULLY DISTINCT

C2 and C3 differ primarily in **where the logical record universe and enumeration criterion are anchored**:

- C2 anchors enumeration in the immutable acquisition artifact;
- C3 anchors enumeration in the qualified record universe.

A conforming architecture could combine them:

```text
IMMUTABLE ACQUISITION ARTIFACT
        ↓
NORMATIVE RECORD MODEL
        ↓
QUALIFIED RECORD MEMBERSHIP
        ↓
DETERMINISTIC ENUMERATION
        ↓
CANONICAL_RECORD_POSITION
```

Therefore the genuine decision is not simply “C2 or C3”. The deeper decision is:

> **What declared non-temporal property of logical primary record occurrences constitutes the canonical enumeration criterion?**

The artifact/qualification boundary determines the domain and immutability point; it does not by itself define the ordering criterion.

---

## 7. DOMINANT CANDIDATE?

**No candidate is yet sufficiently complete to be declared dominant.**

C1 is eliminated by absence of source guarantees.

C4 cannot stand alone because a coordinate requires a generation rule.

C2 and C3 converge into the same viable architectural family but still require the unresolved concrete enumeration criterion and record model.

Therefore selecting one as “dominant” now would conceal the actual human decision rather than resolve it.

---

## 8. CLAUDE / GROK COUNTER-EXPERTISE

No new Claude/Grok round is justified at this stage.

Reason:

1. The remaining uncertainty is not whether the current proposal is underspecified; that has already been independently established.
2. The remaining issue is a genuine architecture choice concerning the canonical enumeration criterion.
3. Without a concrete human-selected candidate, another generic counter-audit would largely repeat the already-established conclusion.
4. The project methodology requires external counter-expertise when it adds independent information, not as a mandatory ritual.

A targeted Claude/Grok round becomes useful **after** a concrete candidate is selected, with the mandate to attack that exact choice.

---

## 9. CURRENT ARCHITECTURAL DECISION QUESTION

The smallest unresolved human decision is:

> **Quelle propriété déterministe, non temporelle et indépendante du traversal runtime des occurrences de records primaires qualifiés doit constituer le critère canonique d'énumération utilisé pour attribuer `CANONICAL_RECORD_POSITION` dans `QUALIFIED_DATASET_DOMAIN` ?**

The decision must also state whether the criterion is anchored in:

1. the immutable acquisition artifact;
2. the qualified logical-record universe;
3. a combination of both;
4. another explicitly justified non-temporal property.

It must **not** select `ordered_ticks`, timestamp precedence, runtime order, or content-only identity.

---

## 10. NO DECISION TAKEN

Current state remains:

```text
POSITIONAL IDENTITY FAMILY          = RESOLVED
QUALIFIED_DATASET_DOMAIN            = RESOLVED
ACQUISITION-SCOPED STABILITY        = RESOLVED
OWNERSHIP                            = RESOLVED UPSTREAM
CANONICAL_RECORD_POSITION           = REQUIRED
GENERATION RULE                     = UNRESOLVED
CONCRETE ENUMERATION CRITERION      = UNRESOLVED
RECORD INDIVIDUATION                = REQUIRED FOR RULE APPLICABILITY
CORPUS HIDDEN PRIMITIVE             = NOT FOUND
1.1.2                               = NOT CLOSED
```

No normative amendment is authorized by this artifact.
