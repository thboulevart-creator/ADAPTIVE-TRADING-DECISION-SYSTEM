# OBSIDIAN P5-D3C — CANDIDATE GENERATION STAGING CONTRACT V0.1

Date: 2026-09-27

## 1. Purpose

P5-D3C defines the real candidate-generation package used after one exact candidate HEAD has:

- a qualified current-head semantic bridge;
- a deterministic projection candidate;
- a passing double-build determinism gate;
- a preregistered candidate-breaker PASS.

P5-D3C is contract-and-breakers only.

It does not yet implement the packager or verifier.

The package remains:

    SEALED_UNPROMOTED

and is neither CURRENT nor live.

## 2. Qualified predecessor

P5-D3B qualification commit:

    51dfa30a9fcca4f012f80410f24f95007d2cf2e6

P5-D3B qualification report:

    94fbe40ffde900040c9a784b205c37e76b7ef834

P5-D3B bridge contract:

    7015db1206cd40b703795d12519707a6455b4fc3

P5-D3B bridge implementation:

    ff3c2dd232487594a5283a9ab7750780ac098f2d

P5-D3C does not reopen P5-D3B.

## 3. What P5-C2 actually qualified

P5-C2 qualified, in its tested Windows/OneDrive sandbox environment:

    immutable complete generation directories
        +
    atomic CURRENT pointer replacement

The reusable architectural property is:

    COMPLETE GENERATION FIRST
        ↓
    PUBLICATION SECOND

P5-D3C preserves that ordering.

P5-D3C does NOT reuse the P5-C2 synthetic fixture generator as a real projection packager.

## 4. Why P5-C2 build_generation() is not the real packager

The P5-C2 experimental generator creates:

    128 synthetic JSON files
    8 synthetic directories
    GEN_A / GEN_B fixture identities
    generation_id embedded inside every synthetic payload

Its verifier also assumes that synthetic representation.

Those conditions prove filesystem visibility behavior for the experiment.

They do not define the identity of a real ATDS projection.

Therefore P5-D3C explicitly forbids treating:

    build_generation()

or:

    validate_generation_dir()

as the real candidate-generation package implementation.

## 5. Candidate input

P5-D3C receives one already verified deterministic projection candidate.

Required identity includes:

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

The selected payload must come from one of two already proven byte-identical deterministic builds.

P5-D3C does not perform that build itself.

## 6. Fresh staging root

Every candidate package begins in a fresh empty root.

The root must be outside:

    canonical Git worktree
    real Obsidian Vault
    any live generation directory

The root must not be a Git repository.

Pre-existing targets are forbidden.

Overwrite-in-place is forbidden.

Symlink, junction or reparse escape is forbidden.

Hard-linked payload files are forbidden.

Payload files must be regular single-link files.

## 7. Package layout

The package root contains exactly two top-level namespaces:

    generated/
    _atds_generation/

The projection payload remains under:

    generated/

Machine generation metadata remains under:

    _atds_generation/

Exact machine files:

    _atds_generation/payload-manifest.json
    _atds_generation/generation-manifest.json
    _atds_generation/SEAL.json

Forbidden package paths include:

    CURRENT
    CURRENT.md
    CURRENT.json
    CURRENT.tmp
    views/
    .obsidian/
    .git/

P5-D3C therefore cannot accidentally become a publication step.

## 8. Payload semantics

The generated payload is an exact byte-for-byte copy of the already verified deterministic projection output.

For every payload file:

    relative path preserved
    bytes preserved
    size preserved
    SHA-256 preserved

Every generated file must be present.

No extra payload file may appear.

The package may not contain:

    source repository files
    raw canonical source blobs
    human views
    Obsidian configuration

The payload is projection output only.

## 9. Payload manifest

Schema:

    ATDS_OBSIDIAN_CANDIDATE_PAYLOAD_MANIFEST_V0_1

Each payload file contributes:

    relative_path
    size_bytes
    sha256

Rows are ordered:

    relative_path UTF-8 bytewise ASC

The payload manifest covers all files below:

    generated/

It does not include itself or the other generation metadata.

The payload file-map digest is:

    SHA256(
      canonical JSON array of
      [relative_path, sha256, size_bytes]
    )

This digest covers all generated payload files, including any build/integrity manifests emitted by the future qualified builder.

## 10. Why projection_tree_digest and payload_file_map_digest are both kept

The upstream projection builder owns:

    projection_tree_digest_sha256

That digest expresses the builder's deterministic projection semantics.

P5-D3C separately computes:

    payload_file_map_digest_sha256

over every actual packaged generated file.

These are deliberately distinct.

P5-D3C does not silently redefine the upstream projection-tree algorithm.

It binds both.

## 11. Candidate generation identity

The generation identity binds:

    repository
    branch
    candidate HEAD
    candidate tree

    dynamic inventory digest
    semantic bridge digest
    semantic record digest

    projection contract version
    projection tree digest
    generated file count

    payload file-map digest
    payload manifest digest

    breaker status
    determinism status
    breaker manifest digest
    breaker result digest
    determinism evidence digest

    exact P5-D3C contract blob

The canonical identity basis is SHA-256 hashed.

Generation ID is:

    gen-<generation_identity_digest_sha256>

No:

    timestamp
    UUID
    randomness
    host name
    local absolute path

may influence generation identity.

## 12. Generation manifest

Schema:

    ATDS_OBSIDIAN_CANDIDATE_GENERATION_MANIFEST_V0_1

Before sealing:

    package_status = COMPLETE_PENDING_SEAL

The generation manifest binds all scientific and technical identities required to prove what exact candidate the package represents.

It explicitly records:

    breaker_status = PASS
    determinism_status = PASS

Presence of a digest alone is not enough.

A failing breaker result cannot be packaged as if it were qualifying.

## 13. Seal

Schema:

    ATDS_OBSIDIAN_CANDIDATE_GENERATION_SEAL_V0_1

The seal is created:

    LAST

and:

    EXCLUSIVELY

It binds:

    generation_id
    generation_identity_digest
    payload manifest digest
    generation manifest digest
    payload file-map digest
    projection tree digest
    candidate HEAD
    candidate tree
    P5-D3C contract blob

Seal status:

    SEALED_UNPROMOTED

The seal contains no publication authority.

## 14. Candidate generation digest

The canonical candidate-generation digest is:

    SHA256(exact canonical SEAL.json bytes)

This means a candidate-generation descriptor can identify one exact sealed package without exposing host-local stage paths.

## 15. Logical immutability

P5-D3C claims logical immutability, not an operating-system immutable attribute.

Once a valid seal exists:

    payload mutation invalidates package
    manifest mutation invalidates package
    file deletion invalidates package
    extra file invalidates package
    seal mutation invalidates package
    seal deletion invalidates package

Repair-in-place is forbidden.

Reseal-in-place is forbidden.

A failed package requires a new fresh staging root.

## 16. Verification

Verification is read-only.

A verifier must check:

    package-root isolation
    exact allowed file set
    schemas
    generation identity
    candidate HEAD/tree
    inventory/bridge/semantic digests
    projection contract
    projection tree digest
    breaker PASS status
    determinism PASS status
    breaker/evidence digests
    exact payload count
    every file size
    every file SHA-256
    payload file-map digest
    payload manifest digest
    generation manifest digest
    seal digest computability
    no links/reparse escape
    no extra files

Success:

    PASS_SEALED_UNPROMOTED

Candidate-evidence failure:

    FAIL_INVALID_CANDIDATE_GENERATION

Infrastructure inability to verify:

    BLOCKED_VERIFICATION_INFRASTRUCTURE

These meanings must not be conflated.

## 17. Candidate generation descriptor

A successful verifier may emit a descriptor containing:

    generation_id
    candidate_generation_digest_sha256
    candidate_head
    candidate_tree
    projection_tree_digest_sha256
    payload_file_count
    payload_file_map_digest_sha256
    semantic_record_digest_sha256
    semantic_bridge_digest_sha256
    breaker_manifest_digest_sha256
    breaker_result_digest_sha256
    verification_status
    promotion_authorized

Required:

    verification_status = PASS_SEALED_UNPROMOTED
    promotion_authorized = false

Absolute stage paths and host metadata are forbidden from the descriptor.

## 18. Reuse of existing integrity primitives

P5-D3C may later reuse qualified/generic integrity mechanics already present:

    SHA-256 byte hashing
    regular-file checks
    single-link checks
    reparse/symlink/junction checks
    deterministic file-entry digest semantics

It may also preserve an existing projection integrity manifest inside the generated payload.

However:

    old builder manifest field names

do not define the new candidate-generation identity.

In particular:

    pilot_inventory_digest_sha256

may not stand in for:

    dynamic_inventory_digest_sha256

## 19. Publication remains separate

A sealed package is not:

    live
    CURRENT
    promoted
    Obsidian-visible

P5-D3C creates no:

    CURRENT
    CURRENT.md
    CURRENT.json
    CURRENT.tmp

and invokes no promotion primitive.

The qualified P5-C2 pointer primitive is a later publication mechanism only.

## 20. No current-head builder claim

P5-D3C does not solve the remaining current-head builder/relation adaptation gap.

That adaptation still must preserve the P5-D3B rule:

    METADATA_ONLY body-read authority = false

P5-D3C only defines how a future verified deterministic projection is packaged after that builder boundary has passed.

## 21. P5-D3C non-authorizations

Still forbidden:

    packager implementation
    verifier implementation
    staging execution
    current-head builder adaptation
    relation adapter execution
    finite evaluation orchestrator
    production promotion
    CURRENT mutation
    real Vault write
    background observer
    polling loop
    Windows startup/task/service registration
    Graph/Search CURRENT semantics

## 22. Next governed boundary

If P5-D3C qualifies, the next required gate is:

    P5-D3C2
    CANDIDATE GENERATION STAGING IMPLEMENTATION
    AND SANDBOX QUALIFICATION

Only after the package implementation itself is qualified may the project move to:

    P5-D3D
    FINITE CANDIDATE EVALUATION ORCHESTRATOR
    WITH CURRENT-HEAD BUILDER ADAPTATION

Then:

    P5-D3E
    SANDBOX CANDIDATE EVALUATION QUALIFICATION
