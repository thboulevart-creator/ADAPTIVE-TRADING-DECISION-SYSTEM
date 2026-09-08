# Architectural Delta — Source Findings vs Existing Systems

**Status:** WORKING DELTA — NON-NORMATIVE  
**Date:** 2026-09-08  
**Authority:** subordinate to all existing LOCKED/FROZEN contracts and adjudications

## 1. Executive conclusion

The source does not justify a redesign. It exposes a missing **execution/control layer** around several capabilities that already exist as contracts, governance or partial implementation.

The principal delta is:

```text
EXISTING CONTRACTS / DOMAIN RULES
              ↓
      EXECUTABLE CONTROL LOOP
              ↓
 validation → diagnosis → repair → revalidation
              ↓
       provenance + memory closure
```

The content repository already has a frozen `ExperimentRunner` application contract, repository boundaries, domain gates, provenance services and conformance tests. Therefore the source must not be used to invent a second experiment lifecycle or bypass the existing V0.1 boundaries.

## 2. Delta register

| ID | Delta | Current state | Classification | Priority | Integration target | Dependency |
|---|---|---|---|---|---|---|
| D-01 | Generic validation harness | Multiple domain-specific gates/tests exist | PARTIAL / NEW CROSS-CUTTING CAPABILITY | P0 | shared application/testing architecture; domain validators remain authoritative | existing contracts + domain gates |
| D-02 | Fault injection / simulation harness | Failure analysis exists; executable generic fault injection not established | ABSENT/PARTIAL | P0 | trading first; reusable pattern later | failure taxonomy + observability |
| D-03 | Diagnosis contract | Failure/rejection concepts exist, but diagnosis is not a reusable execution boundary | PARTIAL | P0 | cross-system control layer | validation + failure records |
| D-04 | Recovery/repair orchestration | Safe-stop/challenge/rollback principles exist; generic repair loop not established | PARTIAL | P0 | application orchestration | diagnosis + policy + gates |
| D-05 | Re-validation after repair | Tests/gates exist, but generic repair→revalidate lifecycle is not established | PARTIAL | P0 | validation harness | D-01 + D-04 |
| D-06 | Experiment-to-memory closure | Experimental Memory is reserved; content already persists experiments/provenance | PARTIAL | P0 | memory architecture | provenance + experiment records |
| D-07 | Execution identity / run envelope | Strong trading provenance; content technical provenance is implemented | STRONG PARTIAL | P1 | shared provenance abstraction | existing provenance stores |
| D-08 | Agent harness pattern | Application/provider/domain boundaries exist; no reusable harness abstraction proven | PARTIAL | P1 | future control/application layer | D-01, D-03, D-07 |
| D-09 | Adversarial evaluator orchestration | Principle and governance already exist | EXISTS | P1 | automation only where useful | existing adversarial protocols |
| D-10 | Cheap reversible POC path | Experimentation exists as principle and application contract | EXISTS/PARTIAL | P1 | experiment runner / research workflow | existing experiment contracts |

## 3. Repository-specific impact

### Trading system

Highest-value additions:

1. executable scenario/simulation layer;
2. controlled fault injection;
3. failure detection and diagnosis records;
4. recovery/safe-hold orchestration;
5. re-validation and regression linkage;
6. closure into experimental memory.

These must integrate with existing research qualification, provenance, adversarial audit and governance rather than replace them.

### Content system

The source confirms rather than fundamentally changes the current direction. The repository already contains:

- explicit Information Model and graph semantics;
- explicit experimentation concepts;
- an ExperimentRunner contract with a frozen persistence boundary;
- domain gates and policy;
- technical provenance and provenance conformance tests;
- database and application tests;
- a corrected target application architecture.

The remaining relevant delta is therefore primarily **control-loop integration**: validation/failure/recovery/observability and eventual Experimental Memory closure. A new experiment state machine must not be introduced merely because the source describes one informally.

## 4. What must NOT change

The following should not be modified merely because of the source:

- LOCKED semantic/data contracts;
- existing domain gates and policy authority;
- provenance semantics that prohibit fabricated ancestry;
- content-system graph semantics;
- trading research separation between exploration and confirmation;
- existing adversarial governance;
- provider/model choice as an architectural invariant;
- the content V0.1 ExperimentRunner boundary.

## 5. Target control-loop pattern

The reusable target should be expressed as a capability graph rather than a mandatory business pipeline:

```text
                 TASK / OBJECTIVE
                        │
                        ▼
                 AGENT / ACTION
                        │
                        ▼
                    OBSERVE
                        │
                        ▼
                   VALIDATE
                  /         \
               PASS          FAIL
                │              │
                ▼              ▼
             ACCEPT        DIAGNOSE
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
                  REPAIR               ESCALATE
                    │                     │
                    └──────────┬──────────┘
                               ▼
                         RE-VALIDATE
                               │
                               ▼
                     DECISION / ACCEPT
                               │
                               ▼
                         PROVENANCE
                               │
                               ▼
                    EXPERIMENTAL MEMORY
```

A domain may omit or branch parts of this graph. No component may bypass applicable domain gates or safety policy.

## 6. Implementation order

### Phase 1 — Contract the control concepts

Define, without implementation commitment:

1. Validation Result contract;
2. Failure Record / Failure Taxonomy;
3. Diagnosis Result contract;
4. Recovery Attempt record;
5. Re-validation linkage;
6. Run/Execution Envelope;
7. Memory closure linkage.

### Phase 2 — Build the validation harness

Expose existing domain gates/tests through a controlled orchestration boundary. The harness reports evidence and provenance; it does not reimplement domain semantics.

### Phase 3 — Build simulation/fault injection

Start with the trading system. Simulation must use declared fault models, deterministic seeds where possible, bounded resource usage and reproducible run identity.

### Phase 4 — Add diagnosis/recovery orchestration

Only after validation and failure records are stable. Recovery must respect domain policy, safe-stop rules and escalation boundaries. Autonomous repair must never silently promote an unvalidated change.

### Phase 5 — Close the experimental memory loop

Link hypotheses, runs, failures, attempted explanations, repairs, validation outcomes and resulting knowledge. Preserve rejected/inconclusive explanations rather than recording only successful outcomes.

### Phase 6 — Generalize as a reusable architecture pattern

Only after the trading implementation demonstrates the pattern should the abstraction be generalized across autonomous systems. Avoid creating a premature universal framework.

## 7. Decision rule for every future integration

```text
SOURCE PRINCIPLE
      ↓
EXISTING CONTRACT CHECK
      ↓
EXISTING IMPLEMENTATION CHECK
      ↓
GAP CONFIRMED?
   /          \
 NO           YES
 │             │
REJECT      CLASSIFY
              │
              ▼
      MINIMAL INTEGRATION
              │
              ▼
        ADVERSARIAL AUDIT
              │
              ▼
             TEST
              │
              ▼
            FREEZE
```

This prevents the source from becoming a feature backlog and preserves architectural minimality.

## 8. Gate before implementation

No P0/P1 item should be implemented directly from this delta. Each must first receive an impact map, ownership check, contract compatibility check, adversarial review and explicit decision according to the existing governance hierarchy.
