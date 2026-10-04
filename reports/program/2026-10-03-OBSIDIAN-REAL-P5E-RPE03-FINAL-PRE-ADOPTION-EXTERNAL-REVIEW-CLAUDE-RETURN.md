# RPE-03 — FINAL PRE-ADOPTION EXTERNAL DELTA REVIEW — CLAUDE RETURN

Date: 2026-10-03

## Verdict

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

`BLOCKING_FINDINGS = NONE`

`RPE03_ADOPTION_READINESS = YES`

## Identity reconstruction

Reviewer reports successful reconstruction of all announced identities, including:
- implementation `145b311…`;
- targeted test `14d63db…` unchanged between RED and GREEN;
- targeted mutation test `0a4dbeb…`;
- preregistration `250f351…`;
- qualification `da4a105…` / `5ab434c…`;
- original historical RED `eca4381…`;
- final pre-closure test `d424f5b…`.

The implementation delta was limited to `_verified_domain`.

Independent reproduction environment:
- Git 2.43.0;
- CPython 3.12.3;
- Linux.

Observed:
- 21 + 9 + 5 tests and the four original mutation tests all PASS;
- P5-E + RPE-01 + RPE-03 targeted regression PASS.

## Non-blocking finding NB-1′ — physical object-store indirection

The exact supplied path confinement is not equivalent to physical object-store containment.

Observed counterexamples:
- a supplied directory whose `.git` is a symlink to another repository's `.git`;
- a worktree repository whose `.git/objects` is a symlink to another object store;
- a bare repository whose `objects` is a symlink to another bare object store.

These cases can still classify correctly because ancestry between immutable commit IDs remains intrinsic, but RPE-03 may not claim that classification proves physical materialization inside an isolated supplied object-store domain.

Reviewer recommendation: close here by rejecting symlink/junction/reparse indirection, or carry the physical-containment requirement explicitly to RPE-04.

## Non-blocking finding NB-6 — bare exact-root condition insufficiently test-locked

The current implementation correctly contains:

```python
if not _same_path(git_dir, repo):
    return None
```

for a bare repository.

However, a mutant removing that check survives the existing RPE-03 suites. With that mutant:

`classify_transition("bare.git/objects", A, B) -> FAST_FORWARD`

while the current implementation correctly returns `UNKNOWN`.

Recommended closure: add one test using a bare-repository subdirectory.

## Domain confinement check

Observed:
- exact main worktree root -> classified;
- exact bare repository root -> classified;
- ordinary subdirectory of parent repository -> UNKNOWN;
- supplied `.git` directory itself -> UNKNOWN;
- bare repository subdirectory -> UNKNOWN in current implementation;
- `.git` redirection file -> UNKNOWN;
- symlink/junction/reparse physical indirection remains outside the qualified claim.

## Discrimination check

Observed:
- annotated tag previous object -> UNKNOWN;
- previous blob -> UNKNOWN;
- unexpected merge-base exit -> UNKNOWN;
- corrupted intermediate ancestry -> UNKNOWN;
- hostile global Git config does not influence classification.

Five targeted mutants are killed. One additional reviewer mutant survives only because NB-6 lacks a direct test.

## RPE-04 carried preconditions

The following remain correctly carried rather than claimed closed:
- explicit/governed Git executable identity;
- preregistered/verified minimum Git version;
- controlled local repository configuration domain;
- `include.path` / `includeIf` may not introduce ungoverned authority/provenance.

Reviewer requests adding filesystem object-domain indirection absence/governance to the RPE-04 carried preconditions.

## Packet fidelity

Original historical RED, final pre-closure test, and targeted RED identities are distinct and correctly represented.

## Authority

This review creates no authority.

`RPE-04 = CLOSED`

`REAL P5-E = CLOSED`
