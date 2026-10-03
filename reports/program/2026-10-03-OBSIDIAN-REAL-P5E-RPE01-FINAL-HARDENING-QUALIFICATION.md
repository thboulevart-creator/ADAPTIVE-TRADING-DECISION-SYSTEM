# RPE-01 — FINAL PORTABILITY + RAW-BREAKER DISCRIMINATION — QUALIFICATION

Date: 2026-10-03

## Result

```text
RPE01_FINAL_HARDENING
= QUALIFIED_FOR_FINAL_EXTERNAL_DELTA_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE-02
= CLOSED

RPE-03
= CLOSED

REAL_P5E
= CLOSED
```

## Purpose

This is the final technical hardening pass requested after the independent review returned:

`PASS_WITH_NON_BLOCKING_NOTES`

with no blocker.

It closes only:
- NB-a — deterministic depth / recursion portability;
- NB-b — discriminating raw breakers;
- NB-c — consumer usage rule clarification.

No adopted P5-E contract, synthetic model or P5-D4 runtime was changed.

## Preregistration

Opening HEAD:
`cbe8b2534e3a4f65edbe1732a5b322e018756713`

Preregistration HEAD:
`cee9f7e4c46a9cef28891561c63e112d81cc3744`

Preregistration blob:
`3fbd871ac3faeaab8d40c730ac539677ac272c33`

The deterministic bound was frozen before RED:

```text
MAX_GOVERNED_JSON_DEPTH = 64
```

Definition:

maximum syntactic nesting of JSON containers outside JSON strings, with the root object/array at depth 1.

Current protected artifacts are far below the bound:

```text
P5-E adopted contract max depth = 3
P5-E governed schema max depth = 8
```

These current-depth observations are non-normative.

## RED

RED HEAD:
`6327333ba27b551ac7c1fcda20fafe3eb488749f`

RED test:
`449898e62f244a275af290559b7441af1798ee09`

RED report:
`33f6f1bea040bddcb452657319e87f90bca9ed54`

Observed before patch:

```text
Ran 14 tests

FAILED
failures = 2
errors = 4

8 tests already passed
6 tests produced the required RED signal
```

The RED did not use an interpreter recursion threshold as evidence.

## NB-a closure

Final guard:

`26f977961d72a062199d71ffd628d5a5cc047887`

The guard now pre-scans raw JSON before `json.loads`.

It tracks container nesting while ignoring braces/brackets inside JSON strings and honoring backslash escapes.

Policy:

```text
depth <= 64
→ depth guard permits parsing

depth > 64
→ GovernedSchemaError
```

The same parser boundary is used for:
- governed documents;
- governed schemas.

Portable exact-boundary tests demonstrate:

```text
document depth 64 → allowed by depth guard
document depth 65 → GovernedSchemaError

schema depth 64 → valid / accepted
schema depth 65 → GovernedSchemaError
```

Residual recursion is also normalized:
- `validate_schema_definition` converts residual `RecursionError`;
- public `validate_governed_json` converts residual document-validation `RecursionError`.

Dedicated tests force recursion failures inside:
- `_validate_schema_node`;
- `_validate_document_node`.

Both emerge as `GovernedSchemaError`.

Therefore the normative property no longer depends on whether a particular Python JSON decoder accepts 5000 nested containers.

The old 5000-level test was replaced by:

`MAX_GOVERNED_JSON_DEPTH + 1`.

## Qualification environment

The final local qualification ran under:

```text
Python
= 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)]

Implementation
= CPython

Platform
= Windows-11-10.0.22631-SP0
```

This environment is evidence context only.

It is not part of the depth semantics.

## NB-b closure — discriminating raw breakers

The parsed-object sweep remains:

```text
433 attempted
0 survivors
```

The seven raw breakers are now built from otherwise-valid governed artifacts and require the intended parser rejection reason.

They are:

1. contradictory duplicate `evaluation_authorized`;
2. escaped duplicate spelling of `evaluation_authorized`;
3. duplicate real numeric `poll_interval_seconds`;
4. NaN injected into real `poll_interval_seconds`;
5. Infinity injected into real `detection_latency_seconds_max`;
6. -Infinity injected into real `detection_latency_seconds_max`;
7. duplicate `artifact_role` in the otherwise-valid raw P5-E schema.

Observed:

```text
RAW BREAKERS = 7
SURVIVORS = 0
```

The breaker no longer passes merely because a dummy key such as `x` is structurally unknown.

## Mutation-kill evidence

Three targeted mutants were exercised:

### Duplicate-member mutant

Protection:
`object_pairs_hook=_strict_object`

Mutant:
duplicate detection replaced by normal dictionary construction.

Result:
the contradictory real `evaluation_authorized` document becomes structurally accepted.

`MUTANT = KILLED`

### Non-standard-constant mutant

Protection:
`parse_constant=_reject_constant`

Mutant:
NaN is allowed through JSON parsing.

Result:
the later schema still fails closed on integer type, but the required parser-specific NaN rejection disappears.

`MUTANT = KILLED`

### Deterministic-depth mutant

Protection:
`_enforce_max_json_depth`

Mutant:
depth guard replaced by no-op.

Result:
depth-65 JSON parses.

`MUTANT = KILLED`

Summary:

```text
MUTATION-KILL CHECKS = 3
KILLS = 3
SURVIVORS = 0
```

## NB-c usage rule

The governed consumer rule is:

```text
AUTHORIZED GOVERNED-ARTIFACT VALIDATION ENTRYPOINT
= validate_governed_json(raw_document, raw_schema)
```

For future RPE consumers:
- underscore-prefixed guard functions are forbidden;
- `validate_schema_definition` is not a governed-document validation entrypoint;
- callers must not use it as a document-validation bypass.

A repository search over `tools/`, excluding the guard module itself, found no runtime consumer of:
- `validate_schema_definition`;
- `_validate_document`;
- `_validate_document_node`;
- `_validate_schema_node`.

RPE-02/RPE-03 remain unopened, so no future runtime consumer exists yet.

## GREEN

Final hardening tests:

```text
14 / 14 PASS
```

Current RPE-01 surface:

```text
42 / 42 PASS
```

Final evidence partition:

```text
PARSED-OBJECT MUTATIONS = 433
RAW-JSON BREAKERS       = 7
RAW SURVIVORS           = 0

MUTATION-KILL CHECKS    = 3
MUTATION KILLS          = 3
MUTATION SURVIVORS      = 0
```

## Final targeted regression

P5-E qualification surface + all RPE-01 tests:

```text
109 / 109 PASS
```

Protected artifact deltas from the adopted readiness base:

```text
P5-E CONTRACT = 0
P5-E MODEL = 0
P5-D4 RUNTIME = 0
```

## Remaining non-blocking scope

Unchanged:

- NB-3: RPE-01 is structural/type/list governance; adopted P5-E invariants retain value semantics.
- NB-4: generic source binding is structurally represented but not dynamically enforced by the generic guard.
- NB-5: contradictory restrictive constraints, ASCII-regex policy and isolated-surrogate handling remain future hardening where relevant.

None of these is claimed closed by this final hardening.

## Real-state integrity

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Final candidate identities

```text
GUARD
= 26f977961d72a062199d71ffd628d5a5cc047887

P5-E GOVERNED SCHEMA
= 87e45cc75753439879e2902d3cbdbd5d71d8a1b2

MAIN RPE-01 TEST
= cd0e091233e5a4473ef280c7061db8cf880169e9

MUTATION SWEEP
= b37ca3e31aecde1beccf08eafe04696e6a7dc4c9

PORTABLE NB1/NB2 TEST
= f52b88a9d56ea12a515e35ad8e915d0a1bc28b91

FINAL HARDENING TEST
= 449898e62f244a275af290559b7441af1798ee09
```

## Maximum claim

```text
NB-a
= CLOSED_CANDIDATE

NB-b
= CLOSED_CANDIDATE

NB-c
= USAGE_RULE_DEFINED

RPE01_FINAL_HARDENING
= QUALIFIED_FOR_FINAL_EXTERNAL_DELTA_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE-02
= CLOSED

RPE-03
= CLOSED

REAL_P5E
= CLOSED
```
