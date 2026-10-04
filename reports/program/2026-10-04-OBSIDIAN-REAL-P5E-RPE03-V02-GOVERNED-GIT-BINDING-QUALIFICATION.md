# RPE-03 V0.2 — GOVERNED GIT EXECUTABLE BINDING — QUALIFICATION

Date: 2026-10-04

## Result

RPE-03 V0.2 = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

This is not human adoption.

## Blocker addressed

BF-1 from the RPE-04 external review required:

VERIFIED GIT EXECUTABLE
=
ACTUALLY EXECUTED ANCESTRY CLASSIFIER GIT EXECUTABLE

V0.1 remains immutable and historically adopted.

V0.2 adds only explicit governed Git executable binding.

## Governed Git identity

Absolute path:
C:\Program Files\Git\cmd\git.exe

SHA-256:
81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5

Observed version:
git version 2.54.0.windows.1

Minimum qualified version:
2.54.0

The classifier rejects:
- any other supplied path;
- SHA mismatch;
- observed-version mismatch;
- version below minimum.

Every Git command issued by V0.2 uses the supplied path only after it has matched the preregistered governed identity.

## Windows falsification

A controlled fake git.exe was placed in the process current directory.

Implicit ["git", "--version"]:
- selected the fake executable;
- return code = 1;
- did not return the governed Git version.

Absolute governed Git:
- return code = 0;
- returned git version 2.54.0.windows.1.

The V0.2 test confirms correct ancestry classification with the fake executable present because the absolute governed path is used.

## Evidence

Targeted V0.2:
8/8 PASS

Targeted mutation tests:
4/4 PASS

RPE-04 call-site compatibility harness:
1/1 PASS

Complete RPE-03 V0.1 + V0.2 regression:
51/51 PASS

RPE-03 V0.1 classifier remains:
145b3112fd9309cc34d95a62c091cb6a6bc3bb11

RPE-01 guard remains:
26f977961d72a062199d71ffd628d5a5cc047887

## Semantic immutability

The transition vocabulary remains:

INITIAL
SAME
FAST_FORWARD
NON_FAST_FORWARD
UNKNOWN

Missing object, non-commit, invalid domain, shallow/graft/alternate domain, unexpected merge-base exit, timeout and corruption remain fail-closed to UNKNOWN.

## Claim boundary

This qualification binds the executable directly launched by the classifier.

It does not claim qualification of the entire downstream Git-for-Windows helper executable chain.

It does not rebind RPE-04 yet.

It does not close RPE-04 BF-1 until V0.2 is externally reviewed and human-adopted, then RPE-04 is rebound.

NF-2 and NF-3 remain open in RPE-04.

RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

Next gate:
EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADOPTION
