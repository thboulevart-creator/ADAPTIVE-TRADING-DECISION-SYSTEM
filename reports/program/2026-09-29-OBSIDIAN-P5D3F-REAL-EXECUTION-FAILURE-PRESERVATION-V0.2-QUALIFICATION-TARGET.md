# OBSIDIAN P5-D3F — REAL EXECUTION FAILURE-PRESERVATION V0.2 QUALIFICATION TARGET

Date: 2026-09-29

## Reason for correction

The first governed real execution attempt reached the real runner and changed the persistent staging prestate from ABSENT to PRESENT_EMPTY.

The runner then emitted WinError 5 on the exact staging path.

Subsequent read-only audit established:

    persistent staging = PRESENT_EMPTY
    PROMOTION-HANDOFF.json = absent

A Python filesystem-semantics probe established:

    implementation _is_alias = false
    alias-free chain = PASS
    reparse bit = false
    validate_persistent_paths = PASS
    validate_staging_prestate = PRESENT_EMPTY

Therefore the OneDrive path is not blocked by the governed Python alias/reparse guard.

Static inspection identified a failure-observability defect: the old runner attempted cleanup deletion after catching the original execution exception. A cleanup PermissionError could therefore replace and hide the original exception.

## Corrected candidate

    d8639fdbaf773f5efbce91b7923723b20cf840d3

Corrected real execution runner blob:

    1b44e12a6c23715ea3d5055c9263f4bccb67fe39

Frozen runner tests blob:

    64033e4b2fe652a936b690293557bcd0eeac2c4f

Governed synthetic re-break blob:

    c8a5e4f52001be17673cb8ecefb4c4871066f6e0

Targeted tests:

    10

## Corrected failure semantics

On execution failure the runner now:

1. preserves the original exception;
2. performs only a read-only residual snapshot;
3. emits P5D3F_PERSISTENT_FAILURE_ORIGINAL;
4. emits P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON;
5. performs no rmdir/unlink/delete cleanup under persistent staging;
6. re-raises the original exception.

Persistent residual evidence is preserved for audit.

## Unchanged authority

The corrected runner does not expand authority.

Still forbidden:

- real Vault write;
- CURRENT/CURRENT.tmp mutation;
- real-Vault generation materialization;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage A;
- Stage B;
- background execution;
- P5-D4;
- P6.

## Required qualification

Before any new real authorization:

- exact remote-race guard;
- exact candidate HEAD;
- exact runner/test/runtime blob pins;
- static surface scan;
- Python compile;
- 10 targeted tests;
- complete historical Obsidian suite;
- clean control clone.

Only after PASS may a new one-shot human authorization be requested.
