# OBSIDIAN P5-C3R — BOUNDED SHARING-CONFLICT RETRY PREFLIGHT

Date: 2026-09-27

## Scope

P5-C3R is the governed successor to the failed P5-C3 Obsidian-open experiment.

It does not repeat the failed primitive unchanged.

It retains the same immutable-generation + atomic CURRENT.tmp -> CURRENT.md replacement architecture and adds only bounded handling of Windows sharing conflicts.

## Failed predecessor

Persisted P5-C3 failure adjudication:

    65003f36eef5bb8b4759d62735d7bf9f08e90ddb

Observed failure:

    cycle_completed_count = 8
    failure_phase = PROMOTION_LOOP
    PermissionError / WinError 5
    os.replace(CURRENT.tmp, CURRENT.md)

The un-retried Obsidian-open primitive is therefore not qualified.

## Candidate branch

    feat/obsidian-projection-p5c3r-access-denied-retry-v0.1

Candidate HEAD before local re-break:

    dc2db6845c18a073b5ab998d5b3724ace0a9e0fa

## Persisted candidate artifacts

Retry contract:

    tools/obsidian_projection/obsidian_open_retry_contract_v0_1.json
    blob: 82cc7e100017d5e2db671ccce989f5e0e2afe912

Retry implementation:

    tools/obsidian_projection/obsidian_open_retry.py
    blob: 3550af5610dd25c0233dd84cb2b0d5af269a2a7f

CLI:

    tools/obsidian_projection/p5c3r_verify.py
    blob: d49a3c6bcc36f1b2b851e9c2199d18f3f924afca

Contract breakers:

    tests/obsidian_projection/test_obsidian_open_retry_contract_v0_1.py
    blob: 3ae3f39377bd3e41b3cae00ad27ea5f2df979aa8

Unit tests:

    tests/obsidian_projection/test_obsidian_open_retry.py
    blob: 0f66284723f24f4cccd1f6a8fc4338b02d0e93d3

Adversarial breakers:

    tests/obsidian_projection/test_p5c3r_adversarial.py
    blob: 3f035d00ade606519c6f781d385bde6b0177820c

Recovery/control runner:

    tools/obsidian_projection/run_p5c3r_recover_control.ps1
    blob: 8dbd82367744b6fe454b57b6985cddde6d0cc74e

Open experiment runner:

    tools/obsidian_projection/run_p5c3r_open.ps1
    blob: ea6dc7d45d98df9507db4015d4e15b76fbc1fd52

Post-close runner:

    tools/obsidian_projection/run_p5c3r_post_close.ps1
    blob: 1409ed062e7a1546ad0d7afa42168d8c47312840

Protocol documentation:

    docs/OBSIDIAN-P5C3R-BOUNDED-SHARING-CONFLICT-RETRY-V0.1.md
    blob: d434fc577a40779b7b854a4d5dbeb5e3b06eba15

Failed P5-C3 evidence:

    reports/program/2026-09-27-OBSIDIAN-P5C3-RUN-OPEN-FAILURE.md
    blob: db73158cbf88c3932007d69815e94e6c14e15437

## Base P5-C3 implementation preservation

The failed P5-C3 harness remains byte-identical:

    tools/obsidian_projection/obsidian_open_compatibility.py
    expected blob:
    b970e65f21792cccc6ee2e4271d630f371102ff7

P5-C3R is implemented in a separate module.

## Retryable conflicts

Only Windows sharing-conflict PermissionErrors are retryable:

    WinError 5
    WinError 32

All other errors remain terminal.

## Write retry bounds

    operation = os.replace(CURRENT.tmp, CURRENT.md)
    deadline = 5000 ms
    initial backoff = 10 ms
    maximum backoff = 500 ms

CURRENT.tmp is written once.

It must retain exact candidate bytes after every failed replace attempt.

CURRENT.md must remain the previous valid generation until replacement succeeds.

## Read retry bounds

Only an underlying PermissionError / WinError 5 or 32 may be retried.

    deadline = 500 ms
    initial backoff = 5 ms
    maximum backoff = 50 ms

Transient access denial is measured separately from semantic corruption.

Terminal reader access error remains forbidden.

## Recovery boundary

Before P5-C3R testing:

- Obsidian must be fully closed;
- the existing sandbox is reused;
- generation rebuild is forbidden;
- CURRENT must be GEN_A;
- immutable-generation and live-Vault digests must match the bound snapshot;
- any surviving CURRENT.tmp may be removed only if its bytes exactly equal the expected failed GEN_B candidate.

## Synthetic Windows lock breaker

Before real Obsidian-open execution, the candidate must pass a real Windows lock test.

The breaker opens CURRENT.md without FILE_SHARE_DELETE for 200 ms.

The candidate must observe at least one retryable sharing conflict and still complete the atomic replacement exactly.

## Real open experiment

After recovery and manual reopen of CURRENT.md:

    250 promotions
    >= 5000 reader samples
    >= 1 fresh reader sample per promotion

Required final state:

    GEN_A

Required terminal anomalies:

    terminal pointer write errors = 0
    retry deadline exceeded = 0
    terminal reader access errors = 0
    mixed generation = 0
    missing entrypoint = 0
    semantic partial generation = 0
    parse errors = 0

Transient sharing-conflict retries may be non-zero and must be reported.

## Manual and post-close gates

Automated PASS alone is insufficient.

Manual visual acceptance while Obsidian remains open is still required.

Then Obsidian must be fully closed and P5-C3R POST-CLOSE must pass.

## Non-authorizations

P5-C3R does not authorize:

- production promotion;
- continuous observer;
- scheduled background task/service;
- Obsidian Sync;
- community plugins;
- human view overwrite.

The Graph/Search CURRENT-generation indexing problem remains deferred to P6.

## Required local sequence

1. exact candidate checkout;
2. close Obsidian fully;
3. targeted P5-C3R tests;
4. full Obsidian suite;
5. control clone clean;
6. synthetic Windows sharing-lock breaker PASS;
7. recovery of failed P5-C3 state PASS;
8. manually reopen sacrificial Vault and CURRENT.md;
9. visual pre-run confirmation;
10. P5-C3R RUN-OPEN;
11. visual final acceptance;
12. close Obsidian;
13. P5-C3R POST-CLOSE.

## Current verdict

**P5-C3R CANDIDATE PERSISTED — LOCAL RE-BREAK + SYNTHETIC LOCK BREAKER + RECOVERY REQUIRED**
