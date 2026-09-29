# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION RUNNER V0.4 MONITORED-HEAD PIN — STATIC REVIEW

Date: 2026-09-29

## Evidence status

SAME-ASSISTANT STATIC REVIEW ONLY.

This is not local execution evidence and does not qualify the runner.

## Exact functional candidate reviewed

    d2445091ad1a0d646cbf016e52f5c9a19057e89b

Runner blob:

    0dfb31d86c84739fc66ee7efb6ca82e97396d87b

Frozen V0.4 tests blob:

    667e458962aca47a1d3f08ef3f12c80015c1390b

Governed V0.4 re-break blob:

    e6c9ab7f98c9fa8f77db3dc98571120e6cbeb7c0

Targeted test count:

    11

## Static findings

PASS — V0.4 has a distinct versioned module and branch identity; V0.3 historical surfaces remain untouched.

PASS — --expected-monitored-head is mandatory and 40-hex validated.

PASS — before any persistent handoff call, the runner reads refs/heads/integration/system-v1 and requires exact equality with the authorized monitored HEAD.

PASS — mismatch fails closed with BLOCKED_MONITORED_HEAD_AUTHORITY_MISMATCH.

PASS — successful handoff result must bind candidate_head exactly to the authorized monitored HEAD.

PASS — post-success-cleanup-block evidence is also revalidated against the authorized monitored HEAD before being surfaced as a successful body result.

PASS — the qualified persistent implementation's independent remote freshness and final pre-handoff race checks remain unchanged, preserving fail-closed behavior if the branch moves after the runner-level authority check.

PASS — exact recovery prestate remains PRESENT_EMPTY_PACKAGES_RECOVERY.

PASS — failure-preservation and post-success cleanup evidence surfaces remain present.

PASS — no live-publication, PROMOTION_CONFIRMED, Stage A, Stage B, pointer replacement, background loop/task/service authority was added.

## Current adjudication

    STATIC REVIEW = PASS
    SYNTHETIC V0.4 QUALIFICATION = PENDING
    REAL EXECUTION = NOT AUTHORIZED
    PRIOR V0.3 AUTHORIZATION = NOT TRANSFERABLE TO V0.4

A fresh V0.4 one-shot human authorization is required only after synthetic qualification and fresh remote/staging prechecks.
