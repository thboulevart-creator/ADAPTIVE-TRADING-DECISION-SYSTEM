# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION V0.4 HUMAN ONE-SHOT AUTHORIZATION V1

Date: 2026-09-29

## Evidence status

USER EXPLICIT AUTHORIZATION RECEIVED IN CHAT.

This artifact records the human authorization boundary.
It does not itself execute the real handoff.

## Exact authorization literal

    AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF

## Qualified runner authority

Qualified V0.4 runner HEAD before authorization record:

    9e4f2eb1e1c22ce2d32391607c272a5a581e1f81

Runner path:

    tools/obsidian_projection/p5d3f_recovery_real_execution_v0_4.py

Runner blob:

    0dfb31d86c84739fc66ee7efb6ca82e97396d87b

## Authorized monitored source head

Exactly:

    integration/system-v1
    59f1dc26973b0b50efefccf12b26784d1e41f546

The V0.4 runner must fail closed before any persistent handoff call if the remote head differs from this exact SHA.

## Authorized persistent prestate

Exactly:

    PRESENT_EMPTY_PACKAGES_RECOVERY

Meaning:

    staging/
      packages/    [empty]

with no other top-level staging entry and no retained PROMOTION-HANDOFF.json.

## Authorized scope

Exactly one governed V0.4 recovery real execution is authorized for:

- exact V0.4 runner identity;
- exact runner blob above;
- exact monitored integration/system-v1 head above;
- exact PRESENT_EMPTY_PACKAGES_RECOVERY staging prestate;
- one READY_UNAUTHORIZED persistent handoff materialization;
- read-only real-Vault fingerprint before and after;
- REAL_VAULT_ZERO_MUTATION proof;
- preservation of original body exception and surviving temp root on failure;
- mandatory STOP after PASS or BLOCKED outcome.

## Explicitly not authorized

- any write in the real Vault;
- CURRENT or CURRENT.tmp creation or mutation;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage A;
- Stage B;
- automatic/background publication;
- P5-D4;
- P6.

## Consumption semantics

This authorization is one-shot.

Any governed invocation that reaches the V0.4 real-execution entrypoint consumes this authorization for governance purposes, regardless of PASS or BLOCKED outcome.

No silent retry is authorized.

A PASS requires mandatory STOP.
A BLOCKED/FAIL outcome requires residual audit before any later authorization.
