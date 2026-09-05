# ADJUDICATION — Q-RM-04 MALFORMED / AMBIGUOUS INPUT — FAILURE-SCOPE POLICY

**Date:** 5 septembre 2026  
**Scope:** normative failure scope for malformed or genuinely ambiguous physical→logical mapping under RB-A / Q-RM-01..03  
**Status:** **PASS — R2 ADOPTED**  
**Independent adjudication:** supplied as adversarial normative review; no implementation preference used.  
**Exclusions:** no `CANONICAL_RECORD_POSITION`, no canonical enumeration, no temporal ordering, no physical identity primitive.

---

## 1. QUESTION

When an anomaly is detected during physical → logical mapping, what normative criterion determines whether its impact is record-local, acquisition-wide, or qualification-blocking?

Candidate outcomes:

```text
O1 — REJECT RECORD
O2 — REJECT ACQUISITION
O3 — QUALIFICATION BLOCKED
```

The policy must preserve the already-closed rules:

```text
INVALID   ≠ C = 0
AMBIGUOUS ≠ C = 0
```

No silent repair, parser preference, heuristic interpretation, or dependence on canonical enumeration is admissible.

---

## 2. INDEPENDENTLY ADJUDICATED RULE

The independent adversarial review proposed and re-broke the following rule:

```text
R2

1. An anomaly is LOCALISABLE iff the applicable versioned
   format binding provides a constructive proof that:
   - boundaries of all other occurrences remain unique and determinable;
   - membership of all other occurrences remains unchanged;
   - no alternative interpretation of the anomaly can modify the
     remainder of the logical universe.

2. If the anomaly is INVALID and LOCALISABLE:
   → REJECT RECORD.

3. In all other cases — including genuine AMBIGUITY, non-localisable
   invalidity, unknown scope, or compromised framing:
   → QUALIFICATION BLOCKED.

4. REJECT ACQUISITION is produced only when the versioned binding
   explicitly declares the anomaly class acquisition-fatal.
```

### Normative interpretation

`LOCALISABLE` is not an implementation judgment. It is a binding-level normative property that must be demonstrated constructively by the applicable versioned binding. A binding that claims localisability while an admissible alternative interpretation can alter the remaining logical universe is non-conforming.

Therefore the policy is deterministic across conforming implementations:

```text
same input + same record-model version + same binding version
→ same anomaly class + same localisability result
→ same qualification outcome
```

---

## 3. ADVERSARIAL CASSAGE

### C-01 — Malformed but perfectly delimited record

A field is invalid, but the binding independently fixes the record boundary and proves neighboring boundaries and membership unaffected.

**Outcome:** `REJECT RECORD`.

No global semantic information is destroyed.

### C-02 — Truncated terminal record

If the binding makes the terminal boundary unambiguous and proves prior occurrences unaffected, the anomaly is localisable.

**Outcome:** `REJECT RECORD`.

If the binding cannot prove this, it is not localisable.

**Outcome:** `QUALIFICATION BLOCKED`.

### C-03 — Missing delimiter / merged records

If the missing delimiter prevents unique determination of the affected boundary or later membership, localisability fails.

**Outcome:** `QUALIFICATION BLOCKED`.

### C-04 — Artificial record creation / extra boundary

If corruption creates uncertainty about occurrence count or boundaries, localisability fails.

**Outcome:** `QUALIFICATION BLOCKED`.

### C-05 — Corrupted global framing

Invalid length prefix, envelope, checksum, or equivalent framing is acquisition-wide only if the binding explicitly classifies it as acquisition-fatal. Otherwise, if its effect on the remaining logical universe cannot be proven local, the result is `QUALIFICATION BLOCKED`.

### C-06 — Unknown anomaly scope

If the binding cannot constructively prove locality, the anomaly is not localisable.

**Outcome:** `QUALIFICATION BLOCKED`.

### C-07 — Anomaly after already interpreted records

Previously interpreted records are not automatically a safe prefix. Keeping them would require a proof that the anomaly cannot affect their boundaries or membership and that the qualification contract permits partial acquisition retention.

Absent that proof, no prefix-only repair is permitted.

### C-08 — Two conforming implementations

Because localisability is defined by the versioned binding rather than parser capability, conforming implementations cannot choose different failure scopes for the same normative input.

---

## 4. WHY O1 / O2 / O3 ARE NOT UNIVERSAL DEFAULTS

### O1 alone — REJECT RECORD

Insufficient. Some anomalies compromise framing, boundaries, or membership beyond one candidate occurrence.

### O2 alone — REJECT ACQUISITION

Not logically forced. An independently delimited invalid occurrence can be rejected without compromising the remainder. Acquisition-wide rejection is therefore a separate normative policy choice.

### O3 alone — QUALIFICATION BLOCKED

Too broad as a universal rule. A proven local invalidity need not block otherwise deterministic qualification.

### Adopted combination

```text
LOCALISABLE INVALID → REJECT RECORD
OTHER UNRESOLVED / NON-LOCALISABLE CASES → QUALIFICATION BLOCKED
EXPLICITLY ACQUISITION-FATAL CLASS → REJECT ACQUISITION
```

This is the only combination surviving the adversarial cases without silently inventing, repairing, or destroying logical membership beyond what the normative evidence requires.

---

## 5. CRITICAL CONFORMANCE CONDITION

The policy closes the universal rule, but it does **not** pretend that concrete bindings are already complete.

Every supported binding must subsequently define, in a versioned and auditable manner:

- anomaly classes;
- constructive localisability conditions;
- acquisition-fatal classes, if any;
- treatment of anomalies not covered by the explicit matrix;
- evidence needed to prove boundaries and membership remain unaffected.

If a future binding does not supply these conditions, the binding is **non-conforming / not eligible for qualification**. The universal policy itself does not degrade to an implementation heuristic.

This preserves the distinction between:

```text
POLICY CLOSED
≠
ALL CONCRETE FORMAT BINDINGS CLOSED
```

---

## 6. INVARIANTS PRESERVED

Q-RM-04 R2 does not alter:

- RB-A semantic logical record model;
- occurrence-based individuality;
- strict duplicate preservation;
- deterministic record boundaries;
- Q-RM-02 cardinality semantics;
- Q-RM-03 non-observation material classification;
- qualification-before-canonical-enumeration;
- temporal authority of `ordered_ticks`;
- acquisition-scoped identity;
- qualification freeze requirements.

No `CANONICAL_RECORD_POSITION` is introduced.

No temporal ordering rule is introduced.

No physical identity primitive is selected.

---

## 7. VERDICT

```text
Q-RM-04 SEMANTIC SAFETY RULE = PASS
Q-RM-04 FAILURE-SCOPE POLICY = PASS
```

**Q-RM-04 is closed at the universal policy level.**

Concrete format-specific anomaly matrices remain a downstream binding obligation and must be audited later under Q-RM-06. They are not silently treated as already complete.

---

## 8. NEXT LOGICAL BLOCK

Proceed to **Q-RM-05 — Acquisition Domain**.

Question to resolve:

> Under RB-A and the now-closed Q-RM-04 policy, what exactly constitutes one logical acquisition domain when the physical input is split across multiple files, partitions, chunks, streams, or independently delivered units, and what identity/failure scope follows from that domain boundary?

Q-RM-05 must not redefine Q-RM-04. It may expose domain-boundary cases that require explicit binding treatment, but the failure-scope policy itself is now normative and closed.

## FIN
