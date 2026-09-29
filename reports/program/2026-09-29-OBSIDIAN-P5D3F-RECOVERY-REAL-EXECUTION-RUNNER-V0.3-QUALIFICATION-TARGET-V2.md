# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION RUNNER V0.3 QUALIFICATION TARGET V2

Date: 2026-09-29

## Correction reason

The first synthetic qualification attempt failed one targeted test:

    test_failure_snapshot_is_read_only

Static review established that the test fixture used text-mode Path.write_text("evidence\n") while asserting an exact byte size of 9.

On Windows, newline translation can persist CRLF bytes and produce a size of 10.

The production runner reports actual filesystem byte size via stat().st_size.

Therefore the correction is test-fixture-only:

    write_text("evidence\n")
    ->
    write_bytes(b"evidence\n")

The expected byte size remains 9.

No runner semantic changed.

## Corrected exact qualification candidate

    7c76e4870d76b09014a0bd58b2936c9583223f36

Runner blob:

    ab9702e0288dedf6c126be35239603d8112e028c

Corrected tests blob:

    aef1dedec8217dff6d3dee4c5ecc184a08f495ab

Governed re-break blob:

    1fcbcc572d53f046849a586de4086f331bcff1d4

Targeted tests:

    10

## Authority effect

None.

This correction does not authorize real execution and does not change staging, Vault, publication, Stage A or Stage B authority.

## Required re-break

A fresh governed synthetic re-break must pass:

- corrected 10 targeted tests;
- complete historical Obsidian suite;
- exact blob pins;
- clean control clone.
