# OBSIDIAN P5-D3F — IMPLEMENTATION QUALIFICATION TARGET V2

Date: 2026-09-29

## Evidence status

Static qualification target only.

No local implementation execution or sacrificial-staging qualification is claimed here.

## Test-first lineage

Initial implementation tests:

    a4fd962007fce15181eabe907dd0c474333e7f02

Additional breaker tests before correction:

    bd8b5c58b03174bf7386bbd956f260f4800c37af

The additional breakers require:

- promotion staging and live Vault to share the same parent context;
- the retained wrapper directory name to equal the package generation_id.

## Exact functional candidate

    4185c20241eaed03d3155e8d9b30d333947c6293

Implementation:

    tools/obsidian_projection/p5d3f_promotion_handoff.py

Implementation blob:

    90922f53b5ac74fc4ac7ad643d3b38860d60abbb

Tests:

    tests/obsidian_projection/test_p5d3f_promotion_handoff.py

Tests blob:

    ec3292b685f8ee107140a2a75f747de6bb1839b0

## Frozen predecessor authorities

P5-D3F contract:

    64744325251db350d26c0269090ce62d5fa5f2e8

P5-D3C2 verifier:

    e2e5867536f4f9c7dec475c6696737249536ff39

P5-D3D finite evaluator:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

## Qualification gate

The existing governed P5-D3F re-break runner must:

1. verify the fresh remote branch head;
2. check out this exact functional candidate;
3. restore the bounded canonical byte-pinned worktree representation;
4. run its targeted contract controls;
5. run the complete Obsidian unittest suite, including the 12 new P5-D3F implementation tests;
6. require a clean control clone after execution.

Only a full PASS may advance to explicit sacrificial-staging qualification evidence.

P5-D3G and all real publication authority remain closed.
