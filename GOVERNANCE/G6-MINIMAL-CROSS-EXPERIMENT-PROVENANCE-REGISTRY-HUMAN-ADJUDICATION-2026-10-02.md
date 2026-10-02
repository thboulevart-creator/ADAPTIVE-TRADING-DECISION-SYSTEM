# G6 — HUMAN ADJUDICATION — MINIMAL CROSS-EXPERIMENT PROVENANCE REGISTRY

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Adjudication base HEAD:** `009295bf5e3fb3e74b6937115e4724153ff6ab9c`  
**Adjudication base TREE:** `6971c00699622b95faae957cea4f52f40dae96db`  
**Status:** HUMAN ADOPTED FOR SEMANTIC DESIGN ONLY

---

## 1. Scope and provenance of this adjudication

This artifact canonically persists the human adjudication of the non-normative study sequence:

```text
G0
G1
G2
G3
G4
G5
G5-R1
```

Those study stages were used to reduce and adversarially challenge the proposed mechanism before adoption.

This artifact does **not** claim that G0 through G5-R1 were separately persisted as canonical ATDS program artifacts. It persists the human decision over the resulting semantic design.

This adjudication is separate from the current SFE program frontier and does not modify any SFE contract, result, authority, or status.

---

## 2. Human decision

```text
G6_VERDICT =
ADOPT

ADOPTED_OBJECT =
MINIMAL CROSS-EXPERIMENT PROVENANCE REGISTRY
SEMANTIC DESIGN G5-R1

DESIGN_STATUS =
HUMAN_ADOPTED_FOR_SEMANTIC_DESIGN ONLY
```

---

## 3. Adopted principles

The adoption covers only the following principles:

1. reuse the existing research-registry concept rather than create a new Research Integrity Ledger;

2. persist outside runtime in a dedicated program-evidence surface;

3. use a content-bound, parent-linked registry chain;

4. identify events by immutable identities bound to their content;

5. identify relations by immutable identities;

6. use only the following minimal relation vocabulary:

```text
INFORMED_BY
PREREGISTERED_BY
RESERVED_FOR
CLASSIFIED_BY
```

7. decisive references must be typed, immutable and resolvable;

8. corrections use explicit supersession rather than silent historical rewrite;

9. an unexplained registry fork is `BLOCKED`;

10. absence of a record does not imply absence of an event;

11. absence of a relation does not imply absence of influence;

12. absence of known exposure does not imply pristine evidence;

13. neither `N_budget` nor `N_famille` may be inferred automatically from a simple count of registry events;

14. the registry may not self-adjudicate scientific classification or research-family membership;

15. the registry is never an autonomous source of scientific truth or operational authority.

---

## 4. Accepted fundamental limits

```text
REGISTRY_COMPLETE =
NOT_CLAIMED

UNRECORDED_HUMAN_COGNITION =
NOT_SOLVED

DISHONEST_DECLARATION =
NOT_SOLVED

UNKNOWN_UNKNOWN_EXPOSURE =
NOT_SOLVED
```

These limits are preserved explicitly. This design improves provenance, reconstructibility and contestability; it does not claim exhaustive capture of human cognition or all unknown exposures.

---

## 5. Explicit non-authorizations

This adjudication does not authorize:

```text
IMPLEMENTATION
RUNTIME_CHANGE
P1_MODIFICATION
SFE_MODIFICATION
MEMORY_ENGINE_MODIFICATION
DECISION_MODIFICATION
BACKTEST
PERFORMANCE_OBSERVATION
STRATEGY_CHANGE
AUTOMATIC_AUTHORITY
AUTOMATIC_PROMOTION
AUTOMATIC_N_BUDGET
AUTOMATIC_N_FAMILLE
```

No implementation, runtime path, scientific experiment, performance observation, strategy behavior or authority surface is opened by this artifact.

---

## 6. Only possible next frontier from this adjudication

The only downstream frontier created as a **candidate requiring separate human authorization** is:

```text
IMPLEMENTATION CONTRACT V0.1
— MINIMAL CROSS-EXPERIMENT PROVENANCE REGISTRY
```

If separately authorized, that future contract must remain:

```text
MINIMAL
TEST_FIRST
FAIL_CLOSED
DELTA_ONLY
NO_RUNTIME_COUPLING
NO_AUTHORITY_EXPANSION
```

This G6 adoption does not itself open that implementation contract.

---

## 7. STOP

```text
G6 =
HUMAN_ADOPTED_FOR_SEMANTIC_DESIGN_ONLY

IMPLEMENTATION =
NOT_AUTHORIZED

NEXT_FRONTIER =
IMPLEMENTATION CONTRACT V0.1
REQUIRES SEPARATE HUMAN AUTHORIZATION

STOP =
TRUE
```
