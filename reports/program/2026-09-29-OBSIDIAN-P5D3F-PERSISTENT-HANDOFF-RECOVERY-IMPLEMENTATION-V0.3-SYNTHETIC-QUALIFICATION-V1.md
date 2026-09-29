# OBSIDIAN P5-D3F — PERSISTENT HANDOFF RECOVERY IMPLEMENTATION V0.3 SYNTHETIC QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed synthetic recovery-implementation re-break.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    970c2fc8fb84be4115a1cddcb652e3fef5182233

Exact qualification candidate:

    c3de1640df0280c34a667b356be279ce3e1eea88

Recovery implementation blob:

    dcd70a9d9794675eab90e41df560f8b030b5dbf3

Frozen targeted tests blob:

    242305bc0f95bbe243158b5c806255508093a357

Governed recovery-implementation re-break blob:

    5d7693552826f2394024ec3c7c3b280ad8b6f5be

Qualified recovery contract V0.2 blob:

    aef627936b6f745017bcace7e8a3e44270f95674

## User-reported governed result

Targeted recovery-implementation tests:

    Ran 13 tests in 0.033s
    OK

Complete historical Obsidian suite:

    Ran 1242 tests in 197.056s
    OK

Terminal markers:

    P5D3F_RECOVERY_IMPLEMENTATION_TARGETED=PASS
    P5D3F_RECOVERY_IMPLEMENTATION_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_RECOVERY_IMPLEMENTATION_REBREAK_COMPLETED=PASS

No FAIL, ERROR, or BLOCKED marker was reported.

## Adjudication

    P5-D3F PERSISTENT HANDOFF RECOVERY IMPLEMENTATION V0.3 — SYNTHETIC QUALIFICATION = PASS

The implementation is qualified against the frozen recovery/adversarial test surface and the complete historical Obsidian suite.

## Qualified recovery semantics

The implementation now:

- admits only the exact empty-packages recovery state;
- blocks arbitrary nonempty staging;
- preserves body failures and surviving temporary evidence;
- never lets temporary cleanup mask a body failure;
- attempts temporary cleanup only after body success;
- classifies cleanup failure after body success distinctly and binds the successful handoff result for audit;
- preserves the real-Vault zero-mutation requirement;
- preserves READY_UNAUTHORIZED semantics.

## Next exact frontier

    P5-D3F — RECOVERY REAL EXECUTION RUNNER V0.3

A new real-execution runner must be frozen and synthetically qualified against this exact V0.3 implementation before any new human one-shot authorization.

Still NOT authorized:

- real execution retry;
- real Vault write;
- CURRENT / CURRENT.tmp mutation;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage A;
- Stage B;
- P5-D4;
- P6.
