# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION TARGET V2

Date: 2026-09-28

## Exact corrected functional candidate

    a12bc12d6279b1dfc58b507c282578310d7fd2b0

This supersedes the prior local qualification target:

    f4d8258a59af52c67b3ddb66c5c1bfc502060e83

only because the Windows working-tree blob assertion was corrected and the governed runner was repinned to the corrected test blob.

## Exact functional identities

P5-D3F contract:

    64744325251db350d26c0269090ce62d5fa5f2e8

Corrected contract tests:

    3dc1d7315874d4352eeaf05407f266961c878e70

Corrected Python governed runner:

    1c574e45a970b290ce78e78a7a0b9967e69e43bd

Runner tests:

    b309c3efb759ac3c9604b76fc7defa9cbe446482

## Required local gate

Run the Python governed contract re-break against this exact functional candidate.

The remote race guard must bind the then-current evidence-only branch HEAD.

## Qualification boundary

A successful local run may qualify the P5-D3F contract and runner.

It does not authorize live publication or real-Vault mutation.
