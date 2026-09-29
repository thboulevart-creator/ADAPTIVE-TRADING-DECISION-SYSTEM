# OBSIDIAN P5-D3F — PERSISTENT HANDOFF RECOVERY CONTRACT V0.2 QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed recovery-contract re-break.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    8f681db866151227605ca80fd8c0cd72263c250e

Recovery contract blob:

    aef627936b6f745017bcace7e8a3e44270f95674

Frozen recovery-contract tests blob:

    38c6b5253750ef15e2b6fb3255e748808404b0b4

Governed recovery-contract re-break runner blob:

    829ede27fa14ec6ea0846d53096c8d4a89e2aed7

## User-reported governed result

Targeted recovery-contract tests:

    Ran 10 tests in 0.008s
    OK

Complete historical Obsidian suite:

    Ran 1229 tests in 201.993s
    OK

Terminal markers:

    P5D3F_RECOVERY_CONTRACT_TARGETED=PASS
    P5D3F_RECOVERY_CONTRACT_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_RECOVERY_CONTRACT_REBREAK_COMPLETED=PASS

No FAIL, ERROR, or BLOCKED marker was reported.

## Adjudication

    P5-D3F PERSISTENT HANDOFF RECOVERY CONTRACT V0.2 = QUALIFIED

The contract qualifies only the narrow recovery state already observed:

    staging/
      packages/    [empty]

with no PROMOTION-HANDOFF.json and no other staging entry.

It also freezes failure-preservation semantics:

- body failures may not be masked by temporary cleanup;
- body failures preserve temporary evidence;
- original body exception remains primary;
- cleanup failure after otherwise successful handoff is distinct;
- successful handoff evidence must survive cleanup failure.

## Next exact frontier

    P5-D3F-PERSISTENT-HANDOFF-RECOVERY-IMPLEMENTATION-V0.3

Still NOT authorized:

- any real execution retry;
- real Vault write;
- CURRENT / CURRENT.tmp mutation;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage A;
- Stage B;
- P5-D4;
- P6.
