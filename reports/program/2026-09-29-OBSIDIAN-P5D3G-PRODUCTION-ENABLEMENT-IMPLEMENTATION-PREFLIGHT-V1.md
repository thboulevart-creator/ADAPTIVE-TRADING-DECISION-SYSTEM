# OBSIDIAN P5-D3G — PRODUCTION ENABLEMENT IMPLEMENTATION PREFLIGHT V1

Date: 2026-09-29

## Evidence status

READ-ONLY / STATIC PREFLIGHT.

No real Vault access is performed by this document.
No real Vault write is authorized.
No Stage-B execution authority is opened.

## Qualified predecessor

Production-enablement contract qualification:

    bd515539a43255750003b188944db0ae1c9ec7d2

Qualified production-enablement contract blob:

    5de65f5d13a93d1325d53e1b58536ed0860921f2

Qualified P5-D3G live-publication implementation blob:

    b8875f8973ddf1076ff20d8e725ce04abbb814a8

## Exact implementation frontier

    P5-D3G-PRODUCTION-ENABLEMENT-IMPLEMENTATION

Allowed scope:

    READ_ONLY_REAL_VAULT_PLAN
    +
    STAGE_A_ONE_SHOT_PLAN_APPROVAL_VALIDATION
    +
    ZERO_REAL_VAULT_MUTATION_PROOF

## Required architecture

The implementation must use a distinct production-planning entrypoint.

The qualified sacrificial runtime and its real-Vault refusal remain unchanged.

The production planner may inspect the exact real Vault only when explicitly invoked.

It may not:

- create CURRENT.md;
- create CURRENT.tmp;
- create generations;
- materialize a target generation;
- create a writer lock in the real Vault;
- create receipts in the real Vault;
- emit P5-D2 PROMOTION_CONFIRMED;
- issue or consume Stage-B authority;
- call the production mutation transaction;
- start a background observer, polling loop, task or service.

## Stage-A semantics

The plan must be built first.

A human Stage-A approval must bind the exact deterministic plan digest and its exact candidate, generation, publication mode and prestate.

Stage-A approval is review authority only.

It is never real-publication authority.

One-shot consumption evidence may be written only to an explicitly separate control/evidence root outside the real Vault and outside the retained handoff.

## Zero-mutation proof

The implementation must fingerprint the real Vault before and after read-only planning / Stage-A validation and require exact equality.

The fingerprint must bind filesystem-relative layout and exact regular-file bytes.

Alias/reparse surfaces are fail-closed.

## Test-first requirement

Adversarial tests are frozen before the implementation candidate.

They must cover at minimum:

- exact real-Vault identity;
- wrong path / alias rejection;
- planning read-only behavior;
- deterministic plan digest;
- CURRENT absent/present prestate;
- CURRENT.tmp preexistence;
- target-generation collision;
- exact retained handoff binding;
- Stage-A missing/mismatched/reused approval;
- Stage-A non-execution semantics;
- zero-mutation proof;
- control-root separation;
- absence of Stage-B / execution / background surfaces.

## Qualification sequence

1. tests frozen;
2. minimal implementation candidate;
3. targeted adversarial tests;
4. complete historical Obsidian suite;
5. exact real-Vault read-only qualification;
6. zero-mutation proof;
7. clean control clone;
8. qualification report;
9. STOP.

No real publication execution is in this sequence.
