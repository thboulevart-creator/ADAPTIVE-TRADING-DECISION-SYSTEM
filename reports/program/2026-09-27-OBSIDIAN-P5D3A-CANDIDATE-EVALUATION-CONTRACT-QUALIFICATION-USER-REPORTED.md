# OBSIDIAN P5-D3A — CANDIDATE EVALUATION CONTRACT QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified functional candidate

Exact P5-D3A functional candidate:

    f145744b5aafbc9837b4cc140df38afd09d3ce39

Branch:

    feat/obsidian-projection-p5d3a-candidate-evaluation-contract-v0.1

Later branch commits before this qualification record contain only preflight/static-review evidence and do not replace the tested functional candidate.

## Reported local re-break result

The user reported:

    Ran 761 tests in 12.093s
    OK
    P5D3A_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3A_LOCAL_REBREAK_COMPLETED=PASS

The governed wrapper reaches the final completion marker only after:

- exact P5-D3A functional-candidate checkout;
- py_compile of the P5-D3A contract breaker;
- targeted P5-D3A contract-breaker execution;
- full tests/obsidian_projection suite;
- final clean-control-clone verification;

complete without a blocking exception.

This qualification therefore records the supplied run as the governed P5-D3A local re-break PASS.

## Qualified P5-D3A boundary

P5-D3A qualifies the finite controlled candidate-evaluation contract only.

Qualified architectural properties include:

- candidate evaluation may begin only from a qualified P5-D2 START_EXACT_HEAD_EVALUATION decision;
- candidate identity must remain bound to the exact P5-D2 decision and FIFO queue head;
- candidate checkout must be disposable and isolated from canonical worktree and Vault;
- exact repository, branch, HEAD and tree identities must be verified;
- P5-B2 dynamic inventory is the current-head inventory authority;
- implicit DynamicInventory -> FrozenInventory conversion is forbidden;
- the legacy 74-record pilot assumption is forbidden for continuous current-head evaluation;
- every dynamic inventory entry must receive an explicit semantic-bridge disposition;
- silent drops and metadata-only -> full-text upgrades are forbidden;
- deterministic double build is mandatory;
- a preregistered candidate-breaker manifest and digest are mandatory;
- P5-C2 experimental fixture generation may not be relabelled as a real candidate-generation packager;
- real candidate-generation staging requires its own governed contract;
- evaluation outcomes are exactly QUALIFIED / REJECTED / BLOCKED;
- REJECTED and BLOCKED semantics may not be conflated;
- BLOCKED emits no P5-D2 EVALUATION_FAILED event;
- determinate outcomes may update observer state only through the qualified P5-D2 one_shot_tick;
- live_projection_head must remain unchanged throughout evaluation;
- real Vault mutation is forbidden;
- production promotion authority remains false.

## Explicit open sub-frontiers preserved

P5-D3A does not claim that these gaps are already solved.

### Current-head semantic projection bridge

Required next because:

    P5-B2 output = DynamicInventory

while the current semantic classifier consumes:

    FrozenInventory

and the current P2 path still contains an exact 74-record pilot expectation.

Therefore:

    P5-D3B — CURRENT-HEAD SEMANTIC PROJECTION BRIDGE

remains mandatory before the finite evaluator implementation.

### Candidate-generation staging

P5-C2 qualified immutable-generation + atomic-pointer semantics in a sacrificial experiment.

That does not qualify its fixture generator as a real current-head projection packager.

Therefore:

    P5-D3C — CANDIDATE GENERATION STAGING CONTRACT

remains mandatory before the finite orchestrator.

## Preserved non-authorizations

P5-D3A qualification does NOT authorize:

    semantic bridge implementation
    candidate-generation packager
    finite evaluation orchestrator
    network fetch execution
    isolated checkout execution
    candidate breaker execution
    P5-D2 result-event execution
    background observer
    polling loop
    production promotion
    continuous Vault write
    Windows startup registration
    scheduled task creation
    Windows service creation
    Graph/Search CURRENT semantics

## Verdict

**PASS — P5-D3A CONTROLLED CANDIDATE EVALUATION CONTRACT QUALIFIED**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This is not independent local execution by the assistant.

## Next governed frontier

The next authorized boundary is:

    P5-D3B — CURRENT-HEAD SEMANTIC PROJECTION BRIDGE

Its purpose is to close the real repository interface gap between:

    P5-B2 DynamicInventory

and:

    the semantic/projection pipeline

without implicit coercion, silent dropping, legacy 74-record assumptions, or weakened provenance.
