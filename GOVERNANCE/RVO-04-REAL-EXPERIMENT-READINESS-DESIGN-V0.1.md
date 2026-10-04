# RVO-04 — REAL-EXPERIMENT READINESS DESIGN

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Mode:** `DESIGN / ROUTING / NO REAL EXPERIMENT`  
**RVO authority:** `NONE`

## 1. Bound RVO-04 design identities

```text
CLAIM_CLASS_TAXONOMY_BLOB =
1fa07fb4b262bfc2a867e66914ce4221cdcd1f79

CLAIM_CAPABILITY_GRAPH_BLOB =
fcd723a30bad063471d7a399c06464b580c87e77

OWNER_GAP_PRIORITIZATION_BLOB =
4c5720b593fc8e955103c55b9ab37b5e6c3e83da

SOURCE_RVO03_CAPABILITY_MATRIX_BLOB =
5f2406189af8e118ca8f20f5a7f92f3a2ce91c13
```

These artifacts are design objects. They do not authorize owner modification, real experiment execution, backtesting, OOS consumption, performance observation, trading, broker interaction or capital use.

## 2. Main finding

There is no single meaningful answer to:

> “Is RVO ready for a real experiment?”

Readiness is claim-scoped.

A protocol-only claim, a retrospective descriptive market claim, a predictive claim, a net-profitability claim, a path-risk claim and an OOS confirmation do not require the same owner capabilities.

Therefore:

```text
CLAIM-SCOPED READINESS
>
GLOBAL "RVO READY" BOOLEAN
```

and:

```text
CAPABILITY DESIRED
!=
CAPABILITY REQUIRED
```

## 3. Claim classes

RVO-04 freezes ten design classes:

```text
CC01 STRUCTURAL / PROTOCOL
CC02 DESCRIPTIVE MARKET BEHAVIOR
CC03 STATISTICAL EFFECT
CC04 PREDICTIVE
CC05 ECONOMIC / NET PROFITABILITY
CC06 ROBUSTNESS / STABILITY
CC07 MULTIPLICITY / MODEL SELECTION
CC08 HISTORICAL POINT-IN-TIME
CC09 PATH-RISK / RUIN
CC10 OOS / PRISTINE CONFIRMATION
```

These are routing classes, not proof levels. A claim does not inherit authority by sounding stronger or by passing another class.

## 4. Current readiness by claim class

### CC01 — Structural / protocol

Current qualified building blocks are sufficient for a **future real protocol-only RVO application** using exact P1 specification identity and PCP evidence/identity controls, provided no market, predictive, historical-availability, economic or OOS claim is made.

```text
CAPABILITY_READINESS =
CONDITIONALLY_READY

REAL_USE_AUTHORITY =
NOT_AUTHORIZED
```

If the protocol claim must itself become a downstream P1 qualified experimental finding, the currently missing RVO binding to the downstream P1 chain must be closed first.

CC01 therefore proves an important negative result:

```text
DATA / TEMPORAL / EXECUTION
ARE NOT GLOBAL PREREQUISITES
FOR EVERY RVO CLAIM.
```

### CC02 — Descriptive market behavior

A first real empirical descriptive claim is **not yet ready**.

Primary blocker:

```text
DATA_EXACT_CLAIM_SURFACE =
AVAILABLE
NOT GENERICALLY QUALIFIED
```

The current executable Data surface is tick-CSV-specific. RVO-04 does not infer that it covers H1, parquet, transformed or derived datasets.

For a purely retrospective description, generic PIT is not necessarily required. If the claim implies historical knowability, decision-time availability or tradability, Temporal becomes required.

### CC03 — Statistical effect

Not ready for real execution.

Minimum blockers:

```text
CLAIM-SCOPED DATA QUALIFICATION
+
RVO P1 DOWNSTREAM BINDING
+
RVO SMF RESULT/PROCEDURE BINDING
```

Temporal becomes mandatory whenever the estimand depends on historical information availability. Execution becomes mandatory whenever the effect is defined on executable/net trading outcomes.

### CC04 — Predictive

Not ready.

Minimum unresolved surfaces:

```text
DATA
+
TEMPORAL / PIT
+
RVO P1 DOWNSTREAM BINDING
+
RVO SMF RESULT BINDING
```

MCEPR durable real provenance becomes required when search/model exposure is material. C11 becomes required only for probabilistic calibration/scoring claims; conditional SMF families are not activated merely because the claim is predictive.

### CC05 — Economic / net profitability

Not ready.

A genuine net-profitability claim requires:

```text
DATA
+
TEMPORAL
+
GENERIC CLAIM-SUFFICIENT EXECUTION / COST
+
SMF M02 AND OTHER APPLICABLE CORE CONTROLS
+
P1 / RVO RESULT BINDINGS
```

The qualified E1-04 runtime cannot be silently promoted to generic execution authority.

It explicitly leaves commission, slippage and financing excluded rather than zero and forbids all-in/broker-realism claims outside its qualified scope.

### CC06 — Robustness / stability

Not independently ready because robustness inherits the materially relevant prerequisites of the base claim.

```text
ROBUSTNESS
!=
A WAY TO BYPASS BASE-CLAIM REQUIREMENTS
```

M07/M10 are core candidates. C04/C05/C06 become relevant only when the exact selection/overfitting failure mode activates them.

### CC07 — Multiplicity / model selection

Not ready for a real claim requiring durable cross-experiment provenance.

The MCEPR runtime is qualified, but current canonical activation V0.2 still states:

```text
FUTURE PILOT NOT AUTHORIZED
REAL EVENT PERSISTENCE NOT AUTHORIZED
RUNTIME INTEGRATION NOT AUTHORIZED
```

Therefore:

```text
MCEPR RUNTIME QUALIFIED
!=
MCEPR REAL PERSISTENCE AUTHORIZED
```

SMF M11 is already CORE. C02/C03/C04/C05/C06 remain on-demand and must not be implemented as a blanket catalogue.

### CC08 — Historical point-in-time

Blocked.

```text
TEMPORAL_GENERIC_POINT_IN_TIME =
UNAVAILABLE
```

The current Temporal document is an architecture proposal / non-normative design. A historical-PIT claim therefore cannot be promoted through RVO by treating timestamps, dataset acquisition time or execution time as substitutes for knowledge availability.

### CC09 — Path-risk / ruin

Blocked.

At minimum, a strategy-policy path-risk claim needs:

```text
DATA
+
CLAIM-SUFFICIENT EXECUTION / POLICY
+
SMF CONDITIONAL C09
```

A Risk-of-Ruin claim additionally requires:

```text
C10
```

Those conditional methods are adopted method families but are not implemented by the current SMF-03 CORE integration.

### CC10 — OOS / pristine confirmation

Blocked.

At minimum:

```text
DATA
+
TEMPORAL
+
SMF M09 / M11 AS APPLICABLE
+
DURABLE SEARCH / EXPOSURE PROVENANCE
+
P1 / RVO DOWNSTREAM BINDING
+
SEPARATE HUMAN OOS CONSUMPTION AUTHORITY
```

Chronological lateness alone is not sufficient to establish pristine OOS.

## 5. Data decision

RVO-04 rejects the requirement to build a universal Data abstraction before any real use.

The correct requirement is narrower:

```text
THE EXACT DATA FAMILY / SCHEMA USED
BY THE FIRST REAL EMPIRICAL CLAIM
MUST BE QUALIFIED FOR THAT USE.
```

Therefore:

```text
GLOBAL GENERIC DATA LAYER BEFORE FIRST USE =
NOT REQUIRED

CLAIM-SCOPED DATA QUALIFICATION BEFORE EMPIRICAL USE =
REQUIRED
```

If the first empirical experiment uses tick CSV, the existing executable boundary is a strong starting point but still needs an explicit qualification/adoption surface for the intended RVO use.

If it uses H1/parquet/derived data, the tick-CSV boundary cannot be substituted.

## 6. Minimum Temporal maturation

RVO-04 does not recommend implementing all of the current Temporal proposal before first use.

The minimum claim-sufficient owner must establish, where relevant:

```text
- declared research mode
- decision/reference time
- world-validity time vs knowledge-availability time
- exact data vintage when revisions matter
- dependency closure through transformations
- UNKNOWN temporal predicate -> fail closed
- manual/model-selection temporal provenance when material
- execution time cannot retroactively enlarge historical knowledge
```

This minimum is mandatory before predictive, historical-PIT, OOS and historical economic claims that depend on decision-time information availability.

## 7. Minimum Execution maturation

Generic execution is not globally required.

It becomes mandatory when the claim is about net trading outcomes or policy-dependent path risk.

The minimum claim-sufficient execution owner must freeze:

```text
- signal-time / execution-time boundary
- causal fill search
- BID / ASK side
- gap / continuity behavior
- quantity / policy identity
- claim-required cost components
- excluded cost != zero
- forbidden claims when realism/cost coverage is incomplete
- reconstructible execution identity
```

E1-04 can only satisfy this requirement for an exact E1-scoped claim that stays inside E1-04's already qualified limits.

## 8. Conditional SMF decision

RVO-04 rejects blanket implementation of C01-C12.

Conditional families become owner work only when the selected claim activates them:

```text
C01  Expected Shortfall
     -> tail-loss claim

C02  Holm FWER
C03  BH FDR
     -> declared multiple-testing family requiring those controls

C04  PBO / CSCV
C05  Hansen SPA
C06  PSR / DSR / MTRL
     -> exact model-selection / backtest-overfitting / performance-selection failure modes

C07  Sequential-valid inference
     -> optional stopping / sequential monitoring

C08  Equivalence / negligibility
     -> equivalence or practically-negligible-effect claim

C09  Dependence-preserving path simulation
     -> path-distribution claim

C10  Risk of Ruin
     -> explicit ruin-probability claim

C11  Proper scoring / calibration
     -> probabilistic forecast claim

C12  Exact binomial / permutation
     -> exact binary/exchangeable structure when activated
```

## 9. MCEPR decision

MCEPR has two distinct states that must not be collapsed:

```text
MINIMAL REGISTRY IMPLEMENTATION =
QUALIFIED

REAL FORWARD PERSISTENCE =
NOT AUTHORIZED BY CURRENT CANONICAL ACTIVATION V0.2
```

RVO-04 therefore treats MCEPR as an activation/authority gap only for claims whose scientific interpretation materially depends on durable search/exposure provenance.

It is not a reason to block every protocol or descriptive claim.

## 10. RVO integration gaps

Two important gaps are not owner failures:

```text
RVO -> P1 DOWNSTREAM FINDING CHAIN
RVO -> SMF QUALIFIED RESULT / PROCEDURE OUTPUTS
```

P1 and SMF already own qualified surfaces.

RVO-03 bound P1 specification and SMF activation, but it did not yet demonstrate an end-to-end RVO binding across the downstream real experiment/evaluation/finding and statistical-result surfaces.

Those future adapters must remain RVO-only.

```text
RVO MAY ADAPT TO OWNER.
RVO MUST NOT MODIFY OWNER TO MAKE INTEGRATION PASS.
```

## 11. Recommended maturation order

For a meaningful first empirical market experiment, the recommended order is:

```text
1. SELECT EXACT FIRST CLAIM CLASS + EXACT FIRST DATA FAMILY

2. DATA-01
   CLAIM-SCOPED DATA ADMISSIBILITY / PROVENANCE QUALIFICATION

3. RVO-ONLY
   DOWNSTREAM P1 + SMF RESULT BINDINGS
   SYNTHETIC-FIRST

4. TEMPORAL-01
   only if the selected claim requires historical/predictive/PIT semantics

5. MCEPR REAL-PERSISTENCE ACTIVATION
   only if search/exposure provenance is material

6. EXECUTION-01
   only if the selected claim asserts economic/net or policy-path outcomes

7. SMF Cxx
   only for the exact conditional method activated by the claim

8. READINESS REQUALIFICATION

9. SEPARATE HUMAN REAL-EXPERIMENT AUTHORIZATION

10. OOS AUTHORIZATION
    separately and only if CC10 is reached
```

## 12. Recommended first owner-specific frontier

The broadest common unresolved owner dependency for meaningful empirical claims is Data.

Therefore the recommended first owner-specific frontier is:

```text
DATA-01
— FIRST-USE DATA SURFACE SELECTION
— CLAIM-SCOPED ADMISSIBILITY
— PROVENANCE / LINEAGE MINIMUM
— IMMUTABLE RESULT-BINDING CONTRACT
— TEST-FIRST QUALIFICATION DESIGN
```

This frontier should not attempt to implement every dataset type.

Its first task is to freeze the exact dataset family required by the selected first empirical claim and qualify only what that claim needs.

## 13. Readiness verdict

```text
FIRST REAL RVO PROTOCOL-ONLY APPLICATION =
CAPABILITY_CONDITIONALLY_READY
REAL_USE_AUTHORITY_NOT_GRANTED

FIRST REAL EMPIRICAL DESCRIPTIVE CLAIM =
BLOCKED_BY_DATA_QUALIFICATION
+ RVO_DOWNSTREAM_BINDING_AS_REQUIRED

FIRST REAL PREDICTIVE CLAIM =
BLOCKED_BY_DATA
+ TEMPORAL
+ RVO_P1/SMF_RESULT_BINDING
+ CLAIM-SPECIFIC_PROVENANCE

FIRST REAL ECONOMIC CLAIM =
BLOCKED_BY_DATA
+ TEMPORAL
+ GENERIC_EXECUTION
+ RVO_P1/SMF_RESULT_BINDING
+ CLAIM-SPECIFIC_PROVENANCE

FIRST REAL PATH-RISK / RUIN CLAIM =
BLOCKED_BY_DATA
+ EXECUTION/POLICY
+ SMF_C09/C10_AS_REQUIRED

FIRST REAL OOS CONFIRMATION =
BLOCKED_BY_DATA
+ TEMPORAL
+ MCEPR/SEARCH_PROVENANCE
+ RVO_P1/SMF_RESULT_BINDING
+ SEPARATE_OOS_AUTHORITY
```

## 14. Authority boundary and STOP

```text
RVO_AUTHORITY =
NONE

OWNER_MODIFICATION =
NONE

REAL_EXPERIMENT =
NONE

REAL_BACKTEST =
NONE

REAL_PERFORMANCE_OBSERVATION =
NONE

OOS_CONSUMPTION =
NONE

PAPER / BROKER / LIVE / CAPITAL =
NONE

RVO-05 =
NOT_AUTHORIZED
```

RVO-04 stops at readiness design and owner-gap prioritization.
