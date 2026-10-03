# RPE-02 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — RED

Date: 2026-10-03

Preregistration HEAD:
`b8b2698252be7f630e435d17313cd1058bec2a51`

Preregistration blob:
`cafee7194155944eb059ead466fd6bc517edde58`

Preregistration schema:
`d67da710e63643c26c0a004cc38109ff4e301b25`

Command:

`python -B -m unittest tests.obsidian_projection.test_rpe02_external_review_targeted_closure_v0_1`

Observed:

```text
Ran 15 tests
FAILED (failures=7)
RPE02_TARGETED_RED_EXIT=1
```

RED findings reproduced:
- unknown outcome not rejected;
- successful remote observation without head not rejected;
- read failure carrying a head not rejected;
- typo outcome carrying target head not rejected;
- infeasible next fixed-rate slot incorrectly reported INCOMPLETE;
- next slot exactly at SLA bound incorrectly reported FAIL_NO_DETECTION;
- out-of-order supplied observations silently sorted.

Already-correct preregistered structural controls remained green.

No protected predecessor was modified.

RPE-04 = CLOSED.
REAL P5-E = CLOSED.
