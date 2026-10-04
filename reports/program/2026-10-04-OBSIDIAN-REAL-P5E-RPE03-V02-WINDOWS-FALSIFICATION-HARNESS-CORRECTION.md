# RPE-03 V0.2 — WINDOWS FALSIFICATION HARNESS CORRECTION — INTERNAL ADJUDICATION

Date: 2026-10-04

The frozen targeted RED test attempted to create a fake git.exe by copying sys.executable.

On this Windows host, Python resolves through WindowsApps and shutil.copy2(sys.executable, ...) fails with WinError 1920 before the executable-search falsification can run.

This is a test-fixture defect, not an implementation finding.

Authorized correction under the existing V0.2 authorization:
- replace the fake executable source only;
- use an accessible inert Windows executable copied as git.exe;
- preserve the same executable-search falsification;
- preserve the same expected security verdict;
- make no implementation change to satisfy the harness.

The corrected test must still prove:
1. implicit subprocess execution of "git" can select the fake executable from the process current directory;
2. RPE-03 V0.2 uses the governed absolute Git path and therefore ignores that fake executable.
