# RPE-01 — FINAL PORTABILITY + RAW-BREAKER DISCRIMINATION — RED EVIDENCE

Date: 2026-10-03

## Preregistered predecessor

HEAD:
`cee9f7e4c46a9cef28891561c63e112d81cc3744`

Preregistration blob:
`3fbd871ac3faeaab8d40c730ac539677ac272c33`

Final delta-review return blob:
`d5ce7aa73a070610a2a56c04647c426cff7d1249`

Normative depth bound preregistered before RED:

`MAX_GOVERNED_JSON_DEPTH = 64`

Definition:
maximum syntactic nesting of JSON containers outside strings, with a root object or array at depth 1.

## RED test

`tests/obsidian_projection/test_rpe01_final_portability_raw_breaker_hardening_v0_1.py`

Written before any guard modification.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_rpe01_final_portability_raw_breaker_hardening_v0_1
```

## Observed result

```text
Ran 14 tests in 0.064s

FAILED
failures = 2
errors = 4

FINAL_HARDENING_RED_EXIT = 1
```

Eight tests passed and six produced the required RED signal.

## NB-a RED signals

Observed before patch:

1. `MAX_GOVERNED_JSON_DEPTH` does not exist.
2. Document JSON at syntactic depth 65 is accepted by `parse_json_strict`.
3. Valid governed schema JSON at syntactic depth 65 is accepted by `parse_schema_json_strict`.
4. Forced `RecursionError` from `_validate_schema_node` escapes `validate_schema_definition`.
5. Forced `RecursionError` from `_validate_document_node` escapes the public `validate_governed_json` boundary.
6. The depth-65 breaker cannot kill a depth-guard mutant because no deterministic depth guard exists yet.

The exact boundary fixtures self-check:
- document depth 64;
- document depth 65;
- schema depth 64;
- schema depth 65.

No interpreter recursion threshold is used as normative evidence.

## NB-b baseline signals

The following real-contract/raw-schema breakers already reject for the intended strict-parser reason:

- contradictory duplicate real key `evaluation_authorized`;
- escaped duplicate of `evaluation_authorized`;
- `NaN` at real field `poll_interval_seconds`;
- `Infinity` at real field `detection_latency_seconds_max`;
- `-Infinity` at real field `detection_latency_seconds_max`;
- duplicate `artifact_role` in the otherwise-valid governed schema.

Targeted mutant checks already demonstrate:
- disabling duplicate-member detection allows the real-contract duplicate authority breaker to survive;
- disabling the non-standard constant parser hook removes the parser-specific NaN rejection signal.

These passing RED-baseline tests are expected; NB-b hardening focuses on incorporating these discriminating families into the final sweep/evidence partition.

## Authority boundary

No adopted contract/model/runtime was modified during RED.

`RPE-02 = CLOSED`

`RPE-03 = CLOSED`

`REAL_P5E = CLOSED`
