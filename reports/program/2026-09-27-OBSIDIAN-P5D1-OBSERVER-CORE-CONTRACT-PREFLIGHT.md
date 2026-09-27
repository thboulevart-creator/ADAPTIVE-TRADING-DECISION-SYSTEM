# OBSIDIAN P5-D1 — OBSERVER CORE CONTRACT PREFLIGHT

Date: 2026-09-27

## Scope

P5-D1 defines only the deterministic and auditable observer state-machine contract.

It does not implement or authorize:

- network observation;
- remote fetch;
- background execution;
- polling loops;
- production promotion;
- continuous Vault writes;
- Windows startup registration;
- scheduled tasks;
- Windows services;
- native Obsidian Graph/Search CURRENT semantics.

## Exact predecessor

P5-C3R2 final qualification commit:

    00ca2946ce30b0e319658f8d5b903357b7ccfc5e

P5-C3R2 qualified runtime candidate:

    b5f3a8de061772e15bc94b20095d419130c20781

P5-C3R remains unqualified.

## Candidate branch

    feat/obsidian-projection-p5d1-observer-core-contract-v0.1

Exact candidate HEAD before local re-break:

    06899f10a758a0a93575ca66c4e5c00fd936699e

## Persisted candidate artifacts

Contract:

    tools/obsidian_projection/continuous_observer_core_contract_v0_1.json
    blob: a20999ae991e07447e25ecd1592964f2d333449b

Contract breakers:

    tests/obsidian_projection/test_continuous_observer_core_contract_v0_1.py
    blob: 08cff6908535838a87ee71054295a67c94d5d529

Documentation:

    docs/OBSIDIAN-P5D1-CONTINUOUS-OBSERVER-CORE-CONTRACT-V0.1.md
    blob: 77bc4ca8c59d91d950e1d664afe76ecd712c77a9

## Qualified dependencies preserved

P5-A continuous projection contract:

    blob: 96ec1a768b8e9ff77d94bbcd36ee513678c258e6

P5-B2 dynamic inventory qualification report:

    blob: 286a81a4f3f71a1d857631c2388d7894908acb5f

P5-C2 promotion qualification report:

    blob: a928598182b25d110c9040c62d846bf9018ac3ed

P5-C3R2 final qualification report:

    blob: fd54a78abde8342c6da708d3a4096b4d0b267905

No qualified predecessor file was modified by the P5-D1 candidate.

## Functional delta

Compared with the P5-C3R2 final qualification commit, P5-D1 adds exactly three governed source artifacts:

1. observer core contract;
2. observer core contract breaker module;
3. observer core documentation.

No implementation module exists in P5-D1.

## Deterministic core

The contract defines:

    next_state, decision
        =
    TRANSITION(previous_state, normalized_input)

The transition forbids:

    network IO
    filesystem IO
    process launch
    wall-clock read
    randomness
    environment-variable read

Same normalized inputs must produce byte-identical normalized outputs.

## State axes

Observer phase:

    IDLE
    CANDIDATE_PENDING
    EVALUATING
    BLOCKED
    STOPPED

Remote freshness:

    KNOWN
    UNKNOWN

Projection state:

    CURRENT
    STALE
    BLOCKED
    ORPHAN
    MISSING

A network observation failure conservatively changes a previous CURRENT projection state to STALE while preserving the live projection head.

## Qualification versus promotion

EVALUATION_PASSED:

    last_qualified_head becomes the exact candidate
    live_projection_head does not change

Promotion is modelled for future state semantics but is explicitly unauthorized in P5-D1.

## HEAD transition policy

    SAME              => NOOP
    INITIAL           => queue exact HEAD
    FAST_FORWARD      => queue exact HEAD
    NON_FAST_FORWARD  => BLOCK_REQUIRES_ADJUDICATION
    UNKNOWN           => BLOCK_REQUIRES_ADJUDICATION

No active evaluation may be retargeted to a newer HEAD.

## Audit model

Every deterministic transition is bound by digests of:

    previous_state
    normalized_input
    decision
    next_state

Volatile timestamps/PID/host identity may exist only in an external event envelope and may not affect deterministic digests.

## Breaker registry

The persisted contract contains:

    50 unique required breakers

The persisted Python breaker module contains:

    24 test methods

These numbers are static artifact counts, not executed-test evidence.

## Required local re-break

Before P5-D1 may qualify:

1. recover exact candidate HEAD 06899f10a758a0a93575ca66c4e5c00fd936699e;
2. require clean control checkout;
3. run py_compile on the new breaker module;
4. run the targeted P5-D1 breaker module;
5. run the full tests/obsidian_projection suite;
6. distinguish generated __pycache__/pyc residue from governed source changes;
7. require no tracked or unexpected untracked mutation.

No P5-D2 implementation is authorized before this re-break passes.

## Next gate on P5-D1 PASS

    P5-D2 — ONE-SHOT OBSERVER TICK IMPLEMENTATION

P5-D2 remains one finite invocation.

The bounded background loop remains deferred to P5-D4.
