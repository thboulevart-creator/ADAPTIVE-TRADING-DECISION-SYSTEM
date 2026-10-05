# BEPD-03A — WEEKLY LIQUIDITY OCCURRENCE MEASUREMENT — HUMAN ADJUDICATION — 2026-10-05

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Adjudication parent HEAD:** `6fc1d67ebc27d5329e4915e58b833ef044631f40`  
**Adjudication parent TREE:** `1a750d3195c7aead0882993eb4d1b1ad71f53ecc`

## 1. Human decision

```text
HUMAN_DECISION = ADOPT
STATUS = HUMAN_ADOPTED / BINDING / FROZEN
```

The human explicitly adopts the following exact objects:

```text
BEPD-03A — PREREGISTERED OCCURRENCE DIMENSIONS V0.1
Git blob =
b7ec6a00e3d2281217c30e11d21527b5ce72aef6

BEPD-03A — WEEKLY LIQUIDITY OCCURRENCE MEASUREMENT CONTRACT V0.1
Git blob =
e117ddea324dd1b6906bc9eadcf8a5806b8b591a

BEPD-03A — SMF M05 OCCURRENCE UNCERTAINTY ACTIVATION RECORD V0.1
Git blob =
53d33074038fa9d971b4672b1d981589da020a1e

BEPD-03A — FROZEN OCCURRENCE MEASUREMENT BREAKER CONTRACT V0.1
Git blob =
d9c3ce44dbc27703cd1cde007a5f806beb01f221

BEPD-03A — EXECUTABLE BREAKER
Git blob =
65ecba3e4d3fab7442532252c1eb173582293064
```

Qualification evidence adopted:

```text
BEPD-03A — WEEKLY LIQUIDITY OCCURRENCE MEASUREMENT CONTRACT QUALIFICATION V0.1
Git blob =
09b5e6f38b7a7e2f6abe502328458995a3e5d79a

QUALIFICATION VERDICT =
PASS
```

## 2. Binding occurrence-estimand semantics

```text
PRIMARY UNIT =
one eligible LEVEL_WEEK_OPPORTUNITY row

NUMERATOR =
count / sum of rows with swept_this_week = true

DENOMINATOR =
all eligible LEVEL_WEEK_OPPORTUNITY rows

ESTIMATOR =
total swept opportunities / total eligible opportunities

MEAN OF WEEKLY RATES =
NOT THE PRIMARY ESTIMATOR
```

## 3. Binding dependence semantics

```text
OPPORTUNITY ROW != IID OBSERVATION

DEPENDENCE KEY =
target_week_id

MULTIPLE ACTIVE LEVELS IN SAME TARGET WEEK =
STRUCTURALLY DEPENDENT

REPEATED SAME LEVEL ACROSS WEEKS =
TEMPORAL REPEATED MEASURE
```

No IID assumption may be introduced silently.

## 4. Binding preregistered dimensions

The initial occurrence-reporting surface is marginal-only and binds:

```text
GLOBAL
HIGH / LOW
TARGET MONTH
TARGET MONTH POSITION
TARGET YEAR
LEVEL AGE BAND
TAKE DAY NY — EVENT-CONDITIONAL ONLY

AUTHORIZED CROSS-PRODUCTS =
NONE
```

Frozen age bands:

```text
AGE_1
AGE_2
AGE_3_4
AGE_5_8
AGE_9_16
AGE_17_32
AGE_33_64
AGE_65_PLUS
```

All preregistered groups must be retained, including zero-event and low-support groups.

Result-based sorting, winner-only reporting and best/worst labeling remain forbidden.

## 5. M05 generalization-uncertainty state

The human explicitly preserves:

```text
M05 GENERALIZATION UNCERTAINTY =
BLOCKED
```

This state remains binding until all of the following are separately closed:

```text
1. NONSTATIONARITY STATUS =
RESOLVED FOR THE CLAIMED RESAMPLING SCOPE

2. MATERIAL BOOTSTRAP PARAMETERS =
SEPARATELY HUMAN-ADJUDICATED

3. RATIO-OF-SUMS MOVING-BLOCK STATISTIC =
SEPARATELY EXECUTABLY QUALIFIED
```

The selected candidate family remains:

```text
SMF M05
SCHEME = MOVING_BLOCK
RESAMPLING UNIT = ordered target_week_id clusters
```

But:

```text
BLOCKED != ACTIVATED
SELECTED CANDIDATE METHOD != AUTHORIZED EXECUTION
```

No IID bootstrap, opportunity-row bootstrap, naive binomial interval or other automatic fallback is permitted.

## 6. Historical-descriptive scope

For the bound historical corpus:

```text
HISTORICAL OCCURRENCE PROPORTION =
EXACT DESCRIPTIVE SUMMARY OF THE BOUND CORPUS
```

This adoption does not turn that descriptor into a future probability, predictive claim, generalization interval or edge claim.

## 7. Explicitly withheld authority

The human explicitly does NOT authorize:

```text
BEPD-03B =
NOT AUTHORIZED

REAL OCCURRENCE CALCULATION =
NOT AUTHORIZED

OCCURRENCE MAP =
NOT AUTHORIZED

RESPONSE MAP =
NOT AUTHORIZED

OCCURRENCE × RESPONSE =
NOT AUTHORIZED

RANKING / BEST PERIOD SEARCH =
NOT AUTHORIZED

PREDICTIVE TEST =
NOT AUTHORIZED

EDGE INFERENCE =
NOT AUTHORIZED

STRATEGY / BACKTEST / PNL / SIZING =
NOT AUTHORIZED

PAPER / BROKER / LIVE / CAPITAL =
NOT AUTHORIZED
```

## 8. Consequence

```text
BEPD-03A =
HUMAN_ADOPTED / BINDING / FROZEN

PRE-RESULT OCCURRENCE MEASUREMENT PROTOCOL =
CLOSED FOR CURRENT SCOPE

M05 GENERALIZATION UNCERTAINTY =
BLOCKED

NEXT FRONTIER =
REQUIRES DISTINCT HUMAN AUTHORIZATION
```

STOP.
