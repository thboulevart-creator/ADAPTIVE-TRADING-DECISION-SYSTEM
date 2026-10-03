# RPE-03 — EXTERNAL REVIEW RETURN — CLAUDE

Date: 2026-10-03

## Verdict

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

`BLOCKING_FINDINGS = NONE`

## Non-blocking findings selected for pre-adoption closure

### NB-1 — supplied-domain confinement

The current classifier verifies the repository discovered by Git, but the supplied path can be:
- an ordinary subdirectory of a parent repository;
- a directory whose `.git` file redirects to another repository.

Required closure before RPE-04 consumption:
- exact supplied root must be a verified main worktree root or exact bare repository root;
- parent discovery and `.git` redirection must not be accepted.

### NB-2 — missing discriminating tests

Required additional tests:
- annotated tag as previous object -> UNKNOWN;
- previous object non-commit -> UNKNOWN;
- merge-base exit other than 0/1 -> UNKNOWN;
- corrupted intermediate ancestry object -> UNKNOWN;
- hostile global Git config must not influence classification.

### NB-3 — Git executable identity

Carried as mandatory RPE-04 prerequisite:
- explicit/governed Git executable identity;
- preregistered and verified minimum supported Git version.

### NB-4 — local repository config

Carried as mandatory RPE-04 domain prerequisite. Local config/include/includeIf must not introduce ungoverned authority/provenance.

### NB-5 — packet fidelity

The previous packet labeled the final test as the RED test. The replacement packet must distinguish historical RED blob from final test blob.

## Adoption readiness

The reviewer considered RPE-03 adoptable with notes, but the human authorization explicitly chooses targeted closure of NB-1/NB-2/NB-5 before adoption.

This review creates no authority.

`RPE-04 = CLOSED`
`REAL_P5E = CLOSED`
