# OBSIDIAN P5-D2 — ONE-SHOT OBSERVER TICK QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified functional candidate

Exact P5-D2 functional candidate:

    b7451db65a555c1828a4113abfb9c61fafda0b90

Branch:

    feat/obsidian-projection-p5d2-one-shot-observer-tick-v0.1

Later branch commits before this qualification record contain evidence-only preflight/static-review reports and do not replace the tested functional candidate.

## Reported local re-break result

The user reported:

    Ran 737 tests in 11.620s
    OK
    P5D2_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D2_LOCAL_REBREAK_COMPLETED=PASS

The prescribed governed wrapper emits the final completion marker only after:

- exact runtime candidate checkout;
- py_compile of the P5-D2 implementation and three P5-D2 test modules;
- targeted P5-D1 + P5-D2 tests;
- full tests/obsidian_projection suite;
- final clean-control-clone check;

complete without a blocking exception.

This qualification therefore records the supplied run as the governed P5-D2 local re-break PASS.

## Qualified P5-D2 boundary

P5-D2 qualifies one finite deterministic observer transition implementation:

    previous_state
          +
    normalized_input
          ↓
      one_shot_tick
          ↓
    next_state
    decision
    audit

Qualified behavior includes:

- strict state-schema validation;
- strict normalized-input field set;
- exactly-next event sequencing;
- lowercase 40-hex HEAD validation;
- CURRENT freshness/identity invariants;
- EVALUATING / CANDIDATE_PENDING / BLOCKED phase invariants;
- INITIAL / SAME / FAST_FORWARD / NON_FAST_FORWARD / UNKNOWN minimal consistency checks;
- SAME => NOOP;
- INITIAL / FAST_FORWARD => exact-HEAD queueing;
- NON_FAST_FORWARD / UNKNOWN => BLOCK_REQUIRES_ADJUDICATION;
- BLOCKED remains sticky until separate adjudication;
- network observation failure preserves live HEAD and degrades fresh CURRENT to STALE;
- evaluation start is bound to FIFO queue head;
- evaluation PASS advances last_qualified_head without changing live_projection_head;
- evaluation FAIL preserves live_projection_head;
- promotion events are logical external confirmations only;
- promotion confirmation requires candidate == last_qualified_head;
- promotion failure preserves previous live HEAD;
- LOCK_CONTENDED is semantic NOOP except monotonic sequence;
- SHUTDOWN preserves pending/live identity and STOPPED is terminal;
- deterministic canonical JSON and SHA-256 audit digests;
- caller-owned state/input objects are not mutated;
- every decision keeps automatic promotion and production write authority false.

## Deterministic audit boundary

The implementation binds:

    previous_state_digest
    input_digest
    decision_digest
    next_state_digest

No timestamp, PID, hostname or host path is generated inside the deterministic audit record.

## Preserved non-authorizations

P5-D2 qualification does NOT authorize:

    network adapter
    Git adapter
    Git ancestry resolution
    remote fetch
    filesystem state persistence
    append-only disk event-log persistence
    background observer
    polling loop
    sleep/timer scheduling
    production promotion
    continuous Vault writes
    Windows startup registration
    scheduled task creation
    Windows service creation
    Graph/Search CURRENT semantics

## Verdict

**PASS — P5-D2 ONE-SHOT OBSERVER TICK IMPLEMENTATION QUALIFIED**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This does not constitute independent local execution by the assistant.

## Next governed frontier

The next authorized boundary is:

    P5-D3 — CONTROLLED CANDIDATE EVALUATION PIPELINE

P5-D3 may connect a finite orchestrator to already qualified components.

It must remain finite and governed.

It must not introduce:

- a background observer loop;
- periodic polling;
- Windows startup persistence;
- production continuous-write authority;
- native Graph/Search CURRENT semantics.

The repeated bounded observer loop remains deferred to:

    P5-D4
