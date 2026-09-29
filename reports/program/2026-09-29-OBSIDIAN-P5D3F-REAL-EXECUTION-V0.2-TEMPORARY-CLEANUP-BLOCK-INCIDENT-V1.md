# OBSIDIAN P5-D3F — REAL EXECUTION V0.2 TEMPORARY CLEANUP BLOCK INCIDENT V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL REAL-EXECUTION ATTEMPT with the synthetically-qualified failure-preservation V0.2 runner.

GitHub execution authority state was independently reverified after the attempt.

## Authorized execution identity

Execution branch:

    feat/obsidian-projection-p5d3f-persistent-real-execution-failure-preservation-v0.2

Authorized runner HEAD:

    28599d5e5a89c70ec70a018e604458d16e8be4cd

Corrected real runner blob:

    1b44e12a6c23715ea3d5055c9263f4bccb67fe39

Persistent handoff implementation blob:

    d2f40c8b2c8fb06b37bb34442c59d78222046452

## User-reported output

    P5D3F_PERSISTENT_REAL_EXECUTION_RUNTIME_IDENTITY=PASS
    P5D3F_PERSISTENT_STAGING_PRESTATE=PRESENT_EMPTY
    P5D3F_PERSISTENT_FAILURE_ORIGINAL=PersistentHandoffBlockedError: BLOCKED_TEMPORARY_CLEANUP
    P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON={"entries":[{"path":"packages","type":"DIRECTORY"}],"exists":true,...,"state":"PRESENT_NONEMPTY"}
    BLOCKED: PersistentHandoffBlockedError: BLOCKED_TEMPORARY_CLEANUP
    EXIT_CODE=2

## Adjudication

    REAL EXECUTION = BLOCKED
    SUCCESS = NOT ESTABLISHED
    READY_UNAUTHORIZED HANDOFF = NOT ESTABLISHED
    RESULT_JSON = NOT EMITTED
    REAL_VAULT_ZERO_MUTATION PASS = NOT EMITTED
    AUTHORIZATION = CONSUMED
    SILENT RETRY = FORBIDDEN

Persistent staging changed from PRESENT_EMPTY to:

    PRESENT_NONEMPTY
    entries = packages/ directory only

No PROMOTION-HANDOFF success evidence was emitted.

## Static masking finding

The V0.2 runner now correctly preserves the exception returned by execute_persistent_production_handoff.

However, the qualified persistent handoff implementation itself contains a finally block that executes:

    shutil.rmtree(temp_root)

and converts any cleanup OSError to:

    PersistentHandoffBlockedError("BLOCKED_TEMPORARY_CLEANUP")

Because this occurs in finally, it can replace an earlier exception from the handoff body.

Therefore the runner-level marker:

    P5D3F_PERSISTENT_FAILURE_ORIGINAL=PersistentHandoffBlockedError: BLOCKED_TEMPORARY_CLEANUP

is the original exception visible to the runner, but it is not sufficient to prove that temporary cleanup was the first execution failure.

An earlier inner failure may still have been masked inside execute_persistent_production_handoff.

## Evidence implied by the staging residual

The presence of an empty packages/ directory shows that execution progressed beyond initial staging prestate validation and into the qualified handoff runtime far enough to create the packages root.

The absence of a reported successful handoff means the READY_UNAUTHORIZED materialization did not complete.

## Required next step

READ-ONLY incident audit only:

- enumerate the exact staging tree;
- enumerate surviving OS temporary roots matching ATDS-P5D3F-PERSISTENT-HANDOFF-*;
- inspect candidate/evaluation residual layout, sizes, attributes and timestamps;
- inspect ACL/attributes for surviving temporary roots;
- do not delete or modify any residual;
- do not retry.

After evidence capture, the persistent handoff implementation itself must be corrected so temporary-cleanup failure cannot mask the first execution failure.

A new synthetic qualification and a new one-shot authorization will be required before any future real execution.

Real Vault write remains closed.
Live publication remains closed.
Stage A remains closed.
Stage B remains closed.
