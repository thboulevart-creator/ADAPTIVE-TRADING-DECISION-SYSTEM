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
