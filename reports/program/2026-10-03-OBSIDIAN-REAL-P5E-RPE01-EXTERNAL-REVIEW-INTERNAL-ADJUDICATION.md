# RPE-01 — GOVERNED CLOSED SCHEMA — EXTERNAL REVIEW INTERNAL ADJUDICATION

Date: 2026-10-03

## External review result

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

`BLOCKING_FINDINGS = NONE`

The external reviewer reproduced:
- 22/22 RPE-01 tests;
- 89/89 targeted P5-E + RPE-01 regression;
- 41 additional adversarial probes.

The N4 exit criterion remains supported: added-key, duplicate-member, and coercion vectors are rejected semantically without relying on P5-E contract blob binding.

## Internal adjudication

```text
NB-1 = CONFIRMED / TARGETED CORRECTION REQUIRED BEFORE HUMAN ADOPTION
NB-2 = CONFIRMED / TARGETED CORRECTION REQUIRED BEFORE HUMAN ADOPTION
NB-3 = CONFIRMED / SCOPE CLARIFICATION + FUTURE RPE REQUIREMENT
NB-4 = CONFIRMED / NON-BLOCKING BINDING NOTE + FUTURE RPE REQUIREMENT
NB-5 = CONFIRMED / NON-BLOCKING HARDENING DEBT
NB-6 = CONFIRMED / EVIDENCE-HYGIENE CORRECTION IN TARGETED CLOSURE
NB-7 = CONFIRMED / PACKET-FIDELITY CORRECTION IN TARGETED CLOSURE
```

## NB-1 — parsed-schema bypass

Confirmed.

Current public API accepts:
`validate_governed_json(raw_document, schema_object)`

and:
`validate_document(document, schema_object)`

A caller may therefore parse raw schema JSON permissively before passing the resulting object to the guard, bypassing duplicate-member rejection in the schema source.

### Required targeted correction

The public validation surface must accept only raw schema bytes/text, or an unforgeable/explicitly validated schema handle produced by the strict parser.

Preferred minimal closure:

```text
validate_governed_json(raw_document, raw_schema)
`

where both inputs are `str | bytes`.

Internal parsed-object validation may remain private only.

All RPE-01 tests and the mutation sweep must consume the raw schema through this public path.

## NB-2 — exception normalization

Confirmed.

The strict parser may leak parser/runtime exceptions such as:
- `ValueError` for pathological integer conversion;
- `RecursionError` for pathological nesting.

These are fail-closed in effect but violate the API contract if callers catch only `GovernedSchemaError`.

### Required targeted correction

Normalize parser and recursive-validation failures into:
`GovernedSchemaError`

at the public boundary.

At minimum add RED coverage for:
- oversized integer conversion;
- pathological nesting.

## NB-3 — structural versus semantic scope

Confirmed and non-blocking.

The concrete P5-E governed schema is a structural/type/list guard, not a replacement for P5-E semantic invariants.

It intentionally does not freeze every existing boolean to `const`, every integer to its current value, or every free string to its exact current value.

The qualification must state explicitly:

`CLOSED STRUCTURE / STRICT TYPES / CLOSED NORMATIVE LISTS; P5-E VALUE SEMANTICS REMAIN GUARDED BY THE ADOPTED P5-E INVARIANTS.`

For future REAL P5-E configuration schemas, authority flags should normally be encoded as schema-level `const: false` where the schema itself is intended to carry the authority boundary.

This requirement is to be carried into RPE-04/RPE-05/RPE-06 preregistration.

## NB-4 — source binding and artifact role

Confirmed and non-blocking for RPE-01.

The current generic guard validates `source_binding` and `artifact_role` structurally but does not itself compare:
- artifact role against an externally expected role;
- source-binding blob against the bytes being validated.

Current P5-E binding is independently proven by the dedicated Git blob test and qualification identity.

For later governed runtime configuration artifacts, preregistration must decide whether pure expected-role/source-blob verification belongs in the generic guard API or in the governed caller boundary.

No silent claim is made that RPE-01 currently enforces source binding dynamically.

## NB-5 — schema-language hardening debt

Confirmed, non-blocking.

Contradictory constraints identified by the review are restrictive, not permissive; they fail closed.

Potential future hardening:
- reject contradictory `const/enum/pattern`;
- reject contradictory `ordered_const/allowed_values`;
- enforce ASCII regex semantics where required;
- reject isolated Unicode surrogates where downstream UTF-8 evidence persistence requires it.

These are not required to close N4.

## NB-6 — mutation-sweep evidence hygiene

Confirmed.

The 433-count sweep covers parsed-object mutation operators only.

Raw duplicate-member and NaN/Infinity families were covered by unit tests, not included in the sweep count.

The targeted closure must:
- route the mutation sweep through strict raw-schema parsing;
- add explicit raw duplicate-member and non-standard numeric-constant mutations to the reported sweep or clearly split the metrics into parsed-object sweep and raw-JSON breaker families.

The final evidence must not imply the 433 count covered operators it did not execute.

## NB-7 — packet fidelity

Confirmed.

The first external packet embedded:
- the current GREEN test under a RED-test source label rather than the historical RED blob;
- Markdown source text whose byte identity did not match the announced historical report blobs, likely due to encoding/newline transformation during packet assembly.

Code and JSON identities were correct.

The targeted delta packet must therefore:
- include the external review return exactly;
- include the historical RED evidence as immutable Git identity/reference rather than mislabeling a later file as the RED blob;
- distinguish verbatim embedded content from Git-identity references;
- avoid claiming byte identity for any transformed Markdown;
- include exact current code/JSON blobs and exact diff.

## Targeted closure authorization interpretation

The user's existing instruction was to execute the full RPE-01 block directly through test-first qualification and external review, stopping before human adoption.

NB-1/NB-2 are within the already-open RPE-01 scope and are required before human adoption/RPE-02 consumption.

Therefore the next technical step is a narrow RPE-01 external-review targeted closure:

1. RED for NB-1 and NB-2;
2. minimal guard/API correction;
3. update RPE-01 tests and sweep to use raw schema;
4. evidence-hygiene correction for NB-6/NB-7;
5. re-run RPE-01 targeted tests, mutation/raw-breaker sweep and targeted P5-E regression;
6. produce a short self-contained delta-review packet;
7. STOP before human adoption.

## Authority boundary

No authorization is created for:
- RPE-02;
- real timing model;
- ancestry classifier;
- remote adapter;
- timed runner;
- sandbox creation;
- real polling;
- real P5-E.

`RPE-02 = CLOSED`

`REAL_P5E = CLOSED`
