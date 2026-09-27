# OBSIDIAN P5-D1 — OBSERVER CORE CONTRACT QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified functional candidate

Exact P5-D1 functional candidate:

    06899f10a758a0a93575ca66c4e5c00fd936699e

Branch:

    feat/obsidian-projection-p5d1-observer-core-contract-v0.1

Later commits on the branch before this qualification record were evidence-only reports and do not replace the tested functional candidate.

## Reported local re-break result

The user reported:

    Ran 642 tests in 11.383s
    OK
    P5D1_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D1_LOCAL_REBREAK_COMPLETED=PASS

The prescribed wrapper emits the final completion marker only after its earlier py_compile and targeted P5-D1 contract-breaker gates complete without raising a blocking exception.

Therefore this qualification records the supplied run as the governed P5-D1 local re-break PASS.

## Qualified P5-D1 boundary

P5-D1 qualifies the deterministic and auditable observer core contract only.

Qualified properties include:

- observer core is specified as a pure deterministic state transition;
- network, filesystem, process, wall-clock, environment-variable and randomness dependencies are excluded from the pure transition;
- SAME HEAD is NOOP;
- INITIAL and FAST_FORWARD may be queued for later evaluation;
- NON_FAST_FORWARD and UNKNOWN require adjudication;
- remote freshness is separate from projection state;
- loss of remote freshness may not create or preserve a fresh CURRENT claim;
- evaluation PASS advances qualification identity without changing the live projection head;
- evaluation FAIL preserves last-known-good;
- queue identity is exact-HEAD, ordered and deduplicated;
- active evaluation may not be retargeted;
- append-only audit digests bind previous state, input, decision and next state;
- volatile event-envelope data does not affect deterministic digests;
- single-writer semantics are required;
- qualified P5-B2 / P5-C2 / P5-C3R2 mechanisms must be reused, not weakened or reimplemented.

## Preserved non-authorizations

P5-D1 qualification does NOT authorize:

    observer core runtime network execution
    remote fetch execution
    background observer execution
    polling loop execution
    production promotion
    continuous Vault writes
    Windows startup registration
    scheduled task creation
    Windows service creation
    Graph/Search CURRENT semantics

## Verdict

**PASS — P5-D1 CONTINUOUS OBSERVER CORE CONTRACT QUALIFIED**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This does not constitute independent local execution by the assistant.

## Next governed frontier

The next authorized boundary is:

    P5-D2 — ONE-SHOT OBSERVER TICK IMPLEMENTATION

P5-D2 must implement one finite invocation of the already-qualified state machine.

It must not introduce:

- a background loop;
- polling cadence;
- Windows persistence;
- production continuous-write authority;
- native Graph/Search CURRENT semantics.
