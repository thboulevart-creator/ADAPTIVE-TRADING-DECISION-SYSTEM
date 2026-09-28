# OBSIDIAN P5-D3F — V9 DYNAMIC INVENTORY CONTRACT BYTE-PIN STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static review. Not independent execution evidence. Does not qualify P5-D3F.

## Exact V9 functional candidate

    3e14ac9a8407814de20843a19085c419e8d0e37b

Runner:

    ea94592b4c168313cb4c398a7d37b32a7c1f7b7d

Runner tests:

    c6c7f3d82868315af77c7af09deb5d78b4204285

Dynamic inventory contract authoritative blob:

    80729156f4ac51b760c4347f581f052a175b88b3

## Static finding

The two remaining V8 failures shared exactly:

    TOOLING_CONTRACT_MISMATCH

The direct local diagnostic established that dynamic_inventory_contract_v0_1.json had CRLF raw worktree bytes while its filtered identity and committed Git blob matched the historical authority.

dynamic_inventory.py performs an exact raw-byte Git blob verification of that contract before inventory construction. A mismatch raises the P5-B contract blob mismatch family that finite_candidate_evaluator.py maps to TOOLING_CONTRACT_MISMATCH.

Therefore this file is directly on the common failing path for both P5-D3D and P5-D3E.

## Test-first sequence

Before the implementation mutation, the historical compatibility breaker was extended to require dynamic_inventory_contract_v0_1.json in BYTE_PIN_COMPATIBILITY_PATHS.

The implementation then added exactly that path.

## Boundary preservation

No expected pin changed.
No historical test changed.
No contract semantic changed.
No existing compatibility path was removed.
No new mechanism was introduced.
No real Vault operation was introduced.

## Remaining uncertainty

V9 has not yet been executed locally.

The full historical suite remains the authority for whether this closes both remaining synthetic failures or exposes another independent issue.

## Verdict

    STATIC CORRECTION REVIEW = PASS
    V9 FUNCTIONAL CANDIDATE = READY FOR LOCAL GATE
    V9 LOCAL GOVERNED RE-BREAK = NOT EXECUTED
    P5-D3F CONTRACT = UNQUALIFIED
    P5-D3F IMPLEMENTATION = UNAUTHORIZED
    P5-D3G = CLOSED
    REAL VAULT WRITE = CLOSED
