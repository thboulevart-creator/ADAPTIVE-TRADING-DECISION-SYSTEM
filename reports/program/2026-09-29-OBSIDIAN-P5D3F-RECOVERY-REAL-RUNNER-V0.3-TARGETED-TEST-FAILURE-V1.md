# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION RUNNER V0.3 TARGETED TEST FAILURE V1

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL SYNTHETIC EXECUTION FAILURE.

Observed:

    FAIL: test_failure_snapshot_is_read_only
    Ran 10 tests in 0.024s
    FAILED (failures=1)
    BLOCKED: recovery real-runner targeted tests failed

The complete historical suite was not reached.

## Static diagnosis

SAME-ASSISTANT STATIC REVIEW identifies a platform-dependent test fixture.

The failing test creates evidence.txt with:

    Path.write_text("evidence\n", encoding="utf-8")

and then asserts:

    size == 9

On Windows, text-mode newline translation can persist CRLF bytes, yielding 10 bytes instead of 9.

The production snapshot function correctly reports the actual filesystem byte size via stat().st_size.

Therefore the frozen test expectation is platform-dependent; the runner behavior is not shown to be wrong by this failure.

## Required correction

Make the fixture byte-deterministic:

    write_bytes(b"evidence\n")

Keep expected size:

    9

No runner semantic change is required.

## Boundary

    RECOVERY REAL RUNNER QUALIFICATION = NOT ESTABLISHED
    REAL EXECUTION RETRY = NOT AUTHORIZED
    REAL VAULT WRITE = CLOSED
    LIVE PUBLICATION = CLOSED
