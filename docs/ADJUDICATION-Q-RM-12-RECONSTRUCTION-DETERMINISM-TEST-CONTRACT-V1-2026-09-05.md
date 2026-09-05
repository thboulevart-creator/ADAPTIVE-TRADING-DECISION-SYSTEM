# ADJUDICATION — Q-RM-12 RECONSTRUCTION & DETERMINISM TEST CONTRACT

**Date:** 5 septembre 2026  
**Status:** **TEST PROTOCOL = PASS; EXECUTABLE RUN = BLOCKED**  
**Depends on:** Q-RM-08..11

## 1. PURPOSE

Provide the final falsifiable protocol proving that two conforming implementations produce the same qualified logical occurrence universe from the same normative inputs.

This document defines the test; it does not fabricate the missing concrete acquisition/format bindings.

## 2. [CONSÉQUENCE NÉCESSAIRE]

For identical:

```text
D = acquisition declaration/version
R = representation identity/version
M = record-model version
B = binding identifier/version + dependencies
Q = qualification contract/version + parameters
```

conforming implementations must produce the same logical boundaries, same occurrence cardinality, same qualification membership, and same occurrence individuality.

Differences in traversal, parallelism, cache, restart, serialization, or downstream ordering are not admissible semantic causes of divergence.

## 3. TEST ORACLE

The comparison oracle must operate on semantic logical occurrences, not physical ordering.

Required comparisons:

```text
acquisition domain membership
logical record boundaries
logical cardinality
non-observation exclusion
anomaly classification/outcome
qualification membership
occurrence individuality
freeze reconstruction tuple
```

Strict duplicates must remain distinct when the normative input contains distinct occurrences.

## 4. REQUIRED TEST VARIANTS

### T01 — Same input, two implementations

Same D/R/M/B/Q; implementations A and B may use different parser libraries and traversal orders.

**Expected:** identical qualified universe.

### T02 — Sequential vs parallel

Same declared acquisition; execution partition differs.

**Expected:** identical universe.

### T03 — Cache hit vs cold parse

**Expected:** identical universe.

### T04 — Restart

Interrupt execution and reconstruct from the declared immutable inputs.

**Expected:** identical final universe, or explicit BLOCKED if reconstruction is insufficient.

### T05 — Serialization round-trip

Serialize and deserialize frozen semantic state with different container ordering.

**Expected:** identical semantic universe.

### T06 — Physical repartitioning

Represent the same declared acquisition using different physical partitions where the applicable binding declares them semantically equivalent.

**Expected:** no semantic divergence caused solely by partitioning.

### T07 — Strict duplicates

Input contains identical payloads as distinct occurrences.

**Expected:** no content-based collapse.

### T08 — Malformed isolated record

Apply a binding with constructive localisability proof.

**Expected:** Q-RM-04 `REJECT RECORD` and deterministic remaining universe.

### T09 — Non-localisable ambiguity

**Expected:** `QUALIFICATION BLOCKED`, not silent repair.

### T10 — New binding version

Change a qualification-relevant binding version.

**Expected:** distinct qualification state; no mutation of prior freeze.

## 5. PASS/FAIL/BLOCKED RULE

```text
PASS
= all required inputs are concretely declared AND all required comparisons agree.

FAIL
= all required inputs are available, implementations are expected to conform,
  and a semantic divergence or forbidden behavior is observed.

BLOCKED
= a required normative input, binding, oracle, artifact, or executable environment
  is missing, ambiguous, or not yet available.
```

BLOCKED must never be converted to PASS by assuming a default.

## 6. RECONSTRUCTION TEST

Given a frozen artifact F, independently reconstruct:

```text
D + R + M + B + Q
```

and rerun qualification.

The reconstructed result must match the original frozen semantic universe exactly.

If the tuple is insufficient, the reconstruction claim fails closed as `BLOCKED` rather than being inferred from physical artifacts.

## 7. [CONTRACTUEL]

Before execution, the project must provide:

- at least one concrete acquisition declaration;
- concrete supported format binding(s);
- concrete anomaly matrix;
- concrete qualification contract/version;
- concrete freeze artifact schema/persistence mechanism;
- an executable reference implementation and independent comparison implementation;
- deterministic semantic comparison oracle.

## 8. [ABSENCE DE PREUVE]

The repository currently establishes the universal architecture and contract rules, but the reviewed evidence does not establish the complete concrete input/binding/artifact set required to execute this final smoke.

Therefore no real determinism PASS is claimed.

## 9. VERDICT

```text
Q-RM-12 TEST PROTOCOL / FALSIFIABILITY = PASS
Q-RM-12 EXECUTABLE DETERMINISM RUN = BLOCKED
```

## FIN
