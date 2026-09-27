# OBSIDIAN P5-D3E — FIRST REAL EXACT-HEAD QUALIFICATION

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following PowerShell adjudication output was supplied by the user.
It was not independently executed by the assistant.

## Qualified P5-D3E implementation

Functional candidate:

    7c6ecec2498d48c4623ecd40aed6c3816f4930b9

Implementation qualification commit:

    1e03d539d48c0fb4760d1b6091e1b2faa125042b

P5-D3E contract blob:

    ae4b1691fae16fcd1616e265a089670b9654db4a

P5-D3E harness blob:

    bd7f63b08432a53eaff5deeb2147396eb60d723f

Qualified P5-D3D evaluator blob:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

## Real candidate evaluated

User-reported candidate HEAD:

    89710b879751d7fcebccf75cd03e64368f1b0e96

User-reported candidate TREE:

    dc85bdb0708f4980e3a0cead0f15c6d077f90290

GitHub verification confirms:

    commit exists
    tree = dc85bdb0708f4980e3a0cead0f15c6d077f90290
    commit message = A0: qualify governed V0.5 replay

At persistence time:

    integration/system-v1

still pointed to:

    89710b879751d7fcebccf75cd03e64368f1b0e96

This current branch position is contextual verification only.
The qualification binds the exact frozen candidate HEAD/TREE above.

## User-reported real-run adjudication

The user reported:

    PYTHON_EXIT_CODE=0
    REPORT_STATUS=PASS_REAL_EXACT_HEAD_FINITE_EVALUATION

    REAL_CANDIDATE_HEAD=89710b879751d7fcebccf75cd03e64368f1b0e96
    REAL_CANDIDATE_TREE=dc85bdb0708f4980e3a0cead0f15c6d077f90290

    REAL_BUILD_A_B_EQUAL=PASS
    REAL_METADATA_ONLY_BODY_READ_COUNT=0
    REAL_ARTIFACT_COMPLETENESS=PASS
    REAL_PACKAGE_SEALED_UNPROMOTED=PASS
    REAL_PACKAGE_REVERIFICATION=PASS

    P5D3E_REAL_EXACT_HEAD_QUALIFICATION=PASS
    CONTROL_CLONE_CLEAN_AFTER_REAL_RUN=PASS

    P5D3E_FIRST_REAL_EXACT_HEAD_RUN_COMPLETED=PASS

## Interpretation of wrapper PASS

The governed PowerShell wrapper prints:

    P5D3E_REAL_EXACT_HEAD_QUALIFICATION=PASS

only after checking all PASS invariants against the parsed P5-D3E report.

Therefore the supplied final PASS marker is consistent with the wrapper having validated, before emission:

    report status = PASS_REAL_EXACT_HEAD_FINITE_EVALUATION
    candidate_outcome = QUALIFIED
    failure_code = null
    candidate HEAD/TREE format valid
    required scientific SHA-256 identities present
    Build A projection tree = Build B projection tree
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count
    evaluator package status = PASS_SEALED_UNPROMOTED
    post-package reverification status = PASS_SEALED_UNPROMOTED
    post-package candidate-generation digest matches evaluator report
    P5-D2 result event emitted
    live projection head unchanged
    real_candidate_evaluated = true
    candidate-resolution network fetch performed = true
    evaluation network fetch performed = false
    candidate repository clean after
    control repository clean after
    real Vault modified = false
    CURRENT pointer created = false
    production promotion authorized = false
    candidate repository retained = false
    evaluation workspace retained = false

These individual values were enforced by the wrapper before the reported PASS marker.
Where the user did not separately paste the underlying JSON field values, they are not represented here as separate direct user-quoted lines.

## Real-path qualification established

This run qualifies the first real exact-head P5-D3E evaluation path for the frozen candidate:

    89710b879751d7fcebccf75cd03e64368f1b0e96

The path exercised:

    governed exact-head resolution
        ↓
    exact candidate HEAD/TREE freeze
        ↓
    sacrificial isolated Git repository
        ↓
    controlled P5-D2 activation
        ↓
    qualified P5-D3D finite evaluator
        ↓
    real DynamicInventory
        ↓
    real current-head semantic bridge
        ↓
    real Build A / Build B
        ↓
    CHP-B01..B12
        ↓
    P5-D3C2 candidate package
        ↓
    PASS_SEALED_UNPROMOTED
        ↓
    post-package read-only reverification
        ↓
    QUALIFIED

## Critical real-candidate properties demonstrated

Directly user-reported:

    Build A/B equality = PASS
    METADATA_ONLY body read count = 0
    artifact completeness = PASS
    sealed-unpromoted package = PASS
    package reverification = PASS
    control repository clean after run = PASS

The final governed PASS also implies that the wrapper's publication and cleanup guards passed before its final marker.

## Publication boundary remains closed

This qualification does NOT authorize:

    production promotion
    CURRENT pointer mutation
    real Vault writes
    background observer execution
    polling
    Windows startup/task/service persistence
    Graph/Search CURRENT semantics

The candidate remained:

    SEALED_UNPROMOTED

throughout the qualified path.

## Verdict

**PASS — P5-D3E FIRST REAL EXACT-HEAD CANDIDATE EVALUATION QUALIFIED**

Evidence basis:

    USER-REPORTED LOCAL EXECUTION

GitHub independently verifies only the persisted repository identities described above, not the local Windows execution itself.

## Governance consequence

P5-D3E has now demonstrated both:

1. synthetic/pre-resolved implementation qualification;
2. one real exact-head end-to-end candidate qualification.

The next boundary must remain separately governed before any publication or live-current behavior is introduced.
