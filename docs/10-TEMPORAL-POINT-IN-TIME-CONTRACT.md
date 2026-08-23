# 10 — TEMPORAL / POINT-IN-TIME CONTRACT

**Version:** 0.1 — ARCHITECTURE PROPOSAL / NON-NORMATIVE  
**Date:** 23 août 2026  
**Status:** proposal derived from `08` and `09`; no rule in this document is normative until arbitrated and incorporated into the applicable contract.

**Purpose:** establish the temporal semantics required to prevent historical, documentary, and pipeline look-ahead, while preserving a reconstructible distinction between when a fact was true, when information became available, and when a research process was allowed to use it.

---

## 0. Why this contract exists

A historical timestamp alone does not prove historical availability.

The system must distinguish at minimum:

```text
WHEN THE WORLD WAS TRUE
        ≠
WHEN THE INFORMATION WAS KNOWN
        ≠
WHEN THE RESEARCH PROCESS WAS ALLOWED TO USE IT
        ≠
WHEN THE RESULT WAS PRODUCED
```

Without this distinction, a research pipeline can accidentally use information reconstructed, corrected, classified, or transformed after the decision timestamp while presenting the result as historical evidence.

This contract therefore acts as a **temporal admissibility gate**, not merely as a timestamp convention.

---

# 1. Scope

This contract applies to any object whose temporal state can affect a research conclusion, including:

- market observations;
- datasets;
- derived datasets;
- metadata;
- classifications;
- validation evidence;
- economic/event information;
- transformations;
- labels;
- features;
- research runs;
- decision timestamps;
- result records.

It does not redefine the validation criteria of `04` or the broader data contract of `05`.

---

# 2. Four distinct clocks

The architecture must preserve four distinct temporal questions.

## 2.1 World validity clock

```text
valid_from
valid_to
```

Question:

> During which period was the represented fact/object valid in the world being studied?

Example: a market observation belongs to a market timestamp in 2019.

---

## 2.2 Knowledge availability clock

```text
known_from
known_to
```

Question:

> During which period was this information actually available to the relevant research process?

`known_from` is not inferred from `valid_from`.

A dataset acquired in 2026 may represent market facts from 2019 while having `known_from = 2026` for that research process.

---

## 2.3 Permitted-use clock

```text
usable_from
usable_to
```

Question:

> From which point was the information contractually/admissibly allowed to influence the consuming process?

This exists because information can be known but still prohibited from use by a research protocol, embargo, validation state, or experiment design.

If this dimension is not needed for a specific object, the record must explicitly state that it is not applicable rather than silently omitting the distinction.

---

## 2.4 Execution clock

```text
used_at
executed_at
registered_at
validated_at
```

Question:

> When did the system actually acquire, validate, register, transform, consume, or produce the object?

Execution timestamps are audit evidence. They do not replace knowledge availability.

---

# 3. Canonical temporal model

The minimum conceptual model is:

```text
                 WORLD
                   │
          valid_from / valid_to
                   │
                   ▼
             INFORMATION
                   │
          known_from / known_to
                   │
                   ▼
             PERMITTED USE
                   │
          usable_from / usable_to
                   │
                   ▼
              CONSUMPTION
                   │
                 used_at
```

The registry in `09` stores the provenance record; this contract defines the temporal semantics consumed by that registry and by research engines.

---

# 4. Decision timestamp

Every historical research decision must have an explicit **decision timestamp**.

```text
decision_at
```

This is the temporal boundary against which information admissibility is evaluated.

For a decision at time `T`, information is admissible only if its availability and usage conditions satisfy the contract at `T`.

The mere fact that an observation carries a timestamp `<= T` is insufficient.

---

# 5. Point-in-time admissibility rule

For a decision at `T`, a data object is temporally admissible only if all required conditions are satisfied:

```text
valid_at(T)                 = TRUE / explicitly applicable
known_at(T)                 = TRUE
usable_at(T)                = TRUE
pipeline_safe_at(T)        = TRUE
```

Conceptually:

```text
ADMISSIBLE(T)
 = VALID(T)
 ∧ KNOWN(T)
 ∧ USABLE(T)
 ∧ PIPELINE_SAFE(T)
```

A missing temporal fact is **not** equivalent to `TRUE`.

If an essential temporal predicate is `UNKNOWN`, the consumer must not silently classify the object as historically admissible.

The exact blocking policy is subject to arbitration with `04`.

---

# 6. The central distinction: true vs known

The following statement is mandatory at the semantic level:

> **Historical truth does not imply historical knowledge.**

Example:

```text
Market fact:
    valid_from = 2019-06-03

Research acquisition:
    known_from = 2026-08-20
```

This may be perfectly legitimate for a modern reconstruction of history.

It must not automatically be treated as evidence that the same information was available to a researcher on `2019-06-03`.

This distinction directly protects against **documentation look-ahead**.

---

# 7. Dataset acquisition is not knowledge of the world

The following timestamps must never be conflated:

```text
market_timestamp
acquired_at
registered_at
validated_at
used_at
```

Example:

```text
market_timestamp = 2019-06-03 14:30
acquired_at       = 2026-08-20
registered_at     = 2026-08-21
validated_at      = 2026-08-21
used_at           = 2026-08-22
```

This record proves that the market observation belongs to 2019.

It does **not** prove that the research process had that information in 2019.

---

# 8. Retroactive revisions

A provider or research process may revise historical information after the represented event.

Examples:

- corrected historical prices;
- revised economic statistics;
- revised index constituents;
- corrected corporate actions;
- revised classifications;
- repaired missing records;
- retrospective event labels.

A revision must preserve its temporal history.

Conceptually:

```text
ORIGINAL VERSION
      ↓
REVISION EVENT
      ↓
REVISED VERSION
```

The revised version must not silently overwrite the historical evidence used by an earlier research run.

If a research question is explicitly **vintage-aware**, the applicable vintage must be selected by knowledge availability, not by today's corrected value.

---

# 9. Vintage principle

When multiple versions of the same historical information exist, the system must be able to distinguish:

```text
EVENT DATE
DATA VINTAGE / KNOWLEDGE DATE
CURRENT CORRECTED VALUE
```

A research process asking:

> "What could have been known at time T?"

must use the appropriate information vintage available at `T`, not necessarily the latest corrected historical dataset.

A process asking:

> "What is the best reconstruction of historical reality today?"

may use a later corrected vintage, but that research mode must be explicitly declared.

These two research modes must not be silently mixed.

---

# 10. Research temporal modes

Every research run should declare one of the following modes.

### MODE-HISTORICAL

Question:

> What could the system have known and used at the historical decision time?

Requirements:

- point-in-time admissibility enforced;
- later information prohibited unless explicitly modeled as available at the time;
- vintage selection required where revisions exist.

### MODE-RECONSTRUCTION

Question:

> What does the best currently available reconstruction say about the historical period?

Later-acquired or revised information may be used when explicitly declared.

This mode is useful for descriptive research but must not be presented as a historical tradability claim.

### MODE-HYBRID

Any combination of historical and reconstructed information.

This mode is considered high-risk and requires explicit declaration of which inputs are historical-vintage and which are retrospective.

It must not be silently labeled `MODE-HISTORICAL`.

---

# 11. Pipeline look-ahead

Temporal safety applies not only to raw inputs but to every transformation.

A transformation can introduce look-ahead even when all source datasets are historically valid.

Examples:

```text
FULL-SAMPLE NORMALIZATION
FUTURE-AWARE IMPUTATION
CENTERED MOVING WINDOW
FUTURE BAR FILTER
LABEL LEAKAGE
POST-EVENT CLASSIFICATION
FULL-PERIOD FEATURE SELECTION
```

Therefore every transformation must be evaluated relative to the consuming decision timestamp.

For a transformation `F` producing output `Y_t`:

```text
Y_t = F(X)
```

The output is point-in-time safe only if every input element influencing `Y_t` was admissible at `t` under the declared research mode.

---

# 12. Transformation dependency closure

A consumer must not inspect only the final dataset timestamp.

Temporal admissibility propagates through the complete dependency graph:

```text
RAW A ─┐
       ├─> TRANSFORM 1 ─> DERIVED B ─┐
RAW C ─┘                             │
                                     ├─> FEATURE D ─> DECISION
RAW E ───────────────> TRANSFORM 2 ──┘
```

For decision time `T`, every node on the dependency path must be temporally admissible at `T`.

A single future-dependent node invalidates the downstream path unless the research mode explicitly permits retrospective reconstruction.

---

# 13. Unknown temporal provenance

The system must distinguish:

```text
KNOWN SAFE
KNOWN UNSAFE
UNKNOWN
NOT APPLICABLE
```

`UNKNOWN` must never be silently converted into `KNOWN SAFE`.

Examples of temporal unknowns:

- acquisition vintage not recorded;
- provider revision history unavailable;
- transformation parameters missing;
- timestamp semantics unclear;
- publication time unknown;
- source availability cannot be reconstructed.

Such uncertainty becomes an explicit limitation of the research evidence.

---

# 14. Publication time vs event time

For external information, the architecture must distinguish at minimum:

```text
event_time
publication_time
availability_time
```

Example:

```text
Economic event:       10:00
Official publication: 10:30
System availability: 10:31
```

A strategy decision at `10:15` cannot use the information merely because its `event_time` is `10:00`.

For information whose availability depends on transmission, ingestion, parsing, or release mechanics, the admissibility boundary must use the earliest defensible **availability time**, not the underlying event time.

---

# 15. Timezone and clock normalization

Temporal comparisons must use an explicit timezone convention.

Every temporal object must declare or inherit an unambiguous timezone.

The system must prevent silent comparison between timestamps whose timezone semantics are unknown.

Canonical storage may be UTC where required by the broader data contract, but this document does not freeze a physical storage format.

The semantic requirement is:

> **A timestamp used for admissibility must be unambiguous and comparable.**

---

# 16. Boundary semantics

Temporal intervals must define whether their endpoints are inclusive or exclusive.

The implementation must not rely on informal interpretation of:

```text
valid_to
known_to
usable_to
```

Recommended conceptual convention:

```text
[start, end)
```

meaning:

```text
start INCLUDED
end EXCLUDED
```

This is a proposal pending technical arbitration; whichever convention is chosen must be globally consistent.

---

# 17. Late-arriving information

Information can become available after the decision timestamp but before research execution.

Example:

```text
decision_at = 10:00
information available = 10:05
research run executed = 10:10
```

The information is valid historical information, but it is **not admissible** for the `10:00` decision in `MODE-HISTORICAL`.

Execution time must never expand the historical information set retroactively.

---

# 18. Future knowledge firewall

The research engine should conceptually enforce:

```text
DECISION AT T
     │
     ├── information available by T  → MAY ENTER
     │
     └── information available after T → BLOCK
```

This firewall applies to:

- raw data;
- metadata;
- labels;
- classifications;
- feature engineering;
- filters;
- parameter selection;
- model selection;
- validation annotations;
- manual research notes.

The firewall is temporal, not merely data-oriented.

---

# 19. Manual research information

Human annotations can also create look-ahead.

Examples:

```text
"This was a high-quality setup" recorded after outcome
"This period was a special regime" classified using later knowledge
"This event was significant" based on subsequent market reaction
```

A manual annotation used by a historical research run must have its own knowledge timestamp or provenance sufficient to establish when the researcher could have known it.

Human judgment is not exempt from point-in-time controls.

---

# 20. Model and parameter look-ahead

Point-in-time protection must include research choices, not only observations.

Potential leakage sources:

- selecting parameters after seeing the complete sample;
- selecting instruments using future performance;
- changing filters after inspecting test outcomes;
- selecting a model because of later results;
- retroactively redefining labels;
- choosing a validation window after observing its result.

These events belong to the broader research/probatory controls, but this temporal contract provides the temporal interface required to detect them.

---

# 21. Temporal provenance object

Minimum proposed object:

```yaml
temporal_provenance:
  event_time:
  valid_from:
  valid_to:
  known_from:
  known_to:
  usable_from:
  usable_to:
  acquired_at:
  registered_at:
  validated_at:
  used_at:
  timezone:
  timestamp_semantics:
  vintage_id:
  source_availability_evidence:
```

Not every field is mandatory for every object. Mandatory fields depend on object type and research mode.

The final mandatory-field matrix must be arbitrated before implementation.

---

# 22. Interface with `09`

`09 DATASET / PROVENANCE REGISTRY` stores provenance and exposes dataset-level temporal metadata.

Direction:

```text
10 TEMPORAL CONTRACT
        ↓ semantics
09 DATASET REGISTRY
        ↓ temporal evidence
RESEARCH CONSUMER
```

`09` must not invent temporal semantics independently.

`10` must not become the owner of dataset identity or lineage.

Ownership remains separated:

```text
10 → temporal semantics
09 → provenance record / dataset registry
```

---

# 23. Interface with `04`

`04` remains the authority for validation criteria and proof-level semantics.

This contract supplies temporal evidence and admissibility status; it does not redefine proof levels.

Conceptual interface:

```text
DATA / PROVENANCE
        ↓
TEMPORAL ADMISSIBILITY
        ↓
04 VALIDATION CRITERIA
        ↓
VALIDATION / PROMOTION DECISION
```

If `04` requires a historical claim that the temporal contract cannot substantiate, the correct result is an explicit evidence/interface failure, not an inferred pass.

---

# 24. Interface with `05`

`05 DATA CONTRACT` is currently a proposal.

This document supplies temporal semantics that may later become part of the frozen data contract.

Potential interface fields include:

```text
market/event timestamp
publication timestamp
availability timestamp
vintage
validity interval
knowledge interval
timezone
revision status
```

No field becomes normative in `05` solely because it appears here.

---

# 25. Failure taxonomy

Minimum temporal failure classes:

| ID | Failure | Example |
|---|---|---|
| TP-01 | Truth/knowledge conflation | Historical fact treated as historically known |
| TP-02 | Acquisition look-ahead | Dataset acquired after decision used as if available before it |
| TP-03 | Publication look-ahead | Later publication used for earlier decision |
| TP-04 | Pipeline look-ahead | Future observations enter a transformation |
| TP-05 | Label leakage | Outcome-derived label influences historical decision |
| TP-06 | Revision leakage | Later corrected vintage used in historical mode |
| TP-07 | Parameter look-ahead | Parameter selected using future/test results |
| TP-08 | Manual annotation leakage | Later human classification used historically |
| TP-09 | Timestamp ambiguity | Timezone/semantics cannot be established |
| TP-10 | Unknown availability | Publication/event time known but actual availability unknown |
| TP-11 | Boundary error | Inclusive/exclusive endpoint mishandled |
| TP-12 | Silent mode mixing | Reconstruction data used inside historical mode |
| TP-13 | Dependency leakage | Safe final dataset depends on unsafe upstream node |
| TP-14 | Retroactive overwrite | Revised data replaces earlier vintage without trace |
| TP-15 | Execution-time leakage | Research execution time incorrectly treated as decision availability |

---

# 26. Acceptance tests

The implementation must eventually demonstrate at least:

1. A 2019 market timestamp acquired in 2026 cannot automatically qualify as historically known in 2019.
2. An information item published after `decision_at` is blocked in `MODE-HISTORICAL`.
3. A transformation using future observations is detected or declared unsafe.
4. A later corrected data vintage can be distinguished from an earlier vintage.
5. Event time and publication/availability time remain distinct.
6. Unknown temporal provenance is distinguishable from verified safety.
7. A downstream feature inherits temporal restrictions from all upstream dependencies.
8. A research run declares its temporal mode.
9. Historical and reconstruction modes cannot be silently mixed.
10. Manual annotations can carry temporal provenance when they influence research.
11. Parameter/model selection can be audited for temporal leakage.
12. Timestamp timezone and boundary semantics are explicit.
13. Retroactive revisions do not overwrite the evidence state of an earlier research run.
14. A decision can be reconstructed from the information set admissible at its decision timestamp.
15. A temporal failure remains visible after downstream transformations and cannot disappear through renaming or re-registration.

---

# 27. Adversarial tests

Before this contract is frozen, the following attacks must be attempted.

### A1 — Historical file acquired today

Claim:

> "The bars are dated 2019, therefore they were known in 2019."

Expected result: **REJECT**.

### A2 — Future normalization

A feature is normalized using the mean and standard deviation of the complete sample.

Expected result: **PIPELINE LOOK-AHEAD**.

### A3 — Revised economic data

A 2019 backtest uses a value revised in 2025.

Expected result: allowed only in reconstruction mode; blocked or explicitly flagged in historical mode.

### A4 — Event timestamp deception

An event occurred at 10:00 but was published at 10:30. A decision occurs at 10:15.

Expected result: event information unavailable at 10:15.

### A5 — Human hindsight label

A researcher labels historical setups after inspecting their future outcomes.

Expected result: label unavailable for historical decision unless independently timestamped and justified.

### A6 — Future parameter optimization

Parameters are optimized on the entire dataset and then presented as fixed historical parameters.

Expected result: research/probatory failure; temporal leakage recorded.

### A7 — Silent vintage replacement

The provider replaces a historical file with a corrected version under the same filename.

Expected result: dataset identity/version/hash changes; substitution event required.

### A8 — Safe child, unsafe parent

A derived dataset carries a clean timestamp but depends on a future-aware parent transformation.

Expected result: dependency-chain failure.

---

# 28. Required temporal audit record

Every historical research run should be capable of producing a compact temporal audit:

```text
RUN_ID
RESEARCH_MODE
DECISION_TIME_POLICY
DATASET_VINTAGES
KNOWLEDGE_CUTOFFS
AVAILABILITY_EVIDENCE
TRANSFORMATION_VERSIONS
TEMPORAL_EXCEPTIONS
TEMPORAL_FAILURES
FINAL_ADMISSIBILITY_VERDICT
```

This record is part of reproducibility evidence and must remain linked to the research run.

---

# 29. Contestability

Temporal semantics must remain contestable through the future `12 UPWARD CHALLENGE PROTOCOL`.

A downstream component may submit:

```text
POINT OF CONTESTATION
    ↓
TEMPORAL OBJECT / RULE
    ↓
EVIDENCE
    ↓
IMPACT
    ↓
AUDIT
    ↓
ARBITRATION
```

A frozen temporal rule is authoritative until changed through governance, but **freeze ≠ immunity from challenge**.

---

# 30. Criticality

Proposed default criticality:

**C3 — central architectural contract.**

Reason: temporal semantics affect historical validity across datasets, research, validation, and downstream decision claims.

Any implementation or extension of this contract must therefore receive the full C3 audit unless a future governance protocol explicitly permits a lower classification for a non-semantic change.

---

# 31. Open decisions — deliberately unresolved

The following are intentionally not invented here:

- final mandatory-field matrix by object type;
- final interval convention;
- exact vintage identifier format;
- physical storage implementation;
- source-specific availability rules;
- maximum tolerated clock uncertainty;
- treatment of missing publication timestamps;
- precise integration point with final `05`;
- exact blocking/escalation policy under `04`;
- whether `usable_from/usable_to` belongs in the final canonical contract or remains a derived governance field.

These require explicit arbitration.

---

# 32. Integration gate

`10` is not integrated merely because this document exists.

Required sequence:

```text
10 PROPOSAL
   ↓
OWNERSHIP / INTERFACE REVIEW
   ↓
04 IMPACT CHECK
   ↓
05 IMPACT CHECK
   ↓
ADVERSARIAL TEMPORAL AUDIT
   ↓
CONTRADICTION REVIEW
   ↓
ARBITRATION
   ↓
VERSIONED CONTRACT
   ↓
IMPLEMENTATION TESTS
   ↓
INTEGRATED
```

Until that sequence is completed, this document is an architectural proposal only.

---

# 33. Next dependency

The next architectural object is:

**`11-CONTRADICTION-ARBITRATION-REGISTRY`**

Its purpose is to prevent contradictory definitions, decisions, and corrections from disappearing from the system history, while preserving explicit ownership, evidence, arbitration rationale, and version lineage.
