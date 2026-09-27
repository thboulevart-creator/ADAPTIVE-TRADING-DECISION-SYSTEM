# OBSIDIAN P5-D3C — CANDIDATE GENERATION STAGING CONTRACT PREFLIGHT

Date: 2026-09-27

## Scope

P5-D3C defines only the candidate-generation staging contract.

It does not implement or authorize:

- a staging packager;
- a staging verifier;
- candidate staging execution;
- current-head builder adaptation;
- relation-adapter execution;
- finite evaluation orchestration;
- promotion;
- CURRENT mutation;
- real Vault writes;
- background observation;
- polling;
- Windows startup/task/service registration;
- Graph/Search CURRENT semantics.

## Qualified predecessor

P5-D3B qualification commit:

    51dfa30a9fcca4f012f80410f24f95007d2cf2e6

P5-D3B qualification report blob:

    94fbe40ffde900040c9a784b205c37e76b7ef834

P5-D3B bridge contract blob:

    7015db1206cd40b703795d12519707a6455b4fc3

P5-D3B bridge implementation blob:

    ff3c2dd232487594a5283a9ab7750780ac098f2d

## Candidate branch

    feat/obsidian-projection-p5d3c-candidate-generation-staging-contract-v0.1

## Exact functional candidate

    f3dc4b582fadff37ffb37108ec677ea88de7dad0

Later preflight/static-review commits are evidence-only and do not replace this candidate.

## Exact functional artifacts

Contract:

    tools/obsidian_projection/candidate_generation_staging_contract_v0_1.json
    blob: 79c6a3380a1dcefc49aa4619259baaa8eeadb535

Contract breakers:

    tests/obsidian_projection/test_candidate_generation_staging_contract_v0_1.py
    blob: 8a986e87c72f8556bcac46e167026db5d849d8d3

Documentation:

    docs/OBSIDIAN-P5D3C-CANDIDATE-GENERATION-STAGING-CONTRACT-V0.1.md
    blob: d23cfd1d0ed520696a57dc104540721e683760ab

## Functional delta

Relative to the qualified P5-D3B checkpoint, P5-D3C adds exactly three functional files.

No previously qualified source, test or contract file is modified.

## Static inventory

Required breakers:

    108 unique

Persisted contract test methods:

    26

These are repository counts only, not execution evidence.

## P5-C2 reuse boundary

P5-D3C reuses only the qualified architectural property:

    complete immutable generation before pointer publication

It does not reuse as real packaging authority:

    promotion_experiment.build_generation()
    promotion_experiment.validate_generation_dir()

The synthetic 128-file GEN_A/GEN_B representation remains an experiment fixture.

No CURRENT pointer is created by P5-D3C.

## Real package layout

Allowed top-level package namespaces:

    generated/
    _atds_generation/

Machine manifests:

    _atds_generation/payload-manifest.json
    _atds_generation/generation-manifest.json
    _atds_generation/SEAL.json

Forbidden:

    CURRENT
    CURRENT.md
    CURRENT.json
    CURRENT.tmp
    views/
    .obsidian/
    .git/

## Payload identity

The package must preserve every already verified generated file byte-for-byte and path-for-path.

The package independently binds all payload files through:

    payload_file_map_digest_sha256

while preserving the upstream:

    projection_tree_digest_sha256

as a separate builder-owned semantic digest.

## Scientific identity binding

Generation identity binds:

    candidate HEAD/tree
    dynamic inventory digest
    semantic bridge digest
    semantic record digest
    projection contract version
    projection tree digest
    generated file count
    payload file-map digest
    payload-manifest digest
    breaker status = PASS
    determinism status = PASS
    breaker manifest digest
    breaker result digest
    determinism evidence digest
    exact P5-D3C contract blob

Generation ID is deterministic:

    gen-<generation_identity_digest_sha256>

No wall clock, UUID, randomness, host identity or absolute path may influence it.

## Seal semantics

The seal is the final package mutation.

Seal status:

    SEALED_UNPROMOTED

The seal binds generation identity, manifests, payload identity, projection identity and exact candidate HEAD/tree.

The candidate-generation digest is the SHA-256 of exact canonical SEAL.json bytes.

Logical immutability begins only after a valid seal exists.

P5-D3C does not claim an OS-level immutable filesystem attribute.

Any post-seal mutation invalidates the package.

Repair/reseal in place is forbidden.

## Verification

Verification must be read-only and exhaustive over:

- exact allowed file set;
- payload file count;
- every file size;
- every file SHA-256;
- candidate HEAD/tree;
- scientific digests;
- breaker/determinism PASS states and evidence;
- manifest digests;
- seal;
- links/reparse points;
- extra or missing files.

Successful status:

    PASS_SEALED_UNPROMOTED

This status does not authorize promotion.

## Required local re-break

Before P5-D3C may qualify:

1. recover exact functional candidate HEAD f3dc4b582fadff37ffb37108ec677ea88de7dad0;
2. require a source-clean control checkout;
3. py_compile the P5-D3C contract breaker;
4. execute the targeted P5-D3C contract tests;
5. execute the full tests/obsidian_projection suite;
6. require the control checkout to remain source-clean.

No packager/verifier implementation is authorized before this re-break passes.

## Next governed boundary on PASS

    P5-D3C2 — CANDIDATE GENERATION STAGING IMPLEMENTATION AND SANDBOX QUALIFICATION
