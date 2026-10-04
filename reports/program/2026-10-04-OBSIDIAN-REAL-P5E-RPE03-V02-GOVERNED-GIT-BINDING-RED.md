# RPE-03 V0.2 — GOVERNED GIT EXECUTABLE BINDING — TARGETED RED

Date: 2026-10-04

Status: RED CONFIRMED / TEST-FIRST

Preregistration HEAD:
6de09282b4a97371d662f8871b3e34d2bb7ee9f0

Targeted RED test blob:
3a3947c6b75038644f84900d8c01a6ce91a360e1

Observed result:
- 8 tests executed
- 8 failures
- reason: rpe03_ancestry_classifier_v0_2.py does not exist
- exit = 1

Covered requirements:
- explicit governed executable parameter;
- absolute executable use;
- wrong path fail-closed;
- wrong SHA fail-closed;
- version below minimum fail-closed;
- identity constants;
- unchanged transition vocabulary/semantics;
- Windows implicit executable-search falsification.

RPE-03 V0.1 remains unchanged.
RPE-04 remains blocked pending adopted RPE-03 V0.2.
RPE-05, RPE-06 and REAL P5-E remain CLOSED.
