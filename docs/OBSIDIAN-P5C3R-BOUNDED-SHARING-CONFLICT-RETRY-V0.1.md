# OBSIDIAN P5-C3R — BOUNDED WINDOWS SHARING-CONFLICT RETRY V0.1

Date: 2026-09-27

## Purpose

P5-C3R addresses the exact P5-C3 RUN-OPEN failure observed while Obsidian had CURRENT.md open.

Observed failure:

    failure_phase = PROMOTION_LOOP
    failure_cycle = 8
    failure_code = PermissionError
    WinError = 5
    operation = os.replace(CURRENT.tmp, CURRENT.md)

P5-C3R does not replace the publication architecture.

It keeps:

    immutable generations
        +
    CURRENT.tmp
        -> flush
        -> fsync
        -> os.replace(..., CURRENT.md)

The only new behavior is bounded handling of Windows sharing conflicts.

## Failed predecessor

P5-C3 failure adjudication:

    65003f36eef5bb8b4759d62735d7bf9f08e90ddb

The failed un-retried open-Vault primitive is not qualified.

## Retryable Windows conflicts

Only:

    PermissionError / WinError 5
    PermissionError / WinError 32

may be retried.

These correspond to the access-denied / sharing-conflict family relevant to the observed Windows file-replacement boundary.

All other errors fail immediately.

## Write-side retry policy

Exact operation:

    os.replace(CURRENT.tmp, CURRENT.md)

Bounds:

    deadline = 5000 ms
    initial backoff = 10 ms
    exponential multiplier = 2
    maximum backoff = 500 ms

Rules:

- CURRENT.tmp is written exactly once before the retry loop;
- it is never rewritten between replace attempts;
- after every retryable failure its bytes must still match the exact candidate SHA-256;
- CURRENT.md must still resolve to the previous valid generation;
- deadline exhaustion is terminal;
- successful replacement must yield the exact candidate bytes, generation ID and tree digest;
- CURRENT.tmp must disappear after success.

## Read-side retry policy

A concurrent reader may encounter the same Windows sharing boundary.

Only an underlying PermissionError with WinError 5 or 32 is retryable.

Bounds:

    deadline = 500 ms
    initial backoff = 5 ms
    maximum backoff = 50 ms

A transient sharing denial is tracked separately from semantic corruption.

Still forbidden:

    mixed generation
    missing entrypoint
    semantic partial generation
    parse error
    terminal reader access error

All must remain zero.

## Recovery of failed P5-C3 state

Recovery requires Obsidian fully closed.

The existing P5-C3 sandbox and snapshot are reused.

Generation rebuild is forbidden.

Required starting state:

    CURRENT.md = GEN_A

Because P5-C3 failed attempting cycle 8, a surviving CURRENT.tmp may only be removed if its bytes exactly match the expected GEN_B candidate derived from the bound snapshot.

Any other CURRENT.tmp content blocks recovery.

## Synthetic Windows sharing-lock breaker

Before real Obsidian-open execution, P5-C3R deliberately opens a temporary CURRENT.md with a Windows handle that allows read/write sharing but denies delete/rename sharing.

The lock remains for at least 200 ms.

The candidate must demonstrate:

    > 0 sharing-conflict retries
    eventual atomic replace success
    exact final GEN_B
    no stale CURRENT.tmp

This is required independently of the real Obsidian run.

## Real open-Vault experiment

Requirements remain:

    250 promotions
    >= 5000 reader samples
    >= 1 fresh reader sample per promotion
    initial GEN_A
    final GEN_A

Required terminal outcomes:

    terminal pointer write errors = 0
    retry deadline exceeded = 0
    mixed generation = 0
    missing entrypoint = 0
    semantic partial generation = 0
    parse errors = 0
    terminal reader access errors = 0

Transient WinError 5/32 retry counts may be non-zero and are explicitly measured.

Telemetry includes:

    total replace attempts
    total sharing conflicts
    maximum retry depth
    maximum promotion latency
    reader sharing-conflict retries
    failure phase / cycle / type / message

## Manual visual and post-close gates

An automated retry experiment PASS remains insufficient.

The user must still visually confirm while Obsidian is open:

    CURRENT
    Active generation: GEN_A
    Open active generation -> generations/GEN_A/INDEX

Then Obsidian must be fully closed and POST-CLOSE must pass.

## Non-authorizations

Even P5-C3R PASS does not authorize:

- production promotion;
- continuous observer;
- Windows Task Scheduler/service registration;
- human views overwrite;
- Obsidian Sync;
- community plugins.

The native Graph CURRENT-generation indexing problem remains deferred to P6.
