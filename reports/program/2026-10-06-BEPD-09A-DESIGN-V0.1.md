# BEPD-09A — EX-ANTE DECISION-TIME INFORMATION + CANDIDATE CLAIM SELECTION GATE — DESIGN V0.1

## Scope

Design-only. No real historical row was read for this phase, no BEPD result was recomputed, and no candidate claim was tested.

## Binding identities

```text
HUMAN AUTHORIZATION =
7324ceafdc66c9fa9e21d2f6d8e455ab85c07e14

BEPD-09A DESIGN CONTRACT =
a3a3dd9fae1548de2b5ee6bf76536e68820ba932

BEPD-09A FROZEN DOCUMENTARY BREAKER =
d5cc742bb4cd256dde6f9a9988caece3a687b54e

BEPD-08D FINAL HUMAN ADJUDICATION =
227ee01f330fc5c10ad29422cab69ac8a6461de4

BEPD-01D LEDGER SCHEMA =
85f5cdda60397fce59efc1e5d36c1128cf9cc185
```

## Decision-time boundary

```text
T0 =
take_h1_close_utc

T0 SEMANTIC =
FIRST QUALIFYING H1 CLOSE AT WHICH
THE ACTIVE WEEKLY LEVEL IS STRICTLY TAKEN
AND THE LEVEL_SWEEP_EVENT CANONICALLY EXISTS
```

A field being present in a completed historical ledger row does **not** make it ex-ante information.

The predictor eligibility rule is:

```text
CAUSAL_AVAILABLE_AT_OR_BEFORE_T0
=
REQUIRED

POST_T0 INFORMATION
=
FORBIDDEN AS PREDICTOR
```

## Frozen predictor-eligible surface

Currently eligible at or before T0, subject to later claim-specific design:

- source_week_id;
- target_week_id as calendar context;
- side;
- level_price_mid;
- level_age_weeks;
- active_level_count_at_target_week_start;
- take_h1_bucket_start_utc;
- take_h1_close_utc;
- take_h1_close_mid.

Quality diagnostics such as H1 gap counts remain diagnostic-only.

Identity keys such as event_id, level_id and sweep_cluster_id are not economic predictors.

## Frozen post-T0 / outcome exclusions

Forbidden as predictors:

- cluster_consumed_level_count;
- reintegration_h1_*;
- same_week_reintegration;
- target_week_close_mid;
- close_displacement;
- CLOSE_SIDE;
- D_CLOSE;
- D_INTERNAL;
- D_EXTERNAL;
- target-week terminal gap diagnostics.

`holiday_tag` is not predictor-eligible until a separately bound calendar source proves ex-ante availability.

## Derived-feature rule

A derived feature is only a candidate if every input is causally available at or before T0 and its transformation is frozen before any response/outcome read.

Post-hoc thresholding, target encoding, outcome-conditioned joins and future cluster information are forbidden.

## Ranked candidate claims

### C1 — preferred first candidate

Question:

> Does information available at T0 contain information about whether the swept Weekly level obtains a strict qualifying H1 reintegration before target-week end?

Response: `same_week_reintegration`.

Critical caveat: available observation time varies with T0. Any future design must explicitly represent or otherwise control remaining time to target-week end.

### C2 — secondary

Question:

> Does information available at T0 contain information about the target-week terminal close side relative to the swept Weekly level?

Response: `CLOSE_SIDE`.

`CLOSE_SIDE` is an outcome here, never a predictor.

### C3 — secondary

Question:

> Does information available at T0 contain information about the absolute target-week-close distance from the swept Weekly level?

Response: `D_CLOSE`.

No target, TP, SL or trading interpretation is created.

### C4 — defer

Question:

> Does information available at T0 contain information about time to first reintegration?

This requires separately frozen survival/time-to-event semantics because non-reintegration and unequal remaining observation windows are material.

## Dependence

```text
EVENT IID =
FALSE

DEPENDENCE KEYS =
target_week_id
sweep_cluster_id
```

No future method may silently assume event-level IID.

## Gate state

```text
FINAL CLAIM SELECTED =
NO

CLAIM TESTING AUTHORIZED =
NO

REAL DATA READ =
NO

HISTORICAL EXPLORATORY TEST =
NO

OOS READ =
NO

THRESHOLD SEARCH =
NO

TP / SL =
NO

STRATEGY =
NO

TRADING AUTHORITY =
NONE
```

## Next action

Human adjudication of this BEPD-09A design package only.

No candidate claim becomes active until a separate human decision selects one exact claim and authorizes its preregistration.

```text
STOP
```
