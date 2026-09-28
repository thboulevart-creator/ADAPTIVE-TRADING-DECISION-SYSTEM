# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION REPORT V9

Date: 2026-09-28

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the frozen governed V9 re-break.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Branch:

    feat/obsidian-projection-p5d3f-promotion-handoff-contract-v0.1

Remote HEAD:

    e562ca19ab07e8a02ad071a5961165fd5ac7b53e

V9 functional candidate:

    3e14ac9a8407814de20843a19085c419e8d0e37b

V9 runner blob:

    ea94592b4c168313cb4c398a7d37b32a7c1f7b7d

V9 runner-tests blob:

    c6c7f3d82868315af77c7af09deb5d78b4204285

Frozen P5-D3F contract blob:

    64744325251db350d26c0269090ce62d5fa5f2e8

Frozen contract-test blob:

    3dc1d7315874d4352eeaf05407f266961c878e70

.gitattributes blob:

    e0154899b5640da025a082ef6b02f4bf179d3030

## Local governed re-break result

User-reported filtered output:

    Ran 32 tests in 1.805s
    OK

    Ran 1090 tests in 22.598s
    OK

    P5D3F_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_CONTRACT_REBREAK_COMPLETED=PASS

No FAIL, ERROR, or BLOCKED marker was reported in the completed V9 run.

## Adjudication

The frozen P5-D3F promotion-handoff contract and its unchanged historical suite have passed the governed V9 qualification gate.

    P5-D3F CONTRACT QUALIFICATION = PASS

This qualification closes the contract-definition gate only.

It does not itself implement or execute the finite promotion handoff.

## Authority boundary after qualification

Still NOT authorized by this report:

- production handoff execution;
- real Vault write;
- CURRENT or CURRENT.tmp creation/mutation;
- P5-C2 promotion primitive invocation;
- P5-C3R2 CURRENT writer invocation;
- P5-D2 PROMOTION_CONFIRMED emission;
- automatic promotion;
- background observer or polling;
- P5-D3G live publication transaction;
- P5-D4 bounded observer loop.

## Next governed frontier

Per the frozen contract:

    P5-D3F IMPLEMENTATION
    —
    FINITE_PROMOTION_HANDOFF_IMPLEMENTATION
    + SACRIFICIAL_STAGING_QUALIFICATION

The implementation must remain outside the real Vault and must preserve the contract's READY_UNAUTHORIZED semantics.

No P5-D3G authority is granted by this qualification.
