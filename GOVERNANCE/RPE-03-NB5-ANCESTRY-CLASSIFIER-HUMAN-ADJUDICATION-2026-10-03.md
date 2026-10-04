# RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1 — HUMAN ADJUDICATION

Date: 2026-10-03

## Human decision

The human authority adopts:

`RPE-03 — NB5 ANCESTRY CLASSIFIER V0.1`

in its final qualified state after:
- initial qualification;
- independent external review;
- external-review targeted closure;
- NB-6 bare-root test-only closure;
- explicit scope adjudication of NB-1′.

The adopted normative state is:

`RPE03_ANCESTRY_CLASSIFIER = QUALIFIED_AND_HUMAN_ADOPTED`

After persistence and verification of this record:

`RPE-03 = CLOSED`

This adoption does not open RPE-04.

## Binding pre-adoption identity

```text
FINAL PRE-ADOPTION HEAD
= 827e7cfadfddc779c915a8efc6d4b33cc784f810

RPE-03 CLASSIFIER
= 145b3112fd9309cc34d95a62c091cb6a6bc3bb11

NB-6 TEST
= b7724499e0fe15b069689afb2f222ed2f4223eeb

FINAL PRE-ADOPTION QUALIFICATION
= 883aa61e90d50c8a2c44f495d985295d16874302

FINAL PRE-ADOPTION QUALIFICATION REPORT
= 25b7e4957306c5f4473c597de2a2a28834c83bec

FINAL EXTERNAL REVIEW RETURN
= 980e0d65da684fac88f16422f4843983c9ecbc8d

FINAL INTERNAL ADJUDICATION
= 8228fae41f7c81598e871858c9cdf2ef4ca74d48
```

Branch at adoption:

`feat/obsidian-projection-rpe03-ancestry-classifier-v0.1`

Pre-adoption local and remote HEAD were equal.

Pre-adoption worktree was clean.

## Final evidence accepted

```text
RPE-03 DEDICATED SURFACE
= 38 / 38 PASS

P5-E + RPE-01 + RPE-03 TARGETED REGRESSION
= 151 / 151 PASS

P5-E CONTRACT DIFF
= 0

P5-E SYNTHETIC MODEL DIFF
= 0

P5-D4 RUNTIME DIFF
= 0
```

## Adopted classification vocabulary

```text
INITIAL
SAME
FAST_FORWARD
NON_FAST_FORWARD
UNKNOWN
```

Adopted properties include:

```text
NETWORK INSIDE CLASSIFIER
= FORBIDDEN

MISSING / INVALID / NON-COMMIT OBJECT
= UNKNOWN

TIMEOUT / CORRUPTION / UNVERIFIED DOMAIN
= UNKNOWN

SAME
= EXPLICITLY DETECTED BEFORE ANCESTRY TEST

MERGE-BASE EXIT 0
= FAST_FORWARD

MERGE-BASE EXIT 1
= NON_FAST_FORWARD

OTHER MERGE-BASE EXIT
= UNKNOWN
```

No caller-supplied transition class may override the classifier result.

## Adopted supplied-path confinement

```text
RPE03_SUPPLIED_PATH_CONFINEMENT
= QUALIFIED
```

Qualified supplied-domain kinds:

```text
MAIN_WORKTREE_ROOT
BARE_REPOSITORY_ROOT
```

according to the exact qualified rules.

## NB-6 — adopted closure

```text
EXACT BARE REPOSITORY ROOT
= ALLOWED

BARE REPOSITORY SUBDIRECTORY
= UNKNOWN

NB-6
= CLOSED
```

The final test-only closure did not modify the classifier implementation.

Classifier blob:
`145b3112fd9309cc34d95a62c091cb6a6bc3bb11`

NB-6 test blob:
`b7724499e0fe15b069689afb2f222ed2f4223eeb`

The targeted mutant removing the exact bare-root condition is killed.

## NB-1' — explicit adopted scope boundary

```text
RPE03_PHYSICAL_OBJECT_STORE_CONTAINMENT
= NOT_CLAIMED
```

Therefore:

```text
PATH IDENTITY
!=
PHYSICAL OBJECT-STORE CONTAINMENT
```

and:

```text
RPE-03 CLASSIFIED
!=
PROOF THAT OBJECTS ARE PHYSICALLY MATERIALIZED
INSIDE AN ISOLATED OBJECT-STORE DOMAIN
```

RPE-03 does not by itself qualify physical object-store containment against:
- SYMLINK;
- JUNCTION;
- REPARSE_POINT;
- equivalent filesystem redirection.

This boundary is intentional and does not reopen RPE-03.

## Mandatory RPE-04 preconditions carried by this adoption

RPE-04 may not consume RPE-03 without separately preregistering and qualifying:

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

The filesystem qualification must cover, when applicable:
- .git
- objects
- objects/pack
- objects/info
- bare repository equivalents.

RPE-04 must preserve:

```text
PATH IDENTITY
!=
PHYSICAL OBJECT-STORE CONTAINMENT
```

and may not infer:

```text
RPE-03 CLASSIFIED
-> OBJECTS PHYSICALLY MATERIALIZED IN ISOLATED DOMAIN
```

without independent qualification evidence.

## Protected predecessor integrity

This persistence step does not modify:
- the adopted P5-E contract;
- the adopted P5-E synthetic model;
- the P5-D4 runtime;
- RPE-01;
- RPE-02;
- any real P5-D4 control state;
- Vault or CURRENT;
- RPE-04 or later stages.

## Stage state after verified persistence

```text
RPE-03
= CLOSED
= QUALIFIED_AND_HUMAN_ADOPTED

RPE-04
= CLOSED

RPE-05
= CLOSED

RPE-06
= CLOSED

REAL P5-E
= CLOSED
```

RPE-02 state is unchanged by this RPE-03 adoption record.

This record does not open or authorize RPE-04.

## Explicitly not authorized

This adoption does not authorize:
- RPE-04 implementation or execution;
- RPE-05 implementation or execution;
- RPE-06 implementation or execution;
- real GitHub observation;
- real polling;
- remote fetch;
- sandbox creation;
- experimental repository/ref creation;
- experimental push;
- P5-D4 real-state mutation;
- Stage A;
- Stage B;
- promotion or publication;
- Vault mutation;
- CURRENT mutation;
- daemon registration;
- Scheduled Task registration;
- Windows Service registration;
- startup registration;
- P6;
- REAL P5-E.

```text
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED
```

## Persistence authority

The only operations authorized by the human adoption statement are:
- persist this human-adoption record;
- commit it;
- push it;
- verify final local/remote repository consistency;
- STOP.

This record persists pre-existing human authority. It does not create or enlarge that authority.

No classifier, test, qualification, P5-E artifact, P5-D4 artifact, control state, Vault/CURRENT artifact, or future RPE artifact may be modified by this persistence step.
