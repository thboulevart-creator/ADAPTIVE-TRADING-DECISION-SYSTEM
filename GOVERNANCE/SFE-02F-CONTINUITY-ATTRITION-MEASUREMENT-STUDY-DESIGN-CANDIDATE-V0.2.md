# SFE-02F — STRUCTURAL CONTINUITY DIAGNOSTIC — DESIGN CANDIDATE V0.2

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Status:** TARGETED AMENDMENT CANDIDATE / EXTERNAL RE-REVIEW REQUIRED  
**Authority:** DOCUMENTARY DESIGN ONLY / NO STUDY EXECUTION

---

## 0. Purpose

V0.2 replaces the inferential intensity-selection design proposed in V0.1.

The new question is deliberately narrower and upstream:

> What is the structural geometry of the exact canonical H1 continuity blocks — their lengths, ending ordinals, boundary mechanisms, and calendar/schedule distribution — and how does that geometry constrain the mechanical availability of a same-block `t+1` after the frozen 20-H1 warmup?

This is a:

```text
CONTINUITY / ADMISSIBILITY GEOMETRY STUDY
```

It is not:

```text
a strategy-performance study
a missing-at-random test
a market-intensity test
a strategy-selection test
a continuity-redesign experiment
```

---

## 1. Amendment provenance

V0.1 candidate:

```text
GOVERNANCE/SFE-02F-CONTINUITY-ATTRITION-MEASUREMENT-STUDY-DESIGN-CANDIDATE-V0.1.md

BLOB =
56a6933a3f9b12228cfabf127669516ea54dc4eb
```

External V0.1 review:

```text
reports/program/2026-10-02-SFE-02F-V0.1-EXTERNAL-ADVERSARIAL-DESIGN-REVIEW.md

BLOB =
3dd7bec203e092c73667cbaf536bed0c1b63456a

VERDICT =
FAIL
```

Review adjudication:

```text
GOVERNANCE/SFE-02F-V0.1-EXTERNAL-REVIEW-ADJUDICATION-2026-10-02.md

STATUS =
N01-N14 ADJUDICATED
AR-01-AR-18 ADJUDICATED
```

V0.2 implements the authorized reduction to a minimal structural diagnostic.

---

## 2. Canonical upstream evidence identities

### 2.1 E1 H1 identity

```text
DATASET =
USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1

CANONICAL STREAM SHA-256 =
15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f

RECORDED JSONL SHA-256 =
94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0

ROWS =
27677

CONTINUITY BLOCKS =
1436

FIRST H1 =
2021-05-25T01:00:00Z

LAST H1 =
2026-05-24T22:00:00Z
```

Binding E1-03 contract:

```text
GOVERNANCE/E1-03-H1-DATASET-IDENTITY-CONTRACT-V0.1.json

BLOB =
c2d4323039d65fcd9319d4f5eb02f45ee27c8afc
```

### 2.2 Source-B discontinuity evidence

```text
reports/data-qualification/source_b_price_core_data_truth_closure_2026-09-25.md

BLOB =
62e9bd1e0892dab7273eed35c8704a9e05611112
```

Persisted facts:

```text
timestamp gaps > 60 s =
1605

series =
DISCONTINUOUS

regular-session boundaries =
1290

in-regular-session gaps before exhaustive holiday overlay =
315

demonstrated historical acquisition losses =
13

historical unknown gaps =
9
```

These classifications are inherited as upstream evidence only.

V0.2 does not infer that every block ending is a provider defect.

### 2.3 AP0 gap/segment semantics

```text
reports/program/2026-09-25-AP0-USTECH-PROFILE-MINUTE-CORE-ADJUDICATION.md

BLOB =
94bba3315e3569993623b8cd2a2bf4264f4ab6f8
```

Persisted AP0 facts include:

```text
gap threshold =
strictly > 60000 ms

gaps > 60 s =
1605

segments =
1606

segment-start rows =
1606
```

---

## 3. Evidence classification

```text
STUDY_CLASS =
STRUCTURAL CONTINUITY / ADMISSIBILITY DIAGNOSTIC

EVIDENCE =
EXPLORATORY / EXPOSED

POST_RESULT_ORIGIN =
YES

PRISTINE_CONFIRMATORY =
FALSE

STRATEGY_CONFIRMATION =
FORBIDDEN
```

SFE-02F V0.2 does not consume:

```text
TD03B
C01 RESERVED EVIDENCE
OTHER PRISTINE CONFIRMATORY SURFACES
```

---

## 4. Strategy-independence invariant

The V0.2 computation must be invariant to removal of all strategy artifacts.

Forbidden inputs include:

```text
BREAKOUT signal
MEAN_REVERSION signal
MOMENTUM signal
strategy Y
strategy theta
strategy CI
strategy event membership
PnL
trade
position
execution
```

The only strategy-related constant permitted is the already-frozen **warmup length 20**, used solely to describe generic structural availability for any same-block H1 kernel requiring 20 prior rows.

No directional state is evaluated.

---

## 5. Canonical H1 row schema

Only these exact fields may be read:

```text
h1_start_ms_utc
source_segment_id
continuity_block_id
continuity_ordinal
mid_close
```

For V0.2 structural geometry:

```text
mid_close =
identity/domain validation only

price-derived statistic =
NONE
```

No return, absolute return, volatility, z-score, range, ATR, or other price transform is computed.

---

## 6. Dataset identity gate

Before any structural output:

1. exact recorded JSONL SHA-256 must match;
2. exact E1 canonical stream SHA-256 must match;
3. row count must equal 27677;
4. continuity-block count must equal 1436;
5. first and last H1 timestamps must match the frozen identity;
6. exact row schema must match;
7. all H1 timestamps must be strictly increasing;
8. all `mid_close` values must remain finite and positive.

Failure:

```text
STUDY =
BLOCKED_DATASET_IDENTITY
```

No partial report is promoted.

---

## 7. Canonical continuity-integrity gate

For every pair of adjacent canonical rows `t, t+1` define:

```text
SOURCE_CHANGE =
source_segment_id(t+1) != source_segment_id(t)

TIME_GAP =
h1_start_ms_utc(t+1)
!=
h1_start_ms_utc(t) + 3600000
```

### 7.1 Expected same-block transition

If:

```text
SOURCE_CHANGE = FALSE
AND
TIME_GAP = FALSE
```

then all must hold:

```text
continuity_block_id(t+1)
=
continuity_block_id(t)

continuity_ordinal(t+1)
=
continuity_ordinal(t) + 1
```

### 7.2 Expected block boundary

If:

```text
SOURCE_CHANGE = TRUE
OR
TIME_GAP = TRUE
```

then all must hold:

```text
continuity_block_id(t+1)
!=
continuity_block_id(t)

continuity_ordinal(t+1)
=
0
```

### 7.3 First row of dataset

Must satisfy:

```text
continuity_ordinal = 0
```

### 7.4 Any inconsistency

Any violation yields:

```text
STUDY =
BLOCKED_CANONICAL_INTEGRITY
```

There is no descriptive `OTHER_CONTRACT_INCONSISTENCY` bucket.

---

## 8. Deterministic boundary mechanism classification

For an internal block boundary between `t` and `t+1`:

```text
SOURCE_CHANGE = TRUE
TIME_GAP = TRUE
→ SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP

SOURCE_CHANGE = TRUE
TIME_GAP = FALSE
→ SOURCE_SEGMENT_CHANGE_ONLY

SOURCE_CHANGE = FALSE
TIME_GAP = TRUE
→ TEMPORAL_GAP_WITHIN_SOURCE_SEGMENT
```

No fourth observational category exists.

The final dataset row is not classified as an internal continuity boundary because the future canonical stream beyond the frozen dataset end is unknown.

It receives:

```text
DATASET_END_TRUNCATION
```

as a separate non-boundary terminal status.

---

## 9. Block definition and length

For each continuity block `b`:

```text
L_b =
number of canonical H1 rows in block b
```

Given a valid block:

```text
first ordinal = 0
last ordinal = L_b - 1
ordinals are contiguous
timestamps are exact +3600000 ms
source_segment_id is constant within block
```

Any violation is already blocked by §7.

---

## 10. Frozen 20-H1 structural availability surface

Both frozen V1 kernels require 20 prior same-block H1 rows.

V0.2 therefore defines, **without computing a strategy signal**:

```text
WARMUP_MATURE_ROW =
continuity_ordinal >= 20
```

For a block of length `L_b`:

```text
N_MATURE_ROWS_b =
max(L_b - 20, 0)

N_MATURE_ROWS_WITH_SAME_BLOCK_T1_b =
max(L_b - 21, 0)
```

For every internal block with:

```text
L_b >= 21
```

exactly one warmup-mature row is the terminal row of that block and therefore lacks a same-block t+1 by construction.

The final dataset block is handled separately because its terminal status is dataset truncation.

This surface quantifies **mechanical opportunity for t+1 measurement**, not strategy-event attrition.

---

## 11. Required structural outputs

Exactly the following families of outputs are proposed.

### 11.1 Dataset/block totals

```text
N_ROWS
N_BLOCKS
N_INTERNAL_BOUNDARIES
N_DATASET_END_TERMINALS
```

### 11.2 Block-length geometry

```text
BLOCK_LENGTH_MIN
BLOCK_LENGTH_MAX
BLOCK_LENGTH_MEDIAN
BLOCK_LENGTH_Q25
BLOCK_LENGTH_Q75

BLOCK_LENGTH_HISTOGRAM_EXACT

N_BLOCKS_LENGTH_1
N_BLOCKS_LENGTH_2_TO_20
N_BLOCKS_LENGTH_21
N_BLOCKS_LENGTH_GE_22

FRACTION_BLOCKS_LENGTH_LE_20
FRACTION_BLOCKS_LENGTH_GE_21
```

No inferential confidence interval is attached.

### 11.3 Ending ordinal geometry

For internal continuity boundaries only:

```text
BLOCK_END_ORDINAL_HISTOGRAM_EXACT
BLOCK_END_ORDINAL_MIN
BLOCK_END_ORDINAL_MAX
BLOCK_END_ORDINAL_MEDIAN
```

### 11.4 Warmup/t+1 mechanical availability

```text
N_WARMUP_MATURE_ROWS
N_WARMUP_MATURE_ROWS_WITH_SAME_BLOCK_T1
N_WARMUP_MATURE_INTERNAL_BLOCK_END_ROWS
N_WARMUP_MATURE_DATASET_END_ROWS

FRACTION_WARMUP_MATURE_WITH_SAME_BLOCK_T1
FRACTION_WARMUP_MATURE_AT_INTERNAL_BLOCK_END
```

These values concern all structurally mature rows.

They do not use strategy event membership.

### 11.5 Boundary mechanism counts

```text
N_SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP
N_SOURCE_SEGMENT_CHANGE_ONLY
N_TEMPORAL_GAP_WITHIN_SOURCE_SEGMENT
```

### 11.6 Calendar/schedule geometry

For each internal boundary, define the **expected next-H1 boundary instant**:

```text
B_t =
h1_start_ms_utc(t) + 3600000
```

Report boundary counts by:

```text
UTC_WEEKDAY
UTC_HOUR
UTC_WEEKDAY_X_HOUR
UTC_CALENDAR_MONTH
UTC_CALENDAR_YEAR
```

No calendar bucket is excluded.

---

## 12. DST annotation

To expose rather than condition away a predictable calendar mechanism, V0.2 proposes descriptive annotation of each internal boundary instant `B_t` with:

```text
IANA timezone =
America/New_York

NY_UTC_OFFSET
NY_DST_STATE
NY_LOCAL_WEEKDAY
NY_LOCAL_HOUR
```

Requirements before any execution:

```text
exact IANA TZDB release identity =
MUST_BE_FROZEN

runtime/library identity =
MUST_BE_FROZEN
```

No exchange-session, holiday, or early-close semantic label is inferred from DST alone.

No holiday or early-close rows are excluded.

If a future design requires an exchange/provider holiday calendar, it must bind a separate authoritative source before execution.

---

## 13. Structural source-calendar cross-tabs

Mandatory descriptive cross-tabs:

```text
BOUNDARY_COUNT
by UTC_WEEKDAY_X_HOUR

BOUNDARY_COUNT
by NY_DST_STATE × UTC_WEEKDAY_X_HOUR

BOUNDARY_COUNT
by NY_UTC_OFFSET × UTC_WEEKDAY_X_HOUR

BOUNDARY_REASON
× UTC_WEEKDAY_X_HOUR

BOUNDARY_REASON
× NY_DST_STATE
```

These are counts only.

No AUC, test statistic, p-value, confidence interval, weighting or equivalence rule is applied.

---

## 14. Upstream Source-B classifications

Where an exact upstream Source-B classification is already persisted and resolvably binds to a gap, V0.2 may report it descriptively.

It must not invent missing classifications.

Allowed inherited labels are limited to exact upstream evidence such as:

```text
REGULAR_SESSION_BOUNDARY
IN_REGULAR_SESSION_PRE_HOLIDAY_OVERLAY
DEMONSTRATED_HISTORICAL_ACQUISITION_LOSS
HISTORICAL_UNKNOWN_GAP
```

If an exact row/boundary cannot be deterministically bound to such an upstream classification:

```text
UPSTREAM_CLASSIFICATION =
UNRESOLVED
```

No provider-failure inference is permitted from `UNRESOLVED`.

If the existing upstream artifacts are insufficient for deterministic row-level binding, the study must report aggregate upstream facts separately rather than fabricate a join.

---

## 15. No inferential or causal decision rule

V0.2 has no:

```text
AUC
Mann-Whitney statistic
bootstrap
RNG
confidence interval
p-value
equivalence band
materiality threshold
SUPPORTED / REFUTED verdict
ESTABLISHED claim
NO_MATERIAL claim
MAR claim
```

The only successful result status is:

```text
STRUCTURAL_PROFILE_PRODUCED_ON_EXPOSED_SURFACE
```

This means only that the preregistered structural counts were reproduced from the exact canonical dataset.

---

## 16. Permitted interpretation

The report may state descriptive facts such as:

```text
a specified fraction of blocks have length <= 20

a specified fraction of warmup-mature rows retain same-block t+1

a specified fraction of internal boundaries occur at particular
calendar/schedule states

specified boundary mechanisms dominate the structural profile
```

It may also state deterministic implications of block geometry, for example:

```text
for a same-block kernel requiring 20 prior rows,
a block of length <=20 contains zero mature rows

a block of length 21 contains one mature row,
which is also the terminal row and has no same-block t+1

a block of length L>=22 contains L-20 mature rows,
of which L-21 have a same-block t+1
```

These are structural identities.

---

## 17. Forbidden interpretation

V0.2 may not conclude:

```text
continuity caused SFE-02D non-decision

continuity biased strategy Y

excluded strategy events would have won or lost

t+1-admissible rows are neutral

missingness is MAR

the H1 construction is defective

the provider feed is defective

continuity rules should be relaxed

a different data construction would improve V1

V1 should be reconfirmed on redesigned 2021-2026 data
```

H-E01 and H-E08 remain post-result hypotheses.

V0.2 characterizes a structural mechanism relevant to them; it does not confirm or falsify them.

---

## 18. Measurement-rescue firewall

Binding rule:

> Any continuity, segmentation, admissibility, aggregation, warmup, or data-construction rule motivated by SFE-02F and then applied to the already-exposed SFE-02D historical surface produces EXPOSED evidence only.

Such evidence:

```text
MAY =
support further hypothesis generation

MAY NOT =
reconfirm
requalify
or promote
BREAKOUT_V1
MEAN_REVERSION_V1
on the same exposed 2021-2026 surface
```

A confirmatory claim requires separately governed non-exposed evidence.

---

## 19. Redesign-after-result firewall

After any future SFE-02F V0.2 execution, changing any of the following creates a new explicitly exposed study version:

```text
block definition
boundary definition
mechanism categories
warmup threshold used for structural reporting
calendar annotation
DST annotation
output family
aggregation rule
dataset identity
continuity identity
```

No silent V0.2 rewrite is permitted.

---

## 20. Stop condition

A future authorized V0.2 execution has exactly two terminal classes:

### Success

```text
STRUCTURAL_PROFILE_PRODUCED_ON_EXPOSED_SURFACE
→ persist report
→ STOP
→ HUMAN ADJUDICATION OR DEFER
```

### Integrity failure

```text
BLOCKED_DATASET_IDENTITY
or
BLOCKED_CANONICAL_INTEGRITY
or
BLOCKED_CALENDAR_IDENTITY
→ persist blocker evidence
→ STOP
```

No outcome automatically opens:

```text
SFE-02G
continuity redesign
strategy replication
strategy revision
new response horizon
new backtest
```

---

## 21. Explicit V0.1 removals

The following V0.1 surfaces are removed, not amended:

```text
X_t
A_t inferential comparison
AUC_cond
pairwise weighting
schedule comparability gates
ISO-week bootstrap
10000 replicates
PCG64
seed
95% bootstrap CI
[0.45,0.55] band
OBSERVABLE_HIGHER_INTENSITY_SELECTION
OBSERVABLE_LOWER_INTENSITY_SELECTION
NO_MATERIAL_INTENSITY_SELECTION_DETECTED
NON_DECISIVE statistical branch
```

Therefore V0.2 does not inherit the statistical defects associated with those surfaces.

---

## 22. External re-review questions

The V0.2 external reviewer must answer at minimum:

```text
R2-01
Does V0.2 fully remove strategy-conditioned inputs and performance semantics?

R2-02
Are dataset and continuity-integrity gates exact and fail-closed?

R2-03
Are boundary mechanism predicates exhaustive for valid E1-03 transitions?

R2-04
Is DATASET_END_TRUNCATION correctly separated from internal continuity boundaries?

R2-05
Are the block-length and ordinal identities mathematically exact?

R2-06
Is ordinal >=20 used only as a structural warmup surface,
not as a strategy-result filter?

R2-07
Does the proposed structural t+1 availability metric avoid using strategy events?

R2-08
Are calendar/DST annotations descriptive rather than confounding adjustments?

R2-09
Is America/New_York annotation acceptable if the exact IANA TZDB identity
is frozen before execution?

R2-10
Is the absence of holiday exclusions scientifically safer than using
an unbound holiday calendar in this descriptive diagnostic?

R2-11
Are Source-B upstream classifications used only where deterministic binding exists?

R2-12
Does V0.2 avoid treating inactivity/schedule closure as provider failure?

R2-13
Does V0.2 fully close N01-N14 from V0.1,
either by correction or by removal of the affected surface?

R2-14
Does the measurement-rescue firewall prevent confirmatory reuse
of redesigned data on the exposed SFE-02D period?

R2-15
Does the redesign-after-result firewall prevent silent structural tuning?

R2-16
Are the permitted interpretation claims narrow enough?

R2-17
Is any inferential statistic actually necessary before this structural diagnostic?

R2-18
Is V0.2 ready for human adjudication as a design,
while study execution remains separately unauthorized?
```

---

## 23. Candidate state

```text
SFE_02F_V0_1 =
SUPERSEDED_AS_DESIGN_CANDIDATE

SFE_02F_V0_2 =
TARGETED_AMENDMENT_CANDIDATE

AUC =
REMOVED

BOOTSTRAP =
REMOVED

EQUIVALENCE_BAND =
REMOVED

STRATEGY_SIGNALS =
FORBIDDEN

Y =
FORBIDDEN

PNL =
FORBIDDEN

RAW_H1_EXECUTION =
NOT_AUTHORIZED

STUDY_EXECUTION =
NOT_AUTHORIZED

NEXT =
EXTERNAL V0.2 ADVERSARIAL RE-REVIEW

STOP =
TRUE
```
