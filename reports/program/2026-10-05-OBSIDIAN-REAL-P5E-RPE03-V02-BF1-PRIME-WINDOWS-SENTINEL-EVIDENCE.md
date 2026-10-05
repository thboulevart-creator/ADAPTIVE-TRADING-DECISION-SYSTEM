# RPE-03 V0.2 — BF-1 PRIME WINDOWS POSITIVE-SENTINEL EVIDENCE

Date: 2026-10-05

A temporary fake git.exe was compiled inside a temporary directory. If executed, it writes a unique sentinel file and exits with code 7.

Observed control:

CONTROL_IMPLICIT_RC = 7
CONTROL_SENTINEL_CREATED = TRUE

The same temporary directory and fake executable remained present for the final candidate classification.

Observed final candidate:

FINAL_CLASSIFICATION = FAST_FORWARD
FINAL_SENTINEL_CREATED = FALSE

Interpretation:
- implicit Windows executable search executed the temporary fake git.exe in the control path;
- the final RPE-03 V0.2 candidate did not execute that fake executable;
- the classifier used the governed absolute Git executable and produced the expected FAST_FORWARD result;
- no write occurred in Program Files, the Python installation directory, or a system directory.

This evidence is specific to direct classifier executable binding. It does not qualify the downstream Git-for-Windows helper chain.
