# P5-E V0.1 — BB1 NORMATIVE GUARD COVERAGE — RED EVIDENCE

Date: 2026-10-02

## Scope

First RED execution after persistence of BB1 internal adjudication and preregistration.

Preregistration HEAD:
`64eb3b5aea96d2d8bb36114737c19489862f85f4`

Adjudication blob:
`32741174bd2ad845af4dbbfb664c38d887e181e9`

Preregistration blob:
`0f12b589fe1b74320732fb531936bf6e843653d9`

## RED test artifact

`tests/obsidian_projection/test_p5e_bb1_normative_guard_closure_v0_1.py`

The test was created before any contract/model/matrix correction.
## Command

```text
python -B -m unittest tests.obsidian_projection.test_p5e_bb1_normative_guard_closure_v0_1
```

## Observed result

```text
Ran 10 tests in 0.050s

FAILED (failures=6, errors=3)

RED_EXIT=1
```

One test passed:
- preregistration freezes the exact 23 normative and 13 non-normative leaf sets.

Nine tests were red as expected.
## RED families demonstrated

1. All 23 preregistered normative leaf mutations still survive the invariant checker.
2. The combined BB1 regression is still accepted.
3. Evidence matrix has no exact contract/model blob binding.
4. NB1 read overrun currently returns PASS instead of fail-closed.
5. NB4 future-adapter-rule fields are absent.
6. NB6 queue-capacity mappings point to declarative P5-E mutation tests rather than behavioral P5-D4 evidence.
7. NB6 pending non-active semantics are mapped to an active-evaluation test.
8. NB7 explicit `INCOMPLETE_SYNTHETIC_WINDOW` non-pass declaration is absent.
9. NB7 duplicate fixed-rate slot still returns `CADENCE_GAP`.

## Authority

No real P5-E execution occurred.

No P5-D4 runtime or real control state was modified.

`REAL_P5E = CLOSED`
