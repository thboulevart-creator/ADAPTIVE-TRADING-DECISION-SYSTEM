# OBSIDIAN P5-D3F — LATEST BLOCKED RUN RESIDUAL SHAPE V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL READ-ONLY INSPECTION.

## Persistent staging

Immediate content:

    packages/    directory    LastWriteTime 2026-09-29 14:26:16

No child entry was displayed under packages/.

Therefore:

    staging root = PRESENT_NONEMPTY
    packages/ = PRESENT_EMPTY

## Latest surviving temporary execution root

    C:\Users\Boulevart\AppData\Local\Temp\ATDS-P5D3F-PERSISTENT-HANDOFF-5dhvsovl

Top-level:

    candidate/     LastWriteTime 2026-09-29 14:21:39
    evaluation/    LastWriteTime 2026-09-29 14:25:40

## Evaluation workspace top-level

    build-a/
    build-b/
    candidate-package/

Observed timestamps:

    build-a            14:23:09
    build-b            14:24:22
    candidate-package  14:25:40

This establishes that both deterministic builds and the final candidate package were produced before the blocked result.

## Temporary candidate identity

    HEAD = 5a61c6150583234b486f6dc614f5071e89cbd3c0
    TREE = 50347ff1f8cd41491e949c2716f9fc4c9d182f64
    CANDIDATE_CLEAN = TRUE

## Narrow execution-path inference

Given the qualified run_finite_promotion_handoff control flow and the observed residuals, execution progressed beyond:

- fresh candidate preparation;
- finite candidate evaluation;
- build-a;
- build-b;
- candidate-package materialization;
- source package availability;
- creation of persistent packages/ root.

The exact first failure is still not proven because execute_persistent_production_handoff can mask an earlier body exception with BLOCKED_TEMPORARY_CLEANUP in its finally block.

Since packages/ is empty, no generation wrapper is currently observed under persistent staging.

## Next diagnostic step

READ-ONLY only.

Inspect the already-built candidate-package using the qualified candidate-generation verifier, recover its generation_id and verification status, and inspect the exact expected persistent target path and packages/ filesystem semantics without creating it.

No delete, create, rename, retry, or cleanup is authorized.
