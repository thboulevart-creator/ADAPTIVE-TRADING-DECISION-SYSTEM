# OBSIDIAN P5-D3F — BLOCKED RUN EXECUTION DEPTH ADJUDICATION V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL READ-ONLY EVIDENCE plus SAME-ASSISTANT STATIC CONTROL-FLOW REVIEW of the frozen P5-D3F handoff runtime.

## User-reported residual evidence

Persistent staging immediate content:

    packages/ only

packages/ immediate content:

    empty

Latest surviving temporary execution root:

    C:\Users\Boulevart\AppData\Local\Temp\ATDS-P5D3F-PERSISTENT-HANDOFF-5dhvsovl

Top-level:

    candidate/
    evaluation/

evaluation/ top-level:

    build-a/
    build-b/
    candidate-package/

Candidate repository:

    HEAD = 5a61c6150583234b486f6dc614f5071e89cbd3c0
    TREE = 50347ff1f8cd41491e949c2716f9fc4c9d182f64
    clean = true

## Static control-flow implication

In run_finite_promotion_handoff, creation of persistent packages/ occurs only after:

- finite evaluator completion;
- evaluator outcome validation;
- build-count validation;
- candidate-package verification;
- PASS_SEALED_UNPROMOTED check;
- candidate/evaluator identity cross-check;
- source package byte-tree digest calculation;
- generation_id recovery.

Therefore the observed packages/ directory establishes that all of those preceding steps completed sufficiently to reach persistent handoff setup.

However, an empty packages/ directory does NOT prove that target generation creation itself failed.

The qualified runtime has its own failure cleanup:

    if not completed and target.exists():
        shutil.rmtree(target)

Therefore a target generation wrapper may have been created and later removed successfully after a subsequent inner failure.

## Main remaining observability defect

execute_persistent_production_handoff wraps its body in a finally that always attempts:

    shutil.rmtree(temp_root)

and raises BLOCKED_TEMPORARY_CLEANUP on cleanup failure.

That finally can replace any earlier body exception.

Consequently, the surviving temporary workspace is valuable evidence, but the exact first body exception cannot be reliably reconstructed from current residual shape alone.

## Adjudication

Further broad filesystem inspection is not required before correcting this masking defect.

Required correction is now architectural and bounded:

- preserve any body exception unchanged;
- preserve temp_root on body failure;
- expose temp_root path to the caller/audit;
- perform temporary cleanup only after body success;
- distinguish cleanup failure after an otherwise successful handoff from body failure;
- never silently delete failure evidence.

No real retry is authorized.

A corrected persistent-handoff implementation must be synthetically qualified before any new one-shot human authorization.
