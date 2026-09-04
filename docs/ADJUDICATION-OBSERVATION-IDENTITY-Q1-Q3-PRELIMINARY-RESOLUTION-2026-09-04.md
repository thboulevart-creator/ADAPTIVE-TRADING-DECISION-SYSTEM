# ADJUDICATION — OBSERVATION IDENTITY — Q1 → Q3 — PRELIMINARY RESOLUTION

**Date:** 4 September 2026

**Status:** PARTIAL RESOLUTION — HUMAN DECISION STILL REQUIRED FOR Q-1 / Q-2

**Parent decision:** `OI-01`

---

## 1. RESULT

The ownership decision `OI-01` permits the semantic questions to be narrowed without inventing an identity implementation.

The current corpus and previously adjudicated invariants establish one strong consequence:

> If the qualified primary dataset contains two distinct primary observations, `1.1.2` must not collapse them merely because their visible values are identical.

Therefore Q-3 cannot be resolved in favor of implicit content-based deduplication.

However, the exact identity composition (Q-1) and exact scope (Q-2) remain architectural choices not determined by the current normative corpus.

---

# 2. Q-3 — DUPLICATE OBSERVATIONS

## Determination

**Selected by necessary consequence:**

```text
Q-3 → PRESERVE INDIVIDUALITY
```

If the qualified primary dataset contains two distinct observations, they remain two distinct observations even when timestamp, price and other visible fields are identical.

This does not prescribe how their distinct identities are encoded.

It also does not prohibit a future upstream qualification rule from declaring that certain source records are not distinct primary observations. Such a rule would have to be explicitly established upstream; `1.1.2` may not invent that semantic collapse.

**Classification:**

```text
[CONSÉQUENCE NÉCESSAIRE]
```

---

# 3. Q-1 — COMPOSITION

## Current determination

No normative composition is established.

The following remain possible but unselected:

```text
source-defined identity
upstream-qualified composite identity
position-based identity
content-derived identity
other explicitly adjudicated mechanism
```

The identity must nevertheless satisfy the already-established individuality requirement and must support the frozen canonicalization requirement.

**Classification:**

```text
QUESTION NON RÉSOLUE
```

---

# 4. Q-2 — SCOPE

## Current determination

No normative scope is established.

The scope must support the actual comparisons required by the architecture, including correspondence between primary observations and derived representations, without silently asserting global uniqueness where the corpus does not require it.

Possible scopes remain:

```text
dataset-version
source-stream
qualified dataset lineage
other explicitly adjudicated scope
```

**Classification:**

```text
QUESTION NON RÉSOLUE
```

---

# 5. CONSEQUENCE FOR NEXT DECISION

The remaining human choice is now narrower than the original seven-question block.

The critical decision is:

```text
Q-1 — WHAT CONSTITUTES THE IDENTITY?
Q-2 — WITHIN WHAT DOMAIN IS IT UNIQUE/STABLE?
```

Q-3 is provisionally resolved by preservation of primary-observation individuality, subject to compatibility review once Q-1/Q-2 are selected.

No identity formula, hash, source-row convention, or serialization format is created by this document.

---

## FIN — PRELIMINARY RESOLUTION
