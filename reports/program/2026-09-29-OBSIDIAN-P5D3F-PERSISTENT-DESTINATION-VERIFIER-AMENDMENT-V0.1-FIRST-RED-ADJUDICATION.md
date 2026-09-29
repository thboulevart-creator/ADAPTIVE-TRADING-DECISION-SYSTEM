# OBSIDIAN P5-D3F — PERSISTENT DESTINATION VERIFIER AMENDMENT V0.1 — FIRST RED RUN ADJUDICATION

Date: 2026-09-29

## Evidence status

USER-REPORTED LOCAL EXECUTION of the RED suite plus SAME-ASSISTANT STATIC REVIEW.

## User-reported RED result

    Ran 6 tests in 0.023s
    FAILED (failures=5)

Observed outcomes:

    PASS — historical temp verifier remains TEMP-only

Expected RED failures:

    FAIL — persistent verifier surface absent
    FAIL — P5-D3F does not import persistent verifier
    FAIL — destination still uses temp-only verifier
    FAIL — explicit authorized_staging_root surface absent

One non-goal failure was also observed:

    FAIL — no-later-authority guard matched generic "while True"

## False-positive adjudication

The generic "while True" token already exists in the historical qualified P5-D3F source inside the bounded filesystem alias-chain traversal helper.

It is not a polling loop, background observer, automatic publication loop, or new authority surface.

Therefore treating every historical "while True" token as forbidden makes the RED guard invalid against the frozen baseline.

The RED guard was corrected narrowly by removing only that generic lexical token while retaining explicit forbidden later-authority surfaces such as:

    execute_finite_live_publication
    PROMOTION_CONFIRMED
    consume_stage_a_plan_approval
    EXECUTE_ONE_FINITE_REAL_LIVE_PUBLICATION_TRANSACTION
    threading.Thread
    schtasks
    CreateService

No implementation code was changed.

## Current exact blobs

Contract blob:

    7d13922e51256f2785af4e6d3062116b2bc324d6

Contract tests blob:

    720470db3dc65d9e335139749a8aebdd0e1ca3d6

Corrected RED tests blob:

    fa421e6c14f7ebf53cc53170a8aaf9f3821acd0b

## Current status

    CONTRACT QUALIFICATION = NOT YET ESTABLISHED FROM USER OUTPUT
    RED FIRST RUN = PARTIALLY VALID
    INTENDED RED SIGNALS = CONFIRMED
    RED TEST HARNESS FALSE POSITIVE = CORRECTED
    IMPLEMENTATION = STILL ABSENT
    REAL EXECUTION = NOT AUTHORIZED

A corrected RED rerun is required before adopting CONTRACT PASS + RED CONFIRMED.
