# RPE-01 — FINAL DELTA REVIEW — CLAUDE RETURN

Date persisted: 2026-10-03

## Verdict

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

`BLOCKING_FINDINGS = NONE`

The reviewer reconstructed the packet copies and reported that the announced code, JSON, test, qualification, RED, and adjudication identities matched, except that the display copy of the persisted external review differed in bytes consistently with the packet's declared normalization.

The reviewer executed the candidate under Python 3.12.3 on Linux and observed:
- 94/95 tests passing;
- the only failure was `test_pathological_nesting_is_normalized`;
- the mutation sweep reproduced 433 parsed-object mutations + 7 raw breakers = 440 attempts, 0 survivors.

## NB-a — deterministic depth / recursion normalization

Status from reviewer:
`NON_BLOCKING`

Observed:
- `parse_json_strict` normalizes parser recursion only if the interpreter/parser itself raises there;
- recursive schema/document validation is not explicitly depth-bounded;
- a sufficiently deeply nested schema can reach `_validate_schema_node` and raise an unnormalized `RecursionError`;
- the existing 5000-level array test is interpreter-dependent: Python 3.12.3 on the reviewer environment parsed the input rather than raising during JSON parsing.

Reviewer correction recommendation:
- define an explicit deterministic maximum governed JSON depth for both documents and schemas;
- test exact boundary and boundary+1 rather than interpreter recursion limits;
- normalize residual validation `RecursionError` to `GovernedSchemaError`;
- record Python version/context in qualification.

## NB-b — raw breakers not all discriminating

Status from reviewer:
`NON_BLOCKING`

Observed:
- the count 433 + 7 = 440 is arithmetically correct;
- some raw probes such as `{"x":NaN}` are rejected by the concrete P5-E schema even if `parse_constant=_reject_constant` is removed, because `x` is itself an unknown key;
- therefore those raw probes do not independently demonstrate the parser protection.

Reviewer correction recommendation:
- construct raw breakers from the otherwise-valid adopted P5-E contract;
- duplicate a real normative key such as `evaluation_authorized`;
- inject NaN/Infinity into real numeric fields;
- use targeted mutation checks to demonstrate that removing the intended protection changes the targeted breaker outcome.

## NB-c — usage rule

Status from reviewer:
`ACCEPTABLE NON_BLOCKING NOTE`

`validate_schema_definition` remains public on a dictionary, but it does not provide a public document-validation bypass.

Adopted usage rule for subsequent RPE stages:
- `validate_governed_json(raw_document, raw_schema)` is the only authorized governed-artifact validation entrypoint;
- underscore-prefixed functions are forbidden to external consumers;
- `validate_schema_definition` must not be used as a bypass for governed document validation.

## Scope / authority

The reviewer found:
- NB-1 closed;
- NB-2 partially closed because of NB-a;
- NB-3/NB-4 correctly bounded;
- NB-5 non-blocking;
- no RPE-02 or REAL P5-E authority leakage.

Reviewer recommended one final technical pass for NB-a + NB-b before RPE-02 consumes the guard, followed by a short delta review.

This persisted review creates no authority.

`RPE-02 = CLOSED`

`REAL_P5E = CLOSED`
