# RPE-03 V0.2 — BF-1 PRIME TEST-HARNESS CORRECTIONS

Date: 2026-10-05

Two test-harness corrections occurred during the authorized BF-1 PRIME closure.

1. The first positive-sentinel helper embedded C# directly inside a PowerShell command string and failed because of quoting. The helper was corrected to write the C# source to a temporary .cs file and invoke Add-Type -Path. No implementation change was made for this failure and no expected security verdict changed.

2. Four pre-existing V0.2 mutation tests used exact source anchors from the pre-BF-1-PRIME implementation. After the implementation changed bool-return branches from False to canonical-path-return branches using None, and changed the subprocess argv to str(resolved), those source anchors no longer existed. Only the mutation anchor strings were updated; their failure modes and expected verdicts were unchanged.

Historical RED evidence remains preserved at its original commit and blob identities. These harness corrections do not rewrite that history.
