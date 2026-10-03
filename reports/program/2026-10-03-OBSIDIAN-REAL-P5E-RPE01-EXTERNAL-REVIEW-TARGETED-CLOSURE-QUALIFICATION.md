# RPE-01 — EXTERNAL REVIEW TARGETED CLOSURE — QUALIFICATION

Date: 2026-10-03

## Result

```text
RPE01_EXTERNAL_REVIEW_TARGETED_CLOSURE
= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE-02
= CLOSED

REAL_P5E
= CLOSED
```

## External-review origin

The first independent RPE-01 review returned:

`PASS_WITH_NON_BLOCKING_NOTES`

with:

`BLOCKING_FINDINGS = NONE`

The reviewer reproduced:
- 22/22 RPE-01 tests;
- 89/89 targeted P5-E + RPE-01 regression;
- 41 additional adversarial probes.

Two notes were adjudicated as targeted corrections required before human adoption / before RPE-02 consumes the guard:

- NB-1 — parsed-schema bypass;
- NB-2 — non-normalized parser exceptions.

NB-6 and NB-7 were accepted as evidence-hygiene corrections for this closure.

## RED

Opening HEAD:
`c9e8ad98aeee6b4ae9346dac554fc599abfe1a8b`

Targeted RED commit:
`0d680623b50a075024107443b14b638b1250e0d8`

Targeted RED test blob:
`1691d7f74e430d65f00fd4603f6da51c23e75a52`

Targeted RED report blob:
`425b8102389e134ef54f6ff95b03afa8a9d9ae8c`

Observed before correction:

```text
Ran 6 tests

FAILED
failures = 2
errors = 3
1 test passed
```

RED demonstrated:
- legitimate raw schema not accepted by public API;
- pre-parsed schema object accepted by public API;
- parsed document/schema bypass still publicly exposed;
- pathological integer leaks ValueError;
- pathological nesting leaks RecursionError.

## NB-1 closure

Final guard blob:
`82f4323316b95ea5895cdd0c6f0c68e801e595ca`

Public API is now:

```text
validate_governed_json(
    raw_document: str | bytes,
    raw_schema: str | bytes,
)
```

The public API strictly parses the schema itself before parsing/validating the document.

A pre-parsed schema dictionary is rejected.

The former public:
`validate_document(document, schema)`

no longer exists.

The internal parsed-document validator is private:

`_validate_document(...)`

and receives an already strictly validated schema only from the raw public path.

Existing RPE-01 tests and the mutation sweep now send the concrete P5-E schema as raw JSON.

## NB-2 closure

`parse_json_strict` now normalizes:

- `ValueError`;
- `RecursionError`;
- `json.JSONDecodeError`;

into:

`GovernedSchemaError`

while preserving existing direct `GovernedSchemaError` failures.

Dedicated RED→GREEN cases cover:
- a 5000-digit integer;
- 5000-level array nesting.

The guard remains fail-closed with one public exception family for these parser failure modes.

## GREEN

Targeted NB-1/NB-2 tests:

```text
6 / 6 PASS
```

Current RPE-01 main + mutation-sweep unittest surface:

```text
22 / 22 PASS
```

## NB-6 — corrected sweep accounting

The previous reported count `433` represented parsed-object mutations only.

The final sweep now reports separately:

```text
PARSED-OBJECT MUTATIONS = 433
RAW-JSON BREAKERS       = 7
TOTAL                    = 440
SURVIVORS                = 0
```

Raw breaker families now executed inside the sweep:

- duplicate top-level member;
- duplicate nested member;
- escaped key duplicate that decodes to the same member;
- NaN;
- Infinity;
- -Infinity;
- duplicate member in raw schema JSON.

The sweep itself uses the raw concrete schema through the strict public API.

Therefore no claim is made that the original 433 count covered raw JSON operators.

## Final targeted regression

Current P5-E qualification surface + RPE-01 + targeted closure:

```text
95 / 95 PASS
```

Relative to the adopted readiness base:

```text
P5-E contract diff = 0
P5-E model diff = 0
P5-D4 runtime diff = 0
```

No full Obsidian suite was run.

## NB-3 — explicit scope clarification

The concrete P5-E governed schema is:

`STRUCTURAL + STRICT-TYPE + CLOSED-NORMATIVE-LIST`

It is not a replacement for the adopted P5-E semantic invariant layer.

Therefore values such as existing authorization booleans, timing integers, and free descriptive strings are not all frozen to their current literal value by this schema.

Existing P5-E value semantics remain guarded by the adopted P5-E invariants.

For future REAL P5-E configuration schemas, an authority flag should normally be encoded as schema-level `const: false` when the schema itself is intended to carry that authority boundary.

This requirement is carried forward to the preregistrations that define RPE-04/RPE-05/RPE-06 configuration surfaces.

## NB-4 — explicit binding limitation

The generic guard validates the structure of:
- `artifact_role`;
- `source_binding`.

It does not currently receive an externally expected role or recompute the Git source blob as part of generic validation.

For the current P5-E schema, source binding remains independently demonstrated by the dedicated Git blob test and qualification evidence.

No claim is made that dynamic source-binding enforcement is already part of the generic RPE-01 guard.

Later REAL P5-E preregistrations must decide explicitly whether expected-role/source-byte binding belongs in the guard API or at the governed caller boundary.

## NB-5 — retained non-blocking hardening debt

The following remain non-blocking future hardening:
- proactively reject contradictory restrictive schema constraints;
- require ASCII regex semantics where a future schema relies on character classes;
- reject isolated Unicode surrogates where downstream UTF-8 evidence persistence requires it.

These do not reopen N4.

## NB-7 — packet-fidelity rule for the next delta packet

The next packet must:
- identify the historical RED only by its exact immutable Git identity/reference unless its exact historical bytes are deliberately extracted;
- not label the current GREEN test as the historical RED source;
- not claim transformed Markdown to be byte-identical to historical report blobs;
- embed the persisted external review from its current canonical file;
- bind exact current code/JSON blobs;
- include an exact Git diff for the targeted closure.

## Final candidate identities

```text
GUARD
= 82f4323316b95ea5895cdd0c6f0c68e801e595ca

P5-E GOVERNED SCHEMA
= 87e45cc75753439879e2902d3cbdbd5d71d8a1b2

MAIN RPE-01 TEST
= cd0e091233e5a4473ef280c7061db8cf880169e9

MUTATION SWEEP TEST
= a8baceaf4a921765ae0fdcb182bef7dd0eba1246

TARGETED CLOSURE TEST
= 1691d7f74e430d65f00fd4603f6da51c23e75a52
```

## Real-state integrity

P5-D4 real state remains unchanged:

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
NB-1
= CLOSED_CANDIDATE

NB-2
= CLOSED_CANDIDATE

NB-6
= EVIDENCE_ACCOUNTING_CORRECTED

NB-7
= DELTA_PACKET_FIDELITY_REQUIREMENT_ACTIVE

RPE01_EXTERNAL_REVIEW_TARGETED_CLOSURE
= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE-02
= CLOSED

REAL_P5E
= CLOSED
```
