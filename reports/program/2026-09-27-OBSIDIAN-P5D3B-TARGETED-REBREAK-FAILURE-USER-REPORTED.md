# OBSIDIAN P5-D3B — TARGETED RE-BREAK FAILURE

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following local Windows execution result and raw unittest traceback were supplied by the user.

This was not independently executed by the assistant.

## Tested functional candidate

    1f7005eb4dd2f59d7416c0862a149ab092e7febc

Branch:

    feat/obsidian-projection-p5d3b-current-head-semantic-bridge-v0.1

## Reported result

Targeted P5-D3A + P5-D3B test batch:

    Ran 114 tests
    FAILED (failures=1)
    TARGETED_EXIT_CODE=1
    CONTROL_CLONE_CLEAN=PASS

The full Obsidian regression suite and real-head bridge harness were not executed because the governed wrapper stopped at the targeted-test failure.

## Exact failing breaker

    tests.obsidian_projection.test_p5d3b_adversarial
    P5D3BAdversarialTests.test_input_is_not_mutated_by_assignment

Failing forbidden literal:

    entry.content_mode =

Observed implementation text contains:

    entry.content_mode == "METADATA_ONLY"
    entry.content_mode == "FULL_TEXT"

The substring-based breaker therefore matched the left prefix of a comparison expression and produced a false positive.

## Technical interpretation

This evidence does NOT establish that the bridge mutates DynamicInventory input.

The bridge input dataclasses are frozen and the behavioral mutation test passed.

The failing breaker implementation is too coarse because string containment cannot distinguish:

    assignment
        entry.content_mode = ...

from:

    comparison
        entry.content_mode == ...

The correct correction is to replace substring assignment detection with AST assignment-target inspection.

## Scope of authorized correction

Only the adversarial breaker implementation is to be corrected.

The following P5-D3B functional artifacts are not implicated by this failure:

    current_head_semantic_bridge.py
    p5d3b_verify.py
    current_head_semantic_bridge_contract_v0_1.json

No semantic policy, runtime authority, bridge behavior, or qualification rule is to be weakened.

## Verdict

**FAIL — TARGETED RE-BREAK NOT QUALIFIED**

Cause:

    FALSE POSITIVE IN SUBSTRING-BASED INPUT-MUTATION BREAKER

P5-D3B remains unqualified.

A corrected functional candidate must be created and re-broken from the start.
