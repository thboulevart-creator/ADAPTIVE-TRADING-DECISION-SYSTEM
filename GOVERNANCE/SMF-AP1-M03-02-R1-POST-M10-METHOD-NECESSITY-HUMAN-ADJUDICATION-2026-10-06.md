# SMF-AP1-M03-02-R1 — POST-M10 METHOD NECESSITY — HUMAN ADJUDICATION — 2026-10-06

HUMAN_DECISION = ADOPT

POST_M10_METHOD_NECESSITY_ANALYSIS = HUMAN_ADOPTED
ANALYSIS_MODE = READ_ONLY
STATUS = HUMAN_ADOPTED / BINDING / CLOSED

## Adopted analysis identity

```text
FRESH_CANONICAL_HEAD =
d40124f450548b6f8d8ff1da90d43f5d4a1059e3

FRESH_CANONICAL_TREE =
8421d6bf821751bcf23add349547cd213b5700fa

DRIFT_SINCE_M10_01 =
NON_MATERIAL_TO_M10_SCIENTIFIC_SEMANTICS
```

Persistence occurs from a later fresh parent after a separately verified non-material drift:

```text
PERSISTENCE_PARENT_HEAD =
fb0d3e3aa7bc37684d499d7ba653f79cb3e6d810

PERSISTENCE_PARENT_TREE =
ec0a9994baeff21c49b21a4e24c35e850816bea5

PERSISTENCE_PARENT_DRIFT =
AO-E0-B12-DATA-01-SR-01 + BEPD-07B ONLY

PERSISTENCE_PARENT_DRIFT_CLASSIFICATION =
NON_MATERIAL_TO_POST_M10_ADJUDICATION
```

## Immediate method decision

```text
IMMEDIATE_ADDITIONAL_STATISTICAL_METHOD =
NONE

M04 =
NOT_REQUIRED_YET

M05 =
NOT_ADMISSIBLE_AS_GLOBAL_2022_2025_RESAMPLING_YET

M08 =
NOT_REQUIRED_ABSENT_SELECTION_ATTRITION_FAILURE_MODE

M09 =
NOT_REQUIRED_UNTIL_PRISTINE_CONFIRMATION_IS_REQUESTED

M11 =
NOT_REQUIRED_ABSENT_INFERENTIAL_MULTIPLICITY_OR_SEARCH_PROMOTION
```

No statistical method is automatically activated by this decision.

## Minimum required control

```text
MINIMUM_REQUIRED_NEXT_CONTROL =
POST_M10_TEMPORAL_POOLING_AND_CONDITIONING_GATE
```

For the eight M10-01 claim units carrying:

```text
MATERIAL_TEMPORAL_VARIATION
```

the binding rule is:

```text
UNCONDITIONAL_POOLING_ACROSS_2022_2025 =
NOT_ALLOWED_BY_DEFAULT
```

Any later scientific analysis operating on one of those claim units must satisfy at least one route:

```text
A =
EXPLICITLY_JUSTIFY_TEMPORAL_POOLING

OR

B =
CONDITION_OR_STRATIFY_BY_TIME

OR

C =
PREREGISTER_A_METHOD_EXPLICITLY_ROBUST_TO_THE_OBSERVED_TEMPORAL_VARIATION
```

Otherwise:

```text
DOWNSTREAM_ANALYSIS_STATUS =
BLOCKED
```

## Non-material M10 claim units

For:

```text
spread_mean p90
spread_mean p95
spread_mean p99
```

the exact status remains:

```text
NO_MATERIAL_TEMPORAL_VARIATION_DETECTED
```

It must not be promoted to:

```text
STABILITY_PROVEN
STATIONARITY_PROVEN
UNCONDITIONAL_POOLING_VALIDATED
```

## Scientific boundaries

The following remain not established:

```text
FORMAL_NONSTATIONARITY =
NOT_ESTABLISHED

CHANGE_POINT =
NOT_ESTABLISHED

STRUCTURAL_BREAK =
NOT_ESTABLISHED

REGIME_CAUSATION =
NOT_ESTABLISHED
```

The existing historical corpus is at minimum:

```text
EVIDENCE_STATE =
EXPOSED
```

Any new hypothesis or estimand created in response to M10-01 cannot obtain confirmatory pristine status on the same exposed corpus:

```text
SAME_CORPUS_CONFIRMATORY_STATUS =
CONTAMINATED / NON_PRISTINE
```

Reset to `PRISTINE` is forbidden.

## M05 consequence

```text
GLOBAL_M05_RESAMPLING_ACROSS_2022_2025 =
BLOCKED_PENDING_TEMPORAL_JUSTIFICATION
```

M04 may be reconsidered only when a later claim needs dependence-sensitive inference or prepares an M05 resampling design.

M08 may be reconsidered only when a material inclusion, exclusion, or temporally asymmetric attrition failure mode is established.

M09 becomes necessary when a genuinely pristine prospective confirmation is requested.

M11 becomes necessary when a later inferential claim materially depends on a search universe or multiplicity.

## Final human decision

```text
POST_M10_METHOD_NECESSITY =
RESOLVED

NEW_STATISTICAL_METHOD =
NONE

TEMPORAL_POOLING_GATE =
REQUIRED

M04 =
CLOSED

M05 =
CLOSED

M08 =
CLOSED

M09 =
CLOSED

M11 =
CLOSED

TRADING_AUTHORITY =
FALSE

CAPITAL_AUTHORITY =
FALSE

NEXT_FRONTIER =
POST_M10_TEMPORAL_POOLING_AND_CONDITIONING_GATE
DESIGN / FREEZE ONLY

AUTOMATIC_EXECUTION =
FORBIDDEN
```

The next frontier, if separately authorized, is limited to materializing and qualifying the pooling/conditioning governance rule.

It must not:
- execute a new statistical method;
- reread real data;
- produce a new market result;
- consume OOS evidence;
- create trading authority;
- create capital authority.

STOP.
