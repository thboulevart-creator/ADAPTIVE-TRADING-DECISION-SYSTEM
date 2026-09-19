# I_A — NATIVE BI5 REFERENCE IMPLEMENTATION CANDIDATE — ADVERSARIAL BREAK

**Date:** 2026-09-19  
**Candidate implementation commit:** `065511e25ad986ff1252da4924e23129fffdda6f`  
**Candidate source blob:** `93601fc155af73f6006af9efeb3705d1254ed386`  
**Qualification runner commit:** `5a0812c000919575db3f4cfbcd770d36670bf70b`

Frozen breaker:

`breakers/native_bi5_ia_reference_qualifier_breaker.py`

Frozen breaker blob:

`64d3a391e1b5cb5aecfdf926551acd3ee5f0d7dd`

## 1. First executable result

Candidate qualification workflow:

```text
run = 35442358489
job = 105895260543
```

All workflow controls passed.

Frozen I_A breaker result:

```text
23 passed in 0.12s
```

This green result is necessary but not sufficient for governed PASS.

The candidate source was therefore attacked beyond the frozen breaker without changing the breaker.

---

## 2. IA-F01 — UNVERIFIED_A08_PROOF_PROMOTION

### Current behavior

The candidate function:

`_matching_terminal_completeness_proof(...)`

accepts a binding as sufficient constructive completeness proof when it contains:

- a matching terminal-fragment target;
- `evidence_role = CONSTRUCTIVE_COMPLETENESS_PROOF`;
- a truthy immutable reference;
- a truthy integrity reference.

The implementation does not independently validate the referenced proof material.

### Attack

Supply a terminal partial fragment plus a fabricated binding with:

```text
matching target
evidence_role = CONSTRUCTIVE_COMPLETENESS_PROOF
immutable_reference = arbitrary non-empty string
integrity_digest_or_reference = arbitrary non-empty string
```

The current implementation promotes:

```text
BI5-A07 QUALIFICATION_BLOCKED
→
BI5-A08 REJECT_RECORD
```

without establishing constructive completeness.

That can incorrectly preserve preceding slots and allow a qualified universe.

### Why this violates the governed contract

A08 requires actual constructive completeness/locality proof.

A decision label or unresolved evidence reference is not the proof itself.

The implementation must fail closed when the proof cannot be independently validated.

### Verdict

```text
IA-F01 = FAIL
```

Minimal correction:

Until an independently qualified evidence verifier exists, I_A must not promote a terminal remainder to A08 merely from self-described binding fields.

Unverified remainder:

`BI5-A07 → QUALIFICATION_BLOCKED`.

---

## 3. IA-F02 — NONQUALIFIED_PARTIAL_SEMANTIC_LEAK

### Current behavior

When a later component blocks qualification, `_blocked_result(...)` may preserve earlier:

`source_accounting`

entries whose disposition is:

`CANDIDATE_RETAINED`.

The result correctly sets:

```text
semantic_status = QUALIFICATION_BLOCKED
freeze_status = NOT_CREATED
qualified_occurrences = null
```

but the top-level semantic accounting field can still expose prefix retention-like dispositions.

Separately, `validate_implementation_result(...)` does not universally require:

`qualified_occurrences = null`

for every non-`COMPLETED + QUALIFIED + FROZEN` state.

### Attack A — blocked prefix

Component 1 yields valid candidates.

Component 2 yields A06 zero-decompressed-bytes.

Current result can be:

```text
QUALIFICATION_BLOCKED
qualified_occurrences = null
source_accounting = prefix entries marked CANDIDATE_RETAINED
```

That accounting is not clearly isolated into non-normative diagnostic evidence.

### Attack B — noncompleted execution with payload

Construct a sealed result with:

```text
execution_status = ENVIRONMENT_BLOCKED
semantic_status = NOT_REACHED
freeze_status = NOT_REACHED
qualified_occurrences = non-null tuple
```

The current validator checks the three status axes but lacks a universal no-partial-universe invariant for this combination.

### Contract consequence

The boundary requires:

```text
partial qualified universe forbidden
for every state other than
COMPLETED + QUALIFIED + FROZEN
```

### Verdict

```text
IA-F02 = FAIL
```

Minimal correction:

- nonqualified/noncompleted results expose no top-level qualified/source-accounting universe;
- prefix physical diagnostics, if retained, must live only under explicitly non-normative terminal evidence;
- validator must enforce the universal no-partial-universe invariant.

---

## 4. IA-F03 — PRESEAL_ALLOWLIST_NOT_ENFORCED

### Current behavior

The candidate verifies:

```text
workspace exists
other-path output unreadable
network = DENY
IPC = DENY
cache = PRIVATE_ONLY
```

but does not require the declared pre-seal input/read allowlist and environment-variable allowlist to match the governed closed boundary.

`_isolation_evidence(...)` constructs `runtime_read_set` as the intersection of required channel names with whatever allowlist is supplied.

### Attack

Provide:

```text
preseal_input_allowlist = ()
environment_variable_allowlist = arbitrary semantic channel names
other isolation fields = acceptable
```

The current implementation may still execute semantic qualification.

The empty runtime read set is trivially a subset of the empty allowlist, so self-reported evidence does not fail.

### Contract consequence

The implementation must not execute when the pre-seal channel declaration itself is incomplete or admits an ungoverned semantic channel.

### Verdict

```text
IA-F03 = FAIL
```

Minimal correction:

Require the exact currently governed synthetic execution allowlists:

```text
preseal inputs =
common_immutable_input_package
own_implementation_runtime
python_stdlib

environment variables =
PYTHONHASHSEED
TZ
LANG
LC_ALL
```

No semantic channel may be added by implementation convenience.

---

## 5. IA-F04 — SEAL_INTEGRITY_WITHOUT_SEMANTIC_VALIDITY

### Current behavior

`is_sealed_implementation_result(...)` checks only whether the deterministic digest matches the result payload.

It does not independently enforce the status/freeze/partial-universe invariants.

### Attack

Because the abstract result schema and sealing algorithm are public and deterministic, construct a contradictory result such as:

```text
execution_status = COMPLETED
semantic_status = QUALIFICATION_BLOCKED
freeze_status = FROZEN
```

then compute the corresponding integrity digest.

Current `is_sealed_implementation_result(...)` can report a valid seal even though `validate_implementation_result(...)` would reject the semantic state.

### Contract consequence

The seal is integrity evidence, not semantic authority, but the public predicate named as a sealed-result validity check must not allow an invalid semantic state to masquerade as a valid implementation result.

### Verdict

```text
IA-F04 = FAIL
```

Minimal correction:

Factor structural/status validation independently from seal validation, and require both for:

`is_sealed_implementation_result(...)=True`.

---

## 6. Attacks that survived

The following behaviors survived the adversarial inspection and frozen breaker:

- exact public surface and schema;
- exact candidate IDs/versions;
- single LZMA-Alone envelope with trailing-data rejection;
- byte-zero / 20-byte framing;
- `>IIIff` field interpretation;
- exact timestamp reconstruction;
- exact rational price numerator with denominator 1000;
- exact finite binary32 odd-coefficient normalization;
- signed-zero collapse;
- A09 local millisecond rejection;
- A10 non-finite-volume rejection;
- zero/crossed price retention;
- finite negative volume retention;
- strict duplicate preservation;
- no timestamp sorting;
- complete-slot source accounting on qualified synthetic inputs;
- no filename-derived hour substitution;
- determinant presence/shape fail-closed behavior;
- result mutation invalidates the existing seal;
- no I_B import;
- no external acquisition/trading surface.

---

## 7. Initial adversarial verdict

```text
I_A REFERENCE IMPLEMENTATION CANDIDATE
FAIL
```

Demonstrated internal defects:

```text
IA-F01 — UNVERIFIED_A08_PROOF_PROMOTION
IA-F02 — NONQUALIFIED_PARTIAL_SEMANTIC_LEAK
IA-F03 — PRESEAL_ALLOWLIST_NOT_ENFORCED
IA-F04 — SEAL_INTEGRITY_WITHOUT_SEMANTIC_VALIDITY
```

The fact that the frozen breaker is green does not override these demonstrated defects.

No upstream D/R/M/B/A/Q/F contract change is authorized.

No breaker weakening is authorized.

---

## 8. External limitations not reclassified as internal defects

This candidate still operates on the synthetic common-input abstraction defined by the frozen breaker.

The current block does not claim that it has independently resolved:

- real D acquisition materialization/completeness evidence;
- provider-independent proof of B/A source semantics;
- actual normative determinant-content materialization from real acquisition inputs.

Those remain reasons the global concrete gate stays BLOCKED.

They are not repaired by inventing real-data logic inside I_A.

---

## 9. Exactly authorized correction

Correct only IA-F01..IA-F04 in:

`src/native_bi5_reference_qualifier.py`.

Then:

1. persist corrected I_A;
2. update only the candidate runner's source blob lock;
3. execute the unchanged frozen breaker;
4. re-attack IA-F01..IA-F04 and the full existing attack matrix;
5. perform persisted-HEAD final re-break;
6. only then pronounce the implementation-layer verdict.

I_B remains absent.

No real BI5 acquisition, processing or backtest is authorized.
