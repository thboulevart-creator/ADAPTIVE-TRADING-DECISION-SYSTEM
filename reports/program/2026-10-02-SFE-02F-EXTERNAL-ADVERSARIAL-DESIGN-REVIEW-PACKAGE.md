# SFE-02F — EXTERNAL ADVERSARIAL DESIGN REVIEW PACKAGE

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`

---

## 0. Review target

Audit exactly:

```text
GOVERNANCE/SFE-02F-CONTINUITY-ATTRITION-MEASUREMENT-STUDY-DESIGN-CANDIDATE-V0.1.md

SOURCE_BLOB_REVIEWED =
56a6933a3f9b12228cfabf127669516ea54dc4eb
```

The source under review is reproduced verbatim in §8.

This is a **design review only**.

Do not execute the study.

Do not invent results.

Do not optimize a trading strategy.

---

## 1. Scientific context

SFE-02D ran two preregistered behavioral experiments:

```text
BREAKOUT_V1
MEAN_REVERSION_V1
```

Both were non-decisive.

SFE-02E then identified a measurement question upstream of strategy modification:

> Are continuity endings associated with observable pre-boundary market-state intensity such that rows with an admissible same-block t+1 cannot be assumed to be a behaviorally neutral subsample of the canonical H1 surface?

The candidate SFE-02F study deliberately does **not** use strategy signals, strategy outcomes, PnL, execution, or parameter search.

The design is intended to test a data/measurement-selection mechanism.

---

## 2. Binding upstream dataset/continuity contract

Source:

```text
GOVERNANCE/E1-03-H1-DATASET-IDENTITY-CONTRACT-V0.1.json

BLOB =
c2d4323039d65fcd9319d4f5eb02f45ee27c8afc
```

The relevant binding facts include:

```text
H1 timezone =
UTC

H1 duration =
3600000 ms

required M1 rows per accepted H1 =
60 exact minutes

same source segment required inside H1 =
TRUE

forward fill =
FALSE

interpolation =
FALSE

synthetic minutes =
FALSE

continuity new block when =
1. source_segment_id changes
OR
2. current_h1_start_ms_utc != previous_h1_start_ms_utc + 3600000

continuity ordinal starts =
0
```

Exact authoritative E1-03 contract is reproduced in §7.

---

## 3. Provenance-governance context

Source:

```text
GOVERNANCE/G6-MINIMAL-CROSS-EXPERIMENT-PROVENANCE-REGISTRY-HUMAN-ADJUDICATION-2026-10-02.md

BLOB =
93e3c87f24b8933fbdfe25b1806d42233b6ec328
```

Relevant limits:

```text
G6 =
HUMAN_ADOPTED_FOR_SEMANTIC_DESIGN_ONLY

IMPLEMENTATION =
NOT_AUTHORIZED
```

Therefore SFE-02F may use G6 semantics conceptually, but must not implement or claim a provenance-registry runtime.

---

## 4. Your role

Act as a hostile but precise scientific-design reviewer.

Your task is to determine whether the candidate can validly answer its stated measurement question **without leaking back into strategy rescue, outcome mining, or unjustified causal claims**.

Challenge the design on:

- construct validity;
- unit definition;
- attrition-label validity;
- look-ahead;
- schedule confounding;
- conditioning strategy;
- comparability;
- estimand choice;
- weighting;
- dependence;
- bootstrap validity;
- practical-equivalence threshold;
- multiplicity;
- exposure/provenance;
- strategy-independence;
- post-result contamination;
- falsification logic;
- interpretive scope.

Do not recommend a trading setup.

Do not propose a profitable parameter.

Do not rank Breakout vs Mean Reversion.

Do not use the already-observed SFE-02D results to tune SFE-02F.

---

## 5. Required adversarial questions

Return a determination for every item:

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
Could hour-of-week conditioning itself introduce material bias
or destroy interpretability?

AR-07
Is pooled within-stratum AUC the right estimand
for the stated measurement question?

AR-08
Can strata with extreme pair counts dominate AUC_cond
in a scientifically undesirable way?

AR-09
Are the comparability gates sufficient and non-opportunistic?

AR-10
Is ISO-week cluster bootstrap defensible for uncertainty here?

AR-11
Is 10,000 bootstrap replicates adequate and reproducible?

AR-12
Is the [0.45,0.55] equivalence band scientifically defensible
without outcome tuning?

AR-13
Should the study avoid a binary materiality conclusion
until that band is justified externally?

AR-14
Are continuity-end reason categories exhaustive and mutually exclusive?

AR-15
Does source_segment_id create circularity because it participates
in block construction?

AR-16
Could the study become a strategy-data rescue mechanism?

AR-17
Are H-E01/H-E08 falsification claims scoped narrowly enough?

AR-18
What minimum correction is required before human adoption?
```

For each:

```text
CLOSED
PARTIALLY_CLOSED
OPEN
NOT_APPLICABLE
```

with reasoning.

---

## 6. Required final output format

Return exactly these top-level sections:

### A. MODEL

State model name/version.

### B. SOURCE IDENTITY

```text
SOURCE_BLOB_REVIEWED =
56a6933a3f9b12228cfabf127669516ea54dc4eb
```

Confirm whether the reviewed source matches this exact identity.

### C. OVERALL VERDICT

Choose one:

```text
PASS

PASS_WITH_NON_BLOCKING_FINDINGS

FAIL
```

### D. AR-01 → AR-18 CLOSURE MATRIX

For each AR item:

```text
AR-XX =
CLOSED | PARTIALLY_CLOSED | OPEN | NOT_APPLICABLE

REASON =
...

BLOCKS_HUMAN_ADOPTION =
YES | NO
```

### E. NEW FINDINGS

For every new finding use:

```text
FINDING_ID =
CATEGORY =
SEVERITY = CRITICAL | HIGH | MEDIUM | LOW
CLAIM_TYPE = FACT | INTERPRETATION | DESIGN_RISK
AFFECTED_SECTION =
REASON =
FALSIFICATION_TEST =
BLOCKS_HUMAN_ADOPTION = YES | NO
MINIMAL_CORRECTION =
```

### F. DESIGN-REGRESSION CHECK

Return:

```text
USES_STRATEGY_SIGNALS =
YES | NO

USES_STRATEGY_Y =
YES | NO

USES_PNL =
YES | NO

SEARCHES_PARAMETERS =
YES | NO

SEARCHES_RESPONSE_HORIZONS =
YES | NO

CHANGES_BREAKOUT_V1 =
YES | NO

CHANGES_MEAN_REVERSION_V1 =
YES | NO

CONSUMES_TD03B =
YES | NO
```

Any unexpected `YES` is potentially blocking.

### G. SPECIFIC STATISTICAL REVIEW

Address separately:

```text
G1 — AUC_cond estimand validity
G2 — within-stratum pair weighting
G3 — schedule overlap / positivity
G4 — ISO-week dependence handling
G5 — bootstrap confidence interval validity
G6 — equivalence/materiality band justification
G7 — multiple-decision / multiplicity risk
G8 — whether the candidate can distinguish
     "no measured intensity selection"
     from
     "missing at random"
```

### H. READINESS

Return separately:

```text
DESIGN_READY_FOR_HUMAN_ADJUDICATION =
YES | NO

STUDY_EXECUTION_READY =
YES | NO

MINIMAL_REQUIRED_CORRECTIONS =
...
```

Important:

Even if the design is ready for human adjudication, study execution remains outside the authority of this package unless separately authorized after human adoption.

---

## 7. AUTHORITATIVE E1-03 CONTRACT — VERBATIM

```json
{
  "schema": "ATDS_E1_03_H1_DATASET_IDENTITY_CONTRACT_V0_1",
  "control_id": "E1-03",
  "status": "HUMAN_ADOPTED_TEST_FIRST",
  "date": "2026-09-28",
  "authority": {
    "implementation_authorized": false,
    "real_h1_build_authorized": false,
    "e1_run_authorized": false,
    "allowed_data_class_for_red": "SYNTHETIC_ONLY"
  },
  "runtime_target": "tools/e1_03_h1_dataset_identity.py",
  "runtime_contract": "ATDS_E1_03_H1_DATASET_IDENTITY_V0_1",
  "required_runtime_surface": [
    "CONTRACT",
    "derive_h1_dataset",
    "canonical_stream_sha256",
    "verify_ap0_binding"
  ],
  "input": {
    "dataset_identity": "USTECH_PROFILE_MINUTE_CORE_V0_1",
    "source_identity": "SOURCE_B_USTECH_PRICE_CORE_V0_1",
    "ap0_manifest_sha256": "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce",
    "ap0_files": 61,
    "ap0_rows": 1709180,
    "ap0_segments": 1606,
    "ap0_gaps_gt_60s": 1605,
    "required_columns": [
      "minute_start_ms_utc",
      "first_tick_ms",
      "last_tick_ms",
      "tick_count",
      "segment_id",
      "segment_start",
      "gap_before_ms",
      "mid_close"
    ]
  },
  "output": {
    "dataset_identity": "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",
    "row_fields_exact": [
      "h1_start_ms_utc",
      "source_segment_id",
      "continuity_block_id",
      "continuity_ordinal",
      "mid_close"
    ]
  },
  "raw_window": {
    "start_utc": "2021-05-25T00:00:00.309Z",
    "end_utc": "2026-05-24T23:59:59.963Z",
    "boundary_partial_hour_policy": "REJECT"
  },
  "h1_bucket": {
    "timezone": "UTC",
    "duration_ms": 3600000,
    "start_rule": "floor(minute_start_ms_utc / 3600000) * 3600000",
    "required_m1_rows": 60,
    "required_offsets_minutes": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23,
      24,
      25,
      26,
      27,
      28,
      29,
      30,
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38,
      39,
      40,
      41,
      42,
      43,
      44,
      45,
      46,
      47,
      48,
      49,
      50,
      51,
      52,
      53,
      54,
      55,
      56,
      57,
      58,
      59
    ],
    "same_segment_required": true,
    "segment_start_allowed_only_at_minute_offset": 0,
    "forward_fill": false,
    "interpolation": false,
    "synthetic_minutes": false,
    "close_rule": "mid_close of minute offset 59"
  },
  "continuity": {
    "new_block_when": [
      "source_segment_id changes",
      "current_h1_start_ms_utc != previous_h1_start_ms_utc + 3600000"
    ],
    "ordinal_start": 0,
    "warmup_h1_bars": 20,
    "first_momentum_eligible_ordinal": 20,
    "cross_block_warmup_forbidden": true
  },
  "oos": {
    "start_utc": "2025-05-25T00:00:00Z",
    "pre_oos_rule": "h1_start_ms_utc < OOS_START",
    "oos_rule": "h1_start_ms_utc >= OOS_START",
    "reset_warmup_at_oos": false,
    "prior_same_block_history_allowed": true
  },
  "input_binding": {
    "manifest_sha256_must_match": true,
    "all_61_files_must_be_rehashed": true,
    "mismatch_status": "BLOCKED"
  },
  "canonical_digest": {
    "prefix_utf8": "ATDS_E1_H1_CANONICAL_STREAM_V0_1\\n",
    "row_binary_big_endian": ">qqqqd",
    "algorithm": "SHA-256",
    "parquet_independent": true
  },
  "test_cases": [
    [
      "H1-01",
      "60 exact M1 minutes, same segment",
      "ACCEPT"
    ],
    [
      "H1-02",
      "59 M1 minutes",
      "REJECT_HOUR"
    ],
    [
      "H1-03",
      "duplicate minute",
      "BLOCKED"
    ],
    [
      "H1-04",
      "wrong minute inside bucket",
      "REJECT_HOUR"
    ],
    [
      "H1-05",
      "segment changes inside H1",
      "REJECT_HOUR"
    ],
    [
      "H1-06",
      "segment_start at minute 00",
      "ACCEPT_AND_RESET"
    ],
    [
      "H1-07",
      "segment_start after minute 00",
      "REJECT_HOUR"
    ],
    [
      "H1-08",
      "first raw boundary hour",
      "REJECT_BOUNDARY"
    ],
    [
      "H1-09",
      "last raw boundary hour",
      "REJECT_BOUNDARY"
    ],
    [
      "H1-10",
      "missing minute must not be forward-filled",
      "FORBIDDEN"
    ],
    [
      "H1-11",
      "H1 close equals M1 minute 59 close",
      "EXACT_CLOSE"
    ],
    [
      "H1-12",
      "continuity block change",
      "ORDINAL_RESET_ZERO"
    ],
    [
      "H1-13",
      "continuity ordinal 19",
      "MOMENTUM_INELIGIBLE"
    ],
    [
      "H1-14",
      "continuity ordinal 20",
      "FIRST_MOMENTUM_ELIGIBLE"
    ],
    [
      "H1-15",
      "t-20 in another continuity block",
      "MOMENTUM_FORBIDDEN"
    ],
    [
      "H1-16",
      "H1 exactly at OOS_START",
      "OOS"
    ],
    [
      "H1-17",
      "OOS with prior same-block history",
      "WARMUP_ALLOWED"
    ],
    [
      "H1-18",
      "AP0 manifest hash mutation",
      "BLOCKED"
    ],
    [
      "H1-19",
      "one AP0 file hash mutation",
      "BLOCKED"
    ],
    [
      "H1-20",
      "two identical builds",
      "SAME_CANONICAL_DIGEST"
    ],
    [
      "H1-21",
      "one H1 row mutation",
      "CANONICAL_DIGEST_CHANGES"
    ]
  ],
  "non_authorizations": [
    "MOMENTUM_SIGNAL",
    "POSITION",
    "TRADE",
    "PNL",
    "EXECUTION",
    "OPTIMIZATION",
    "REGIME",
    "BACKTEST",
    "E1_RUN",
    "E1_05"
  ]
}

```

---

## 8. SFE-02F DESIGN CANDIDATE V0.1 — VERBATIM

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


---

## 9. Hard stop

Do not:

- calculate SFE-02F results;
- inspect raw H1 data;
- calculate strategy performance;
- modify strategy definitions;
- suggest optimization based on SFE-02D outcomes.

The review ends at design adjudication readiness.
