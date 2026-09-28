# OBSIDIAN — LOCAL EXECUTION METHOD V0.1

Date: 2026-09-28

## Objective

Reduce shell-specific fragility and user copy/paste burden without weakening the existing governed evidence model.

## Default local interface

The preferred local execution environment is:

    VS Code
        +
    integrated terminal
        +
    repository-native Python runners

PowerShell is no longer the preferred place for qualification logic.

It may still be used for:

    opening VS Code
    launching a command
    Windows-only primitives when Python must call Win32 behavior

but governance logic should live in versioned Python code whenever practical.

## Why

Large ad hoc PowerShell blocks create avoidable failure classes:

    wrong current working directory
    shell quoting
    multiline paste damage
    stale variables
    partial execution
    path expansion
    user-profile traversal
    difficult unit testing

Repository-native Python runners are easier to:

    version
    review
    unit test
    pin by Git blob
    execute identically from VS Code
    bind to exact repository paths
    reuse across future gates

## Repository-root rule

A governed Python runner must derive its repository root from its own source file:

    Path(__file__).resolve()

It must not trust:

    current shell directory
    user profile directory
    environment-specific prompt state

All Git subprocesses must receive an explicit:

    cwd=<verified repository root>

This rule prevents a mistaken terminal location from causing Git to traverse unrelated directories such as:

    AppData
    Documents
    user-profile junctions

## Shell independence

Qualification code should use:

    Python standard library
    subprocess with argument arrays
    pathlib

It should avoid:

    shell=True
    shell-specific interpolation
    shell pipelines for evidence-critical logic

## Evidence model unchanged

This interface change does not alter the evidence taxonomy.

Local execution supplied by the user remains:

    USER-REPORTED LOCAL EXECUTION

GitHub repository identities verified by connector remain:

    VERIFIED IN GITHUB

A Python runner does not become independent execution merely because its implementation is versioned.

## Governed-run expectations

Each runner should, where relevant:

    verify canonical repository identity
    verify clean worktree before execution
    perform a remote race guard when network resolution is authorized
    checkout or verify the exact functional candidate
    verify contract/runtime/test blob identities
    use an external pycache
    execute targeted tests first
    execute the full relevant regression suite
    verify final worktree cleanliness
    emit stable machine-readable PASS/BLOCKED markers

## VS Code role

VS Code is an execution surface, not an authority source.

The authority remains:

    persisted Git contract
    exact commit/blob identities
    governed local runner
    observed runtime evidence

No VS Code extension, workspace setting or local editor state may silently expand runtime authority.

## Windows-specific behavior

When a qualification specifically concerns Windows behavior such as:

    sharing violations
    Win32 file handles
    OneDrive interaction
    Obsidian-open behavior
    atomic pointer replacement

Python may call the required Windows APIs directly or invoke narrowly scoped OS commands.

The architecture remains versioned and testable in Python.

## User interaction target

The intended future interaction is:

    user says:
    "prochaine action logique"

    assistant:
    performs all GitHub/static work to the next true local gate

    user locally runs:
    one short versioned command

    user returns:
    output

The user should not need to paste hundreds of lines of transient shell logic.

## Current P5-D3F application

P5-D3F contract re-break now uses:

    tools/obsidian_projection/p5d3f_contract_rebreak.py

Its tests explicitly verify that repository-root discovery remains stable even when the process current working directory changes.

The previous PowerShell contract runner was retired before qualification.

## Non-authorizations

This execution-method document grants no additional project authority.

It does not authorize:

    publication
    CURRENT mutation
    real Vault writes
    background execution
    polling
    startup persistence
    Graph/Search CURRENT semantics
