# OBSIDIAN P5-D3F — PROMOTION HANDOFF CONTRACT PREFLIGHT

Date: 2026-09-28

## Status

Evidence-only preflight.

No P5-D3F runtime is implemented or authorized by this record.

## Starting checkpoint

Base checkpoint:

    0f81d444bac91af4d504472d1901f9933cf3dc1b

P5-D3E is CLOSED / QUALIFIED.

The next finite publication-oriented boundary is intentionally inserted before P5-D4.

## Frontier identity

    P5-D3F —
    FINITE PROMOTION HANDOFF /
    RETAINED SEALED GENERATION CONTRACT V0.1

Branch:

    feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1

Exact functional contract candidate:

    5e1aede1b2071c7985a0938ef97025f5e6c03cfa

## Functional artifacts

Contract:

    tools/obsidian_projection/promotion_handoff_contract_v0_1.json

Blob:

    64744325251db350d26c0269090ce62d5fa5f2e8

Contract tests:

    tests/obsidian_projection/test_promotion_handoff_contract_v0_1.py

Blob:

    6c7f3d5e1962132f4b609b637d176e67ccd376d5

Contract documentation:

    docs/OBSIDIAN-P5D3F-PROMOTION-HANDOFF-CONTRACT-V0.1.md

Blob:

    e07dc28c106a17f426044cb057d7598fe7f05b38

Governed local re-break runner:

    tools/obsidian_projection/run_p5d3f_contract_rebreak.ps1

Blob:

    f8d7b5406082d7f8fbe19bdfee7caa9f66c75e51

Architecture review:

    reports/program/2026-09-28-OBSIDIAN-P5D3F-PROMOTION-ARCHITECTURE-REVIEW.md

Blob:

    6bddaf43d3d20f2ba0a0bf9bea6234462432784e

## Delta from prior checkpoint

The functional delta is additive only.

No qualified predecessor runtime or contract was modified.

Added surfaces:

    promotion handoff architecture review
    promotion handoff contract
    promotion handoff contract tests
    promotion handoff documentation
    governed contract re-break runner

No publication runtime was added.

## Contract inventory

Required breakers:

    65

Unique required breakers:

    65

Contract test methods:

    21

## Key architecture decision

P5-D3E does not retain its successful evaluation workspace.

Therefore a future publication transaction cannot safely consume the deleted P5-D3E package.

P5-D3F introduces a separate durable handoff:

    fresh exact candidate evaluation
        ↓
    PASS_SEALED_UNPROMOTED
        ↓
    byte-exact retained copy outside real Vault
        ↓
    PROMOTION-HANDOFF.json
        ↓
    READY_UNAUTHORIZED

P5-D3F does not publish.

## Authority boundary

At this contract candidate:

    handoff_runtime_implementation_authorized = false
    sacrificial_handoff_execution_authorized = false
    production_handoff_execution_authorized = false
    real_vault_write_authorized = false
    current_pointer_creation_authorized = false
    current_pointer_mutation_authorized = false
    p5c2_pointer_primitive_invocation_authorized = false
    p5c3r2_current_writer_invocation_authorized = false
    p5d2_promotion_confirmed_event_authorized = false
    production_promotion_authorized = false
    automatic_promotion_authorized = false
    background_observer_authorized = false
    polling_loop_authorized = false
    graph_search_current_semantics_authorized = false

## Next preflight action

Perform static contract review.

If static review passes:

    local governed P5-D3F contract re-break

must still be executed before contract qualification.

No handoff implementation is authorized before that local PASS.
