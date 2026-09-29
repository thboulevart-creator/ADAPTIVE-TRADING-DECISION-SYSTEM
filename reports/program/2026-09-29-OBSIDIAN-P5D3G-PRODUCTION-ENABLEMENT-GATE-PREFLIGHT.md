# OBSIDIAN P5-D3G — PRODUCTION ENABLEMENT / REAL-LIVE PUBLICATION GATE PREFLIGHT

Date: 2026-09-29

## Evidence status

READ-ONLY / STATIC PREFLIGHT.

No production runtime is opened by this document.
No real Vault write is authorized or performed.
No production CURRENT.md or CURRENT.tmp mutation is authorized.
No production P5-D2 PROMOTION_CONFIRMED is authorized.

## Qualified source checkpoint

P5-D3G implementation qualification commit:

    87c189cd3b0fe6ce40845214a943a14407618ece

Qualified finite publication implementation candidate:

    f725854a7539d1a3b589ca2e49d45c22f6699d3d

Qualified implementation blob:

    b8875f8973ddf1076ff20d8e725ce04abbb814a8

Qualified implementation tests blob:

    bb66cc935b8632eef8fec4a70e205e2fb5b02fd4

Qualified contract blob:

    64997ddd9977229961387f66af4de356c045c0ac

## Exact frontier

    P5-D3G — PRODUCTION ENABLEMENT / REAL-LIVE PUBLICATION GATE

The purpose of this frontier is not to publish.

The purpose is to define and qualify the authority transition required before any real-Vault mutation can ever be considered.

## Required two-stage human authority

Stage A — PLAN APPROVAL

- build one exact real-Vault publication plan READ-ONLY;
- bind a one-shot human plan approval to that exact plan digest;
- prove that neither planning nor plan approval mutates the real Vault;
- qualify the production-enablement surface;
- STOP.

Stage B — EXECUTION AUTHORIZATION

- separate later human authorization;
- may exist only after Stage A qualification;
- must bind the exact already-approved plan plus the Stage-A approval identity;
- must authorize exactly one finite real-live publication transaction;
- is not created or implied by this contract-qualification phase.

Stage-A approval MUST NOT itself be executable publication authority.

## Fail-closed production path

The currently qualified sacrificial runtime hard-rejects the real production Vault.

That guard must remain in force during contract qualification.

No implementation may simply delete, bypass, monkey-patch or weaken that guard.

A later implementation must introduce a distinct, explicit production planning path whose only authority before Stage B is READ-ONLY inspection.

## Production planning requirements

A real-Vault plan must capture at minimum:

- exact qualified retained P5-D3F handoff identity;
- exact candidate HEAD and tree;
- exact generation ID and publication-generation digest;
- exact real Vault resolved identity;
- exact CURRENT.md prestate, including raw-byte digest if present;
- exact CURRENT.tmp state;
- exact target-generation state;
- exact publication mode;
- exact operation-sequence digest;
- exact qualified implementation / contract identities;
- timestamp-free deterministic plan digest semantics.

Planning must create no file, directory, lock, temp file, receipt, authorization-consumption record or pointer mutation inside or outside the real Vault except the caller explicitly choosing to persist the plan as evidence outside the Vault after planning.

## Qualification target

This gate may qualify only:

    PRODUCTION READ-ONLY PLANNING
    +
    EXACT ONE-SHOT PLAN-APPROVAL VALIDATION
    +
    PROOF OF ZERO REAL-VAULT MUTATION

It may not qualify:

    REAL-LIVE EXECUTION
    REAL CURRENT MUTATION
    REAL TARGET MATERIALIZATION
    REAL PROMOTION_CONFIRMED
    AUTOMATIC PUBLICATION
    BACKGROUND OBSERVER

## STOP condition

After this gate qualifies:

    STOP

A distinct human instruction is required before any Stage-B execution authorization can be designed, issued or consumed.
