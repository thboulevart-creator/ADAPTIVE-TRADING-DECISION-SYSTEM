# ATDS-AO-00 V0.2 — TARGETED DELTA CONTRACT

**Candidate revision:** `R2.1 — GLM non-blocking clarifications + RVO-04 read-only reconciliation`  

## 0. STATUS / AUTHORITY

```text
DOCUMENT =
ATDS-AO-00 V0.2 — TARGETED DELTA CONTRACT

STATUS =
PRE-ADOPTION / NON-CANONICAL CANDIDATE

MODE =
DOCUMENTARY CONSTRUCTION ONLY

REPOSITORY MUTATION =
NOT AUTHORIZED

CANONICAL PERSISTENCE =
NOT AUTHORIZED

HUMAN ADOPTION =
NOT CLAIMED

AO-E0 EXECUTION =
NOT AUTHORIZED

REVIEW STATUS =
PRE-ADJUDICATION / NO SELF-DECLARED PASS

BACKTEST / PERFORMANCE OBSERVATION =
NOT AUTHORIZED

PAPER / BROKER / MT5 / LIVE / CAPITAL =
CLOSED
```

This contract is a targeted delta over existing ATDS governance.

It must not duplicate an existing canonical owner where the required responsibility already exists.

---

# 1. CANONICAL BINDING

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

GOVERNED_BRANCH =
integration/system-v1

ORIGINAL_DOCUMENTARY_AUTH_PARENT_HEAD =
1a6b4e3e62e37e1e5827abb14472f84d1aed9888

ORIGINAL_DOCUMENTARY_AUTH_PARENT_TREE =
d47bb260ead57fd3ee46da4eeed78e1246c816dc

CURRENT_READ_ONLY_RECONCILED_HEAD =
1a4ea7f19a4bdee0cd632f8f42adb40fa1f0fe86

CURRENT_READ_ONLY_RECONCILED_TREE =
b84b4a8538be3eb4a34d81665202e217cf3c483f

CURRENT_HEAD_DELTA_FROM_ORIGINAL_PARENT =
11 COMMITS / RVO-ONLY ADDITIONS OBSERVED

CANONICAL_PERSISTENCE_ON_CURRENT_HEAD =
NOT AUTHORIZED
```

Reconciliation source:

```text
AO-RC-01 — CANONICAL RECONCILIATION CLOSURE V0.1

SHA256 =
81a2ffdcabe3c8eab131e9c364cb6d7c11278b451334e15a1d6e3af24e1c4df0
```

This V0.2 originated from that exact reconciliation surface.

R2.1 additionally performs a read-only reconciliation against the current canonical state:

```text
HEAD =
1a4ea7f19a4bdee0cd632f8f42adb40fa1f0fe86

TREE =
b84b4a8538be3eb4a34d81665202e217cf3c483f
```

Observed delta from the original documentary parent:

```text
11 COMMITS
ALL OBSERVED CHANGES = RVO SURFACES ADDED
ORIGINAL V0.2 OWNER BLOBS = UNCHANGED
```

The latest two commits after the R2 reconciliation add only RVO-04 claim-routing/readiness surfaces.

Review provenance used for R2.1:

```text
INTERNAL_R1_REVIEW =
ATDS-AO-00_V0.2_INTERNAL_ADVERSARIAL_REVIEW_R1.md
SHA256 =
11dfd48f50935a6f915fadb400c94ae34dfe17cc3fb2d7fb1f6db1ed257f2042
STATUS =
LOCAL / NON-CANONICAL

EXTERNAL_DELTA_REVIEW_1 =
CLAUDE REVIEW PROVIDED 2026-10-04
SHA256 =
5080e0882209c74bb7488adbdf1fc7cf800fcb273c24c64b07105536f4b4cd31
STATUS =
EXTERNAL EVIDENCE / NON-CANONICAL

EXTERNAL_DELTA_REVIEW_2 =
GLM REVIEW PROVIDED 2026-10-04
SHA256 =
0cb00045bd41a5e11f46c5c8c42f71cb788f2fdf013722a5f5e72a1f61311edb
STATUS =
EXTERNAL EVIDENCE / NON-CANONICAL
VERDICT =
NO BLOCKING FINDINGS
```

Neither review artifact grants authority.

If any materially referenced canonical dependency changes after the current read-only reconciliation, V0.2 must be re-reconciled again before persistence or adoption.

---

# 2. PRIMARY PURPOSE

V0.2 does not define a new AO governance stack.

Its purpose is only to close the minimum semantic gaps confirmed by AO-RC-01 while explicitly reusing existing ATDS authorities and contracts.

Core rule:

```text
EXISTING CANONICAL OWNER
≠
AO DUPLICATE
```

and:

```text
TARGET ARCHITECTURE
≠
BUILD AUTHORITY
```

---

# 3. EXISTING CANONICAL OWNERS — REUSED, NOT REDEFINED

The following responsibilities remain owned by existing ATDS artifacts.

## 3.1 Human / policy authority

Canonical owner:

```text
04-REFERENCE/
ALGO-ECOSYSTEM-METHODOLOGIE-GOUVERNANCE-V1.md

BLOB =
f8c693b9d56c3749b6a4f9c7fda799a84ffcbc7b
```

AO inherits:

```text
HUMAN NORMATIVE AUTHORITY
MULTI-MODEL REVIEW ≠ NORMATIVE AUTHORITY
CONTESTER ≠ MODIFIER ≠ ARBITRER
NON-DRIFT OF RESPONSIBILITIES
```

AO creates no separate policy-authority subsystem.

---

## 3.2 Promotion / authority increase

Canonical owner:

```text
04-REFERENCE/PROMOTION-GATE-CONTRACT.md

BLOB =
1265c4fca142f278e41d7d20a33d2f6ee9999ed7
```

AO inherits:

```text
EVIDENCE ≠ AUTHORITY
READINESS ≠ PROMOTION
UNKNOWN / AMBIGUOUS ≠ PASS
PERMISSION INCREASE REQUIRES EXPLICIT GATE
```

AO does not redefine promotion semantics.

---

## 3.3 Decision → Action authorization

Canonical owner:

```text
04-REFERENCE/
DECISION-ACTION-AUTHORIZATION-BOUNDARY-CONTRACT.md

BLOB =
7a77a37a961e8830988ca878cfce9e3fe61eb2ff
```

AO inherits:

```text
DECISION EXISTENCE ≠ ACTION AUTHORITY
AUTHORIZED ≠ EXECUTE
RECONSTRUCTION ≠ AUTHENTIC ADMISSIBILITY
CALLER-DECLARED AUTHORIZATION ≠ PROOF
```

The positive ACTION path remains governed by P1.1 and is not opened here.

---

## 3.4 System reproducibility

Canonical owners:

```text
04-REFERENCE/SYSTEM-REPRODUCIBILITY-CONTRACT.md
BLOB =
0e9d50afc6160aafc66fe625b836f43e71c00c46
```

and:

```text
GOVERNANCE/
E1-07-EXACT-PREFLIGHT-REPRODUCIBILITY-TRACE-CONTRACT-V0.1.json

BLOB =
b19f9b5a4505f50d77f1cbd09b2b6381241b5205
```

AO must reuse the existing exact binding pattern for:

```text
REPOSITORY
BRANCH
HEAD
TREE
STRATEGY IDENTITY
DATA IDENTITY
DATA HASHES
WINDOW
OOS
EXECUTION/COST MODEL
RUNNER
QUALIFICATION IDENTITY
ENVIRONMENT
DEPENDENCIES
RESULT SCHEMA
TRACE
```

No separate AO reproducibility framework is authorized.

---

## 3.5 Cross-experiment provenance

Canonical semantic owner:

```text
GOVERNANCE/
G6-MINIMAL-CROSS-EXPERIMENT-PROVENANCE-REGISTRY-HUMAN-ADJUDICATION-2026-10-02.md

BLOB =
93e3c87f24b8933fbdfe25b1806d42233b6ec328
```

Qualified implementation:

```text
src/mcepr_registry.py

BLOB =
e5d5e2bace6a352c01f68cab77bea23b55b293b8
```

AO inherits:

```text
CONTENT-BOUND EVENT IDENTITY
PARENT-LINKED CHAIN
IMMUTABLE DECISIVE REFERENCES
EXPLICIT SUPERSESSION
FORK = BLOCKED
REGISTRY ≠ SCIENTIFIC TRUTH
REGISTRY ≠ OPERATIONAL AUTHORITY
MISSING RECORD ≠ EVENT DID NOT OCCUR
```

Observed at the authorized parent:

```text
MCEPR FORWARD CUTOVER RECORD =
PRESENT

CANONICAL MCEPR SEGMENTS =
0
```

Therefore AO may not claim that the existing ledger already contains the AO research history or that an AO event can already be appended under this V0.2 authority.

AO must reuse MCEPR if and when its recording/admission path is separately authorized.

No second AO research ledger is permitted.

---

## 3.6 No-trade principle

Canonical design owner:

```text
04-REFERENCE/
PRINCIPES-TRANSVERSAUX-ALGORITHMES.md

BLOB =
168b845ef61df63a28cb7cd607f6a16a1e75fb97
```

AO inherits:

```text
NO TRADE
=
VALID DECISION
```

AO does not create a duplicate abstention doctrine.

---

## 3.7 Validation orchestration (RVO)

Current canonical RVO owners added after the original AO parent:

```text
GOVERNANCE/
RVO-THIN-ORCHESTRATOR-TARGET-ARCHITECTURE-R1-HUMAN-ADJUDICATION-2026-10-04.md

BLOB =
d83685b23938b4b7baa9ab098416aa1e1178ab67
```

```text
GOVERNANCE/
RVO-03-CANONICAL-OWNER-CAPABILITY-MATRIX-V0.1.json

BLOB =
5f2406189af8e118ca8f20f5a7f92f3a2ce91c13
```

```text
src/rvo_orchestrator.py

BLOB =
20766da0d609d0056e40df0115a3151d5c703938
```

RVO owns non-authoritative validation orchestration:

```text
ROUTING OF VALIDATION CONTROLS
OWNER BINDING
VALIDATION-PACKAGE ASSEMBLY
PACKAGE COMPLETENESS / RECONSTRUCTIBILITY
```

and explicitly owns no:

```text
SCIENTIFIC AUTHORITY
OPERATIONAL AUTHORITY
TRADING AUTHORITY
CAPITAL AUTHORITY
OWNER SEMANTICS
```

Naming invariant:

```text
RVO ORCHESTRATOR
=
VALIDATION ORCHESTRATION

AO STRATEGY ROUTER
=
FUTURE STRATEGY-SELECTION / ROUTING RESPONSIBILITY

RVO ORCHESTRATOR
≠
AO STRATEGY ROUTER
```

AO must not use the generic word `ORCHESTRATOR` without a qualifier when the referent could be ambiguous.

Evidence-package interface:

```text
AO DOES NOT DEFINE
A COMPETING VALIDATION-PACKAGE SCHEMA.
```

When RVO is applicable to an AO qualification, the exact RVO validation-package digest may be referenced as decisive qualification evidence. RVO package completeness does not itself qualify a strategy cell.

Current RVO-04 claim-routing/readiness artifacts at the R2.1 reconciliation state:

```text
GOVERNANCE/RVO-04-CLAIM-CLASS-TAXONOMY-V0.1.json
BLOB =
1fa07fb4b262bfc2a867e66914ce4221cdcd1f79

GOVERNANCE/RVO-04-CLAIM-CAPABILITY-GRAPH-V0.1.json
BLOB =
fcd723a30bad063471d7a399c06464b580c87e77

GOVERNANCE/RVO-04-OWNER-GAP-PRIORITIZATION-V0.1.json
BLOB =
4c5720b593fc8e955103c55b9ab37b5e6c3e83da

GOVERNANCE/RVO-04-REAL-EXPERIMENT-READINESS-DESIGN-V0.1.md
BLOB =
3f6875e1a1a1aa36396d10c43eae25478963a48a

reports/program/2026-10-04-RVO-04-CLAIM-ROUTING-READINESS-QUALIFICATION.md
BLOB =
60dc4b5717e629d1d50361b46d3ddda8f079076b
```

RVO-04 adds claim-scoped readiness routing only. It grants:

```text
RVO_AUTHORITY =
NONE

REAL_EXPERIMENT =
NOT_AUTHORIZED

OOS_CONSUMPTION =
NOT_AUTHORIZED
```

For the future AO-E0 economic/OOS path, RVO-04 makes visible additional prerequisites such as exact first-use data qualification and separate OOS authority. These are readiness blockers, not new AO deltas.

---

# 4. IMPORTANT NON-NORMATIVE OWNER

The following existing artifact is semantically relevant but not yet normative:

```text
docs/10-TEMPORAL-POINT-IN-TIME-CONTRACT.md

BLOB =
861362264a3602aa875bb16487d12558f700c250
```

It already defines:

```text
WORLD VALIDITY
KNOWLEDGE AVAILABILITY
PERMITTED USE
EXECUTION TIME
DECISION TIME
VINTAGE
PUBLICATION / AVAILABILITY
REVISION
PIPELINE LOOK-AHEAD
PARAMETER LOOK-AHEAD
MANUAL HINDSIGHT LABELS
```

AO rule:

```text
AO MUST NOT CREATE
A PARALLEL TEMPORAL SEMANTICS MODEL
```

But:

```text
NON-NORMATIVE TEMPORAL PROPOSAL
≠
CANONICAL POINT-IN-TIME AUTHORITY
```

Any AO claim requiring historical point-in-time admissibility remains dependent on a governed admissibility path sufficient for that exact claim.

This does not automatically require promotion of the entire temporal proposal as one monolithic prerequisite; a narrower already-qualified or separately governed path may be sufficient if it closes the relevant temporal failure modes without semantic duplication.

---

# 5. DELTA-1 — GENERIC STRATEGY-VERSION IDENTITY

## 5.1 Problem

E1 already freezes a precise identity for `MOMENTUM_V1`, but ATDS lacks a generic AO-level rule defining what constitutes the same or a different strategy version across future algorithms.

## 5.2 Required abstraction

```text
STRATEGY_VERSION_IDENTITY
```

must bind at minimum:

```text
ALGORITHM / STRATEGY ID
CODE IDENTITY
MATERIAL PARAMETER IDENTITY
MATERIAL CONFIGURATION IDENTITY
DECLARED INPUT / INTERFACE IDENTITY
```

where applicable.

## 5.3 Material-change invariant

```text
MATERIAL IDENTITY CHANGE
→
NO AUTOMATIC QUALIFICATION TRANSFER
```

Default rule:

```text
ANY CHANGE TO
CODE
PARAMETERS
MATERIAL CONFIGURATION
OR DECLARED INTERFACE
=
MATERIAL
FOR QUALIFICATION-TRANSFER PURPOSES
```

unless a separate governed decision adjudicates that the exact change is immaterial to the qualification claim.

The author of the change may propose immateriality but may not self-declare it.

Therefore:

```text
IMMATERIALITY CLAIM
≠
SELF-AUTHORIZING QUALIFICATION TRANSFER
```

A strategy-specific materiality policy may later narrow this conservative default only through explicit governed adjudication.

## 5.4 Non-goal

V0.2 does not prescribe one universal hash format.

It defines the semantic ownership requirement only.

---

# 6. DELTA-2 — STRATEGY QUALIFICATION CELL

## 6.1 Problem

A global:

```text
ALGORITHM = QUALIFIED
```

can silently transfer evidence between materially different domains.

## 6.2 Required unit

The minimum qualification object is:

```text
STRATEGY_QUALIFICATION_CELL
```

bound to:

```text
STRATEGY_VERSION_IDENTITY
QUALIFICATION_CLAIM_IDENTITY
ASSET / INSTRUMENT IDENTITY
TIMEFRAME / HORIZON
EXECUTION MODEL IDENTITY
COST SCOPE IDENTITY
MATERIAL CONTEXT-DOMAIN IDENTITY
```

Each candidate domain dimension must have an explicit scope mode:

```text
EXPLICIT
FIXED_BY_EVIDENCE
NOT_MATERIAL
```

Default:

```text
OMITTED / UNRESOLVED DIMENSION
→
FIXED_BY_EVIDENCE
```

`NOT_MATERIAL` requires a governed adjudication with stated rationale; it cannot be inferred from omission.

The specific dataset, window, OOS partition, test run and evidence package are NOT part of the semantic cell identity. They belong to the qualification evidence / decision record so that the same cell can accumulate, supersede or contest evidence without silently becoming a different cell.

For the first `MOMENTUM_V1` AO-E0 candidate:

```text
CONTEXT_ROUTING =
NONE

CONTEXT_DOMAIN_CLAIM =
NO UNIVERSAL CONTEXT TRANSFER CLAIM

CONTEXT_SCOPE_MODE =
FIXED_BY_EVIDENCE
```

This means AO-E0 is not context-routed and does not qualify MOMENTUM_V1 across unobserved or materially different contexts merely because no context gate is used.

## 6.3 Domain semantics

AO must distinguish:

```text
CLAIMED_DOMAIN
```

from:

```text
QUALIFIED_DOMAIN
```

Invariant:

```text
QUALIFIED_IN_CELL_A
≠
QUALIFIED_IN_CELL_B
```

unless a separate transportability claim has itself been qualified.

## 6.4 Unknown domain

If the relation between two cells is unknown:

```text
TRANSFER_STATUS =
UNKNOWN
```

not:

```text
ASSUMED_EQUIVALENT
```

---

# 7. DELTA-3 — QUALIFICATION EVIDENCE ≠ QUALIFICATION DECISION

## 7.1 Separation

```text
EVALUATION
→
PRODUCES EVIDENCE

QUALIFICATION DECISION
→
ADJUDICATES THE EVIDENCE

REGISTRY
→
RECORDS THE DECISION + SCOPE + REFERENCES
```

## 7.2 Minimum qualification-decision record

A future record must bind at minimum:

```text
QUALIFICATION_CELL_IDENTITY
STRATEGY_VERSION_IDENTITY
DECISIVE_EVIDENCE_REFS
EVIDENCE_SCOPE
DECISION
DECISION_AUTHORITY
DECIDED_AT
APPLICABLE POLICY VERSION
SUPERSESSION / INVALIDATION RELATION
```

The final vocabulary is not frozen by this candidate, but it must preserve at least two orthogonal fields:

```text
QUALIFICATION_STATUS
QUALIFICATION_REASON
```

Candidate status surface:

```text
QUALIFIED
NOT_QUALIFIED
UNDER_REVIEW
INVALIDATED
```

When:

```text
QUALIFICATION_STATUS =
NOT_QUALIFIED
```

the reason must preserve the evidence state, for example:

```text
REFUTED
INCONCLUSIVE
INSUFFICIENT_EVIDENCE
OUT_OF_SCOPE
```

Critical epistemic invariant:

```text
INCONCLUSIVE EVIDENCE
≠
QUALIFIED

INCONCLUSIVE EVIDENCE
≠
REFUTED
```

The qualification-decision layer must preserve uncertainty rather than force every evidence package into a binary pass/fail interpretation.

When RVO is applicable, the exact RVO validation-package digest may appear in `DECISIVE_EVIDENCE_REFS`; AO does not create a second validation-package schema.

## 7.3 Authority

The evidence producer cannot self-promote the candidate merely because tests passed.

The qualification decision must remain bound to existing human/promotion governance.

---

# 8. DELTA-4 — ELIGIBILITY ≠ PORTFOLIO CONSTRUCTION ≠ RISK AUTHORITY ≠ EXECUTION

AO introduces four distinct logical responsibilities.

## 8.1 Strategy eligibility

Question:

```text
IS THIS QUALIFIED STRATEGY CELL
ADMISSIBLE UNDER THE CURRENT
EVIDENCE / CONTEXT / POLICY?
```

Eligibility produces no capital amount and no market action.

## 8.2 Portfolio construction

Question:

```text
HOW SHOULD THE CURRENTLY ADMISSIBLE
STRATEGY CELLS BE COMBINED,
IF AT ALL?
```

This is the only logical responsibility that may own portfolio-weight proposals and diversification objectives.

## 8.3 Risk authority

Question:

```text
IS THE PROPOSED JOINT EXPOSURE
PERMITTED UNDER HARD RISK CONSTRAINTS?
```

Risk may:

```text
APPROVE
REDUCE
VETO
```

under pre-governed rules.

Risk must not invent a new alpha thesis and must not substitute another strategy.

If a risk reduction, veto, a governed qualification-status change away from `QUALIFIED` (including `UNDER_REVIEW` or `INVALIDATED`), or another loss of eligibility frees risk budget:

```text
FREED BUDGET
=
UNALLOCATED
```

until a new governed portfolio-construction decision allocates it.

If a risk reduction or veto makes the proposed portfolio infeasible, any alternative allocation must return to the governed portfolio-construction policy rather than being invented inside Risk.

## 8.4 Execution

Question:

```text
WHAT MARKET ACTION
IS REQUIRED BY THE
EXACT AUTHORIZED INTENT?
```

Execution owns actual action/fill/position effects when that future path is qualified.

## 8.5 No physical decomposition implied

```text
LOGICAL RESPONSIBILITY
≠
SERVICE
≠
PROCESS
≠
REPOSITORY
```

V0.2 authorizes no new runtime component.

---

# 9. DELTA-5 — SELECTION ≠ TRANSITION

## 9.1 Problem

A preference change:

```text
A → B
```

must not silently imply:

```text
CLOSE A NOW
+
OPEN B NOW
```

## 9.2 Required distinction

```text
SELECTION_DECISION
```

answers:

```text
WHICH ELIGIBLE STRATEGY CELL
SHOULD BE PROPOSED FOR
NEW EXPOSURE / ALLOCATION?
```

Selection does not grant capital authority. Final permission remains downstream of portfolio construction and Risk authorization.

while:

```text
TRANSITION_DECISION
```

answers:

```text
HOW SHOULD EXISTING POSITIONS /
EXPOSURES BE MOVED,
IF AT ALL?
```

## 9.3 Transition evidence

A future transition decision may need to consider:

```text
OPEN POSITIONS
UNWIND COST
SPREAD
SLIPPAGE
MARKET IMPACT
OPPORTUNITY COST
FINANCING
UNCERTAINTY
EXPECTED PERSISTENCE
RISK
```

depending on strategy and venue.

## 9.4 Build status

```text
TRANSITION IMPLEMENTATION =
CLOSED
```

until multiple qualified strategy cells and a real transition problem exist.

---

# 10. DELTA-6 — UNCOVERED STATE ≠ RESEARCH-WORTHY GAP

## 10.1 First distinction

```text
UNCOVERED_STATE
```

means only:

```text
NO CURRENT QUALIFIED STRATEGY CELL
COVERS THIS DECLARED CONTEXT
```

It is a property of the current partition + registry.

It is not yet evidence of an economic opportunity.

## 10.2 Research-worthy gap

A future:

```text
RESEARCH_WORTHY_GAP
```

requires separate evidence.

Candidate minimum properties:

```text
POINT-IN-TIME IDENTIFIABLE
ROBUST TO REASONABLE CONTEXT DEFINITIONS
RECURRING ACROSS DISTINCT EPISODES
REPRESENTS A SPECIFIC MARKET BEHAVIOR
TRADEABLE
PLAUSIBLY ECONOMICALLY MATERIAL
FALSIFIABLE HYPOTHESIS AVAILABLE
BOUNDED RESEARCH BUDGET AVAILABLE
SEPARATE AUTHORITY OPENS RESEARCH
```

These properties are candidate semantics, not yet a qualified detector.

## 10.3 Build status

```text
COVERAGE ENGINE =
CLOSED

FACTORY TRIGGER =
CLOSED
```

until AO-E5.

---

# 11. NON-DELTA SEMANTIC CLARIFICATION — EDGE / EXPECTANCY

AO adopts the corrected terminology:

```text
MARKET BEHAVIOR
STATISTICAL PATTERN
ANOMALY
CONTEXT SIGNAL
```

may exist before a trading policy.

But:

```text
TRADING EDGE / EXPECTANCY
```

must be relative to a specified:

```text
STRATEGY
ASSET
HORIZON
ENTRY / EXIT
EXECUTION
COST SCOPE
RISK / EXPOSURE RULE
```

Therefore:

```text
MARKET OPPORTUNITY
≠
QUALIFIED STRATEGY EDGE
```

This constraint is a direct semantic corollary of Delta-2 (qualification-cell binding) and Delta-3 (evidence/decision scope). It is not an independent seventh delta.

---

# 12. CURRENT EXECUTION / COST LIMIT

Canonical cost owner:

```text
GOVERNANCE/
E1-04-EXECUTION-COST-MODEL-CONTRACT-V0.1.json

BLOB =
cf07f1400af614fa53fe41afe8a40e412d28c87d
```

Current included cost:

```text
RAW BID / ASK SPREAD
```

Current excluded-but-not-zero costs:

```text
COMMISSION
SLIPPAGE
FINANCING
```

Therefore:

```text
CURRENT E1-04 SCOPE
CANNOT AUTHORIZE THE CLAIM
ALL_IN_NET_PROFITABILITY
```

AO-E0 must declare its estimand exactly.

Two candidate future routes exist:

```text
A.
LIMITED-SCOPE EXPECTANCY
UNDER E1-04 COST SCOPE

OR

B.
EXTEND COST / EXECUTION EVIDENCE
BEFORE FULL NET-EXPECTANCY CLAIM
```

V0.2 does not choose between A and B.

Interpretation asymmetry:

```text
POSITIVE RESULT UNDER ROUTE A
≠
ALL-IN ECONOMIC QUALIFICATION
```

A negative or immaterial Route-A result may serve as a cheap kill-test for fuller net expectancy only if the excluded cost components are separately governed as incapable of contributing enough positive PnL to reverse that conclusion.

Without such a bound:

```text
NEGATIVE SPREAD-ONLY RESULT
≠
LOGICAL PROOF OF
NEGATIVE ALL-IN EXPECTANCY
```

because excluded financing, rebates, favorable execution effects or other unmodeled components have not been formally bounded by E1-04.

Therefore Route A may be used as a screening stage, but its exact support/refutation semantics must be preregistered.

The B5 decision remains human and is a blocker for AO-E0 preregistration.

---

# 13. EXISTING MOMENTUM_V1 BASE

Canonical frozen artifacts already establish:

```text
STRATEGY_ID =
MOMENTUM_V1

DATA SOURCE =
SOURCE_B_USTECH_PRICE_CORE_V0_1

TIMEFRAME =
H1

LOOKBACK =
20 COMPLETED ADMISSIBLE H1 BARS

PARAMETER OPTIMIZATION =
FORBIDDEN

OOS BOUNDARY =
FROZEN BEFORE MOMENTUM PERFORMANCE OBSERVATION
```

These artifacts establish experimental identity and reproducibility.

They explicitly do NOT establish:

```text
STRATEGY_QUALIFIED
EDGE_CONFIRMED
ROBUST
CONFIRMATORY_RESULT
CAPITAL_AUTHORIZED
```

Therefore:

```text
AO-E0
≠
DUPLICATION OF E1 READINESS
```

AO-E0 targets the missing economic qualification claim.

---

# 14. CONTEXT / REGIME STATUS

Existing CR1 evidence supports several exploratory `N0` context axes.

Here `N0` is the exploratory research level used by the canonical CR1 adjudication:

```text
reports/program/2026-09-26-CR1-CONTEXT-INFORMATIVENESS-ADJUDICATION.md

BLOB =
47d16c33ba80da75da7aac313a9885198ef89abb
```

`SUPPORTED_N0` means exploratory reproducible information under the declared CR1 protocol; it does not mean validated/OOS regime evidence.

It does not authorize:

```text
VALIDATED REGIME
CONFIRMED REGIME
OOS REGIME
STRATEGY-CONDITIONAL VALUE
PORTFOLIO ROUTING
```

Therefore:

```text
CR1 CONTEXT INFORMATIVENESS
≠
AO-E2 CONTEXT VALUE
```

Existing canonical owner status remains unchanged:

```text
PTA-003 — CONDITIONAL PORTFOLIO SELECTIVITY
STATUS IN OWNER =
PRINCIPE DE CONCEPTION
```

V0.2 does NOT reclassify that owner record.

Instead, V0.2 proposes the following owner-targeted interpretive amendment for future AO decision use:

```text
PTA-003 MUST NOT BE USED
AS ECONOMIC AUTHORITY
FOR CONTEXT GATING / ROUTING
UNTIL AO-E2 / AO-E3
OR EQUIVALENT EVIDENCE
SUPPORTS THE RELEVANT CLAIM.
```

This proposal requires the applicable human/owner adjudication before it can modify the canonical owner.

Until then:

```text
PTA-003 OWNER STATUS =
UNCHANGED

AO ECONOMIC ROUTING AUTHORITY FROM PTA-003 =
NONE
```

---

# 15. EXPERIMENTAL LADDER

The target architecture must remain subordinate to this evidence ladder.

## AO-E0 — Individual strategy-cell expectancy

Question:

```text
DOES ONE EXACT STRATEGY CELL
HAVE SUFFICIENTLY SUPPORTED
ECONOMIC EXPECTANCY
UNDER ITS DECLARED COST SCOPE?
```

Status:

```text
NEXT ECONOMIC FRONTIER
NOT OPENED HERE
```

## AO-E1 — Static portfolio value

Requires multiple AO-E0-supported cells, with dependence between them explicitly measured or bounded rather than assumed absent.

Question:

```text
DOES A SIMPLE STATIC COMBINATION
ADD VALUE OVER THE COMPONENTS?
```

## AO-E2 — Context decision value

Question:

```text
DOES POINT-IN-TIME CONTEXT
CHANGE CONDITIONAL STRATEGY VALUE
IN A MATERIAL AND REPRODUCIBLE WAY?
```

## AO-E3 — Dynamic strategy routing value

Question:

```text
DOES DYNAMIC ROUTING
ADD INCREMENTAL NET VALUE
OVER SIMPLE STATIC BASELINES?
```

## AO-E4 — Degradation / switching value

Question:

```text
DO DETECTORS / SWITCH RULES
ADD INCREMENTAL VALUE
BEYOND SIMPLE POLICIES?
```

## AO-E5 — Research-worthy gaps

Question:

```text
DO REAL, REPEATED,
ECONOMICALLY MATERIAL
UNCOVERED OPPORTUNITIES EXIST?
```

## AO-E6 — Factory justification

Question:

```text
DOES A STRUCTURED / AUTOMATED FACTORY
PRODUCE QUALIFIED RESEARCH VALUE
BETTER THAN A SIMPLER GOVERNED
RESEARCH PROCESS?
```

Each experiment must allow:

```text
SUPPORT
REFUTE
INCONCLUSIVE
```

and:

```text
INCONCLUSIVE
=
VALID STOP CONDITION
```

---

# 16. COMPONENT ACTIVATION STATUS

```text
GENERIC STRATEGY IDENTITY CONTRACT =
CANDIDATE DELTA

QUALIFICATION CELL =
CANDIDATE DELTA

QUALIFICATION DECISION RECORD =
CANDIDATE DELTA

ELIGIBILITY RESPONSIBILITY =
CANDIDATE DELTA

PORTFOLIO CONSTRUCTION RESPONSIBILITY =
CANDIDATE DELTA

RISK AUTHORITY RESPONSIBILITY =
REUSE / INTERFACE

SELECTION / TRANSITION DISTINCTION =
CANDIDATE DELTA
IMPLEMENTATION CLOSED

RESEARCH-GAP SEMANTICS =
CANDIDATE DELTA
ENGINE CLOSED

DYNAMIC STRATEGY ROUTER =
CLOSED

DEGRADATION AUTHORITY =
CLOSED

COVERAGE ENGINE =
CLOSED

ALGO FACTORY =
CLOSED

LEARNED ROUTING =
CLOSED

PAPER / BROKER / LIVE =
CLOSED
```

---

# 17. NON-DELTA CROSS-CUTTING CONTROL — SAFE-FAILURE INVARIANT

AO adopts the following cross-cutting invariant:

```text
UNKNOWN
STALE
UNAVAILABLE
CONFLICT
QUALIFICATION_STATUS != QUALIFIED
```

where `QUALIFICATION_STATUS != QUALIFIED` includes:

```text
NOT_QUALIFIED
UNDER_REVIEW
INVALIDATED
NO QUALIFICATION DECISION
```

These conditions must never silently become:

```text
ELIGIBLE
AUTHORIZED
ACTIVE
CAPITAL-INCREASING
```

Where the applicable existing ATDS owner already defines stronger fail-closed behavior, that stronger behavior controls.

---

# 18. NON-DELTA CROSS-CUTTING CONTROL — NON-TRANSFER INVARIANTS

```text
OBSERVATION
≠
INTERPRETATION

INTERPRETATION
≠
HYPOTHESIS

HYPOTHESIS
≠
EVIDENCE

EVIDENCE
≠
QUALIFICATION

QUALIFICATION
≠
CURRENT ELIGIBILITY

ELIGIBILITY
≠
PORTFOLIO WEIGHT

PORTFOLIO WEIGHT
≠
RISK AUTHORIZATION

RISK AUTHORIZATION
≠
EXECUTION

EXECUTION
≠
EXPECTED EXECUTION

RESULT
≠
CAUSAL VALIDATION

INCONCLUSIVE
≠
REFUTED
```

and:

```text
CREATION
≠
QUALIFICATION

QUALIFICATION
≠
ELIGIBILITY

SELECTION
≠
TRANSITION

UNCOVERED
≠
RESEARCH-WORTHY

CONTEXT CHANGE
≠
EDGE DECAY
```

---

# 19. NON-DELTA CROSS-CUTTING CONTROL — ANTI-DUPLICATION RULE

Before any future AO artifact is created, the responsible process must answer:

```text
DOES AN EXISTING CANONICAL OWNER
ALREADY DEFINE THIS SEMANTIC?
```

If YES:

```text
REFERENCE / EXTEND OWNER
```

If PARTIAL:

```text
TARGETED DELTA ONLY
```

If NO:

```text
NEW CONTRACT MAY BE PROPOSED
BUT REQUIRES SEPARATE AUTHORITY
```

---

# 20. NON-DELTA CROSS-CUTTING CONTROL — ANTI-INFINITE-ARCHITECTURE RULE

A future AO component may be activated only if it:

```text
1. PROTECTS AGAINST
   A DISTINCT MATERIAL FAILURE MODE

OR

2. CHANGES AN ECONOMIC /
   OPERATIONAL DECISION

OR

3. IS NECESSARY TO TEST
   AN ECONOMICALLY MATERIAL CLAIM
```

and it must have:

```text
ACTIVATION EVIDENCE
+
RETIREMENT / DEACTIVATION CONDITION
```

A component whose motivating claim is:

```text
REFUTED
```

or persistently:

```text
INCONCLUSIVE
```

must not survive merely because it already exists.

`PERSISTENTLY` is intentionally not assigned a universal numerical threshold by V0.2. Whether inconclusiveness is persistent enough to trigger retirement/deactivation requires explicit human adjudication with a stated rationale for that component and claim.

---

# 21. AO-E0 BLOCKERS

AO-E0 must not open until the following are resolved:

```text
B1 =
EXACT STRATEGY QUALIFICATION CELL IDENTITY

B2 =
QUALIFICATION DECISION RECORD SEMANTICS

B3 =
EXACT AO-E0 ESTIMAND

B4 =
ECONOMIC MATERIALITY RULE
TO BE DERIVED / PREREGISTERED

B5 =
COST SCOPE:
LIMITED E1-04
OR
EXTENDED COST MODEL

B6 =
POINT-IN-TIME ADMISSIBILITY PATH
SUFFICIENT FOR THE CLAIM

B7 =
MCEPR RECORDING / ADMISSION PATH
FOR AO-E0 PREREGISTRATION AND RESEARCH EVENTS

B8 =
AO-E0 PREREGISTRATION MUST BE
PERSISTED BEFORE ANY REAL
E1 OOS PERFORMANCE OBSERVATION
ON THE SAME STRATEGY CELL,
OR AO-E0 MUST EXPLICITLY USE
ONLY NEW FORWARD DATA AFTER
THAT OBSERVATION

B9 =
MULTIPLICITY FAMILY /
PRIOR-RESEARCH-EXPOSURE DECLARATION,
INCLUDING KNOWN PRE-CUTOVER ATTEMPTS
AND EXPLICIT UNKNOWN / UNRECORDED
PRE-CUTOVER SEARCH LIMITATIONS

B10 =
CLAIM-SCOPED DATA ADMISSIBILITY /
PROVENANCE QUALIFICATION FOR
THE EXACT FIRST-USE DATA FAMILY
CONSUMED BY AO-E0

B11 =
RVO CLAIM-CLASS / OWNER-BINDING
READINESS FOR THE EXACT AO-E0 CLAIM,
INCLUDING ANY REQUIRED DOWNSTREAM
P1 / SMF BINDING

B12 =
SEPARATE EXPLICIT HUMAN
OOS-CONSUMPTION AUTHORITY
IMMEDIATELY BEFORE ANY REAL
OOS PERFORMANCE OBSERVATION
```

B8 is an information-order firewall:

```text
AO-E0 DECISION RULE
MUST PRECEDE
THE PERFORMANCE RESULT
IT INTENDS TO USE
AS UNCONSUMED EVIDENCE.
```

The preferred economy-of-evidence path is to make the first real E1 performance run serve AO-E0 where the exact estimand, materiality rule, cost interpretation and qualification decision rule were frozen beforehand. This is not authorized by V0.2; it is a candidate future sequencing rule.

B9 does not assume MCEPR is historically complete. Absence of a pre-cutover registry record must not be interpreted as zero prior search.

B10 is derived from current RVO-04 readiness: the existing tick-CSV boundary cannot be substituted for an H1/derived-data claim merely because it is executable. The exact first-use data family must be qualified for the claim.

B11 preserves RVO as the validation-orchestration owner. AO does not reproduce RVO routing or package semantics.

B12 is distinct from B8:

```text
B8 =
INFORMATION-ORDER / PREREGISTRATION FIREWALL

B12 =
EXPLICIT AUTHORITY TO CONSUME OOS
```

Neither one implies the other.

No threshold is invented by V0.2.

---

# 22. R2.1 GLM REVIEW CLARIFICATIONS

GLM returned no blocking finding and identified five LOW / INFORMATIONAL clarifications.

R2.1 adjudicates them as follows:

```text
R2-F01 UNCERTAINTY TRANSITION =
ACCEPTED / AMBIGUOUS TERM REMOVED

R2-F02 N0 TERM =
ACCEPTED / CANONICAL CR1 REFERENCE + INLINE MEANING ADDED

R2-F03 UNQUALIFIED VOCABULARY =
ACCEPTED / ALIGNED TO QUALIFICATION_STATUS != QUALIFIED

R2-F04 PERSISTENTLY INCONCLUSIVE =
ACCEPTED / HUMAN-ADJUDICATED, NO UNIVERSAL NUMERIC THRESHOLD

R2-F05 EDGE SECTION AS NON-DELTA =
ACCEPTED / DECLARED DIRECT COROLLARY OF DELTA-2 + DELTA-3
```

GLM verdict:

```text
BLOCKING FINDINGS =
NONE

R2 HUMAN-ADOPTABLE AS SEMANTIC CONTRACT =
YES, SUBJECT TO HUMAN ADJUDICATION

NEW ARCHITECTURAL COMPONENT REQUIRED =
NO
```

No GLM finding or agreement grants adoption, persistence or execution authority.

---

# 23. R2 DELTA-REVIEW CORRECTIONS

R2 adjudicates the external delta-review findings as follows:

```text
D-01 OOS ORDERING =
ACCEPTED / B8 ADDED

D-02 INCONCLUSIVE VERDICT PRESERVATION =
ACCEPTED

D-03 MATERIALITY BURDEN =
ACCEPTED WITH CONSERVATIVE DEFAULT

D-04 OMITTED DOMAIN DIMENSION =
ACCEPTED WITH FIXED_BY_EVIDENCE DEFAULT

D-05 CURRENT RVO RECONCILIATION =
ACCEPTED

D-06 PTA-003 OWNER STATUS =
ACCEPTED / CHANGED TO OWNER-TARGETED AMENDMENT PROPOSAL

D-07 SPREAD-ONLY KILL TEST =
ACCEPTED ONLY CONDITIONALLY;
UNBOUNDED EXCLUDED COSTS PREVENT UNIVERSAL REFUTATION CLAIM

D-08 PRE-CUTOVER MULTIPLICITY =
ACCEPTED / B9 ADDED

D-09 RISK SUBSTITUTION =
ACCEPTED / RISK NEVER SUBSTITUTES

D-10 SELF-DECLARED REVIEW STATUS =
ACCEPTED / REMOVED
```

No finding above grants adoption or persistence authority.

---

# 24. V0.2 VERDICT

```text
ONE LOGICAL ATDS =
RETAIN

SECOND INDEPENDENT AO SYSTEM =
NOT JUSTIFIED

STATIC / DYNAMIC / HYBRID =
UNDECIDED

REGIME-BASED ROUTING =
UNPROVEN

ALGO FACTORY =
UNPROVEN / CLOSED

TARGETED AO DELTAS =
6

DUPLICATE GOVERNANCE BUILD =
FORBIDDEN

AO-E0 =
NEXT ECONOMIC FRONTIER
BUT NOT OPENED BY THIS CONTRACT
```

---

# 25. NON-AUTHORIZATIONS

This V0.2 candidate does not authorize:

```text
REPOSITORY WRITE
CANONICAL PERSISTENCE
HUMAN ADOPTION
AO-E0 EXECUTION
NEW BACKTEST
PNL OBSERVATION
PERFORMANCE INTERPRETATION
MCEPR POPULATION
TEMPORAL-CONTRACT PROMOTION
COST-MODEL EXTENSION
ORCHESTRATOR IMPLEMENTATION
PORTFOLIO ENGINE IMPLEMENTATION
DEGRADATION DETECTOR
COVERAGE ENGINE
FACTORY
PAPER
BROKER
MT5
LIVE
CAPITAL
```

---

# 26. NEXT GOVERNED FRONTIER

If this candidate survives review and human adjudication, the next frontier is not implementation of the Orchestrator.

The next frontier is:

```text
AO-E0 — ONE STRATEGY-CELL ECONOMIC QUALIFICATION
PRE-DRAFT / PREREGISTRATION
```

using `MOMENTUM_V1` as the current candidate only if the exact AO-E0 blockers are resolved under fresh canonical state.

Before AO-E0, a separate decision is required on the cost-scope question and the MCEPR recording path.

STOP.
