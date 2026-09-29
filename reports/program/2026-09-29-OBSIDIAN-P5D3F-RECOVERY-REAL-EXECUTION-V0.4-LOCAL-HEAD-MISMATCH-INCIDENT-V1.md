# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION V0.4 LOCAL HEAD MISMATCH INCIDENT V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL REAL-EXECUTION ATTEMPT plus VERIFIED GITHUB post-attempt state.

## Authorized execution identity

Authorized V0.4 runner HEAD:

    1d725a35490fbf0c137072152d2876c53d63f183

Authorized V0.4 runner blob:

    0dfb31d86c84739fc66ee7efb6ca82e97396d87b

Authorized monitored integration/system-v1 HEAD:

    59f1dc26973b0b50efefccf12b26784d1e41f546

## User-reported governed output

    === P5-D3F PERSISTENT PRODUCTION HANDOFF REAL EXECUTION ===
    AUTHORITY=ONE_FINITE_READY_UNAUTHORIZED_HANDOFF_ONLY
    REAL_VAULT_WRITE_AUTHORIZED=FALSE
    LIVE_PUBLICATION_AUTHORIZED=FALSE
    STAGE_A_AUTHORIZED=FALSE
    STAGE_B_AUTHORIZED=FALSE
    BLOCKED: RealExecutionRunnerError: local HEAD is not the authorized runner HEAD
    EXIT_CODE=2

## Control-flow adjudication

The V0.4 runner checks the local repository HEAD inside _verify_exact_runtime before:

- fetching the governed runner branch;
- validating persistent staging paths;
- validating staging prestate;
- fingerprinting the real Vault;
- invoking execute_persistent_production_handoff.

Therefore this attempt failed before any persistent staging or real-Vault access by the runner.

No READY_UNAUTHORIZED handoff was attempted.
No package materialization was attempted.
No real-Vault mutation path was reached.

## Governance adjudication

    REAL EXECUTION = BLOCKED
    CAUSE = LOCAL RUNNER HEAD MISMATCH
    AUTHORIZATION = CONSUMED
    SILENT RETRY = FORBIDDEN

The one-shot authorization is treated as consumed because the governed V0.4 entrypoint was invoked.

A later attempt requires a fresh explicit human one-shot authorization.

## Independently verified GitHub state after attempt

V0.4 runner branch HEAD remains:

    1d725a35490fbf0c137072152d2876c53d63f183

Runner blob remains:

    0dfb31d86c84739fc66ee7efb6ca82e97396d87b

integration/system-v1 remains:

    59f1dc26973b0b50efefccf12b26784d1e41f546

The remote monitored head therefore still matches the previously authorized SHA.

## Next exact action

READ-ONLY local identity confirmation only:

    git rev-parse HEAD
    git status --porcelain --untracked-files=all

Do not rerun the V0.4 real runner under the consumed authorization.

If the local HEAD is the earlier functional qualification candidate, the cause is operational: the pre-execution switch to the authorization-bearing HEAD was skipped.

A later retry must:

1. switch to the exact then-current authorization-bearing V0.4 HEAD before invocation;
2. re-verify clean worktree;
3. re-verify monitored head and staging prestate;
4. receive a fresh human one-shot authorization;
5. execute once;
6. mandatory STOP.
