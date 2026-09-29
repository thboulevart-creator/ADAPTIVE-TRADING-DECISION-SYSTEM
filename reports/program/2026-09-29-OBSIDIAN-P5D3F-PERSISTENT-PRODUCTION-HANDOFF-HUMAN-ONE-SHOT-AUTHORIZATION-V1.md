# OBSIDIAN P5-D3F — PERSISTENT PRODUCTION HANDOFF HUMAN ONE-SHOT AUTHORIZATION V1

Date: 2026-09-29

## Evidence status

USER EXPLICIT AUTHORIZATION RECEIVED IN CHAT.

This artifact records the human authorization boundary. It does not itself execute the handoff.

## Exact authorization literal

    AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF

## Authorized scope

Exactly one finite P5-D3F persistent handoff execution is authorized for:

- creation of the exact persistent staging root if absent;
- read-only fingerprinting of the real Vault before and after;
- fresh observation of origin/integration/system-v1;
- construction of a clean temporary detached candidate repository;
- one invocation of the qualified P5-D3F handoff runtime;
- persistence of exactly one READY_UNAUTHORIZED handoff in the exact staging root;
- post-write handoff reverification;
- REAL_VAULT_ZERO_MUTATION proof;
- temporary candidate/evaluation cleanup;
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

## Qualified execution surface

Real execution runner blob:

    e56501e3710ab23537975e950aff016e4a832742

Persistent handoff implementation blob:

    d2f40c8b2c8fb06b37bb34442c59d78222046452

Persistent handoff gate contract blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

Real execution runner synthetic qualification commit:

    60d4eca5cf62dbf78a5f8795574bf72e0fee100b

## Consumption semantics

This human authorization is one-shot.

A successful persistent handoff consumes the authorization and requires STOP.

A BLOCKED or FAIL result does not permit silent retry if any nonempty persistent staging residue exists; such residue requires audit.

No later gate is implied by this authorization.
