# OBSIDIAN P5-D3F — PERSISTENT DESTINATION VERIFIER AMENDMENT V0.1 — DOWNSTREAM PIN DRIFT CONFIRMATION

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL EXECUTION plus VERIFIED GITHUB dependency state.

## Historical P5-D3C2 compatibility correction

The user reran the complete P5-D3C2 adversarial suite on:

    3b44371bbdbdfda4660bd767b54d028ef0171a82

Reported result:

    Ran 20 tests in 0.080s
    OK

This confirms the two direct amendment-induced historical compatibility regressions are locally closed:

- descriptor authority remains visibly literal false on the historical public verifier surface;
- no new unbounded background-loop surface remains.

## Targeted downstream discrimination

The user then ran only:

    test_p5d3g_live_publication_transaction.
    P5D3GLivePublicationImplementationTests.
    test_planning_is_read_only

Reported result:

    ERROR

Exact failure:

    LivePublicationGovernanceError:
    qualified tooling commit mismatch:
    tools/obsidian_projection/p5d3f_promotion_handoff.py

The failure originates in:

    live_publication_transaction._verify_tooling_identity()

before the planning logic proceeds.

## Verified GitHub dependency state

Current amended candidate-generation verifier blob:

    398bda75604f8172128fbe0ddaf78cab4cee9f92

Current amended P5-D3F promotion-handoff blob:

    23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60

P5-D3G live-publication implementation still pins:

    P5D3F_IMPLEMENTATION_BLOB =
    2108131914cf65bb076b80f5bb63cd63267567fa

and:

    P5D3C2_VERIFIER_BLOB =
    e2e5867536f4f9c7dec475c6696737249536ff39

Therefore the observed P5-D3G error is conclusively a stale downstream tooling-identity pin.

After P5-D3F pin realignment, the stale P5-D3C2 verifier pin would also need realignment before _verify_tooling_identity can pass.

## Adjudication

    P5-D3C2 HISTORICAL COMPATIBILITY = USER-REPORTED PASS
    P5-D3G ERROR CAUSE = VERIFIED STALE DEPENDENCY PINS
    P5-D3F AMENDMENT TARGETED SURFACE = PREVIOUSLY USER-REPORTED PASS
    FULL OBSIDIAN RE-BREAK = STILL BLOCKED
    REAL PERSISTENT HANDOFF = NOT AUTHORIZED
    LIVE PUBLICATION = NOT AUTHORIZED

This is not evidence of a semantic defect in the new persistent verifier.

It is an explicit downstream qualification dependency boundary.

## Required next governed frontier

A separate, narrow P5-D3G downstream dependency-pin requalification is required before the full Obsidian suite can be expected to pass.

That frontier may only mechanically rebind P5-D3G tooling identity to the newly qualified upstream blobs and rerun P5-D3G synthetic/adversarial qualification.

No live publication, no real Vault access, no CURRENT mutation, no PROMOTION_CONFIRMED, no Stage A, and no Stage B may be authorized by that frontier.
