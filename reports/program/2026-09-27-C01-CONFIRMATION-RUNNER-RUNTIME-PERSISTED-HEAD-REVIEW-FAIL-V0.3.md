# C01 CONFIRMATION RUNNER — RUNTIME PERSISTED-HEAD REVIEW — FAIL V0.3

Date: 2026-09-27

Reviewed persisted HEAD:

`9ab446cb602f41bc461ef56b790b2776cf15a217`

Parent:

`279f7c8dcbec7bc68426243f7fa5867a161f0d0d`

Persisted runtime blob:

`0680718c0778875cab0c884e9554c01027bb885d`

Qualified breaker blob:

`f2596da79f37a7bd7f46078e6b60a661158b6bf7`

Frozen Charter blob:

`ada0ebf41ecd7ab406d2656ac745ed7003d5b5c1`

Confirmation execution contract blob:

`f6823cfa7b3c582524b3d512d45b16fdc0450ee8`

## Scope

This review is strictly synthetic and documentary.

It does not:

- access confirmation-window outcome data;
- compute any primary confirmation score;
- authorize real confirmation execution;
- modify the frozen Charter;
- modify the frozen model;
- modify the confirmation runner;
- modify the qualified breaker;
- modify any seal object.

## Previously recorded qualification

The persisted checkpoint previously recorded the runtime re-break as PASS after closure of:

- `CRITICAL_CONTROL_ABSENCE_FAILS_OPEN`;
- `STRICT_NUMERIC_TYPE_COERCION_FAILS_OPEN`.

That PASS is superseded by this review for the runtime qualification claim.

The historical PASS artifact remains preserved as audit history; it is not deleted or rewritten.

## New adversarial finding

Verdict:

`FAIL`

Finding:

`FROZEN_WINDOW_BINDING_FAILS_OPEN`

### Frozen temporal contract

The Charter fixes:

- `eligible_start_utc = 2026-05-25T00:00:00Z`;
- `fixed_end_utc = 2027-05-24T23:59:59Z`.

The confirmation execution contract additionally fixes:

- `earliest_primary_evaluation_utc = 2027-05-25T00:00:00Z`.

### Persisted runtime behavior

The runtime validates the frozen object identities in `EXPECTED_BINDINGS`, including the Charter/model/seal bindings.

However, the runtime does not bind the caller-provided `window` values to the three frozen temporal values above.

For the `window` block it requires only typed boolean controls:

- `real_execution_requested`;
- `partial_window_primary_scoring`;
- `early_primary_score_exposed`.

When real execution is requested, the runtime reads `window["fixed_end_utc"]` from caller input for the comparison against `as_of_utc`.

It does not compare:

- caller `eligible_start_utc` to the frozen Charter value;
- caller `fixed_end_utc` to the frozen Charter/contract value;
- caller `earliest_primary_evaluation_utc` to the frozen execution-contract value.

There are no runtime constants or equivalent source-derived checks that enforce these three exact temporal bindings.

### Breaker gap

The persisted breaker includes the three correct window values in the positive fixture.

It does not adversarially mutate:

- `eligible_start_utc`;
- `earliest_primary_evaluation_utc`.

Its `fixed_end_utc` use in the existing real-execution breaker does not establish identity binding to the frozen Charter/contract; it only participates in the fixture's temporal comparison.

Therefore the previous qualified harness did not prove exact frozen-window binding.

## Impact

Current real confirmation execution remains blocked by the runtime.

This finding does **not** demonstrate:

- confirmation-data access;
- real confirmation execution;
- primary scientific scoring;
- a scientific `CONFIRMED` claim.

It demonstrates that the synthetic runtime qualification was too strong: an input window can diverge from the frozen temporal contract without that mismatch itself being rejected.

The correct status is therefore:

`RUNTIME QUALIFICATION = FALSE`

until the exact three temporal bindings are enforced and adversarially re-broken.

## Scientific state

Confirmation data accessed:

`false`

Primary confirmation score computed:

`false`

Real confirmation execution:

`false`

Scientific confirmation:

`NOT_YET_PERFORMED`

Frozen model:

`UNCHANGED`

Frozen Charter:

`UNCHANGED`

## Minimal correction required

Before runtime qualification may return to PASS:

1. bind `eligible_start_utc` exactly to `2026-05-25T00:00:00Z`;
2. bind `fixed_end_utc` exactly to `2027-05-24T23:59:59Z`;
3. bind `earliest_primary_evaluation_utc` exactly to `2027-05-25T00:00:00Z`;
4. add dedicated adversarial breakers for independent mutation/absence/malformed representation of those bindings as applicable;
5. rerun the qualified historical harness and the new breakers;
6. persist the correction;
7. perform a fresh persisted-head adversarial re-break.

## Verdict

`C01_RUNTIME_PERSISTED_HEAD_REVIEW_V0_3 = FAIL`

`FROZEN_WINDOW_BINDING_FAILS_OPEN = CONFIRMED`

Runtime qualification:

`FALSE`

Real confirmation execution authorized:

`FALSE`

Primary scientific scoring authorized:

`FALSE`

## Next governed action

Implement only the minimal synthetic correction for the three frozen temporal bindings and the dedicated breakers.

No confirmation data may be accessed.

No C01 model, Charter, seal or scientific result may be changed.
