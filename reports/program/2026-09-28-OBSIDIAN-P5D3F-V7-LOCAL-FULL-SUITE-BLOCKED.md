# OBSIDIAN P5-D3F — V7 LOCAL FULL-SUITE BLOCKED REPORT

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION.

Static GitHub inspection by assistant is identified separately below.

This report does not qualify P5-D3F.

## Verified GitHub state before persistence

Branch:

    feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1

Remote HEAD:

    e917b193099a78d2a375524abf29f91daaabe016

V7 functional candidate:

    49eda71d200cca7a860fd9b0d212aa0e94e9cea7

## User-reported V7 local execution

The governed V7 run reached and passed the P5-D3F-specific gates:

    CONTROL_CLONE_CLEAN_BEFORE=PASS
    FETCHED_HEAD=e917b193099a78d2a375524abf29f91daaabe016
    REMOTE_RACE_GUARD=PASS
    P5D3F_RUNTIME_HEAD=49eda71d200cca7a860fd9b0d212aa0e94e9cea7
    P5D3F_CANONICAL_BLOB_MATERIALIZATION=PASS
    P5D3F_INDEX_STAT_REFRESH=PASS
    P5D3F_BYTE_PIN_COMPATIBILITY=PASS
    P5D3F_CONTRACT_BLOB=PASS
    P5D3F_CONTRACT_TEST_BLOB=PASS
    P5D3F_CONTRACT_PY_COMPILE=PASS
    P5D3F_CONTRACT_TARGETED=PASS

The full Obsidian suite then reported:

    Ran 1089 tests in 19.458s
    FAILED (failures=1, errors=4)
    BLOCKED: full Obsidian suite failed

Observed errors/failure:

1. test_first_open.FirstOpenHarnessUnitTests.test_dependency_blob_pins_match_persisted_package

       P3-A materialization contract blob mismatch
       expected=b11120c9f6d3ee68b253928b125747159536bbf0
       actual=8a6b93e59556a869d863f337d7f55360c0916d80

2. test_first_open_onedrive.P3D2OneDriveUnitTests.test_persisted_dependencies_are_pinned

       same P3-A materialization contract expected/actual mismatch

3. test_materialize.P3MaterializationTests.test_qualified_p2_core_blob_pins_match_package

       P2 core blob mismatch: tools/obsidian_projection/rendering.py
       expected=5111518bc4d842fd39f0e5a1a00f2cc66f681501
       actual=0572ff84b5272fc7cd53a4f855eeaac68ca9fea4

4. test_p5d3d_verify.P5D3DSyntheticQualificationTests.test_full_synthetic_finite_evaluation_passes

       SyntheticQualificationBlockedError:
       synthetic control evaluation blocked

5. test_p5d3e_verify.P5D3EVerifyTests.test_pre_resolved_sandbox_exercises_full_qualified_core

       expected PASS_SYNTHETIC_PRE_RESOLVED_SANDBOX
       actual BLOCKED_REAL_EXACT_HEAD_EVALUATION

No final full-rebreak PASS or final qualification marker was emitted.

## Static GitHub inspection

At the exact V7 functional candidate:

materialization_contract_v0_1.json Git blob:

    b11120c9f6d3ee68b253928b125747159536bbf0

This exactly equals the historical expected MATERIALIZATION_CONTRACT_BLOB used by first_open.py and first_open_onedrive.py.

rendering.py Git blob:

    5111518bc4d842fd39f0e5a1a00f2cc66f681501

This exactly equals the qualified P2 core pin stored in materialization_contract_v0_1.json.

Therefore the two directly observed expected pins are consistent with the committed GitHub candidate.

## Current interpretation

Strongly supported:

- the original V5/V6 Git stat issue is closed by V7 through the P5-D3F targeted gate;
- the full-suite block occurs later;
- the two directly observed historical expected pins are not stale relative to the candidate Git blobs;
- the local raw bytes seen by historical byte-pinned tests differ from the committed Git blobs for at least:
    - materialization_contract_v0_1.json
    - rendering.py

Not yet proven:

- exact cause of those local raw-byte differences;
- whether CRLF is the mechanism;
- whether additional P2/P3 pinned files have the same mismatch;
- whether the P5-D3D/P5-D3E failures are entirely downstream cascades from the same package-byte mismatch.

## Next bounded diagnostic

Before any V8 mutation, compare HEAD Git blob versus raw worktree blob and Git EOL classification for the complete directly relevant P2/P3 pinned dependency set.

No historical pin may be changed or repinned based on this failure.
