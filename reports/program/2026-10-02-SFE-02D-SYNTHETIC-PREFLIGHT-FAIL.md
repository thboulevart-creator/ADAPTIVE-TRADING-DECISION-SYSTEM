# SFE-02D — SYNTHETIC PREFLIGHT FAIL

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## Observed persisted state

```text
HEAD =
3259f05c7c71cc256c82ffcec6e5823f35fdb3a1

TREE =
4e50488e1c815df80f67b8d58850f4403b9d9d53
```

## Frozen execution identities

```text
SFE-02D CONTRACT BLOB =
4fd8b1adb2bb8e6d2ca11870bdee88fd232c757f

SFE-02D RUNNER BLOB =
539d9fa0198a92cc1424a06ebb5606c708a71472
```

## Synthetic breaker result

```text
TOTAL = 10
PASS = 8
FAIL = 2

REAL DATA RUN =
NOT STARTED

PERFORMANCE OBSERVATION =
NONE
```

### Failure 1 — invalid synthetic continuity fixture

The test split a continuity block and reset the H1 ordinals, but it retained synthetic directional signals in the first 20 rows of the new block.

That fixture is impossible under either qualified strategy runtime because:

```text
continuity_ordinal < 20
→ signal = UNDEFINED
```

The runner correctly rejected the impossible fixture when it encountered a directional event with a negative fixed inference-block index.

Classification:

```text
RUNNER DEFECT = NOT ESTABLISHED
BREAKER FIXTURE DEFECT = ESTABLISHED
```

Required correction:

- keep the directional event immediately before the continuity break to test `t+1` exclusion;
- set the new block ordinals 0..19 to `UNDEFINED` in the synthetic signal fixture.

### Failure 2 — non-claim token incorrectly treated as forbidden output

The breaker asserted that the serialized envelope must not contain the literal key/value token `PNL`.

The result envelope intentionally contains:

```text
non_claims = ["PNL", "PROFITABILITY", ...]
```

This is governance metadata and not a PnL result field.

Classification:

```text
RUNNER DEFECT = NOT ESTABLISHED
BREAKER ASSERTION DEFECT = ESTABLISHED
```

Required correction:

- verify that the envelope has no decision/result fields representing PnL or execution;
- permit `PNL` inside the explicit `non_claims` list.

## Decision

```text
SFE_02D_SYNTHETIC_PREFLIGHT =
FAIL

REAL_DUAL_RESULT_RUN =
BLOCKED

RUNNER_CHANGE =
NONE

EXPERIMENT_CONTRACT_CHANGE =
NONE

PERFORMANCE_OBSERVED =
NO

NEXT =
TARGETED BREAKER V0.2 CORRECTION
```
