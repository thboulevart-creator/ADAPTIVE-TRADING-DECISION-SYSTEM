# OBSIDIAN P5-D3F — FAILURE-PRESERVATION V0.2 HUMAN ONE-SHOT AUTHORIZATION V1

Date: 2026-09-29

## Evidence status

USER EXPLICIT AUTHORIZATION RECEIVED IN CHAT.

The authorization text was duplicated verbatim in the same user message. It is adjudicated as one authorization event, not two independent authorizations.

This artifact records the human authorization boundary. It does not itself execute the handoff.

## Exact authorization literal

    AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF

## Qualified execution surface

Failure-preservation V0.2 synthetic qualification commit:

    b86a586644ccf1bf34fdc0bac621135ca21b7e20

Corrected real execution runner blob:

    1b44e12a6c23715ea3d5055c9263f4bccb67fe39

Persistent handoff implementation blob:

    d2f40c8b2c8fb06b37bb34442c59d78222046452

Persistent handoff gate contract blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## Authorized prestate

    PERSISTENT STAGING = PRESENT_EMPTY
    PROMOTION-HANDOFF.json = ABSENT

## Authorized scope

Exactly one finite P5-D3F persistent handoff retry is authorized for:

- use of the exact persistent staging root in PRESENT_EMPTY state;
- read-only fingerprinting of the real Vault before and after;
- fresh observation of origin/integration/system-v1;
- construction of a clean temporary detached candidate repository;
- one invocation of the qualified P5-D3F handoff runtime;
- persistence of exactly one READY_UNAUTHORIZED handoff;
- post-write handoff reverification;
- REAL_VAULT_ZERO_MUTATION proof;
- preservation of the original failure and residual snapshot if execution fails;
- mandatory STOP.

## Explicitly not authorized

- any real-Vault write;
- CURRENT or CURRENT.tmp mutation;
- real-Vault generation materialization;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage-A approval;
- Stage-B execution authority;
- automatic publication;
- background observer / polling;
- P5-D4;
- P6.

## Consumption semantics

This authorization is one-shot.

Any governed invocation that reaches the corrected real-execution entrypoint consumes this authorization for governance purposes, regardless of PASS or BLOCKED outcome.

No silent retry is authorized.

A PASS requires mandatory STOP.
A BLOCKED/FAIL outcome requires residual audit before any future authorization.
