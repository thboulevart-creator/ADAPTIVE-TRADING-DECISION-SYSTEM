# OBSIDIAN P5-D3F — PERSISTENT HANDOFF RECOVERY IMPLEMENTATION V0.3 QUALIFICATION TARGET

Date: 2026-09-29

## Evidence status

Synthetic qualification target only.

No persistent staging mutation.
No real Vault access.
No real execution.

## Exact candidate

    c3de1640df0280c34a667b356be279ce3e1eea88

Recovery implementation:

    tools/obsidian_projection/persistent_production_handoff.py

Implementation blob:

    dcd70a9d9794675eab90e41df560f8b030b5dbf3

Frozen targeted tests:

    tests/obsidian_projection/test_p5d3f_persistent_handoff_recovery_implementation_v0_3.py

Tests blob:

    242305bc0f95bbe243158b5c806255508093a357

Governed synthetic re-break:

    tools/obsidian_projection/p5d3f_persistent_handoff_recovery_implementation_rebreak_v0_3.py

Re-break blob:

    5d7693552826f2394024ec3c7c3b280ad8b6f5be

Qualified recovery contract V0.2 blob:

    aef627936b6f745017bcace7e8a3e44270f95674

Qualified original persistent gate contract V0.1 blob:

    59ce9e079d256799d072405fa4a623ba58b75c0d

Qualified P5-D3F runtime blob:

    2108131914cf65bb076b80f5bb63cd63267567fa

## Frozen targeted surface

    13 tests

## Candidate behavior

The candidate:

1. retains V0.1 authority pins and adds the qualified recovery-contract V0.2 pin;
2. admits only the exact PRESENT_EMPTY_PACKAGES_RECOVERY state;
3. continues to block arbitrary nonempty staging;
4. handles the ABSENT -> PRESENT_EMPTY setup transition without treating it as a race;
5. requires all other staging prestates to remain exact;
6. preserves body failures and annotates them with the temporary root;
7. does not delete temporary evidence after body failure;
8. performs temporary cleanup only after body success;
9. classifies post-success cleanup failure distinctly as BLOCKED_TEMPORARY_CLEANUP_AFTER_BODY_SUCCESS;
10. binds the successful handoff result to that post-success cleanup exception for later audit;
11. keeps live-publication and later-stage authority absent.

## Qualification sequence

- exact remote-race guard;
- exact candidate HEAD;
- exact implementation/test/contract/runtime blob pins;
- static required/forbidden surface scan;
- Python compilation;
- 13 targeted tests;
- complete historical Obsidian suite;
- final clean-control-clone gate.

## Authority

Synthetic qualification only.

No real retry is authorized by this target.
Real Vault write remains closed.
Live publication remains closed.
Stage A and Stage B remain closed.
