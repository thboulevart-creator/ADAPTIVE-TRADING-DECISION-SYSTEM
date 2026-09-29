# OBSIDIAN P5-D3F — PERSISTENT DESTINATION VERIFIER AMENDMENT V0.1 — CONTRACT + RED QUALIFICATION

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL EXECUTION plus VERIFIED GITHUB source state plus SAME-ASSISTANT STATIC REVIEW.

## User-reported contract result

The user reported that the contract qualification script completed successfully before the RED suite.

Contract test surface:

    10 tests

Contract tests blob:

    720470db3dc65d9e335139749a8aebdd0e1ca3d6

## User-reported corrected RED result

    Ran 6 tests in 0.009s
    FAILED (failures=4)

The reported visible failure included:

    test_red_persistent_verifier_surface_exists
    AssertionError: False is not true : RED_EXPECTED: persistent verifier surface absent

## Verified GitHub RED state

Corrected RED tests blob:

    fa421e6c14f7ebf53cc53170a8aaf9f3821acd0b

Historical verifier blob:

    e2e5867536f4f9c7dec475c6696737249536ff39

Historical P5-D3F handoff blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

Static verification confirms:

- verify_persistent_candidate_generation is absent;
- P5-D3F has no persistent-verifier destination binding;
- historical verify_candidate_generation remains TEMP-only;
- the prior generic "while True" false-positive guard has been removed from the RED harness only.

Therefore the corrected RED shape is exactly the intended pre-implementation state:

    PASS — historical TEMP-only verifier preserved
    PASS — no explicit later-authority surface introduced
    FAIL — persistent verifier surface absent
    FAIL — P5-D3F import absent
    FAIL — destination binding absent
    FAIL — explicit authorized_staging_root surface absent

## Exact contract

Contract blob:

    7d13922e51256f2785af4e6d3062116b2bc324d6

## Adjudication

    CONTRACT = PASS
    RED = CONFIRMED
    IMPLEMENTATION = ABSENT
    REAL EXECUTION = NOT AUTHORIZED

The RED failures are required evidence. They are not implementation regressions.

## Next governed frontier

    P5-D3F — PERSISTENT DESTINATION VERIFIER AMENDMENT
    MINIMAL IMPLEMENTATION V0.1

The minimal implementation may only:

1. add a separate explicit persistent-package verification entrypoint;
2. keep the historical TEMP-only verifier behavior unchanged;
3. share the same semantic/content verification core;
4. authorize only the exact persistent staging wrapper shape;
5. keep real Vault, arbitrary persistent roots, aliases/reparse points, hardlinks, tampered content, and later publication authority closed;
6. rebind only the P5-D3F destination verification call to the persistent verifier.

No real persistent execution is authorized by this qualification.
