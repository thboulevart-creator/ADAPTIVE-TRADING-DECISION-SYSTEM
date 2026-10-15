# 07 — SYSTEM ARCHITECTURE — OWNERSHIP & INTERFACE MAP

**Version:** 0.1 — FACTUAL CARTOGRAPHY / NO REDESIGN
**Date:** 23 août 2026
**Scope:** `04-VALIDATION-CRITERIA` + `05-DATA-CONTRACT`
**Purpose:** establish what already exists before creating any new system brick.

> **This document is a map, not an architecture proposal.** It records explicit ownership, interfaces,
dependencies and gaps visible in the current documents. Where ownership is not explicitly defined,
`NON DÉFINI` is retained rather than inferred.

---

## 0. Authority baseline

| Document | Version | Current status | Primary authority observed |
|---|---:|---|---|
| `04-VALIDATION-CRITERIA` | 0.6.1 | PROPOSITION, candidate for freeze | Validation / evidentiary governance |
| `05-DATA-CONTRACT` | 0.1 | PROPOSITION, not validated | Data integrity / data contract |

`04` explicitly states that it fixes, before confirmatory research, what constitutes sufficient proof to
retain, promote or abandon a hypothesis. `05` states that every datum entering a calculation must carry
a verifiable identity and that every engine traversing a series must prove it respects its assumptions.

**Important:** neither document is currently a universal owner of every downstream implementation detail.
`04` explicitly uses `[INTERFACE]` where the detail belongs elsewhere; `05` explicitly leaves several
parameters to the Asset Profile or a technical decision.

---

# 1. Ownership map — concepts already present

## 1.1 Core normative concepts

| Concept | Definiteur | Producteur | Dépositaire | Consommateurs | Status |
|---|---|---|---|---|---|
| Exploration vs confirmatory regime | `04` | Research process | Research charter / registry | All confirmatory research | Explicit |
| Research charter | `04` | Research operator/process | Charter + version history | Validation engine / auditor | Explicit |
| `N_budget` | `04` | Research process | Charter | Multiplicity/governance audit | Explicit |
| `N_famille` | `04` | Research process | Charter | Statistical correction / promotion | Explicit |
| Phase boundaries A/B/C/D | `04` | Research process | Charter | Validation process | Explicit |
| Configuration freeze | `04` | Technical process | Frozen artefact identifiers | Confirmatory engine | Explicit interface |
| Period state VIERGE/CONSULTÉE/CONSOMMÉE | `04` | Observation/research process | §4.6 registry | Evidence engine / promotion | Explicit |
| Consultation intensity I1/I2/I3 | `04` | Observation/research process | §4.6 registry | Probative-status calculation | Explicit |
| Probative status | `04` | Governance process | §4.6 registry | Promotion / evidence level | Explicit |
| Research family | `04` | Governance process | Charter / registry | Consumption and multiplicity rules | Explicit |
| Promotion conditions | `04` | Confirmatory evaluation | Research result / audit record | Promotion decision | Explicit |
| Invalidation / falsification / non-interpretable result | `04` | Confirmatory evaluation | Research result / audit record | Abandonment / replay decision | Explicit |
| Evidence level N0–N4 | `04` | Promotion evaluation | Research result | Capital-allocation policy | Explicit |
| Data continuity | `05` | Data QA process | Dataset QA report | Every engine using indexed series | Explicit |
| Data coverage | `05` | Data QA process | Coverage report | Every quantitative result | Explicit |
| Dataset transformation identity | `05` | Data transformation pipeline | Dataset metadata | Downstream data consumers | Explicit |
| Dataset lineage / parent reference | `05` | Transformation pipeline | Dataset metadata | Audit / reproducibility | Explicit |
| Temporal convention | Asset Profile, referenced by `05` | Asset Profile | Asset Profile | All engines | Explicit cross-document dependency |
| Canonical price format | `05` principle; value TBD | Technical owner NON DÉFINI | TBD | All data consumers | Incomplete interface |
| Cost model | Asset Profile, enforced by `05` and consumed by `04` | Asset Profile / execution model | Asset Profile | Research + validation + execution | Explicit dependency |
| Anti-look-ahead control | `05` | Engine implementation | Test / execution artefact | Research engines | Explicit |

---

## 1.2 Concepts currently NOT owned by either document

These are deliberately recorded as gaps rather than assigned by assumption:

| Concept / governance need | Current owner | Consequence |
|---|---|---|
| Bitemporal validity (`valide_du`, `valide_au`, `connu_depuis`) | **NON DÉFINI** | Point-in-time knowledge cannot yet be represented by a canonical contract |
| Contradiction registry + arbitration history | **NON DÉFINI** | Contradictions can be discussed but no canonical decision object is defined here |
| Upward challenge / contestation of `04` | **NON DÉFINI** | `04` has explicit version history but no formal downstream challenge interface |
| Global ownership registry for every system concept | **NON DÉFINI** | Current ownership is distributed across documents and implicit processes |
| Cross-document dependency registry | **NON DÉFINI** | Interfaces are partly explicit in `04`, but no single machine-readable map exists |
| Capital-allocation policy | Outside `04` | `04` defines admissible evidence levels but not the actual risk policy |
| Post-promotion surveillance / champion degradation | Outside `04` | Explicitly identified as outside its scope |
| Regime taxonomy/classification | Dedicated future document | Condition 11 in `04` is suspended |
| Independent-review procedure | Governance protocol | `04` defines the principle but not the detailed procedure |

---

# 2. Interface map — `04` ↔ `05`

## 2.1 Explicit interfaces declared by `04`

`04 §9` explicitly identifies these interfaces:

| Interface | `04` responsibility | `05` / other responsibility | Failure if missing |
|---|---|---|---|
| Data QA / continuity | Validation principle | Detailed data contract | Quantitative result may be invalid |
| Full cost model | Promotion condition | Cost model detail | Promotion can be blocked or mis-measured |
| Technical freeze | Principle + required artefact scope | Detailed procedure | Confirmatory result not reproducible |
| Capacity / liquidity / market impact / factor exposure / leverage | Not treated | `05` or risk document | Portfolio suitability unresolved |
| Regime taxonomy | Suspended condition | Dedicated document | Regime coherence cannot currently promote/reject |
| Independent review | Principle | Governance protocol | Conflict/adjudication procedure unresolved |
| Post-promotion surveillance | Not treated | Master checklist phases 11/12 | Live degradation governance unresolved |

**Important rule already present in `04`:** a requirement cannot be considered satisfied by an implicit
reference to another document; the reference must appear in the interface table.

---

## 2.2 Directional dependency graph

```text
ASSET PROFILE
    │
    ├── temporal convention ───────────────┐
    ├── cost model ────────────────────────┤
    └── asset-specific parameters ─────────┤
                                           ↓
                                      05 DATA CONTRACT
                                           │
                ┌──────────────────────────┼──────────────────────────┐
                │                          │                          │
         coverage / QA              lineage / limits          anti-look-ahead
                │                          │                          │
                └──────────────────────────┼──────────────────────────┘
                                           ↓
                                    RESEARCH ENGINE
                                           │
                                           ↓
                              CONFIRMATORY RESULT / REPORT
                                           │
                                           ↓
                                      04 VALIDATION
                                           │
                 ┌─────────────────────────┼──────────────────────────┐
                 ↓                         ↓                          ↓
          evidence status            promotion                  invalidation /
          N0–N4                      conditions                  falsification
                 │                         │                          │
                 └─────────────────────────┼──────────────────────────┘
                                           ↓
                                  CAPITAL POLICY / GOVERNANCE
```

**This graph is descriptive only.** It does not assert that the research engine is already implemented
according to this graph; it records the interfaces implied by the current contracts.

---

# 3. Definitive separation: Définiteur / Producteur / Dépositaire / Consommateur

The current documents support a critical separation:

```text
DÉFINITEUR
    ↓
PRODUCTEUR
    ↓
DÉPOSITAIRE
    ↓
CONSOMMATEURS
```

A producer does not acquire semantic ownership merely by generating a value.

### Example: evidence level

```text
Définition       → 04 §7
Production       → promotion/evidence evaluation process (implementation not yet specified)
Dépôt            → research result / evidence record (canonical schema not yet specified)
Consommation     → promotion / capital-governance process
```

### Example: dataset identity

```text
Définition       → 05 §3
Production       → data transformation pipeline
Dépôt            → dataset metadata + QA/coverage report
Consommation     → research engines and validation reports
```

### Example: cost model

```text
Définition       → Asset Profile, referenced/enforced by 05
Production       → Asset Profile / cost-model process
Dépôt            → Asset Profile version
Consommation     → research, validation, execution
```

Where the current repository does not define the concrete producer or repository schema, the map keeps
that field explicitly unresolved.

---

# 4. Dependency inventory

## 4.1 `04` consumes

- Research charter inputs and declarations.
- Data-quality / continuity results from `05`.
- Full cost model governed by the Asset Profile / `05` interface.
- Technical freeze identifiers.
- Period consultation/consumption registry.
- Confirmatory test results.
- Bias audit results.
- Stability and robustness controls.
- Portfolio/contextual information for contextual drawdown assessment.

## 4.2 `04` produces

- Promotion eligibility decision.
- Evidence level N0–N4.
- Classification of result as invalidated, falsified, or non-interpretable.
- Governance state for period consumption and research family.
- Explicit requirements for the research charter.

## 4.3 `05` consumes

- Raw/source datasets.
- Asset Profile conventions.
- Transformation parameters.
- Multiple data sources where available.
- Engine implementation behaviour for anti-look-ahead and parity tests.

## 4.4 `05` produces

- Dataset identity and lineage.
- Coverage report.
- Continuity verdict.
- Transformation usage limits.
- Data QA verdict.
- Parity report.
- Evidence that anti-look-ahead checks were executed.
- Data contract constraints consumed by research/validation.

---

# 5. Contract status matrix

| Interface / contract | Status today | Frozen? | Owner explicit? | Machine-readable schema? |
|---|---|---:|---:|---:|
| `04` normative validation rules | Candidate freeze | No | Yes — `04` | No |
| `05` data integrity rules | Proposal / not validated | No | Yes — `05` | No |
| Research charter | Required by `04` | Per research | Yes — `04` | No |
| Dataset identity | Required by `05` | Per dataset | Partial | No |
| Coverage report | Required by `05` | Per dataset/result | Partial | No |
| Dataset lineage | Required by `05` | Per dataset | Partial | No |
| Technical freeze manifest | Required by `04` | Per confirmatory run | Interface only | No |
| Cost-model contract | Asset Profile dependency | Per asset/version | Partial | No |
| Evidence record | Required conceptually by `04` | Per result | Partial | No |
| Contradiction record | Not defined | — | No | No |
| Bitemporal record | Not defined | — | No | No |
| Upward challenge record | Not defined | — | No | No |

---

# 6. Contradictions and unresolved tensions discovered by mapping

This section does **not** resolve contradictions. It records them for later governance.

### C-01 — `04` is candidate-for-freeze while downstream interfaces are incomplete

`04` describes itself as complete/applicable except for the suspended regime condition, yet §9 leaves
several operational details to `05`, a risk document, a dedicated regime document, or governance
protocols. This is not necessarily a contradiction; it is an interface-boundary condition that must be
preserved when freezing `04`.

### C-02 — `05` is non-validated while `04` already makes `05` compliance blocking

`04 §5.3 c.4` makes survival under the complete costs of `05` blocking, while `05` is explicitly marked
proposal/non-validated. The current architecture therefore has a **normative dependency on a contract
that is not yet frozen**.

This must be tracked; it must not be silently resolved inside `07`.

### C-03 — Canonical format is required but not selected

`05 §6.1` requires a single canonical price-series format while leaving the format itself as a parameter
to decide. The contract principle exists; the concrete interface value does not.

### C-04 — Point-in-time protection is partial, not bitemporal

`04` protects temporal phase boundaries and records consultation/consumption history. That is not the
same as a canonical bitemporal representation of world validity versus knowledge time. No explicit
`valide_du / valide_au / connu_depuis` contract currently exists in `04` or `05`.

### C-05 — Contradiction governance is not a first-class object

`04` has a version journal and explicit arbitration history for some decisions, but the repository does
not yet define a generic contradiction lifecycle:

```text
contradiction → analysis → arbitration → decision → reason → version
```

This remains an architecture gap, not a defect to patch inside `04` or `05` at this stage.

### C-06 — Downstream contestation of `04` is not formalized

`04` can be modified by explicit arbitration and versioning, but there is currently no formal contract
for a downstream brick to issue a machine-auditable `POINT DE CONTESTATION — 04 §X` with impact and
resolution.

---

# 7. Architecture gaps that must be resolved BEFORE the next substantive brick

These are the outputs of the cartography, not proposed implementation details yet:

1. **Global concept registry:** one place that identifies the authoritative definer of every cross-system concept.
2. **Interface registry:** one place that records source → object → contract → version → destination.
3. **Dataset/evidence record schemas:** the current documents define concepts but not machine-readable records.
4. **Bitemporal contract:** world validity vs knowledge validity must become explicit if point-in-time research is required.
5. **Contradiction object + arbitration ledger:** preserve why a contradiction was resolved and against which version.
6. **Upward challenge mechanism:** downstream bricks must be able to contest an upstream rule without silently overriding it.
7. **Criticality classification:** determine when a change requires full, intermediate or light audit.

**No new Asset Mechanics / Asset Profile redesign should be accepted as canonical until these ownership
and interface questions have been resolved at the required criticality.**

---

# 8. Criticality rule — recorded as architecture requirement, not yet implemented

The proposed R1 model is compatible with the current map:

| Criticality | Trigger | Audit depth |
|---|---|---|
| C3 | New normative concept or central architecture | Full |
| C2 | New brick consuming frozen contracts | Intermediate |
| C1 | Documentary extension with no semantic change | Light |

**Status:** proposal to be validated by the architecture/governance phase. It is not silently promoted to
`04` or `05`.

---

# 9. Next required object

The next object should be a **formal machine-readable System Registry**, generated from this factual map,
with at minimum:

```text
CONCEPT_ID
DEFINITION_OWNER
PRODUCER
REPOSITORY
CONSUMERS
CONTRACT_ID
CONTRACT_VERSION
SOURCE_OF_TRUTH
VALID_FROM
VALID_TO
KNOWN_SINCE
CRITICALITY
CHALLENGE_STATUS
```

This is the point at which the proposed bitemporal, contradiction and upward-contestation safeguards can
become actual system mechanisms rather than prose principles.

---

## 10. Source anchors

Primary sources used for this cartography:

- `docs/04-VALIDATION-CRITERIA.md`, v0.6.1, SHA `e398bb8a96a97bf496550ad569910b3f35507093`.
- `docs/05-DATA-CONTRACT.md`, v0.1, SHA `e7426c6c5ee4a122aecc8c8719f9cdd9173841e7`.

No attempt was made in this document to rewrite either source.
