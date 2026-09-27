# C01 CONFIRMATION RUNNER — RUNTIME PERSISTED-HEAD REVIEW — FAIL V0.2

Date: 2026-09-27

Reviewed persisted HEAD:

`9cedc0a6eb8c38e5138d53de93da989a72a91738`

Parent:

`ce109b6c6ef4b1ee7d200ef4452b303646b265d3`

Persisted runtime blob:

`867eae8dc1ebe6fcf9ba2a25f6920cd8cd0a94aa`

Qualified breaker blob:

`f2596da79f37a7bd7f46078e6b60a661158b6bf7`

## Structural verification

PASS:

- branch identity;
- parent identity;
- exact persisted correction scope;
- qualified breaker unchanged;
- Charter/model/seal/preflight objects unchanged;
- previous fail-closed correction present;
- confirmation data not accessed;
- real confirmation execution not performed;
- primary scientific score not computed.

## Previous finding

The V0.1 finding:

`CRITICAL_CONTROL_ABSENCE_FAILS_OPEN`

is corrected in the persisted runtime.

Missing or malformed critical control blocks now fail closed.

## New adversarial finding

FAIL:

`STRICT_NUMERIC_TYPE_COERCION_FAILS_OPEN`

The persisted runtime still accepted semantically invalid numeric payloads through Python coercion/equality behavior.

Examples:

- `target_start_offset_minutes = True` could satisfy equality with integer `1`;
- boolean primary metrics could be converted to numeric values;
- string primary metrics could be converted through `float(...)`;
- invalid metric domains were not fully rejected;
- comparison sample counts were not cross-checked against the nine primary joint-state counts.

These paths could allow malformed evidence to participate in a synthetic `CONFIRMED` or `REFUTED` adjudication instead of failing closed.

## Verdict

`PERSISTED_HEAD_ADVERSARIAL_REBREAK = FAIL`

Runtime qualification:

`FALSE`

Real confirmation execution authorized:

`FALSE`

Primary scientific scoring authorized:

`FALSE`

## Minimal correction

The runtime was corrected locally to enforce:

- exact integer type for `target_start_offset_minutes`;
- exact numeric, non-boolean primary metric types;
- finite primary metrics;
- non-negative primary metric domain;
- strictly positive integer comparison sample count;
- comparison `n` equal to the sum of the nine joint-state counts.

Corrected working runtime blob:

`0680718c0778875cab0c884e9554c01027bb885d`

## Corrected local verification

PASS:

- `py_compile`;
- qualified harness: `33 passed`;
- collection errors: `0`;
- consolidated adversarial probes: `15/15 PASS`.

Probe groups:

- non-finite hardening: `3/3 PASS`;
- explicit-control hardening: `6/6 PASS`;
- strict-numeric hardening: `6/6 PASS`.

## Scientific state

Confirmation data accessed:

`false`

Primary confirmation score computed:

`false`

Real confirmation execution:

`false`

Scientific confirmation:

`NOT_YET_PERFORMED`

## Status

**STRICT-NUMERIC CORRECTION — PERSISTENCE CANDIDATE, NOT YET QUALIFIED.**

## Next governed action

Persist:

1. corrected runtime;
2. this FAIL V0.2 review;
3. checkpoint update.

Then perform a fresh persisted-head adversarial re-break.

Only after that re-break returns PASS may runtime qualification proceed.
