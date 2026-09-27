# OBSIDIAN P5-D3E — REAL EXACT-HEAD SANDBOX IMPLEMENTATION PREFLIGHT

Date: 2026-09-27

## Scope

P5-D3E implementation candidate only.

No real integration/system-v1 candidate evaluation is authorized by this preflight.

Authorized execution before the real run remains:

    py_compile
    implementation unit tests
    adversarial implementation tests
    full tests/obsidian_projection
    local pre-resolved synthetic sandbox only

## Qualified contract checkpoint

P5-D3E contract qualification commit:

    f413171075fb002b7c6080a10247cad65954f2be

P5-D3E contract blob:

    ae4b1691fae16fcd1616e265a089670b9654db4a

Qualified P5-D3D evaluator blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

## Candidate branch

    feat/obsidian-projection-p5d3e-real-exact-head-sandbox-implementation-v0.1

## Exact functional candidate

    d403482b222b8bcfa4b0befa7684eda4b9d662fc

Later preflight/static-review commits are evidence-only and do not replace this candidate.

## Exact functional artifacts

Real exact-head sandbox harness:

    tools/obsidian_projection/p5d3e_verify.py
    blob: 2380cddc3e15caf1b3f4d1b7942f064c179389ee

Harness tests:

    tests/obsidian_projection/test_p5d3e_verify.py
    blob: a1ae77ae7bfe768d1152885a2cfa154695c47bf0

Adversarial implementation tests:

    tests/obsidian_projection/test_p5d3e_adversarial.py
    blob: 6af423b77b4ad78a833f7f4e3dedc53f5f23cead

Implementation documentation:

    docs/OBSIDIAN-P5D3E-REAL-EXACT-HEAD-SANDBOX-IMPLEMENTATION-V0.1.md
    blob: b21440ea7321da10cbafdb28170972570f530461

## Functional delta

Relative to qualified P5-D3E contract checkpoint:

    4 files added
    0 qualified predecessor files modified

## Static test inventory

P5-D3E implementation-specific persisted test methods:

    harness tests = 5
    adversarial tests = 15

Total:

    20

These are static repository counts only.

## Candidate resolution boundary

The real entry point:

    run_real_exact_head_qualification()

must call:

    resolve_real_candidate()

before any real evaluation.

The resolver is the only path that is allowed to perform the governed network branch fetch.

It freezes:

    candidate_head
    candidate_tree

The public pre-resolved sandbox entry point cannot claim a real PASS.

Its success status is limited to:

    PASS_SYNTHETIC_PRE_RESOLVED_SANDBOX

The internal real_context=True path is reachable only from the real wrapper.

## OS-temp safety

Before a sandbox directory is created, the implementation resolves the OS temp root.

If that temp root is inside:

    control repository
    real Vault
    additional forbidden root

the harness blocks.

This prevents sandbox creation itself from writing into a protected root.

## Sacrificial clone boundary

The harness uses:

    git clone --no-hardlinks --no-checkout

from the local control repository.

It then transfers the exact remote-tracking candidate ref locally.

The candidate clone is required to have:

    canonical GitHub origin
    detached exact HEAD
    exact TREE
    clean worktree
    no .git/objects/info/alternates
    object-store file link count exactly 1

## Real Vault evidence

The harness computes a deterministic protected-root fingerprint before and after evaluation.

It does not follow reparse/symlink entries.

A mismatch is:

    FAIL_P5D3E_GOVERNANCE_VIOLATION

The qualification report does not contain the absolute Vault path.

## Qualified evaluator reuse

The implementation calls the already-qualified:

    evaluate_candidate_finitely()

No alternate evaluator is introduced.

The runtime contains no:

    requests
    urllib
    socket network client
    polling loop
    time.sleep
    promotion_experiment
    PROMOTION_CONFIRMED
    pointer-writing helper

## Post-package verification

For a QUALIFIED evaluator outcome, the harness calls:

    verify_candidate_generation()

again in read-only mode.

It requires:

    PASS_SEALED_UNPROMOTED

and exact agreement on:

    candidate HEAD
    candidate TREE
    candidate-generation digest
    semantic bridge digest
    semantic-record digest
    breaker manifest digest
    breaker result digest

## Implementation qualification gate

Before the real HEAD may be evaluated:

1. recover exact candidate d403482b222b8bcfa4b0befa7684eda4b9d662fc;
2. verify exact P5-D3E contract blob;
3. verify exact harness/test blobs;
4. py_compile runtime and both test modules;
5. run P5-D3E contract + implementation tests;
6. run full tests/obsidian_projection;
7. require source-clean control checkout;
8. execute the public pre-resolved sandbox test path only;
9. require that synthetic success cannot claim PASS_REAL_EXACT_HEAD_FINITE_EVALUATION;
10. require final source-clean checkout.

No governed network candidate-resolution run is part of this implementation qualification.

## Next action on PASS

Only after the implementation gate passes may P5-D3E perform the real run:

    resolve current integration/system-v1 once
    freeze exact HEAD/TREE
    execute real exact-head sandbox
    adjudicate QUALIFIED / REJECTED / BLOCKED

Still forbidden:

    production promotion
    CURRENT mutation
    real Vault write
    background observer
    polling
    Graph/Search CURRENT semantics
