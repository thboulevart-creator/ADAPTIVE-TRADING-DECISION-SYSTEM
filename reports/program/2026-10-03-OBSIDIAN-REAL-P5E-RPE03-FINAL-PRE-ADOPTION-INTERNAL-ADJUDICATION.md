# RPE-03 — FINAL PRE-ADOPTION TEST + SCOPE CLOSURE V0.1 — INTERNAL ADJUDICATION

Date: 2026-10-03

External review:

```text
VERDICT = PASS_WITH_NON_BLOCKING_NOTES
BLOCKING_FINDINGS = NONE
RPE03_ADOPTION_READINESS = YES
```

## NB-6 adjudication

`NB-6 = CONFIRMED / TEST-ONLY CLOSURE REQUIRED`

The current implementation already rejects a bare-repository subdirectory because a bare domain is accepted only when:

```text
git_dir == supplied resolved path
```

A dedicated regression and mutation check must now make this invariant non-regressible.

No implementation change is authorized unless that new test fails against the current implementation.

## NB-1′ scope adjudication

Adopted scope:

```text
RPE03_SUPPLIED_PATH_CONFINEMENT
= QUALIFIED

RPE03_PHYSICAL_OBJECT_STORE_CONTAINMENT
= NOT_CLAIMED
```

RPE-03 qualifies exact supplied-path identity for:
- MAIN_WORKTREE_ROOT;
- BARE_REPOSITORY_ROOT.

RPE-03 does not claim that the underlying object store is physically contained within that supplied root.

The following filesystem indirections are explicitly outside RPE-03's qualified claim:
- SYMLINK;
- JUNCTION;
- REPARSE_POINT;
- equivalent filesystem redirection.

## Mandatory RPE-04 carried precondition

RPE-04 must preregister and qualify:

```text
PATH IDENTITY
!=
PHYSICAL OBJECT-STORE CONTAINMENT
```

and may not infer:

```text
RPE-03 CLASSIFIED
=> OBJECTS PHYSICALLY MATERIALIZED IN ISOLATED DOMAIN
```

without additional qualification.

At minimum, when present, RPE-04 must control filesystem indirection for:
- `.git`;
- `objects`;
- `objects/pack`;
- `objects/info`;
- bare-repository equivalents.

Additional carried RPE-04 preconditions remain:

```text
GIT EXECUTABLE IDENTITY
= EXPLICIT / GOVERNED

MINIMUM SUPPORTED GIT VERSION
= PREREGISTERED / VERIFIED

LOCAL REPOSITORY CONFIG
= CONTROLLED DOMAIN REQUIRED

include.path / includeIf
= MUST NOT INTRODUCE UNGOVERNED AUTHORITY OR PROVENANCE

FILESYSTEM OBJECT-DOMAIN INDIRECTION
= ABSENT OR EXPLICITLY GOVERNED AND QUALIFIED
```

## Authority boundary

This adjudication does not adopt RPE-03.

It does not open:
- RPE-04;
- RPE-05;
- RPE-06;
- REAL P5-E;
- network;
- real polling/fetch;
- P5-D4 real-state mutation;
- Vault/CURRENT;
- persistent runtime.

STOP remains before human adoption.
