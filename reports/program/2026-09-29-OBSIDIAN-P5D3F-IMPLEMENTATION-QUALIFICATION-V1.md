# OBSIDIAN P5-D3F — IMPLEMENTATION QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed full P5-D3F re-break.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    d835f5e92d93ef24cc0cec054550965ba8b22a5e

Qualified implementation candidate:

    a41c5b150168c2e4eb06648237022a4974868423

Implementation blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

Implementation tests blob:

    b467cbdbe8fced11b0b1b13e6f245f92d0a93c28

## User-reported local result

Targeted P5-D3F controls:

    Ran 32 tests in 2.284s
    OK

Full Obsidian suite:

    Ran 1104 tests in 54.205s
    OK

Terminal markers:

    P5D3F_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_CONTRACT_REBREAK_COMPLETED=PASS

## Adjudication

The P5-D3F implementation candidate passes the governed regression gate.

    P5-D3F IMPLEMENTATION QUALIFICATION = PASS

The implementation remains bounded to READY_UNAUTHORIZED semantics.

This qualification does not authorize:

- real Vault writes;
- CURRENT or CURRENT.tmp mutation;
- P5-C2/P5-C3R2 publication;
- P5-D2 PROMOTION_CONFIRMED;
- automatic publication;
- background polling/observer;
- P5-D3G runtime.

## Remaining gate

The next exact gate is the explicit sacrificial-staging qualification run and persistence of its evidence.

P5-D3G remains closed until that gate is separately qualified.
