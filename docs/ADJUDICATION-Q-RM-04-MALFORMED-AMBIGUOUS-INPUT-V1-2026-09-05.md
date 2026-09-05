# ADJUDICATION — Q-RM-04 MALFORMED / AMBIGUOUS INPUT

**Date:** 5 septembre 2026  
**Scope:** qualification outcome for malformed or genuinely ambiguous record-model input under RB-A / Q-RM-01..03  
**Status:** **BLOCKED — NORMATIVE ACQUISITION/RECORD FAILURE POLICY NOT PRESENT IN FROZEN CORPUS**  
**Exclusions:** no `CANONICAL_RECORD_POSITION`, no canonical enumeration, no temporal ordering, no physical identity primitive.

---

## 1. QUESTION

When a physical unit cannot be deterministically interpreted under the applicable versioned record binding, what exact qualification outcome is mandatory?

Candidate outcomes include:

```text
REJECT RECORD
REJECT ACQUISITION
QUALIFICATION BLOCKED
```

The decision must also distinguish:

```text
INVALID
AMBIGUOUS
```

and must prevent either from being silently converted into valid `C = 0`.

---

## 2. ESTABLISHED SEMANTIC RULES

Q-RM-02 established that malformed or ambiguous input is outside numeric cardinality:

```text
INVALID   ≠ C = 0
AMBIGUOUS ≠ C = 0
```

Q-RM-03 established that inability to recognize material as non-observation does not prove that it is non-observation.

The normative logical record-model audit also requires ambiguous input to remain an explicit qualification failure/unknown state rather than being resolved by implementation preference. cite-not-used-in-repo-document

Therefore the following is already closed:

> **No conforming implementation may silently repair, reinterpret, discard, or convert a genuinely invalid/ambiguous input into a valid zero-observation result merely to continue qualification.**

What is **not** closed is the scope of the failure.

---

## 3. FORMALIZATION

For unit `u`, representation `R`, and binding version `B`:

```text
I_B(u) → VALID | INVALID | AMBIGUOUS
```

For `VALID`, Q-RM-02 supplies:

```text
C_B(u) ∈ {0, 1, N}
```

For `INVALID` or `AMBIGUOUS`, the system requires an outcome function:

```text
F_B(u, anomaly_class) → record-local rejection | acquisition rejection | qualification block
```

The corpus does not currently provide a frozen universal definition of `F_B` or an exhaustive anomaly-class matrix.

---

## 4. CANDIDATE OPTIONS

### O1 — Invalidity determined → REJECT RECORD; genuine ambiguity → QUALIFICATION BLOCKED

Advantages:

- preserves usable acquisition content when one record is independently invalid;
- prevents arbitrary resolution of ambiguity;
- keeps local and global failure scopes conceptually distinct.

Unresolved issue:

- not every invalidity is necessarily local; a corrupt framing/header/schema may invalidate interpretation of the acquisition as a whole.

### O2 — Any invalid/ambiguous unit → QUALIFICATION BLOCKED

Advantages:

- maximally conservative;
- prevents qualification from proceeding over unresolved data semantics.

Unresolved issue:

- may make a single independently isolated malformed unit invalidate an otherwise fully interpretable acquisition, without evidence that the project requires this policy.

### O3 — Classify anomaly by normative severity matrix

Under this option, the binding/qualification contract defines anomaly classes and maps each to:

```text
REJECT RECORD
REJECT ACQUISITION
QUALIFICATION BLOCKED
```

Advantages:

- expresses the actual semantic scope of the failure;
- permits local recoverability where proven safe;
- prevents implementation-specific escalation/de-escalation.

Unresolved issue:

- the required anomaly classes and default treatment are not currently frozen in the corpus.

---

## 5. ADVERSARIAL CASSAGE

### C-01 — Treat every malformed record as local

**Failure:** malformed framing, schema, delimiter, encoding, or envelope information can make interpretation of neighboring records impossible. Local rejection would then silently alter the logical universe.

**Result:** O1 cannot be adopted as a universal rule without an anomaly-class boundary.

### C-02 — Block every anomaly globally

**Failure:** an isolated, independently delimited malformed occurrence may not compromise the semantics of the remaining acquisition. Global blocking would be a policy choice, not a logical consequence of RB-A.

**Result:** O2 is conservative but not derivable from the existing frozen constraints.

### C-03 — Parser-dependent recovery

**Failure:** implementation A repairs and continues while implementation B blocks. Same normative input would produce different qualified universes.

**Result:** recovery must be normatively specified, never inferred from parser capability.

### C-04 — Convert anomaly to C=0

**Failure:** silently masks data loss and violates Q-RM-02.

**Result:** forbidden.

### C-05 — Ambiguity resolved by majority/heuristic

**Failure:** the choice between plausible interpretations becomes implementation-dependent.

**Result:** forbidden until the applicable normative contract uniquely resolves the ambiguity.

### C-06 — Continue after ambiguous shared framing

**Failure:** if ambiguity affects record boundaries, later records may have no uniquely defined identity or cardinality.

**Result:** local continuation cannot be assumed safe.

---

## 6. RE-CASSAGE

### RC-01 — "Reject record" is sufficient

Counterexample: a malformed length prefix or delimiter can make the boundary of subsequent records unknowable. The failure is not local.

**Conclusion:** a local reject rule requires an explicit proof that the anomaly is boundary-local and cannot contaminate the remaining acquisition interpretation.

### RC-02 — "Qualification blocked" is always sufficient

Counterexample: a representation can contain independently delimited records where one record is malformed but all other boundaries and semantics remain deterministic. Global blocking is then a stricter policy rather than a necessary semantic consequence.

**Conclusion:** conservative blocking cannot be declared universal without normative authorization.

### RC-03 — Let each binding choose freely

Counterexample: two supported representations could apply incompatible failure scopes to semantically equivalent acquisition failures, making reproducibility and cross-format behavior depend on implementation-specific policy.

**Conclusion:** binding-specific behavior must remain subordinate to a global qualification-failure policy or explicit normative severity matrix.

### RC-04 — Default unclassified anomaly to local rejection

Counterexample: an unclassified anomaly could affect framing or schema interpretation and therefore compromise the entire qualified universe.

**Conclusion:** no safe universal default is derivable from the present corpus.

### RC-05 — Default unclassified anomaly to global block

Counterexample: this may unnecessarily reject otherwise deterministic data, but unlike local recovery it does not invent observations or silently discard an ambiguous interpretation.

**Conclusion:** this may be a viable governance default, but adopting it would be a new normative decision and cannot be presented as already proven by the corpus.

---

## 7. ROBUSTLY CLOSED SUBSET

The following rules are now sufficiently established:

```text
1. INVALID and AMBIGUOUS are not numeric cardinalities.
2. INVALID and AMBIGUOUS must not become C = 0.
3. No silent repair or parser-dependent reinterpretation is permitted.
4. Genuine ambiguity cannot yield a normative qualified universe.
5. Failure scope must be deterministic and versioned.
6. If an anomaly can affect record boundaries beyond the local unit,
   local rejection cannot be assumed safe.
7. If an anomaly is proven independently local, global blocking is not
   logically forced by RB-A alone.
```

---

## 8. BLOCKING NORMATIVE DECISION

The missing decision is:

> **What anomaly classes are record-local, acquisition-fatal, or qualification-blocking, and what is the mandatory default for an anomaly not covered by the matrix?**

This cannot be derived solely from RB-A, Q-RM-02, or Q-RM-03.

It is a genuine upstream qualification-policy decision because it determines whether a physical anomaly changes:

```text
only one candidate occurrence
or
an entire acquisition's qualified universe.
```

Selecting O1, O2, or O3 here without explicit normative authorization would violate the project rule against silently filling normative gaps.

---

## 9. VERDICT

```text
Q-RM-04 SEMANTIC SAFETY RULE = PASS
Q-RM-04 FAILURE-SCOPE POLICY = BLOCKED
```

The semantic prohibition against masking invalidity/ambiguity is closed.

The exact failure-scope policy remains unresolved and blocks a full freeze of the record model.

---

## 10. GOVERNANCE / NEXT ACTION

No implementation repair is authorized.

No `CANONICAL_RECORD_POSITION` is defined.

No enumeration rule is selected.

No `1.1.2` rule is modified.

The next non-derivable question is the upstream acquisition-domain boundary (Q-RM-05), but it must not be used to bypass the unresolved failure-scope policy. Q-RM-06/Q-RM-07 likewise cannot silently supply the missing rule.

## FIN
