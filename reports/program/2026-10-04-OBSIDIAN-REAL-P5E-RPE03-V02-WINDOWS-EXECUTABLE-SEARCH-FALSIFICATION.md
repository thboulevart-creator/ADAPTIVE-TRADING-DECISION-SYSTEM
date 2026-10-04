# RPE-03 V0.2 — WINDOWS EXECUTABLE SEARCH FALSIFICATION EVIDENCE

Date: 2026-10-04

Environment:
- Windows host
- governed Git: C:\Program Files\Git\cmd\git.exe
- governed Git version: git version 2.54.0.windows.1

Controlled falsification:
- a temporary fake git.exe was created by copying C:\WINDOWS\System32\where.exe;
- the process current directory was changed to the temporary directory;
- an implicit subprocess invocation ["git", "--version"] was executed;
- in the same process context, the governed absolute Git path was executed directly.

Observed output:

FAKE_SOURCE = C:\WINDOWS\System32\where.exe
IMPLICIT_RC = 1
IMPLICIT_STDOUT = empty
IMPLICIT_STDERR = empty
ABSOLUTE_RC = 0
ABSOLUTE_STDOUT = git version 2.54.0.windows.1

Interpretation:
- the implicit token "git" did not execute the governed Git binary, because the governed binary returns rc=0 and the exact version string;
- the controlled fake executable won implicit Windows executable resolution from the process current directory;
- absolute execution of C:\Program Files\Git\cmd\git.exe remained bound to the governed binary in the same context.

The targeted V0.2 test additionally verifies that ancestry classification still returns the correct transition while the fake git.exe is present because V0.2 uses the absolute governed path.

This evidence closes the Windows-search falsification requirement for the V0.2 candidate only. It does not adopt V0.2.
