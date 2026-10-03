# RPE-03 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — QUALIFICATION

Date: 2026-10-03

## Result

`RPE-03 TARGETED CLOSURE = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW`

The prior external verdict was `PASS_WITH_NON_BLOCKING_NOTES`. No human adoption is created here.

## Closure identities

External review:
`50acb047475ba568a54b15ea8a4d3aaea170878c`

Internal adjudication:
`bf9caa0792e6e47fd48f4186f7e3e71577375459`

Targeted preregistration:
`250f351c656d5a782a4c4e4edad42bfa52a3e498`

Schema:
`8f2ccf1cbfa5196785a7cc8edb591f3f1fc381da`

Targeted RED HEAD:
`9cf0056eb938c631100ac7e4891b750d0bdb5984`

Targeted RED test:
`14d63db2c986d19f217ec598404927764944a05d`

Targeted RED report:
`2125afe83dc58ffff6305d22dacf0b35b9bc8664`

Final candidate HEAD:
`b0e57da54c09a838107e33fed34e0afc0afab6de`

Final implementation:
`145b3112fd9309cc34d95a62c091cb6a6bc3bb11`

Targeted mutation tests:
`0a4dbebcb61b13badc8c15b14b41924e3d9c031d`

## NB-1 supplied-domain confinement

The supplied path is now accepted only as:
- exact main worktree root; or
- exact bare repository root.

Main-worktree acceptance requires:
- git --show-toplevel equals the supplied resolved path;
- .git is a local directory, not a redirection file;
- git-dir equals common-dir;
- git-dir equals supplied_path/.git.

Bare acceptance requires git-dir/common-dir to equal the supplied resolved root.

An ordinary subdirectory of a parent repository returns UNKNOWN.
A directory using a .git redirection file returns UNKNOWN.

## NB-2 discrimination

New permanent cases cover:
- annotated tag as previous object -> UNKNOWN;
- previous blob -> UNKNOWN;
- merge-base exit other than 0/1 -> UNKNOWN;
- corrupted intermediate ancestry object -> UNKNOWN;
- hostile global Git configuration -> no influence.

Five targeted mutants are killed, covering:
- parent-repository discovery;
- .git redirection;
- commit-type enforcement using an annotated tag;
- merge-base unexpected-exit mapping;
- global-config neutralization.

## NB-3 / NB-4 carry

RPE-04 must not consume RPE-03 until it qualifies:
- explicit governed Git executable identity;
- preregistered/verified minimum Git version;
- a controlled repository configuration domain;
- include.path/includeIf cannot create ungoverned authority or provenance.

These are explicit preconditions, not claimed closed by RPE-03.

## Evidence

Targeted closure:
`9 / 9 PASS`

Targeted mutation discrimination:
`5 / 5 PASS; 5 / 5 mutants killed`

P5-E + RPE-01 + RPE-03 regression:
`148 / 148 PASS`

Protected diffs:
- P5-E contract = 0;
- P5-E synthetic model = 0;
- P5-D4 runtime = 0.

## Packet fidelity

The rebuilt packet must distinguish:
- original historical RED test blob `eca438187aceb64b4d96d29bcda6c5896864b12e`;
- original final test blob `d424f5becbb40d5b9a9276132a1ac684986b7d0d`;
- targeted historical RED test blob `14d63db2c986d19f217ec598404927764944a05d`.

## Authority

RPE-03 human adoption = pending.
RPE-04/05/06 = closed.
REAL P5-E = closed.
