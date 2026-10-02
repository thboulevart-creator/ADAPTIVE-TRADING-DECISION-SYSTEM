# SFE-02F V0.1 — EXTERNAL REVIEW ADJUDICATION

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Authority:** HUMAN-AUTHORIZED TARGETED AMENDMENT ONLY  
**Execution authority:** NONE

---

## 1. Reviewed object and evidence

Reviewed candidate:

```text
GOVERNANCE/SFE-02F-CONTINUITY-ATTRITION-MEASUREMENT-STUDY-DESIGN-CANDIDATE-V0.1.md

BLOB =
56a6933a3f9b12228cfabf127669516ea54dc4eb
```

External review evidence:

```text
reports/program/2026-10-02-SFE-02F-V0.1-EXTERNAL-ADVERSARIAL-DESIGN-REVIEW.md

BLOB =
3dd7bec203e092c73667cbaf536bed0c1b63456a

MODEL =
Claude Opus 5.5

OVERALL VERDICT =
FAIL
```

The review verified the exact candidate blob and did not inspect H1 data or calculate SFE-02F, strategy Y, PnL, or backtest results.

---

## 2. Human-authorized amendment direction

The authorized response to the review is not to patch the V0.1 AUC design into a larger inferential study.

The authorized direction is:

```text
SFE-02F V0.2 =
TARGETED STRUCTURAL CONTINUITY DIAGNOSTIC

PURPOSE =
characterize the geometry and mechanism of canonical H1 continuity
before deciding whether any intensity-selection test is necessary
```

V0.2 must therefore remove or defer:

```text
X_t decision statistic
AUC_cond
pair weighting
comparability inference gates
ISO-week bootstrap
confidence interval
[0.45,0.55] band
binary materiality labels
H-E01/H-E08 falsification claims
```

No execution is authorized by this adjudication.

---

## 3. Finding adjudication — N01 → N14

### N01 — calendar / DST confounding

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
REMOVE inferential UTC-hour conditioning.
Retain calendar/schedule geometry only as descriptive structure.

Required schedule annotations:
- UTC weekday/hour from canonical timestamp;
- America/New_York UTC offset / DST-state annotation,
  using an explicitly frozen IANA TZDB identity before execution.

No holiday or early-close exclusion may be introduced without
a separately bound authoritative calendar source.
```

Because V0.2 has no AUC comparison, DST state is used to expose structure, not to rescue an estimand.

### N02 — pair weighting / undefined target population

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
AUC_cond and pair weighting REMOVED.
No weighted cross-class estimand remains.
```

### N03 — estimand/question mismatch

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
Question narrowed to structural geometry only.

V0.2 does NOT ask whether the t+1-admissible sample is neutral.
It asks how continuity blocks and their endings are mechanically
distributed relative to ordinals and calendar/schedule state.

Marginal neutrality and strategy-eligible outcome neutrality =
OUT_OF_SCOPE.
```

### N04 — exposed-surface confirmation / overclaim

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
No ESTABLISHED or confirmatory label.
Outputs are descriptive observations on an EXPOSED surface.

H-E01 and H-E08 are not claimed falsified or confirmed.
```

### N05 — unjustified equivalence band

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
[0.45,0.55] band REMOVED.
No materiality threshold remains.
```

### N06 — rescue through measurement redesign

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
Binding firewall added:

Any continuity/admissibility rule motivated by SFE-02F and then
applied to the already-exposed SFE-02D historical surface creates
EXPOSED evidence only.

It may not be used to reclassify or reconfirm V1 on that same
2021-2026 surface.

Any confirmatory use requires separately governed non-exposed evidence.
```

### N07 — continuity label is not synonymous with data quality

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
Study class renamed:
CONTINUITY / ADMISSIBILITY GEOMETRY STUDY.

A block ending may reflect:
- regular schedule closure;
- actual market inactivity;
- acquisition interruption;
- unresolved source discontinuity.

V0.2 does not classify a block end as provider defect unless an
authoritative upstream artifact already supports that classification.
```

Upstream Source-B data truth is explicitly bound:

```text
reports/data-qualification/source_b_price_core_data_truth_closure_2026-09-25.md
BLOB =
62e9bd1e0892dab7273eed35c8704a9e05611112

known:
1605 gaps > 60 s
1290 regular-session boundaries
315 in regular session before exhaustive holiday overlay
13 demonstrated historical acquisition losses
9 historical unknown gaps
series declared DISCONTINUOUS
```

### N08 — study eligibility can omit single-row blocks

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
No prior-return requirement exists in V0.2.

All canonical continuity blocks, including length-1 blocks,
are part of the structural population.

Mandatory:
N_BLOCKS_LENGTH_1
N_BLOCKS_LENGTH_LE_20
N_BLOCKS_LENGTH_GE_21

No end is hidden because X_t is no longer required.
```

### N09 — mechanism predicates / integrity inconsistency

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
Reason predicates are deterministic and integrity-first.

For adjacent canonical H1 rows t and t+1:

source_change =
source_segment_id(t+1) != source_segment_id(t)

time_gap =
h1_start_ms_utc(t+1) != h1_start_ms_utc(t) + 3600000

Expected same block:
source_change = false
AND time_gap = false
AND continuity_block_id unchanged
AND continuity_ordinal increments exactly +1

Expected boundary:
continuity_block_id changes
AND continuity_ordinal(t+1) = 0
AND (source_change OR time_gap)

Boundary class:
source_change && time_gap
→ SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP

source_change && !time_gap
→ SOURCE_SEGMENT_CHANGE_ONLY

!source_change && time_gap
→ TEMPORAL_GAP_WITHIN_SOURCE_SEGMENT

Any state inconsistent with E1-03 =
BLOCKED_CANONICAL_INTEGRITY

No OTHER descriptive bucket.
```

### N10 — bootstrap dependence ambiguity

```text
ADJUDICATION =
CLOSED_BY_REMOVAL

V0.2 RESOLUTION =
No bootstrap.
No resampling.
No inferential interval.
```

### N11 — bootstrap reproducibility

```text
ADJUDICATION =
CLOSED_BY_REMOVAL

V0.2 RESOLUTION =
No RNG, percentile algorithm, or bootstrap library is required.
```

### N12 — redesign after result

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
Any design change after observing SFE-02F structural outputs is a new,
explicitly EXPOSED study version.

The same structural output may not silently justify changing:
- continuity rules;
- warmup;
- admissibility;
- strategy parameters;
- response horizon;
- evidence classification.
```

### N13 — missing stopping condition

```text
ADJUDICATION =
ACCEPT

V0.2 RESOLUTION =
SFE-02F V0.2 ends after one structural diagnostic artifact.

Outcomes do not automatically open:
- another SFE study;
- a continuity redesign;
- replication;
- strategy revision.

NEXT =
HUMAN ADJUDICATION OR DEFER

STOP =
TRUE
```

### N14 — AUC cannot detect bilateral selection

```text
ADJUDICATION =
CLOSED_BY_REMOVAL

V0.2 RESOLUTION =
AUC removed.
No claim of stochastic-ordering neutrality or general selection neutrality.
```

---

## 4. AR-01 → AR-18 adjudication

```text
AR-01  CLOSED
        Strategy-independence preserved and strengthened.

AR-02  CLOSED_WITH_SCOPE_CORRECTION
        Continuity is treated as an admissibility/mechanism label,
        not a pure pipeline-failure label.

AR-03  CLOSED
        Final-row truncation handling remains explicit.

AR-04  NOT_APPLICABLE_V0_2
        X_t removed.

AR-05  CLOSED_BY_REDUCTION
        No inferential UTC-hour conditioning remains.
        DST/calendar state becomes descriptive structure.

AR-06  CLOSED_BY_REDUCTION
        No conditioned causal/inferential claim remains.

AR-07  CLOSED_BY_REMOVAL
        AUC estimand removed.

AR-08  CLOSED_BY_REMOVAL
        Pair weighting removed.

AR-09  CLOSED_BY_REMOVAL
        Inferential comparability gates removed.
        Only canonical-integrity gates remain.

AR-10  CLOSED_BY_REMOVAL
        Bootstrap removed.

AR-11  CLOSED_BY_REMOVAL
        Bootstrap reproducibility surface removed.

AR-12  CLOSED_BY_REMOVAL
        Equivalence band removed.

AR-13  CLOSED_BY_REMOVAL
        No binary materiality claim.

AR-14  CLOSED_WITH_EXPLICIT_PREDICATES
        Boundary categories frozen; inconsistent states block.

AR-15  CLOSED_WITH_SCOPE_CORRECTION
        Mechanical coupling between source segmentation and inactivity
        is treated as a property to describe, not a provider-defect discovery.

AR-16  CLOSED_WITH_EXPOSURE_FIREWALL
        Measurement-driven redesign cannot reconfirm V1 on exposed data.

AR-17  CLOSED_BY_CLAIM_REDUCTION
        H-E01/H-E08 are not claimed falsified or confirmed by V0.2.

AR-18  TARGETED_CORRECTION_APPLIED_IN_V0_2_CANDIDATE
```

---

## 5. V0.2 scientific question

The amended question is:

> What is the structural geometry of the canonical H1 continuity blocks — their lengths, ending ordinals, boundary mechanisms, and calendar/schedule distribution — and how does that geometry constrain the availability of a same-block t+1 after the frozen 20-H1 warmup?

This is a measurement-geometry question.

It is not a strategy-performance question.

---

## 6. Allowed V0.2 descriptive outputs

V0.2 may define, but not yet execute, deterministic reporting of:

```text
N_ROWS
N_BLOCKS
BLOCK_LENGTH_MIN
BLOCK_LENGTH_MAX
BLOCK_LENGTH_MEDIAN
BLOCK_LENGTH_QUANTILES

N_BLOCKS_LENGTH_1
N_BLOCKS_LENGTH_LE_20
N_BLOCKS_LENGTH_GE_21

BLOCK_END_ORDINAL_COUNTS
BLOCK_END_ORDINAL_FRACTIONS

N_ROWS_ORDINAL_GE_20
N_ROWS_ORDINAL_GE_20_WITH_SAME_BLOCK_T1
N_ROWS_ORDINAL_GE_20_WITHOUT_SAME_BLOCK_T1
FRACTION_ORDINAL_GE_20_WITH_SAME_BLOCK_T1

BOUNDARY_REASON_COUNTS

BOUNDARY_COUNTS_BY_UTC_WEEKDAY_HOUR
BOUNDARY_COUNTS_BY_AMERICA_NEW_YORK_UTC_OFFSET
BOUNDARY_COUNTS_BY_AMERICA_NEW_YORK_DST_STATE
BOUNDARY_COUNTS_BY_CALENDAR_YEAR
BOUNDARY_COUNTS_BY_CALENDAR_MONTH
```

The `ordinal >= 20` surface is a **mechanical availability surface only** because both frozen V1 kernels require 20 prior same-block H1 rows.

No strategy signal is evaluated.

---

## 7. Explicitly removed from V0.2

```text
X_t
A_t inferential comparison
AUC_cond
Mann-Whitney interpretation
pair weights
minimum comparable-stratum gates
bootstrap
RNG
confidence interval
equivalence band
materiality labels
selection-neutrality claim
MAR claim
strategy replication recommendation
```

---

## 8. Authority boundary

This adjudication and the forthcoming V0.2 candidate do not authorize:

```text
RAW H1 EXECUTION
STRUCTURAL OUTPUT CALCULATION
STRATEGY SIGNALS
BEHAVIORAL Y
THETA
PNL
BACKTEST
OPTIMIZATION
STRATEGY CHANGE
CONTINUITY CHANGE
ADMISSIBILITY CHANGE
RESPONSE-HORIZON CHANGE
TD03B CONSUMPTION
C01 CONSUMPTION
```

---

## 9. Adjudication state

```text
V0_1_EXTERNAL_REVIEW =
PERSISTED

V0_1_EXTERNAL_VERDICT =
FAIL

N01_TO_N14 =
ADJUDICATED

AR01_TO_AR18 =
ADJUDICATED

TARGETED_DIRECTION =
STRUCTURAL_CONTINUITY_DIAGNOSTIC

V0_2_EXECUTION =
NOT_AUTHORIZED

NEXT =
PRODUCE V0.2 CANDIDATE
+
EXTERNAL V0.2 RE-REVIEW PACKAGE

STOP_AFTER_PACKAGE =
TRUE
```
