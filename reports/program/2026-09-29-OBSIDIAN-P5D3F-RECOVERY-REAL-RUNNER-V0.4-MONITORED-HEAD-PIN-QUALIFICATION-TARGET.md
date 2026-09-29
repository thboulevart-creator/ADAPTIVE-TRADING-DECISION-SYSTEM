# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION RUNNER V0.4 MONITORED-HEAD PIN — QUALIFICATION TARGET

Date: 2026-09-29

## Evidence status

Synthetic qualification target only.

No persistent staging access.
No real Vault access.
No real execution.

## Exact functional candidate

    d2445091ad1a0d646cbf016e52f5c9a19057e89b

Versioned V0.4 runner:

    tools/obsidian_projection/p5d3f_recovery_real_execution_v0_4.py

Runner blob:

    0dfb31d86c84739fc66ee7efb6ca82e97396d87b

Frozen V0.4 tests:

    tests/obsidian_projection/test_p5d3f_recovery_real_execution_runner_v0_4.py

Tests blob:

    667e458962aca47a1d3f08ef3f12c80015c1390b

Governed V0.4 re-break:

    tools/obsidian_projection/p5d3f_recovery_real_execution_runner_rebreak_v0_4.py

Re-break blob:

    e6c9ab7f98c9fa8f77db3dc98571120e6cbeb7c0

Qualified recovery implementation blob:

    dcd70a9d9794675eab90e41df560f8b030b5dbf3

Qualified recovery contract V0.2 blob:

    aef627936b6f745017bcace7e8a3e44270f95674

Qualified original P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## V0.4 authority closure

The V0.4 runner adds a mandatory CLI authority binding:

    --expected-monitored-head <40-hex SHA>

Before any persistent handoff call, the runner performs an exact read-only ls-remote check of:

    refs/heads/integration/system-v1

and requires the current remote head to equal the human-authorized SHA.

If it differs, execution fails closed with:

    BLOCKED_MONITORED_HEAD_AUTHORITY_MISMATCH

The successful result is also revalidated so:

    result["candidate_head"] == expected_monitored_head

The same candidate-head binding is revalidated if the handoff body succeeded but temporary cleanup later blocks.

The qualified persistent implementation retains its independent fresh-remote and final pre-handoff race guards, so movement after the V0.4 authority check still fails closed.

## Frozen targeted surface

    11 tests

## Historical preservation

The V0.3 runner and its frozen tests remain unchanged at their versioned paths.

No prior qualification or historical test is rewritten.

## Authorization status

The prior V0.3 human one-shot authorization is NOT authority for V0.4.

It was bound to:

    runner V0.3
    monitored head fda1d9724165192385fed1c22817d9c33334fde8

The monitored branch has subsequently moved, and V0.4 is a new runner identity.

Therefore any future V0.4 real execution requires a fresh one-shot human authorization after synthetic qualification and a fresh quiet-window/prestate check.

## Authority

Synthetic qualification only.

Real execution remains unauthorized.
Real Vault write remains closed.
Live publication remains closed.
Stage A and Stage B remain closed.
