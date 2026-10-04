# RPE-04 — EXTERNAL ADVERSARIAL REVIEW RETURN

Date: 2026-10-04

Source: external Claude review returned by the human principal.

## Verdict

VERDICT = FAIL

RPE-04 tests were not independently executed by the reviewer because the package is Windows-bound. The reviewer replayed the exact Git command shape under Git 2.43/Linux, executed the physical-domain verifier extracted from the package, and tested the RPE-02 handoff of adapter failure events.

## Blocking finding

BF-1 — The Git executable whose identity is verified is not proven to be the Git executable actually used by RPE-03.

Observed code relationship:
- RPE-04 verifies C:\Program Files\Git\cmd\git.exe.
- RPE-03 V0.1 invokes the implicit executable token "git".
- On Windows, CreateProcess executable search can select a different git.exe before PATH.
- Therefore the binary producing FAST_FORWARD / NON_FAST_FORWARD is not bound to the verified binary.

Reviewer status: strong inference, not executed under Windows.

Required correction:
RPE-03 must execute an absolute governed Git executable path and tests must verify the actually launched binary.

## Non-blocking findings accepted for adjudication

NF-2 — Annotated-tag dereference can turn contained commit content into OBSERVED_REMOTE_TIP.
Correction: read exact ref without ^{commit}, then require exact object type == commit.

NF-3 — Physical containment covers objects paths but not the full authority-bearing bare repository domain. A redirected refs path can write outside the domain.
Correction: extend containment or create a fresh controlled domain and recursively reject indirections.

NF-4 — RPE-02 timing handoff is valid only for success paths; failure-event mapping is not yet a valid RPE-02 observation.

NF-5 — The hashed Git executable may be a launcher rather than the full executable chain.

NF-6 — Runtime binding has a small TOCTOU/import limitation; raw SHA-256 is environment/line-ending bound.

NF-7 — Pre-fetch checks occur before attempt_started_at_ns and therefore contribute to future RPE-05 scheduling delay.

NF-8 — Source identity checks are valid only for the local bare-remote qualification and do not transpose directly to GitHub.

NF-9 — Some qualification provenance uses abbreviated commit SHAs; full-SHA hygiene should be restored.

NF-10 — Mutation proof is indirect but acceptable with the main suite.

## Review conclusion

RPE04_ADOPTION_READINESS = NOT_READY

Recommended next action:
1. Targeted RPE-03 amendment binding the actually executed Git binary.
2. Then rebind RPE-04 and close BF-1, NF-2 and NF-3.
3. Carry NF-4 and NF-7 to RPE-05.
4. Use a Windows falsification test for BF-1 in the delta review.

This review creates no authority.

RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED
