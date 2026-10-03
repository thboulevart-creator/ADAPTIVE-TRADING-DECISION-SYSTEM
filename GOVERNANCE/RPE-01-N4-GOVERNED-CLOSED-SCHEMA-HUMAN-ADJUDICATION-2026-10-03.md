# RPE-01 — N4 GOVERNED CLOSED SCHEMA — HUMAN ADJUDICATION

Date: 2026-10-03

## Human decision

The human authority adopts:

`RPE-01 — N4 GOVERNED CLOSED SCHEMA`

in its final qualified state after:
- initial RPE-01 qualification;
- external review `PASS_WITH_NON_BLOCKING_NOTES` with no blocker;
- NB-1 / NB-2 targeted closure;
- portability and raw-breaker discrimination hardening;
- final external delta-review `PASS_WITH_NON_BLOCKING_NOTES` with `BLOCKING_FINDINGS = NONE`;
- NB-α scanner string/escape test-only closure.

The adopted normative state is:

`RPE01_GOVERNED_CLOSED_SCHEMA = QUALIFIED_AND_HUMAN_ADOPTED`

After persistence and verification of this record:

`RPE-01 = CLOSED`

This adoption does not automatically open RPE-02 or RPE-03.

## Binding pre-adoption identity

This human adoption is bound to the exact pre-adoption repository state:

```text
PRE-ADOPTION HEAD
= 686e9266f84e1a9ae05938bf3260728492a17c92

FINAL GUARD
= 26f977961d72a062199d71ffd628d5a5cc047887

P5-E GOVERNED SCHEMA
= 87e45cc75753439879e2902d3cbdbd5d71d8a1b2

FINAL HARDENING QUALIFICATION
= f514af4bf01a62b3f751e14cfffaaf20bfe66885

FINAL HARDENING QUALIFICATION REPORT
= 92e45cf8fa279c0b9643a9ad77d4c1f19d6a7cdf

NB-α TEST
= a170019180579f82e9f9ea0918f4fed445cab1ba

NB-α CLOSURE PROOF
= 76e8b5c2f85fc1088df0a25ef3df194f63904b75
```

Branch at adoption:

`feat/obsidian-projection-rpe01-governed-closed-schema-v0.1`

Pre-adoption local HEAD and remote HEAD were equal.

Pre-adoption worktree was clean.

## Adopted governed-artifact consumer contract

The following constraints are adopted for every future consumer of RPE-01:

```text
AUTHORIZED GOVERNED-ARTIFACT VALIDATION ENTRYPOINT
= validate_governed_json(raw_document, raw_schema)

UNDERSCORE-PREFIXED GUARD FUNCTIONS
= FORBIDDEN FOR EXTERNAL CONSUMERS

validate_schema_definition
= NOT AN AUTHORIZED GOVERNED-DOCUMENT VALIDATION ENTRYPOINT
```

RPE-02, RPE-03 and later consumers must carry this contract explicitly into their preregistration and implementation boundaries.

No future consumer may use a private `_*` guard function as a normative validation path.

## Adopted deterministic JSON depth rule

The final qualified guard contains the preregistered rule:

```text
MAX_GOVERNED_JSON_DEPTH = 64
```

Normative interpretation:

- JSON container nesting is counted lexically outside strings;
- a root object or array has depth 1;
- document and schema raw JSON are both checked before `json.loads`;
- depth `<= 64` is permitted by the depth guard subject to all other validation;
- depth `> 64` is rejected with `GovernedSchemaError`;
- interpreter recursion limits are not normative.

Residual validation recursion is normalized to `GovernedSchemaError` at the qualified boundary.

## Final scanner string/escape proof

NB-α is accepted as test-locked by the final test-only closure.

The qualified guard itself was not modified during NB-α closure.

The final proof establishes:

```text
container characters inside governed JSON strings
→ do not consume JSON depth budget

escaped quote/backslash handling
→ cannot hide later real container depth

in_string mutant
→ KILLED

escaped-state mutant
→ KILLED
```

Final local evidence before adoption:

```text
NB-α dedicated tests
= 4 / 4 PASS

current RPE-01 surface
= 46 / 46 PASS

P5-E + RPE-01 targeted regression
= 113 / 113 PASS
```

## Retained scope boundaries

### NB-3 — structural scope

RPE-01 protects:

- closed object structure;
- strict JSON/member handling;
- strict types;
- closed normative lists and list order where specified;
- governed schema-language structure;
- deterministic JSON depth;
- fail-closed parser/validation behavior covered by the qualified guard.

RPE-01 does not replace the adopted P5-E value-semantic invariant layer.

Existing P5-E invariants continue to carry value semantics.

Future schemas that themselves carry authority flags should normally encode those flags with explicit constraints such as `const: false` where preregistered.

### NB-4 — binding scope

`source_binding` and `artifact_role` are structurally represented and validated.

The generic RPE-01 guard does not claim dynamic verification of expected artifact role or recomputation/enforcement of source Git blob identity.

Where such dynamic binding is required, the future consumer/caller boundary must preregister and enforce it explicitly.

### NB-5 — non-blocking future hardening

The following remain non-blocking future hardening only where a distinct future failure mode requires them:

- proactive rejection of contradictory restrictive schema constraints;
- explicit ASCII regex semantics where relevant;
- isolated Unicode-surrogate handling where downstream UTF-8 persistence requires it.

These notes do not reopen RPE-01.

## NB-β / NB-c consumer-state interpretation

Static repository checks before adoption found no runtime Python consumer under `tools/` using:

- `validate_schema_definition`;
- `_validate_document`;
- `_validate_document_node`;
- `_validate_schema_node`.

No runtime Python consumer currently invokes `validate_governed_json`, which is expected because RPE-02/RPE-03 remain unopened.

Tests may exercise schema utilities directly for qualification purposes; this does not constitute a runtime governed-document consumer.

The consumer contract above is mandatory for future stages.

## Protected predecessor integrity

At adoption, the protected identities remain:

```text
P5-E ADOPTED CONTRACT
= 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-E ADOPTED SYNTHETIC MODEL
= c0f16baa151c1466e30ba5778f1fca8184cd4aac

P5-D4 RUNTIME
= 1825e53d195ba2a63b5b646a5b78eb77939b94b5
```

No mutation of those artifacts is part of this adoption.

## Real P5-D4 state integrity before adoption

```text
observer-events.jsonl SHA256
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json SHA256
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json SHA256
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

No real P5-D4 control-state mutation is authorized by this persistence step.

## Stage state after verified persistence

The human decision closes RPE-01 only.

```text
RPE-01
= CLOSED
= QUALIFIED_AND_HUMAN_ADOPTED

RPE-02
= CLOSED

RPE-03
= CLOSED

RPE-04
= CLOSED

RPE-05
= CLOSED

RPE-06
= CLOSED

REAL P5-E
= CLOSED
```

Under the already adopted readiness DAG, RPE-02 and RPE-03 become eligible to be separately opened after RPE-01 closure, but this record does not itself open or authorize either stage.

## Explicitly not authorized

This adoption does not authorize:

- implementation or execution of RPE-02;
- implementation or execution of RPE-03;
- implementation or execution of RPE-04;
- implementation or execution of RPE-05;
- implementation or execution of RPE-06;
- real GitHub polling;
- sandbox repository or ref creation;
- experimental push;
- real HEAD evaluation;
- Stage A;
- Stage B;
- promotion;
- publication;
- Vault mutation;
- `CURRENT.md` mutation;
- real P5-D4 control-state mutation;
- daemon registration;
- Scheduled Task registration;
- Windows Service registration;
- startup registration;
- P6.

`REAL_P5E = CLOSED`

## Persistence authority

The only operations authorized by the human adoption statement are:

- persist this adjudication record;
- commit and push it;
- verify final repository consistency;
- STOP.

No guard, schema, qualification, test, P5-E contract/model, P5-D4 runtime, control state, Vault, CURRENT or future RPE artifact may be modified by this persistence step.
