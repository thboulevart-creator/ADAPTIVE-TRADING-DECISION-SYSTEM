# RPE-03 V0.2 — BF-1 PRIME EXECUTABLE IDENTITY CLOSURE — RED

Date: 2026-10-05

Status: RED CONFIRMED / TEST-FIRST

Preregistration HEAD:
d91d7d373b631e887c087ef6558e507e2c7187f9

Frozen RED test blob:
984249ee982d652678517707c3f683a8acd57d44

Observed result:
- 4 tests executed
- 4 failures
- exit = 1

Observed failures:
1. bare git.exe is accepted when cwd resolves it to the governed file;
2. .\\git.exe is accepted in the same condition;
3. classify_transition(repo, A, B, "git.exe") returns FAST_FORWARD instead of UNKNOWN;
4. _run_git receives argv[0] = git.exe instead of the governed absolute path.

This reproduces BF-1 PRIME against the current V0.2 candidate before correction.

No RPE-03 ancestry semantics were changed to produce this RED.
RPE-04 remains blocked.
RPE-05, RPE-06 and REAL P5-E remain CLOSED.
