# SMF-02 — METHOD ACTIVATION & EXECUTABLE QUALIFICATION CONTRACT DESIGN V0.1 — HUMAN ADJUDICATION

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Status:** HUMAN ADOPTED WITH AMENDMENTS — CONTRACT SEMANTICS ONLY

## 1. Provenance of this persistence

This record canonically persists a human decision supplied in conversation before any SMF-02 artifact had been persisted on the governed branch.

It does not claim that a prior canonical SMF-02 blob or path existed at adoption time.

Fresh pre-persistence base:

```text
PRE_PERSISTENCE_HEAD =
88f6978a77e87bed4ccef0708cdde7bfbbf7e929

PRE_PERSISTENCE_TREE =
586bc319990d7f1e0c45b38d6e32a5cea7203765
```

## 2. Human decision

```text
SMF-02 V0.1 =
ADOPT_WITH_AMENDMENTS

ADOPTION_SCOPE =
CONTRACT_SEMANTICS_ONLY
```

The contract semantics apply to the M01-M11 CORE and C01-C12 CONDITIONAL method families adopted in SMF-01.

## 3. Pre-result activation invariant

Method activation must occur before exposure to the method result.

```text
ACTIVATION
↓
ASSUMPTIONS
↓
DATA COMPATIBILITY
↓
EXECUTION
↓
EVALUATION
```

A method may not be selected after seeing a favorable result.

```text
METHOD SHOPPING =
FORBIDDEN
```

## 4. Fail-closed state semantics

The design preserves distinct states including:

```text
ACTIVATED
NOT_APPLICABLE
BLOCKED
```

and explicitly:

```text
BLOCKED != NOT_APPLICABLE
```

Control validity is distinct from the substantive result of the claim being evaluated.

A valid control can produce adverse evidence. A favorable claim result does not make an invalid control valid.

## 5. Material parameter discipline

No materially consequential statistical parameter may be silently defaulted.

This includes, when applicable:

- estimator identity;
- lag set;
- significance or confidence level;
- multiplicity policy;
- resampling scheme;
- block length;
- simulation count;
- seed;
- null / benchmark / direction;
- effect-size threshold;
- stopping rule;
- trial-universe semantics.

Where multiple scientifically admissible specifications exist and the choice is material, human adjudication remains required.

## 6. Assumption routing

```text
NO IMPLICIT IID
```

An IID-dependent method cannot silently grant itself IID validity.

Assumptions must be explicit and their failure must propagate to the control state.

## 7. Search-universe discipline

```text
UNKNOWN SEARCH UNIVERSE
!=
N_TRIALS
```

A registry record count is not automatically a defensible search budget or trial count.

Unknown or partial search-universe status must remain unresolved rather than being converted into an invented multiplicity parameter.

## 8. Model-risk and numerical semantics

```text
NUMERICAL CONVERGENCE
!=
MODEL VALIDITY
```

A large number of simulations can reduce Monte-Carlo numerical error without validating the assumed model.

Exactness claims are valid only within the exact frozen contract and tested surface.

## 9. Contradictions

Material contradictions between prerequisites, assumptions, provenance, activation state or evidence semantics must fail closed.

They may not be averaged away through metric voting.

## 10. Explicit non-authorizations

This adoption does not authorize:

```text
AUTOMATIC METHOD ADOPTION
CODE
REAL BACKTEST
REAL PERFORMANCE OBSERVATION
OOS CONSUMPTION
STRATEGY MODIFICATION
SFE MODIFICATION
RISK ENGINE
PORTFOLIO ENGINE
SIZING POLICY
PAPER
BROKER
LIVE
CAPITAL
AUTOMATIC SCIENTIFIC PROMOTION
```

## 11. Historical next frontier

The only implementation frontier opened later by separate human authority was:

```text
SMF-03 — TEST-FIRST STATISTICAL IMPLEMENTATION
+ INDEPENDENT REFERENCE QUALIFICATION
```

SMF-02 did not itself authorize code.
