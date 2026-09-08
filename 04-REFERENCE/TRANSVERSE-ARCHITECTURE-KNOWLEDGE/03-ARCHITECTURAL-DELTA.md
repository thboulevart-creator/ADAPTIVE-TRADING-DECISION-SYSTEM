# Architectural Delta — Initial Baseline

**Status:** WORKING DELTA — NON-NORMATIVE
**Date:** 2026-09-08

This document records what the source changes, if anything, after comparison with the existing architecture.

## P0 — Connect existing capabilities into a closed feedback loop

### Problem
The repositories already contain validation, experimentation, adversarial review, provenance and governance, but these capabilities are not yet proven to form one reusable executable control loop around autonomous agents.

### Target pattern

```text
OBJECTIVE / HYPOTHESIS
        ↓
PLANNING
        ↓
ACTION / GENERATION
        ↓
OBSERVATION
        ↓
VALIDATION
        ↓
CRITIQUE / FAILURE ANALYSIS
        ↓
REPAIR / RE-EXECUTION
        ↓
VALIDATION AGAIN
        ↓
ACCEPT / REJECT / ESCALATE
        ↓
EXPERIMENTAL MEMORY
```

This is a control-loop abstraction, not a mandatory linear business workflow. It must remain compatible with the content system's path-dependent graph principle.

## P0 — Executable simulation and fault injection

### Problem
Governance documents describe adversarial/failure analysis, but an executable general-purpose simulator/fault-injection layer is not yet established by the inspected baseline.

### Priority
Highest for the trading system because market-data, execution and decision behavior must be tested under degraded and pathological conditions.

### Candidate capabilities

- deterministic scenario replay;
- malformed/duplicate/out-of-order data injection;
- missing-data/interruption scenarios;
- latency/slippage/spread perturbation where applicable;
- regime and volatility perturbation;
- controlled dependency failure;
- randomized fault campaigns with reproducible seeds;
- expected-vs-observed failure records;
- automatic linkage to failure matrix and experiment memory.

### Constraint
Simulation must never be confused with real-market evidence. Simulated results remain simulation evidence with explicit status.

## P0 — Failure lifecycle and safe recovery

### Required lifecycle

```text
FAILURE
  ↓
DETECTION
  ↓
DIAGNOSIS
  ↓
CONTAINMENT / SAFE HOLD
  ↓
REPAIR OR ESCALATION
  ↓
RE-VALIDATION
  ↓
DECISION
  ↓
MEMORY
```

The existing Upward Challenge Protocol already establishes a governed SAFE HOLD concept for critical upstream constraints. The delta is to connect such mechanisms to executable component-level failure handling without allowing autonomous repair to bypass ownership or contracts.

## P1 — Reusable validation harness

The source suggests that the validator, not the generator, becomes the dominant safety boundary. Existing validation artifacts should therefore be exposed through a reusable harness concept.

Minimum conceptual interface:

```text
candidate
context
expected_contracts
→ validation_report
→ verdict
→ failure_records
```

The harness should be able to invoke domain-specific validators without imposing one domain's semantics on another.

## P1 — Experiment closure into memory

The Experimental Memory Charter already reserves the required conceptual fields. The delta is an explicit lifecycle link:

```text
EXPERIMENT
   ↓
RESULT
   ↓
EVIDENCE / VALIDATION
   ↓
EXPLANATION STATUS
   ↓
PROMOTION / REJECTION
   ↓
EXPERIMENTAL MEMORY RECORD
```

No unvalidated result should silently become durable system knowledge or alter decision behavior.

## P1 — Generalized provenance anchor

Trading already has a detailed dataset provenance registry. The reusable abstraction should be generalized carefully:

```text
RUN_ID
CODE_VERSION
CONFIGURATION_VERSION
INPUT_IDENTITIES
ENVIRONMENT_VERSION
MODEL/AGENT VERSION
RESULTS
VALIDATION EVIDENCE
```

Domain-specific provenance remains owned by the relevant domain contract.

## P2 — Agent harness as a pattern

Do not create a monolithic framework prematurely. First define the interfaces between:

- agent/reasoner;
- planner;
- executor;
- validator;
- critic/adversary;
- safety/governance;
- memory;
- observability.

Only implement concrete components when a verified use case requires them.

## Explicitly rejected as architectural requirements

The source does not justify making any of the following system invariants:

- use of Rust;
- use of Claude, GPT, Gemini, Grok or any specific model;
- use of a specific coding IDE/orchestrator;
- replacement of all legacy code;
- multi-model execution for every task;
- unlimited autonomous modification;
- treating tests passing as proof of optimality or safety.

These remain optional implementation choices subject to evidence.

## Dependency order

```text
1. Freeze / verify current contracts and ownership
        ↓
2. Define reusable validation-report interface
        ↓
3. Define simulation / fault-injection contract
        ↓
4. Define failure detection + diagnosis + recovery interfaces
        ↓
5. Connect validation/failure outputs to experimental memory
        ↓
6. Implement trading-domain simulator first
        ↓
7. Reuse/adapt proven patterns for content and future systems
```

## Gate before implementation

No P0/P1 item should be implemented directly from this delta. Each must first receive an impact map, ownership check, contract compatibility check, adversarial review and explicit decision according to the existing governance hierarchy.
