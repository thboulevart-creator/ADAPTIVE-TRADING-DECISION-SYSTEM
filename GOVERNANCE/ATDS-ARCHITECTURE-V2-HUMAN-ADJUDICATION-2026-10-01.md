# ATDS — PROGRAM ARCHITECTURE V2

## HUMAN ADJUDICATION — ADOPT WITH AMENDMENTS

Date: 2026-10-01

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Human decision supplied in conversation:

```text
DECISION = ADOPT_WITH_AMENDMENTS
DATE = 2026-10-01
```

This record persists the human architectural decision. It is not represented as independent cryptographic proof of human identity.

## 1. Persistence base

Fresh-verified immediately before persistence:

```text
PRE_PERSISTENCE_HEAD =
59f1dc26973b0b50efefccf12b26784d1e41f546

PRE_PERSISTENCE_TREE =
beb85ddb99e8a87afc4e8a6ed9b989ed0f83e1ea
```

The target path did not exist before this persistence.

## 2. Canonical functional backbone

The ATDS functional backbone remains:

```text
DATA
↓
CONTEXT
↓
RESEARCH / EXPERIENCE
↓
DECISION
↓
ACTION
↓
RESULT
↓
TRACE
↓
MEMORY
↓
AUDIT / SELF-CHALLENGE
↓
REVISION
└────────→ NEW RESEARCH / EXPERIENCE
```

Architecture V2 does not replace this chain. It clarifies epistemic, dependency, and authority boundaries.

## 3. Conceptual epistemic domains

The following are adopted as conceptual classification domains only:

```text
O — OBSERVATION
K — KNOWLEDGE / RESEARCH
D — DECISION / EFFECT
```

They do not authorize creation of three new modules, services, repositories, or runtimes.

### O — Observation

Includes raw data, source identity, provenance, integrity, current observations, and real results. A real RESULT re-enters the system as a new observation.

### K — Knowledge / Research

Includes asset-behavior profiles, context models, hypotheses, experiments, evidence, evaluations, qualified findings, and experimental memory.

Derived objects must preserve their epistemic status where materially relevant, including:

```text
OBSERVED
INFERRED
QUALIFIED
REFUTED
NOT_INTERPRETABLE
UNKNOWN
```

### D — Decision / Effect

Consumes current observations, qualified knowledge, constraints, and authority, and may eventually produce Decision → Action.

Current operational effect authority remains CLOSED. Existing semantic Decision/Action machinery does not imply paper, broker, live, or capital authority.

## 4. Program / meta layer

Project Control Plane V0, governance, self-challenge, adversarial qualification, governance-effectiveness review, and program audit remain outside the trading system-object as a non-authoritative program/meta layer.

```text
PHASE_22 = CLOSED
P22-01 = PASS
P22-02 = PASS
P22-03 = PASS
P22-04 = NOT_AUTHORIZED
```

## 5. Authority invariant

The following invariant is adopted:

```text
NO MODEL
NO PLAN
NO CONTROL
NO AGENT
NO LLM

MAY GRANT ITSELF
CONSEQUENTIAL AUTHORITY
OR CLOSE ITS OWN
CONSEQUENTIAL FINDING
```

Consequential promotion remains subject to explicit human adjudication.

Conceptually:

```text
CANDIDATE
↓
EVIDENCE
↓
CHALLENGE
↓
HUMAN ADJUDICATION
↓
ADOPT / REJECT / DEFER / BLOCK
```

## 6. Unknown-unknown discovery problem

ATDS does not claim that it can identify all unknown unknowns.

The existing META-GOVERNANCE / SELF-CHALLENGE foundation remains the normative source. The program preserves the problem:

```text
UNKNOWN-UNKNOWN DISCOVERY PROBLEM
```

and the requirement to create discovery pressure against the system's own representation, without claiming complete coverage.

No normative component named `UNKNOWN-UNKNOWN DETECTOR` is created.

## 7. Future executable discovery properties

The following are retained only as future governed candidate boundaries:

```text
UU-P1 — DEPENDENCY / COVERAGE MAP
UU-P2 — BLIND DETECTION QUALIFICATION
UU-P3 — SURPRISE REGISTRY
```

None is authorized for implementation by this decision.

Any future implementation requires its own explicit governed boundary, test-first qualification, and human authorization.

## 8. Scoped PASS

Architecture V2 adopts:

```text
PASS
=
NO FAILURE FOUND
WITHIN THE DEFINED
AND ACTUALLY TESTED SURFACE
```

PASS does not mean:

```text
NO MATERIAL FAILURE EXISTS
```

Where materially relevant, evidence should preserve the tested surface, validity domain, assumptions, known limitations, and out-of-scope surfaces.

This decision does not retroactively reopen Phase 22.

## 9. Independence

Architecture V2 explicitly distinguishes:

```text
IMPLEMENTATION INDEPENDENCE
DATA / SOURCE INDEPENDENCE
SPECIFICATION / ASSUMPTION DIVERSITY
AUTHORITY INDEPENDENCE
```

Multiple controls that share the same source, specification, or critical assumption are not treated as multiple independent validations of that shared assumption.

Preferred concepts are:

```text
ASSUMPTION-DIVERSE
NON-SHARED ASSUMPTION PATH
NON-SHARED SOURCE PATH
```

rather than claiming absolute assumption independence.

## 10. Source-scoped claims

Findings dependent exclusively on:

```text
SOURCE_B_USTECH_PRICE_CORE_V0_1
```

must remain interpreted under the governed Source-B / USTECH semantics and must not silently become universal claims about the Nasdaq-100 market.

A materially stronger source-general claim requires separate evidence with appropriately different source or measurement dependencies.

## 11. Surprise and pristine evidence

Architecture V2 adopts:

```text
SURPRISE != ERROR TO HIDE
SURPRISE != NEW TRUTH
SURPRISE = CANDIDATE RESEARCH TRIGGER
```

and:

```text
DISCOVERY MUST NOT SILENTLY CONSUME
CONFIRMATORY EVIDENCE
```

Any exploratory inspection that exceeds an existing permitted exposure boundary must explicitly alter the exposure status of the affected evidence.

Evidence used to generate a new hypothesis cannot simultaneously be relabeled as independent confirmation of that hypothesis.

Existing contamination and evidence-admissibility rules remain authoritative.

## 12. E1-TD remains unchanged

This architectural adoption does not alter:

```text
TD-01
TD-02
TD-03
TD-03A
TD-03B
```

The frozen research design remains:

```text
WINDOW =
2026-10-01T00:00:00Z
→
2027-10-01T00:00:00Z

PRIMARY_METRIC =
FLIP_FRACTION

MINIMUM_CLOSED_TRADES =
100

SOURCE_POLICY =
SOURCE_B_CONTINUATION_OR_BLOCK
```

Current state at adoption:

```text
TD03B =
WAITING_SOURCE_CONTINUATION

TD03B_EVENT_BUDGET =
0 / 1
```

No automatic source substitution is authorized.

## 13. Preserved open debts

This adoption does not silently close:

```text
P1.16 FINAL CLOSURE
A0 V0.3 FULL COVERAGE
C01 REAL CONFIRMATION
GOVERNANCE EFFECTIVENESS
REPOSITORY TEST TOPOLOGY
SOURCE-INDEPENDENT VALIDATION
```

These remain separate program debts or future frontiers.

## 14. Explicit non-authorizations

This decision does not authorize:

```text
P22-04
AUTOMATIC AUTHORITY GRANTING
AUTOMATIC MUTATION ORCHESTRATION
AUTOMATIC UNKNOWN-UNKNOWN DETECTOR
AUTOMATIC HYPOTHESIS GENERATOR
AUTOMATIC SOURCE FALLBACK
NEW DATASET SUBSTITUTION
E1 RERUN
MOMENTUM_V1 MODIFICATION
RISK ENGINE
PORTFOLIO ENGINE
MT5
PAPER
BROKER
LIVE
CAPITAL
MULTI-PROJECT AGENT MASTER
OBSIDIAN REARCHITECTURE
```

## 15. Adopted architectural state

```text
ARCHITECTURE_V2 =
HUMAN_ADOPTED_WITH_AMENDMENTS

CANDIDATE_A =
SUPERSEDED

CANDIDATE_B =
REJECTED_AS_NORMATIVE

CANDIDATE_C =
ADOPTED_WITH_AMENDMENTS

CLAUDE_ADVERSARIAL_REVIEW =
INCORPORATED_WITH_EVIDENCE_RESOLUTION

UNKNOWN_UNKNOWN_DISCOVERY_PROBLEM =
PRESERVED

UU-P1 =
FUTURE_BOUNDARY_NOT_AUTHORIZED

UU-P2 =
FUTURE_BOUNDARY_NOT_AUTHORIZED

UU-P3 =
FUTURE_BOUNDARY_NOT_AUTHORIZED
```

## 16. Persistence authority and limits

The human explicitly authorized persistence of this decision as one canonical document, with:

```text
RUNTIME_MODIFICATION = FORBIDDEN
UU_P1_IMPLEMENTATION = FORBIDDEN
UU_P2_IMPLEMENTATION = FORBIDDEN
UU_P3_IMPLEMENTATION = FORBIDDEN
E1_MUTATION = FORBIDDEN
E1_TD_MUTATION = FORBIDDEN
TD03B_MUTATION = FORBIDDEN
TD03B_EVENT_CONSUMPTION = FORBIDDEN
MOMENTUM_V1_MODIFICATION = FORBIDDEN
P22_04_OPENING = FORBIDDEN
PHASE_23_OPENING = FORBIDDEN
MT5 = FORBIDDEN
PAPER = FORBIDDEN
BROKER = FORBIDDEN
LIVE = FORBIDDEN
CAPITAL = FORBIDDEN
```

## 17. Stop boundary

After persistence and post-persistence verification:

```text
NEW_IMPLEMENTATION =
NOT_AUTHORIZED

NEXT_PROGRAM_FRONTIER =
REQUIRES SEPARATE HUMAN ADJUDICATION

STOP =
TRUE
```
