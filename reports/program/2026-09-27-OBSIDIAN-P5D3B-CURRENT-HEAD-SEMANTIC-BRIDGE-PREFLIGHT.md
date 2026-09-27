# OBSIDIAN P5-D3B — CURRENT-HEAD SEMANTIC BRIDGE PREFLIGHT

Date: 2026-09-27

## Scope

P5-D3B closes the qualified P5-D3A interface gap between:

    P5-B2 DynamicInventory

and:

    current-head semantic projection input

It does not qualify or execute a current-head projection builder, relation extractor, candidate-generation packager, evaluation orchestrator, promotion path, background observer, or Vault write.

## Qualified predecessor

P5-D3A qualification commit:

    d1198a5b7e32607d2a2ef46084f6d11bca36b3e2

P5-D3A qualification report blob:

    bf8c5e917b08a6a1b1de7fdd7c0098a5969bfb87

P5-B2 qualified implementation blob:

    5f6ed61f36e889dc27ef14ef09467ada9f9f0f58

## Candidate branch

    feat/obsidian-projection-p5d3b-current-head-semantic-bridge-v0.1

## Exact functional candidate

    1f7005eb4dd2f59d7416c0862a149ab092e7febc

Later report commits are evidence-only and do not replace this candidate.

## Exact candidate artifacts

Contract:

    tools/obsidian_projection/current_head_semantic_bridge_contract_v0_1.json
    blob: 7015db1206cd40b703795d12519707a6455b4fc3

Bridge implementation:

    tools/obsidian_projection/current_head_semantic_bridge.py
    blob: ff3c2dd232487594a5283a9ab7750780ac098f2d

Real-head qualification harness:

    tools/obsidian_projection/p5d3b_verify.py
    blob: 9b283a2198fcc464b9ac75b07286b07713efd666

Contract tests:

    tests/obsidian_projection/test_current_head_semantic_bridge_contract_v0_1.py
    blob: 97276fbfa4a3bb91a019fcfdd59cc93fc43ca156

Behavioral tests:

    tests/obsidian_projection/test_current_head_semantic_bridge.py
    blob: 23209a5fdf8c0ea8be1dad1fda564d4e8ce56f43

Harness tests:

    tests/obsidian_projection/test_p5d3b_verify.py
    blob: e87f25ab5e4cb0c86024647cc83a0d8c6268de0a

Adversarial tests:

    tests/obsidian_projection/test_p5d3b_adversarial.py
    blob: 755c899b36eefb0c708543fa9c072f4b2f6eab32

Documentation:

    docs/OBSIDIAN-P5D3B-CURRENT-HEAD-SEMANTIC-PROJECTION-BRIDGE-V0.1.md
    blob: 7fc086bd88745187146b2fe5faafd14de234321f

## Static inventory

Required breakers in contract:

    84 unique

Persisted Python test methods:

    contract = 21
    behavioral = 37
    verifier = 10
    adversarial = 22

These are repository counts, not execution evidence.

## Bridge boundary

The bridge consumes only:

    DynamicInventory

It does not instantiate or load:

    FrozenInventory
    pilot_inventory_v0_1.json
    semantic_classification_rules_v0_1.json

It does not call:

    classify_inventory()
    classify_record()
    extract_relations()
    build_projection_from_records()

The bridge itself performs no source-body read.

## One-to-one mapping

Every P5-B2 inventory entry must produce exactly one bridge entry and one conservative semantic record.

No fixed corpus count is used.

No silent drop is permitted.

## Conservative semantics

V0.1 does not perform body-derived semantic inference.

All semantic axes remain conservative UNKNOWN/NONE defaults.

The source Git blob remains CANONICAL and TRACKED_IN_GIT_TREE.

selection_zone is preserved as non-semantic provenance and may not determine semantic axes or artifact family.

## Content-mode boundary

FULL_TEXT:

    disposition = SEMANTIC_FULL_TEXT
    semantic_body_read = false
    downstream_body_read_allowed = true

METADATA_ONLY:

    disposition = SEMANTIC_METADATA_ONLY
    artifact_family = METADATA_ONLY
    semantic_body_read = false
    downstream_body_read_allowed = false

## Legacy relation/builder boundary

The historical relation extractor reads and UTF-8 decodes every SemanticRecord body, therefore it is not safe for unfiltered METADATA_ONLY bridge records.

The historical P2 projection contract remains pilot-bound and includes pilot_source_count = 74.

P5-D3B therefore does not claim the old builder/relation stack is current-head qualified.

## Real-head qualification harness

The harness may reuse qualified P5-B2 against one exact monitored HEAD/tree.

It emits summary only and verifies:

- exact source HEAD/tree binding;
- dynamic inventory digest binding;
- bridge count == dynamic inventory count;
- FULL_TEXT / METADATA_ONLY count equality;
- semantic record count equality;
- no semantic body read;
- no downstream body-read authority for METADATA_ONLY.

It writes neither Vault nor projection.

No expected count such as 74 or 908 is hardcoded.

## Functional delta

Relative to the qualified P5-D3A checkpoint, the functional candidate adds exactly eight P5-D3B files and modifies no predecessor file.

## Required local qualification

Before P5-D3B may qualify:

1. recover exact functional candidate HEAD 1f7005eb4dd2f59d7416c0862a149ab092e7febc;
2. require a clean control checkout;
3. py_compile bridge, verifier and all four P5-D3B test modules;
4. run targeted P5-D3B contract/behavior/verifier/adversarial tests;
5. run the full tests/obsidian_projection suite;
6. fetch origin/integration/system-v1;
7. resolve its exact HEAD and tree;
8. execute the P5-D3B real-head harness against that exact identity;
9. require harness status PASS;
10. require final source-clean control checkout.

No P5-D3C work is authorized before these gates pass.

## Next governed boundary on PASS

    P5-D3C — CANDIDATE GENERATION STAGING CONTRACT
