# RPE-03 — FINAL PRE-ADOPTION TEST + SCOPE CLOSURE V0.1 — QUALIFICATION

Date: 2026-10-03

## Result

`RPE-03 FINAL PRE-ADOPTION = QUALIFIED_FOR_HUMAN_ADOPTION`

This is not a human adoption.

## External review basis

The final external delta review returned:

```text
VERDICT = PASS_WITH_NON_BLOCKING_NOTES
BLOCKING_FINDINGS = NONE
RPE03_ADOPTION_READINESS = YES
```

Persisted external-review blob:

`980e0d65da684fac88f16422f4843983c9ecbc8d`

Internal adjudication blob:

`8228fae41f7c81598e871858c9cdf2ef4ca74d48`

## NB-6 — CLOSED TEST-ONLY

The classifier implementation was not modified.

Classifier blob remains:

`145b3112fd9309cc34d95a62c091cb6a6bc3bb11`

New NB-6 test blob:

`b7724499e0fe15b069689afb2f222ed2f4223eeb`

Observed:

```text
3 / 3 PASS
```

The test proves:

```text
EXACT BARE REPOSITORY ROOT
→ allowed

BARE REPOSITORY SUBDIRECTORY
→ UNKNOWN
```

A targeted mutant removing the bare-root condition:

```python
if not _same_path(git_dir, repo):
    return None
```

is killed: the mutant classifies the bare `objects` subdirectory as FAST_FORWARD while the qualified implementation returns UNKNOWN.

Therefore:

`NB-6 = CLOSED`

with no functional code change.

## NB-1′ — SCOPE CLOSED BY EXPLICIT NON-CLAIM

Adopted qualification boundary:

```text
RPE03_SUPPLIED_PATH_CONFINEMENT
= QUALIFIED

RPE03_PHYSICAL_OBJECT_STORE_CONTAINMENT
= NOT_CLAIMED
```

RPE-03 qualifies supplied-path identity for exact main-worktree and exact bare-repository roots.

RPE-03 does not qualify physical containment of the underlying object store against:

- symlinks;
- junctions;
- reparse points;
- equivalent filesystem indirection.

This is not treated as a hidden omission.

It is an explicit mandatory RPE-04 precondition.

## Mandatory RPE-04 preconditions

RPE-04 may not consume RPE-03 without preregistering and qualifying:

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

At minimum, filesystem-domain qualification must cover, when present:

- `.git`;
- `objects`;
- `objects/pack`;
- `objects/info`;
- equivalent bare-repository paths.

RPE-04 must preserve:

```text
PATH IDENTITY
!=
PHYSICAL OBJECT-STORE CONTAINMENT
```

and must not infer:

```text
RPE-03 CLASSIFIED
→ OBJECTS PHYSICALLY MATERIALIZED IN ISOLATED DOMAIN
```

without separate evidence.

## Regression

Complete RPE-03 dedicated surface:

`38 / 38 PASS`

P5-E + RPE-01 + RPE-03 targeted regression:

`151 / 151 PASS`

Protected predecessor diffs:

```text
P5-E CONTRACT = 0
P5-E SYNTHETIC MODEL = 0
P5-D4 RUNTIME = 0
```

## Authority boundary

No human adoption has occurred.

```text
RPE-03 HUMAN ADOPTION = PENDING
RPE-03 CLOSED = NO
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED
```

No network runtime, P5-D4 real-state mutation, Vault/CURRENT mutation, daemon/service/startup or P6 authority is created.

## Next gate

`HUMAN ADOPTION RPE-03`
