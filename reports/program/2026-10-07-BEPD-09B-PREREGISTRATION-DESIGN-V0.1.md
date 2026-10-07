# BEPD-09B — C1 CLAIM PREREGISTRATION + EXPOSURE-TIME CONTROL DESIGN V0.1

## Status

```text
PHASE =
DESIGN_ONLY / PREREGISTRATION_ONLY / PRE_RESULT

C1 =
SELECTED FOR PREREGISTRATION

C1 REAL EXECUTION =
NOT AUTHORIZED
```

## Exact claim

The preregistered question is:

> Does a fixed, prespecified set of information available at T0 add out-of-forward predictive information about `same_week_reintegration` beyond the information contained in remaining calendar exposure time alone?

This is an incremental predictive-information question, not a causal claim and not a trading claim.

## Response

```text
T0 =
take_h1_close_utc

RESPONSE =
same_week_reintegration
```

The response retains the already-qualified BEPD-04A meaning. It is never recomputed in BEPD-09B.

## Mandatory exposure control

```text
REMAINING_CALENDAR_HOURS_TO_TARGET_WEEK_END =
(target_week_end_utc - take_h1_close_utc) / 3600
```

The target-week end is determined from the bound complete-week calendar using the Sunday 18:00 America/New_York boundary and converted to UTC.

This quantity is known at T0 and is the mandatory exposure control.

The following are forbidden because they depend on post-T0 observations:

```text
ACTUAL FUTURE H1 COUNT
FUTURE GAP-ADJUSTED EXPOSURE
POST-T0 OBSERVATION-QUALITY ADJUSTMENT
```

## Frozen claim-scoped context

Beyond exposure, C1 is allowed exactly four context inputs:

```text
SIDE_HIGH_INDICATOR
LEVEL_AGE_WEEKS
ACTIVE_LEVEL_COUNT_AT_TARGET_WEEK_START
SWEEP_OVERSHOOT_RELATIVE
```

where:

```text
SIDE_HIGH_INDICATOR =
1 for HIGH
0 for LOW

SWEEP_OVERSHOOT_RELATIVE =
abs(take_h1_close_mid - level_price_mid)
/
abs(level_price_mid)
```

No other feature, interaction, subgroup or nonlinear search is authorized.

Raw dates, raw timestamps, raw prices and identity keys are excluded from the model surface.

## Future exploratory method — preregistered but not executable yet

Two fixed logistic models are preregistered:

```text
BASELINE =
EXPOSURE ONLY

CONTEXT =
EXPOSURE
+ SIDE
+ LEVEL AGE
+ ACTIVE LEVEL COUNT
+ RELATIVE SWEEP OVERSHOOT
```

No regularization, variable selection, interaction search or hyperparameter tuning is permitted.

Continuous variables are standardized using training-fold statistics only.

Zero/nonfinite training standard deviation, perfect separation or nonconvergence causes fail-closed.

## Forward calendar evaluation

The bound complete target-week calendar is partitioned into six contiguous chronological blocks with week counts differing by at most one.

Five expanding-window evaluations are frozen:

```text
TRAIN B1       → TEST B2
TRAIN B1-B2    → TEST B3
TRAIN B1-B3    → TEST B4
TRAIN B1-B4    → TEST B5
TRAIN B1-B5    → TEST B6
```

Empty calendar weeks remain in the calendar partition.

No target week or sweep cluster may be split between train and test.

No random shuffle is permitted.

Because the historical corpus is already exposed, this is only an exploratory pseudo-forward evaluation and is not confirmatory OOS evidence.

## Exact estimand

Primary:

```text
WEEK_BALANCED_OUT_OF_FORWARD_LOGLOSS_IMPROVEMENT

DELTA =
BASELINE LOGLOSS
-
CONTEXT LOGLOSS

POSITIVE =
LOWER HELD-OUT LOGLOSS FOR CONTEXT MODEL
```

Each held-out event receives a log-loss; losses are first averaged within target week, then averaged across event-bearing held-out target weeks.

Secondary:

```text
WEEK_BALANCED_OUT_OF_FORWARD_BRIER_IMPROVEMENT
```

Event-weighted log-loss and Brier scores are diagnostic only.

No automatic success threshold is frozen. Any later real result requires human adjudication.

## Dependence

```text
EVENT IID =
FALSE

PRIMARY DEPENDENCE UNIT =
target_week_id

SWEEP CLUSTER INTEGRITY =
PRESERVED
```

Week-balanced scoring limits domination by multi-event weeks but does not create confirmatory independence.

## Missingness / inadmissibility

No required row may be silently dropped and no value may be imputed.

Any missing required predictor/response, invalid side, nonfinite numeric, nonpositive remaining exposure, zero level price, duplicate event ID, target-week calendar mismatch or cluster/week mismatch causes fail-closed.

## Multiplicity boundary

```text
CONTEXT FEATURES =
4 FIXED

MODELS =
2 FIXED

SUBGROUP SEARCH =
FORBIDDEN

FEATURE IMPORTANCE SEARCH =
FORBIDDEN

COEFFICIENT SIGN HUNTING =
FORBIDDEN

THRESHOLD SEARCH =
FORBIDDEN

AUC =
FORBIDDEN

ALTERNATIVE MODEL FAMILY SEARCH =
FORBIDDEN
```

## Future result surface

A later separately authorized execution may expose only deterministic integrity/admissibility evidence, fold boundaries/counts, convergence status, per-fold and aggregate week-balanced log-loss/Brier for baseline and context, their deltas, event-weighted diagnostics, deterministic replay identity and independent-reference parity.

It may not expose p-values, confidence intervals, bootstrap/permutation inference, feature importance, coefficient ranking, subgroup results, threshold optimization, TP/SL, PnL or trading signals.

## Evidence boundary

```text
HISTORICAL CORPUS =
ALREADY EXPOSED

ANY FIRST HISTORICAL C1 EXECUTION =
EXPLORATORY_ONLY

CONFIRMATORY GENERALIZATION =
FRESH UNEXPOSED OOS REQUIRED

CURRENT OOS READ =
NOT AUTHORIZED

PREDICTION VALIDATED =
NO

GENERALIZATION =
NOT_ESTABLISHED

EDGE =
NO

TRADING AUTHORITY =
NONE
```

## Stop boundary

BEPD-09B may be qualified documentarily/programmatically and verified at persisted head.

No real ledger read and no model fit are authorized.

After qualification:

```text
STOP FOR HUMAN ADJUDICATION
```
