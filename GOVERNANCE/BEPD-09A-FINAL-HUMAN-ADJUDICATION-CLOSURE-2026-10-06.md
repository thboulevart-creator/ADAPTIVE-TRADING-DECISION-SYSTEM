# BEPD-09A — FINAL HUMAN ADJUDICATION / CLOSURE — 2026-10-06

## Fresh pre-mutation verification

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

FRESH PRE-MUTATION HEAD =
694494ffd922f290cdee5201910ffeb22f198ebd

FRESH PRE-MUTATION TREE =
c9e2b86c3ed4862b61a9a344c4544036c5b16f06

CONCURRENT DRIFT FROM LAST BEPD-09A CHECKPOINT =
NON_MATERIAL_TO_BEPD_09A

OBSERVED CONCURRENT WORK =
SMF-AP1-M03-02-R1-POST-M10-PCG-02C ONLY
```

The identities above are the branch state observed immediately before this authorized mutation. They are not imposed as future HEAD/TREE values.

## Human decision

```text
HUMAN ADJUDICATION =
ADOPT
```

The human principal adopts the qualified package:

`BEPD-09A — EX-ANTE DECISION-TIME INFORMATION + CANDIDATE CLAIM SELECTION GATE V0.1`

This adoption is limited to the design, freeze and qualification of the ex-ante information boundary for future BEPD work.

It does not create predictive validation, statistical validation of any candidate claim, a selected predictor/model, generalization evidence, edge, strategy authority or trading authority.

## Qualified package identities

```text
BEPD-09A DESIGN PACKAGE HEAD =
374ab2c04401eecb2b8f3319022df924ca889a8e

BEPD-09A DESIGN PACKAGE TREE =
df4937f4934edec87a34449b27454d07453b44fb

HUMAN AUTHORIZATION =
7324ceafdc66c9fa9e21d2f6d8e455ab85c07e14

BEPD-09A DESIGN CONTRACT =
a3a3dd9fae1548de2b5ee6bf76536e68820ba932

BEPD-09A FROZEN DOCUMENTARY BREAKER =
d5cc742bb4cd256dde6f9a9988caece3a687b54e

BEPD-09A DESIGN REPORT =
a5dead3f42e2ce0521a168bfa9905f9a0a83c18d

QUALIFICATION HEAD =
d65c48e4c6bd727567f800146684b3901543ff08

QUALIFICATION TREE =
72dbcb9e02fe844ed417689f1ff5f1ab2810c444

DOCUMENTARY / PROGRAMMATIC QUALIFICATION RECEIPT =
cff9cdc47e59be1e6c77a05bbcd3661bba99a810

DOCUMENTARY / PROGRAMMATIC QUALIFICATION REPORT =
59609d27a6c1943dfef71cd1631a236c364e9c15

PERSISTED-HEAD VERIFICATION RECEIPT =
823b9d0557d73b13e33af1d807c057f192a69782
```

## Accepted qualification

```text
PROGRAMMATIC CHECKS =
33 / 33 PASS

DOCUMENTARY HARD-FAIL CASES =
28 / 28 PRESENT

REAL EVENT_LEDGER ROWS READ =
NO

REAL RESULT RECOMPUTATION =
NO

STATISTICAL TEST =
NO

MODEL FIT =
NO

OOS READ =
NO
```

## Adopted decision-time boundary

```text
T0 =
take_h1_close_utc

T0 =
FIRST QUALIFYING H1 CLOSE
AT WHICH THE ACTIVE WEEKLY LEVEL
IS STRICTLY TAKEN
AND THE QUALIFIED LEVEL_SWEEP_EVENT
CANONICALLY EXISTS
```

The following rule is adopted, binding and frozen:

```text
INFORMATION CAUSALLY AVAILABLE
AT OR BEFORE T0
=
POTENTIALLY PREDICTOR-ELIGIBLE

INFORMATION AVAILABLE
STRICTLY AFTER T0
=
FORBIDDEN AS EX-ANTE PREDICTOR
```

Also binding:

```text
FIELD PRESENT
IN COMPLETED HISTORICAL LEDGER ROW
!=
FIELD AVAILABLE EX-ANTE AT T0
```

Historical row presence alone never proves predictor eligibility.

## Current predictor-eligibility surface

The following fields are recognized only as potentially eligible for future claim-specific design because they are available at or before T0:

```text
source_week_id
target_week_id AS CALENDAR CONTEXT ONLY
side
level_price_mid
level_age_weeks
active_level_count_at_target_week_start
take_h1_bucket_start_utc
take_h1_close_utc
take_h1_close_mid
```

This does not establish that any of them is predictive, informative, material, statistically significant, generalizable or useful for trading.

## Identity and diagnostic boundary

```text
event_id
level_id
sweep_cluster_id
```

remain identity / join / dependence keys and are not promoted as economic predictors.

Quality and provenance fields remain diagnostic-only unless separately justified and authorized.

## Adopted post-T0 exclusions

The following remain forbidden as ex-ante predictors:

```text
cluster_consumed_level_count
reintegration_h1_bucket_start_utc
reintegration_h1_close_utc
reintegration_h1_close_mid
reintegration_h1_internal_gap_count
same_week_reintegration
target_week_close_mid
close_displacement
CLOSE_SIDE
D_CLOSE
D_INTERNAL
D_EXTERNAL
target_week_gap_count_gt60s
target_week_max_gap_ms
```

Binding interpretation:

```text
CLOSE_SIDE =
OUTCOME / NOT PREDICTOR

D_CLOSE =
OUTCOME / NOT PREDICTOR

D_INTERNAL =
OUTCOME-CONDITIONED DESCRIPTION / NOT PREDICTOR

D_EXTERNAL =
OUTCOME-CONDITIONED DESCRIPTION / NOT PREDICTOR
```

`cluster_consumed_level_count` is forbidden as a predictor in its current definition because its final value can include levels consumed after T0.

## Holiday / calendar boundary

```text
holiday_tag =
NOT CURRENTLY PREDICTOR-ELIGIBLE
```

Future use requires a separately bound ex-ante calendar source and proof that the information is causally available at or before T0.

Historical terminal metadata cannot substitute for that source.

## Derived-feature anti-leakage rule

A derived feature may become a future candidate if and only if:

```text
ALL SOURCE INPUTS
ARE INDIVIDUALLY
CAUSALLY AVAILABLE <= T0

AND

THE TRANSFORMATION FORMULA
IS FROZEN
BEFORE RESPONSE / OUTCOME READ
```

Forbidden:

```text
POST-T0 INPUTS
TARGET-WEEK-END INPUTS
FUTURE CLUSTER INFORMATION
OUTCOME-CONDITIONED JOINS
TARGET ENCODING FROM EXPOSED OUTCOMES
POST-HOC THRESHOLD OPTIMIZATION
FEATURE SELECTION BECAUSE OF OBSERVED RESPONSE PERFORMANCE
LABEL LEAKAGE
```

## Dependence boundary

```text
EVENT IS IID =
FALSE

DEPENDENCE KEYS =
target_week_id
sweep_cluster_id
```

Future methods may not silently introduce event-level IID.

## Adopted candidate-claim ranking

### C1 — Rank 1 / preferred first candidate

```text
T0-AVAILABLE CONTEXT
→
SAME-WEEK REINTEGRATION
```

Response:

`same_week_reintegration`

Status:

```text
PREFERRED FIRST CANDIDATE
NOT SELECTED
NOT ACTIVATED
NOT TESTED
```

Material caveat:

```text
REMAINING OBSERVATION TIME
FROM T0 TO TARGET-WEEK END
VARIES ACROSS EVENTS
```

Any future C1 design must explicitly represent or otherwise control this unequal exposure time.

### C2 — Rank 2

```text
T0-AVAILABLE CONTEXT
→
TARGET-WEEK CLOSE_SIDE
```

`CLOSE_SIDE` is response/outcome only, never predictor.

### C3 — Rank 3

```text
T0-AVAILABLE CONTEXT
→
D_CLOSE
```

`D_CLOSE` is a continuous target-week-end outcome and is not a TP, SL or trade target.

### C4 — Rank 4 / defer

```text
T0-AVAILABLE CONTEXT
→
TIME TO FIRST REINTEGRATION
```

C4 remains deferred until separately frozen time-to-event estimand, non-reintegration state, censoring, unequal-observation-window and survival semantics exist.

## No claim selection created

```text
FINAL CLAIM SELECTED =
NO

C1 SELECTED =
NO

C2 SELECTED =
NO

C3 SELECTED =
NO

C4 SELECTED =
NO
```

The ranking `C1 > C2 > C3 > C4` is design guidance only.

It is neither scientific validation nor execution authority.

## Scientific status

```text
HISTORICAL CORPUS =
ALREADY EXPOSED

BEPD-09A REAL ROW ANALYSIS =
NONE

GENERALIZATION =
NOT_ESTABLISHED

CONFIRMATORY GENERALIZATION =
NOT_ESTABLISHED

PREDICTION =
NO

CAUSATION =
NOT_ESTABLISHED

EDGE =
NO

STRATEGY VALIDATION =
NO

TRADING AUTHORITY =
NONE
```

## Closed frontiers

```text
HISTORICAL CLAIM TESTING =
CLOSED

C1 EXECUTION =
CLOSED

C2 EXECUTION =
CLOSED

C3 EXECUTION =
CLOSED

C4 EXECUTION =
CLOSED

FEATURE SELECTION FROM OUTCOMES =
CLOSED

COMPARATIVE TESTING =
CLOSED

THRESHOLD SEARCH =
CLOSED

MODEL TRAINING =
CLOSED

OOS CONSUMPTION =
CLOSED

TP / SL =
CLOSED

BACKTEST STRATEGY =
CLOSED

PNL =
CLOSED

PAPER TRADING =
CLOSED

BROKER EXECUTION =
CLOSED

LIVE TRADING =
CLOSED

CAPITAL DEPLOYMENT =
CLOSED
```

## Final BEPD-09A decision

```text
BEPD-09A =
HUMAN_ADOPTED

DECISION-TIME BOUNDARY =
ADOPTED / BINDING / FROZEN

CAUSAL INFORMATION-AVAILABILITY RULE =
ADOPTED / BINDING / FROZEN

PREDICTOR / RESPONSE / OUTCOME SEPARATION =
ADOPTED / BINDING / FROZEN

DERIVED-FEATURE ANTI-LEAKAGE RULE =
ADOPTED / BINDING / FROZEN

DEPENDENCE BOUNDARY =
ADOPTED / BINDING / FROZEN

CANDIDATE CLAIM GATE =
ADOPTED / BINDING / FROZEN

CANDIDATE CLAIM RANKING =
ADOPTED AS DESIGN GUIDANCE ONLY

TECHNICAL / DOCUMENTARY QUALIFICATION =
ACCEPTED

STATUS =
QUALIFIED / HUMAN_ADOPTED / CLOSED
```

No BEPD-09A re-execution is authorized.

No real EVENT_LEDGER read is authorized.

No prior BEPD result recomputation is authorized.

No candidate claim is automatically selected.

No new scientific frontier is automatically opened.

```text
STOP
```

Any later selection of C1 or another candidate requires a separate human decision.
