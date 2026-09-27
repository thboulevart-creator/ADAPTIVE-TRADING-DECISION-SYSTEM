# OBSIDIAN P5-D3D — IMPLEMENTATION PREFLIGHT

Date: 2026-09-27

## Scope

P5-D3D implementation candidate only.

Authorized execution after this preflight remains:

    synthetic fixture only

Not authorized:

    real exact-head candidate evaluation
    network fetch
    checkout creation by evaluator
    production promotion
    CURRENT mutation
    real Vault write
    background observer
    polling
    Graph/Search CURRENT semantics

## Qualified contract checkpoint

P5-D3D contract qualification commit:

    c2d0323df53c40c8818d7f8d9805210e1961116e

Current-head projection contract blob:

    6bc5286367890a8c393e4f5bea2b4ecb0fb20af2

Finite evaluator contract blob:

    b6c17167875874db30a575be95e8e6aa33d630dd

## Candidate branch

    feat/obsidian-projection-p5d3d-implementation-v0.1

## Exact functional candidate

    53ff8ba07baa4ff7be90d9d24f53da8e9601e019

Later preflight/static-review commits are evidence-only and do not replace this candidate.

## Exact functional artifacts

Metadata-safe relation adapter:

    tools/obsidian_projection/current_head_relations.py
    blob: 5cedad0cfec2a777972e6c9ae11488484b3b93f1

Current-head projection builder:

    tools/obsidian_projection/current_head_projection.py
    blob: 851b8c8517c9c380d350365ed98088435f7d6893

CHP breaker runner:

    tools/obsidian_projection/current_head_breakers.py
    blob: 98ef9d070a7a793007b0199f9983ea1836d1f776

Finite evaluator:

    tools/obsidian_projection/finite_candidate_evaluator.py
    blob: bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

Synthetic qualification harness:

    tools/obsidian_projection/p5d3d_verify.py
    blob: 589eec51d18a4385927af6005ebba3c82138cc2f

Relation tests:

    tests/obsidian_projection/test_current_head_relations.py
    blob: eda4dfa4409db2392e08c8c6e980e228450fd86e

Projection-builder tests:

    tests/obsidian_projection/test_current_head_projection.py
    blob: 4de6f71b33677f7b6d58ef93ed6b4477a3da255f

CHP breaker-runner tests:

    tests/obsidian_projection/test_current_head_breakers.py
    blob: f039c76ff5135e44d823aa00301694d4a36d5ff4

Finite evaluator tests:

    tests/obsidian_projection/test_finite_candidate_evaluator.py
    blob: fa776566df5376f06e1f3a45c09c8f785e7ddd29

Synthetic qualification test:

    tests/obsidian_projection/test_p5d3d_verify.py
    blob: 71b4ea7f34d9cc9eb59f032d89062c69cf1d5ed0

Adversarial implementation breakers:

    tests/obsidian_projection/test_p5d3d_adversarial.py
    blob: cc764e1521179466dc5aea29b17ed65f45d60a31

Documentation:

    docs/OBSIDIAN-P5D3D-FINITE-EVALUATOR-IMPLEMENTATION-V0.1.md
    blob: 1154d9dc52f4ca40990a4aa5a41faca524504a79

## Functional delta

Relative to the qualified P5-D3D contract checkpoint:

    12 files added
    0 predecessor files modified

## Static test inventory

P5-D3D implementation-specific persisted test methods:

    relation adapter = 7
    projection builder = 7
    CHP breaker runner = 7
    finite evaluator = 5
    synthetic qualification = 1
    adversarial = 15

Total:

    42

These are static repository counts, not execution evidence.

## Relation adapter boundary

Only one source.read_blob() call site exists.

It is reachable only after:

    content_mode == FULL_TEXT
    downstream_body_read_allowed == true
    suffix in {.md, .json}

METADATA_ONLY returns before the read site.

FULL_TEXT with any other suffix returns before the read site.

Every body read checks:

    exact Git blob SHA
    exact source blob size

Target matching is exact and unnormalized.

Whitespace-wrapped path strings do not resolve.

## Projection-builder boundary

The builder:

    does not read source bodies directly;
    renders one artifact per bridge entry;
    validates exact SemanticRecord ↔ bridge-entry provenance;
    delegates body reads only to the metadata-safe relation adapter;
    writes only a fresh OS-temp staging root;
    writes a current-head build manifest with no pilot identity;
    verifies integrity before returning.

## CHP breaker boundary

CHP-B01..B12 are implemented read-only.

The runner additionally requires B07 integrity-manifest coverage to equal the exact generated artifact/relation file set.

CHP-B04 binds relation evidence through:

    evidence path
    evidence blob SHA
    source_record_id
    source commit
    body-read audit

## Finite evaluator boundary

One invocation evaluates one candidate.

It:

    validates the P5-D2 EVALUATION_STARTED activation;
    verifies an already prepared isolated candidate repository;
    invokes qualified P5-B2;
    invokes qualified P5-D3B;
    builds A and B;
    requires deterministic equality;
    runs CHP-B01..B12;
    packages only after determinism + breakers PASS;
    applies determinate results only through one_shot_tick().

BLOCKED emits no P5-D2 result event.

REJECTED emits EVALUATION_FAILED.

QUALIFIED emits EVALUATION_PASSED.

Live projection head remains unchanged.

## Tooling-failure classification

Qualified local contract/tooling mismatch is classified:

    BLOCKED
    TOOLING_CONTRACT_MISMATCH

not candidate REJECTED.

Candidate-validity failures remain REJECTED.

## Synthetic qualification fixture

The P5-D3D harness creates a local sacrificial Git repository with four tracked sources:

    3 FULL_TEXT
    1 METADATA_ONLY

Expected:

    4 artifacts
    2 explicit REFERENCES relations
    2 eligible relation source body reads
    0 METADATA_ONLY body reads

The harness does not fetch network state.

It emits:

    real_candidate_evaluated = false
    network_fetch_performed = false

The synthetic repo/workspace are deleted after the run.

## Required local qualification

Before P5-D3D implementation may qualify:

1. recover exact functional candidate 53ff8ba07baa4ff7be90d9d24f53da8e9601e019;
2. verify exact projection/evaluator contract blobs;
3. verify exact five runtime implementation blobs;
4. py_compile all five runtime modules plus six P5-D3D test modules;
5. run targeted qualified contract chain + all P5-D3D implementation tests;
6. run full tests/obsidian_projection;
7. require clean source checkout;
8. execute p5d3d_verify synthetic harness only;
9. require PASS_SYNTHETIC_FINITE_EVALUATION;
10. require METADATA_ONLY body-read count zero;
11. require Build A == Build B;
12. require P5-D2 result event emitted for QUALIFIED;
13. require live projection unchanged;
14. require no current pointer / promotion / real Vault mutation;
15. require final clean checkout.

## Next governed boundary on PASS

    P5-D3E —
    REAL EXACT-HEAD SANDBOX CANDIDATE EVALUATION QUALIFICATION

P5-D3E, not P5-D3D, will prepare and evaluate a real isolated exact-head candidate.
