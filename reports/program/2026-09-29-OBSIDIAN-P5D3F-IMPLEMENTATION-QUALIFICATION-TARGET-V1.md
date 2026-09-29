# OBSIDIAN P5-D3F — IMPLEMENTATION QUALIFICATION TARGET V1

Date: 2026-09-29

## Evidence status

Static qualification target only.

No local implementation test or sacrificial staging execution is claimed here.

## Test-first commit

    a4fd962007fce15181eabe907dd0c474333e7f02

Tests blob:

    a48caad8ac253bcb9a11a422415c81e42ab20ac6

## Exact functional implementation candidate

    d7f400a5934a4aa6ac7ead31d05ab4b0cc472ec3

Implementation blob:

    03ea39bccd11d923e7aedaaf86009e22b2b2b2fa

## Frozen authorities

P5-D3F contract:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3C2 packager/verifier:

    e2e5867536f4f9c7dec475c6696737249536ff39

P5-D3D finite evaluator:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

## Candidate scope

The implementation adds only a finite promotion-handoff candidate and its tests.

The candidate:

- accepts an already prepared exact candidate repository;
- performs no network resolution;
- performs a fresh P5-D3D finite evaluation;
- preserves REJECTED vs BLOCKED;
- verifies the P5-D3C2 source package;
- copies the sealed package path-by-path and byte-for-byte;
- rejects aliases/reparse surfaces and hard links;
- recomputes package byte-tree identity;
- reverifies the destination package;
- writes PROMOTION-HANDOFF.json last;
- verifies the completed handoff read-only;
- returns only READY_UNAUTHORIZED success;
- does not create or mutate CURRENT/CURRENT.tmp;
- does not invoke P5-C2 or P5-C3R2 publication primitives;
- does not emit PROMOTION_CONFIRMED;
- does not perform real-Vault writes.

## Local gate

The existing governed P5-D3F re-break runner may be used to check out this exact candidate, restore canonical byte-pinned worktree representation, and execute the full Obsidian suite.

A full-suite PASS is required before the implementation candidate can advance to a separately persisted sacrificial-staging qualification result.

P5-D3G remains closed.
