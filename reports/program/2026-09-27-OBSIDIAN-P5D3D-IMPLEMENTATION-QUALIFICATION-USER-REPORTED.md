# OBSIDIAN P5-D3D — IMPLEMENTATION QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified functional candidate

Exact corrected P5-D3D implementation candidate:

    6efa84c657bbea4edaa56d643d2b9dc0150bcdb1

Branch:

    feat/obsidian-projection-p5d3d-implementation-v0.1

The earlier candidate:

    53ff8ba07baa4ff7be90d9d24f53da8e9601e019

remains a failed py_compile candidate due to an adversarial-test string quoting defect.

The corrected candidate changed only the adversarial test source quoting.

The five runtime implementation blobs remained unchanged.

## Qualified contracts

Current-head projection contract:

    6bc5286367890a8c393e4f5bea2b4ecb0fb20af2

Finite candidate evaluator contract:

    b6c17167875874db30a575be95e8e6aa33d630dd

## Runtime implementation blobs

Metadata-safe relation adapter:

    5cedad0cfec2a777972e6c9ae11488484b3b93f1

Current-head projection builder:

    851b8c8517c9c380d350365ed98088435f7d6893

CHP breaker runner:

    98ef9d070a7a793007b0199f9983ea1836d1f776

Finite candidate evaluator:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

Synthetic qualification harness:

    589eec51d18a4385927af6005ebba3c82138cc2f

## Reported full regression result

The user reported:

    Ran 1022 tests in 19.338s
    OK
    P5D3D_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN_AFTER_TESTS=PASS

The governed wrapper therefore reached the full repository-wide Obsidian regression PASS on the corrected implementation candidate and preserved a source-clean control checkout after tests.

## Reported synthetic finite-evaluation result

Reported schema:

    ATDS_OBSIDIAN_P5D3D_SYNTHETIC_QUALIFICATION_REPORT_V0_1

Reported status:

    PASS_SYNTHETIC_FINITE_EVALUATION

Reported outcome:

    QUALIFIED

Reported package verification status:

    PASS_SEALED_UNPROMOTED

Reported counts:

    source_record_count=4
    full_text_count=3
    metadata_only_count=1
    artifact_record_count=4
    relation_record_count=2
    relation_source_body_read_count=2
    metadata_only_body_read_count=0

Reported deterministic equality:

    projection_a_equals_b=true

Reported P5-D2 mapping:

    p5d2_result_event_emitted=true

Reported live/publication invariants:

    live_projection_head_unchanged=true
    current_pointer_created=false
    production_promotion_authorized=false
    real_vault_modified=false

Reported execution-boundary invariants:

    network_fetch_performed=false
    real_candidate_evaluated=false
    synthetic_repository_retained=false
    synthetic_workspace_retained=false

Final wrapper markers:

    P5D3D_SYNTHETIC_QUALIFICATION=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3D_IMPLEMENTATION_QUALIFICATION_COMPLETED=PASS

## Qualified P5-D3D implementation boundary

Within the supplied synthetic qualification evidence, P5-D3D now qualifies:

- the current-head projection builder implementation;
- the METADATA-safe relation adapter;
- the CHP-B01..B12 breaker runner;
- the finite candidate evaluator core;
- deterministic Build A / Build B equality handling;
- exact current-head projection packaging into qualified P5-D3C2 SEALED_UNPROMOTED staging;
- QUALIFIED result mapping through P5-D2;
- preservation of the live projection head during evaluation;
- zero METADATA_ONLY body reads in the synthetic fixture;
- finite execution without network fetch;
- no CURRENT mutation;
- no production promotion;
- no real Vault modification.

## Synthetic qualification interpretation

The synthetic fixture demonstrated:

    4 source records
    4 projected artifacts
    3 FULL_TEXT records
    1 METADATA_ONLY record
    2 explicit relation records
    2 eligible FULL_TEXT relation-source body reads
    0 METADATA_ONLY body reads

Build A and Build B were reported equal.

The resulting candidate package verified:

    PASS_SEALED_UNPROMOTED

and the finite evaluator reported:

    QUALIFIED

with a P5-D2 result event emitted.

## Explicit limitations preserved

This qualification does NOT establish that a real exact candidate HEAD from integration/system-v1 has yet passed the end-to-end finite evaluator.

It does NOT qualify:

- real exact-head checkout preparation;
- real current-head dataset/inventory behavior under the finite evaluator;
- real current-head relation extraction outcomes;
- real candidate Build A / Build B determinism;
- real candidate CHP-B01..B12 results;
- real candidate P5-D3C2 package identity;
- real candidate QUALIFIED / REJECTED / BLOCKED adjudication;
- production promotion;
- CURRENT pointer mutation;
- real Vault writes;
- background observer execution;
- polling;
- Graph/Search CURRENT semantics.

The synthetic fixture is not evidence that a real monitored branch candidate will qualify.

## Verdict

**PASS — P5-D3D IMPLEMENTATION AND SYNTHETIC-FIXTURE QUALIFICATION**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This is not independent execution by the assistant.

## Next governed frontier

The next authorized boundary is:

    P5-D3E —
    REAL EXACT-HEAD SANDBOX
    CANDIDATE EVALUATION QUALIFICATION

P5-D3E must take one exact real candidate HEAD in a sacrificial isolated repository and execute the already-qualified P5-D3D finite evaluator end-to-end.

P5-D3E must still preserve:

- no production promotion;
- no CURRENT mutation;
- no real Vault write;
- no background observer;
- no polling;
- no Graph/Search CURRENT semantics.

P5-D3E may qualify only the real exact-head sandbox evaluation path.
