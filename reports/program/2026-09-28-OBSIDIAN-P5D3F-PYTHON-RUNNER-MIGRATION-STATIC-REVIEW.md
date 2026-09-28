# OBSIDIAN P5-D3F — PYTHON RUNNER MIGRATION STATIC REVIEW

Date: 2026-09-28

## Evidence status

Same-assistant static review.

This is not local execution evidence and does not qualify P5-D3F.

## Motivation

A local PowerShell invocation produced user-profile traversal warnings involving AppData and other unrelated directories.

The issue is treated as an execution-interface problem, not as a P5-D3F contract failure.

The prior large PowerShell runner was therefore retired before qualification.

## New preferred execution surface

    VS Code
        +
    integrated terminal
        +
    repository-native Python runner

Authoritative runner:

    tools/obsidian_projection/p5d3f_contract_rebreak.py

Runner blob:

    b2d17f51705e4c806ef15160edb66501ef0827e1

Runner tests:

    tests/obsidian_projection/test_p5d3f_contract_rebreak_runner.py

Runner-test blob:

    b309c3efb759ac3c9604b76fc7defa9cbe446482

Execution-method documentation:

    docs/OBSIDIAN-LOCAL-EXECUTION-METHOD-V0.1.md

Blob:

    e86c2315ce0ef5f0373fa0495bdb5c5e3800fdee

## Contract identities unchanged

P5-D3F contract blob:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract-test blob:

    6c7f3d5e1962132f4b609b637d176e67ccd376d5

The runner migration does not change the P5-D3F contract semantics.

## New functional runner candidate

Exact functional runner candidate:

    f4d8258a59af52c67b3ddb66c5c1bfc502060e83

The later documentation commit:

    b933832e70aa6488d036dd0f62964d44c2aa7b9c

does not change runner behavior.

## Static runner properties

The Python runner:

- derives repository root from Path(__file__).resolve().parents[2];
- does not trust the terminal current working directory;
- invokes Git through subprocess argument arrays;
- supplies cwd=<derived repository root> for Git;
- does not use shell=True;
- verifies canonical GitHub repository identity;
- requires a clean worktree before the governed run;
- fetches only the P5-D3F contract branch for the remote race guard;
- verifies exact FETCH_HEAD against a caller-supplied expected remote HEAD;
- checks out an exact caller-supplied functional candidate;
- verifies exact contract and contract-test blob identities;
- places Python bytecode cache outside the repository;
- runs py_compile;
- runs targeted contract and runner tests;
- runs the full tests/obsidian_projection regression;
- requires the final worktree to remain clean;
- emits stable PASS/BLOCKED markers.

## Explicit protection against the observed warning class

The runner-test surface includes:

    test_repo_root_is_derived_from_runner_not_cwd

This test changes process cwd to an unrelated temporary directory and requires the runner to continue resolving the repository root from its own source path.

Therefore the new execution design explicitly rejects the previous assumption:

    current terminal directory == repository root

## PowerShell status

The unqualified file:

    tools/obsidian_projection/run_p5d3f_contract_rebreak.ps1

was deleted from the branch.

No qualified predecessor depends on it.

PowerShell remains available for narrowly Windows-specific experiments when required, but it is no longer the default container for governance logic.

## Evidence taxonomy unchanged

A successful future run remains:

    USER-REPORTED LOCAL EXECUTION

The migration to Python does not turn it into independent assistant execution.

## Publication boundary unchanged

Still unauthorized:

    P5-D3F handoff runtime
    sacrificial handoff execution
    production handoff execution
    CURRENT creation
    CURRENT mutation
    real Vault writes
    P5-C2 pointer invocation
    P5-C3R2 CURRENT writer invocation
    P5-D2 PROMOTION_CONFIRMED
    production promotion
    automatic promotion
    background observer
    polling
    Windows startup/task/service persistence
    Graph/Search CURRENT semantics

## Verdict

**STATIC REVIEW PASS — PYTHON RUNNER LOCAL RE-BREAK REQUIRED**

The next local gate should be executed through the Python runner from a VS Code workspace opened on the actual ATDS repository.

No large PowerShell qualification block is required.
