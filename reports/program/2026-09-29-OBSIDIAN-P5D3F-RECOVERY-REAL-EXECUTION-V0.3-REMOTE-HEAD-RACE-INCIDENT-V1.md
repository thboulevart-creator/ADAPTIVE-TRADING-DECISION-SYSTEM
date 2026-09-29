# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION V0.3 REMOTE HEAD RACE INCIDENT V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL REAL-EXECUTION ATTEMPT using the synthetically-qualified P5-D3F Recovery V0.3 runner.

GitHub runner authority was independently reverified after the attempt.

## Authorized execution identity

Authorization-bearing runner branch HEAD:

    599f95bd0a9a3d409925ff2d15c7656d3bf445fb

Versioned V0.3 recovery real-execution runner blob:

    2d22734c73c7e95eed88141c3237ed61afe39dfe

Qualified recovery implementation blob:

    dcd70a9d9794675eab90e41df560f8b030b5dbf3

Qualified recovery contract V0.2 blob:

    aef627936b6f745017bcace7e8a3e44270f95674

## User-reported governed output

    P5D3F_PERSISTENT_REAL_EXECUTION_RUNTIME_IDENTITY=PASS
    P5D3F_PERSISTENT_STAGING_PRESTATE=PRESENT_EMPTY_PACKAGES_RECOVERY
    P5D3F_RECOVERY_PRESTATE_AUTHORIZED=PASS
    P5D3F_PERSISTENT_FAILURE_ORIGINAL=PersistentHandoffBlockedError: BLOCKED_REMOTE_HEAD_RACE
    P5D3F_PERSISTENT_FAILURE_TEMP_ROOT=C:\Users\Boulevart\AppData\Local\Temp\ATDS-P5D3F-PERSISTENT-HANDOFF-pg0epofm
    P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON={"entries":[{"path":"packages","type":"DIRECTORY"}],"exists":true,...,"state":"PRESENT_NONEMPTY"}
    BLOCKED: PersistentHandoffBlockedError: BLOCKED_REMOTE_HEAD_RACE
    EXIT_CODE=2

## Adjudication

    REAL EXECUTION = BLOCKED
    READY_UNAUTHORIZED HANDOFF = NOT ESTABLISHED
    RESULT_JSON = NOT EMITTED
    REAL_VAULT_ZERO_MUTATION PASS = NOT EMITTED
    AUTHORIZATION = CONSUMED
    SILENT RETRY = FORBIDDEN

The failure-preservation correction worked as intended:

- the body exception remained primary;
- the temporary root was preserved and surfaced;
- the persistent residual was surfaced;
- no cleanup exception replaced BLOCKED_REMOTE_HEAD_RACE.

## Persistent residual

Observed staging remains:

    staging/
      packages/

with no child entry reported in the runner residual snapshot.

This is consistent with the exact recovery prestate remaining materially unchanged.

## Remote state after incident

VERIFIED GITHUB after the attempt:

    integration/system-v1 current HEAD = e47563d523369a988d0a97822e5d8aa6e4ec4371

This post-incident HEAD alone does not identify which remote-race checkpoint fired.

The recovery implementation can emit BLOCKED_REMOTE_HEAD_RACE at multiple bounded checkpoints.

Because a temporary root exists, the exception necessarily occurred after the initial _fresh_remote_identity call returned successfully. Therefore the two race checks inside that initial identity function are excluded for this specific attempt.

The remaining possibilities are:

- temporary candidate fetch no longer matched the initially frozen head; or
- temporary candidate preparation completed, then the final pre-handoff remote recheck detected movement.

## Required next action

READ-ONLY incident discrimination only.

Recover from the preserved temporary root:

- control-repository FETCH_HEAD;
- temporary candidate FETCH_HEAD;
- temporary candidate HEAD if available;
- temporary candidate TREE if available;
- current remote integration/system-v1 head.

Do not delete the temporary root.
Do not mutate staging.
Do not retry real execution.

A later retry requires a new human one-shot authorization after the race is understood and the persistent prestate is reverified.
