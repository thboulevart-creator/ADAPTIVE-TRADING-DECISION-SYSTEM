# RPE-04 — RPE-03 V0.2 REBIND + NF-2 + NF-3 — TARGETED RED

Date: 2026-10-05

Preregistration HEAD:
1ba14c2d89904c51b6766a686f4249cca3b6b7ee

## RPE-03 V0.2 rebind + NF-2

Test:
tests/obsidian_projection/test_rpe04_rpe03v02_rebind_nf2_v0_1.py

Blob:
49540da4a64c25febe0bec26edbf0ce768193551

Observed:
- 5 tests
- 1 PASS
- 4 FAIL
- no ERROR

Confirmed RED findings:
- runtime binding still targets rpe03_ancestry_classifier_v0_1.py;
- RPE-03 call site supplies only 3 arguments, not governed Git path;
- annotated tag object is peeled to its contained commit and accepted as OBSERVED_REMOTE_TIP;
- exact local observation ref identity is not preserved because ^{commit} changes tag object ID to peeled commit ID.

Healthy control:
- normal commit ref remains a valid OBSERVED_REMOTE_TIP.

## NF-3 full physical Git domain

Test:
tests/obsidian_projection/test_rpe04_nf3_full_physical_domain_v0_1.py

Blob:
eadddb42e5806c57d95737965ba501dbe427722c

Observed:
- 7 tests
- 1 PASS
- 6 FAIL
- no ERROR

Confirmed RED findings:
- refs indirection not checked;
- refs/rpe04 indirection not checked;
- config / HEAD / packed-refs indirection not checked;
- objects/info/alternates presence not rejected by RPE-04 physical-domain verifier;
- pack-file-level indirection is not inspected recursively;
- alternates introduced after fetch are not rejected by RPE-04 before positive observation.

Healthy control:
- normal bare observation domain is accepted.

No RPE-04 implementation change existed during these RED runs.

RPE-03 V0.2 remains HUMAN_ADOPTED.
RPE-04 HUMAN ADOPTION remains PENDING.
RPE-05, RPE-06 and REAL P5-E remain CLOSED.
