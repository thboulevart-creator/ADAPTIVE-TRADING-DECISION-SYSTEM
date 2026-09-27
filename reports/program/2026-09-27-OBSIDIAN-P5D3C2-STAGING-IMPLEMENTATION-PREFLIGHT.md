# OBSIDIAN P5-D3C2 — STAGING IMPLEMENTATION PREFLIGHT

Date: 2026-09-27

## Scope

P5-D3C2 implements the real generic candidate-generation packager and read-only verifier defined by qualified P5-D3C, then qualifies their mechanics in a sacrificial OS-temp sandbox.

It does not implement or authorize:

- current-head builder adaptation;
- relation-adapter execution;
- finite candidate-evaluation orchestration;
- production promotion;
- CURRENT mutation;
- real Vault writes;
- background observation;
- polling;
- Windows persistence;
- Graph/Search CURRENT semantics.

## Qualified predecessor

P5-D3C qualification commit:

    437ab790f2a1fa4b490344d28cb7b7a2e8116db3

P5-D3C qualification report blob:

    7390a01e9f7af1bdf9d2f5c5251765ce68faf533

P5-D3C staging contract blob:

    79c6a3380a1dcefc49aa4619259baaa8eeadb535

## Candidate branch

    feat/obsidian-projection-p5d3c2-staging-implementation-v0.1

## Exact functional candidate

    f5304fa9697bd33ea98214598321473087b65e24

Later preflight/static-review commits must not replace this runtime candidate.

## Exact candidate artifacts

P5-D3C2 runtime contract:

    tools/obsidian_projection/candidate_generation_staging_implementation_contract_v0_1.json
    blob: 12f04ad90567c6b0451713a4180f3b10df66de41

Packager + verifier implementation:

    tools/obsidian_projection/candidate_generation_staging.py
    blob: e2e5867536f4f9c7dec475c6696737249536ff39

Sandbox qualification runner:

    tools/obsidian_projection/p5d3c2_verify.py
    blob: 82f5ad9aab8582c32a4e38069934ed4849b8f08e

Implementation-contract breakers:

    tests/obsidian_projection/test_candidate_generation_staging_implementation_contract_v0_1.py
    blob: cffd4bf979521c998e4aab4a113e9eda1d282d32

Packager/verifier behavioral tests:

    tests/obsidian_projection/test_candidate_generation_staging.py
    blob: 23a299ad31b183855ef4ab1f7e1d0156d82a847c

Sandbox harness tests:

    tests/obsidian_projection/test_p5d3c2_verify.py
    blob: a381f9fd10399d412febeba07f560bad7097633a

Adversarial breakers:

    tests/obsidian_projection/test_p5d3c2_adversarial.py
    blob: ac4b679a64d354c342e18d7caa40aef1f12e005d

Documentation:

    docs/OBSIDIAN-P5D3C2-CANDIDATE-GENERATION-STAGING-IMPLEMENTATION-V0.1.md
    blob: a66c3061a17d610e603e36b46190d8976167460d

## Static inventory

Preregistered P5-D3C2 breakers:

    76 unique

Persisted Python test methods:

    implementation contract = 15
    behavior = 29
    sandbox harness = 5
    adversarial = 20

Total P5-D3C2-specific test methods:

    69

These are repository counts only, not execution evidence.

## Functional delta

Relative to qualified P5-D3C, the P5-D3C2 functional candidate adds exactly eight P5-D3C2 files.

No previously qualified file is modified.

## Implementation identity

The implementation pins:

    P5-D3C staging contract blob
        79c6a3380a1dcefc49aa4619259baaa8eeadb535

    P5-D3C qualification commit
        437ab790f2a1fa4b490344d28cb7b7a2e8116db3

    P5-D3C2 runtime contract blob
        12f04ad90567c6b0451713a4180f3b10df66de41

## Staging boundary

The implementation accepts only a fresh package root below the OS temp directory.

It rejects intersection with:

- verified projection input root;
- caller-supplied canonical worktree;
- caller-supplied real Vault root;
- caller-supplied live generation roots.

No absolute sandbox path enters package identity.

## Packager behavior

The packager:

1. validates candidate scientific identity;
2. recomputes source generated-file count;
3. recomputes source projection-tree digest;
4. creates fresh package root;
5. copies each generated file exclusively and byte-exact;
6. writes payload-manifest;
7. derives deterministic generation identity;
8. writes generation-manifest;
9. verifies exact pre-seal file set and payload;
10. recomputes packaged projection-tree digest;
11. writes SEAL.json exclusively as final package mutation;
12. calls the read-only verifier and returns its descriptor.

## Read-only verifier

The verifier recomputes:

- exact file set;
- every payload size and SHA-256;
- payload file-map digest;
- payload-manifest digest;
- packaged projection-tree digest;
- generation identity;
- generation ID;
- breaker/determinism PASS state;
- generation-manifest digest;
- exact seal content.

It rejects:

- noncanonical JSON;
- extra/missing manifest fields;
- symlinks/reparse/junctions;
- hard-link aliases;
- extra/missing payload files;
- mutated manifests;
- mutated seal;
- wrong staging contract binding.

No write surface exists inside verify_candidate_generation().

## Sandboxed destructive qualification

The sandbox runner creates one explicit packager-input fixture only.

It is not evidence for current-head builder qualification.

A valid control package must:

    PASS_SEALED_UNPROMOTED

twice with identical descriptor and unchanged package content digest.

Then seven independent mutation copies are required to fail verification:

    PAYLOAD_BYTE_MUTATION
    PAYLOAD_FILE_DELETION
    UNMANIFESTED_EXTRA_FILE
    PAYLOAD_MANIFEST_MUTATION
    GENERATION_MANIFEST_MUTATION
    SEAL_MUTATION
    HARD_LINK_ALIAS

A symlink/reparse mutation is also attempted.

If host policy prevents symlink creation, the report may state:

    CAPABILITY_UNAVAILABLE

but static/unit reparse breakers remain mandatory.

After mutation copies, the original control package must still verify unchanged.

## Failure semantics

Contract violation:

    FAIL_INVALID_CANDIDATE_GENERATION

Sandbox/filesystem capability failure:

    BLOCKED_SANDBOX_INFRASTRUCTURE

Mutation surviving verifier:

    FAIL_BREAKER_SURVIVED

Verifier changing control package:

    FAIL_VERIFIER_MUTATED_PACKAGE

No partial PASS is allowed.

## Required local qualification sequence

Before P5-D3C2 may qualify:

1. recover exact candidate HEAD f5304fa9697bd33ea98214598321473087b65e24;
2. require source-clean control checkout;
3. py_compile implementation, runner and all four P5-D3C2 test modules;
4. run targeted P5-D3C + P5-D3C2 tests;
5. run the full tests/obsidian_projection suite;
6. require source-clean checkout;
7. execute the P5-D3C2 sacrificial sandbox runner;
8. require report status PASS_SANDBOX_SEALED_UNPROMOTED;
9. require exactly seven required mutation breakers passed;
10. require control verifier repeat equality;
11. require unchanged control content digest;
12. require no CURRENT/promotion authority;
13. require final source-clean checkout.

No P5-D3D work is authorized before these gates pass.

## Next governed frontier on PASS

    P5-D3D —
    FINITE CANDIDATE EVALUATION ORCHESTRATOR
    WITH CURRENT-HEAD BUILDER ADAPTATION
