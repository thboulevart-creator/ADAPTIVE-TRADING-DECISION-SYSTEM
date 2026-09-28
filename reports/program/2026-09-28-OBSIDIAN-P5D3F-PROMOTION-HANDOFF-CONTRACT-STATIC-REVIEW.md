# OBSIDIAN P5-D3F — PROMOTION HANDOFF CONTRACT STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static review.

This is not independent execution evidence.

This review does not qualify the contract and does not authorize P5-D3F runtime implementation.

## Candidate reviewed

Exact functional contract candidate:

    5e1aede1b2071c7985a0938ef97025f5e6c03cfa

Branch:

    feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1

Later preflight/static-review commits are evidence-only and do not replace the functional contract candidate.

## Functional artifact identities

Contract:

    tools/obsidian_projection/promotion_handoff_contract_v0_1.json

Blob:

    64744325251db350d26c0269090ce62d5fa5f2e8

Contract tests:

    tests/obsidian_projection/test_promotion_handoff_contract_v0_1.py

Blob:

    6c7f3d5e1962132f4b609b637d176e67ccd376d5

Documentation:

    docs/OBSIDIAN-P5D3F-PROMOTION-HANDOFF-CONTRACT-V0.1.md

Blob:

    e07dc28c106a17f426044cb057d7598fe7f05b38

Governed re-break runner:

    tools/obsidian_projection/run_p5d3f_contract_rebreak.ps1

Blob:

    f8d7b5406082d7f8fbe19bdfee7caa9f66c75e51

## Delta review

Relative to the end-of-day checkpoint:

    0f81d444bac91af4d504472d1901f9933cf3dc1b

the branch adds only P5-D3F architecture/contract/test/documentation/re-break-runner surfaces.

No existing qualified predecessor file is modified.

No publication runtime is present.

No CURRENT writer is added.

No real-Vault mutation implementation is added.

## Architectural review

### PASS — missing handoff boundary identified

P5-D3E successful cleanup deletes its candidate repository and evaluation workspace.

Therefore its SEALED_UNPROMOTED package is not a durable future publication input.

The contract correctly avoids weakening P5-D3E cleanup semantics.

It introduces a new finite boundary instead.

### PASS — P5-D4 name preserved

Existing contracts reserve:

    P5-D4 = BOUNDED_OBSERVER_LOOP_CANDIDATE

P5-D3F therefore occupies the missing finite handoff boundary and P5-D3G is reserved for a later finite live publication transaction.

This avoids silently changing the already-preregistered P5-D4 meaning.

### PASS — evaluation and publication remain separate

P5-D3F requires:

    fresh finite candidate evaluation
    outcome = QUALIFIED
    failure_code = null
    Build A == Build B
    METADATA_ONLY body reads = 0
    artifact/source completeness
    PASS_SEALED_UNPROMOTED package

but still requires all publication-authority flags to remain false.

Therefore:

    qualification != publication

is preserved.

### PASS — physical and logical promotion remain separate

P5-D2 PROMOTION_CONFIRMED is explicitly forbidden in P5-D3F.

A future publication component must first confirm physical publication before that logical event may be emitted.

### PASS — P5-D3C2 package is not extended or mutated

The P5-D3C2 package remains an unchanged inner package.

P5-D3F adds wrapper metadata outside it:

    PROMOTION-HANDOFF.json

The contract explicitly forbids placing handoff metadata inside the sealed package.

### PASS — copy identity is stronger than descriptor-only comparison

The contract requires:

    source package verification
    source package byte-tree digest before copy
    byte-exact/path-exact copy
    destination package byte-tree digest after copy
    source/destination byte-tree equality
    destination package verification
    source/destination descriptor equality

This prevents an implementation from treating a semantically similar but byte-different copy as equivalent.

### PASS — future consumers must reverify

A retained handoff is not trusted indefinitely.

The contract explicitly requires a future publication consumer to perform fresh read-only handoff verification before any publication action.

### PASS — staging/live boundary is explicit

Promotion staging must be outside the real Vault and may not alias it through symlink, junction or reparse behavior.

No live Vault write is authorized by P5-D3F.

## Contract inventory

Required adversarial breakers:

    65

Unique adversarial breakers:

    65

Contract test methods:

    21

The test surface covers:

- exact contract blob/schema;
- preservation of P5-D4 naming;
- exact P5-C2 authority binding;
- exact P5-C3R2 authority binding;
- exact P5-D2 logical-promotion boundary;
- exact P5-D3C2 package authority;
- P5-D3E cleanup preservation;
- first-real-candidate lineage not hardcoded as runtime authority;
- exact-head/network-free handoff core;
- finite evaluation gates;
- promotion-staging isolation;
- immutable inner package;
- alias/hard-link rejection semantics;
- publication-authority false requirements;
- scientific identity fields;
- read-only handoff verification;
- explicit READY_UNAUTHORIZED success;
- REJECTED/BLOCKED distinction;
- contract-only authority boundary;
- unique adversarial breaker registry;
- next-gate ordering.

## Required breaker families

Static inspection confirms preregistration of breakers for at least:

    P5-D3E ephemeral-package misuse
    cleanup-boundary weakening
    unqualified evaluator/verifier substitution
    candidate HEAD/TREE mismatch
    dirty/wrong candidate repository
    network fetch inside handoff core
    REJECTED laundering
    BLOCKED laundering
    scientific-digest omission
    Build A/B mismatch
    METADATA_ONLY body-read violation
    artifact/source incompleteness
    non-SEALED source package
    live-Vault overlap/aliasing
    staging Git contamination
    target overwrite
    hard-link/symlink/junction/reparse aliasing
    copy byte/path drift
    dropped/extra files
    sealed-package mutation
    handoff-record placement/order/canonicalization
    identity mismatch
    publication-authority laundering
    CURRENT creation
    real-Vault mutation
    P5-C2 pointer invocation
    P5-C3R2 writer invocation
    P5-D2 PROMOTION_CONFIRMED emission
    background execution
    polling
    Windows persistence
    Graph/Search semantic overclaim
    P5-D4 name reuse

## Static boundary verification

The contract currently states:

    contract_tests_only = true

and all of the following remain false:

    handoff_runtime_implementation_authorized
    sacrificial_handoff_execution_authorized
    production_handoff_execution_authorized
    real_vault_write_authorized
    current_pointer_creation_authorized
    current_pointer_mutation_authorized
    p5c2_pointer_primitive_invocation_authorized
    p5c3r2_current_writer_invocation_authorized
    p5d2_promotion_confirmed_event_authorized
    production_promotion_authorized
    automatic_promotion_authorized
    background_observer_authorized
    polling_loop_authorized
    windows_startup_registration_authorized
    scheduled_task_authorized
    windows_service_authorized
    graph_search_current_semantics_authorized

## Static limitations

No claim is made that:

- the Python contract tests have executed locally;
- the full Obsidian regression suite has passed with P5-D3F added;
- the PowerShell runner has executed on Windows;
- a promotion-staging directory has been created;
- a durable handoff implementation exists;
- any real Vault publication has occurred.

Those remain outside static evidence.

## Verdict

**STATIC REVIEW PASS — LOCAL CONTRACT RE-BREAK REQUIRED**

The next permitted action is exactly:

    execute P5-D3F contract re-break
    on functional candidate
    5e1aede1b2071c7985a0938ef97025f5e6c03cfa

A local PASS may qualify the P5-D3F contract and authorize the next boundary:

    P5-D3F IMPLEMENTATION CANDIDATE

A local FAIL/BLOCKED must be persisted and corrected before implementation.

P5-D3G and all live publication remain closed.
