# OBSIDIAN P5-D3F — PERSISTENT HANDOFF RECOVERY CONTRACT V0.2 QUALIFICATION TARGET

Date: 2026-09-29

## Evidence status

Contract qualification target only.

No persistent staging mutation.
No real Vault access.
No real execution.

## Exact candidate

    29c78d80cdfd7c0e9e5acac344d96d5095885c78

Contract:

    tools/obsidian_projection/persistent_production_handoff_gate_contract_v0_2.json

Contract blob:

    aef627936b6f745017bcace7e8a3e44270f95674

Frozen tests:

    tests/obsidian_projection/test_p5d3f_persistent_handoff_recovery_contract_v0_2.py

Tests blob:

    38c6b5253750ef15e2b6fb3255e748808404b0b4

Governed re-break runner:

    tools/obsidian_projection/p5d3f_persistent_handoff_recovery_contract_rebreak_v0_2.py

Runner blob:

    829ede27fa14ec6ea0846d53096c8d4a89e2aed7

Targeted tests:

    10

## Amendment scope

V0.2 is a narrow recovery amendment over V0.1.

It permits only the exact previously-observed residual:

    staging/
      packages/   [empty]

with no PROMOTION-HANDOFF.json and no other staging entry.

It does not authorize arbitrary nonempty staging.

It also requires future implementation semantics where:

- body failure cannot be masked by temporary cleanup;
- body failure preserves temporary evidence;
- post-success temporary cleanup failure is distinct;
- handoff evidence is preserved if post-success cleanup blocks.

## Boundary

Contract tests only.

Persistent handoff execution remains unauthorized.
Real Vault read/write remains unauthorized.
Live publication remains unauthorized.
Stage A and Stage B remain unauthorized.

## Next gate after PASS

    P5-D3F-PERSISTENT-HANDOFF-RECOVERY-IMPLEMENTATION-V0.3
