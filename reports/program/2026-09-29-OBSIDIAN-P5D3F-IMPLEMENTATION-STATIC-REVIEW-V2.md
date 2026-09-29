# OBSIDIAN P5-D3F — IMPLEMENTATION STATIC REVIEW V2

Date: 2026-09-29

## Evidence status

Same-assistant static review.

This is not execution evidence and does not qualify the implementation.

## Exact candidate

    4185c20241eaed03d3155e8d9b30d333947c6293

Implementation blob:

    90922f53b5ac74fc4ac7ad643d3b38860d60abbb

Tests blob:

    ec3292b685f8ee107140a2a75f747de6bb1839b0

## Static review

PASS — exact authorities remain pinned:

    P5-D3F contract
    64744325251db350d26c0269090ce62d5fa5f2e8

    P5-D3C2 verifier
    e2e5867536f4f9c7dec475c6696737249536ff39

    P5-D3D evaluator
    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

PASS — the implementation performs fresh finite evaluation before any promotion-staging mutation.

PASS — REJECTED and BLOCKED evaluator outcomes remain distinct and return without creating a retained handoff target.

PASS — source and destination P5-D3C2 packages are both reverified.

PASS — the source package is copied path-by-path and byte-by-byte; evaluator-workspace rename is not used.

PASS — source and destination byte-tree identities are recomputed and required equal.

PASS — hard links, symlinks, junctions and reparse entries fail closed.

PASS — promotion staging and live Vault must not overlap and must share the same parent context.

PASS — staging may not be a Git worktree.

PASS — a pre-existing generation target blocks instead of being overwritten.

PASS — wrapper layout is exact and the wrapper directory name must equal generation_id.

PASS — PROMOTION-HANDOFF.json is canonical, exact-field, outside the sealed package, and written only after copied-package verification.

PASS — the verifier is read-only and independently reverifies the copied package, byte-tree identity and wrapper/package bindings.

PASS — all publication-authority flags remain false.

PASS — there is no os.replace, CURRENT.tmp writer, PROMOTION_CONFIRMED emission, HTTP client, sleep loop, scheduler, service, or publication primitive in the candidate.

The single `while True` is a finite parent-directory ascent that terminates at the filesystem root; it is not polling or background observation.

## Test surface

New P5-D3F implementation test methods:

    12

They cover:

- frozen tooling identities;
- successful synthetic READY_UNAUTHORIZED handoff;
- REJECTED no-handoff behavior;
- BLOCKED no-handoff behavior;
- live/staging overlap rejection;
- common parent-context enforcement;
- wrapper generation-ID binding;
- existing-target collision;
- copied-payload tamper rejection;
- handoff-record tamper rejection;
- read-only verification;
- hard-link rejection.

## Remaining uncertainty

No Python compilation or local unittest execution has yet been observed for this candidate.

No sacrificial handoff has yet been qualified.

## Verdict

    STATIC IMPLEMENTATION REVIEW = PASS
    FUNCTIONAL CANDIDATE = READY FOR GOVERNED LOCAL RE-BREAK
    P5-D3F IMPLEMENTATION = NOT YET QUALIFIED
    SACRIFICIAL STAGING QUALIFICATION = NOT YET ESTABLISHED
    P5-D3G = CLOSED
    REAL VAULT WRITE = CLOSED
