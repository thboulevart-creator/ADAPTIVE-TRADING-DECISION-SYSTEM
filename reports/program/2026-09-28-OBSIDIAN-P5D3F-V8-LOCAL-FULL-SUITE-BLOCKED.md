# OBSIDIAN P5-D3F — V8 LOCAL FULL-SUITE BLOCKED REPORT

Date: 2026-09-28

## Evidence status

USER-REPORTED LOCAL EXECUTION.

Not independent execution evidence.

## Verified GitHub state before persistence

Branch:

    feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1

Remote HEAD:

    e03b32d2b8f8d1e0633c47b1ef6d2d6b79a353b9

V8 functional candidate:

    6b45681bf060d6571782b83593a347ca6acd7a30

## User-reported V8 local execution

The governed run reached the V8 candidate and the historical suite result was:

    Ran 1090 tests in 19.545s
    FAILED (failures=1, errors=1)
    BLOCKED: full Obsidian suite failed

Remaining failures:

1. test_p5d3d_verify.P5D3DSyntheticQualificationTests.test_full_synthetic_finite_evaluation_passes

       SyntheticQualificationBlockedError:
       synthetic control evaluation blocked

2. test_p5d3e_verify.P5D3EVerifyTests.test_pre_resolved_sandbox_exercises_full_qualified_core

       expected PASS_SYNTHETIC_PRE_RESOLVED_SANDBOX
       actual BLOCKED_REAL_EXACT_HEAD_EVALUATION

The prior direct P3-A and P2 core raw-byte pin failures observed in V7 were no longer present in the filtered failure output.

## Adjudication

Supported:

- V8 removed the previously observed direct historical raw-byte pin failures;
- the remaining full-suite block is now concentrated in the synthetic finite-evaluation / pre-resolved sandbox path;
- P5-D3F is still unqualified because the full historical suite is not green.

Not yet proven:

- exact common cause of the P5-D3D and P5-D3E failures;
- whether an additional uncanonicalized dependency is involved;
- whether the two failures are one cascade or two independent defects.

## Next action

Perform static code inspection first, then one compact targeted local diagnostic if needed.

No runner mutation is authorized until the common failure cause is identified.
