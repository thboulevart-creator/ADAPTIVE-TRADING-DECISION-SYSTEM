# RPE-03 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — RED

Date: 2026-10-03

Preregistration HEAD:
`cd2804ac3ec865e065e121cdd7dd92a09b304a8b`

Preregistration blob:
`250f351c656d5a782a4c4e4edad42bfa52a3e498`

Preregistration schema:
`8f2ccf1cbfa5196785a7cc8edb591f3f1fc381da`

Command:

`python -B -m unittest tests.obsidian_projection.test_rpe03_external_review_targeted_closure_v0_1`

Observed:

```text
Ran 9 tests
FAILED (failures=2)
RPE03_TARGETED_RED_EXIT=1
```

RED findings reproduced:
- ordinary subdirectory of a parent repository is accepted as the parent domain;
- directory with a .git redirection file is accepted as another repository domain.

Already-correct cases remained green:
- main worktree root;
- bare repository root;
- annotated tag previous object -> UNKNOWN;
- previous blob -> UNKNOWN;
- merge-base other exit -> UNKNOWN;
- corrupted intermediate ancestry -> UNKNOWN;
- hostile global Git config does not influence classification.

No network operation or protected predecessor mutation occurred.

RPE-04 = CLOSED.
REAL P5-E = CLOSED.
