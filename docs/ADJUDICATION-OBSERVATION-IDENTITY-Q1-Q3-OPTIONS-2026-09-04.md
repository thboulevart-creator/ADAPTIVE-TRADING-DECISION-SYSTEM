# ADJUDICATION INPUT — OBSERVATION IDENTITY — Q1 → Q3

**Status:** DECISION INPUT ONLY — NO DECISION CREATED

**Parent:** `OI-01`

This document separates the choices requiring explicit adjudication. It does not promote any option to a normative rule.

---

## Q-1 — COMPOSITION

### Option A — Source-defined identity

Use an identity supplied by the upstream source, provided it is stable, complete for the relevant scope, and preserved by qualification.

### Option B — Upstream-qualified composite identity

The upstream qualification layer defines a deterministic identity from source-level information sufficient to distinguish individual primary observations.

### Option C — Dataset-position identity

Use a deterministic position/ordinal within a qualified dataset or stream.

### Option D — Content-derived identity

Use a deterministic function of the observation content.

**Adjudication warning:** content-only identity may collapse distinct duplicate observations and therefore cannot be accepted without an explicit duplicate decision.

---

## Q-2 — SCOPE

### Option A — Dataset-version scope

Identity is unique within a specific qualified dataset version.

### Option B — Source-stream scope

Identity is unique within the relevant source stream/instrument scope.

### Option C — Dataset-lineage scope

Identity remains comparable across derived dataset artifacts belonging to the same qualified lineage.

### Option D — Global scope

Identity is globally unique across datasets and sources.

No option is currently selected.

---

## Q-3 — DUPLICATE OBSERVATIONS

### Option A — Preserve individuality

If the qualified primary dataset contains two distinct observations, both remain distinct observations even when all visible values are identical.

### Option B — Semantic deduplication

Identical observations may represent one logical observation and may be collapsed under an explicit rule.

### Option C — Conditional rule

Duplicate treatment depends on upstream source semantics and must be explicitly declared by the qualification layer.

No option is currently selected.

---

## DECISION RULE

The adjudication must select explicit answers for Q-1, Q-2 and Q-3.

A decision must not silently imply answers to Q-4 → Q-7 unless those implications are logically unavoidable and explicitly recorded as consequences.

No `tick_id`, hash algorithm, serialization scheme, collision policy or implementation identifier is authorized by this document.

---

## FIN
