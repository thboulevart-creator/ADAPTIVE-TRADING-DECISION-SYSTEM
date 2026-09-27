# OBSIDIAN P5-D3C — CANDIDATE GENERATION STAGING CONTRACT STATIC REVIEW

Date: 2026-09-27

## Review status

Same-assistant static review.

It is not independent.
It is not runtime evidence.
It does not qualify P5-D3C.
It does not authorize P5-D3C2.

## Functional candidate reviewed

    f3dc4b582fadff37ffb37108ec677ea88de7dad0

Branch:

    feat/obsidian-projection-p5d3c-candidate-generation-staging-contract-v0.1

Evidence-only preflight commit:

    45a5609da8ab2f46104a403068c85af8daf01221

## Exact candidate artifacts

Contract:

    79c6a3380a1dcefc49aa4619259baaa8eeadb535

Contract breakers:

    8a986e87c72f8556bcac46e167026db5d849d8d3

Documentation:

    d23cfd1d0ed520696a57dc104540721e683760ab

## Delta review

Relative to P5-D3B qualification, P5-D3C adds exactly:

- one staging contract;
- one contract-breaker module;
- one documentation file.

No previously qualified file is modified.

Static review: PASS.

## Predecessor identity

    P5-D3B qualification commit pinned                 PASS
    P5-D3B qualification report pinned                 PASS
    P5-D3B bridge contract pinned                      PASS
    P5-D3B bridge implementation pinned                PASS
    P5-C2 promotion contract pinned                    PASS
    P5-C2 qualification report pinned                  PASS
    existing integrity implementation pinned           PASS

## P5-C2 semantic reuse boundary

The contract correctly distinguishes:

    qualified publication property
        complete immutable generation before pointer publication

from:

    experimental synthetic representation
        GEN_A / GEN_B
        fixed 128 files
        generation_id embedded in each JSON payload

The contract explicitly forbids reusing:

    build_generation()

as the real current-head packager and:

    validate_generation_dir()

as the real package verifier.

It also forbids CURRENT creation during P5-D3C.

Static review: PASS.

## Input qualification boundary

P5-D3C requires one exact verified projection candidate with:

    exact repository/branch
    exact candidate HEAD/tree
    dynamic inventory digest
    semantic bridge digest
    semantic record digest
    projection contract version
    projection tree digest
    generated file count
    breaker PASS
    determinism PASS
    breaker manifest/result digests
    determinism evidence digest

A partial or unverified projection is forbidden.

Static review: PASS.

## Staging isolation

Required:

    fresh empty root                                  PASS
    outside canonical worktree                        PASS
    outside real Vault                                PASS
    outside live generation namespace                 PASS
    not a Git repository                              PASS
    no symlink/junction/reparse escape                 PASS
    no hard-linked payload files                      PASS
    regular single-link payload files                 PASS
    no pre-existing target                            PASS
    no overwrite in place                             PASS
    canonical worktree unchanged                      PASS
    source checkout unchanged                         PASS

## Package layout

Exact package roots:

    generated/
    _atds_generation/

Exact machine metadata:

    payload-manifest.json
    generation-manifest.json
    SEAL.json

Explicitly forbidden:

    CURRENT
    CURRENT.md
    CURRENT.json
    CURRENT.tmp
    views
    .obsidian
    .git

Unmanifested extra files are forbidden.

Static review: PASS.

## Payload semantics

The payload is defined as an exact path/byte copy of an already verified deterministic generated tree.

Required:

    all generated files included                       PASS
    no silent file drop                                PASS
    no extra payload file                              PASS
    generated_file_count equality                      PASS
    relative path identity preserved                   PASS
    payload byte identity preserved                    PASS
    no source checkout files                           PASS
    no raw source blobs                                PASS
    no human views                                     PASS
    no .obsidian                                       PASS

Path traversal, absolute paths, backslashes and duplicate paths are rejected by contract.

## Dual digest model

The contract deliberately keeps:

    projection_tree_digest_sha256

as upstream builder-owned evidence, and separately defines:

    payload_file_map_digest_sha256

over every packaged generated file.

This avoids silently redefining the historical projection-tree algorithm while still byte-binding the complete staged payload.

Static review: PASS.

## Payload manifest

Schema:

    ATDS_OBSIDIAN_CANDIDATE_PAYLOAD_MANIFEST_V0_1

The manifest:

    covers all payload files                           PASS
    excludes machine manifests                         PASS
    excludes itself                                    PASS
    bytewise-sorts file rows                           PASS
    binds relative path                                PASS
    binds file size                                    PASS
    binds SHA-256                                      PASS
    has an independent manifest digest                 PASS

## Generation identity

Generation identity includes all required scientific/evaluation evidence:

    candidate HEAD/tree                                PASS
    inventory digest                                   PASS
    bridge digest                                      PASS
    semantic-record digest                             PASS
    projection contract                                PASS
    projection tree                                    PASS
    generated count                                    PASS
    payload map                                        PASS
    payload manifest                                   PASS
    breaker PASS status                                PASS
    determinism PASS status                            PASS
    breaker manifest/result digests                    PASS
    determinism evidence digest                        PASS
    exact staging contract blob                        PASS

Generation ID is deterministically derived from the identity digest.

Forbidden from identity:

    wall clock
    UUID
    randomness
    host identity
    absolute local path

Static review: PASS.

## Generation manifest

The generation manifest explicitly records:

    breaker_status = PASS
    determinism_status = PASS

rather than relying only on opaque evidence digests.

Before seal:

    package_status = COMPLETE_PENDING_SEAL

Volatile host/runtime fields are forbidden.

Static review: PASS.

## Seal ordering and semantics

The sealing sequence requires:

    complete payload
        before payload manifest

    verified payload
        before seal

    generation manifest
        before seal

    seal
        as final package mutation

The seal is exclusive-create only.

Seal status:

    SEALED_UNPROMOTED

The seal binds:

    generation identity
    payload manifest digest
    generation manifest digest
    payload file-map digest
    projection-tree digest
    exact candidate HEAD/tree
    exact staging contract blob

It grants no promotion authority and claims no live visibility.

Static review: PASS.

## Candidate-generation digest

Candidate generation digest is defined as:

    SHA256(exact canonical SEAL.json bytes)

This creates one deterministic package identifier without introducing a self-hashing manifest cycle.

Static review: PASS.

## Immutability semantics

The contract correctly claims:

    logical immutability

and explicitly does not claim:

    OS-level immutable filesystem attribute

After a valid seal, any payload/manifest mutation, deletion or extra file invalidates the package.

Repair or reseal in place is forbidden.

A failed package requires a new fresh root.

Static review: PASS.

## Verification semantics

Verification is explicitly read-only.

Required checks cover:

    exact file set
    schemas
    generation identity
    candidate HEAD/tree
    scientific digests
    breaker/determinism PASS
    payload count
    every file size
    every file SHA-256
    file-map digest
    manifest digests
    seal
    links/reparse/hard-link anomalies
    extra files

Outcome vocabulary preserves:

    PASS_SEALED_UNPROMOTED
    FAIL_INVALID_CANDIDATE_GENERATION
    BLOCKED_VERIFICATION_INFRASTRUCTURE

Candidate evidence and infrastructure failures may not be conflated.

Static review: PASS.

## Descriptor semantics

The descriptor may expose deterministic candidate identity only.

Required:

    verification_status = PASS_SEALED_UNPROMOTED
    promotion_authorized = false

Forbidden:

    absolute stage path
    volatile host metadata

Static review: PASS.

## Existing integrity primitive reuse

The contract allows narrow reuse of generic integrity mechanics:

    SHA-256 bytes
    regular-file checks
    single-link checks
    reparse/symlink/junction checks
    deterministic file-entry digest semantics

It does not let legacy manifest vocabulary define current-head scientific identity.

In particular:

    pilot_inventory_digest_sha256

cannot replace:

    dynamic_inventory_digest_sha256

Static review: PASS.

## Publication boundary

The package is explicitly:

    not live
    not CURRENT
    not promoted
    not claimed Obsidian-visible

P5-D3C forbids:

    pointer write
    P5-C2 promotion invocation
    live-generation copy
    real Vault write

Static review: PASS.

## Current-head builder gap preserved

P5-D3C does not claim the historical builder/relation stack is current-head qualified.

The later builder adaptation must still preserve the qualified P5-D3B boundary:

    METADATA_ONLY downstream body read = false

Static review: PASS.

## Runtime non-authorizations

P5-D3C boundary keeps false for:

    staging packager implementation                    PASS
    staging verifier implementation                    PASS
    staging execution                                  PASS
    current-head builder adaptation                    PASS
    relation adapter execution                         PASS
    finite evaluator                                   PASS
    production promotion                               PASS
    CURRENT mutation                                   PASS
    real Vault write                                   PASS
    background observer                                PASS
    polling                                            PASS
    Windows startup/task/service                       PASS
    Graph/Search CURRENT semantics                     PASS

## Breaker inventory

Required breakers:

    108

Unique required breakers:

    108

Persisted contract-test methods:

    26

These are static repository facts, not executed evidence.

## Next-gate ordering

The contract inserts an explicit implementation/qualification boundary before orchestration:

    P5-D3C2
      CANDIDATE GENERATION STAGING IMPLEMENTATION
      AND SANDBOX QUALIFICATION

then:

    P5-D3D
      FINITE CANDIDATE EVALUATION ORCHESTRATOR
      WITH CURRENT-HEAD BUILDER ADAPTATION

This avoids implementing the packager implicitly inside the orchestrator.

## Limitation

No packager, verifier, staging root, payload copy, manifest, seal, CURRENT file, Vault mutation or promotion primitive was executed by this static review.

## Verdict

**STATIC REVIEW PASS — LOCAL RE-BREAK REQUIRED.**

P5-D3C remains unqualified until the exact functional candidate:

    f3dc4b582fadff37ffb37108ec677ea88de7dad0

passes the governed local re-break.
