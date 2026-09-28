# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION TARGET V9

Date: 2026-09-28

## Evidence status

Static target only. No governed V9 local execution has been performed by this assistant.

## Exact functional candidate

    3e14ac9a8407814de20843a19085c419e8d0e37b

## Exact functional blobs

Runner:

    ea94592b4c168313cb4c398a7d37b32a7c1f7b7d

Runner tests:

    c6c7f3d82868315af77c7af09deb5d78b4204285

P5-D3F contract unchanged:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract tests unchanged:

    3dc1d7315874d4352eeaf05407f266961c878e70

.gitattributes unchanged:

    e0154899b5640da025a082ef6b02f4bf179d3030

Dynamic inventory contract authoritative blob:

    80729156f4ac51b760c4347f581f052a175b88b3

## Triggering evidence

USER-REPORTED local V8 execution reduced the full historical suite to two failures, both reporting:

    TOOLING_CONTRACT_MISMATCH

A direct local byte diagnostic then established for dynamic_inventory_contract_v0_1.json:

    HEAD=80729156...
    RAW=4e4d4ed8...
    FILTER=80729156...
    i/lf
    w/crlf

Static inspection confirmed dynamic_inventory.py reads this contract as raw bytes, computes its Git blob OID, and maps a mismatch into the P5-B contract blob mismatch family consumed by finite_candidate_evaluator.py as TOOLING_CONTRACT_MISMATCH.

## V9 bounded correction

V9 adds exactly:

    tools/obsidian_projection/dynamic_inventory_contract_v0_1.json

to the existing BYTE_PIN_COMPATIBILITY_PATHS set.

All existing exact committed-byte materialization, raw identity verification, individually path-scoped stat reconciliation, staged representation invariance, clean-worktree gates, targeted tests, and full historical suite remain unchanged.

## Authority boundary

No historical expected blob was repinned.
No historical test was weakened.
No P5-D3F contract semantic changed.
No real Vault write is authorized.
No P5-D3G authority is granted.

## Qualification gate

The governed local runner must pass the complete historical Obsidian suite unchanged and emit its final completion marker before P5-D3F can qualify.
