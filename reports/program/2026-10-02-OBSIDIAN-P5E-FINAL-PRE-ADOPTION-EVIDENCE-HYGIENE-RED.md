# P5-E V0.1 — FINAL PRE-ADOPTION EVIDENCE HYGIENE — RED

Date: 2026-10-02

## Scope

Targeted RED for the authorized delta-only hygiene pass N1 / N2 / N6.

Base adjudication HEAD:
`4f280938a0f1bbc569aabffe0dc92daa31f37ae1`

## RED test

`tests/obsidian_projection/test_p5e_final_pre_adoption_evidence_hygiene_v0_1.py`

Created before any contract or evidence-matrix correction.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_p5e_final_pre_adoption_evidence_hygiene_v0_1
```

## Observed result

```text
Ran 6 tests in 0.012s

FAILED (failures=3, errors=1)

RED_EXIT=1
```

Interpretation:

- N1 behavioral runtime case already passes:
  `READ_COMPLETION_PRECEDES_ATTEMPT_START`;
- N1 explicit contract field is absent;
- N1 strict invariant guard is absent;
- N2 still labels the two newly introduced D2-file tests as
  `REUSED_QUALIFIED_P5D2_P5D4`;
- N6 stale `built_against_head` remains present;
- covered contract/model blob authority remains present and valid.

## Authority

No runtime model behavior was changed by this RED.

No full Obsidian suite was executed.

No real P5-E operation was executed.

`REAL_P5E = CLOSED`
