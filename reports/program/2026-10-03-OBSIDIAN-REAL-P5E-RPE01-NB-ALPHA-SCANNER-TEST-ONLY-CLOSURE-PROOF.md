# RPE-01 — NB-α SCANNER STRING/ESCAPE TEST-ONLY CLOSURE — PROOF

Date: 2026-10-03

## Result

```text
NB-α
= TEST-LOCKED_CANDIDATE

GUARD CODE CHANGE
= NONE

MAX_GOVERNED_JSON_DEPTH
= 64 UNCHANGED

RPE01_HUMAN_ADOPTION
= PENDING

RPE-02
= CLOSED

RPE-03
= CLOSED

REAL_P5E
= CLOSED
```

## Opening identity

Opening HEAD:

`d52805e1d3ec8491e2feea214be031cb098e077a`

Final guard at opening:

`26f977961d72a062199d71ffd628d5a5cc047887`

P5-E governed schema:

`87e45cc75753439879e2902d3cbdbd5d71d8a1b2`

The external review preceding this closure returned:

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

with:

`BLOCKING_FINDINGS = NONE`

and:

`RPE01_ADOPTION_READINESS = YES`.

The remaining requested proof gap was NB-α: the scanner's string/escape branches were correct in code but not explicitly test-locked.

## Authorized scope

This closure is test-only.

No guard modification was permitted unless a newly added test demonstrated that the current guard violated the already-claimed behavior.

The current guard passed the final tests, therefore:

`GUARD MODIFICATION = NOT REQUIRED`

## New test artifact

`tests/obsidian_projection/test_rpe01_nb_alpha_scanner_string_escape_closure_v0_1.py`

Pre-commit worktree Git blob:

`a170019180579f82e9f9ea0918f4fed445cab1ba`

The file contains four tests covering two properties plus two mutation kills.

## Property 1 — container characters inside a real governed string

The test starts from the adopted P5-E contract and changes only:

`objective.purpose`

to a valid JSON string containing:

```text
"[" repeated 100 times
```

This is greater than:

`MAX_GOVERNED_JSON_DEPTH = 64`

The otherwise-valid contract is validated through:

`validate_governed_json(raw_document, raw_schema)`

Observed:

`PASS`

Therefore JSON container characters inside a string do not consume the syntactic depth budget.

### in_string mutant

A source-level in-memory mutant neutralizes only the branch that enters string state:

```text
if char == '"':
    in_string = True
```

The same real-contract property then fails.

Observed:

`MUTANT KILLED`

An initial symmetric candidate fixture using balanced `[]{}` pairs did not discriminate the mutant because openings and closings cancelled numerically. That fixture was not persisted. The final persisted test uses 100 opening brackets and is discriminating.

## Property 2 — escaped quote cannot hide real depth

The adversarial raw document is valid JSON and contains:

1. a string containing an escaped quote;
2. close-bracket characters after that escaped quote while still inside the string;
3. a later branch with real JSON container depth 67.

With the qualified scanner:

```text
REAL DEPTH > 64
→ GovernedSchemaError
→ reason contains "maximum governed JSON depth"
```

Observed:

`PASS`

### escaped-state mutant

A source-level in-memory mutant neutralizes only:

```text
elif char == "\\":
    escaped = True
```

This causes the scanner to leave the string incorrectly after the escaped quote and under-count the later real depth.

The same adversarial property no longer detects the depth violation.

Observed:

`MUTANT KILLED`

Therefore the persisted test discriminates the `escaped` branch and specifically guards against the fail-open case identified by the external reviewer.

## Test results

Dedicated NB-α closure:

```text
4 / 4 PASS
```

Current RPE-01 surface:

```text
46 / 46 PASS
```

P5-E + complete current RPE-01 targeted regression:

```text
113 / 113 PASS
```

## Protected artifact integrity

Relative to the adopted readiness base:

```text
RPE-01 guard worktree diff
= 0

P5-E contract diff
= 0

P5-E synthetic model diff
= 0

P5-D4 runtime diff
= 0
```

The guard remains exactly:

`26f977961d72a062199d71ffd628d5a5cc047887`

The depth bound remains:

`MAX_GOVERNED_JSON_DEPTH = 64`

## NB-β / NB-c consumer check

Static search over runtime Python files under `tools/`, excluding the guard module itself:

```text
private guard function runtime consumers
= 0

validate_governed_json runtime consumers
= 0
```

The absence of a runtime consumer is expected because RPE-02/RPE-03 remain unopened.

Tests may call `validate_schema_definition` directly to test schema-language behavior; this is not a runtime governed-document consumer.

The carried consumer contract remains:

```text
AUTHORIZED GOVERNED-ARTIFACT ENTRYPOINT
= validate_governed_json(raw_document, raw_schema)

underscore-prefixed guard functions
= forbidden to external runtime consumers

validate_schema_definition
= not an authorized governed-document validation entrypoint
```

This rule must be carried into RPE-02/RPE-03 preregistration.

## Real P5-D4 state integrity

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Maximum claim

```text
NB-α
= TEST-LOCKED_CANDIDATE

IN_STRING MUTANT
= KILLED

ESCAPED-STATE MUTANT
= KILLED

RPE01 TECHNICAL SURFACE
= READY_FOR_HUMAN_ADJUDICATION

RPE01 HUMAN ADOPTION
= NOT AUTOMATIC

RPE-02
= CLOSED

RPE-03
= CLOSED

REAL_P5E
= CLOSED
```

This proof creates no authority beyond the user-authorized test-only closure.

STOP before human adoption.
