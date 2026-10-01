# P5-E V0.1 — REQUIREMENT / EVIDENCE MATRIX RED

Date: 2026-10-01

## Scope

Test-first evidence for the explicit P5-E requirement-to-executable-proof matrix required by the targeted closure preregistration.

## RED test

`tests/obsidian_projection/test_p5e_requirement_evidence_matrix_v0_1.py`

The test was created before the matrix artifact.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_p5e_requirement_evidence_matrix_v0_1
```

## Observed result

```text
Ran 5 tests in 0.005s

FAILED (failures=1, errors=4)

MATRIX_RED_EXIT=1
```

All failures are caused by the intentionally absent matrix:

`tools/obsidian_projection/p5e_v0_1_requirement_evidence_matrix.json`

## Required matrix properties

The matrix must:

- map all 10 required synthetic cases;
- map all 25 base breakers;
- map all 8 targeted-closure breakers;
- contain no unmapped or deferred requirement;
- bind every mapping to an existing executable test path;
- bind every mapping to the exact Git blob of that test file;
- name a real test method present in that file;
- distinguish direct P5-E evidence from reused qualified P5-D2/P5-D4 evidence;
- preserve `REAL_P5E = CLOSED`;
- make no real 60-second SLA claim;
- make no per-transient-tip detection SLA claim;
- grant no evaluation, promotion, or publication authority.

The next step is creation of the minimal matrix satisfying this already-persisted test.
