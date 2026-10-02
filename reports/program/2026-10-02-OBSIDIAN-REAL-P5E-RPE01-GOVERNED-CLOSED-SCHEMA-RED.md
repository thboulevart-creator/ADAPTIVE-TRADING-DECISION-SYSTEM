# RPE-01 — N4 GOVERNED CLOSED SCHEMA — RED EVIDENCE

Date: 2026-10-02

## Preregistered predecessor

HEAD:
`0c6089b56a438a3faad23af20216f9666685ba0f`

Preregistration blob:
`406e67da3ab197c5a9ae4b3e971368549af6e1da`

## RED test

`tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py`

Created before:
- `tools/obsidian_projection/rpe01_governed_closed_schema.py`;
- `tools/obsidian_projection/p5e_v0_1_governed_schema_v0_1.json`.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_rpe01_governed_closed_schema_v0_1
```

## Observed result

```text
Ran 19 tests in 0.016s

FAILED (failures=20)

RED_EXIT=1
```

The failure count exceeds the test count because one test contains multiple failing subtests.

## Important RED signal

One test intentionally PASSED:

`ExistingGapEvidenceTests.test_existing_p5e_invariants_do_not_close_unknown_keys`

It inserted:

`authority_boundary.rpe01_probe_unknown_authority = true`

into an in-memory copy of the adopted P5-E contract.

The existing semantic invariant checker accepted that mutated object.

This demonstrates the exact N4 gap independently of P5-E contract blob binding.

## RED failures

All new RPE-01 guard capabilities failed because the guard module and concrete governed schema did not yet exist.

The RED covers:

- duplicate raw JSON members;
- nested duplicates;
- NaN / ±Infinity;
- strict integer/boolean distinction;
- float/scientific-float rejection where integer is required;
- enum closure;
- list uniqueness;
- normative list order;
- adjacent config unknown authority/environment/CLI override keys;
- schema-language unknown keys;
- schema-language wrong types;
- unsupported schema node kinds;
- P5-E contract exact object-depth closure;
- missing required keys;
- concrete normative-list closure;
- guard purity / no implicit authority channels.

## Authority boundary

No runtime, adopted contract, adopted synthetic model, P5-D4 state, Vault or CURRENT artifact was modified.

`REAL_P5E = CLOSED`
