# ADJUDICATION — INDIVIDUAL OBSERVATION IDENTITY — Q1 → Q3

**Date:** 4 September 2026

**Status:** ADJUDICATION BLOCK — DECISION REQUIRED

**Parent decision:** `ADJUDICATION-OBSERVATION-IDENTITY-DECISION-2026-09-04.md` / `OI-01`

---

## 1. SCOPE

`OI-01` has resolved ownership: normative individual observation identity belongs upstream of `1.1.2`, at the `1.1.1` / upstream data-contract responsibility boundary.

The identity itself remains undefined.

This block therefore adjudicates the first three semantic questions only:

```text
Q-1 — composition
Q-2 — scope
Q-3 — duplicate observations
```

No implementation-specific identity is assumed.

---

# 2. Q-1 — COMPOSITION

## Question

What information constitutes the normative identity of one individual primary observation?

Candidate classes include, without adopting any of them:

- source-provided identifier;
- source position / record identity;
- dataset-relative ordinal;
- timestamp;
- price fields;
- complete raw observation payload;
- deterministic composite of source and positional information;
- other upstream-defined identity mechanism.

## Constraint

The composition must distinguish individual observations whenever the primary dataset treats them as distinct observations.

In particular, an identity definition must not silently collapse two primary observations merely because their visible market values are equal.

## Status

```text
UNRESOLVED
```

No composition is authorized by this artifact.

---

# 3. Q-2 — SCOPE

## Question

Within what domain is an observation identity unique and stable?

Possible scopes include, without adopting any of them:

- source stream;
- instrument + source;
- qualified dataset version;
- dataset lineage;
- global system scope.

## Constraint

The scope must be sufficient for every normative comparison in which the identity is used, including correspondence between primary observations and derived representations.

Dataset-level provenance identifiers must not be confused with individual-observation identity.

## Status

```text
UNRESOLVED
```

No scope is authorized by this artifact.

---

# 4. Q-3 — DUPLICATE OBSERVATIONS

## Question

When two primary observations have identical visible content, are they:

```text
ONE OBSERVATION
```

or:

```text
TWO DISTINCT OBSERVATIONS WITH DISTINCT IDENTITIES
```

when the source/qualified dataset preserves both?

## Constraint already established

The primary dataset is not permitted to lose distinct observations merely through a content-based identity shortcut.

Therefore any identity mechanism that can map multiple distinct primary observations to one identity requires an explicit adjudication before it can be normative.

## Status

```text
UNRESOLVED
```

No deduplication or identity-collapsing rule is authorized by this artifact.

---

# 5. REQUIRED DECISION QUALITY

The eventual Q1–Q3 decision must establish, at minimum:

```text
IDENTITY CANONICALITY
INDIVIDUALITY
SCOPE
DUPLICATE SEMANTICS
DETERMINISTIC COMPARABILITY
```

It must remain compatible with:

- preservation of the primary observation universe;
- `ordered_ticks` observation identity correspondence;
- H-04 / A-09 canonicalization requirements;
- reproducibility across conforming implementations;
- absence of information loss caused solely by identity assignment.

---

# 6. NON-DÉRIVE GUARD

This document does not select:

- `tick_id` format;
- hash algorithm;
- source row number;
- timestamp-based identity;
- content hash;
- collision policy;
- serialization format.

Those remain decisions for the appropriate adjudication stage.

---

## FIN — Q1 → Q3
