# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION TARGET V4

Date: 2026-09-28

## Exact functional candidate

    28a1dd16e09c6534e4af404e1a5b2779113e453e

This candidate supersedes V3 only for execution-environment hardening.

## Exact identities

P5-D3F contract:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3F contract tests:

    3dc1d7315874d4352eeaf05407f266961c878e70

Canonical checkout policy:

    .gitattributes
    e0154899b5640da025a082ef6b02f4bf179d3030

Governed Python runner:

    b2bdbd90fcb27568940b28c0b389ac2222f76f9a

Runner tests:

    a188bf40a8f1e8bc6a457040f8f469d13d8d0281

## Required local proof

The governed run must demonstrate:

    P5D3F_CANONICAL_LF_CHECKOUT=PASS
    P5D3F_BYTE_PIN_COMPATIBILITY=PASS
    P5D3F_CONTRACT_BLOB=PASS
    P5D3F_CONTRACT_TEST_BLOB=PASS
    P5D3F_CONTRACT_PY_COMPILE=PASS
    P5D3F_CONTRACT_TARGETED=PASS
    P5D3F_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_CONTRACT_REBREAK_COMPLETED=PASS

## Boundary

A successful local run may qualify the P5-D3F contract and its runner.

No P5-D3F implementation, live publication, CURRENT mutation or real Vault write is authorized before that PASS is adjudicated and persisted.
