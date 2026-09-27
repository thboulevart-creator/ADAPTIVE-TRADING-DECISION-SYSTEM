# OBSIDIAN P5-D3E — FIRST REAL EXACT-HEAD RUN PREFLIGHT

Date: 2026-09-27

## Status

Evidence-only preflight.

This document does not execute or qualify a real candidate.

## Qualified P5-D3E implementation

Qualification commit:

    1e03d539d48c0fb4760d1b6091e1b2faa125042b

Qualified functional candidate:

    7c6ecec2498d48c4623ecd40aed6c3816f4930b9

P5-D3E contract blob:

    ae4b1691fae16fcd1616e265a089670b9654db4a

P5-D3E harness blob:

    bd7f63b08432a53eaff5deeb2147396eb60d723f

P5-D3E harness-test blob:

    fe47910cf7f10a09021d958d7ae60693d0def4bf

P5-D3E adversarial-test blob:

    6b159ede31fb26ac366f9c69cd72256ee553753c

Qualified P5-D3D evaluator blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

## Context-only current monitored-branch observation

At preflight time GitHub reported:

    integration/system-v1 HEAD:
    b737dc101a3efbce5ad073671c72871ba0ffca27

    tree:
    cc465e31cd2f3c232268d0e1f0a3fac99baae961

This is contextual only.

The real P5-D3E run must not hardcode these identities.

It must resolve integration/system-v1 again through the qualified harness immediately before evaluation.

## Authorized real-run chain

    resolve_real_candidate()
        ↓
    one governed fetch of integration/system-v1
        ↓
    freeze exact HEAD + TREE
        ↓
    run_real_exact_head_qualification()
        ↓
    qualified P5-D3D evaluator
        ↓
    real DynamicInventory
        ↓
    real semantic bridge
        ↓
    real Build A / Build B
        ↓
    real CHP-B01..B12
        ↓
    P5-D3C2 SEALED_UNPROMOTED package
        ↓
    post-package read-only reverification
        ↓
    QUALIFIED / REJECTED / BLOCKED

## PASS adjudication

P5-D3E PASS requires:

    status = PASS_REAL_EXACT_HEAD_FINITE_EVALUATION
    candidate_outcome = QUALIFIED
    failure_code = null
    candidate_generation_verification_status = PASS_SEALED_UNPROMOTED
    package_reverification_status = PASS_SEALED_UNPROMOTED
    package_reverification_digest_matches = true
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count
    projection_a_tree_digest_sha256 = projection_b_tree_digest_sha256
    p5d2_result_event_emitted = true
    live_projection_head_unchanged = true
    real_candidate_evaluated = true
    candidate_resolution_network_fetch_performed = true
    evaluation_network_fetch_performed = false
    candidate_repository_clean_after = true
    control_repository_clean_after = true
    real_vault_modified = false
    current_pointer_created = false
    production_promotion_authorized = false
    candidate_repository_retained = false
    evaluation_workspace_retained = false

## Non-PASS outcomes

Real candidate rejection:

    FAIL_REAL_CANDIDATE_REJECTED

Infrastructure/evidence block:

    BLOCKED_REAL_EXACT_HEAD_EVALUATION

Governance violation:

    FAIL_P5D3E_GOVERNANCE_VIOLATION

None may be relabelled PASS.

## Publication boundary

Still unauthorized:

    production promotion
    CURRENT mutation
    real Vault writes
    background observer
    polling
    Windows startup/task/service
    Graph/Search CURRENT semantics

## Next action

Execute the qualified P5-D3E CLI exactly once against the then-current integration/system-v1 candidate and persist the user-reported result before any further governance decision.
