# OBSIDIAN P5-D3C2 — STAGING IMPLEMENTATION STATIC REVIEW

Date: 2026-09-27

## Review status

This is a same-assistant static review.

It is not independent.
It is not local runtime evidence.
It does not qualify P5-D3C2.
It does not authorize P5-D3D.

## Functional candidate reviewed

    f5304fa9697bd33ea98214598321473087b65e24

Branch:

    feat/obsidian-projection-p5d3c2-staging-implementation-v0.1

Evidence-only preflight commit:

    ef83e16ab97e7b118a3e7ac677ec149be746c924

## Exact candidate blobs

Runtime contract:

    12f04ad90567c6b0451713a4180f3b10df66de41

Packager/verifier:

    e2e5867536f4f9c7dec475c6696737249536ff39

Sandbox runner:

    82f5ad9aab8582c32a4e38069934ed4849b8f08e

Implementation-contract tests:

    cffd4bf979521c998e4aab4a113e9eda1d282d32

Behavioral tests:

    23a299ad31b183855ef4ab1f7e1d0156d82a847c

Sandbox tests:

    a381f9fd10399d412febeba07f560bad7097633a

Adversarial tests:

    ac4b679a64d354c342e18d7caa40aef1f12e005d

Documentation:

    a66c3061a17d610e603e36b46190d8976167460d

## Delta review

Relative to qualified P5-D3C, the functional candidate adds exactly eight P5-D3C2 files.

No previously qualified file is modified.

Static review: PASS.

## Predecessor and runtime identity

The implementation pins:

    P5-D3C staging contract blob                         PASS
    P5-D3C qualification commit                         PASS
    P5-D3C2 implementation contract blob                PASS

The P5-D3C2 implementation contract pins the qualified P5-D3C report and contract identities.

Static review: PASS.

## P5-C2 fixture separation

No P5-C2 experimental fixture runtime is imported.

Absent from implementation and sandbox runner:

    promotion_experiment
    build_generation
    validate_generation_dir
    _write_pointer
    validate_pointer_entry

Therefore P5-D3C2 does not relabel the P5-C2 synthetic experiment as the real packager.

Static review: PASS.

## Network / Git / background boundary

No runtime import was found for:

    subprocess
    socket
    urllib
    requests
    http
    threading
    multiprocessing
    asyncio
    winreg
    ctypes

No background observer or polling entrypoint is present.

The implementation contains one while-loop only:

    _assert_directory_chain_no_alias()

This is a finite parent-chain walk terminating at the package root.

There is no while-loop in:

    stage_candidate_generation()
    verify_candidate_generation()
    p5d3c2_verify.py

Static review: PASS.

## Temp-only staging boundary

New package roots pass through:

    validate_new_temp_staging_path()

The implementation additionally rejects intersection with:

    verified projection input
    caller-supplied forbidden roots

The same normalized forbidden-root tuple is reused during post-seal verification.

This prevents an iterator from being consumed before the final boundary check.

Static review: PASS.

## Source projection verification

Before staging:

    generated/ must exist                               PASS
    tree aliases/reparse links rejected                 PASS
    regular single-link files required                  PASS
    payload paths validated                             PASS
    generated-file count recomputed                     PASS
    projection-tree digest recomputed                   PASS

The source projection directory is not modified.

Static review: PASS.

## Payload copy

Each destination path is path-normalized and root-bound.

Before every write, the full directory chain back to package root is checked for alias/reparse behavior.

Files are created with exclusive mode:

    xb

Every copied file is immediately rebound to exact:

    relative path
    size
    SHA-256

Static review: PASS.

## Manifest canonicalization

Canonical machine JSON uses:

    UTF-8
    sort_keys=True
    compact separators
    allow_nan=False
    terminal LF

The verifier requires exact canonical bytes, not merely semantically equivalent JSON.

Static review: PASS.

## Payload-manifest verification

The verifier enforces:

    exact field set                                      PASS
    exact schema                                         PASS
    integer nonnegative file_count                       PASS
    count/list equality                                  PASS
    unique paths                                         PASS
    UTF-8 bytewise path order                            PASS
    safe generated/ prefix                               PASS
    every file existence                                 PASS
    every file size                                      PASS
    every file SHA-256                                   PASS
    file-map digest                                      PASS

Static review: PASS.

## Generation identity

The generation identity contains no runtime path, clock, UUID, randomness or host identity.

Generation ID remains:

    gen-<generation_identity_digest_sha256>

The same input/payload therefore has a path-independent identity.

Static review: PASS.

## Pre-seal ordering

The implementation order is:

    source verification
    package-root creation
    payload copy
    payload-manifest
    generation identity
    generation-manifest
    exact pre-seal file-set check
    payload verification
    packaged projection-tree recomputation
    generation-manifest digest check
    SEAL.json exclusive write
    read-only verifier

The seal write occurs exactly once in the packager.

Static review: PASS.

## Packaged projection-tree binding

The implementation recalculates projection_tree_digest twice over the staged package lifecycle:

1. pre-seal;
2. final read-only verification.

The value must equal the upstream verified candidate projection-tree digest.

This prevents the projection-tree field from being accepted as manifest-only evidence.

Static review: PASS.

## Read-only verifier

No direct write surface exists inside:

    verify_candidate_generation()

Static inspection found no:

    _write_exclusive
    write_bytes
    write_text
    mkdir
    unlink
    rename
    replace

inside the verifier body.

The verifier recomputes:

    payload file digests
    file-map digest
    payload-manifest digest
    packaged projection-tree digest
    generation identity
    generation ID
    generation-manifest digest
    exact seal

Static review: PASS.

## Filesystem alias and hard-link boundary

Filesystem checks reject:

    symlink
    Windows reparse point / junction
    non-regular file
    hard-link count != 1

The packager also checks the complete ancestor chain before writes.

Static review: PASS.

## Candidate / infrastructure failure classification

P5-D3C2 distinguishes candidate evidence from infrastructure inability.

Historical IntegrityError is translated as infrastructure when it represents:

    cannot lstat
    cannot stat
    hard-link count unavailable

Other deterministic integrity violations remain candidate-invalid.

The sandbox CLI also maps raw OSError to:

    BLOCKED_SANDBOX_INFRASTRUCTURE

Static review: PASS.

## Descriptor boundary

Successful verifier output contains:

    verification_status = PASS_SEALED_UNPROMOTED
    promotion_authorized = false

No absolute package path, sandbox path, PID, timestamp or host identity is included.

Static review: PASS.

## Sandbox qualification runner

The runner creates a fixture explicitly named:

    P5D3C2_SANDBOX_PACKAGER_INPUT

It does not claim current-head builder qualification.

It creates one valid control package, then:

    verifies control twice;
    compares descriptors;
    checks unchanged content digest;
    attacks mutation copies only;
    verifies control again after attacks.

Required mutation attacks:

    PAYLOAD_BYTE_MUTATION
    PAYLOAD_FILE_DELETION
    UNMANIFESTED_EXTRA_FILE
    PAYLOAD_MANIFEST_MUTATION
    GENERATION_MANIFEST_MUTATION
    SEAL_MUTATION
    HARD_LINK_ALIAS

Each required mutation must be rejected.

Static review: PASS.

## Reparse runtime probe

A symlink/reparse mutation is attempted separately.

Possible accepted evidence states:

    REJECTED_AS_INVALID
    CAPABILITY_UNAVAILABLE

A created link that survives verification is FAIL.

An unexpected infrastructure block after link creation is FAIL.

Static review: PASS.

## Control-package isolation

Mutation copies are created independently.

The hard-link mutation is created only within the mutation copy.

The original control package is verified again after every mutation phase.

This directly checks that destructive attacks do not corrupt the control candidate.

Static review: PASS.

## Report boundary

Success report:

    ATDS_OBSIDIAN_P5D3C2_SANDBOX_REPORT_V0_1
    PASS_SANDBOX_SEALED_UNPROMOTED

It records deterministic package identity and breaker summary only.

It does not expose an absolute sandbox path.

It asserts:

    real_vault_modified = false
    current_pointer_created = false
    production_promotion_authorized = false
    sandbox_retained = false

The sandbox is deleted after evidence computation.

## Runtime non-authorizations

P5-D3C2 still does not authorize:

    current-head builder adaptation                     PASS
    relation-adapter execution                          PASS
    finite evaluation orchestrator                      PASS
    production promotion                                PASS
    CURRENT mutation                                    PASS
    real Vault write                                    PASS
    background observer                                 PASS
    polling                                             PASS
    Windows startup/task/service                        PASS
    Graph/Search CURRENT semantics                      PASS

## Test and breaker inventory

P5-D3C2 contract breakers:

    76 unique

Persisted P5-D3C2 test methods:

    implementation contract = 15
    behavior = 29
    sandbox harness = 5
    adversarial = 20

Total:

    69

These are static counts only.

They are not executed evidence.

## Required runtime qualification

P5-D3C2 still requires:

1. py_compile all P5-D3C2 modules/tests;
2. targeted P5-D3C + P5-D3C2 tests;
3. full tests/obsidian_projection regression suite;
4. source-clean control checkout;
5. sacrificial sandbox execution;
6. valid control SEALED_UNPROMOTED package;
7. repeated read-only verification equality;
8. unchanged control content digest;
9. all seven required mutation breakers rejected;
10. reparse probe adjudicated;
11. final source-clean control checkout.

## Verdict

**STATIC REVIEW PASS — LOCAL RE-BREAK + SANDBOX QUALIFICATION REQUIRED.**

P5-D3C2 remains unqualified.

Exact functional candidate to execute:

    f5304fa9697bd33ea98214598321473087b65e24
