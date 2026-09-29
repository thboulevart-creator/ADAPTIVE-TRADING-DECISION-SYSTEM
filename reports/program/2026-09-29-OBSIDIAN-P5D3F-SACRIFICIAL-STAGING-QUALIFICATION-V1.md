# OBSIDIAN P5-D3F — SACRIFICIAL STAGING QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed P5-D3F full unittest discovery.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    fb934d81c435416ce4099d20ff3c58f3ed348ab5

Implementation candidate:

    a41c5b150168c2e4eb06648237022a4974868423

Implementation blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

Implementation tests blob:

    b467cbdbe8fced11b0b1b13e6f245f92d0a93c28

Governed runner blob:

    ea94592b4c168313cb4c398a7d37b32a7c1f7b7d

## User-reported local governed result

    Ran 32 tests in 2.284s
    OK

    Ran 1104 tests in 54.205s
    OK

    P5D3F_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_CONTRACT_REBREAK_COMPLETED=PASS

## Sacrificial staging coverage inside the passing full discovery

The discovered suite contains and therefore passed the following concrete P5-D3F execution tests:

    test_successful_synthetic_handoff_is_ready_unauthorized
    test_handoff_verifier_is_read_only
    test_tampered_copied_payload_is_rejected
    test_tampered_handoff_identity_is_rejected
    test_existing_generation_target_blocks

The successful synthetic handoff test uses a sacrificial temporary root with sibling:

    candidate repository
    evaluation workspace
    promotion staging
    real-vault sentinel directory

and asserts:

    PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED
    QUALIFIED evaluator outcome
    PASS_SEALED_UNPROMOTED source package
    PASS_SEALED_UNPROMOTED copied package
    exact retained wrapper layout
    no CURRENT / CURRENT.md / CURRENT.tmp
    read-only handoff verification
    unchanged live-vault fingerprint

The remaining execution tests prove fail-closed behavior for tampering, collision and verifier mutation boundaries.

## Adjudication

    P5-D3F SACRIFICIAL STAGING QUALIFICATION = PASS

The P5-D3F finite promotion handoff implementation and its sacrificial equivalent staging behavior are now qualified.

## Authority boundary

Still NOT authorized:

- persistent production handoff execution;
- real Vault publication;
- CURRENT/CURRENT.tmp mutation;
- P5-C2/P5-C3R2 live publication primitives;
- P5-D2 PROMOTION_CONFIRMED;
- automatic publication;
- background observer/polling;
- P5-D3G runtime.

## Next governed frontier

Per the frozen P5-D3F contract:

    P5-D3G —
    FINITE_LIVE_PUBLICATION_TRANSACTION_CONTRACT

Only the P5-D3G contract-definition boundary is now eligible to open.

No live publication runtime is authorized by this qualification.
