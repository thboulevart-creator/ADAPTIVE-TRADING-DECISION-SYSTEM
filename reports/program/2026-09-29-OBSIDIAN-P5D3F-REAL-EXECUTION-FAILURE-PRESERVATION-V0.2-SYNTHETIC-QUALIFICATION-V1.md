# OBSIDIAN P5-D3F — REAL EXECUTION FAILURE-PRESERVATION V0.2 SYNTHETIC QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed synthetic re-break for the corrected real-execution runner.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    6f60851987500c0b3e538e9a6bf162705ae73615

Exact qualification candidate:

    d8639fdbaf773f5efbce91b7923723b20cf840d3

Corrected real execution runner blob:

    1b44e12a6c23715ea3d5055c9263f4bccb67fe39

Frozen runner tests blob:

    64033e4b2fe652a936b690293557bcd0eeac2c4f

Governed synthetic re-break blob:

    c8a5e4f52001be17673cb8ecefb4c4871066f6e0

Persistent handoff implementation blob:

    d2f40c8b2c8fb06b37bb34442c59d78222046452

Persistent handoff gate contract blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## User-reported governed result

Targeted corrected real-runner tests:

    Ran 10 tests in 0.010s
    OK

Complete historical Obsidian suite:

    Ran 1219 tests in 182.873s
    OK

Terminal markers:

    P5D3F_PERSISTENT_REAL_RUNNER_TARGETED=PASS
    P5D3F_PERSISTENT_REAL_RUNNER_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_PERSISTENT_REAL_RUNNER_REBREAK_COMPLETED=PASS

No FAIL, ERROR, or BLOCKED marker was reported in the completed governed run.

## Adjudication

    P5-D3F REAL EXECUTION FAILURE-PRESERVATION V0.2 — SYNTHETIC QUALIFICATION = PASS

The corrected runner is qualified against its frozen targeted surface and the complete historical Obsidian suite.

## Failure semantics now frozen

On any future governed real execution failure:

- the original execution exception must remain visible;
- a read-only residual snapshot must be emitted;
- persistent staging residuals must be preserved;
- no rmdir/unlink/delete cleanup may mask the original failure.

## Current persistent prestate carried forward from audit

    PERSISTENT STAGING = PRESENT_EMPTY
    PROMOTION-HANDOFF.json = ABSENT

This state is admissible to the qualified implementation through validate_staging_prestate = PRESENT_EMPTY.

## Next exact gate

    NEW HUMAN ONE-SHOT REAL P5-D3F PERSISTENT HANDOFF AUTHORIZATION

The previous one-shot authorization is consumed and cannot be reused.

A new explicit human authorization is required before any real retry.

## Authority remains closed until new authorization

- real persistent handoff retry;
- any real-Vault write;
- CURRENT / CURRENT.tmp mutation;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage A;
- Stage B;
- background observer / polling;
- P5-D4;
- P6.
