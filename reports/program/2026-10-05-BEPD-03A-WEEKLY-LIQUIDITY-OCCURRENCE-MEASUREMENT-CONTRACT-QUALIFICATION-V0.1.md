# BEPD-03A — WEEKLY LIQUIDITY OCCURRENCE MEASUREMENT CONTRACT — QUALIFICATION V0.1

**Date:** 2026-10-05  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Qualification persistence parent HEAD:** `eef7090743d453529edaa2b592d3ff1dcab12c1e`  
**Qualification persistence parent TREE:** `e327e00fda3b72d857ad182acec1afc60e5fcac1`  
**Status:** QUALIFIED_CANDIDATE / PASS / HUMAN_ADOPTION_PENDING

## 1. Verdict

```text
BEPD-03A PRE-RESULT OCCURRENCE MEASUREMENT PROTOCOL =
PASS

EXECUTABLE BREAKER =
PASS

EXACT OUTPUT =
BEPD_03A_OCCURRENCE_MEASUREMENT_BREAKER_PASS

PROCESS EXIT CODE =
0

REAL OCCURRENCE RESULTS =
NOT CALCULATED

OCCURRENCE MAP =
NOT PRODUCED
```

PASS means no failure was found within the preregistered protocol / synthetic breaker surface.

It does not mean any occurrence relation has been observed or supported.

## 2. Exact qualified candidate identities

```text
HUMAN AUTHORIZATION =
03d1cf01b41f662280f00c8271bab411b5754b3a

PREREGISTERED DIMENSIONS =
b7ec6a00e3d2281217c30e11d21527b5ce72aef6

OCCURRENCE MEASUREMENT CONTRACT =
e117ddea324dd1b6906bc9eadcf8a5806b8b591a

SMF M05 ACTIVATION RECORD =
53d33074038fa9d971b4672b1d981589da020a1e

FROZEN BREAKER CONTRACT =
d9c3ce44dbc27703cd1cde007a5f806beb01f221

EXECUTABLE BREAKER =
65ecba3e4d3fab7442532252c1eb173582293064
```

Bound raw inputs remain:

```text
LEVEL_WEEK_OPPORTUNITY =
0e97fb3b45bf8510b8531bb733cc155467a2ce49

EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2

RUN_MANIFEST =
ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5

BEPD-02 RUN_ID =
68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821
```

No line-level real occurrence outcome values were consumed by the BEPD-03A executable breaker.

## 3. Primary historical estimand

The preregistered primary descriptive estimand is:

```text
GLOBAL_WEEKLY_LEVEL_SWEEP_OCCURRENCE

UNIT =
one eligible LEVEL_WEEK_OPPORTUNITY row

Y_i =
1 if swept_this_week = true
0 otherwise

NUMERATOR =
sum(Y_i)

DENOMINATOR =
count(all eligible LEVEL_WEEK_OPPORTUNITY rows)

ESTIMATOR =
sum(Y_i) / N
```

Each eligible level-week opportunity has equal weight.

The estimator is explicitly:

```text
RATIO OF TOTAL EVENTS TO TOTAL OPPORTUNITIES
```

and not:

```text
MEAN OF WEEKLY RATES
```

## 4. Dependence semantics

```text
OPPORTUNITY ROW != IID OBSERVATION

DEPENDENCE KEY =
target_week_id

MULTIPLE LEVELS IN SAME TARGET WEEK =
STRUCTURALLY DEPENDENT

SAME LEVEL ACROSS MULTIPLE WEEKS =
TEMPORAL REPEATED MEASURE UNTIL CONSUMPTION/CENSORING
```

No opportunity-row IID inference is authorized.

## 5. Mandatory views preregistered before results

Initial occurrence reporting is marginal-only.

```text
V00 = GLOBAL ALL SIDES
V01 = SIDE: HIGH / LOW
V02 = TARGET MONTH: 1..12
V03 = TARGET MONTH POSITION: EARLY_01_15 / LATE_16_EOM
V04 = TARGET YEAR
V05 = LEVEL AGE BAND
V06 = TAKE DAY NY — EVENT-CONDITIONAL ONLY
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

The initial map authorizes zero cross-products.

Every preregistered group must be reported, including zero-event or low-support cells.

Sorting by result and best/worst labels are forbidden.

## 6. Calendar semantics

Pre-event occurrence context:

```text
TARGET MONTH =
month(target_week_id)

TARGET MONTH POSITION =
EARLY if day(target_week_id) <= 15
LATE if day(target_week_id) >= 16

TARGET YEAR =
year(target_week_id)

AGE BAND =
function(level_age_weeks)
```

These values are available before the target-week outcome.

By contrast:

```text
TAKE DAY NY
```

is outcome-conditional and may not be presented as a pre-event occurrence denominator.

## 7. Uncertainty semantics

### Fixed bound historical corpus

```text
STATE =
EXACT_DESCRIPTIVE_SUMMARY

INFERENTIAL SAMPLING INTERVAL =
NOT REQUIRED / NOT AUTHORIZED BY DEFAULT
```

The observed historical numerator and denominator are fixed quantities in the bound BEPD-02 corpus.

A sampling interval must not be used to imply a future population without a separate generalization claim.

### Process / future generalization

Selected candidate method family:

```text
SMF M05
SCHEME = MOVING_BLOCK

RESAMPLING UNIT =
ordered target_week_id clusters

RULE =
all opportunity rows belonging to a selected week move together

REPLICATE ESTIMATOR =
ratio of summed sweep numerators
/
summed opportunity denominators
```

Current activation state:

```text
BLOCKED
```

Blockers:

```text
UNRESOLVED_NONSTATIONARITY_STATUS

MATERIAL BOOTSTRAP PARAMETERS
NOT HUMAN-ADJUDICATED

RATIO-OF-SUMS MOVING-BLOCK EXECUTABLE
NOT SEPARATELY QUALIFIED
```

Therefore no bootstrap interval may be produced automatically.

No IID bootstrap, opportunity-row bootstrap or naive binomial fallback is permitted.

## 8. Multiplicity / search control

The first occurrence map is:

```text
DESCRIPTIVE
MARGINAL-ONLY
NO P-VALUES
NO SIGNIFICANCE LABELS
NO CROSS-PRODUCTS
NO RANKING
COMPLETE REPORTING
```

Differences between cells remain descriptive heterogeneity only.

A later hypothesis test requires a new claim, method activation, multiplicity policy and authority.

## 9. Breaker qualification

Thirty frozen synthetic / documentary cases cover:

```text
event count != occurrence rate
pooled ratio != mean weekly rate
opportunity rows != IID
same-week dependence
repeated-level dependence
side masking
unauthorized HIGH/LOW testing
outcome-derived calendar context
month-position drift
year suppression
post-hoc age bins
age-bin boundary drift
take-day occurrence laundering
cross-product fishing
zero-event suppression
low-support suppression
result sorting
ranking language
historical-to-future laundering
unauthorized fixed-corpus CI
row bootstrap
IID fallback
nonstationary M05 activation
unadjudicated bootstrap parameters
SMF runtime scope laundering
null/adverse cell deletion
descriptive-to-predictive laundering
occurrence/response conflation
edge laundering
result-execution authority expansion
```

Observed:

```text
BEPD_03A_OCCURRENCE_MEASUREMENT_BREAKER_PASS
BEPD03A_BREAKER_EXIT_CODE=0
```

## 10. Human decision state

```text
BEPD-03A CONTRACT =
QUALIFIED CANDIDATE

PREREGISTERED DIMENSIONS =
QUALIFIED CANDIDATE

BREAKER =
GREEN

HUMAN ADOPTION =
NOT YET SUPPLIED
```

The qualified candidate may not silently become binding policy.

## 11. Authority boundary

```text
REAL OCCURRENCE CALCULATION =
NOT AUTHORIZED

BEPD-03B =
NOT OPEN

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

EDGE / STRATEGY / BACKTEST / PNL =
NOT AUTHORIZED

PAPER / BROKER / LIVE / CAPITAL =
NOT AUTHORIZED
```

STOP before BEPD-03B.
