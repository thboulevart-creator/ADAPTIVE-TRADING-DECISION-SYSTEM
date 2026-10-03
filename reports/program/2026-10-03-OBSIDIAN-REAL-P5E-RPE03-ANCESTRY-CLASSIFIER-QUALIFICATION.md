# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — QUALIFICATION

Date: 2026-10-03

## Verdict

`RPE-03 = QUALIFIED_FOR_EXTERNAL_REVIEW`

Human adoption is pending. RPE-04/RPE-05/RPE-06 and REAL P5-E remain closed.

## Canonical base

RPE-01 adoption commit:
`8ed3ec4079f3f996a5159b78fc40d0f32a917b25`

RPE-01 adoption blob:
`49203ebc2fb208c5dd23ded140295ac00c0afab6`

The adopted P5-E contract, synthetic model and P5-D4 runtime remain unchanged.

## Preregistration and RED

Preregistration HEAD:
`8aa4ee2128a404fd57e64affc4f3b04751e86d87`

Preregistration blob:
`4eca84a17f7d0c53a794f34af65d1d0a81302930`

Closed-schema blob:
`621f909fcde85694a0cc7548adffad7e14ae3970`

The preregistration validates through the adopted RPE-01 public entrypoint.

RED HEAD:
`55f00460dd1ae1004a2d450528937e7a870fc61d`

Observed RED:
`16 tests / 14 failures / 2 passes`.

The fourteen failures reflected the absence of the preregistered classifier.

A Windows-only fixture correction was later required for the corruption test: Git's loose object was non-writable, so the fixture now makes it writable and corrupts its bytes instead of deleting it. No classifier correction was required by that fixture issue.

## No-lazy-fetch hardening amendment

During adversarial qualification, the no-network contract was tightened against Git promisor-object lazy retrieval.

Amendment HEAD:
`b15e9ddeab00257f96cd622f3c80d45d96108e30`

Amendment blob:
`acb57635ee2daf0a65aa57b7f2dab7d5d7d5dcec`

Amendment schema:
`b05984dc868655e0a05f1fab66769032fed2ab3c`

Every classifier Git subprocess receives:
`GIT_NO_LAZY_FETCH=1`.

## Final implementation

Implementation HEAD:
`c1ccde876b9ef9e542e97dd70f290b819e837ac2`

Module:
`7c41bb66a1438c2df9e2e77149a2c3cccb131abb`

Main tests:
`d424f5becbb40d5b9a9276132a1ac684986b7d0d`

Mutation tests:
`72d5f6d5ec38c7dc5785834e636943d7ec5ad181`

## Qualified classifier semantics

The only outputs are:

```text
INITIAL
SAME
FAST_FORWARD
NON_FAST_FORWARD
UNKNOWN
```

The caller cannot provide or override a transition class.

Before classification, the component verifies the local Git domain and requested commit identities.

Fail-closed cases map to `UNKNOWN`, including:
- invalid SHA identity;
- missing object;
- non-commit object;
- command failure;
- timeout;
- requested-object corruption;
- linked worktree/common-dir mismatch;
- shallow repository;
- graft presence;
- objects/info/alternates presence.

`SAME` is explicit and precedes ancestry testing.

`INITIAL` requires a verified new commit in a verified domain and no predecessor.

Only after both commit identities and the object domain are verified does:

`git merge-base --is-ancestor A B`

map:
- exit 0 → `FAST_FORWARD`;
- exit 1 → `NON_FAST_FORWARD`;
- other exit → `UNKNOWN`.

## Git execution isolation

Every Git subprocess:
- uses only local command families `rev-parse`, `cat-file`, and `merge-base --is-ancestor`;
- uses `-c core.commitGraph=false`;
- strips all inherited `GIT_*` variables;
- sets `GIT_NO_REPLACE_OBJECTS=1`;
- sets `GIT_NO_LAZY_FETCH=1`;
- disables system and global Git config;
- disables terminal prompts;
- disables optional locks.

The source contains no network command/API family used by the classifier.

## Governed configuration provenance

The RPE-03 preregistration and its no-lazy-fetch amendment are both closed-schema artifacts validated through RPE-01.

A dedicated parity test binds implementation timeout/environment requirements to those governed artifacts.

No environment, CLI or unlisted file supplies normative classifier authority.

## Mutation/discrimination

Four targeted mutants were killed:

1. merge-base exit 1 incorrectly mapped to FAST_FORWARD;
2. inherited `GIT_*` stripping removed;
3. replace-object neutralization removed;
4. explicit no-lazy-fetch environment hardening removed.

Result:
`4 / 4 KILLED`.

The replace-object mutation uses an unrelated replacement root so the mutant actually changes the ancestry outcome.

## Test result

Dedicated RPE-03 surface:
`21 / 21 PASS`

P5-E + RPE-01 + RPE-03 targeted regression:
`134 / 134 PASS`

Protected diffs:
```text
P5-E CONTRACT = 0
P5-E SYNTHETIC MODEL = 0
P5-D4 RUNTIME = 0
```

Qualification environment:
`Git 2.54.0.windows.1 / CPython 3.13.14 / Windows-11-10.0.22631-SP0`.

## Authority boundary

This qualification does not authorize:
- RPE-04/05/06;
- fetch, remote observation or GitHub polling;
- P5-D4 real-state mutation;
- Vault/CURRENT mutation;
- REAL P5-E;
- human adoption of RPE-03.

Maximum claim:
`RPE03_ANCESTRY_CLASSIFIER = QUALIFIED_FOR_EXTERNAL_REVIEW`.
