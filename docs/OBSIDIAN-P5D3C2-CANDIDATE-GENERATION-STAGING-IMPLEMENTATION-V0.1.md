# OBSIDIAN P5-D3C2 — CANDIDATE GENERATION STAGING IMPLEMENTATION V0.1

Date: 2026-09-27

## 1. Purpose

P5-D3C2 implements and qualifies the packaging mechanics defined by qualified P5-D3C.

It implements:

    verified deterministic projection directory
            ↓
    exact isolated payload copy
            ↓
    payload-manifest
            ↓
    deterministic generation identity
            ↓
    generation-manifest
            ↓
    SEAL.json written last
            ↓
    read-only verification
            ↓
    PASS_SEALED_UNPROMOTED

P5-D3C2 does not build the current-head projection itself.

It does not promote the package.

## 2. Qualified predecessor

P5-D3C qualification commit:

    437ab790f2a1fa4b490344d28cb7b7a2e8116db3

P5-D3C qualification report:

    7390a01e9f7af1bdf9d2f5c5251765ce68faf533

Qualified staging contract:

    79c6a3380a1dcefc49aa4619259baaa8eeadb535

P5-D3C2 runtime contract:

    tools/obsidian_projection/candidate_generation_staging_implementation_contract_v0_1.json

## 3. Runtime scope is intentionally narrower than future production staging

P5-D3C2 permits package roots only below:

    OS temporary directory

This is a qualification boundary.

It prevents the P5-D3C2 packager from selecting arbitrary production paths.

The package identity itself remains host-independent because no temporary absolute path enters:

    generation identity
    generation manifest
    seal
    descriptor

## 4. Input model

The packager receives:

    VerifiedProjectionCandidate

plus one directory already asserted to contain a verified deterministic projection.

Candidate identity includes:

    repository
    branch
    candidate_head
    candidate_tree

    dynamic_inventory_digest_sha256
    semantic_bridge_digest_sha256
    semantic_record_digest_sha256

    projection_contract_version
    projection_tree_digest_sha256
    generated_file_count

    breaker_status = PASS
    determinism_status = PASS

    breaker_manifest_digest_sha256
    breaker_result_digest_sha256
    determinism_evidence_digest_sha256

P5-D3C2 independently recomputes:

    generated_file_count
    projection_tree_digest_sha256

from the supplied projection directory before staging.

## 5. Source projection isolation

The package root may not intersect:

    verified projection input root
    caller-supplied canonical worktree roots
    caller-supplied real Vault roots
    caller-supplied live generation roots

The source projection is never modified.

Only its generated/ subtree is read.

## 6. Payload materialization

Every source payload file must be:

    regular
    non-symlink
    non-junction/reparse
    single-link

Every relative path is validated.

Forbidden payload semantics include:

    absolute path
    backslash path
    parent traversal
    .git component
    .obsidian component
    views component
    CURRENT
    CURRENT.md
    CURRENT.json
    CURRENT.tmp

Each destination file is created using exclusive creation.

Bytes are copied exactly.

The copied file's size and SHA-256 must match the source file immediately after materialization.

## 7. Alias-chain protection

Before every exclusive package write, P5-D3C2 verifies every directory from the destination parent back to the package root.

Any symlink, junction or reparse point fails closed.

This applies to nested payload paths as well as generation metadata.

## 8. Payload manifest

After every payload file exists, P5-D3C2 creates:

    _atds_generation/payload-manifest.json

It is canonical:

    UTF-8
    sorted keys
    compact separators
    LF terminated
    NaN forbidden

It binds every payload file through:

    relative_path
    size_bytes
    sha256

and:

    payload_file_map_digest_sha256

## 9. Generation identity

The packager derives:

    generation_identity_digest_sha256

from the exact P5-D3C identity basis.

Then:

    generation_id =
    gen-<generation_identity_digest_sha256>

The identity contains no:

    timestamp
    UUID
    randomness
    hostname
    PID
    absolute host path

Two identical candidate inputs and identical payloads therefore produce the same generation identity regardless of sandbox location.

## 10. Generation manifest

After payload-manifest completion:

    _atds_generation/generation-manifest.json

is written exclusively.

It binds all candidate/scientific identities, including:

    breaker_status = PASS
    determinism_status = PASS

and:

    package_status = COMPLETE_PENDING_SEAL

No seal exists yet.

## 11. Pre-seal verification

Before writing SEAL.json, the packager verifies:

    exact pre-seal file set
    every payload size
    every payload SHA-256
    payload file-map digest
    payload-manifest digest
    packaged projection_tree_digest
    generation-manifest digest

The packaged projection tree digest is recomputed directly from:

    package/generated/

and must equal the upstream verified projection digest.

This prevents projection_tree_digest from becoming a manifest-only assertion.

## 12. Seal

Only after all pre-seal checks pass is:

    _atds_generation/SEAL.json

created.

It is created exclusively and is the final package mutation.

Seal status:

    SEALED_UNPROMOTED

The seal grants no publication authority.

## 13. Read-only verifier

verify_candidate_generation() is a read-only verifier.

It verifies:

    temp-only package location
    forbidden-root separation
    filesystem alias/reparse safety
    hard-link count
    exact top-level layout
    exact package file set
    canonical manifest bytes
    exact manifest field sets
    every payload size/SHA-256
    payload file-map digest
    payload-manifest digest
    packaged projection_tree_digest
    generation identity
    generation ID
    staging contract binding
    breaker PASS
    determinism PASS
    generation-manifest digest
    exact seal reconstruction

On success it returns a descriptor with:

    verification_status = PASS_SEALED_UNPROMOTED
    promotion_authorized = false

The descriptor contains no package path.

## 14. Sandbox qualification fixture

P5-D3C2 contains a dedicated fixture marked:

    P5D3C2_SANDBOX_PACKAGER_INPUT

Its only purpose is to exercise packaging mechanics.

It contains at least four generated files and nested paths.

It is not:

    a current-head build
    evidence that the historical builder is current-head qualified
    evidence that relation extraction is metadata-only safe
    evidence for production promotion

## 15. Required destructive breakers

The qualification runner first creates one valid control package.

It verifies the control twice and requires that its content digest remain unchanged.

It then copies the control package into isolated mutation roots and applies exactly seven required destructive attacks:

    PAYLOAD_BYTE_MUTATION
    PAYLOAD_FILE_DELETION
    UNMANIFESTED_EXTRA_FILE
    PAYLOAD_MANIFEST_MUTATION
    GENERATION_MANIFEST_MUTATION
    SEAL_MUTATION
    HARD_LINK_ALIAS

Every mutation copy must be rejected as:

    invalid candidate generation

A mutation that survives is qualification failure.

An inability to create the hard-link breaker is infrastructure BLOCKED, not PASS.

## 16. Reparse/symlink runtime probe

The runner also attempts one symlink/reparse mutation.

If the host permits link creation:

    verifier must reject it

If Windows policy or filesystem capability prevents link creation:

    reparse_probe_status =
    CAPABILITY_UNAVAILABLE

This does not waive the implementation/unit/static reparse breakers.

## 17. Control-package preservation

All destructive mutations occur only on copies.

After all attacks, the original control package must still verify to the exact same descriptor.

This is a direct breaker against accidental shared hard-link/copy aliasing between control and mutation packages.

## 18. Sandbox report

Success schema:

    ATDS_OBSIDIAN_P5D3C2_SANDBOX_REPORT_V0_1

Success status:

    PASS_SANDBOX_SEALED_UNPROMOTED

The report binds:

    generation_id
    candidate_generation_digest_sha256
    payload_file_count
    payload_file_map_digest_sha256
    repeated verifier equality
    unchanged control content digest
    passed mutation registry
    reparse probe status

and states:

    real_vault_modified = false
    current_pointer_created = false
    production_promotion_authorized = false
    sandbox_retained = false

No absolute sandbox path or host identity is emitted.

## 19. Sandbox cleanup

The sandbox is sacrificial.

After evidence is computed, the temporary sandbox is deleted.

Deletion does not convert that destroyed package into a live or reusable candidate.

Qualification concerns the correctness of staging/verifying mechanics demonstrated before cleanup.

## 20. P5-D3C2 non-authorizations

P5-D3C2 still does not authorize:

    current-head builder adaptation
    relation-adapter execution
    finite candidate-evaluation orchestrator
    production promotion
    CURRENT mutation
    real Vault writes
    background observer
    polling
    Windows startup/task/service persistence
    Graph/Search CURRENT semantics

## 21. Next governed frontier

If P5-D3C2 qualifies, the next implementation frontier is:

    P5-D3D —
    FINITE CANDIDATE EVALUATION ORCHESTRATOR
    WITH CURRENT-HEAD BUILDER ADAPTATION

P5-D3D must close the remaining current-head projection builder/relation boundary before it can feed a real projection into this qualified packager.

Only later gates may connect qualification to promotion.
