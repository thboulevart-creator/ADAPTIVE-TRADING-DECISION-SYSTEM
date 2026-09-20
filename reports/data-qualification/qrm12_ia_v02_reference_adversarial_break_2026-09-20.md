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


---

## 6. Second adversarial re-break after IA2-F01..F06 correction

Corrected source commit:

`86ad991a28f4012ccbb8f0a98c20080546175b0f`

Corrected source blob:

`bba5c38a8e49103bb041f61805888a51009d56c4`

Targeted frozen-contract evidence:

```text
run = 35497770165
job = 106043878724
9 tests collected
9 passed
```

Initial adversarial suite after correction:

```text
run = 35497770201
job = 106043879182
7 tests collected
7 passed
```

The adversarial breaker was then extended without modifying the frozen Q-RM-12 breaker.

Extended adversarial breaker blob:

`cde59a15e678c3e60a5cee0621a6596d9d244588`

Extended re-break commit:

`c707469658e4f66e9e2ed6bf3393ba1689865e46`

Extended re-break:

```text
run = 35497850364
job = 106044108167

12 tests collected
7 passed
5 failed
locks / environment / clean worktree = PASS
```

## 7. Residual demonstrated defects

### IA2-R01 — NONJSON_ISOLATION_CONTEXT_ESCAPES_ENVIRONMENT_FAIL_CLOSED

A non-string value inside the pre-seal allowlist correctly made the environment invalid, but the same raw bytes were copied into `isolation_evidence` and result sealing crashed.

Required correction:

- isolation evidence must remain strict-JSON serializable even when the supplied execution context is malformed;
- malformed context must still yield `ENVIRONMENT_BLOCKED / NOT_REACHED / NOT_REACHED`.

### IA2-R02 — NONJSON_D_COMPLETENESS_MISCLASSIFIED_AS_IMPLEMENTATION_ERROR

D completeness evidence with valid required fields plus an opaque bytes value passed common-input validation and failed only while constructing/sealing F.

Required correction:

- validate persisted D completeness evidence for strict JSON during common-input validation;
- reject as `COMPLETED / QUALIFICATION_BLOCKED / NOT_CREATED`.

### IA2-R03 — RESEALED_OPEN_ISOLATION_EVIDENCE_IS_LOCALLY_ACCEPTED

A qualified result with `network_policy = ALLOW`, resealed after the mutation, remained valid under `is_sealed_implementation_result_v2`.

Required correction:

- locally valid completed/qualified results must carry closed isolation evidence;
- environment-blocked evidence remains intentionally non-closed.

### IA2-R04 — PRIVATE_F_VALIDATOR_ACCEPTS_BOOLEAN_SLOT_INDEX

Because Python bool is an int subtype and `False == 0`, a forged F artifact could use `False` as slot index in accounting and occurrence witnesses and still pass the private validator.

Required correction:

- explicitly reject bool for source-accounting and occurrence-witness slot indexes.

### IA2-R05 — PRIVATE_F_VALIDATOR_ACCEPTS_NONCANONICAL_TIMESTAMP_WIDTH

The private F validator accepted `.0Z` fractional seconds although the qualified F normal form requires exactly millisecond-width `.mmmZ`.

Required correction:

- require exact `YYYY-MM-DDTHH:MM:SS.mmmZ` syntax before datetime parsing.

## 8. Updated verdict before residual correction

```text
Q-RM-12 I_A V0.2 REFERENCE COMPATIBILITY CANDIDATE = FAIL
```

Only IA2-R01..IA2-R05 are authorized for the next correction.
