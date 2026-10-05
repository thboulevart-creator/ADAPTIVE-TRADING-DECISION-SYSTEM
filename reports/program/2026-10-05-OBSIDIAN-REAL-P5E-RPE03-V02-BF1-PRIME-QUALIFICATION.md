# RPE-03 V0.2 — BF-1 PRIME VERIFIED/EXECUTED EXECUTABLE IDENTITY — QUALIFICATION

Date: 2026-10-05

## Result

RPE03_V02_DIRECT_CLASSIFIER_EXECUTABLE_BINDING
= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

This is not human adoption.

## BF-1 PRIME closure

The final candidate requires the caller-supplied executable string to be absolute.

The absolute input is strictly resolved, matched to the governed canonical Git path, SHA-256 verified, exact-version verified, minimum-version verified, and returned as the verified canonical executable.

Only that verified canonical executable is propagated into the ancestry-domain checks and Git subprocess calls.

The raw caller string is not reused after verification.

Internal _run_git additionally rejects non-absolute or non-governed executable paths.

## Governed identity

ABSOLUTE PATH
= C:\Program Files\Git\cmd\git.exe

SHA-256
= 81ef35ae005ca9318018d18e3327578ce939fb99feaad6b2d7c8ab15f3de8db5

OBSERVED VERSION
= git version 2.54.0.windows.1

MINIMUM VERSION
= 2.54.0

## Evidence

Historical BF-1 PRIME RED:
4/4 FAIL

Final BF-1 PRIME closure:
5/5 PASS

BF-1 PRIME mutations:
3/3 PASS

Updated prior V0.2 mutation harness:
4/4 PASS

Complete RPE-03 surface including V0.1, V0.2 and RPE-04 call-site compatibility:
59/59 PASS

## Windows positive-sentinel falsification

CONTROL / implicit executable search:
CONTROL_IMPLICIT_RC = 7
CONTROL_SENTINEL_CREATED = TRUE

FINAL CANDIDATE with the same fake git.exe present:
FINAL_CLASSIFICATION = FAST_FORWARD
FINAL_SENTINEL_CREATED = FALSE

Therefore the implicit search path can execute the temporary fake git.exe, while the final candidate does not execute it.

## Protected predecessors

RPE-03 V0.1 classifier remains:
145b3112fd9309cc34d95a62c091cb6a6bc3bb11

RPE-01 guard remains:
26f977961d72a062199d71ffd628d5a5cc047887

P5-E contract remains:
43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-D4 runtime remains:
1825e53d195ba2a63b5b646a5b78eb77939b94b5

The RPE-02 model is not present on this historical RPE-03 lineage, so no local blob comparison is claimed for it.

## Claim boundary

This candidate qualifies only the directly executed classifier Git executable.

It does not qualify the full Git-for-Windows helper executable chain.

The privileged Program Files replacement TOCTOU scenario remains outside the current threat model and is documented as non-blocking.

Exact-version and minimum-version checks remain intentionally redundant.

RPE-04 has not been rebound to this candidate.

RPE-04 NF-2 and NF-3 remain open.

RPE-03 V0.2 HUMAN ADOPTION = PENDING
RPE-04 = BLOCKED_PENDING_RPE03_V0.2
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

Next gate:
EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADOPTION
