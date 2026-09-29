# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION V0.3 HUMAN ONE-SHOT AUTHORIZATION V1

Date: 2026-09-29

## Evidence status

USER EXPLICIT AUTHORIZATION RECEIVED IN CHAT.

This artifact records the human authorization boundary.
It does not itself execute the real handoff.

## Exact authorization literal

    AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF

## Qualified execution surface

Synthetic qualification commit:

    1a258a66b538dc5705b72f53760760d0bf1c568b

Exact V0.3 recovery real-execution runner:

    tools/obsidian_projection/p5d3f_recovery_real_execution_v0_3.py

Runner blob:

    2d22734c73c7e95eed88141c3237ed61afe39dfe

Qualified recovery implementation blob:

    dcd70a9d9794675eab90e41df560f8b030b5dbf3

Qualified recovery contract V0.2 blob:

    aef627936b6f745017bcace7e8a3e44270f95674

Qualified original P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## Authorized persistent prestate

Exactly:

    PRESENT_EMPTY_PACKAGES_RECOVERY

Meaning:

    staging/
      packages/    [empty]

with no other top-level staging entry and no retained PROMOTION-HANDOFF.json.

## Authorized scope

Exactly one governed V0.3 recovery real execution is authorized for:

- exact qualified V0.3 runner only;
- exact PRESENT_EMPTY_PACKAGES_RECOVERY staging prestate only;
- one READY_UNAUTHORIZED persistent handoff materialization;
- read-only real-Vault fingerprint before and after;
- independent REAL_VAULT_ZERO_MUTATION proof;
- preservation of original body exception and surviving temporary root on body failure;
- preservation and explicit surfacing of the successful body result if only post-success temporary cleanup blocks;
- mandatory STOP after PASS or BLOCKED outcome.

## Explicitly not authorized

- any write in the real Vault;
- CURRENT or CURRENT.tmp creation or mutation;
- generation materialization in the real Vault;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage A;
- Stage B;
- automatic/background publication;
- P5-D4;
- P6.

## Consumption semantics

This authorization is one-shot.

Any governed invocation that reaches the V0.3 real-execution entrypoint consumes this authorization for governance purposes, regardless of PASS or BLOCKED outcome.

No silent retry is authorized.

A PASS requires mandatory STOP.
A BLOCKED/FAIL outcome requires residual audit before any later authorization.
