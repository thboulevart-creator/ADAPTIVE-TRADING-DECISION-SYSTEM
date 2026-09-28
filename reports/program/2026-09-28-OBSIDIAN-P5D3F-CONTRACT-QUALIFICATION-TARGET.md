# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION TARGET

Date: 2026-09-28

## Purpose

Freeze the exact functional candidate that must be used for the first local P5-D3F contract re-break after migration from ad hoc PowerShell to a repository-native Python runner.

## Exact functional candidate

    f4d8258a59af52c67b3ddb66c5c1bfc502060e83

This commit is the first functional qualification target containing all required executable qualification surfaces together:

    P5-D3F contract
    P5-D3F contract tests
    Python governed re-break runner
    runner cwd-independence tests

Later commits are evidence/documentation only unless explicitly stated otherwise.

## Exact blobs at functional candidate

Contract:

    tools/obsidian_projection/promotion_handoff_contract_v0_1.json

Blob:

    64744325251db350d26c0269090ce62d5fa5f2e8

Contract tests:

    tests/obsidian_projection/test_promotion_handoff_contract_v0_1.py

Blob:

    6c7f3d5e1962132f4b609b637d176e67ccd376d5

Python governed runner:

    tools/obsidian_projection/p5d3f_contract_rebreak.py

Blob:

    b2d17f51705e4c806ef15160edb66501ef0827e1

Runner tests:

    tests/obsidian_projection/test_p5d3f_contract_rebreak_runner.py

Blob:

    b309c3efb759ac3c9604b76fc7defa9cbe446482

## Why the older contract candidate is not the local execution target

The earlier contract candidate:

    5e1aede1b2071c7985a0938ef97025f5e6c03cfa

contains the contract semantics, but predates the final Python runner test surface.

Checking out that older commit before targeted runner tests would remove the runner-test module from the worktree.

Therefore it is not the correct complete local qualification target.

The contract blob itself remains unchanged.

## Local qualification requirement

The governed Python runner must:

1. derive the repository root from its own source file;
2. verify the canonical repository;
3. require a clean worktree;
4. fetch the P5-D3F branch and enforce exact remote-head race guard;
5. detach at this exact functional candidate;
6. verify the exact contract and contract-test blobs;
7. py_compile the runner plus both P5-D3F test modules;
8. execute targeted P5-D3F contract + runner tests;
9. execute the full tests/obsidian_projection regression;
10. require a clean worktree after execution.

## Qualification semantics

A local PASS is:

    USER-REPORTED LOCAL EXECUTION

It may qualify the P5-D3F contract and its qualification runner.

It does not independently authorize:

    P5-D3F handoff implementation
    until the PASS is persisted and adjudicated

and it never authorizes:

    production promotion
    CURRENT mutation
    real Vault writes
    P5-D2 PROMOTION_CONFIRMED
    background observer
    polling
    Windows startup persistence
    Graph/Search CURRENT semantics

## Next gate

    LOCAL GOVERNED P5-D3F CONTRACT RE-BREAK

using:

    f4d8258a59af52c67b3ddb66c5c1bfc502060e83
