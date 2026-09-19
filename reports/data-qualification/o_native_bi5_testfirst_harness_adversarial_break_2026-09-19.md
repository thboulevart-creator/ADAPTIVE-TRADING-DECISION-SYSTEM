# O — NATIVE BI5 SEMANTIC-COMPARATOR TEST-FIRST HARNESS — ADVERSARIAL BREAK

**Date:** 2026-09-19  
**Initial breaker/workflow commit:** `89c060d2ea24f67030707d662ae1097a8319c6a6`

Breaker:

`breakers/native_bi5_o_semantic_comparator_breaker.py`

Initial breaker blob:

`8fad392da525f46641c60a194b33c1040da3a9b0`

Workflow:

`.github/workflows/native-bi5-o-semantic-comparator-preimplementation.yml`

Initial workflow blob:

`151da16291bd7970fdd3f03e72c34849ca2a9617`

F source remains:

`src/native_bi5_freeze_persistence.py`

blob:

`199b07929fe8ec40d719b001b0321d1f26c8faab`

O production runtime:

`src/native_bi5_semantic_universe_comparator.py = ABSENT`

No real BI5 input, acquisition or backtest was used.

---

## 1. Initial executable RED baseline

Workflow:

`Native BI5 O Semantic Comparator Preimplementation RED`

Run:

```text
run = 35456941833
job = 105933804252
```

Controls:

```text
exact HEAD / F source / F-O contract / O breaker locks = PASS
O production runtime absent                            = PASS
qualification environment                              = PASS
pytest collection                                      = 27 tests / PASS
clean worktree                                         = PASS
```

Breaker execution is intentionally RED.

Every collected test setup stops only at:

```text
O runtime absent — expected pre-implementation RED:
src.native_bi5_semantic_universe_comparator does not exist
```

No syntax, collection, environment or unrelated import failure is present.

The RED baseline is necessary but does not qualify the harness.

---

## 2. OTF-F01 — COMPONENT_MEMBERSHIP_DIFFERENCE_EXPECTATION_VIOLATES_COMPARABILITY_GATE

Initial test:

`test_b4_component_membership_difference_is_semantic_different`

expects:

```text
different D component membership
→ SEMANTIC_DIFFERENT
```

while both artifacts intentionally retain the same:

```text
D normative id
D normative version
D integrity digest
acquisition_domain_id
```

This is not an ordinary same-state semantic divergence.

O section 15 requires the same materialized acquisition identity/input state before semantic comparison.

Therefore different component membership under the same determinant binding is contradictory evidence and must not be treated as a clean comparable state.

### Verdict

```text
OTF-F01 = FAIL
```

### Minimal correction

Replace the expectation with a fail-closed comparability result:

```text
oracle_result = BLOCKED
qualified_universe_comparison = BLOCKED
```

and require a reason/scope that makes clear the acquisition state is contradictory/non-comparable.

A true component-membership `SEMANTIC_DIFFERENT` case cannot be fabricated while also claiming the exact same materialized D state.

---

## 3. OTF-F02 — REPARTITION_TEST_INVENTS_A_COMPARABLE_STATE

Initial test:

`test_b5_physical_repartition_equivalence_is_not_invented`

constructs another valid F artifact with a different physical component partition while preserving the logical payload bag and expects `SEMANTIC_DIFFERENT`.

But current B V0.1 explicitly declares no general physical repartition-equivalence transform.

For Q-RM-12 same-state comparison, the exact D/B materialization relation is part of the state.

A different physical partition cannot be silently promoted to an alternate comparable representation of the same input.

### Verdict

```text
OTF-F02 = FAIL
```

### Minimal correction

The harness must require:

```text
qualified_universe_comparison = BLOCKED
```

for an invented physical repartition under the current B version.

This proves O does not manufacture equivalence authority.

---

## 4. OTF-F03 — ANOMALY_RELATION_ATTACK_NOT_INDEPENDENTLY_IDENTIFIABLE

Initial test:

`test_b3_anomaly_semantic_relation_difference_is_different`

compares:

- a no-rejection artifact;
- an A10-rejection artifact.

This changes simultaneously:

- source accounting;
- retained occurrence cardinality;
- source→logical relation;
- anomaly semantic relation.

An implementation that ignores the anomaly relation entirely can still pass by detecting the other differences.

For the currently qualified F candidate, an isolated valid anomaly-only mutation is not freely available because F enforces the exact reject-accounting ↔ anomaly relation.

### Verdict

```text
OTF-F03 = FAIL
```

### Minimal correction

Use two valid local-reject artifacts targeting the same exact slot:

```text
left  = A09 / REJECT_RECORD
right = A10 / REJECT_RECORD
```

with the same retained cardinality and target slot.

Rename the test to make clear it attacks the complete rejected-source semantic relation.

Also add a malformed anomaly-only mutation and require O to BLOCK it at the F-validity gate rather than compare it.

Do not claim an independently isolated anomaly-only valid state that current F cannot produce.

---

## 5. OTF-F04 — SECOND_LEGITIMATE_VERSION_BRANCH_CANNOT_BE_FABRICATED

The contract contains:

```text
different legitimate qualification-relevant version
→ DISTINCT_QUALIFICATION_STATE
→ qualified-universe comparison BLOCKED
```

The repository currently contains only one qualified concrete F/D/R/M/B/A/Q version tuple.

Creating a second version string in the breaker and calling it “legitimate” would be a self-attested authority bypass.

The initial harness correctly rejects an unqualified synthetic Q-v2 mutation as invalid, but it does not explicitly record that the positive distinct-version branch is currently non-executable.

### Verdict

```text
OTF-F04 = FAIL
```

### Minimal correction

Keep:

```text
unqualified version mutation
→ INVALID_F_INPUT / BLOCKED
```

and use a genuine current-contract parameter difference to exercise:

```text
DISTINCT_QUALIFICATION_STATE / BLOCKED
```

Record explicitly in the harness baseline that the **positive second-legitimate-version fixture is deferred** until a separately qualified second normative version exists.

No fake “legitimate v2” fixture may be introduced.

---

## 6. OTF-F05 — FROZEN_F_HARNESS_DEPENDENCIES_NOT_FULLY_HASH_LOCKED

The O breaker imports synthetic fixture helpers from:

`breakers/native_bi5_f_freeze_persistence_breaker.py`

but the initial O workflow locks only:

- F production source;
- F/O contract;
- O breaker.

Therefore a later mutation of the frozen F breaker could alter O fixtures without invalidating the O workflow lock.

The checkpoint also requires F and its qualified breakers to remain unchanged during O test-first work.

### Verdict

```text
OTF-F05 = FAIL
```

### Minimal correction

Lock both:

```text
breakers/native_bi5_f_freeze_persistence_breaker.py
= 3d9eb75c2f4e988c984da67af0af344d3dc24148

breakers/native_bi5_f_freeze_persistence_adversarial.py
= c4c499d5e76e15a8fdcaeb91dde80beadad6487a
```

and add them to the workflow path set.

---

## 7. OTF-F06 — RESULT_NONAUTHORITY_CHECKS_ARE_ONLY_TOP_LEVEL

The initial harness checks that a few canonical/temporal identity keys do not appear at the top level of the comparator result.

A future O implementation could still emit nested:

- canonical occurrence IDs;
- temporal ranks;
- canonical sequence;
- source-witness-as-identity structures.

### Verdict

```text
OTF-F06 = FAIL
```

### Minimal correction

Add a recursive result-key scan for forbidden identity/temporal-authority keys.

---

## 8. OTF-F07 — COMPARATOR_SYMMETRY_AND_INPUT_IMMUTABILITY_UNTESTED

Semantic equality/difference is unordered with respect to which implementation is passed as left or right.

The harness does not yet prove:

```text
compare(A,B) semantic verdict
=
compare(B,A) semantic verdict
```

nor that the pure comparator leaves both input artifacts unchanged.

### Verdict

```text
OTF-F07 = FAIL
```

### Minimal correction

Add:

- symmetry tests for EQUAL, DIFFERENT and BLOCKED conflict cases;
- deep-copy input immutability assertion.

---

## 9. OTF-F08 — DETERMINANT_REFERENCE_CONFLICT_UNTESTED

Section 15 requires comparison of:

```text
normative_id
normative_version
bound immutable content/integrity reference
```

The initial harness attacks only differing `integrity_digest`.

A comparator that ignores `immutable_reference` can still pass.

### Verdict

```text
OTF-F08 = FAIL
```

### Minimal correction

Add a same-id/same-version fixture with changed `immutable_reference` and require:

```text
BLOCKED
NORMATIVE_VERSION_INTEGRITY_CONFLICT
```

---

## 10. Initial harness verdict

```text
O TEST-FIRST SEMANTIC-COMPARATOR BREAKER / HARNESS = FAIL
```

Demonstrated defects:

```text
OTF-F01..OTF-F08
```

Exactly authorized next action:

```text
correct OTF-F01..OTF-F08 only
→ keep O runtime absent
→ keep F source and both qualified F breakers byte-identical
→ persisted collection + expected RED
→ adversarially re-break harness
```

No production O implementation is authorized.


---

## 11. Residual re-break after first correction

First correction commit:

`f3c21a173e07ca712309b9e446d46e9e36cdf432`

Corrected breaker blob:

`ae5f8ce6f2fbec0331dbfe82a7addeeb09ca710a`

Corrected workflow blob:

`40e87cf7469ad122739557bfa4f2f69a07a2659b`

Executable RED:

```text
run = 35457076905
job = 105934161225
collection = 33 tests / PASS
execution = RED only because O runtime is absent
```

F source and both qualified F breakers remained exactly hash-locked.

OTF-F01..OTF-F08 are materially corrected.

Further adversarial review demonstrates the following residual harness defects.

### OTF-R01 — DETERMINANT_CONFLICT_COVERAGE_ONLY_EXERCISES_D

The contract requires O to compare all normative determinant bindings:

```text
D / R / M / B / A / Q / F
```

The corrected harness still tests changed integrity/reference only on D.

A defective O implementation that verifies D but ignores R/M/B/A/Q/F could pass.

Verdict:

```text
OTF-R01 = FAIL
```

Correction:

parameterize same-id/same-version integrity-digest and immutable-reference conflicts across every stage D/R/M/B/A/Q/F.

### OTF-R02 — POSITIVE_DISTINCT_VERSION_BRANCH_IS_EXECUTABLE_AFTER_ALL

The first attack record concluded that no honest second-version fixture could be constructed.

Fresh review of the qualified F runtime shows that D's acquisition materialization version is intentionally supplied by:

`acquisition_declaration_version`

and the D reconstruction binding must match it.

Therefore the breaker can construct two individually F-valid artifacts:

```text
left:
D normative_version = D_MATERIALIZATION_V0_1_SYNTHETIC

right:
D normative_version = D_MATERIALIZATION_V0_2_SYNTHETIC
acquisition_declaration_version = D_MATERIALIZATION_V0_2_SYNTHETIC
```

without inventing a fake R/M/B/A/Q/F contract version or bypassing F validation.

This is sufficient to exercise the positive:

```text
DISTINCT_QUALIFICATION_STATE
→ BLOCKED
```

branch.

Verdict:

```text
OTF-R02 = FAIL
```

Correction:

add this exact F-valid D-version distinction test while retaining the unqualified synthetic Q-v2 mutation as INVALID_F_INPUT.

### OTF-R03 — INVALID_AND_TERMINAL_INPUT_SIDE_ASYMMETRY

The harness currently places malformed/terminal input primarily on the right-hand side.

A comparator could validate only the right artifact and pass most tests.

Verdict:

```text
OTF-R03 = FAIL
```

Correction:

attack terminal and malformed artifacts independently on both left and right.

### OTF-R04 — ACQUISITION_DOMAIN_IDENTITY_GATE_UNTESTED

Same-state comparison requires the same materialized acquisition identity/input state.

The harness attacks component membership but does not independently change:

`acquisition_domain_id`

while keeping each F artifact individually valid.

Verdict:

```text
OTF-R04 = FAIL
```

Correction:

construct a second F-valid artifact with both top-level and acquisition-snapshot domain ID changed, while determinant bindings remain otherwise unchanged, and require:

```text
BLOCKED
NONCOMPARABLE_ACQUISITION_STATE
```

not `SEMANTIC_DIFFERENT`.

### OTF-R05 — TEMPORAL/CANONICAL_RESULT_KEY_SCAN_CAN_BE_EVADED_BY_NEAR-SYNONYMS

The recursive scan is now structurally correct but its forbidden vocabulary remains too narrow.

A comparator could expose semantic authority under names such as:

```text
ordered_occurrences
sorted_occurrences
sequence_position
source_sequence
chronological_rank
```

Verdict:

```text
OTF-R05 = FAIL
```

Correction:

extend the recursive forbidden-key vocabulary to these direct authority aliases.

---

## 12. Second authorized correction

Correct only OTF-R01..OTF-R05.

Keep:

- O runtime absent;
- F source byte-identical;
- both qualified F breakers byte-identical;
- no real BI5 data/acquisition/backtest.

Then perform another persisted collection + RED execution and re-break the harness.
