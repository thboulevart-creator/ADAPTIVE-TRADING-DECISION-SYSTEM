# OBSIDIAN P5-D3D — PY_COMPILE FAILURE

Date: 2026-09-27

## Evidence status

**USER-REPORTED LOCAL EXECUTION**

The following Windows execution result was supplied by the user.
It was not independently executed by the assistant.

## Tested functional candidate

    53ff8ba07baa4ff7be90d9d24f53da8e9601e019

Branch:

    feat/obsidian-projection-p5d3d-implementation-v0.1

## Reported execution

The governed wrapper reached:

    REMOTE_RACE_GUARD=PASS
    P5D3D_RUNTIME_HEAD=53ff8ba07baa4ff7be90d9d24f53da8e9601e019
    P5D3D_PROJECTION_CONTRACT_BLOB=PASS
    P5D3D_EVALUATOR_CONTRACT_BLOB=PASS
    P5D3D_RUNTIME_BLOBS=PASS

It then failed during:

    PY_COMPILE

Exact reported error:

    File "tests\obsidian_projection\test_p5d3d_adversarial.py", line 414
      "Path("CURRENT",
                    ^
    SyntaxError: unterminated string literal

Wrapper result:

    BLOCKED: P5-D3D py_compile failed.

Therefore:

    P5D3D_TARGETED_IMPLEMENTATION_TESTS=NOT_EXECUTED
    P5D3D_FULL_REBREAK=NOT_EXECUTED
    P5D3D_SYNTHETIC_QUALIFICATION=NOT_EXECUTED
    P5D3D_IMPLEMENTATION_QUALIFICATION=NOT_GRANTED

## Static adjudication

The failing line belongs only to:

    tests/obsidian_projection/test_p5d3d_adversarial.py

The intended forbidden literal is:

    Path("CURRENT

The persisted test incorrectly encoded it as:

    "Path("CURRENT",

which is invalid Python syntax.

The five runtime implementation blobs are not implicated:

    current_head_relations.py
    current_head_projection.py
    current_head_breakers.py
    finite_candidate_evaluator.py
    p5d3d_verify.py

The qualified P5-D3D contracts are not implicated.

## Authorized correction scope

Correction is limited to:

    tests/obsidian_projection/test_p5d3d_adversarial.py

Replace the invalid Python literal with a valid string carrying the exact same forbidden text.

No runtime behavior, contract authority, breaker meaning, outcome semantics or synthetic qualification expectation may be weakened.

## Verdict

**FAIL — PY_COMPILE BLOCKED**

Cause:

    ADVERSARIAL TEST STRING QUOTING ERROR

P5-D3D implementation remains unqualified.

A corrected functional candidate must restart the governed qualification from py_compile.
