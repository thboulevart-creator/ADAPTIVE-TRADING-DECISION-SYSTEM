# Source Findings — Extracted Architectural Knowledge

**Status:** WORKING ASSESSMENT — NON-NORMATIVE  
**Date:** 2026-09-08  
**Source:** interview/transcript supplied in the work session

## Purpose

This document extracts only architecture-relevant principles from the source. Product names, vendor preferences, organizational anecdotes and unsupported numerical productivity claims are intentionally excluded.

## A. Closed feedback loop

An autonomous coding/production system should not be modeled as a generator followed by human review. The useful architectural pattern is:

```text
OBJECTIVE / SPECIFICATION
        ↓
      ACTION
        ↓
    OBSERVATION
        ↓
    VALIDATION
        ↓
    DIAGNOSIS
        ↓
  REPAIR / ESCALATE
        ↓
   RE-VALIDATION
        ↓
     DECISION
        ↓
     MEMORY
```

This is a reusable control-loop pattern, not a mandatory linear business lifecycle.

## B. Validation is an execution environment, not a final checkbox

The source emphasizes that autonomous generation becomes materially safer when the generated artifact is surrounded by increasingly strong feedback mechanisms:

1. static/type/compile validation;
2. unit tests;
3. integration tests;
4. behavioral/system tests;
5. simulation and fault injection;
6. adversarial/security validation;
7. regression/re-validation.

The exact layers must remain domain-specific. The architectural requirement is composable validation with explicit gates.

## C. Strong constraints can improve autonomous execution

A precise specification, strict interfaces, typed contracts and deterministic validation reduce the space of acceptable outputs and therefore improve the feedback loop.

For our systems, the transferable principle is **constraint-rich execution**, not adoption of a particular programming language.

## D. Deliberate failure injection

A mature autonomous system should not only wait for naturally occurring failures. It should be able to deliberately introduce controlled faults and observe whether the system detects, contains, diagnoses and recovers from them.

Examples from the source include packet loss, component restart and distributed-system perturbations. These are examples only; the reusable concept is fault injection against declared failure models.

## E. Cheap experiments / proof-of-concept path

Autonomous systems can reduce the cost of exploring migrations, alternative implementations and technical hypotheses. This is valuable when the experiment is isolated, measurable and reversible.

The architecture must therefore support low-cost experimental branches without allowing experimental output to silently become production truth.

## F. Agent harness

An autonomous agent is more safely treated as an execution component inside a harness containing:

- explicit task/specification;
- contracts and constraints;
- tools/interfaces;
- validation;
- observability;
- permissions/safety boundaries;
- provenance;
- failure handling;
- memory.

The source's language of an agent being "inhuman" is interpreted architecturally as a reason to give agents machine-scale tasks, not as permission to remove controls.

## G. Adversarial self-testing

Independent evaluators or multiple independent evaluation passes can be used to attack the system's own output. This reinforces the existing adversarial-audit architecture.

The reusable principle is evaluator independence and attack diversity, not dependence on specific LLM vendors.

## H. Failure-to-memory closure

Failures should become durable learning material when appropriate. The system should preserve:

- what failed;
- under which conditions;
- why it failed or which explanations were tested;
- what repair was attempted;
- whether the repair worked;
- what validation was performed afterwards;
- whether the result is reusable knowledge.

This directly strengthens the existing Experimental Memory requirement.

## I. Reproducible execution identity

Every meaningful autonomous experiment or execution should be reconstructable from an appropriate combination of:

- task/specification version;
- code/artifact version;
- configuration;
- data/evidence inputs;
- environment/tool versions;
- provider/model information where relevant;
- validation results;
- outcome and provenance.

The required fields are domain-dependent; the invariant is reconstructability without fabricated ancestry.

## J. Architecture over raw model capability

The source strongly argues that raw model quality alone does not determine system quality. The surrounding architecture determines whether generated work can be cheaply tested, corrected and trusted.

For our repositories this is an architectural reinforcement, not a new model-selection requirement.

## Explicit exclusions

The following are **not** extracted as architectural requirements:

- Rust as a mandatory language;
- Claude, Codex, Gemini, Grok or any other specific model as a mandatory provider;
- a specific IDE/orchestrator;
- claims about exact productivity multipliers;
- organizational policies described only as Clever Cloud management choices;
- geopolitical/sovereignty arguments unless separately relevant to deployment governance;
- replacing humans with agents as a general organizational policy.
