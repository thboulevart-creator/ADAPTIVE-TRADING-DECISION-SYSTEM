# RPE-01 — N4 GOVERNED CLOSED SCHEMA — QUALIFICATION

Date: 2026-10-02

## Result

```text
RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE
= QUALIFIED_FOR_EXTERNAL_REVIEW
```

RPE-01 is not yet human-adopted.

RPE-02 and later stages remain closed.

## Lineage

Adopted readiness base:
`d904eb61d9b704dc8ac38da445eb1cd491a58b33`

Preregistration:
`406e67da3ab197c5a9ae4b3e971368549af6e1da`

RED test:
`803709c26769fc9889b4ac1e47c0dd8df2782580`

RED report:
`b3a7df32198fd5a618f927c83d04d5f3a6491050`

## Qualified implementation identities

Guard:
`3f61b9191e0ee7fb8c18fdecf60f45c586c74629`

Concrete P5-E governed schema:
`87e45cc75753439879e2902d3cbdbd5d71d8a1b2`

Green test:
`391663ee2b8634c0221b5352c8d1242bfdb3c04e`

Mutation sweep test:
`bad495950ddce5c171cac4c667e40654c6673724`

Adopted P5-E contract covered by the concrete schema:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

## Test-first evidence

Initial RED:

```text
Ran 19 tests
FAILED
1 intentional PASS demonstrated the pre-RPE01 gap:
unknown authority key survived the old semantic invariant checker.
```

After implementation:

```text
RPE-01 targeted
= 22 / 22 PASS
```

## Mutation sweep

The programmatic sweep did not use P5-E contract blob binding as a rejection mechanism.

It mutated:
- every object node with an unknown key;
- every required object key by deletion;
- every scalar leaf to a different JSON type;
- every concrete normative list with duplicate and unknown members;
- the normative order of `real_end_to_end_stages`.

Observed:

```text
attempted = 433
survivors = 0
```

Therefore the preregistered exit criterion is satisfied:

`ALL_PREREGISTERED_SCHEMA_MUTATIONS_REJECTED_WITHOUT_USING_P5E_CONTRACT_BLOB_BINDING`

## Parser and schema-language properties

The qualified guard rejects before dictionary construction:
- duplicate raw JSON object members;
- nested duplicates;
- `NaN`;
- `Infinity`;
- `-Infinity`.

The validator enforces:
- exact closed object key sets;
- strict JSON type identity;
- bool is not accepted as integer;
- float/scientific-float is not accepted as integer;
- enums;
- regex patterns;
- integer bounds;
- list length;
- list uniqueness;
- closed list vocabulary;
- exact normative order where configured.

The schema definition itself is also parsed through the strict parser and strictly validated.

## Authority-channel property

The guard implementation is pure with respect to configuration authority.

Its source imports none of:
- `os`;
- `sys`;
- `argparse`;
- `socket`;
- `subprocess`;
- HTTP client modules.

It does not use:
- environment variables;
- CLI arguments;
- interactive input;
- implicit file reads;
- network state.

Inputs are only:
- explicit raw JSON;
- explicit schema object/raw schema.

This prevents the guard itself from becoming a hidden adjacent configuration authority.

## Concrete P5-E schema

The concrete P5-E schema:
- closes every current object depth;
- requires every current key;
- enforces strict leaf types;
- freezes the vocabulary and cardinality of current normative lists;
- requires normative list uniqueness;
- freezes exact order for `real_end_to_end_stages`;
- includes source binding to the adopted P5-E contract blob.

The source-binding test recomputes the Git object identity and matches:

`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

The adopted contract bytes were not modified.

## Targeted regression

Executed the current P5-E qualification surface plus RPE-01:

```text
Ran 89 tests
OK
```

Repository deltas relative to the adopted readiness base:

```text
P5-E contract diff = 0
P5-E model diff = 0
P5-D4 runtime diff = 0
```

No full Obsidian suite was required or executed.

## Real state

P5-D4 real-state fingerprints remained:

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Binding

The qualification binds the exact guard blob and P5-E schema blob.

Any modification of either requires a new qualification before the modified artifact may be treated as RPE-01-qualified.

## Maximum claim

```text
RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE
= QUALIFIED_FOR_EXTERNAL_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE02
= CLOSED

REAL_P5E
= CLOSED
```
