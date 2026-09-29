# OBSIDIAN P5-D3F — REAL EXECUTION FAILURE-PRESERVATION V0.2 STATIC REVIEW

Date: 2026-09-29

## Evidence status

SAME-ASSISTANT STATIC REVIEW ONLY.

This is not execution evidence and does not qualify the corrected runner.

## Exact candidate reviewed

    d8639fdbaf773f5efbce91b7923723b20cf840d3

Corrected runner blob:

    1b44e12a6c23715ea3d5055c9263f4bccb67fe39

Frozen runner tests blob:

    64033e4b2fe652a936b690293557bcd0eeac2c4f

Governed synthetic re-break blob:

    c8a5e4f52001be17673cb8ecefb4c4871066f6e0

## Static findings

PASS — the runner is bound to the v0.2 correction branch.

PASS — the original execution exception is preserved and re-raised.

PASS — the runner emits the original exception type/message.

PASS — the runner emits a read-only persistent-staging residual snapshot.

PASS — the failure path contains no staging.rmdir(), packages.rmdir(), unlink, or equivalent persistent cleanup deletion.

PASS — nonempty residual evidence is preserved for audit.

PASS — the corrected runner does not add live-publication authority.

PASS — no Stage-B execution action is present.

PASS — qualified persistent-handoff implementation, tests, contract and P5-D3F runtime authority pins remain unchanged.

## Targeted adversarial surface

    10 tests

The added/changed tests specifically freeze:

- PRESENT_EMPTY residual preservation;
- nonempty residual evidence preservation;
- absent staging snapshot without creation;
- no cleanup deletion in the failure path;
- exact corrected runner-branch binding.

## Current adjudication

    STATIC REVIEW = PASS
    SYNTHETIC QUALIFICATION = PENDING
    REAL EXECUTION RETRY = NOT AUTHORIZED
    PRIOR ONE-SHOT AUTHORIZATION = CONSUMED
    NEW ONE-SHOT AUTHORIZATION = REQUIRED AFTER QUALIFICATION

Real Vault write remains closed.
Live publication remains closed.
Stage A remains closed.
Stage B remains closed.
