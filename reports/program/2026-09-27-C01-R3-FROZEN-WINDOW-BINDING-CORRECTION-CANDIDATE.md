# C01-R3 — FROZEN WINDOW BINDING MINIMAL CORRECTION — PERSISTENCE CANDIDATE

Date: 2026-09-27

Governed base HEAD:

`7f07396a5f3936847d3271c5f242cebddb66a163`

Finding being corrected:

`FROZEN_WINDOW_BINDING_FAILS_OPEN`

## Closed scope

This correction is limited to exact binding of:

- `eligible_start_utc = 2026-05-25T00:00:00Z`;
- `fixed_end_utc = 2027-05-24T23:59:59Z`;
- `earliest_primary_evaluation_utc = 2027-05-25T00:00:00Z`.

No other runtime semantics are intentionally changed.

## Runtime correction

The runtime now defines the three frozen temporal constants and rejects any `window` whose corresponding value is absent, malformed or not exactly equal to the frozen contract value.

Failure remains fail-closed as:

- `execution_status = BLOCKED`;
- `primary_decision_status = NOT_INTERPRETABLE`;
- guard failure `WINDOW_BINDING_MISMATCH:<field>`.

## Breakers

Three dedicated C01-R3 tests were added, one per frozen temporal binding.

Each test attacks:

- wrong value;
- missing value;
- malformed boolean value.

The existing 32 contractual breakers and positive synthetic control are unchanged.

## Sandbox qualification

Sandbox branch:

`sandbox/c01-r3-frozen-window-binding`

Qualification workflow run:

`36321233678`

Results:

- `py_compile = PASS`;
- historical qualified harness = `33/33 PASS`;
- C01-R3 frozen-window breakers = `3/3 PASS`;
- full C01 runner harness = `36/36 PASS`.

Qualified runtime blob:

`7ea6ed6796eae8618cfd823b49eee1a63a19e096`

Qualified breaker blob:

`cf275dba96e50e8b899223a57267e811af4693ec`

## Protected scientific state

Confirmation data accessed:

`false`

Primary confirmation score computed:

`false`

Real confirmation execution:

`false`

Scientific confirmation:

`NOT_YET_PERFORMED`

The following remain unchanged:

- C01 Charter;
- frozen model;
- seal candidate;
- final seal;
- confirmation execution contract.

## Status

`C01_R3_LOCAL_SANDBOX_QUALIFICATION = PASS`

Runtime qualification:

`NOT_YET_FINAL`

## Next governed action

Persist exactly the qualified runtime, qualified breaker, this report and checkpoint update.

Then perform a fresh adversarial re-break by checking out the exact persisted governed HEAD.

Only after that re-break passes may a new runtime PASS be issued.
