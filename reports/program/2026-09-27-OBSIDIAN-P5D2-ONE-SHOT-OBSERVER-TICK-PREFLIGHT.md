# OBSIDIAN P5-D2 — ONE-SHOT OBSERVER TICK PREFLIGHT

Date: 2026-09-27

## Scope

P5-D2 implements exactly one deterministic observer state transition per invocation.

It does not implement or authorize:

- network observation;
- Git ancestry resolution;
- remote fetch;
- filesystem state persistence;
- append-only disk event persistence;
- background execution;
- polling loops;
- timers or sleep;
- production promotion;
- continuous Vault writes;
- Windows startup/scheduled-task/service registration;
- native Obsidian Graph/Search CURRENT semantics.

## Qualified predecessor

P5-D1 qualification commit:

    dce36303982d73a37d8498400f0a13e708e841b6

P5-D1 contract blob:

    a20999ae991e07447e25ecd1592964f2d333449b

P5-D1 qualification report blob:

    fbe4a60f2349a96bf7a1f4c5dea0eb28328af841

## Candidate branch

    feat/obsidian-projection-p5d2-one-shot-observer-tick-v0.1

## Exact functional candidate

    b7451db65a555c1828a4113abfb9c61fafda0b90

This exact HEAD is the P5-D2 functional candidate for local re-break.

Later evidence-only commits must not replace this runtime candidate.

## Candidate artifacts

Contract:

    tools/obsidian_projection/one_shot_observer_tick_contract_v0_1.json
    blob: 5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3

Implementation:

    tools/obsidian_projection/observer_tick.py
    blob: fd212f61ec38332b677110f40265638af55a73e2

Contract breakers:

    tests/obsidian_projection/test_one_shot_observer_tick_contract_v0_1.py
    blob: 25ef701b4b58cc40f2c23488260f7c19824350c1

Behavioral tests:

    tests/obsidian_projection/test_observer_tick.py
    blob: 9c472a39e3d8eed8cf6cfc910bce27ee5fac7c58

Adversarial breakers:

    tests/obsidian_projection/test_p5d2_adversarial.py
    blob: 27aa21c17afddac388f27d04b8b6aae829eb5405

Documentation:

    docs/OBSIDIAN-P5D2-ONE-SHOT-OBSERVER-TICK-V0.1.md
    blob: fa3aea834e6e09efdc52d56c18ab09ccfbb9d6cc

## Contract identity

The implementation pins:

    CONTRACT_BLOB = 5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3

The adversarial breaker independently checks that same identity.

## Static inventory

Preregistered required breakers:

    67 unique

Persisted Python test methods:

    contract = 24
    behavioral = 54
    adversarial = 17

These are repository counts only, not execution evidence.

## Pure implementation boundary

The implementation has one observer-tick entrypoint:

    one_shot_tick(previous_state, normalized_input)

Static inspection found:

    repeated one_shot_tick definition count = 1
    while-loop count = 0

No forbidden runtime dependency string was found for:

    subprocess
    socket
    urllib
    requests
    pathlib
    os.environ
    time
    sleep
    random
    threading
    multiprocessing
    asyncio
    winreg
    ctypes
    Start-Process
    schtasks
    production Vault path

This is a static inspection, not execution evidence.

## Core fail-closed properties

P5-D2 rejects:

- malformed state;
- malformed or uppercase HEAD identities;
- duplicate pending HEADs;
- invalid CURRENT claims;
- inconsistent BLOCKED/CANDIDATE_PENDING/EVALUATING state;
- skipped/replayed event sequence;
- extra normalized input fields;
- malformed event-specific fields;
- minimally inconsistent transition classification;
- invalid evaluation candidate identity;
- invalid promotion-confirmation identity;
- any event after STOPPED.

Invalid inputs raise ObserverTickError and return no partial result.

## Qualification/promotion separation

EVALUATION_PASSED may advance:

    last_qualified_head

but may not change:

    live_projection_head

PROMOTION_CONFIRMED is only a logical state input from a future external governed component.

P5-D2 itself performs no promotion I/O.

Every decision keeps:

    automatic_promotion_authorized = false
    production_write_authorized = false

## Sticky block

Once BLOCKED, later remote observations remain auditable but do not:

- clear BLOCKED;
- change live projection;
- grow the pending queue;
- replace the blocking HEAD;
- replace the blocking failure code.

## Delta boundary

Relative to the P5-D1 qualification commit, the P5-D2 functional candidate adds only P5-D2-specific contract, implementation, tests and documentation.

No pre-existing qualified component is modified.

## Required local re-break

Before P5-D2 may qualify:

1. fetch the P5-D2 branch;
2. recover exact functional candidate HEAD b7451db65a555c1828a4113abfb9c61fafda0b90;
3. require clean control checkout;
4. py_compile observer_tick.py and all three P5-D2 test modules;
5. run targeted P5-D2 contract, behavioral and adversarial tests;
6. run the full tests/obsidian_projection suite;
7. require clean control checkout after execution;
8. treat generated pycache/pyc only according to the existing source-cleanliness rule.

No P5-D3 implementation is authorized before this re-break passes.

## Next governed boundary on PASS

    P5-D3 — CONTROLLED CANDIDATE EVALUATION PIPELINE
