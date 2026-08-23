# AUDIT PACKAGE — 08 → 13

**Version:** 0.1 — AUDIT WORKING PAPER / NON-NORMATIVE  
**Date:** 23 août 2026  
**Status:** DRAFT — ready for adversarial review; not a system contract.  

---

## 0. Purpose

This document is an audit package for the interfaces between:

```text
08 SYSTEM REGISTRY
09 DATASET / PROVENANCE REGISTRY
10 TEMPORAL / POINT-IN-TIME CONTRACT
11 CONTRADICTION & ARBITRATION REGISTRY
12 UPWARD CHALLENGE PROTOCOL
13 CRITICALITY & AUDIT PROTOCOL
```

It does **not** redesign these documents. Its purpose is to test whether the six components actually compose into one coherent governance system before any later normative integration.

No conclusion in this document changes `04` or `05`.

---

# 1. Current architectural chain

```text
08
SYSTEM REGISTRY
   │
   ├── ownership
   ├── interfaces
   └── dependencies
        ↓
09
DATASET / PROVENANCE
   │
   └── evidence + lineage
        ↓
10
TEMPORAL / POINT-IN-TIME
   │
   └── temporal admissibility
        ↓
11
CONTRADICTION / ARBITRATION
   │
   └── conflict history + decision
        ↓
12
UPWARD CHALLENGE
   │
   └── downstream contestation
        ↓
13
CRITICALITY / AUDIT
   │
   └── proportional governance depth
        ↓
AUDIT / DECISION / VERSION / INTEGRATION
```

**Important:** `13` is not merely a sequential dependency after `12`. It is a transverse governance control that should classify and govern material changes/challenges throughout the chain.

---

# 2. Ownership / authority map

| Concept / function | Semantic owner | Producer | Depositor / record | Main consumers | Current status |
|---|---|---|---|---|---|
| Validation criteria / proof semantics | `04` | Validation process | `04` / research records | Research / promotion | Existing authority |
| Dataset identity | `09` registry | Acquisition / registration process | `09` | Research / validation | Proposed |
| Dataset lineage | `09` registry | Transformation pipeline | `09` | Audit / reproduction | Proposed |
| Temporal semantics | `10` | Temporal control / admissibility process | `09` temporal fields + run records | Research / validation | Proposed |
| Contradiction record | `11` | Detector / governance process | `11` | Audit / arbitration | Proposed |
| Arbitration decision | Governance authority defined by process | Arbitrator | `11` | All impacted components | Proposed |
| Upward challenge | `12` protocol | Downstream challenger | `12` + `11` when conflict | Governance | Proposed |
| Criticality classification | `13` | Audit/governance process | Audit record | All governed changes | Proposed |
| Audit evidence | Audit process | Human/system/AI sources | Audit record | Arbitration / integration | Proposed |

**Test:** no producer is allowed to redefine the semantics of a concept merely because it generates its value.

---

# 3. Interface map

## IF-08-09 — Registry → Dataset/Provenance

```text
SOURCE: 08 System Registry
OBJECT: dataset/provenance ownership + interface registration
CONTRACT: 09 proposal
VERSION: 08 v0.1 / 09 v0.1
DESTINATION: dataset registry / research consumers
POINT-IN-TIME: delegated to 10
PROVENANCE: 09
IMPACT 04: evidence availability / validation conditions
FAILURE MODE: dataset interface exists in map but exact admissibility evidence is absent
CRITICALITY: C2 minimum; C3 if it changes validation authority
```

**Question:** Can `08` register an interface without accidentally becoming the owner of dataset semantics?

---

## IF-09-10 — Dataset Provenance → Temporal Semantics

```text
SOURCE: 09 Dataset / Provenance Registry
OBJECT: temporal metadata and provenance
CONTRACT: 10 Temporal / Point-in-Time Contract
VERSION: 09 v0.1 / 10 v0.1
DESTINATION: research / validation consumers
POINT-IN-TIME: defined semantically by 10
PROVENANCE: stored by 09
IMPACT 04: temporal evidence / admissibility
FAILURE MODE: 09 invents temporal meaning independently from 10
CRITICALITY: C3 when semantics are modified
```

**Invariant to test:** `10` owns temporal semantics; `09` owns the provenance record. Neither may silently absorb the other's authority.

---

## IF-10-04 — Temporal Admissibility → Validation

```text
SOURCE: 10 temporal contract
OBJECT: temporal admissibility evidence/status
CONTRACT: 04 validation criteria
VERSION: 10 v0.1 / 04 v0.6.1
DESTINATION: validation / promotion process
POINT-IN-TIME: decision_at(T)
PROVENANCE: 09 + temporal evidence
IMPACT 04: potentially decision-critical
FAILURE MODE: temporal admissibility silently becomes a new validation criterion
CRITICALITY: C3
```

**Critical ownership test:** `10` may provide temporal evidence/admissibility; it must not redefine proof levels or validation semantics owned by `04`.

---

## IF-09-05 — Provenance → Data Contract

```text
SOURCE: 09 dataset/provenance registry
OBJECT: identity, lineage, coverage, transformations, usage limits
CONTRACT: 05 proposal
VERSION: 09 v0.1 / 05 v0.1
DESTINATION: data-contract consumers
POINT-IN-TIME: 10
PROVENANCE: 09
IMPACT 04: indirect until 05 is normative
FAILURE MODE: proposal fields become de facto mandatory rules without arbitration
CRITICALITY: C2 now; C3 if frozen into 05
```

---

## IF-11-12 — Contradiction ↔ Upward Challenge

```text
SOURCE: 12 upward challenge
OBJECT: formal contestation of upstream rule/contract
CONTRACT: 12 + 11
VERSION: v0.1 / v0.1
DESTINATION: 11 contradiction/arbitration process
POINT-IN-TIME: 10 where historical claims are involved
PROVENANCE: challenge evidence + contradiction record
IMPACT: depends on target
FAILURE MODE: every challenge is incorrectly treated as a contradiction, or a contradiction bypasses 11
CRITICALITY: C2 normally; C3 when normative authority is challenged
```

**Invariant:** `challenge ≠ contradiction` in every case; when a challenge establishes incompatible claims/contracts, it must link to `11`.

---

## IF-12-13 — Challenge → Criticality/Audit

```text
SOURCE: 12 upward challenge
OBJECT: challenge severity / potential impact
CONTRACT: 13 criticality protocol
VERSION: v0.1 / proposed
DESTINATION: audit process
POINT-IN-TIME: inherited from target and 10 where applicable
PROVENANCE: challenge record
IMPACT: determines audit depth
FAILURE MODE: challenge is downgraded because the target is frozen or because the local implementation impact appears small
CRITICALITY: C2/C3 depending on target
```

**Invariant:** a challenge to a frozen normative component inherits the potential impact until assessed; `FROZEN` never implies `UNCONTESTABLE`.

---

## IF-11-13 — Contradiction → Criticality/Audit

```text
SOURCE: 11 contradiction registry
OBJECT: contradiction severity / governance impact
CONTRACT: 13
VERSION: v0.1 / proposed
DESTINATION: audit process
POINT-IN-TIME: contradiction decision timestamps governed by 10
PROVENANCE: 11 evidence
IMPACT: determines audit depth
FAILURE MODE: K3 contradiction handled as local documentation change
CRITICALITY: C3 for normative/architectural conflicts
```

**Key distinction:** `K1/K2/K3` describes contradiction impact; `C0/C1/C2/C3` describes required audit depth. They must not be treated as the same scale.

---

## IF-13-11 — Audit → Arbitration

```text
SOURCE: 13 audit protocol
OBJECT: audit findings / decision recommendation
CONTRACT: 11 arbitration registry
VERSION: v0.1 / v0.1
DESTINATION: governance arbitration
POINT-IN-TIME: audit decision timestamp + applicable historical scope
PROVENANCE: audit record
IMPACT: decision-critical
FAILURE MODE: audit recommendation is mistaken for arbitration authority
CRITICALITY: C3 when 04/05/core architecture is affected
```

**Invariant:** `13` determines audit depth and records findings; `11` records the contradiction/arbitration history. Neither should silently acquire the other's authority.

---

# 4. Cross-system invariants to test

## INV-01 — Ownership conservation

No downstream component may redefine a concept it merely consumes.

## INV-02 — Frozen ≠ immutable

A frozen contract may be challenged through `12`, but cannot be modified outside governed arbitration/versioning.

## INV-03 — Challenge ≠ arbitration

`12` creates a governed contestation. `11` records/arbitrates conflicts. `13` controls audit depth.

## INV-04 — Temporal semantics have one owner

`10` defines temporal semantics. `09` records provenance. `04` retains validation authority.

## INV-05 — Evidence ≠ decision

Dataset evidence, temporal evidence and audit findings cannot automatically become normative decisions.

## INV-06 — AI ≠ authority

AI may detect, challenge, analyse and counter-expertise. AI output cannot silently become an arbitration decision.

## INV-07 — Unknown ≠ safe

An unresolved temporal, provenance, ownership, impact or downstream condition cannot be silently treated as valid/zero/no-impact.

## INV-08 — History is append-preserving

Contradictions, challenges, audits and decisions remain traceable after resolution/versioning.

## INV-09 — Criticality follows impact

Document size, number of changed lines or implementation effort cannot be used to reduce audit class.

## INV-10 — Historical knowledge is not reconstructed retrospectively

A later discovery cannot be represented as historically known without evidence supporting that knowledge state.

---

# 5. Potential tension points discovered before external audit

These are **audit hypotheses**, not confirmed defects.

### H-01 — `10` introduces `usable_from / usable_to`

Need to verify whether this is a genuinely distinct temporal dimension or whether it duplicates a governance/usage constraint that belongs elsewhere. If retained, ownership and interaction with `09` must be explicit.

### H-02 — `13` says C3 requires independent counter-expertise “where appropriate”

For the current project, any audit touching `04`, temporal semantics, ownership, contradiction arbitration or the core architecture should probably be treated as requiring both adversarial review and independent counter-expertise. This must be tested, not assumed.

### H-03 — `11 K1/K2/K3` versus `13 C0/C1/C2/C3`

The separation is conceptually correct, but the mapping between contradiction severity and audit criticality needs an explicit decision rule. A K3 contradiction should normally force C3, but the reverse is not necessarily true.

### H-04 — `12` SAFE HOLD

Need to test who is authorized to trigger, review and release a SAFE HOLD, and whether the protocol can accidentally become an operational override mechanism.

### H-05 — `13` as transverse governance

The sequential documentation order `08→09→10→11→12→13` is a construction order, not necessarily a runtime dependency chain. This distinction should be made explicit before implementation.

### H-06 — Migration of C-01…C-06

`08` records the original discovery. `11` proposes migrating those contradictions. Need to verify that migration preserves identity, evidence, date, scope and historical meaning rather than silently recreating them as new contradictions.

### H-07 — `04` dependency on proposed `05`

The system must prevent the mere existence of `09/10` from making `05` effectively normative by accretion.

### H-08 — Post-integration verification

`13` requires post-integration verification, but the exact evidence proving that the integrated component still conforms to the audited contract is not yet specified.

---

# 6. Adversarial test matrix

| Test ID | Attack | Expected protection | Primary components |
|---|---|---|---|
| ADV-01 | Downstream component silently redefines an upstream concept | Ownership violation detected and blocked | 08/11/12 |
| ADV-02 | Frozen `04` is modified directly | Modification rejected; challenge path required | 04/12/13 |
| ADV-03 | AI consensus used as arbitration | AI output retained as evidence, not authority | 11/13 |
| ADV-04 | Later dataset vintage presented as historically known | Point-in-time failure | 09/10 |
| ADV-05 | Unknown provenance treated as PASS | Consumer gate blocks or marks restricted | 09/10/04 |
| ADV-06 | Contradiction corrected without ledger entry | Silent-fix detection | 11 |
| ADV-07 | Challenge is used to bypass contract | No-contournement rule | 12 |
| ADV-08 | K3 contradiction processed as C1 | Criticality escalation | 11/13 |
| ADV-09 | Large cosmetic change forces unnecessary C3 | Impact-based classification | 13 |
| ADV-10 | One material change split into cosmetic commits | Anti-splitting control | 13 |
| ADV-11 | `09` invents temporal semantics | Ownership violation | 09/10 |
| ADV-12 | `10` redefines validation criteria | Ownership violation | 10/04 |
| ADV-13 | `13` becomes arbitration authority | Governance boundary failure | 11/13 |
| ADV-14 | SAFE HOLD becomes permanent bypass | Explicit release/decision requirement | 12/11/13 |
| ADV-15 | C-01…C-06 migrated and historical context lost | Migration traceability failure | 08/11 |
| ADV-16 | Post-integration implementation drifts from audited contract | Post-integration verification catches drift | 13 + all |

---

# 7. Current preliminary assessment

### What appears coherent

- Ownership is explicitly separated in `08`.
- `09` treats provenance as evidence rather than semantic authority.
- `10` gives temporal semantics a dedicated owner.
- `11` preserves contradiction history and separates it from modification.
- `12` separates contestation from modification and arbitration.
- `13` makes audit depth impact-based and explicitly rejects AI as normative authority.

### What is NOT yet proven

- The six components have not yet passed adversarial external review.
- The exact mapping `K → C` is not frozen.
- SAFE HOLD governance is not yet fully tested.
- Migration from `08 C-01…C-06` into `11` is not yet performed.
- Post-integration verification evidence is not yet specified.
- The boundary between construction order and runtime dependency has not yet been formally recorded.
- `05` remains non-normative and must remain so until separately approved.

Therefore:

> **08→13 is structurally promising but NOT YET VALIDATED.**

---

# 8. External adversarial review brief

The external reviewers must NOT be asked to redesign the architecture initially.

They must answer only:

1. What is logically inconsistent?
2. What ownership boundary is ambiguous?
3. What interface is underspecified?
4. What contradiction can escape `11`?
5. What challenge can bypass `12`?
6. What audit can be incorrectly downgraded under `13`?
7. What temporal/look-ahead failure can still pass?
8. What historical evidence can be silently overwritten?
9. What AI-governance failure remains possible?
10. What failure would allow the exact class of mistake that motivated this architecture to recur?

Each finding must include:

```text
FINDING_ID
COMPONENT(S)
CLAIM
EVIDENCE
FAILURE_SCENARIO
SEVERITY
PROPOSED_TEST
```

**Reviewers may propose fixes, but fixes are non-authoritative until arbitrated.**

---

# 9. Gate after external review

```text
AUDIT PACKAGE 0.1
      ↓
CLAUDE — ADVERSARIAL AUDIT
      ↓
PERPLEXITY — INDEPENDENT COUNTER-EXPERTISE
      ↓
COMPARE FINDINGS
      ↓
REGISTER MATERIAL DISAGREEMENTS IN 11
      ↓
CLASSIFY WITH 13
      ↓
ARBITRATE
      ↓
CORRECT / VERSION
      ↓
RETEST ADV-01…ADV-16
      ↓
ONLY THEN
      ↓
INTEGRATE 08→13
```

No external reviewer is an authority over `04`, `05`, or the architecture merely by producing a recommendation.

---

# 10. Decision status

**NOT VALIDATED**  
**NOT NORMATIVE**  
**READY FOR ADVERSARIAL REVIEW**
