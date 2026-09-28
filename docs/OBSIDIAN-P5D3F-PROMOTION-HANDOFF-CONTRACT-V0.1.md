# OBSIDIAN P5-D3F — PROMOTION HANDOFF CONTRACT V0.1

Date: 2026-09-28

## 1. Objective

P5-D3F defines the finite governed handoff between:

    a freshly QUALIFIED exact-head candidate

and:

    a durable retained SEALED_UNPROMOTED package
    ready to be considered by a later publication transaction

P5-D3F does not publish.

Its successful terminal status is deliberately:

    PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED

The contract authority is:

    tools/obsidian_projection/promotion_handoff_contract_v0_1.json

## 2. Why this boundary exists

P5-D3E proved a real end-to-end exact-head evaluation.

However its successful sandbox is intentionally ephemeral:

    candidate_repository_retained = false
    evaluation_workspace_retained = false

The sealed package generated inside P5-D3E is therefore destroyed during successful cleanup.

Publication cannot safely assume that package still exists.

P5-D3F closes that gap without reopening P5-D3E.

## 3. Architecture sequence

The finite architecture is now:

    P5-D3E
    qualified evaluator architecture
        ↓
    P5-D3F
    durable promotion handoff
        ↓
    P5-D3G
    future finite live publication transaction
        ↓
    P5-D4
    future bounded observer loop

P5-D4 is not renamed.

Its preregistered meaning remains:

    BOUNDED_OBSERVER_LOOP_CANDIDATE

## 4. Existing authorities

P5-D3F binds to already-qualified authorities rather than re-defining them.

### Filesystem visibility

P5-C2 selected:

    IMMUTABLE_GENERATION_ATOMIC_POINTER

No directory-swap fallback is implicitly authorized.

### Obsidian-open compatibility

P5-C3R2 qualified:

    CURRENT.md
    CURRENT.tmp
    os.replace(CURRENT.tmp, CURRENT.md)

with bounded Windows sharing-conflict handling.

That writer is not invoked by P5-D3F.

### Logical observer state

P5-D2 defines:

    EVALUATION_PASSED
    PROMOTION_CONFIRMED

as different facts.

P5-D3F may produce evaluation PASS evidence.

It may not emit:

    PROMOTION_CONFIRMED

### Sealed package

P5-D3C2 is the only package authority.

The inner package remains exactly:

    generated/
    _atds_generation/

and retains:

    PASS_SEALED_UNPROMOTED

P5-D3F metadata is outside that package.

## 5. Input

P5-D3F requires an exact prepared candidate repository.

Required identity:

    repository =
    thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

    branch =
    integration/system-v1

    candidate HEAD =
    full lowercase 40-hex

    candidate TREE =
    full lowercase 40-hex

The candidate repository must be:

    isolated
    exact-HEAD
    exact-TREE
    clean

Network resolution occurs outside the handoff core.

The handoff core itself is network-free.

## 6. Fresh finite evaluation

A prior historical PASS is not enough by itself.

P5-D3F requires a fresh finite evaluation of the candidate through the exact qualified P5-D3D evaluator.

Required:

    outcome = QUALIFIED
    failure_code = null
    Build A == Build B
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count
    candidate package = PASS_SEALED_UNPROMOTED

All required scientific identity digests must be present.

## 7. Promotion staging

Candidate production path:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING

This is not the real Vault.

The staging root must:

    not equal the real Vault
    not be inside the real Vault
    not contain the real Vault
    not be a Git repository
    reject alias/reparse paths
    reject symlinks/junctions
    use a fresh generation handoff target

A sacrificial equivalent root may be used for implementation qualification before any persistent staging use is authorized.

## 8. Handoff package layout

Conceptual layout:

    packages/
        <generation_id>/
            package/
                generated/
                _atds_generation/
            PROMOTION-HANDOFF.json

The package directory is byte-for-byte P5-D3C2 package content.

PROMOTION-HANDOFF.json is a wrapper-level record.

It must never be injected into:

    package/

because that would invalidate the sealed package.

## 9. Copy semantics

Before copy:

    verify_candidate_generation(source_package)

must return:

    PASS_SEALED_UNPROMOTED

Then copy:

    every path exactly
    every byte exactly

Forbidden:

    hard links
    symlinks
    junctions
    reparse points
    non-regular payload entries

After copy:

    verify_candidate_generation(destination_package)

must return the same immutable identity.

P5-D3F must also recompute a byte-tree digest before and after copy and require exact equality.

The copied package may not depend on the evaluator workspace continuing to exist.

Any future publication consumer must perform a fresh read-only verification of the retained handoff before publication planning or authorization.

## 10. PROMOTION-HANDOFF.json

This record is written after the package copy and verification.

It binds the candidate, scientific evidence and package identity.

It includes:

    candidate_head
    candidate_tree
    generation_id
    candidate_generation_digest_sha256
    dynamic_inventory_digest_sha256
    semantic_bridge_digest_sha256
    semantic_record_digest_sha256
    projection_tree_digest_sha256
    breaker_manifest_digest_sha256
    breaker_result_digest_sha256
    determinism_evidence_digest_sha256
    payload_file_map_digest_sha256
    package_byte_tree_digest_sha256

It also explicitly carries:

    publication_authorized = false
    current_pointer_mutation_authorized = false
    real_vault_write_authorized = false
    promotion_confirmed_event_authorized = false
    handoff_status = READY_UNAUTHORIZED

## 11. Handoff verification

The P5-D3F verifier must be read-only.

It must independently:

    validate exact wrapper layout
    reverify the P5-D3C2 package
    recompute package byte-tree digest
    validate canonical handoff JSON
    reject extra/missing fields
    cross-check candidate identity
    cross-check scientific identity
    cross-check generation identity
    require every publication authority bit false

Repeated verification must not mutate the handoff.

## 12. Success

Only this success is allowed:

    PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED

Success means:

    exact candidate qualified
    package sealed
    retained copy exact
    handoff record exact
    no real Vault mutation
    no CURRENT creation
    no promotion
    no PROMOTION_CONFIRMED

It does not mean:

    ready to auto-publish

It means:

    technically eligible to enter a later separately governed
    publication decision.

## 13. Rejected and blocked candidates

Candidate evaluator:

    REJECTED
        ↓
    FAIL_CANDIDATE_REJECTED

Candidate evaluator:

    BLOCKED
        ↓
    BLOCKED_CANDIDATE_EVALUATION

These outcomes are not interchangeable.

Neither may create a handoff-ready success artifact.

## 14. Publication authority remains closed

P5-D3F V0.1 contract itself authorizes only contract tests.

It does not yet authorize even its handoff runtime.

Explicitly forbidden:

    real Vault writes
    CURRENT creation
    CURRENT mutation
    P5-C2 promotion primitive invocation
    P5-C3R2 CURRENT writer invocation
    P5-D2 PROMOTION_CONFIRMED
    production promotion
    automatic promotion
    background observer
    polling
    startup persistence
    scheduled task
    Windows service
    Graph/Search CURRENT semantics

## 15. Future P5-D3G

Only after P5-D3F implementation and sacrificial staging qualification may P5-D3G be opened.

P5-D3G will need a separate contract for:

    read-only publication plan
    explicit bounded human authorization
    single-writer ownership
    previous CURRENT capture
    immutable live generation materialization
    complete target verification
    CURRENT.tmp exclusive write
    atomic CURRENT.md replace
    P5-C3R2 retry semantics
    read-after-write verification
    crash recovery
    rollback
    physical/logical confirmation ordering

No P5-D3G runtime should be written before that contract exists.

## 16. Graph/Search

Publication mechanics are not Graph/Search semantics.

Multiple immutable generations may coexist physically.

P5-D3F makes no claim that Obsidian Graph/Search already filters to CURRENT.

That remains:

    P6 CONTROLLED KNOWLEDGE GRAPH ARCHITECTURE

## 17. Next gate

After this contract passes its own static and local re-break:

    P5-D3F —
    FINITE PROMOTION HANDOFF
    IMPLEMENTATION + SACRIFICIAL STAGING QUALIFICATION

No real Vault write is part of that next gate.
