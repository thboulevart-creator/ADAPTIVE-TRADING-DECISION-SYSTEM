# ADJUDICATION — NORMATIVE OWNERSHIP OF INDIVIDUAL OBSERVATION IDENTITY

**Date:** 4 September 2026

**Scope:** Upstream dependency of `1.1.2` — identity of individual primary market observations

**Status:** DECISION EXPLICIT — OWNERSHIP ADJUDICATED

**Decision source:** User adjudication following corpus verification and independent counter-expertise.

---

## 1. QUESTION

Where must the normative identity of each individual primary market observation be owned and defined?

The question was raised because `1.1.2` requires stable observation identity for canonicalization and identity correspondence, while the verified authoritative corpus did not contain a normative definition of that identity.

---

## 2. CORPUS STATE AT ADJUDICATION

The upstream corpus verification established:

```text
NO NORMATIVE INDIVIDUAL-OBSERVATION IDENTITY VERIFIED
```

`05-DATA-CONTRACT.md`, `08-SYSTEM-REGISTRY.md`, `09-DATASET-PROVENANCE-REGISTRY.md` and `10-TEMPORAL-POINT-IN-TIME-CONTRACT.md` could not be imported as normative identity definitions merely from their existing content/status.

The independent counter-expertise confirmed the same factual conclusion and identified the unresolved dependencies Q-1 through Q-7.

The existing `1.1.2` adjudication therefore correctly maintained `V12-01` as blocking and prohibited `1.1.2` from inventing a local identity.

---

## 3. EXPLICIT DECISION

### DECISION OI-01 — OWNERSHIP

**DECISION:**

> The normative individual identity of primary market observations shall be owned and defined by the normative layer upstream of `1.1.2` that is responsible for qualification and identity of the primary dataset, i.e. the `1.1.1` / upstream data-contract responsibility boundary, subject to the exact existing Master Plan terminology being preserved when the upstream contract is amended.

`1.1.2` is therefore **not** the owner of individual observation identity.

`1.1.2` shall consume, preserve, propagate and use the upstream-defined identity, but shall not create a competing identity for the same primary observation.

**Classification:**

```text
[DECISION EXPLICITE — ARCHITECTURAL OWNERSHIP]
```

This decision resolves ownership only. It does **not** define the identity's composition, encoding, hashing, serialization, collision policy, or transformation semantics.

---

## 4. RESPONSIBILITY BOUNDARY

The normative responsibility boundary is:

```text
UPSTREAM QUALIFICATION / DATA CONTRACT
        │
        │ defines normative identity
        ▼
QUALIFIED PRIMARY OBSERVATIONS
        │
        │ identity preserved
        ▼
1.1.2 — DATA TRANSFORMATION & TEMPORAL REPRESENTATION
        │
        │ consumes / preserves / propagates identity
        ▼
DERIVED REPRESENTATIONS
```

The identity belongs semantically to the primary observation, not to a derived representation such as a bar.

A derived representation must therefore retain a deterministic correspondence to the identities of the primary observations from which it was derived whenever such correspondence is required by its contract.

---

## 5. WHAT THIS DECISION DOES NOT DECIDE

The following remain open and must not be inferred from OI-01:

```text
Q-1 — identity composition
Q-2 — identity scope
Q-3 — treatment of duplicate observations
Q-4 — stability across transformations
Q-5 — stability under reordering
Q-6 — canonical comparison / serialization
Q-7 — collision handling
```

In particular, this decision does **not** authorize:

- `tick_id = hash(timestamp + bid + ask)`;
- a source-row number as identity;
- a runtime-generated identifier;
- a content hash as identity;
- any specific hash algorithm;
- any collision-resolution mechanism.

Those are separate decisions.

---

## 6. CONSEQUENCES FOR 1.1.2

The following consequences are now authorized as necessary consequences of OI-01:

1. `1.1.2` must not define an independent identity for primary observations.
2. `1.1.2` must preserve the upstream identity through temporal partitioning and derived representations where correspondence is required.
3. Tests comparing primary observations across representations may rely on the upstream identity only once its definition is normatively established.
4. The `ordered_ticks.observations` universe must remain referentially connected to the same primary observation identities.
5. Any future correction of `1.1.2` must distinguish identity ownership from identity implementation.

These consequences do not close `V12-01` yet because the actual identity definition remains absent.

---

## 7. PIPELINE STATE

Before this decision:

```text
OWNERSHIP                  UNRESOLVED
IDENTITY DEFINITION        UNRESOLVED
V12-01                     BLOCKED
1.1.2                      NOT CLOSED
```

After this decision:

```text
OWNERSHIP                  RESOLVED → UPSTREAM / 1.1.1 BOUNDARY
IDENTITY DEFINITION        UNRESOLVED
V12-01                     STILL BLOCKED
1.1.2                      NOT CLOSED
```

Therefore this decision authorizes the next upstream adjudication block but does not authorize a `1.1.2` correction yet.

---

## 8. NEXT ADJUDICATION TARGET

The next decision must define the semantics of the individual observation identity itself, beginning with:

```text
Q-1 — composition
Q-2 — scope
Q-3 — duplicate observations
```

Then, as dependent questions:

```text
Q-4 — transformation stability
Q-5 — reordering stability
Q-6 — canonical comparison / serialization
Q-7 — collision handling
```

No implementation-specific identity may be promoted to normative status before these questions are adjudicated.

---

## 9. NON-DÉRIVE GUARD

This decision does not:

- modify `1.1.2`;
- create V13/V14;
- close `V12-01`;
- define `tick_id`;
- select a hash;
- define duplicate semantics;
- define late-tick policy;
- define `event_time` / `availability_time`;
- promote any previously non-normative document to normative status.

---

## FIN — OI-01
