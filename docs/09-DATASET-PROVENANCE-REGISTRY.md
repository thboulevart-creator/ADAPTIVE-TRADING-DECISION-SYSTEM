# 09 — DATASET / PROVENANCE REGISTRY

**Version:** 0.1 — ARCHITECTURE PROPOSAL / NON-NORMATIVE
**Date:** 23 août 2026
**Status:** proposal derived from `04`, `05` and `08`; no rule in this document is normative until arbitrated and incorporated into the applicable contract.
**Purpose:** establish the minimum architecture required to identify every dataset used by research, reconstruct its lineage, expose transformations and usage limits, and prevent an unverified or temporally invalid dataset from silently entering a quantitative result.

---

## 0. Scope

This registry covers **datasets**, not individual market facts or research conclusions.

It answers five questions:

1. **What exactly was used?**
2. **Where did it come from?**
3. **What happened to it before use?**
4. **What was known about it, and when?**
5. **What uses are permitted or prohibited?**

This document does not define the semantics of validation criteria. `04` remains the reference for validation concepts. `05` remains a proposal until separately approved.

---

# 1. Core principle

> **A dataset is not identified by its filename, location, or intended meaning. It is identified by a verifiable record of its content, provenance, transformation history, temporal status, and declared usage constraints.**

Therefore:

```text
SOURCE
  ↓
ACQUISITION
  ↓
RAW DATASET
  ↓
VALIDATION
  ↓
TRANSFORMATION
  ↓
DERIVED DATASET
  ↓
CONSUMPTION
  ↓
RESULT
```

Every arrow must be reconstructable.

---

# 2. Dataset identity

Every dataset receives a stable identifier independent of its filename.

Minimum identity record:

| Field | Meaning |
|---|---|
| `dataset_id` | Globally unique immutable identifier |
| `dataset_version` | Version of the dataset record/content |
| `content_hash` | Cryptographic hash of the exact content used |
| `format` | Physical representation |
| `schema_version` | Schema applied to the dataset |
| `instrument` | Instrument / asset represented |
| `granularity` | Tick, M1, H1, etc. |
| `timezone_storage` | Storage timezone, expected UTC when contract requires it |
| `created_at` | Registry creation timestamp |
| `created_by` | Actor/process creating the record |
| `status` | Proposed / validated / restricted / retired |

**Important:** filename, folder and URL are metadata only. They cannot constitute identity.

---

# 3. Source record

Each dataset must identify its immediate source.

Minimum fields:

```text
source_id
source_type
provider
instrument
acquisition_method
source_location_or_reference
acquired_at
acquired_by
source_version_if_known
source_content_hash_if_available
```

A source reference that cannot be independently verified must be marked accordingly. The registry must never silently convert an unverifiable source into a verified one.

---

# 4. Parent / lineage

Every transformed dataset must reference its immediate parent dataset(s).

```text
DERIVED DATASET
    ↓
parent_dataset_id
    ↓
TRANSFORMATION RECORD
    ↓
child_dataset_id
```

For a merge:

```text
PARENT A ─┐
          ├── TRANSFORMATION ──> CHILD
PARENT B ─┘
```

The registry must support one-to-many and many-to-one lineage.

A dataset without a known parent is not automatically invalid; it must instead carry an explicit `lineage_status = UNKNOWN` and the resulting limitation must be visible to consumers.

---

# 5. Transformation record

Every transformation creates a new dataset identity.

Minimum record:

| Field | Requirement |
|---|---|
| `transformation_id` | Unique identifier |
| `parent_dataset_ids` | All immediate parents |
| `child_dataset_id` | Produced dataset |
| `operation_type` | Filter / extract / merge / aggregate / resample / convert / repair / other |
| `parameters` | Exact parameters used |
| `code_or_tool_version` | Version of implementation |
| `operator` | Human or automated process |
| `executed_at` | Execution timestamp |
| `input_validation_status` | Status of parent at execution |
| `output_validation_status` | Resulting status |
| `declared_limitations` | Known restrictions |

**No validation is inherited automatically from a parent.** A child must be assessed according to its own characteristics and intended use.

---

# 6. Coverage and integrity evidence

The registry must link each dataset to a coverage/integrity report.

Minimum evidence:

```text
source(s)
files / objects inspected
instrument
frequency
period observed
row / bar count
duplicates
missing periods
interruptions
continuity verdict
anomalies
validation timestamp
validator / process version
```

The registry must distinguish:

```text
NOT CHECKED
CHECKED — PASS
CHECKED — FAIL
CHECKED — RESTRICTED
```

Absence of a check is **not** equivalent to a pass.

A filename-based inventory is never sufficient evidence of coverage.

---

# 7. Usage contract

Every dataset must declare its intended usage envelope.

```text
AUTHORIZED USES
PROHIBITED USES
VALIDITY CONDITIONS
KNOWN LIMITATIONS
REQUIRED PRECONDITIONS
```

Example:

```text
Authorized:
  setup detection
  transactions shorter than declared horizon

Prohibited:
  simulation beyond extracted window
  index traversal across undeclared gaps
  use as a continuous market series

Condition:
  transaction horizon < declared maximum
```

A consumer must not infer permitted usage from the dataset name or from the existence of a prior validation.

---

# 8. Temporal provenance — bitemporal compatibility

The registry must support two distinct temporal dimensions.

### 8.1 World validity

```text
valid_from
valid_to
```

This describes when the represented market/data fact is valid in the world.

### 8.2 Knowledge validity

```text
known_from
known_to   [optional when knowledge ceases to be available/valid]
```

This describes when the information was available to the research process.

Therefore:

> `valid_from = 2019` does **not** imply `known_from = 2019`.

A historical dataset reconstructed in 2026 must not be presented as information that was necessarily available to a researcher in 2019.

The exact semantics and mandatory fields belong to the future temporal contract (`10`); this registry only reserves the interface.

---

# 9. Acquisition timestamp vs market timestamp

The registry must never conflate:

```text
market_timestamp
acquired_at
validated_at
registered_at
used_at
```

These timestamps answer different questions and must remain separately queryable.

Example:

```text
Market observation: 2019-06-03
Acquired:           2026-08-20
Validated:          2026-08-21
Used in research:  2026-08-22
```

This is historically valid market data, but it is not evidence that the researcher knew the observation in 2019.

---

# 10. Reproducibility anchor

A result must be traceable to an immutable dataset state.

Minimum result-to-data linkage:

```text
RESULT_ID
  ↓
RESEARCH_RUN_ID
  ↓
CODE_VERSION
  ↓
CONFIGURATION_VERSION
  ↓
DATASET_ID + DATASET_VERSION
  ↓
CONTENT_HASH
  ↓
PROVENANCE CHAIN
```

Changing the dataset must therefore produce a distinguishable research state, even when the filename remains unchanged.

---

# 11. Dataset status machine

Proposed lifecycle:

```text
REGISTERED
    ↓
IDENTITY-CHECKED
    ↓
COVERAGE-CHECKED
    ↓
QUALITY-CHECKED
    ↓
USAGE-DECLARED
    ↓
VALIDATED / RESTRICTED
    ↓
CONSUMABLE
```

Failure at any stage must be represented explicitly.

A dataset marked `RESTRICTED` may be consumable only for explicitly authorized uses.

A dataset marked `FAILED` must not be silently promoted to `CONSUMABLE`.

---

# 12. Dataset substitution control

A research run must not silently substitute one dataset for another.

If a dataset changes:

```text
OLD DATASET
    ↓
SUBSTITUTION EVENT
    ↓
NEW DATASET
    ↓
IMPACT ASSESSMENT
    ↓
NEW RESEARCH RUN / EXPLICIT REPRODUCTION
```

A filename remaining identical is irrelevant.

The substitution record must identify:

- old dataset ID/version/hash;
- new dataset ID/version/hash;
- reason;
- actor/process;
- timestamp;
- whether the result must be recomputed;
- affected research runs.

---

# 13. Immutable evidence vs mutable metadata

The architecture must distinguish evidence from annotation.

### Immutable evidence

Examples:

- content hash;
- captured raw file/object;
- exact transformation parameters;
- code/tool version;
- source artifact when retained;
- validation output.

### Mutable metadata

Examples:

- description;
- owner/contact;
- tags;
- human commentary.

Updating commentary must not alter the identity of the dataset content.

If content changes, the dataset identity/version must change.

---

# 14. Consumer gate

Before a research or validation engine consumes a dataset, it must be able to answer:

```text
Is the dataset identified?
Is the exact content anchored?
Is lineage known or explicitly unknown?
Is coverage checked?
Is continuity status known?
Are usage restrictions satisfied?
Is the temporal status compatible with the research question?
Is the dataset version reproducible?
```

If a mandatory answer is `NO` or `UNKNOWN`, the engine must not silently treat the dataset as fully validated.

The exact blocking policy is a future implementation/validation decision and must be aligned with `04` before becoming normative.

---

# 15. Look-ahead protection

The registry must make it possible to detect at least three distinct failures:

### A. Data look-ahead

A dataset contains information unavailable at the decision timestamp.

### B. Documentation look-ahead

A research process uses a later reconstruction or classification as if it had been known at the historical timestamp.

### C. Pipeline look-ahead

A transformation, cleaning step, feature, label or filter uses information occurring after the point at which the consuming decision was supposed to be made.

These are distinct failure classes and must not be collapsed into a generic `look_ahead = true/false` flag.

---

# 16. Failure modes

Minimum registry failure taxonomy:

| ID | Failure | Example |
|---|---|---|
| DF-01 | Unknown identity | Dataset referenced only by filename |
| DF-02 | Unknown lineage | Derived file has no parent reference |
| DF-03 | Unverified coverage | Acquisition assumed complete from filenames |
| DF-04 | Hidden transformation | File converted without new identity |
| DF-05 | Usage overreach | Restricted extraction used as continuous series |
| DF-06 | Temporal ambiguity | Acquisition date confused with market date |
| DF-07 | Knowledge look-ahead | Later information treated as historically known |
| DF-08 | Silent substitution | Dataset changed without new research run |
| DF-09 | Integrity drift | Content changes while identifier remains unchanged |
| DF-10 | Validation inheritance | Child dataset assumed valid because parent was valid |
| DF-11 | Pipeline look-ahead | Transformation uses future information |
| DF-12 | Provenance break | One or more lineage links cannot be reconstructed |

---

# 17. Ownership and interface map

| Element | Owner role | Consumer |
|---|---|---|
| Dataset identity | Dataset Registry | All research engines |
| Content hash | Registry / acquisition pipeline | Reproducibility / audit |
| Source record | Acquisition process | Registry / audit |
| Transformation record | Transformation pipeline | Registry / audit |
| Coverage report | Quality-control process | Validation / audit |
| Usage declaration | Dataset governance | Research / validation |
| Temporal provenance | Temporal contract + registry | Historical research / validation |
| Research-run linkage | Research execution layer | Audit / reproduction |

**Important:** the registry is the depositor of provenance records; it does not become the semantic owner of concepts defined elsewhere.

---

# 18. Required interface with `04`

This registry must provide `04` with evidence sufficient to determine whether the dataset-related validation conditions are satisfied.

It must **not** redefine `04`'s validation criteria.

Interface direction:

```text
DATASET REGISTRY
      ↓ evidence
04 VALIDATION CRITERIA
      ↓ verdict / promotion decision
RESEARCH STATE
```

If `04` requires a concept that this registry cannot currently prove, that gap becomes an explicit interface failure rather than an implicit assumption.

---

# 19. Required interface with `05`

`05` is the proposed home of the broader data contract. This registry operationalizes the dataset/provenance portion without assuming that `05` is already approved.

Potential future contract fields include:

```text
dataset identity
coverage
continuity
transformation
lineage
format
units
temporal provenance
cost model reference
usage limits
```

No field in this section becomes normative merely because it appears here.

---

# 20. Minimum registry object — proposed schema

```yaml
dataset_id:
dataset_version:
content_hash:
status:
source:
  source_id:
  provider:
  acquisition_method:
  acquired_at:
  source_reference:
market_scope:
  instrument:
  granularity:
  valid_from:
  valid_to:
knowledge_scope:
  known_from:
  known_to:
lineage:
  parent_dataset_ids: []
  lineage_status:
transformation:
  transformation_id:
  operation_type:
  parameters:
  code_version:
  executed_at:
quality:
  coverage_report_id:
  continuity_status:
  validation_status:
usage:
  authorized: []
  prohibited: []
  conditions: []
limitations: []
research_runs: []
registered_at:
registered_by:
```

This schema is an architectural proposal, not yet a frozen implementation contract.

---

# 21. Acceptance tests for the future implementation

The registry implementation should not be accepted until it can demonstrate at minimum:

1. Two files with different content cannot share the same immutable dataset identity.
2. A transformed dataset automatically receives a distinct identity.
3. Parent datasets can be reconstructed from a child record.
4. A missing coverage check is distinguishable from a passed coverage check.
5. Usage restrictions are visible to consumers.
6. Acquisition date and market timestamp remain distinct.
7. `valid_from` and `known_from` can represent different dates.
8. A dataset substitution creates an auditable event.
9. A research run can be reproduced against the exact dataset hash/version.
10. A restricted dataset cannot silently enter a consumer path requiring full validation.
11. A future-looking transformation can be recorded as a pipeline look-ahead failure.
12. Provenance can be reconstructed from raw/source dataset to final consumed dataset.

---

# 22. Open decisions — deliberately not resolved here

The following remain architecture decisions rather than invented defaults:

- exact identifier format;
- hash algorithm if not already fixed globally;
- physical registry implementation;
- retention policy for raw source artifacts;
- exact bitemporal semantics (`10`);
- mandatory vs optional provenance fields by criticality;
- blocking policy at consumer gate;
- relationship with the final frozen `05` contract;
- handling of corrected source data and retroactive provider revisions.

These must be resolved before implementation is declared normative.

---

# 23. Integration gate

`09` is not considered integrated merely because this file exists.

Integration requires:

```text
09 PROPOSAL
   ↓
OWNERSHIP / INTERFACE REVIEW
   ↓
ADVERSARIAL AUDIT
   ↓
04 IMPACT CHECK
   ↓
05 IMPACT CHECK
   ↓
ARBITRATION
   ↓
VERSIONED CONTRACT
   ↓
IMPLEMENTATION TESTS
   ↓
INTEGRATED
```

Until then, this document is an architectural proposal and must not be cited as a frozen normative rule.

---

# 24. Next dependency

The next architectural object is:

**`10-TEMPORAL-POINT-IN-TIME-CONTRACT`**

Its role is to freeze the semantics of `valid_from / valid_to / known_from / known_to`, decision timestamps, information availability, and the tests required to prevent historical and documentary look-ahead.
