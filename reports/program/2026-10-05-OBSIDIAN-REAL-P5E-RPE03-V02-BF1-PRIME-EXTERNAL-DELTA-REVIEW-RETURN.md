# RPE-03 V0.2 — BF-1 PRIME EXTERNAL DELTA REVIEW RETURN

Date: 2026-10-05

## Verdict

VERDICT = FAIL

BF-1 PRIME = ACCEPTED AS BLOCKING

## Blocking finding

The V0.2 classifier verifies a resolved executable path but _run_git executes the raw caller-supplied string.

Therefore a relative or bare value such as git.exe can be resolved during verification to the governed executable while later being resolved by subprocess executable search to a different executable.

Observed Linux analogue supplied by the external reviewer:
- absolute governed path on a true rollback: NON_FAST_FORWARD;
- _verify_governed_git_executable("git.exe"): True;
- classify_transition(repo, B, A, "git.exe"): FAST_FORWARD.

This demonstrates that VERIFIED EXECUTABLE and ACTUALLY EXECUTED EXECUTABLE are not identical for non-absolute caller input.

## Required correction

The classifier must:
1. reject non-absolute supplied executable strings;
2. resolve the supplied absolute path strictly;
3. require equality with the governed canonical executable;
4. verify SHA-256;
5. verify exact version;
6. verify minimum version;
7. return the verified canonical absolute path;
8. execute only that verified canonical path in every Git subprocess.

The raw caller string must not be reused after validation.

## Non-blocking findings

NB-1 = TOCTOU note, non-blocking in current threat model.
NB-2 = exact-version plus minimum-version redundancy, accepted.
NB-3 = Windows falsification evidence should use a positive sentinel.
NB-4 = previous harness correction accepted.
NB-5 = V0.1 packet copy newline/provenance note accepted.

## Scope

RPE-03 V0.2 = NOT READY FOR HUMAN ADOPTION
RPE-04 = BLOCKED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

This review creates no authority.
