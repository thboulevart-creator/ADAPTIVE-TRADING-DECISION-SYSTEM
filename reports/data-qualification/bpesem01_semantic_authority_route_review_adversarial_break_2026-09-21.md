# B-PE-SEM-01 — ADVERSARIAL BREAK OF PERSISTED CANDIDATE

**Date:** 2026-09-21  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Persisted candidate HEAD attacked:** `af0a078732d0ed02e747f83cc70a660af729ffc4`  
**Candidate blob:** `da888021276851c872f4b175ec6021d51c3efa70`

## Verdict

```text
B-PE-SEM-01 candidate adversarial break = FAIL
```

The selected high-level route remains plausible, but the persisted candidate is not yet sufficiently closed for qualification.

No provider contact, provider GET, FULL_INTERVAL execution, D materialization or backtest occurred.

## Demonstrated defects

### BPESEM01-F01 — PREEXECUTION / FULL-INTERVAL CIRCULARITY IN SIGNEDNESS EQUIVALENCE

The candidate says the signed/unsigned ambiguity may be neutralized when the high bit is zero on every accepted target-domain record.

That mathematical equivalence is valid, but the candidate does not separate:

```text
authority of the conditional rule before execution
from
evidence that every future record satisfies the rule
```

If current-authority semantics required the full-domain observation before FULL_INTERVAL may start, the proposed route would remain circular.

Required correction:

```text
pre-execution authority may qualify the conditional semantic rule:
  high-bit-zero -> signed/unsigned numeric equivalence
  high-bit-one -> BLOCKED

FULL_INTERVAL later evaluates the condition per record.
```

The rule may be current authority before the data satisfy it; the execution result cannot.

### BPESEM01-F02 — SEMANTIC ANCHOR CLASS IS NOT CLOSED PROSPECTIVELY

The candidate gives examples of possible future anchors, but does not define a closed admissibility contract.

This permits post-hoc source selection after seeing which interpretation is convenient.

Required correction:

Before any semantic discrimination execution, a successor contract must seal:

```text
anchor class
anchor source identity
anchor lineage requirements
anchor capture/materialization policy
target claim/dimension
candidate interpretation set
expected discriminating observation
contradiction rule
```

Unknown/unsealed anchors cannot be introduced after observing candidate results.

### BPESEM01-F03 — COMPETING-HYPOTHESIS UNIVERSE IS NOT IDENTITY-BOUND

“Predeclare competing envelope hypotheses” is insufficient without exact immutable hypothesis identities and decision rules.

Required correction:

Each material ambiguity must have a sealed `SemanticHypothesisSet` containing exact hypothesis IDs, interpretation functions or normative descriptions, expected discriminators, and ambiguity disposition.

A hypothesis may not be added, removed or edited after evidence is observed without reopening the adjudication.

### BPESEM01-F04 — SEMANTIC RULE AUTHORITY AND CAPTURE SATISFACTION ARE CONFLATED

B-FIQ needs semantic rules to know what to test, while FULL_INTERVAL evidence later determines whether provider captures satisfy those rules.

The candidate does not name these as separate artifacts/states.

Required correction:

Separate:

```text
OperationalSemanticRuleAdjudication
from
QualificationExecutionResult
```

The former may authorize decisive invariants before exhaustive execution.
The latter records whether the capture set passes them.

Neither may substitute for the other.

### BPESEM01-F05 — EXISTING B-ERD-02 PROVIDER-DIRECT BYTES HAVE NO REUSE BOUNDARY

The candidate does not state whether the already captured nine K1 probes may be used by the successor.

That omission risks either needless provider re-contact or silent reuse outside their qualified scope.

Required correction:

Existing B-ERD-02 exact durable probe evidence may be reused only as bounded semantic-discrimination evidence when:

```text
exact capture identities/hashes remain verifiable
provider-origin binding remains valid
the successor contract explicitly names the reused probes
no full-domain continuity claim is inferred
no B-PE-01R C08 authority is silently transferred to C01-C07
```

### BPESEM01-F06 — C05-D3 / C06-D3 REPLACEMENTS ARE NOT FORMALLY SPECIFIED

The candidate correctly observes that “provider-owned metadata must exist” is an evidence-method requirement rather than the semantic content itself, but it does not freeze the substitute operational propositions.

Required correction:

Define at least:

```text
C05-D3-OP:
no unresolved prerequisite semantic state remains between raw side fields
and the qualified price conversion

C06-D3-OP:
the /1000 scale is supported by an admissible, non-circular
OperationalSemanticRuleAdjudication whose evidence path is identity-bound
and contradiction-sensitive
```

These are not documentary PASSes for original C05-D3/C06-D3.

### BPESEM01-F07 — B-FIQ AUTHORITY REFRESH LACKS EXACT REOPEN EFFECT

The candidate says B-FIQ must later be refreshed, but does not state what happens to the currently sealed B-FIQ-02 package.

Required correction:

Any semantic authority identity change must force:

```text
current B-FIQ-02 SemanticInvariantManifest -> historical only
current provisional authority_scope_tuple -> historical only
pre-execution eligibility -> remains BLOCKED
new governed rematerialization/reseal required
```

No field-in-place reinterpretation is allowed.

### BPESEM01-F08 — NON-PROJECT REFERENCE IMPLEMENTATION COULD STILL BE A COMMON-PREMISE ANCHOR

The candidate permits an exact version-pinned non-project reference implementation when expected meaning is independently established, but does not require proof of that independent establishment.

Required correction:

A reference implementation alone may support physical compatibility but cannot be the sole semantic anchor for timestamp meaning, side meaning, price scale or volume meaning unless its semantic source lineage is separately established and independent of the candidate project interpretation.

## Non-defects confirmed

The break did NOT demonstrate a defect in these candidate conclusions:

```text
B-PE-01/BPE02 documentary axis must remain unchanged
B-PE-01R C08-only supersession cannot be reused silently
C01/C02 operational semantics remain required
C04 timestamp semantics remain required
C06 target price scale remains required
C07 remains required under the current logical payload
two-decoder agreement alone is insufficient
plausibility alone is insufficient
```

## Required next correction

Correct only F01-F08.

Do not broaden into provider execution or B-FIQ rematerialization.

STOP.
