# SFE-02F — CONTINUITY ATTRITION MEASUREMENT STUDY — DESIGN CANDIDATE V0.1

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Status:** PRE-DRAFT CANDIDATE / EXTERNAL ADVERSARIAL DESIGN REVIEW REQUIRED  
**Authority:** DOCUMENTARY DESIGN ONLY / NO STUDY EXECUTION

---

## 0. Purpose

SFE-02D produced non-decisive behavioral evidence for both frozen V1 strategy families.

SFE-02E then identified a measurement question that is upstream of strategy modification:

> Are continuity endings associated with observable pre-boundary market-state intensity such that rows with an admissible `t+1` cannot be assumed to be a behaviorally neutral subsample of the canonical H1 surface?

SFE-02F V0.1 defines a **strategy-independent continuity measurement study** to answer that question without:

- using BREAKOUT_V1 or MEAN_REVERSION_V1 signals;
- recomputing strategy `Y`;
- using PnL;
- changing either strategy;
- searching response horizons;
- searching parameters;
- optimizing any trading rule.

This candidate is not yet adopted and does not authorize execution.

---

## 1. Canonical provenance

### 1.1 SFE-02E diagnostic source

```text
GOVERNANCE/SFE-02E-NON-DECISIVE-RESULT-DIAGNOSTIC-CONTRACT-V0.1.json
BLOB =
eda45af67ec9c708b9c24871eb339ea123035a56

reports/program/2026-10-02-SFE-02E-NON-DECISIVE-RESULT-DIAGNOSTIC-AND-HYPOTHESIS-MAP.md
BLOB =
f40a2f5746fb70557167d8170cc802fdc25c7607
```

Relevant post-result hypotheses:

```text
H-E01 — continuity attrition may materially affect evidentiary resolution

H-E08 — continuity exclusions may interact with observable market-state intensity
```

Both are:

```text
POST_RESULT_EXPOSED
HYPOTHESIS_GENERATING
NOT_CONFIRMATORY
```

### 1.2 SFE-02D result source

```text
SFE-02D FINAL CLOSURE BLOB =
4365bef87dd9dd4613261aeba70dffe2e8ba4500
```

Persisted diagnostic motivating this study:

```text
BREAKOUT excluded directional events =
391 / 688
≈ 56.8%

MEAN REVERSION excluded directional events =
804 / 1416
≈ 56.8%

all exclusions =
END_OF_CONTINUITY_BLOCK
```

Persisted prior-movement diagnostic:

```text
BREAKOUT
median prior abs H1 return:
included = 0.0022926043866677848
excluded = 0.002584055401291252

MEAN REVERSION
median prior abs H1 return:
included = 0.0016091355635006188
excluded = 0.0017347183911985975
```

These strategy-conditioned diagnostics motivate the measurement question.

They are **not** reused as SFE-02F outcome data or decision statistics.

### 1.3 G6 semantic provenance

```text
G6 HUMAN ADJUDICATION BLOB =
93e3c87f24b8933fbdfe25b1806d42233b6ec328
```

G6 is adopted for semantic design only.

No G6 registry implementation is authorized.

Conceptually, SFE-02F is:

```text
INFORMED_BY
SFE-02E

PREREGISTERED_BY
future SFE-02F adopted contract
```

This document does not create or implement registry events.

---

## 2. Epistemic classification

```text
STUDY_CLASS =
MEASUREMENT / DATA-QUALITY / SELECTION-MECHANISM STUDY

STRATEGY_PERFORMANCE_STUDY =
NO

POST_RESULT_ORIGIN =
YES

HYPOTHESIS_EXPOSURE =
POST_RESULT_EXPOSED

CONFIRMATORY_STRATEGY_EVIDENCE =
NO

TRADING_EDGE_CLAIM =
FORBIDDEN
```

SFE-02F can establish properties of the continuity/admissibility mechanism.

It cannot establish whether either trading strategy works.

---

## 3. Exact evidence surface proposed

Candidate evidence source:

```text
USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1

canonical H1 stream SHA-256 =
15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f

recorded local H1 JSONL SHA-256 =
94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0

rows =
27677

continuity blocks =
1436

first H1 =
2021-05-25T01:00:00Z

last H1 =
2026-05-24T22:00:00Z
```

This evidence is already exposed.

Therefore:

```text
SFE_02F_EVIDENCE =
EXPLORATORY / EXPOSED

PRISTINE_CONFIRMATORY =
FALSE
```

SFE-02F does not consume TD03B or C01 reserved evidence.

---

## 4. Strategy-independence invariant

No strategy state may be used to define:

- the population;
- the attrition label;
- the predictor;
- the schedule stratum;
- the primary statistic;
- eligibility;
- inclusion/exclusion;
- inference blocks;
- interpretation.

Specifically forbidden inputs:

```text
BREAKOUT signal
MEAN_REVERSION signal
MOMENTUM signal
strategy Y
strategy theta
strategy CI
PnL
position
execution
trade outcome
```

The measurement study must produce the same result if every strategy artifact is removed from the runtime environment.

---

## 5. Unit of analysis

The unit is an H1 row `t` from the exact canonical H1 stream.

A row is **primary-analysis eligible** only if an immediately preceding H1 exists satisfying all of:

```text
same continuity_block_id
continuity_ordinal(t-1) = continuity_ordinal(t) - 1
h1_start(t) = h1_start(t-1) + 3600000 ms
finite positive C_(t-1)
finite positive C_t
```

Reason:

The primary pre-boundary observable requires one already-observed prior H1 transition.

The final dataset row is excluded from the primary attrition-label study because its missing next row is caused by dataset truncation and not an observed internal continuity break.

---

## 6. Attrition label

For each primary-analysis eligible row `t` that is not the final dataset row:

### 6.1 CONTINUES

```text
A_t = 0
```

if the next canonical H1 row satisfies:

```text
same continuity_block_id
continuity_ordinal(t+1) = continuity_ordinal(t) + 1
h1_start(t+1) = h1_start(t) + 3600000 ms
```

### 6.2 CONTINUITY_END

```text
A_t = 1
```

if a later canonical row exists but the immediately following canonical row fails one or more of those same-block +1-hour conditions.

No future return is used.

The next row is inspected only to classify **data continuity**, not market outcome.

---

## 7. Continuity-end mechanism categories

Every `A_t = 1` row must additionally receive exactly one descriptive reason:

```text
SOURCE_SEGMENT_CHANGE
TEMPORAL_GAP_WITHIN_SOURCE_SEGMENT
SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP
OTHER_CONTRACT_INCONSISTENCY
```

Definitions compare row `t` and the next canonical H1 row using:

- `source_segment_id`;
- `h1_start_ms_utc`;
- `continuity_block_id`;
- `continuity_ordinal`.

These categories are descriptive.

They do not change the primary decision rule.

---

## 8. Primary pre-boundary observable

The sole candidate **decision-bearing market-state variable** is:

```text
X_t =
abs(C_t / C_(t-1) - 1)
```

where both H1 rows are already observed by time `t`.

Interpretation:

```text
X_t =
absolute immediately-prior H1 price movement
available at the continuity boundary
```

No future price is used.

No rolling volatility filter, ATR, strategy state, z-score, breakout state or alternative movement horizon is decision-bearing in V0.1.

This restriction is deliberate to prevent post-result feature proliferation.

---

## 9. Calendar/schedule confounding

Continuity endings may be structurally concentrated at particular market-calendar times.

Therefore a raw comparison:

```text
X | A=1
vs
X | A=0
```

is not sufficient.

Candidate schedule stratum:

```text
S_t =
UTC weekday × UTC hour
```

yielding at most 168 fixed hour-of-week strata.

The primary intensity comparison must be **within the same S_t stratum**.

No local timezone, daylight-saving transformation or market-session label is used in the primary statistic.

UTC is inherited from the canonical H1 construction.

---

## 10. Primary question

> Conditional on the same UTC hour-of-week, is pre-boundary absolute H1 movement intensity systematically different for rows that terminate a continuity block versus rows that retain an admissible same-block t+1?

This asks about observable selection.

It does not ask whether any strategy would have won on excluded events.

---

## 11. Candidate primary effect statistic

### 11.1 Stratified pairwise AUC

For each comparable schedule stratum `s` containing both:

```text
at least one A=1 row
and
at least one A=0 row
```

compare all cross-class pairs:

```text
(X_end, X_continue)
```

Pair score:

```text
1.0 if X_end > X_continue
0.5 if X_end = X_continue
0.0 if X_end < X_continue
```

The candidate primary statistic is the pooled within-stratum pairwise probability:

```text
AUC_cond =
sum(pair scores across comparable strata)
/
number of within-stratum cross-class pairs
```

Interpretation:

```text
AUC_cond = 0.5
→ no directional intensity separation

AUC_cond > 0.5
→ continuity ends tend to follow higher X

AUC_cond < 0.5
→ continuity ends tend to follow lower X
```

This statistic is scale-free and conditions comparisons on identical UTC hour-of-week.

---

## 12. Comparability / coverage gate

A conditional statistic can hide non-comparable schedule strata.

Therefore the following must be reported before interpretation:

```text
N_END_TOTAL
N_CONTINUE_TOTAL
N_COMPARABLE_END
N_COMPARABLE_CONTINUE
N_COMPARABLE_STRATA
FRACTION_END_COVERED_BY_COMPARABLE_STRATA
```

Candidate minimum gates:

```text
N_COMPARABLE_END >= 100

N_COMPARABLE_CONTINUE >= 100

N_COMPARABLE_STRATA >= 10

FRACTION_END_COVERED_BY_COMPARABLE_STRATA >= 0.50
```

If any gate fails:

```text
PRIMARY STATUS =
NOT_INTERPRETABLE /
SCHEDULE_NONCOMPARABILITY
```

These numerical gates are **candidate values requiring adversarial review before adoption**.

They have not been selected from an SFE-02F execution result.

---

## 13. Candidate dependence-aware uncertainty procedure

Serial and calendar dependence must not be ignored.

Candidate resampling unit:

```text
UTC ISO WEEK
```

Procedure:

1. assign each eligible H1 row to its UTC ISO year-week;
2. sample year-week clusters with replacement;
3. retain all eligible rows belonging to sampled weeks;
4. recompute `AUC_cond` using the frozen hour-of-week strata;
5. repeat a fixed number of times;
6. use percentile bounds.

Candidate parameters:

```text
BOOTSTRAP_REPLICATES =
10000

RNG =
PCG64

SEED =
20261002

TWO-SIDED CONFIDENCE =
95%
```

This is a candidate design.

External review must challenge whether ISO-week resampling is adequate for the dependence structure.

---

## 14. Candidate materiality / equivalence band

A statistically detectable deviation from 0.5 may be too small to matter as a measurement-selection effect.

V0.1 therefore proposes a candidate practical-equivalence band:

```text
AUC_cond ∈ [0.45, 0.55]
```

Candidate mapping:

### Higher-intensity observable selection

```text
lower 95% CI > 0.55
→ OBSERVABLE_HIGHER_INTENSITY_SELECTION
```

### Lower-intensity observable selection

```text
upper 95% CI < 0.45
→ OBSERVABLE_LOWER_INTENSITY_SELECTION
```

### Practical equivalence

```text
entire 95% CI inside [0.45, 0.55]
→ NO_MATERIAL_INTENSITY_SELECTION_DETECTED
   WITHIN_PREDEFINED_BAND
```

### Otherwise

```text
→ NON_DECISIVE
```

The `0.45–0.55` band is a **candidate governance choice**, not yet adopted.

External review must specifically assess whether this threshold has adequate scientific justification or should remain unresolved until a stronger non-outcome-based rationale is provided.

---

## 15. Mandatory descriptive schedule diagnostics

These are descriptive and non-decision-bearing:

- count of eligible rows by UTC hour-of-week;
- count and fraction of continuity ends by UTC hour-of-week;
- count of each continuity-end mechanism category;
- continuity-end count by calendar month;
- continuity-end count by calendar year;
- number of rows per continuity block;
- distribution of continuity-block lengths;
- fraction of continuity ends occurring after each mechanism category.

These diagnostics may explain the data-generation mechanism.

They may not be converted post hoc into strategy filters.

---

## 16. Mandatory descriptive intensity diagnostics

Report without additional hypothesis tests:

```text
median X for A=1
median X for A=0

25th / 75th percentile X for A=1
25th / 75th percentile X for A=0

AUC_cond point estimate
AUC_cond CI
```

No alternative movement transform may replace `X_t` after result observation.

---

## 17. Explicit non-questions

SFE-02F does **not** ask:

- whether excluded Breakout events were profitable;
- whether excluded Mean-Reversion events were profitable;
- what their missing `Y` would have been;
- whether a different continuity rule improves strategy performance;
- whether another source gives a better backtest;
- whether another response horizon performs better;
- whether continuity should be relaxed for trading.

---

## 18. Falsification logic for H-E01 / H-E08

### Candidate support for observable selection

If the adopted study ultimately finds a confidence interval materially outside the practical-equivalence band after schedule conditioning, then:

```text
OBSERVABLE_PRE_BOUNDARY_SELECTION =
ESTABLISHED
on this exposed H1 measurement surface
```

This would support further investigation of measurement/continuity before treating the t+1-admissible rows as observationally neutral.

It would **not** prove bias in strategy `Y`.

### Candidate evidence against material observable selection

If the entire adopted confidence interval lies within the practical-equivalence band:

```text
NO_MATERIAL_INTENSITY_SELECTION_DETECTED
WITHIN THE PREREGISTERED BAND
```

This would reduce the specific concern that immediately prior H1 intensity materially distinguishes continuity ends after schedule conditioning.

It would **not** prove full missing-at-random behavior.

### Non-decision

All other outcomes remain:

```text
NON_DECISIVE
```

---

## 19. Why this study is upstream of strategy revision

If observable selection is established, the next problem is measurement/data design.

If no material observable selection is detected under an adequate design, replication of the frozen V1 propositions on new evidence becomes more defensible.

In neither case does SFE-02F itself justify:

```text
BREAKOUT_V2
MEAN_REVERSION_V2
new lookback
new z threshold
new response horizon
compression filter
ATR filter
strategy optimization
```

---

## 20. Known limitations of the candidate design

V0.1 explicitly acknowledges:

1. `X_t` measures only one observable aspect of market state;
2. conditioning on UTC hour-of-week may not capture all schedule/source mechanisms;
3. some hour-of-week strata may have no class overlap;
4. ISO-week bootstrap may or may not fully represent dependence;
5. AUC materiality bounds require independent justification;
6. observed selection in `X_t` does not establish selection in unobserved future returns;
7. absence of selection in `X_t` does not prove absence of selection on other state variables;
8. the evidence surface is already post-result exposed;
9. the data source and instrument remain Source-B / USTECH specific.

These limitations must not be hidden by a PASS label.

---

## 21. Adversarial questions required before adoption

External review must answer at minimum:

```text
AR-01
Does the proposed unit/label accidentally use strategy information?

AR-02
Does A_t use only continuity information rather than market outcome?

AR-03
Is excluding the final dataset row correct and sufficiently specified?

AR-04
Is X_t truly available by time t and free of look-ahead?

AR-05
Does hour-of-week conditioning appropriately address obvious schedule confounding?

AR-06
Could hour-of-week conditioning itself introduce a material bias or destroy interpretability?

AR-07
Is pooled within-stratum AUC the right estimand for the stated measurement question?

AR-08
Can strata with extreme pair counts dominate AUC_cond in a scientifically undesirable way?

AR-09
Are the comparability gates sufficient and non-opportunistic?

AR-10
Is ISO-week cluster bootstrap defensible for uncertainty here?

AR-11
Is 10,000 bootstrap replicates adequate and reproducible?

AR-12
Is the [0.45,0.55] equivalence band scientifically defensible without outcome tuning?

AR-13
Should the study instead avoid a binary materiality conclusion until that band is justified externally?

AR-14
Are continuity-end reason categories exhaustive and mutually exclusive?

AR-15
Does source_segment_id create any circularity because it participates in block construction?

AR-16
Could the proposed study accidentally become a strategy-data rescue mechanism?

AR-17
Are H-E01/H-E08 falsification claims scoped narrowly enough?

AR-18
What minimum correction is required before human adoption?
```

---

## 22. Candidate state

```text
SFE_02F_DESIGN_CANDIDATE_V0_1 =
PRODUCED

STUDY_EXECUTION =
NOT_AUTHORIZED

RAW_H1_ANALYSIS =
NOT_AUTHORIZED

BREAKOUT_SIGNAL =
NOT_USED

MEAN_REVERSION_SIGNAL =
NOT_USED

BEHAVIORAL_Y =
NOT_AUTHORIZED

THETA =
NOT_AUTHORIZED

PNL =
NOT_AUTHORIZED

PARAMETER_SEARCH =
NOT_AUTHORIZED

STRATEGY_CHANGE =
NOT_AUTHORIZED

NEXT =
EXTERNAL ADVERSARIAL DESIGN REVIEW

STOP =
TRUE
```
