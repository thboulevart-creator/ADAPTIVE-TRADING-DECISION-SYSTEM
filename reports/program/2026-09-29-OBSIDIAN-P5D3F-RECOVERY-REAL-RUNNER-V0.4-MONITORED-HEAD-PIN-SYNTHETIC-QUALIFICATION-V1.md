# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION RUNNER V0.4 MONITORED-HEAD PIN — SYNTHETIC QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed V0.4 synthetic re-break.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    5c3a6287352ec934346b5aa10311ad16d1bf9127

Exact functional candidate:

    d2445091ad1a0d646cbf016e52f5c9a19057e89b

V0.4 runner:

    tools/obsidian_projection/p5d3f_recovery_real_execution_v0_4.py

Runner blob:

    0dfb31d86c84739fc66ee7efb6ca82e97396d87b

Frozen V0.4 tests blob:

    667e458962aca47a1d3f08ef3f12c80015c1390b

Governed V0.4 re-break blob:

    e6c9ab7f98c9fa8f77db3dc98571120e6cbeb7c0

## User-reported governed result

Targeted V0.4 tests:

    Ran 11 tests in 0.009s
    OK

Complete historical Obsidian suite:

    Ran 1263 tests in 200.440s
    OK

Terminal markers:

    P5D3F_RECOVERY_REAL_RUNNER_TARGETED=PASS
    P5D3F_RECOVERY_REAL_RUNNER_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_RECOVERY_REAL_RUNNER_REBREAK_COMPLETED=PASS

No FAIL, ERROR, or BLOCKED marker was reported.

## Adjudication

    P5-D3F RECOVERY REAL EXECUTION RUNNER V0.4 — SYNTHETIC QUALIFICATION = PASS

## Qualified authority semantics

The V0.4 runner requires all of the following before a real handoff attempt:

- exact qualified runner HEAD/blob identity;
- exact PRESENT_EMPTY_PACKAGES_RECOVERY staging prestate;
- explicit --expected-monitored-head authority pin;
- exact equality between refs/heads/integration/system-v1 and the human-authorized monitored HEAD before any persistent handoff call;
- independent remote-race guards inside the qualified persistent implementation;
- successful result candidate_head exactly equal to the authorized monitored HEAD;
- REAL_VAULT_ZERO_MUTATION proof;
- mandatory STOP.

If the monitored branch does not equal the authorized SHA, the runner fails closed with:

    BLOCKED_MONITORED_HEAD_AUTHORITY_MISMATCH

## User-reported prestate immediately before synthetic qualification

    P5D3F_RECOVERY_PRESTATE=PRESENT_EMPTY_PACKAGES_RECOVERY

The synthetic qualification itself is defined to perform no real staging or real Vault access.

## Current integration branch observation

At qualification persistence time:

    integration/system-v1 = 59f1dc26973b0b50efefccf12b26784d1e41f546

This is an observation only, not yet a human-authorized monitored HEAD.

## Next exact gate

Before a V0.4 real execution can be authorized:

1. obtain a fresh bounded REMOTE_QUIET_WINDOW=PASS for integration/system-v1;
2. re-verify the staging prestate remains PRESENT_EMPTY_PACKAGES_RECOVERY if there is any doubt or intervening mutation;
3. record a fresh human one-shot authorization bound to:
   - V0.4 qualified runner;
   - exact then-stable monitored HEAD;
   - PRESENT_EMPTY_PACKAGES_RECOVERY;
4. perform at most one real attempt;
5. mandatory STOP.

Real execution is not authorized by this qualification report.
Real Vault write remains closed.
Live publication remains closed.
Stage A and Stage B remain closed.
