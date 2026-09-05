# ADJUDICATION — Q-RM-08 ACQUISITION-DOMAIN CONTRACT

**Date:** 5 septembre 2026  
**Status:** **CONTRACT SCHEMA = PASS; PROJECT-SPECIFIC ACQUISITION DECLARATIONS = BLOCKED**  
**Depends on:** RB-A, Q-RM-01..07  
**Purpose:** turn the universal Q-RM-05 domain rule into an executable, falsifiable contract without inventing unsupported acquisition facts.

---

## 1. QUESTION

What exact artifact must exist before an acquisition can enter normative qualification?

Q-RM-05 already establishes that the acquisition boundary is semantic and declaration-owned, not inferred from files, partitions, timestamps, provider, traversal, or workers.

The concrete contract must therefore define the declaration itself.

---

## 2. NECESSARY CONSEQUENCES

The following are forced by the validated architecture:

- an acquisition domain must be uniquely identifiable;
- its physical component membership must be explicit;
- completeness must be testable;
- the declaration must bind the applicable record-model / qualification semantics;
- missing, extra, duplicate, or ambiguous components cannot be silently ignored;
- worker/chunk/file boundaries cannot redefine the domain;
- the declaration must be immutable for the qualification run;
- the declaration must be reconstructible after restart.

These are **[CONSÉQUENCE NÉCESSAIRE]**, not implementation preferences.

---

## 3. CONCRETE CONTRACT SCHEMA

An acquisition declaration shall contain, at minimum:

```text
acquisition_declaration_version
acquisition_domain_id
representation_id
representation_version
record_model_version
format_binding_id
format_binding_version
qualification_contract_id
qualification_contract_version
component_manifest
component_membership_policy
completeness_evidence
acquisition_state
```

Each field must have a single normative meaning. No field may be populated by an implicit runtime convention.

### Component manifest

The manifest must enumerate the physical components belonging to the declared acquisition, using a representation-level locator/provenance mechanism that is later defined by the concrete binding.

The contract does **not** yet select path, URI, byte offset, provider ID, hash, or other physical identity primitive.

### Membership policy

The declaration must state whether the listed component set is:

```text
COMPLETE
or
INCOMPLETE / NOT YET QUALIFIABLE
```

Optionality cannot be inferred from absence.

### Completeness evidence

The declaration must identify the evidence by which the system can falsify a missing or extra component claim. A filename list alone is insufficient, consistently with the existing data-contract warning that coverage must be established from content rather than names. fileciteturn21file0L2-L2

---

## 4. NORMATIVE STATES

```text
DECLARED
  ↓
MATERIALISED
  ↓
COMPLETE
  ↓
ELIGIBLE_FOR_QUALIFICATION
```

Any unresolved ambiguity in membership or completeness prevents the `ELIGIBLE_FOR_QUALIFICATION` state.

A physical artifact that exists but is not declared is not thereby part of the acquisition.

A declared artifact that is absent is not thereby removed from the acquisition.

---

## 5. ADVERSARIAL TEST MATRIX

| Case | Required result |
|---|---|
| One declaration, ten files | One acquisition domain |
| Ten files, no declaration joining them | No implicit fusion; blocked if qualification requires a domain |
| One domain, four worker partitions | One acquisition domain |
| Missing declared component | No silent shrink; classify and block where determinability is affected |
| Extra undeclared component | Not silently admitted |
| Same component delivered twice | Must be classified; no automatic deduplication or occurrence creation |
| Same observations reacquired | Distinct acquisition domains |
| Different traversal orders | Same domain membership |
| Ambiguous declaration | Qualification blocked |
| Filename continuity only | Insufficient evidence |
| Provider continuity only | Insufficient evidence |
| Timestamp continuity only | Insufficient evidence |

---

## 6. [CONTRACTUEL]

The project must choose and freeze the concrete representation of:

1. `acquisition_domain_id`;
2. component locator/provenance;
3. completeness evidence;
4. component inclusion/exclusion rules;
5. treatment of repeated delivery;
6. treatment of missing/extra components.

These choices are not derivable from RB-A/Q-RM-05 alone.

---

## 7. [ABSENCE DE PREUVE]

The current repository contains the universal acquisition-domain decision, but no validated project-specific acquisition declaration inventory that closes the concrete values above.

The existing `05-DATA-CONTRACT.md` is explicitly marked as a proposal and non-validé; it therefore cannot silently supply those missing semantics. fileciteturn21file0L2-L2

This is a genuine specification gap, not a reason to invent a default.

---

## 8. VERDICT

```text
Q-RM-08 CONTRACT SCHEMA / EXECUTABLE REQUIREMENTS = PASS
Q-RM-08 PROJECT-SPECIFIC ACQUISITION DECLARATIONS = BLOCKED
```

The contract itself can be fixed without choosing an identity primitive. The project cannot truthfully claim a concrete acquisition is qualification-ready until its declaration and completeness evidence exist.

**No Grok escalation is required for the universal rule; the blocker is missing project-specific normative input.**

## FIN
