# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION TARGET V8

Date: 2026-09-28

## Evidence status

Static target only. No governed V8 local execution has been performed by this assistant.

## Exact functional candidate

    6b45681bf060d6571782b83593a347ca6acd7a30

## Exact functional blobs

Runner:

    ec4ad41f26334e1350106c79650c6d381a7cfcdc

Runner tests:

    2adf0d72f3d4d7d007ee3ed3ee6ccb184431b2d2

P5-D3F contract unchanged:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract tests unchanged:

    3dc1d7315874d4352eeaf05407f266961c878e70

.gitattributes unchanged:

    e0154899b5640da025a082ef6b02f4bf179d3030

## Triggering evidence

USER-REPORTED local V7 execution passed all P5-D3F-specific gates through P5D3F_CONTRACT_TARGETED=PASS, then the full historical suite blocked.

A bounded local byte diagnostic established seven additional historical P2/P3 pinned dependency paths with:

    RAW=MISMATCH
    FILTER=PASS
    i/lf
    w/crlf

while Git status remained logically clean.

## V8 bounded correction

V8 adds exactly these seven already-pinned historical dependencies to BYTE_PIN_COMPATIBILITY_PATHS:

    tools/obsidian_projection/materialization_contract_v0_1.json
    tools/obsidian_projection/materialize.py
    tools/obsidian_projection/rendering.py
    tools/obsidian_projection/relations.py
    tools/obsidian_projection/integrity.py
    tools/obsidian_projection/builder.py
    tools/obsidian_projection/p2_verify.py

The existing exact committed-blob materialization, raw-blob equality, individually path-scoped index stat refresh, staged representation invariance, and final clean-worktree gates remain unchanged.

## Test-first protection

Before implementation, a runner test was persisted requiring these seven paths to be present in the compatibility surface.

## Authority boundary

No historical expected blob was repinned.
No historical test was weakened.
No P5-D3F contract semantic changed.
No real Vault write is authorized.
No P5-D3G authority is granted.

## Qualification gate

The existing governed local runner must pass its targeted controls and the complete historical Obsidian suite unchanged before P5-D3F can qualify.
