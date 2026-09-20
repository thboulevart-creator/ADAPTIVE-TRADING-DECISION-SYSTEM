# Q-RM-12 — I_A V0.2 REFERENCE COMPATIBILITY — ADVERSARIAL BREAK

**Date:** 2026-09-20  
**Candidate source:** `src/native_bi5_reference_qualifier_qrm12.py`  
**Candidate blob:** `a6672982631e5fc9c132fd475335d467dea0e095`  
**Candidate persistence commit:** `59b114a44c6929a3cf3fc354b2421f4af9a7ba9e`  
**Frozen Q-RM-12 breaker:** `967ab86d517cc8736344bb27154641eb9bac7996`

## 1. Candidate baseline

Targeted frozen-contract run:

```text
workflow = Native BI5 Q-RM-12 I_A V0.2 Candidate
run = 35497605829
job = 106043383303

9 tests collected
9 passed
clean worktree = PASS
I_B V0.2 absent = PASS
Q-RM-12 handoff absent = PASS
```

This established only a candidate baseline.

## 2. Adversarial breaker

Breaker:

`breakers/native_bi5_qrm12_ia_v02_adversarial.py`

blob:

`5f5451cd2a4d7ef9dac2ece8d86b9f1ee9f15591`

Workflow:

`Native BI5 Q-RM-12 I_A V0.2 Adversarial`

Run:

`35497690426`

Job:

`106043641458`

Observed:

```text
7 tests collected
1 passed
6 failed
environment / locks / clean worktree = PASS
```

## 3. Demonstrated defects

### IA2-F01 — RESULT_ACQUISITION_NOT_CROSS_BOUND_TO_EMBEDDED_F

A sealed result with a forged `materialized_acquisition_id` remained locally valid while its embedded F artifact still named the original acquisition.

Required correction:

```text
qualified result.materialized_acquisition_id
==
bound_f_artifact.qualified_universe.acquisition_domain_id
```

### IA2-F02 — RESULT_BINDINGS_NOT_CROSS_BOUND_TO_EMBEDDED_F

A sealed qualified result whose R binding digest was changed remained locally valid while the embedded F reconstruction tuple retained the original binding.

Required correction:

- validate the complete result D/R/M/B/A/Q/F/O binding set;
- require exact D/R/M/B/A/Q/F equality with embedded F reconstruction tuple.

### IA2-F03 — EMBEDDED_F_RECONSTRUCTION_CAN_DIVERGE_FROM_RESULT_BINDINGS

A validly resealed F artifact with a changed R integrity digest could be embedded into an otherwise unchanged result and the result still validated.

Required correction:

- exact result/F binding equality at result validation;
- do not reconstruct or repair either side.

### IA2-F04 — PRIVATE_F_VALIDATOR_ACCEPTS_EMPTY_QUALIFIED_COMPONENT_UNIVERSE

The path-private F validator accepted a frozen qualified artifact with:

```text
components = []
source_accounting = []
retained_occurrences = []
b_candidate_occurrences = []
qualified_occurrence_count = 0
```

Required correction:

- qualified F component universe must be non-empty.

### IA2-F05 — MALFORMED_NONJSON_BINDING_ESCAPES_FAIL_CLOSED_PATH

An invalid determinant binding carrying raw bytes correctly failed input validation, but terminal-result sealing then retried the unsafe raw binding and raised:

`TypeError: Object of type bytes is not JSON serializable`

Required correction:

- malformed input must still produce a sealed fail-closed result;
- diagnostic binding preservation must never reintroduce non-strict-JSON values.

### IA2-F06 — NONFINITE_QUALIFICATION_PARAMETER_MISCLASSIFIED_AS_IMPLEMENTATION_ERROR

A `NaN` qualification parameter was accepted by common-input validation, failed later during strict artifact persistence, and was classified as:

`IMPLEMENTATION_ERROR / NOT_REACHED`

This is an input-domain defect, not an implementation failure.

Required correction:

- validate persisted qualification parameters for strict canonical JSON during common-input validation;
- reject as `COMPLETED / QUALIFICATION_BLOCKED / NOT_CREATED`.

## 4. Control

`test_control_valid_result_is_locally_sealed_and_f_valid` passed.

Therefore the adversarial breaker is not merely rejecting every candidate result.

## 5. Verdict before correction

```text
Q-RM-12 I_A V0.2 REFERENCE COMPATIBILITY CANDIDATE = FAIL
```

Scope of correction is limited to IA2-F01..IA2-F06.

Frozen Q-RM-12 breaker must remain unchanged.

Still prohibited:

```text
I_B V0.2 creation
Q-RM-12 handoff creation
real BI5
real acquisition
real backtest
paper/broker/live
```
