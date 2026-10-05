# BEPD-03B — GLOBAL WEEKLY LIQUIDITY OCCURRENCE BASELINE V0.1 — HUMAN AUTHORIZATION — 2026-10-05

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Authorization parent HEAD:** `139b4ff2b420aab4b07d8a845e9a358263398525`  
**Authorization parent TREE:** `f392f0f10d770c2db27085e601d66c953e271fee`

## 1. Human authorization

```text
BEPD-03B — GLOBAL WEEKLY LIQUIDITY OCCURRENCE BASELINE V0.1

STATUS =
HUMAN_AUTHORIZED
```

Authorized question:

> In the fixed BEPD-02 historical corpus, among all eligible Weekly-level × target-week opportunities, what fraction were consumed during the target week?

## 2. Bound BEPD-03A policy

```text
PREREGISTERED DIMENSIONS =
b7ec6a00e3d2281217c30e11d21527b5ce72aef6

MEASUREMENT CONTRACT =
e117ddea324dd1b6906bc9eadcf8a5806b8b591a

M05 ACTIVATION RECORD =
53d33074038fa9d971b4672b1d981589da020a1e

BREAKER CONTRACT =
d9c3ce44dbc27703cd1cde007a5f806beb01f221

EXECUTABLE BREAKER =
65ecba3e4d3fab7442532252c1eb173582293064

HUMAN ADJUDICATION =
b796fd69a9b40c0397cc89db5be755d59974b1fe

QUALIFICATION =
09b5e6f38b7a7e2f6abe502328458995a3e5d79a
```

## 3. Bound BEPD-02 inputs

```text
LEVEL_LEDGER =
c50cea414a95e498199fbe0c426f4d246a1f1f99

EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2

LEVEL_WEEK_OPPORTUNITY =
0e97fb3b45bf8510b8531bb733cc155467a2ce49

RUN_MANIFEST =
ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5

BEPD-02 RUN_ID =
68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821
```

## 4. Authorized calculation

Primary:

```text
NUMERATOR =
count LEVEL_WEEK_OPPORTUNITY rows where swept_this_week=true

DENOMINATOR =
count all eligible LEVEL_WEEK_OPPORTUNITY rows

ESTIMATOR =
NUMERATOR / DENOMINATOR
```

Mandatory outputs:

```text
GLOBAL ALL SIDES
HIGH
LOW
```

For each output, persist only:

```text
eligible target-week count
unique level count
opportunity count
event count
historical fixed-corpus occurrence proportion
```

## 5. Binding interpretation

```text
RESULT TYPE =
HISTORICAL FIXED-CORPUS DESCRIPTIVE PROPORTION

OPPORTUNITY ROW != IID OBSERVATION

DEPENDENCE KEY =
target_week_id

MULTIPLE ACTIVE LEVELS IN SAME WEEK =
STRUCTURALLY DEPENDENT
```

No future-probability interpretation is authorized.

## 6. M05 remains blocked

```text
M05 GENERALIZATION UNCERTAINTY =
BLOCKED
```

No bootstrap, inferential confidence interval or fallback interval is authorized.

## 7. Explicit prohibitions

Not authorized:

```text
TARGET MONTH
EARLY/LATE MONTH
TARGET YEAR segmentation
LEVEL AGE BAND
TAKE DAY NY
cross-products
free segmentation
HIGH-vs-LOW ranking or hypothesis test
best/worst labels
p-values
significance tests
generalization intervals
bootstrap
M05 activation
future probability
Response Map
Occurrence × Response
predictive research
edge
strategy
backtest / PnL / sizing
paper / broker / live / capital
```

## 8. Fail-closed and stop

Before result exposure:

- replay the frozen BEPD-03A breaker;
- freeze the BEPD-03B implementation/qualification semantics.

After calculation:

- independently verify numerator, denominator, ratio and HIGH/LOW/global count parity;
- verify no rows were excluded;
- verify no weekly-rate averaging was substituted;
- verify provenance;
- persist only after PASS;
- re-break persisted HEAD;
- STOP.

No Calendar Occurrence Map or other downstream segmentation is authorized.
