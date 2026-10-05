# BEPD-03B — GLOBAL WEEKLY LIQUIDITY OCCURRENCE BASELINE — QUALIFICATION V0.1

**Date:** 2026-10-05  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Qualification persistence parent HEAD:** `799c24d493531d604d5e194b175dad3934d1ee0b`  
**Qualification persistence parent TREE:** `32296462cc7f3259d7395c43a0958f0b361058af`  
**Status:** QUALIFIED / COMPLETE / DESCRIPTIVE_FIXED_CORPUS_ONLY

## 1. Verdict

```text
BEPD-03B GLOBAL WEEKLY LIQUIDITY OCCURRENCE BASELINE =
PASS

RESULT =
PERSISTED

BEPD-03B INDEPENDENT BREAKER =
PASS

BEPD-03A REGRESSION =
PASS

M05 GENERALIZATION UNCERTAINTY =
BLOCKED

POST-BASELINE SEGMENTATION =
NOT AUTHORIZED / NOT EXECUTED
```

The result is a historical fixed-corpus descriptive proportion only.

It is not a future probability, predictive claim, edge or strategy result.

## 2. Exact execution identity

```text
EXECUTED HEAD =
48037e94b9df2dc7fa93b350bcb86f8cd3187484

EXECUTED TREE =
dec6dddf6326579fef4672f1b228189adbade6e6

RUN_ID =
85f19aca696736c3a832715bdf0ef4876e6f025bb612d642e7651aa674a7fd3a

SOURCE BEPD-02 RUN_ID =
68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821
```

## 3. Bound implementation and breaker identities

```text
HUMAN AUTHORIZATION =
506e75c4c88a04019ae71156dbebf3c8f02d5d2b

IMPLEMENTATION CONTRACT =
a949cdf6b43a20a981e4a1fb4667de16f3b3c260

CALCULATOR =
7f8cebd92437ec724c8ebe81f0e9befdccc7dba4

FROZEN BREAKER CONTRACT =
a559aae07f7c5471949c9c5de6cfa6fdcaa20926

EXECUTABLE BREAKER =
a63f186d0ef88d4dbef81e873cd4cf26beebf686
```

BEPD-03A remained bound to:

```text
MEASUREMENT CONTRACT =
e117ddea324dd1b6906bc9eadcf8a5806b8b591a

M05 ACTIVATION RECORD =
53d33074038fa9d971b4672b1d981589da020a1e

HUMAN ADJUDICATION =
b796fd69a9b40c0397cc89db5be755d59974b1fe
```

## 4. Persisted result identities

```text
RESULT.json
Git blob =
a2d083b67415b6cb8aa92395d702d1ab558dd4c1

SHA256 =
ce7393cc50a36030ed5819459a06ecda9e33f66484744324542d4fe378408750

BYTES =
1519
```

```text
RUN_MANIFEST.json
Git blob =
98abfece6796ecfb355714c31bcf0126a28729c9

SHA256 =
f9598e525fd8dcba30381443989544d9228d3407ceb131ff21f40d7f11e1a7b2

BYTES =
1598
```

Persistence commit:

```text
799c24d493531d604d5e194b175dad3934d1ee0b
```

Persistence tree:

```text
32296462cc7f3259d7395c43a0958f0b361058af
```

## 5. Global baseline — primary descriptive result

```text
VIEW =
GLOBAL_ALL_SIDES

ELIGIBLE TARGET WEEKS =
259

UNIQUE LEVELS REPRESENTED =
518

OPPORTUNITIES =
7213

EVENTS =
472

EXACT FRACTION =
472 / 7213

HISTORICAL FIXED-CORPUS OCCURRENCE PROPORTION =
0.065437404685983641
```

This value is:

```text
total swept opportunities
/
total eligible opportunities
```

It is not the mean of weekly rates.

## 6. Mandatory HIGH view

```text
VIEW =
HIGH

ELIGIBLE TARGET WEEKS =
259

UNIQUE LEVELS REPRESENTED =
259

OPPORTUNITIES =
1573

EVENTS =
258

EXACT FRACTION =
258 / 1573

HISTORICAL FIXED-CORPUS OCCURRENCE PROPORTION =
0.164017800381436745
```

This is a mandatory descriptive side view.

No HIGH-vs-LOW ranking, superiority claim or hypothesis test is authorized.

## 7. Mandatory LOW view

```text
VIEW =
LOW

ELIGIBLE TARGET WEEKS =
259

UNIQUE LEVELS REPRESENTED =
259

OPPORTUNITIES =
5640

EVENTS =
214

EXACT FRACTION =
214 / 5640

HISTORICAL FIXED-CORPUS OCCURRENCE PROPORTION =
0.037943262411347518
```

This is a mandatory descriptive side view.

No HIGH-vs-LOW ranking, superiority claim or hypothesis test is authorized.

## 8. Count parity

The independent breaker verified:

```text
GLOBAL OPPORTUNITIES =
HIGH OPPORTUNITIES + LOW OPPORTUNITIES

7213 =
1573 + 5640
```

```text
GLOBAL EVENTS =
HIGH EVENTS + LOW EVENTS

472 =
258 + 214
```

```text
GLOBAL UNIQUE LEVELS =
HIGH UNIQUE LEVELS + LOW UNIQUE LEVELS

518 =
259 + 259
```

The GLOBAL target-week set equals the union of the HIGH and LOW target-week sets.

All source opportunity rows were accounted for exactly once by side.

## 9. Dependence interpretation

```text
OPPORTUNITY ROW != IID OBSERVATION

DEPENDENCE KEY =
target_week_id

MULTIPLE ACTIVE LEVELS IN SAME TARGET WEEK =
STRUCTURALLY DEPENDENT
```

Therefore the descriptive proportions above are not accompanied by naive binomial inference.

## 10. M05 remains blocked

```text
M05 GENERALIZATION UNCERTAINTY =
BLOCKED
```

No:

- confidence interval;
- bootstrap;
- p-value;
- significance test;
- future-probability interval

was computed.

The three BEPD-03A blockers remain unchanged.

## 11. Independent qualification

The breaker recomputed the three views directly from the bound `LEVEL_WEEK_OPPORTUNITY` ledger and cross-checked event counts against `EVENT_LEDGER`.

Observed:

```text
BEPD_03B_GLOBAL_OCCURRENCE_BASELINE_BREAKER_PASS
BEPD03B_BREAKER_EXIT_CODE=0
```

After persistence:

```text
BEPD_03B_GLOBAL_OCCURRENCE_BASELINE_BREAKER_PASS
BEPD_03A_OCCURRENCE_MEASUREMENT_BREAKER_PASS
BEPD03A_PERSISTED_REGRESSION_EXIT=0
```

PASS establishes calculation/provenance parity only.

## 12. Explicit non-claims

BEPD-03B does not establish:

```text
future sweep probability
statistical significance
stationarity
generalization uncertainty
HIGH superiority
LOW inferiority
calendar seasonality
age effect
predictive information
response magnitude
edge
strategy
PnL
trading authority
```

The observed HIGH and LOW proportions may not be ranked or interpreted causally under this authorization.

## 13. Authority boundary

```text
GLOBAL FIXED-CORPUS BASELINE =
QUALIFIED / COMPLETE

HIGH / LOW MANDATORY DESCRIPTIVE VIEWS =
QUALIFIED / COMPLETE

CALENDAR OCCURRENCE MAP =
NOT AUTHORIZED

TARGET MONTH / EARLY-LATE / YEAR =
NOT EXECUTED

LEVEL AGE BAND =
NOT EXECUTED

TAKE DAY NY =
NOT EXECUTED

M05 =
BLOCKED

RESPONSE MAP =
NOT AUTHORIZED

OCCURRENCE × RESPONSE =
NOT AUTHORIZED

EDGE / STRATEGY / BACKTEST / PNL =
NOT AUTHORIZED
```

STOP.

Any additional segmentation, uncertainty/generalization analysis or response analysis requires a separate human authorization.
