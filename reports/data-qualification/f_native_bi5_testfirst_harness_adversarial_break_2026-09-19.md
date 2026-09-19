# F — NATIVE BI5 FREEZE-PERSISTENCE TEST-FIRST HARNESS — ADVERSARIAL BREAK

**Date:** 2026-09-19
**Candidate breaker/workflow commit:** 82d65e33c88c09d3f7507b953c8239d15dd7dce6

Breaker:

breakers/native_bi5_f_freeze_persistence_breaker.py

Initial breaker blob:

612139be940c6bebd56f69e1d3bb1042e42bebba

Workflow:

.github/workflows/native-bi5-f-freeze-persistence-preimplementation.yml

Initial workflow blob:

2dae20e7a59dc81455640f216cf4aa0313835ec7

Production F runtime:

src/native_bi5_freeze_persistence.py = ABSENT

Production O implementation = ABSENT

No real BI5 input, acquisition or backtest was used.

---

## 1. Initial executable RED baseline

Workflow: Native BI5 F Freeze Persistence Preimplementation RED

~~~text
run = 35453046792
job = 105923426481
~~~

Controls outside the breaker:

~~~text
exact persisted HEAD / F-contract / breaker locks = PASS
F production runtime absent                       = PASS
O implementation absent                           = PASS
qualification environment                         = PASS
clean worktree                                    = PASS
~~~

Breaker execution is RED.

Every collected test setup reports exactly:

~~~text
F runtime absent — expected pre-implementation RED:
src.native_bi5_freeze_persistence does not exist
~~~

No production F runtime was created to obtain this baseline.

The RED state is necessary but does not by itself qualify the harness.

---

## 2. FTF-F01 — SOURCE_TO_LOGICAL_CORRUPTION_ATTACK_NOT_INDEPENDENTLY_FALSIFIABLE

The synthetic input contains retained occurrences with source witnesses and source-accounting dispositions, but no separate upstream B candidate source→logical relation.

A source-witness swap can therefore remain internally self-consistent. A validator cannot reconstruct the original B source→payload mapping from the mutated F artifact alone.

Verdict:

~~~text
FTF-F01 = FAIL
~~~

Minimal correction: add synthetic b_candidate_occurrences as the authoritative pre-Q source→logical mapping. Attack the Q-retained mapping while leaving B candidates unchanged. F must emit NOT_CREATED.

---

## 3. FTF-F02 — A08 ATTACK CONFLATES TWO DIFFERENT VIOLATIONS

The current A08 fixture simultaneously puts a terminal-fragment anomaly into complete-slot accounting and omits the required qualification evidence binding.

A defective runtime could therefore pass by rejecting only the accounting-shape contradiction while ignoring the missing A08 evidence.

Verdict:

~~~text
FTF-F02 = FAIL
~~~

Minimal correction: create a component with complete_slot_count=2, a separate terminal_fragment object, two retained complete slots, and an A08 anomaly targeting only that fragment with qualification_evidence_bindings empty. The intended failure is then isolated.

---

## 4. FTF-F03 — ORDER / TEMPORAL ATTACKS ARE PARTLY OVERCONSTRAINED AND PARTLY UNDERCOVERED

The current timestamp test requires build output to preserve the producer's unsorted occurrence array. F forbids normative temporal authority, not every possible deterministic container ordering.

At the same time, component order and anomaly order are not actually attacked because the fixture contains only one component and at most one anomaly.

Verdict:

~~~text
FTF-F03 = FAIL
~~~

Minimal correction:
- do not require build output to preserve input timestamp order;
- instead reorder a valid artifact into a timestamp regression and require validation to accept it;
- add valid two-component and multi-anomaly fixtures;
- reverse component/anomaly/accounting/occurrence arrays independently and require validation to remain valid.

---

## 5. FTF-F04 — MATERIALIZATION / COMPLETENESS / Q-PARAMETER GAPS

The breaker does not explicitly attack missing D completeness evidence, non-materialized declared components, or missing qualification parameters that F must bind.

Verdict:

~~~text
FTF-F04 = FAIL
~~~

Minimal correction: add separate NOT_CREATED attacks for each missing or incomplete condition.

---

## 6. FTF-F05 — RED BASELINE DOES NOT PROVE COLLECTION INDEPENDENTLY OF RUNTIME ABSENCE

The workflow proves runtime absence and then executes pytest RED, but has no separate collection-only proof.

A syntax/collection defect could therefore be confused with the expected RED without manual log inspection.

Verdict:

~~~text
FTF-F05 = FAIL
~~~

Minimal correction: run pytest --collect-only -q on the breaker before the intentionally RED execution.

---

## 7. Attacks already structurally present

The first candidate already covers qualified/non-qualified artifact classes, partial-universe leakage, missing reconstruction determinant, conflicting determinant binding, accounting gap, candidate/reject overlap, terminal-fragment accounting, anomaly relation preservation, occurrence multiplicity, binary32 normalization, signed zero, witness identity leakage, JSON whitespace/key order, byte-hash non-authority, determinant-content change, malformed F count and permission leakage.

These remain subject to the corrected fixture model and final re-break.

---

## 8. Initial harness verdict

~~~text
F TEST-FIRST FREEZE-PERSISTENCE BREAKER / HARNESS
FAIL
~~~

Demonstrated defects:

~~~text
FTF-F01 — SOURCE_TO_LOGICAL_CORRUPTION_ATTACK_NOT_INDEPENDENTLY_FALSIFIABLE
FTF-F02 — A08_ATTACK_CONFLATES_TWO_DIFFERENT_VIOLATIONS
FTF-F03 — ORDER_TEMPORAL_ATTACKS_OVERCONSTRAINED_AND_UNDERCOVERED
FTF-F04 — MATERIALIZATION_COMPLETENESS_Q_PARAMETER_GAPS
FTF-F05 — NO_INDEPENDENT_COLLECTION_PROOF
~~~

Exactly authorized next correction: correct FTF-F01..FTF-F05 only, keep F runtime absent, keep O absent, rerun the persisted RED baseline, then adversarially re-break the harness.

No production F/O implementation is authorized.

---

## 9. Residual re-break after first correction

First correction commit:

f57e64e22e353682d97defe76ecc42a771433b25

Corrected breaker blob:

e5898e1358908541d0603413d282b42302a667f7

Corrected workflow blob:

bbc951abc5557d5e64c862ce65e323a3886b47c2

Executable result:

~~~text
run = 35453243248
job = 105923939847
collection = 35 tests collected / PASS
execution  = RED
all test setups = expected missing F runtime
~~~

FTF-F01..FTF-F05 are materially corrected.

Further attack of the harness itself demonstrates the following residuals.

### FTF-R01 — ORDER TESTS MUTATE A POST-CONSTRUCTION ARTIFACT

The current component/anomaly/timestamp-order tests reorder arrays after build and then call validate_freeze_artifact.

If the future F artifact carries legitimate physical immutability/integrity evidence, any post-construction mutation may be rejected even when the changed array order is semantically irrelevant.

This conflates:

~~~text
semantic order non-authority
with
physical persisted-artifact mutation
~~~

Verdict: FTF-R01 = FAIL.

Correction: create independently built artifacts from permuted but semantically equivalent input packages, then compare breaker-owned semantic projections. Do not require an already-built artifact to remain integrity-valid after mutation.

### FTF-R02 — POSITIVE RECONSTRUCTIBILITY IS NOT EXPLICITLY ASSERTED

The harness attacks missing completeness evidence and missing Q parameters, but a runtime could validate those inputs and then omit them from the frozen qualified universe.

F requires the persisted state to bind enough information to reconstruct the exact qualification state.

Verdict: FTF-R02 = FAIL.

Correction: the positive qualified test must assert persistence of the complete D/R/M/B/A/Q/F reconstruction tuple, acquisition-domain identity, D completeness evidence, component snapshot, qualification parameters, source accounting, anomaly relation and retained occurrence relation.

### FTF-R03 — OBJECT-KEY ORDER IS NOT ACTUALLY VARIED

Compact versus pretty JSON changes whitespace but does not necessarily change object-key insertion order.

Verdict: FTF-R03 = FAIL.

Correction: independently reserialize an equivalent artifact with recursively reversed object-key insertion order and require deserialize/validation to preserve the same breaker-owned semantic projection.

### FTF-R04 — B-CANDIDATE RELATION MAY STILL BE DEFAULTED FROM Q RETAINED OUTPUT

The corrected fixture now provides b_candidate_occurrences, but there is no attack removing that input entirely.

A future runtime could silently substitute retained_occurrences when the B candidate relation is missing, defeating the purpose of FTF-F01.

Verdict: FTF-R04 = FAIL.

Correction: missing b_candidate_occurrences on QUALIFIED input must produce NOT_CREATED.

### FTF-R05 — TERMINAL NON-FREEZE EVIDENCE IS NOT REQUIRED POSITIVELY

The terminal tests assert class/state/null-universe, but do not require a non-null terminal evidence payload binding the reason/outcome.

Verdict: FTF-R05 = FAIL.

Correction: require terminal_evidence to exist for QUALIFICATION_BLOCKED and ACQUISITION_REJECTED while remaining clearly non-freeze.

---

## 10. Second authorized correction

Correct only FTF-R01..FTF-R05.

Keep F runtime absent and O absent.

Then perform a fresh persisted-head collection + RED execution and a final adversarial re-break before any harness PASS.

---

## 11. Residual re-break after second correction

Second correction commit:

1a944616eb73f7d1c0a52dc656386f5f18f780e3

Breaker blob:

9ef3fe902403b06dbc96bddc94c51c32a9da1462

Workflow blob:

236fc37f1b6ec53600142fc90b91deb368f65116

Executable result:

~~~text
run = 35453372575
job = 105924284280
collection = 36 tests / PASS
execution  = expected RED only because F runtime is absent
~~~

### FTF-R06 — CANDIDATE/REJECT OVERLAP ATTACK STILL HAS A SECOND FAILURE CAUSE

The overlap attack adds slot 2 to retained_occurrences but does not add the same slot to the independently specified b_candidate_occurrences relation.

A runtime can therefore reject only because the retained mapping lacks B authority, while ignoring the intended contradiction that one B candidate slot is simultaneously targeted by REJECT_RECORD.

Verdict: FTF-R06 = FAIL.

Correction: add the exact slot-2 candidate to both B candidate occurrences and Q retained occurrences while source accounting/anomaly still reject the same slot.

### FTF-R07 — POSITIVE RECONSTRUCTION SNAPSHOT IS NOT YET EXACT ENOUGH

The positive qualified test proves stage presence and component IDs, but not exact preservation of every determinant immutable reference/integrity digest and every component snapshot field.

A runtime could validate those inputs, then persist a lossy reconstruction and still satisfy the current assertions.

Verdict: FTF-R07 = FAIL.

Correction: compare the complete reconstruction tuple and complete component snapshot as unordered exact relations.

### FTF-R08 — BLOCKED A06 FIXTURE HAS CONTRADICTORY FRAMING METADATA

The QUALIFICATION_BLOCKED terminal fixture declares BI5-A06 ZERO_DECOMPRESSED_BYTES but leaves complete_slot_count=3 in the component snapshot.

A correct runtime may terminalize because of that contradiction rather than because it correctly persists the blocked Q outcome.

Verdict: FTF-R08 = FAIL.

Correction: for the blocked A06 fixture set complete_slot_count=0 and no terminal fragment.

### FTF-R09 — OUTPUT KEY-ORDER TEST CAN CONFLATE SEMANTICS WITH PHYSICAL INTEGRITY

The current test manually reserializes an already-built artifact with reversed object keys and then requires full validation.

If a future persisted artifact carries legitimate physical-instance integrity evidence, such manual byte mutation may invalidate that physical instance even though object-key order remains semantically irrelevant.

Verdict: FTF-R09 = FAIL.

Correction:
- test key-order non-authority by building from an input mapping whose key insertion order is recursively reversed and compare breaker-owned semantic projections;
- keep pretty/compact serialization as evidence that byte hashes can differ;
- do not require arbitrary post-persistence byte mutation to remain physical-integrity valid.

---

## 12. Third authorized correction

Correct only FTF-R06..FTF-R09, keep F and O production implementations absent, then perform the final persisted-head collection/RED re-break.
