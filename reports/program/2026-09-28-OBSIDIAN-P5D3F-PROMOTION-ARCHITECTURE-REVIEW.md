# OBSIDIAN P5-D3F — PROMOTION ARCHITECTURE REVIEW

Date: 2026-09-28

## Status

Architecture review only.

This record does not authorize runtime publication, CURRENT mutation, real-Vault writes, automatic promotion, background execution, polling, Windows persistence, or Graph/Search CURRENT semantics.

## 1. Starting boundary

P5-D3E is CLOSED / QUALIFIED.

The qualified finite real exact-head chain has demonstrated:

    exact integration/system-v1 HEAD
        ↓
    frozen HEAD/TREE
        ↓
    isolated candidate repository
        ↓
    deterministic current-head projection
        ↓
    Build A == Build B
        ↓
    preregistered breakers PASS
        ↓
    P5-D3C2 candidate package
        ↓
    PASS_SEALED_UNPROMOTED
        ↓
    read-only package reverification
        ↓
    candidate outcome QUALIFIED

The first real exact-head qualification was persisted at:

    a24c248a68f530f82a1f0c578036ccd4b8a54fee

Real candidate:

    89710b879751d7fcebccf75cd03e64368f1b0e96

Real candidate tree:

    dc85bdb0708f4980e3a0cead0f15c6d077f90290

## 2. Existing qualified authorities relevant to publication

### P5-C2 — filesystem publication primitive

Qualification report blob:

    a928598182b25d110c9040c62d846bf9018ac3ed

Selected primitive:

    IMMUTABLE_GENERATION_ATOMIC_POINTER

Rejected / unsupported alternatives:

    DIRECTORY_TWO_RENAME_SWAP
        FAIL / PermissionError

    WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE
        NOT_SUPPORTED / MOVEFILEEX_ERROR_5

P5-C2 demonstrated in its bounded Windows/OneDrive sandbox:

    250 / 250 pointer promotions
    >= 5000 reader samples
    zero mixed generation
    zero missing entrypoint
    zero partial generation
    zero parse error

P5-C2 qualifies only the filesystem primitive.

It does not authorize production promotion.

### P5-C3R2 — Obsidian-open pointer compatibility

Qualified runtime candidate:

    b5f3a8de061772e15bc94b20095d419130c20781

Qualification report blob:

    fd54a78abde8342c6da708d3a4096b4d0b267905

Qualified runtime primitives include:

    CURRENT.md
    CURRENT.tmp
    os.replace(CURRENT.tmp, CURRENT.md)

with bounded write retry only for:

    PermissionError
    winerror in {5, 32}

and bounded reader-only fallback for:

    PermissionError
    winerror is None
    errno == EACCES (13)

P5-C3R2 demonstrated Obsidian-open compatibility in a sacrificial Vault.

It still explicitly leaves:

    production_promotion_authorized = false
    continuous_observer_authorized = false
    graph_current_pointer_semantics_qualified = false

### P5-D2 — logical observer state

Qualified candidate:

    b7451db65a555c1828a4113abfb9c61fafda0b90

Runtime blob:

    fd212f61ec38332b677110f40265638af55a73e2

Qualification report blob:

    68cda09d273f19a2a93e1fcd9b0c393e72cd5a35

P5-D2 establishes:

    qualification != promotion

and:

    PROMOTION_CONFIRMED

is only a logical external confirmation after a future governed component has already confirmed physical promotion.

P5-D2 performs no promotion I/O.

### P5-D3C2 — sealed candidate package

Qualified candidate:

    41d19df20dc5214e3b64098dd72519a23ea6e010

Packager/verifier blob:

    e2e5867536f4f9c7dec475c6696737249536ff39

Qualification report blob:

    d1ffea5fefc8845831c11a153a0e17492401ef60

Successful package state:

    PASS_SEALED_UNPROMOTED

The package is immutable after SEAL.json and is independently read-only verifiable.

### P5-D3E — real exact-head evaluator

Qualified implementation candidate:

    7c6ecec2498d48c4623ecd40aed6c3816f4930b9

Harness blob:

    bd7f63b08432a53eaff5deeb2147396eb60d723f

P5-D3E qualifies real exact-head evaluation but deliberately reports:

    candidate_repository_retained = false
    evaluation_workspace_retained = false

## 3. Critical architecture gap discovered

A direct transition:

    P5-D3E QUALIFIED
        ↓
    live promotion

is not currently valid.

Reason:

The P5-D3E candidate package exists only inside the sacrificial evaluation workspace.

Successful P5-D3E cleanup removes:

    candidate repository
    evaluation workspace
    candidate package

Therefore the system has qualified evidence that a real candidate CAN produce a valid SEALED_UNPROMOTED package, but it does not leave behind a durable package that a later publication transaction can consume.

Reopening P5-D3E merely to retain its sandbox would weaken an already-qualified cleanup boundary and is not preferred.

## 4. Architecture decision

Split publication into two finite governed boundaries before any bounded observer loop.

### P5-D3F — FINITE PROMOTION HANDOFF

Purpose:

Re-evaluate an exact candidate through already-qualified components and materialize one durable, immutable, independently verified SEALED_UNPROMOTED package in a dedicated promotion-staging namespace OUTSIDE the real Vault.

Output state:

    PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED

The word UNAUTHORIZED is mandatory.

P5-D3F does NOT mutate CURRENT and does NOT publish to the real Vault.

### P5-D3G — FINITE LIVE PUBLICATION TRANSACTION

Future boundary only.

It will consume exactly one P5-D3F handoff and an explicit bounded human authorization.

Only P5-D3G may eventually be allowed to:

    copy a complete immutable generation into the machine-owned live generation namespace
    verify it completely
    atomically replace CURRENT.md
    read-after-write verify CURRENT
    rollback CURRENT if required
    emit P5-D2 PROMOTION_CONFIRMED only after physical publication is confirmed

P5-D3G is NOT opened by this review.

### P5-D4 — BOUNDED OBSERVER LOOP

P5-D4 keeps its already-preregistered meaning from prior contracts:

    BOUNDED_OBSERVER_LOOP_CANDIDATE

It must not be reused as the finite publication contract name.

Automatic repeated orchestration remains after the finite handoff and finite publication transactions are individually qualified.

## 5. Why P5-D3F must exist

P5-D3F provides a clean authority handoff between:

    finite evaluation evidence

and:

    physical publication input

without changing P5-D3E.

It prevents a future publication runtime from:

- rebuilding an unverified generation ad hoc;
- assuming the deleted P5-D3E sandbox still exists;
- publishing directly from Build A or Build B;
- bypassing P5-D3C2 sealing;
- silently regenerating different bytes during publication;
- using P5-C2 synthetic fixture builders as production content;
- claiming publication authority merely because evaluation passed.

## 6. P5-D3F target artifact

A P5-D3F handoff is a wrapper around an unchanged P5-D3C2 package.

Conceptual layout:

    promotion-staging/
        packages/
            <generation_id>/
                package/
                    generated/
                    _atds_generation/
                        payload-manifest.json
                        generation-manifest.json
                        SEAL.json
                PROMOTION-HANDOFF.json

The inner package must remain byte-identical to the package accepted by:

    verify_candidate_generation()

PROMOTION-HANDOFF.json is outside the sealed package.

It does not mutate or extend the P5-D3C2 package contract.

## 7. Handoff identity

The handoff must bind at least:

    source_repository
    source_branch
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
    P5-D3C2 package verification status
    P5-D3E / evaluator authority identities
    package byte-tree digest
    handoff contract identity

It must also state explicitly:

    publication_authorized = false
    current_pointer_mutation_authorized = false
    real_vault_write_authorized = false
    promotion_confirmed_event_authorized = false

## 8. Handoff materialization semantics

The intended future implementation sequence is:

    exact candidate HEAD/TREE supplied
        ↓
    isolated candidate repository
        ↓
    qualified finite evaluator
        ↓
    require outcome QUALIFIED
        ↓
    require PASS_SEALED_UNPROMOTED
        ↓
    read-only verify package
        ↓
    copy package byte-exact to fresh handoff target
        ↓
    reject hard links / symlinks / junctions / reparse points
        ↓
    read-only verify copied package
        ↓
    require copied package descriptor == source package descriptor
        ↓
    compute wrapper byte-tree digest
        ↓
    write PROMOTION-HANDOFF.json last
        ↓
    read-only verify handoff
        ↓
    PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED

No CURRENT file is created.

No real Vault path is modified.

## 9. Promotion-staging root

The first qualification should use a dedicated sacrificial / machine-owned sibling root, not the live Vault.

Target environment candidate:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING

Required properties:

    same OneDrive parent context as the live Vault
    must not equal the live Vault
    must not be inside the live Vault
    live Vault must not be inside it
    must not be a Git repository
    must reject symlink / junction / reparse aliases
    fresh target generation directory required
    no overwrite of a different existing handoff

An identical pre-existing handoff may eventually be treated as an idempotent no-op only after exact byte and identity verification.

## 10. Why live publication is not implemented in P5-D3F

The physical publication transaction has additional failure classes that do not belong in materialization:

    live generation copy interrupted
    pre-existing generation collision
    stale CURRENT
    malformed CURRENT
    CURRENT.tmp exists
    two writers
    pointer replace sharing conflict
    crash after pointer commit
    post-commit verification failure
    rollback
    logical confirmation ordering

These require their own contract and breakers.

Combining them with handoff materialization would make the first production-write boundary too large to falsify cleanly.

## 11. Future P5-D3G publication architecture

P5-D3G should be contract-first and finite.

Expected high-level transaction:

    verified P5-D3F handoff
        ↓
    read-only publication plan
        ↓
    exact human authorization bound to plan digest
        ↓
    acquire single-writer authority
        ↓
    verify old CURRENT / previous-current identity
        ↓
    materialize target immutable generation in live machine namespace
        ↓
    byte/digest verify target generation
        ↓
    create CURRENT.tmp exclusively
        ↓
    fsync CURRENT.tmp
        ↓
    atomic os.replace(CURRENT.tmp, CURRENT.md)
        ↓
    bounded P5-C3R2-compatible retry
        ↓
    read-after-write verify CURRENT and referenced generation
        ↓
    only then physical promotion is CONFIRMED
        ↓
    only then P5-D2 PROMOTION_CONFIRMED may be emitted

If post-commit verification cannot confirm the new CURRENT, the transaction must enter a separately defined recovery / rollback state rather than pretending failure occurred before publication.

## 12. Rollback rule

Rollback must be designed before P5-D3G is authorized.

At minimum it must bind:

    previous CURRENT bytes
    previous generation ID
    previous generation digest
    previous candidate HEAD if known
    exact rollback target
    rollback authorization
    atomic pointer restoration
    read-after-rollback verification

The previous immutable generation may not be deleted before the new publication transaction and its rollback window are closed.

## 13. Graph/Search boundary

The P5-C2 and P5-C3R2 pointer architecture does not qualify native Obsidian Graph/Search semantics for multiple immutable generations.

Therefore:

    P6 CONTROLLED KNOWLEDGE GRAPH ARCHITECTURE

remains separate.

P5-D3F and future P5-D3G may qualify controlled publication mechanics without claiming that all Obsidian visual/search surfaces already obey CURRENT-generation filtering.

## 14. Decision

The next exact governed frontier is:

    P5-D3F —
    FINITE PROMOTION HANDOFF /
    RETAINED SEALED GENERATION CONTRACT V0.1

It is contract-only first.

No runtime publication is authorized.

## 15. Sequence

    architecture review
        ↓
    P5-D3F contract
        ↓
    P5-D3F contract breakers
        ↓
    static review
        ↓
    local governed contract re-break
        ↓
    contract qualification
        ↓
    minimal P5-D3F implementation candidate
        ↓
    sacrificial staging qualification
        ↓
    only then P5-D3G contract

P5-D4 remains reserved for the bounded observer loop.
