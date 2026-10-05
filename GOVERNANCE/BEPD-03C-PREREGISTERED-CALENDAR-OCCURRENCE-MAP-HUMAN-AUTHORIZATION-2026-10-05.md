# BEPD-03C — PREREGISTERED CALENDAR OCCURRENCE MAP V0.1 — HUMAN AUTHORIZATION — 2026-10-05

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Authorization parent HEAD:** `a0156f73932f54926d96c5c88a8239671cc271e5`  
**Authorization parent TREE:** `5c9e67ea7859e2274a8dbeb46df3ff90944dbfd2`

## 1. Human authorization

```text
BEPD-03C — PREREGISTERED CALENDAR OCCURRENCE MAP V0.1

STATUS =
HUMAN_AUTHORIZED
```

Authorized question:

> How does the already-defined historical fixed-corpus occurrence proportion distribute descriptively by preregistered target month, early/late target-month position, and target year?

## 2. Bound upstream policy

```text
BEPD-03A PREREGISTERED DIMENSIONS =
b7ec6a00e3d2281217c30e11d21527b5ce72aef6

BEPD-03A MEASUREMENT CONTRACT =
e117ddea324dd1b6906bc9eadcf8a5806b8b591a

BEPD-03A M05 ACTIVATION RECORD =
53d33074038fa9d971b4672b1d981589da020a1e

BEPD-03A HUMAN ADJUDICATION =
b796fd69a9b40c0397cc89db5be755d59974b1fe

BEPD-03B RESULT =
a2d083b67415b6cb8aa92395d702d1ab558dd4c1

BEPD-03B RUN MANIFEST =
98abfece6796ecfb355714c31bcf0126a28729c9

BEPD-03B QUALIFICATION =
e88bcce2d3256a9e374e76cfb5e9ebc641316d56
```

## 3. Bound source ledgers

```text
LEVEL_WEEK_OPPORTUNITY =
0e97fb3b45bf8510b8531bb733cc155467a2ce49

LEVEL_LEDGER =
c50cea414a95e498199fbe0c426f4d246a1f1f99

EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2

BEPD-02 RUN MANIFEST =
ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5
```

## 4. Authorized dimensions only

```text
V02 — TARGET_MONTH =
month(target_week_id)

CATEGORIES =
1..12

V03 — TARGET_MONTH_POSITION =
EARLY_01_15 if day(target_week_id) <= 15
LATE_16_EOM if day(target_week_id) >= 16

V04 — TARGET_YEAR =
year(target_week_id)

YEAR CATEGORIES =
all years represented by eligible opportunity rows, chronological order
```

No cross-product is authorized.

## 5. Authorized cell outputs

For every preregistered cell:

```text
eligible_target_week_count
unique_level_count
opportunity_count
event_count
historical_fixed_corpus_occurrence_proportion
```

Estimator:

```text
event_count / opportunity_count
```

All preregistered cells must be emitted, including zero-event and low-support cells.

## 6. Interpretation

```text
RESULT TYPE =
HISTORICAL_FIXED_CORPUS_DESCRIPTIVE_HETEROGENEITY

OPPORTUNITY ROW != IID OBSERVATION

DEPENDENCE KEY =
target_week_id

M05 GENERALIZATION UNCERTAINTY =
BLOCKED
```

No future-probability or predictive interpretation is authorized.

## 7. Canonical ordering

```text
MONTH =
1 → 12

MONTH POSITION =
EARLY_01_15
LATE_16_EOM

YEAR =
chronological
```

Result-based sorting is forbidden.

## 8. Explicit prohibitions

Not authorized:

```text
MONTH × SIDE
MONTH × AGE
YEAR × MONTH
EARLY/LATE × SIDE
any other cross-product
ranking
best/worst
subgroup selection
significance testing
p-values
generalization CI
bootstrap
M05 activation
causal interpretation
predictive interpretation
LEVEL AGE BAND
TAKE DAY NY
Response Map
Occurrence × Response
edge
strategy
backtest / PnL / sizing
paper / broker / live / capital
```

## 9. Fail-closed sequence

Before result exposure:

- replay BEPD-03A and BEPD-03B breakers;
- freeze BEPD-03C implementation semantics;
- freeze BEPD-03C qualification breaker without encoding discovered market values.

After calculation:

- independently recompute every cell from the bound opportunity ledger;
- verify complete category coverage;
- verify row-accounting parity within each marginal partition;
- verify baseline reconciliation;
- verify no unauthorized output dimensions;
- persist only after PASS;
- re-break persisted HEAD;
- STOP.

No LEVEL AGE, TAKE DAY, Response Map or downstream strategy analysis is authorized.
