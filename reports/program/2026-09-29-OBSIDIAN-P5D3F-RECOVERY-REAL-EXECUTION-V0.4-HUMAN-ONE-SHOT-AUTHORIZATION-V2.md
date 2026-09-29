# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION V0.4 HUMAN ONE-SHOT AUTHORIZATION V2

Date: 2026-09-29

## Evidence status

USER EXPLICIT AUTHORIZATION RECEIVED IN CHAT.

This record is persisted on the audit branch so the authorized runner branch itself remains frozen at the exact human-authorized runner HEAD.

## Exact authorization literal

    AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF

## Authorized runner identity

Runner branch:

    feat/obsidian-projection-p5d3f-recovery-real-execution-runner-v0.4-monitored-head-pin

Exact authorized runner HEAD:

    1d725a35490fbf0c137072152d2876c53d63f183

Exact authorized runner blob:

    0dfb31d86c84739fc66ee7efb6ca82e97396d87b

Runner path:

    tools/obsidian_projection/p5d3f_recovery_real_execution_v0_4.py

## Authorized monitored source head

Exactly:

    integration/system-v1
    59f1dc26973b0b50efefccf12b26784d1e41f546

## Authorized staging prestate

Exactly:

    PRESENT_EMPTY_PACKAGES_RECOVERY

Meaning:

    staging/
      packages/    [empty]

with no other top-level entry.

## Authorized scope

Exactly one governed V0.4 real execution is authorized for:

- exact runner HEAD above;
- exact runner blob above;
- exact monitored integration/system-v1 HEAD above;
- exact PRESENT_EMPTY_PACKAGES_RECOVERY staging prestate;
- one READY_UNAUTHORIZED persistent handoff materialization;
- read-only real-Vault fingerprint before and after;
- REAL_VAULT_ZERO_MUTATION proof;
- preservation of the original error and temp root on failure;
- mandatory STOP after PASS or BLOCKED outcome.

## Explicitly not authorized

- any write in the real Vault;
- CURRENT or CURRENT.tmp creation or mutation;
- live publication;
- PROMOTION_CONFIRMED;
- Stage A;
- Stage B;
- automatic/background publication;
- P5-D4;
- P6.

## Consumption semantics

This authorization is one-shot.

Any governed invocation that reaches the V0.4 real-execution entrypoint consumes it, regardless of PASS or BLOCKED outcome.

No silent retry is authorized.

A PASS requires mandatory STOP.
A BLOCKED/FAIL outcome requires residual audit before any later authorization.
