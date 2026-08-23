# 13 — CRITICALITY & AUDIT PROTOCOL

**Status:** PROPOSED — governance control
**Purpose:** Determine the minimum audit depth required for a change, challenge, contradiction, interface modification, or new system component.

---

## 1. Purpose

This protocol prevents two opposite failures:

1. treating a material architectural or semantic change as a minor documentation edit;
2. applying an unnecessarily heavy governance process to a non-semantic editorial change.

Audit depth is determined by **impact**, not by the size of the document or the amount of text changed.

---

## 2. Core principle

> **The greater the potential effect on system meaning, decision validity, historical integrity, or downstream behavior, the greater the required audit depth.**

A small textual change can therefore be C3.
A large formatting change can remain C1.

---

## 3. Criticality classes

| Class | Definition | Typical examples | Minimum audit |
|---|---|---|---|
| **C0** | No substantive system effect | typo, formatting, broken link, wording with no semantic effect | self-check |
| **C1** | Documentation extension without semantic or contractual change | explanatory note, example, clarification that does not alter meaning | lightweight review |
| **C2** | Material change consuming or modifying existing contracts without redefining core system authority | new consumer, interface extension, new operational rule based on existing contracts | structured audit |
| **C3** | New normative concept, change to core architecture, ownership, temporal semantics, validation authority, or decision-critical contract | change to 04 semantics, ownership transfer, point-in-time rules, contradiction arbitration rules | full adversarial audit + integration review |

**C3 is the highest normal criticality.** If a change creates an unprecedented systemic risk, it must be escalated explicitly rather than silently assigned a higher number.

---

## 4. Classification test

Before implementation, classify the proposed change by asking:

- Does it change the meaning of an existing concept?
- Does it create a new normative concept?
- Does it alter who owns a concept?
- Does it alter a frozen contract?
- Does it alter point-in-time or provenance semantics?
- Does it change how contradictions are resolved?
- Does it create or modify an interface between authoritative components?
- Can it create look-ahead, leakage, survivorship, or historical contamination?
- Can it materially change downstream trading decisions or research conclusions?
- Can a downstream component become invalid if this change is wrong?

If any answer indicates architectural, semantic, temporal, or decision-critical impact, **C2 or C3 must be considered**. The lowest class must not be selected merely to reduce governance effort.

---

## 5. Escalation rule

When classification is uncertain:

> **Choose the higher criticality until evidence supports de-escalation.**

A classification may be downgraded only after the relevant impact has been demonstrated to be absent.

---

## 6. Audit depth

### C0 — Self-check

Required:

- verify no semantic change;
- verify links/references;
- verify formatting and naming consistency.

No architectural arbitration required.

### C1 — Lightweight review

Required:

- identify affected document/component;
- confirm ownership is unchanged;
- confirm contracts are unchanged;
- review by one independent pass;
- record the change if it affects a governed document.

### C2 — Structured audit

Required:

1. impact map;
2. ownership check;
3. interface/dependency check;
4. contract compatibility check;
5. point-in-time/provenance check where applicable;
6. contradiction check;
7. downstream consumer review;
8. explicit acceptance decision.

### C3 — Full adversarial audit

Required:

1. complete impact map;
2. ownership and authority verification;
3. interface and dependency analysis;
4. contradiction/arbitration review;
5. point-in-time and provenance audit;
6. adversarial challenge;
7. independent counter-expertise where appropriate;
8. failure-mode analysis;
9. downstream integration test;
10. explicit decision record;
11. version/revision traceability;
12. post-integration verification.

C3 changes must not be accepted solely because the author or a single AI system considers them correct.

---

## 7. AI governance

AI systems may assist with:

- classification;
- impact discovery;
- contradiction detection;
- adversarial challenge;
- test generation;
- documentation.

AI systems do **not** automatically possess normative authority.

An AI recommendation is evidence or analysis, not an arbitration decision.

For C3 changes, disagreement between AI analyses must be preserved and resolved through the governed arbitration process rather than averaged or silently discarded.

---

## 8. Interaction with the Upward Challenge Protocol

A challenge to a higher-level component inherits the criticality of the potential impact until assessed.

Example:

```text
Downstream discovery
      ↓
UPWARD CHALLENGE — 12
      ↓
Potential impact on 04 semantics
      ↓
C3 classification
      ↓
Full adversarial audit
      ↓
11 — Contradiction & Arbitration Registry
      ↓
Decision
      ↓
Versioned integration
```

A challenge must never be downgraded simply because the challenged document is frozen.

---

## 9. Interaction with frozen contracts

**Frozen** means that modification is controlled.
It does not mean that the contract is immune from challenge.

Any proposed modification to a frozen contract must record:

- current version;
- proposed version;
- reason for challenge;
- affected concepts;
- affected consumers;
- temporal/provenance implications;
- contradiction status;
- criticality;
- audit result;
- final decision.

---

## 10. No silent downgrade

The following are prohibited:

- classifying a semantic change as C0/C1 to bypass review;
- splitting one material change into several cosmetic commits to avoid C2/C3 treatment;
- modifying a downstream interpretation instead of challenging the upstream contract;
- deleting contradictory evidence without recording the arbitration;
- treating successful implementation as proof of semantic correctness.

---

## 11. Audit record

Every C2/C3 audit must produce a minimal durable record:

```text
AUDIT_ID
CHANGE_ID
COMPONENT
CURRENT_VERSION
PROPOSED_VERSION
CRITICALITY
TRIGGER
AFFECTED_CONCEPTS
AFFECTED_INTERFACES
AFFECTED_CONSUMERS
POINT_IN_TIME_IMPACT
PROVENANCE_IMPACT
CONTRADICTIONS
ADVERSARIAL_FINDINGS
DECISION
DECISION_REASON
DECISION_AUTHORITY
INTEGRATION_STATUS
DATE
```

The audit record is part of the system's provenance and must remain traceable after implementation.

---

## 12. Stop conditions

Implementation must stop when any of the following occurs:

- ownership is unresolved;
- contract semantics are ambiguous;
- a critical contradiction is unresolved;
- point-in-time validity cannot be established where required;
- a C3 change has not completed its required audit;
- downstream impact is unknown for a decision-critical interface;
- evidence required to support the decision is missing.

A system component is not considered integrated merely because its code or documentation exists in the repository.

---

## 13. Minimum governance chain

```text
CHANGE / CHALLENGE
       ↓
CRITICALITY CLASSIFICATION
       ↓
IMPACT MAP
       ↓
AUDIT DEPTH
       ↓
CONTRADICTION / ARBITRATION
       ↓
ADVERSARIAL TESTING
       ↓
DECISION
       ↓
VERSIONING
       ↓
INTEGRATION
       ↓
POST-INTEGRATION CHECK
```

This protocol is designed to make the governance process **proportional without making it permissive**.
