# F — NATIVE BI5 FREEZE-PERSISTENCE IMPLEMENTATION CANDIDATE — ADVERSARIAL BREAK

**Date:** 2026-09-19  
**Initial implementation commit:** `e83169226578040eb52bef45e65813e54c44b3f5`  
**Initial qualification-runner commit:** `0b09b8055c88f829d0f1ebac29b834d62730b56c`

Production source:

`src/native_bi5_freeze_persistence.py`

Initial source blob:

`7bf05f9383252f8bcfe3db06d08b2d0c2cc550ad`

Frozen F breaker:

`breakers/native_bi5_f_freeze_persistence_breaker.py`

Frozen breaker blob:

`3d9eb75c2f4e988c984da67af0af344d3dc24148`

Executable O implementation remains absent.

No real BI5 input, acquisition or backtest was used.

## 1. Initial executable qualification

Workflow:

`Native BI5 F Freeze Persistence Candidate`

Run:

```text
run = 35454862558
job = 105928242031
```

Controls:

```text
exact F source / frozen breaker / contract locks = PASS
O implementation absent                          = PASS
qualification environment                        = PASS
clean worktree                                   = PASS
```

Frozen breaker result:

```text
24 passed
12 failed
```

Initial candidate verdict:

```text
F FREEZE-PERSISTENCE IMPLEMENTATION CANDIDATE = FAIL
```

## 2. F-F01 — ACCOUNTING_WITNESS_SHAPE_OVERRESTRICTION

### Demonstrated behavior

A valid qualified synthetic input was emitted as:

```text
QUALIFICATION_TERMINAL_EVIDENCE
NOT_CREATED
```

instead of:

```text
QUALIFIED_UNIVERSE_FREEZE
FROZEN
```

The failure propagated into the duplicate, ordering, serialization, determinant-change and validation tests.

### Root cause

The candidate helper for a pure source witness requires exactly:

```text
component_manifest_entry_id
component_local_slot_index
```

That exact-shape rule is correct for:

```text
retained_occurrence.source_witness
```

but the same helper was incorrectly reused for:

```text
source_accounting entry
```

whose normative shape also contains:

```text
disposition
anomaly_class_id
```

Therefore valid complete-slot accounting was rejected merely because it carried its required disposition semantics.

The same over-reuse also affects COMPLETE_SLOT anomaly targets, whose shape additionally contains `target_scope`.

### Why this is a real implementation defect

F owns persistence of several different relations that share a source locator but do not share the same object shape.

Therefore:

```text
source locator fields
≠ whole-object schema
```

Requiring the whole accounting/anomaly object to equal the pure witness schema confuses locator validation with relation-schema validation.

### Verdict

```text
F-F01 = FAIL
```

### Authorized minimal correction

Keep the exact-shape rule for retained-occurrence `source_witness`.

For accounting and COMPLETE_SLOT anomaly targets:

- validate their own full relation shape;
- extract and validate only the two locator fields as a locator;
- do not force the whole object through the pure-witness schema.

No F contract semantics, frozen breaker, O implementation or permission boundary may change.

## 3. Current state

```text
F test-first breaker/harness = PASS
F production candidate       = FAIL
F global gate                = BLOCKED
O implementation             = ABSENT
O global gate                = BLOCKED
```

Exactly authorized next action:

```text
fresh HEAD
→ correct F-F01 only
→ update candidate workflow source lock
→ persisted frozen-breaker re-run
→ adversarially attack the corrected implementation
```

No real BI5 data/acquisition/backtest is authorized.
