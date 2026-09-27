# OBSIDIAN P5-D3B — CURRENT-HEAD SEMANTIC BRIDGE QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Qualified functional candidate

Exact corrected P5-D3B functional candidate:

    b45a692bc90953e1cfe06106da596023ed2fb248

Branch:

    feat/obsidian-projection-p5d3b-current-head-semantic-bridge-v0.1

The previous functional candidate:

    1f7005eb4dd2f59d7416c0862a149ab092e7febc

remains a failed targeted-test candidate due to a false-positive substring mutation breaker.

The corrected candidate changed only the adversarial mutation breaker to structural AST inspection. The bridge implementation, verifier and contract remained unchanged.

## Reported regression result

The user reported:

    Ran 851 tests in 12.119s
    OK
    P5D3B_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN_AFTER_TESTS=PASS

The governed wrapper therefore passed the corrected targeted gates and the full tests/obsidian_projection regression suite before proceeding to real-head execution.

## Real monitored HEAD identity

The user-reported run fetched:

    origin/integration/system-v1

and resolved:

    SOURCE_HEAD=9ab446cb602f41bc461ef56b790b2776cf15a217
    SOURCE_TREE=d399ca0ad8a1c05a4f0850e5b5019f8a60422bdb

## Real-head bridge result

Reported schema:

    ATDS_OBSIDIAN_P5D3B_REAL_HEAD_BRIDGE_REPORT_V0_1

Reported status:

    PASS

Exact bridge contract:

    7015db1206cd40b703795d12519707a6455b4fc3

Reported dynamic inventory digest:

    2cad27ec04c914f4457f841af19ea9b0256d2e50ebe0625c06cc52c06bd770ab

Reported bridge entry digest:

    d7cd9b99116392730a37d63189851f66f215b1eadb3409a16d4f8511116926b6

Reported semantic-record digest:

    8fa1283733e5d9761a535cd3cf9e0276d004631246cb32d5da7997a6980bb909

Reported counts:

    source_blob_count=923
    full_text_count=905
    metadata_only_count=18
    semantic_record_count=923

Count invariants therefore hold:

    905 + 18 = 923
    semantic_record_count = source_blob_count = 923

No fixed expected corpus size was used.

## Body-read safety

Reported:

    all_semantic_body_read_false=true
    all_metadata_only_downstream_body_read_false=true

This establishes, for the reported real-head run, that P5-D3B preserved the no-body-read bridge boundary and did not grant downstream body-read authority to METADATA_ONLY entries.

## Mutation / authority boundary

Reported:

    canonical_worktree_write_required=false
    projection_modified=false
    real_vault_modified=false
    fixed_expected_source_count_used=false

Final wrapper result:

    P5D3B_REAL_HEAD_BRIDGE=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3B_QUALIFICATION_EXECUTION_COMPLETED=PASS

## Qualified P5-D3B boundary

P5-D3B now qualifies:

- direct DynamicInventory -> current-head semantic bridge input mapping;
- exactly one bridge entry and one conservative SemanticRecord per DynamicInventory entry;
- no FrozenInventory coercion;
- no pilot 74-record assumption;
- no silent source-entry drop;
- exact source repository/branch/commit/tree/path/blob provenance preservation;
- content_mode preservation;
- selection_zone preservation as non-semantic provenance;
- conservative semantic defaults without source-body reads;
- METADATA_ONLY body-read prohibition;
- deterministic bridge-entry and semantic-record digests;
- real-head execution over the exact monitored branch HEAD resolved during qualification.

## Explicit limitations preserved

P5-D3B does NOT qualify:

- body-derived semantic enrichment;
- legacy classifier execution against DynamicInventory;
- legacy relation extraction for unfiltered bridge output;
- the historical P2 projection builder as current-head qualified;
- candidate-generation staging;
- finite candidate-evaluation orchestration;
- production promotion;
- continuous Vault writes;
- background observer execution;
- polling;
- Graph/Search CURRENT semantics.

The historical relation extractor remains incompatible with unfiltered METADATA_ONLY bridge records because it reads source bodies.

The historical builder remains pilot-bound and therefore requires governed current-head adaptation before deterministic current-head projection A/B can be claimed.

## Verdict

**PASS — P5-D3B CURRENT-HEAD SEMANTIC PROJECTION BRIDGE QUALIFIED**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

This does not constitute independent local execution by the assistant.

## Next governed frontier

The next preregistered boundary is:

    P5-D3C — CANDIDATE GENERATION STAGING CONTRACT

P5-D3C must define a real candidate-generation package and sealing/verification model.

It must not relabel the P5-C2 experimental fixture generator as a current-head packager and must not invoke promotion or mutate CURRENT.

The later P5-D3D orchestrator must also include or depend on a governed current-head builder/relation adaptation that preserves the qualified P5-D3B METADATA_ONLY no-body-read boundary.
