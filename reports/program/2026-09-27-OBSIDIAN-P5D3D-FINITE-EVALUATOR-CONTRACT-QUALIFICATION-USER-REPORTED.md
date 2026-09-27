# OBSIDIAN P5-D3D — FINITE EVALUATOR CONTRACT QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified contract candidate

Exact P5-D3D contract candidate:

    f94c708f312dc0338531cdba7e963cbbeea1dfb8

Branch:

    feat/obsidian-projection-p5d3d-finite-evaluator-contract-v0.1

Evidence-only commits after this candidate do not replace the tested contract candidate.

## Exact qualified contract artifacts

Current-head projection contract:

    tools/obsidian_projection/current_head_projection_contract_v0_1.json
    blob: 6bc5286367890a8c393e4f5bea2b4ecb0fb20af2

Finite evaluator contract:

    tools/obsidian_projection/finite_candidate_evaluator_contract_v0_1.json
    blob: b6c17167875874db30a575be95e8e6aa33d630dd

Projection contract tests:

    tests/obsidian_projection/test_current_head_projection_contract_v0_1.py
    blob: 34252aa1aff0b97b99bb8a4758218ca89d2fbaa1

Finite evaluator contract tests:

    tests/obsidian_projection/test_finite_candidate_evaluator_contract_v0_1.py
    blob: 75b0209429a05d0e18ad82f1c860a5a21229589a

Documentation:

    docs/OBSIDIAN-P5D3D-FINITE-CANDIDATE-EVALUATOR-CONTRACT-V0.1.md
    blob: dc1bced19edeff4cdd69830dc2a8470f5e30abe0

## Reported full regression result

The user reported:

    Ran 980 tests in 15.097s
    OK
    P5D3D_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3D_CONTRACT_REBREAK_COMPLETED=PASS

This directly supports successful completion of the full tests/obsidian_projection re-break and a clean control checkout after execution.

Because the governed wrapper stops immediately on py_compile or targeted-contract failure, reaching the reported full-suite PASS and final completion marker is consistent with the earlier wrapper gates having passed. Those earlier individual markers were not included in the supplied excerpt and are therefore not separately claimed as direct user-reported lines.

## Qualified authority

This qualification authorizes the P5-D3D contract boundary only.

It qualifies the preregistered authority for:

- current-head deterministic projection semantics;
- METADATA_ONLY body-read prohibition;
- FULL_TEXT .md/.json-only relation-body reads;
- exact body-read audit requirements;
- current-head REFERENCES-only relation rules;
- exact current-head build-manifest identity;
- deterministic Build A / Build B equality;
- twelve CHP projection breakers;
- P5-D3C2 package mapping;
- QUALIFIED / REJECTED / BLOCKED outcome semantics;
- P5-D2 EVALUATION_PASSED / EVALUATION_FAILED mapping;
- no P5-D2 event on BLOCKED;
- live projection preservation during evaluation;
- retry from fresh roots after BLOCKED.

## Breaker registries qualified by this contract gate

Current-head projection contract:

    73 required breakers
    73 unique

Finite evaluator contract:

    91 required breakers
    91 unique

Persisted P5-D3D contract-test methods:

    15 projection-contract tests
    19 finite-evaluator-contract tests
    34 total

The reported full regression included these tests in the repository-wide Obsidian suite.

## Structural decisions now authorized for implementation

The qualified contract explicitly permits a future P5-D3D implementation candidate to reuse generic legacy mechanics:

    render_artifact()
    render_relation()
    integrity primitives

but not to directly reuse as current-head authority:

    FrozenInventory
    legacy classify_inventory()
    legacy build_projection_from_records()
    legacy extract_relations()
    fixed 74-source assumptions
    pilot_inventory_digest_sha256

The current-head projection contract is the authority for the new implementation.

## METADATA_ONLY boundary preserved

The qualified contract requires:

    metadata_only_body_read_count = 0

METADATA_ONLY entries:

    may be projected as artifact metadata;
    may be exact-path relation targets;
    may not be relation body-read sources.

Relation-body reads are limited to eligible:

    FULL_TEXT .md
    FULL_TEXT .json

with exact source path/blob identity and deterministic audit.

## Implementation scope now authorized

Under the same P5-D3D frontier, implementation may now begin for:

    CURRENT-HEAD PROJECTION BUILDER
    METADATA-SAFE RELATION ADAPTER
    CHP BREAKER RUNNER
    FINITE CANDIDATE EVALUATOR

Initial runtime execution is restricted to synthetic fixtures.

The implementation must remain finite and non-promoting.

## Explicit non-authorizations preserved

This contract qualification does NOT authorize:

- real exact-head sandbox evaluation;
- network fetch inside the evaluator;
- Git checkout creation by the evaluator;
- production promotion;
- CURRENT pointer mutation;
- real Vault writes;
- background observer execution;
- polling;
- Windows startup/task/service persistence;
- Graph/Search CURRENT semantics.

A complete real candidate sandbox evaluation remains reserved for P5-D3E.

## Verdict

**PASS — P5-D3D FINITE EVALUATOR CONTRACT QUALIFIED**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This is not independent local execution by the assistant.

## Next governed action

Remain inside P5-D3D and create the implementation candidate, test-first:

    CURRENT-HEAD PROJECTION BUILDER
        +
    METADATA-SAFE RELATION ADAPTER
        +
    CHP BREAKER RUNNER
        +
    FINITE EVALUATOR

Only synthetic-fixture execution is authorized during this implementation/qualification phase.
