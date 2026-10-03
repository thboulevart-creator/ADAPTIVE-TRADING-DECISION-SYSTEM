# RPE-01 — NB-1 / NB-2 TARGETED CLOSURE — RED EVIDENCE

Date: 2026-10-03

## Opening identity

Branch:
`feat/obsidian-projection-rpe01-governed-closed-schema-v0.1`

Opening HEAD:
`c9e8ad98aeee6b4ae9346dac554fc599abfe1a8b`

External review:
`PASS_WITH_NON_BLOCKING_NOTES`

External review blob:
`51b168dd9973b748e8e592093dc16497d2a42301`

Internal adjudication blob:
`b6bf8eabfeefff2e264ae0b0d957b1492d2a0c5a`

Guard blob before targeted closure:
`3f61b9191e0ee7fb8c18fdecf60f45c586c74629`

## RED test

`tests/obsidian_projection/test_rpe01_external_review_targeted_closure_v0_1.py`

The test was written before modifying the guard.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_rpe01_external_review_targeted_closure_v0_1
```

## Observed result

```text
Ran 6 tests in 0.043s

FAILED (failures=2, errors=3)

TARGETED_RED_EXIT=1
```

One test passed; five produced the required RED signal.

## NB-1 reproduced

Observed before patch:

1. A legitimate raw schema passed directly to `validate_governed_json` fails because the API expects an already parsed object.
2. A permissively pre-parsed schema object is accepted by `validate_governed_json`.
3. The parsed-object helper `validate_document` remains publicly exposed.
4. The raw duplicate-schema-member attack is already rejected when strict raw parsing is actually used.

Therefore the defect is specifically the public API path allowing a parsed schema object.

## NB-2 reproduced

Observed before patch:

### Pathological integer

A JSON integer containing 5000 digits raises:

`ValueError`

from Python's integer-string conversion limit.

It is not normalized to:

`GovernedSchemaError`

### Pathological nesting

A JSON array nested 5000 levels deep raises:

`RecursionError`

from the JSON decoder.

It is not normalized to:

`GovernedSchemaError`

Both behaviors remain fail-closed in effect but violate the guard's intended single exception contract.

## Targeted correction boundary

The RED authorizes only the already-adjudicated minimal closure:

- public `validate_governed_json(document_raw, schema_raw)`;
- reject parsed schema objects at the public boundary;
- remove/privatize the parsed document/schema bypass;
- normalize `ValueError` and `RecursionError` into `GovernedSchemaError`;
- update existing RPE-01 tests/sweep to use raw schema input;
- correct NB-6/NB-7 evidence hygiene.

No semantic P5-E contract/model/runtime modification is authorized.

`RPE-02 = CLOSED`

`REAL_P5E = CLOSED`
