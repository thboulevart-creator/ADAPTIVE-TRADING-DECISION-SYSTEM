# OBSIDIAN P5-D3F — RECOVERY REAL RUNNER V0.3 HISTORICAL COMPATIBILITY CORRECTION V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL SYNTHETIC RUN plus SAME-ASSISTANT STATIC REVIEW.

## Observed governed result

Targeted V0.3 recovery-runner tests:

    Ran 10 tests
    OK

Complete historical Obsidian suite:

    Ran 1252 tests
    FAILED (failures=2)

Historical failures:

    test_runner_branch_is_exact
    test_runtime_authority_pins_are_exact

## Root cause

The V0.3 recovery runner had replaced the historical V0.2 runner at the same module path:

    tools/obsidian_projection/p5d3f_persistent_production_handoff_real_execution.py

Historical tests intentionally freeze the V0.2 runner's branch and authority pins.

Therefore the full-suite failures correctly detected an authority/history overwrite.

## Correction

V0.2 runner restored byte-exact at its historical path.

Historical V0.2 runner blob:

    1b44e12a6c23715ea3d5055c9263f4bccb67fe39

Historical V0.2 tests blob remains:

    64033e4b2fe652a936b690293557bcd0eeac2c4f

V0.3 recovery runner moved to a distinct versioned path:

    tools/obsidian_projection/p5d3f_recovery_real_execution_v0_3.py

V0.3 runner blob:

    2d22734c73c7e95eed88141c3237ed61afe39dfe

V0.3 tests now import only that versioned module.

V0.3 tests blob:

    0bb06b5a836b69f3a83e57ad0840b21fe993339c

Governed re-break updated to the versioned runner path and exact new blobs.

Re-break blob:

    e369efc5276c70dfde57a172614fad42ad974de3

## Adjudication

This is a compatibility/authority-preservation correction.

No V0.3 runner behavior was broadened.
No historical V0.2 test expectation was weakened.
No historical V0.2 runner authority was rewritten.

    TARGETED V0.3 QUALIFICATION = PREVIOUSLY PASS
    FULL HISTORICAL SUITE = PREVIOUSLY FAIL
    CORRECTED FULL QUALIFICATION = PENDING

Real execution remains unauthorized.
