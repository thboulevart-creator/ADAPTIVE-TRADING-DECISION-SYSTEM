# BEPD-08C — INTERNAL / EXTERNAL TARGET-WEEK-CLOSE DISTANCE DECOMPOSITION — QUALIFICATION V0.1

## Verdict

```text
BEPD-08C =
QUALIFIED_FOR_HUMAN_ADOPTION

HUMAN ADOPTION =
NOT AUTOMATIC

REAL INTERNAL DISTANCE RESULT =
NOT PRODUCED

REAL EXTERNAL DISTANCE RESULT =
NOT PRODUCED

REAL CONDITIONAL EXECUTION AUTHORITY =
NONE
```

## Qualified identities

```text
HUMAN AUTHORIZATION =
c47d2cc172b2f624037d333a0282dc1e8760421f

DECOMPOSITION CONTRACT =
dc767d77b8f0c8cf89f6d87e9a4cd2401dd0b42e

FROZEN PRE-RESULT BREAKER =
13ad7dba0d4e83036ea1f40b47f1a0a8d1f40bb8

PRE-RESULT FREEZE =
e4d6ebb35147f8cb884dbe569197236ed34251da
```

## Frozen close-side semantics

```text
close_displacement > 0
→ CLOSE_SIDE = INTERNAL

close_displacement < 0
→ CLOSE_SIDE = EXTERNAL

close_displacement = 0
→ CLOSE_SIDE = EXACT_LEVEL
```

`EXACT_LEVEL` belongs to neither INTERNAL nor EXTERNAL.

## Critical non-equivalence

```text
same_week_reintegration =
PATH / EVENT HISTORY PROPERTY

CLOSE_SIDE =
TARGET-WEEK TERMINAL CLOSE POSITION
RELATIVE TO THE SWEPT LEVEL

SAME-WEEK REINTEGRATION
!=
TARGET-WEEK CLOSE SIDE
```

Neither `same_week_reintegration`, `reintegration_h1_close_utc`, nor HIGH/LOW may construct the close-side partition.

## Frozen population invariants

```text
TOTAL N = 472
INTERNAL N = 207
EXTERNAL N = 265
EXACT_LEVEL N = 0

207 + 265 + 0 = 472

INTERNAL FRACTION =
207/472 =
0.438559322033898305

EXTERNAL FRACTION =
265/472 =
0.561440677966101695
```

The partition is mutually exclusive and collectively exhaustive including EXACT_LEVEL.

## Frozen distance semantics

```text
D_CLOSE =
abs(close_displacement)

D_INTERNAL =
D_CLOSE conditional on close_displacement > 0

D_EXTERNAL =
D_CLOSE conditional on close_displacement < 0

D_INTERNAL >= 0
D_EXTERNAL >= 0

UNIT =
USTECH_PRICE_UNITS_AS_PERSISTED
```

## Frozen future dual surface

For each of INTERNAL and EXTERNAL:

```text
N
MINIMUM
MAXIMUM
MEAN
MEDIAN
P01
P05
P10
P25
P50
P75
P90
P95
P99
ZERO_COUNT
ZERO_FRACTION
EMPIRICAL_CDF
```

with:

```text
QUANTILE METHOD =
HYNDMAN-FAN TYPE 7

P50 =
MEDIAN

ECDF =
EXACT / UNSMOOTHED / UNBINNED

CANONICAL SCALAR OUTPUT =
18-DECIMAL ROUND_HALF_EVEN
```

## Outcome-conditioning boundary

```text
CLOSE_SIDE =
OUTCOME-CONDITIONING VARIABLE

CLOSE_SIDE =
NOT KNOWN AT INITIAL SWEEP

CLOSE_SIDE != EX-ANTE PREDICTOR
```

Therefore future INTERNAL/EXTERNAL distance distributions remain descriptive and cannot be used as an ex-ante trading rule without a separately qualified predictive layer.

## Breaker qualification

```text
BREAKER CASES =
32 / 32 PRESENT

EXPECTED OUTCOME =
HARD_FAIL FOR ALL 32
```

Coverage includes wrong identities, wrong classification variables, sign reversal, zero misclassification, row dropping, overlapping or non-exhaustive partitioning, market reconstruction, AP0/H1 read, negative/signed conditional distance, numerical-method drift, subgroup/threshold search, TP/SL laundering, outcome-to-predictor laundering, IID, prediction, edge, strategy and trading-authority laundering.

## No real conditional result exposed

```text
REAL INTERNAL DISTANCE DISTRIBUTION =
NOT EXECUTED

REAL EXTERNAL DISTANCE DISTRIBUTION =
NOT EXECUTED

REAL CONDITIONAL AGGREGATION =
NOT EXECUTED

INTERNAL vs EXTERNAL COMPARATIVE TEST =
NOT EXECUTED
```

## Scientific status

```text
HISTORICAL CORPUS =
ALREADY EXPOSED

ANALYSIS STATUS =
EXPLORATORY_ONLY

GENERALIZATION =
NOT_ESTABLISHED

CONFIRMATORY GENERALIZATION =
FRESH_OOS_EVIDENCE_REQUIRED

PREDICTION =
NO

CAUSATION =
NOT ESTABLISHED

EDGE =
NO

STRATEGY VALIDATION =
NO

TRADING AUTHORITY =
NONE
```

## Terminal state

```text
BEPD-08C =
QUALIFIED_FOR_HUMAN_ADOPTION

NEXT REQUIRED ACTION =
HUMAN ADJUDICATION OF BEPD-08C

AFTER ADOPTION ONLY =
BEPD-08D —
FIRST REAL INTERNAL / EXTERNAL
TARGET-WEEK-CLOSE DISTANCE DISTRIBUTIONS
+ TECHNICAL QUALIFICATION

STOP.
```
