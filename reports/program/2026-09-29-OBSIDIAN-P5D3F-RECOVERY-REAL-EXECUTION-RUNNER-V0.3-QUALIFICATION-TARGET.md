# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION RUNNER V0.3 QUALIFICATION TARGET

Date: 2026-09-29

## Evidence status

Synthetic qualification target only.

No persistent staging access.
No real Vault access.
No real execution.

## Exact candidate

    365056dec5bb87ccf3f7dc0e7b902e2875f90cf4

Recovery real-execution runner:

    tools/obsidian_projection/p5d3f_persistent_production_handoff_real_execution.py

Runner blob:

    ab9702e0288dedf6c126be35239603d8112e028c

Frozen targeted tests:

    tests/obsidian_projection/test_p5d3f_recovery_real_execution_runner_v0_3.py

Tests blob:

    21d4c1531b020c4abe8e5ecf86e0e21b3c0bc6be

Governed synthetic re-break:

    tools/obsidian_projection/p5d3f_recovery_real_execution_runner_rebreak_v0_3.py

Re-break blob:

    de95629b0f44a4ac555ce12347800e1b9f1b0b90

Qualified recovery implementation blob:

    dcd70a9d9794675eab90e41df560f8b030b5dbf3

Qualified recovery implementation tests blob:

    242305bc0f95bbe243158b5c806255508093a357

Qualified recovery contract V0.2 blob:

    aef627936b6f745017bcace7e8a3e44270f95674

Qualified original persistent gate contract V0.1 blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## Frozen targeted surface

    10 tests

## Runner semantics

The runner:

1. binds the exact V0.3 recovery implementation and V0.2 recovery contract;
2. accepts only staging prestate PRESENT_EMPTY_PACKAGES_RECOVERY;
3. rejects ABSENT, PRESENT_EMPTY and arbitrary nonempty states for this recovery retry;
4. preserves generic body-failure original exception, surviving temp-root path and read-only staging residual snapshot;
5. distinguishes PersistentHandoffPostSuccessCleanupBlockedError from body failure;
6. validates the success result bound to that post-success cleanup exception, including REAL_VAULT_ZERO_MUTATION;
7. emits the successful body result and surviving temp-root path for audit if cleanup alone blocks;
8. emits full PASS only when handoff body and temporary cleanup both complete;
9. preserves READY_UNAUTHORIZED and mandatory STOP semantics;
10. contains no later live-publication or Stage-B authority.

## Qualification sequence

- exact remote-race guard;
- exact candidate HEAD;
- exact runner/test/recovery/runtime blob pins;
- static required/forbidden surface scan;
- Python compilation;
- 10 targeted tests;
- complete historical Obsidian suite;
- final clean-control-clone gate.

## Authority

Synthetic qualification only.

No real retry is authorized.
A new one-shot human authorization is required after PASS.

Real Vault write remains closed.
Live publication remains closed.
Stage A and Stage B remain closed.
