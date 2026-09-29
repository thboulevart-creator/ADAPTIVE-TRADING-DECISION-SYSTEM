# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION RUNNER V0.3 SYNTHETIC QUALIFICATION V1

Date: 2026-09-29

## Evidence status

Qualification is based on USER-REPORTED LOCAL EXECUTION of the governed V0.3 recovery real-runner re-break.

This is not independently executed evidence by the assistant.

## Verified GitHub state before persistence

Remote HEAD:

    81eb57e05ce9accd999e4d1f9fac28575dfb3bdb

Exact qualification candidate:

    6a2a3e096713c1c2682b9bbb4c47620046956747

Versioned V0.3 recovery real-execution runner:

    tools/obsidian_projection/p5d3f_recovery_real_execution_v0_3.py

Runner blob:

    2d22734c73c7e95eed88141c3237ed61afe39dfe

Frozen V0.3 tests blob:

    0bb06b5a836b69f3a83e57ad0840b21fe993339c

Governed V0.3 re-break blob:

    e369efc5276c70dfde57a172614fad42ad974de3

Qualified recovery implementation blob:

    dcd70a9d9794675eab90e41df560f8b030b5dbf3

Qualified recovery implementation tests blob:

    242305bc0f95bbe243158b5c806255508093a357

Qualified recovery contract V0.2 blob:

    aef627936b6f745017bcace7e8a3e44270f95674

Qualified original persistent gate contract V0.1 blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## User-reported governed result

Targeted V0.3 recovery real-runner tests:

    Ran 10 tests in 0.008s
    OK

Complete historical Obsidian suite:

    Ran 1252 tests in 205.640s
    OK

Terminal markers:

    P5D3F_RECOVERY_REAL_RUNNER_TARGETED=PASS
    P5D3F_RECOVERY_REAL_RUNNER_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3F_RECOVERY_REAL_RUNNER_REBREAK_COMPLETED=PASS

No FAIL, ERROR, or BLOCKED marker was reported in the completed governed run.

## Historical compatibility result

The previously observed historical-suite failures were closed by restoring the V0.2 runner byte-exact at its historical path and moving V0.3 to a distinct versioned module.

No historical V0.2 test expectation was weakened.

## Adjudication

    P5-D3F RECOVERY REAL EXECUTION RUNNER V0.3 — SYNTHETIC QUALIFICATION = PASS

## Qualified real-retry precondition

The V0.3 runner may only accept:

    PERSISTENT STAGING PRESTATE = PRESENT_EMPTY_PACKAGES_RECOVERY

This means exactly:

    staging/
      packages/    [empty]

with no other top-level staging entry and no retained handoff record.

## Next exact gate

    NEW HUMAN ONE-SHOT P5-D3F RECOVERY REAL EXECUTION AUTHORIZATION

A new explicit human authorization is required before any real retry.

## Authority remaining closed until that new authorization

- real execution retry;
- any real-Vault write;
- CURRENT / CURRENT.tmp mutation;
- live publication;
- P5-D2 PROMOTION_CONFIRMED;
- Stage A;
- Stage B;
- automatic/background publication;
- P5-D4;
- P6.

Any future real invocation consumes its authorization when the governed V0.3 entrypoint is reached, whether the result is PASS or BLOCKED.

A PASS requires mandatory STOP.
A BLOCKED/FAIL result requires residual audit before any later authorization.
