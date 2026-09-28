# OBSIDIAN P5-D3F — CONTRACT QUALIFICATION TARGET V3

Date: 2026-09-28

## Exact functional candidate

    6ed8a755499c73b80eacfa0886fac6702d591d78

## Exact blobs

Contract:

    64744325251db350d26c0269090ce62d5fa5f2e8

Contract tests:

    3dc1d7315874d4352eeaf05407f266961c878e70

Governed Python runner:

    6e1d8980fcd41971de4ab61deb3b9f85ddd1ea7b

Runner tests:

    843f3b7d97fbe2750379709b777bc4eceac3e2e8

## Why V3 supersedes V2

V2 fixed checkout-normalization-safe contract blob assertions.

V3 additionally fixes the runner bootstrap boundary so a process that changes its own checkout re-execs from the target candidate before any evidence-critical checks.

## Required local result

The local governed run must reach:

    P5D3F_CONTRACT_BLOB=PASS
    P5D3F_CONTRACT_TEST_BLOB=PASS
    P5D3F_CONTRACT_PY_COMPILE=PASS
    P5D3F_CONTRACT_TARGETED=PASS
    P5D3F_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_CONTRACT_REBREAK_COMPLETED=PASS

No implementation or publication authority is granted before that PASS is adjudicated and persisted.
