# DATA-01 — DATA ↔ TEMPORAL OWNERSHIP BOUNDARY V0.1

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Status:** `FROZEN DOCUMENTARY BOUNDARY / IMPLEMENTATION NOT AUTHORIZED`  
**First-use claim:** `CC02_DESCRIPTIVE_MARKET_BEHAVIOR`  
**First-use semantic limit:** `RETROSPECTIVE_DESCRIPTIVE_ONLY`

## 1. Purpose

DATA-01 selects the exact first-use dataset surface and freezes the interface between Data-owned semantics and future Temporal-owned semantics.

The boundary exists to prevent a valid Data identity/admissibility result from being laundered into a historical point-in-time claim.

```text
DATA VALIDITY != TEMPORAL VALIDITY
```

## 2. Data-owned semantics

For the selected first-use surface, Data may own and attest only facts such as:

```text
- exact dataset identity;
- exact content binding;
- exact file-set binding;
- exact schema identity;
- source identity;
- parent/lineage identity;
- transformation identity;
- transformation parameters;
- coverage and integrity evidence;
- ordering and domain checks;
- gap / segment encoding;
- usage envelope;
- result-to-dataset identity binding;
- reproducibility references;
- market timestamps as encoded dataset fields.
```

Data may state that a field represents UTC epoch milliseconds or that a dataset covers a declared market period.

That is not a statement that the represented information was historically known or usable at a trading decision time.

## 3. Temporal-owned semantics

The following predicates remain exclusively outside DATA-01:

```text
KNOWN_FROM
POINT_IN_TIME_AVAILABILITY
DECISION_TIME_ADMISSIBILITY
VINTAGE_AVAILABILITY
PUBLICATION_DELAY
REVISION_AVAILABILITY
TEMPORAL_DEPENDENCY_LEAKAGE
HISTORICAL_TRADABILITY
RESEARCH_CHOICE_AVAILABILITY
MODEL_OR_PARAMETER_SELECTION_AVAILABILITY
```

DATA-01 may require these predicates from a future Temporal owner. It may not define their truth.

## 4. Current first-use claim

The selected consumer is:

```text
ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1
```

using:

```text
USTECH_PROFILE_MINUTE_CORE_V0_1
```

for a retrospective descriptive claim only.

Therefore the current Temporal applicability state is:

```text
TEMPORAL_STATUS =
NOT_APPLICABLE_WITH_EXPLICIT_BASIS
```

with basis:

```text
The claim describes the observed retrospective dataset.
It does not assert that these observations, classifications,
features, thresholds, vintages, or conclusions were historically
available to a trader at any decision timestamp.
```

This is not a Temporal PASS.

```text
NOT_APPLICABLE != PASS
```

## 5. Expansion firewall

If a future claim adds any of the following:

- predictive validity;
- historical decision validity;
- historical tradability;
- pristine OOS confirmation;
- vintage-sensitive data;
- revision-sensitive economic/event data;
- a feature whose historical availability matters;
- a parameter/model-selection step presented as historically fixed;

then the current Data contract must produce:

```text
TEMPORAL_OWNER_REQUIRED
```

and must not convert its own Data PASS into temporal admissibility.

## 6. Timestamps are not availability proof

For the selected AP0 surface:

```text
minute_start_ms_utc
first_tick_ms
last_tick_ms
```

are market-data timestamps.

They may support ordering, grouping, period coverage, gap detection and source reconstruction.

They do not establish:

```text
known_from <= decision_at
```

or any equivalent historical-availability proposition.

## 7. Latest/revised data firewall

DATA-01 preserves:

```text
LATEST DATA != HISTORICALLY AVAILABLE DATA
```

A later corrected/reconstructed dataset may remain valid as retrospective descriptive evidence while being unsuitable for a historical/PIT claim.

Data must expose the identity/provenance distinction. Temporal must adjudicate historical availability.

## 8. Dependency firewall

A derived dataset cannot become temporally admissible merely because its final row timestamps appear historical.

If a future claim needs historical validity of a transformation dependency chain:

```text
DATA =
provide exact lineage and transformation identities

TEMPORAL =
adjudicate temporal admissibility through dependency closure
```

A missing temporal predicate remains outside Data authority.

## 9. Authority boundary

```text
DATA_AUTHORITY =
CLAIM-SCOPED DATA IDENTITY / ADMISSIBILITY / PROVENANCE ONLY

TEMPORAL_AUTHORITY =
NONE IN DATA-01

SCIENTIFIC_AUTHORITY =
NONE

OPERATIONAL_AUTHORITY =
NONE

TRADING_AUTHORITY =
NONE

RVO_AUTHORITY =
NONE
```

## 10. STOP

This boundary is documentary only.

```text
TEMPORAL IMPLEMENTATION =
NOT AUTHORIZED

DATA RUNTIME MODIFICATION =
NOT AUTHORIZED

REAL EMPIRICAL EXPERIMENT =
NOT AUTHORIZED

OOS CONSUMPTION =
NOT AUTHORIZED
```
