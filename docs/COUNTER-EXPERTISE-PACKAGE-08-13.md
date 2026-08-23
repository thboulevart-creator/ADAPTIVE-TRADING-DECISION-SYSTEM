# COUNTER-EXPERTISE PACKAGE — 08 → 13

**Version:** 0.1 — REVIEW TRANSPORT PACKAGE
**Date:** 23 août 2026
**Status:** NON-NORMATIVE / REVIEW MATERIAL ONLY
**Purpose:** provide a transportable, source-anchored package for independent adversarial review by external AI reviewers when direct repository access is unavailable.

---

## 0. IMPORTANT GOVERNANCE RULE

This package is **not a replacement for the source documents**.

The authoritative working source remains the repository and the exact versions of:

- `08-SYSTEM-REGISTRY.md`
- `09-DATASET-PROVENANCE-REGISTRY.md`
- `10-TEMPORAL-POINT-IN-TIME-CONTRACT.md`
- `11-CONTRADICTION-ARBITRATION-REGISTRY.md`
- `12-UPWARD-CHALLENGE-PROTOCOL.md`
- `13-CRITICALITY-AUDIT-PROTOCOL.md`
- `AUDIT-08-13-INTERFACE-MAP.md`

This package exists only to transport the architecture and the adversarial test plan to a reviewer that cannot access the repository directly.

**No reviewer conclusion is normative. No reviewer may silently redefine `04`, `05`, ownership, or any frozen contract.**

---

# 1. SOURCE DOCUMENTS

Repository:

`https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Source files:

- `docs/08-SYSTEM-REGISTRY.md`
- `docs/09-DATASET-PROVENANCE-REGISTRY.md`
- `docs/10-TEMPORAL-POINT-IN-TIME-CONTRACT.md`
- `docs/11-CONTRADICTION-ARBITRATION-REGISTRY.md`
- `docs/12-UPWARD-CHALLENGE-PROTOCOL.md`
- `docs/13-CRITICALITY-AUDIT-PROTOCOL.md`
- `docs/AUDIT-08-13-INTERFACE-MAP.md`

The source documents explicitly remain proposals/non-normative until audit and arbitration. The audit map states that `08→13` is structurally promising but **NOT YET VALIDATED**.

---

# 2. ARCHITECTURAL CHAIN

```text
08 SYSTEM REGISTRY
    ownership / interfaces / dependencies
            ↓
09 DATASET / PROVENANCE REGISTRY
    evidence / identity / lineage / usage limits
            ↓
10 TEMPORAL / POINT-IN-TIME CONTRACT
    temporal semantics / admissibility / look-ahead control
            ↓
11 CONTRADICTION & ARBITRATION REGISTRY
    contradiction history / arbitration / version traceability
            ↓
12 UPWARD CHALLENGE PROTOCOL
    downstream contestation without authority inversion
            ↓
13 CRITICALITY & AUDIT PROTOCOL
    impact-based governance depth
            ↓
AUDIT → DECISION → VERSION → INTEGRATION → POST-INTEGRATION CHECK
```

**Critical interpretation:** `08→09→10→11→12→13` is primarily the current construction order. `13` is a transverse governance control and must not accidentally be treated as merely a runtime successor of `12`.

---

# 3. OWNERSHIP MAP

| Concept / function | Owner | Producer | Depositary / record | Consumers |
|---|---|---|---|---|
| Validation criteria / proof semantics | `04` | Validation process | `04` / research records | Research / promotion |
| Dataset identity | `09` | Acquisition / registration | `09` | Research / validation |
| Dataset lineage | `09` | Transformation pipeline | `09` | Audit / reproduction |
| Temporal semantics | `10` | Temporal control | `09` temporal fields + run records | Research / validation |
| Contradiction record | `11` | Detector / governance process | `11` | Audit / arbitration |
| Arbitration decision | Governance process / defined authority | Arbitrator | `11` | Impacted components |
| Upward challenge | `12` | Downstream challenger | `12`, plus `11` if contradiction | Governance |
| Criticality classification | `13` | Audit/governance process | Audit record | Governed changes |
| Audit evidence | Audit process | Human / system / AI | Audit record | Arbitration / integration |

**Invariant:** producing a value does not grant semantic ownership of the concept represented by that value.

---

# 4. WHAT EACH COMPONENT IS RESPONSIBLE FOR

## 08 — SYSTEM REGISTRY

Purpose: factual system map. It distinguishes **definer / producer / depositor / consumer**, records interfaces and dependencies, and explicitly avoids redefining `04` or `05`.

Important current facts:

- `04` remains the observed methodological reference.
- `05` remains a proposal and is not normative.
- The registry identifies current gaps such as missing canonical dataset registry, contradiction ledger and upward challenge protocol.
- `08` explicitly states that the bitemporal model is an architectural need, not yet a frozen rule.

## 09 — DATASET / PROVENANCE REGISTRY

Purpose: identify datasets independently from filenames and preserve content identity, provenance, lineage, transformation history, usage limits and reproducibility anchors.

Core controls:

- immutable dataset identity/content hash;
- explicit source record;
- parent/child lineage;
- new identity for transformed datasets;
- coverage/integrity evidence;
- explicit authorized/prohibited uses;
- distinction between market timestamp and acquisition/validation/use timestamps;
- result → run → code/config → dataset/version/hash linkage;
- substitution events;
- explicit `UNKNOWN` rather than silently assuming PASS;
- consumer gate;
- separate data, documentation and pipeline look-ahead failure classes.

`09` must not invent temporal semantics; it reserves the interface to `10`.

## 10 — TEMPORAL / POINT-IN-TIME CONTRACT

Purpose: prevent historical, documentary and pipeline look-ahead.

It distinguishes:

```text
WORLD VALIDITY       valid_from / valid_to
KNOWLEDGE            known_from / known_to
PERMITTED USE        usable_from / usable_to
EXECUTION            acquired_at / registered_at / validated_at / used_at / executed_at
```

It introduces an explicit `decision_at` and conceptual admissibility:

```text
ADMISSIBLE(T)
 = VALID(T)
 ∧ KNOWN(T)
 ∧ USABLE(T)
 ∧ PIPELINE_SAFE(T)
```

Central invariant:

> Historical truth does not imply historical knowledge.

The contract also distinguishes historical mode from reconstruction mode and requires explicit handling of vintage/revision, publication/availability time, transformations, manual annotations, parameter/model selection and dependency closure.

`10` owns temporal semantics. It must not redefine `04` validation semantics.

## 11 — CONTRADICTION & ARBITRATION REGISTRY

Purpose: prevent silent correction/deletion of contradictions.

Required history:

```text
CONTRADICTION
→ DETECTION
→ QUALIFICATION
→ ANALYSIS
→ ARBITRATION
→ DECISION
→ REASON
→ VERSION / EFFECTIVITY
```

Contradictions have stable IDs and explicit types, versions, evidence, owner, impact and decision history.

A contradiction must be recorded before a material correction.

A resolved contradiction is never deleted.

The registry separates contradiction severity `K1/K2/K3` from audit criticality `C0/C1/C2/C3`.

## 12 — UPWARD CHALLENGE PROTOCOL

Purpose: permit a downstream consumer to formally challenge an upstream rule without automatically acquiring the right to modify it.

Core separation:

```text
CONTESTER ≠ MODIFIER ≠ ARBITRATOR
```

Challenges require a target/version, observed failure, evidence, scope, impact and appropriate temporal information.

A challenge can be rejected for insufficient evidence, but the rejection and evidence remain recorded.

`SAFE HOLD` exists for critical cases: it can suspend use without modifying the upstream contract and must trigger a challenge/audit/arbitration path.

`FROZEN` means controlled modification, **not immunity from challenge**.

## 13 — CRITICALITY & AUDIT PROTOCOL

Purpose: scale governance to impact rather than document size or number of changed lines.

Classes:

| Class | Meaning | Minimum |
|---|---|---|
| C0 | no substantive system effect | self-check |
| C1 | non-semantic documentation extension | lightweight review |
| C2 | material interface/contract consumer change | structured audit |
| C3 | normative/core architecture/ownership/temporal/decision-critical change | full adversarial audit + integration review |

If uncertain, choose the higher class until evidence supports de-escalation.

C3 requires, among other controls, adversarial review, independent counter-expertise where appropriate, failure-mode analysis, integration testing, decision record and post-integration verification.

AI is explicitly analysis/evidence, not normative authority.

---

# 5. INTERFACE MAP

## IF-08-09

`08` registers dataset/provenance ownership and interfaces; `09` provides dataset/provenance records. `08` must not become the semantic owner of dataset concepts merely by registering them.

## IF-09-10

`09` stores temporal metadata; `10` defines its semantics. `09` must not invent temporal meaning independently.

## IF-10-04

`10` supplies temporal admissibility evidence/status to `04`; `10` must not redefine proof levels or validation criteria.

## IF-09-05

`09` operationalizes dataset/provenance information that may feed proposed `05`; the existence of these fields must not make `05` de facto normative.

## IF-11-12

`12` records contestation; `11` records/arbitrates actual conflicts. A challenge is not automatically a contradiction, but an actual incompatible claim/contract must link to `11`.

## IF-12-13

`12` provides challenge impact; `13` determines audit depth. A challenge against a frozen normative component cannot be downgraded simply because the target is frozen.

## IF-11-13

`11` preserves contradiction/arbitration history; `13` determines audit depth. `13` findings are not automatically arbitration decisions.

## IF-13-11

Audit results/recommendations flow into governed arbitration; audit authority and arbitration authority remain separate.

---

# 6. CROSS-SYSTEM INVARIANTS

1. **Ownership conservation** — consumers cannot silently redefine consumed concepts.
2. **Frozen ≠ immutable** — frozen contracts can be challenged, not bypassed.
3. **Challenge ≠ arbitration** — contestation, contradiction and audit remain distinct functions.
4. **One owner for temporal semantics** — `10` defines them; `09` records provenance.
5. **Evidence ≠ decision** — evidence never silently becomes a rule.
6. **AI ≠ authority** — AI analysis cannot silently become arbitration.
7. **Unknown ≠ safe** — unresolved conditions cannot be treated as PASS/zero/no-impact.
8. **History is append-preserving** — contradictions/challenges/audits/decisions survive resolution.
9. **Criticality follows impact** — text size/implementation effort cannot lower governance class.
10. **Historical knowledge is not retrospective** — later discovery cannot be represented as earlier knowledge without evidence.

---

# 7. HYPOTHESES TO ATTACK — H-01 → H-08

These are **not confirmed defects**. They are deliberately exposed hypotheses for adversarial testing.

### H-01 — `usable_from / usable_to`

Test whether this is genuinely distinct from ordinary usage constraints or whether it duplicates another ownership domain. If retained, ownership and interface must be explicit.

### H-02 — C3 counter-expertise wording

Test whether `04`, temporal semantics, ownership, contradiction arbitration and core architecture should automatically require independent counter-expertise rather than the current “where appropriate” wording.

### H-03 — K vs C mapping

Test whether the mapping from contradiction severity `K1/K2/K3` to audit class `C0/C1/C2/C3` is sufficiently explicit. Expected concern: K3 should normally force C3, but C3 does not necessarily imply K3.

### H-04 — SAFE HOLD governance

Test who may trigger, review and release a SAFE HOLD and whether it can become an operational bypass or indefinite suspension.

### H-05 — Construction order vs runtime dependency

Test whether the repository's sequential numbering can be misread as runtime dependency. `13` is intended as transverse governance, not simply a successor of `12`.

### H-06 — Migration C-01…C-06

Test whether migrating contradictions identified in `08` into `11` preserves original identity, evidence, date, scope and historical meaning.

### H-07 — `05` de facto normativity

Test whether downstream proposals (`09/10`) could cumulatively make `05` mandatory without a formal arbitration/version event.

### H-08 — Post-integration verification

Test whether `13` defines enough evidence to prove that an implementation still conforms to the audited contract after integration.

---

# 8. ADVERSARIAL TEST MATRIX — ADV-01 → ADV-16

| ID | Attack | Expected protection | Components |
|---|---|---|---|
| ADV-01 | downstream silently redefines upstream concept | ownership violation detected/blocked | 08/11/12 |
| ADV-02 | frozen `04` modified directly | governed challenge path required | 04/12/13 |
| ADV-03 | AI consensus used as arbitration | AI output remains evidence, not authority | 11/13 |
| ADV-04 | later dataset vintage presented as historically known | point-in-time failure | 09/10 |
| ADV-05 | unknown provenance treated as PASS | consumer gate blocks/restricts | 09/10/04 |
| ADV-06 | contradiction corrected without ledger entry | silent-fix detection | 11 |
| ADV-07 | challenge used to bypass contract | no-contournement control | 12 |
| ADV-08 | K3 contradiction processed as C1 | criticality escalation | 11/13 |
| ADV-09 | cosmetic change forces unnecessary C3 | impact-based classification | 13 |
| ADV-10 | material change split into cosmetic commits | anti-splitting control | 13 |
| ADV-11 | `09` invents temporal semantics | ownership violation | 09/10 |
| ADV-12 | `10` redefines validation criteria | ownership violation | 10/04 |
| ADV-13 | `13` becomes arbitration authority | governance boundary failure | 11/13 |
| ADV-14 | SAFE HOLD becomes permanent bypass | release/decision requirement | 12/11/13 |
| ADV-15 | C-01…C-06 migration loses historical context | migration traceability failure | 08/11 |
| ADV-16 | post-integration implementation drifts from audited contract | post-integration verification catches drift | 13 + all |

---

# 9. REQUIRED REVIEW METHOD

The reviewer must **not redesign the architecture first**.

The first pass must answer only:

1. What is logically inconsistent?
2. What ownership boundary is ambiguous?
3. What interface is underspecified?
4. What contradiction can escape `11`?
5. What challenge can bypass `12`?
6. What audit can be incorrectly downgraded under `13`?
7. What temporal/look-ahead failure can still pass?
8. What historical evidence can be silently overwritten?
9. What AI-governance failure remains possible?
10. What failure would allow the original class of error to recur?

For every finding, return:

```text
FINDING_ID
COMPONENT(S)
CLAIM
EVIDENCE
FAILURE_SCENARIO
SEVERITY
PROPOSED_TEST
```

**Do not treat the proposed fixes as authoritative.**

---

# 10. SPECIAL INSTRUCTION FOR INDEPENDENT COUNTER-EXPERTISE

If this package is supplied after another AI has already audited the architecture, the second reviewer must:

- independently inspect the source claims;
- explicitly identify where it agrees/disagrees with the first reviewer;
- not assume the first reviewer's conclusions are correct;
- preserve disagreements rather than averaging them;
- distinguish factual/documentary findings from proposed redesign;
- identify any finding that cannot be verified from the source material.

A reviewer must never claim to have verified source text that it did not actually receive or access.

---

# 11. GOVERNANCE GATE AFTER REVIEW

```text
SOURCE DOCUMENTS
      ↓
08→13 AUDIT PACKAGE
      ↓
CLAUDE — ADVERSARIAL AUDIT
      ↓
PERPLEXITY — INDEPENDENT COUNTER-EXPERTISE
      ↓
COMPARE FINDINGS
      ↓
MATERIAL DISAGREEMENTS → 11
      ↓
CRITICALITY → 13
      ↓
ARBITRATION
      ↓
CORRECT / VERSION
      ↓
RETEST ADV-01…ADV-16
      ↓
POST-INTEGRATION VERIFICATION
      ↓
ONLY THEN
      ↓
NORMATIVE INTEGRATION
```

No AI reviewer becomes the architecture's authority by producing an audit.

---

# 12. CURRENT DECISION STATUS

**08→13: NOT VALIDATED**

**08→13: NOT NORMATIVE**

**08→13: READY FOR ADVERSARIAL REVIEW**

This package is a transport mechanism for that review. It must not itself be treated as a new contract.
