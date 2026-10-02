# P5-E V0.1 — BB1 NORMATIVE GUARD COVERAGE — GREEN EVIDENCE

Date: 2026-10-02

## Scope

Minimal closure of:
- BB1 normative guard coverage;
- NB1 fixed-rate read overrun;
- NB4 claim scope;
- NB6 evidence mapping;
- NB7 non-pass / duplicate-slot semantics.

RED predecessor:
`e9b5f1664d2fd215fe77edbecbb24f24c306e2c3`

No real P5-E execution occurred.

## Corrected prospective identities

Contract:
`7e3e18ba946246065b43bc5fbabdc35980140eb9`

Model:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`
Evidence matrix:
`88e13a447a96455d4ac1d9d0f96e11b29329616d`

Observer-tick behavioral tests:
`f5b4bca7524f74f221927d1ec389e23d607d1eee`

P5-E adversarial tests:
`16b6fdb9c0bb5be980e5db59eb6f87f93e160205`

Matrix tests:
`182a7b60b440ddb8d5c0c9fdc65f423309383244`

BB1 closure tests remain:
`ed4a2c3d9c67f2d67d32b632bfa5c25d36cd0880`

P5-D4 runtime remains:
`1825e53d195ba2a63b5b646a5b78eb77939b94b5`
## BB1 guard closure

The original 23 normative survivor leaves are now rejected by strict invariant checks.

The combined BB1 regression is rejected.

Newly introduced NB1/NB4/NB7 normative fields are also strictly guarded.

## Matrix object binding

The evidence matrix now binds:
- exact contract blob;
- exact model blob.

`covered_object_drift_must_fail = true`

The matrix test recomputes Git object identity using `git hash-object --path` and fails on drift.

## NB1

A terminal read extending beyond its next required fixed-rate slot now returns:

```text
BLOCKED_REQUIRES_ADJUDICATION
ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT
```
Existing multi-observation overlap semantics remain separately testable.

## NB4

The contract now distinguishes:
- future adapter non-injection rule = true;
- current runtime-qualified non-injection property = false.

No adapter/runtime authority was introduced.

## NB6

Queue-capacity replacement/coalescing mappings now reuse:
`P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick`

Pending non-active FIFO/no-retarget semantics now use a dedicated D2 behavioral test:
`ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation`

No D2 runtime modification occurred.

## NB7

`INCOMPLETE_SYNTHETIC_WINDOW` is explicitly NON-PASS.

Duplicate fixed-rate slots now return:
`DUPLICATE_FIXED_RATE_SLOT`
instead of `CADENCE_GAP`.
## Targeted green execution

Covered:
- BB1 closure tests;
- P5-E contract tests;
- P5-E adversarial tests;
- prior B1→B5 closure tests;
- evidence-matrix tests;
- D2 observer-tick behavioral tests;
- P5-D4 bounded-loop runtime tests.

Observed:
```text
Ran 133 tests in 2.625s
OK
```

## Mutation-sweep exit criterion

Post-correction full P5-E surface baseline:
```text
51 tests
0 failures
0 errors
```

Every contract leaf was then independently mutated in a temporary copy.
Observed:
```text
FULL50_LEAF_MUTATIONS_TOTAL = 161
FULL50_SURVIVORS = 0
```

Therefore:
`NORMATIVE_LEAF_MUTATIONS_SURVIVING = 0`

This satisfies the preregistered BB1 exit criterion.

## Current boundary

```text
BB1_TARGETED_GREEN = PASS
TARGETED_PREDECESSOR_REGRESSION = NEXT
FULL_SUITE = NOT_YET_RUN
REAL_P5E = CLOSED
HUMAN_NORMATIVE_ADOPTION = CLOSED
```
