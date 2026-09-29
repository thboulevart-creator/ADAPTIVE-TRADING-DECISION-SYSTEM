# OBSIDIAN P5-D3F — RECOVERY REAL EXECUTION RUNNER V0.3 STATIC REVIEW V3

Date: 2026-09-29

## Evidence status

SAME-ASSISTANT STATIC REVIEW ONLY.

## Exact corrected candidate

    6a2a3e096713c1c2682b9bbb4c47620046956747

V0.3 versioned runner:

    tools/obsidian_projection/p5d3f_recovery_real_execution_v0_3.py

V0.3 runner blob:

    2d22734c73c7e95eed88141c3237ed61afe39dfe

V0.3 tests blob:

    0bb06b5a836b69f3a83e57ad0840b21fe993339c

V0.3 governed re-break blob:

    e369efc5276c70dfde57a172614fad42ad974de3

Historical V0.2 runner restored blob:

    1b44e12a6c23715ea3d5055c9263f4bccb67fe39

Historical V0.2 tests blob:

    64033e4b2fe652a936b690293557bcd0eeac2c4f

## Static findings

PASS — V0.3 no longer overwrites the historical V0.2 runner module.

PASS — historical V0.2 branch/pin expectations are again byte-compatible with their frozen tests.

PASS — V0.3 has a distinct module path and distinct frozen tests.

PASS — the V0.3 re-break binds the new module path and exact V0.3 blobs.

PASS — V0.3 execution semantics are unchanged from the previously targeted runner apart from module versioning.

PASS — no historical test expectation was weakened or removed.

## Current adjudication

    STATIC REVIEW V3 = PASS
    SYNTHETIC V0.3 QUALIFICATION = PENDING
    REAL EXECUTION RETRY = NOT AUTHORIZED
