# BEPD-09B-R1 — EXPOSURE-CONTROL FUNCTIONAL-FORM TARGETED AMENDMENT V0.1

## Scope

R1 changes only the functional form used to represent remaining exposure time.

```text
REAL EVENT_LEDGER READ =
NO

REAL C1 MODEL FIT =
NO

REAL RESULT EXPOSURE =
NO
```

## Human decision

```text
BEPD-09B V0.1 =
ADOPT_WITH_AMENDMENTS

LINEAR EXPOSURE FORM =
NOT ADOPTED

R1 TARGET =
FIXED OUTCOME-BLIND NONLINEAR EXPOSURE BASIS
```

## Normalized exposure

```text
TARGET_WEEK_DURATION_HOURS =
(target_week_end_utc - target_week_start_utc) / 3600

REMAINING_CALENDAR_HOURS_TO_TARGET_WEEK_END =
(target_week_end_utc - take_h1_close_utc) / 3600

EXPOSURE_FRACTION =
REMAINING_CALENDAR_HOURS_TO_TARGET_WEEK_END
/
TARGET_WEEK_DURATION_HOURS
```

The calendar boundaries remain Sunday 18:00 America/New_York and are converted to UTC. This explicitly preserves 167-hour and 169-hour DST transition weeks.

Valid range:

```text
0 < EXPOSURE_FRACTION <= 1
```

## Exact frozen spline

```text
KNOT VECTOR =
[0.00, 0.25, 0.50, 0.75, 1.00]

P(x,k) =
max(x-k,0)^3

B0(x) =
x
```

Let:

```text
t1=0
t2=0.25
t3=0.50
t4=0.75
t5=1
```

For j in {1,2,3}:

```text
Bj(x) =
P(x,tj)
-
P(x,t4) * (t5-tj)/(t5-t4)
+
P(x,t5) * (t4-tj)/(t5-t4)
```

Ordered exposure columns:

```text
B0
B1
B2
B3
```

No basis scaling or standardization is permitted.

The knots are fixed prospectively and cannot be optimized, cross-validated, moved or selected from the response.

## Amended models

```text
BASELINE_R1 =
INTERCEPT
+ B0 + B1 + B2 + B3

CONTEXT_R1 =
BASELINE_R1
+ SIDE_HIGH_INDICATOR
+ standardized LEVEL_AGE_WEEKS
+ standardized ACTIVE_LEVEL_COUNT_AT_TARGET_WEEK_START
+ standardized SWEEP_OVERSHOOT_RELATIVE
```

The exposure basis must be exactly identical in both models.

The four context features remain unchanged and frozen.

## Preserved BEPD-09B elements

Unchanged:

```text
C1 CLAIM
T0
RESPONSE
FOUR CONTEXT FEATURES
6 CALENDAR BLOCKS
5 EXPANDING FORWARD FOLDS
NO RANDOM SHUFFLE
NO TARGET-WEEK SPLIT
NO SWEEP-CLUSTER SPLIT
PRIMARY LOGLOSS DELTA
SECONDARY BRIER DELTA
NO AUTOMATIC SUCCESS THRESHOLD
EVENT IID = FALSE
EXPLORATORY HISTORICAL STATUS
FRESH OOS CLOSED
TRADING AUTHORITY = NONE
```

## Synthetic-only qualification surface

Synthetic fixture verifies:

```text
NORMAL WEEK =
168 HOURS

SPRING DST WEEK =
167 HOURS

FALL DST WEEK =
169 HOURS
```

and exact basis vectors at x = 0.25, 0.50, 0.75 and 1.00.

Invalid exposure fractions fail closed.

## Stop

After documentary/programmatic synthetic qualification and persisted-head verification:

```text
STOP FOR HUMAN ADJUDICATION
```
