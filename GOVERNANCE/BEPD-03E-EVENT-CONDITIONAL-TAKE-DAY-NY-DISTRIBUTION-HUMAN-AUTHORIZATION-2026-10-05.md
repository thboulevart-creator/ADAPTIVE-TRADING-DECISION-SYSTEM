# BEPD-03E — EVENT-CONDITIONAL TAKE-DAY NY DISTRIBUTION V0.1 — HUMAN AUTHORIZATION — 2026-10-05

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Authorization parent HEAD:** `78047f01ad6a2c7dfaeb7dd1e5023cbad630abd0`  
**Authorization parent TREE:** `9b6195667ace368123fcca52d5a91d75351958fa`

## 1. Human authorization

```text
BEPD-03E — EVENT-CONDITIONAL TAKE-DAY NY DISTRIBUTION V0.1

STATUS =
HUMAN_AUTHORIZED
```

Authorized question:

> Among already-observed historical sweep events, how is the take timing distributed by local weekday in America/New_York?

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

BEPD-03B QUALIFICATION =
e88bcce2d3256a9e374e76cfb5e9ebc641316d56

BEPD-03C QUALIFICATION =
fd3b0caa97361e61e81510a2e69f0fbeb25cbe12

BEPD-03D QUALIFICATION =
c7151af0bd7acce71f5d7f0e1e059c6f141c57d1
```

## 3. Bound source

```text
EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2

BEPD-02 RUN MANIFEST =
ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5

SOURCE UNIT =
one LEVEL_SWEEP_EVENT
```

## 4. Authorized dimension only

```text
V06 — TAKE_DAY_NY

TIMESTAMP SOURCE =
take_h1_close_utc

TIMEZONE =
America/New_York

DERIVATION =
take_h1_close_utc
→ timezone conversion to America/New_York
→ local weekday
```

Canonical categories:

```text
SUNDAY_OPEN
MONDAY
TUESDAY
WEDNESDAY
THURSDAY
FRIDAY
```

Saturday is fail-closed.

## 5. Population and denominator

```text
POPULATION =
all qualified EVENT_LEDGER rows

CONDITION =
sweep already observed

DENOMINATOR =
count(EVENT_LEDGER rows)

LEVEL_WEEK_OPPORTUNITY DENOMINATOR =
FORBIDDEN
```

For each category:

```text
event_count
conditional_event_share

conditional_event_share =
event_count_in_category / total_EVENT_LEDGER_event_count
```

This is not an occurrence rate.

## 6. Dependence

```text
EVENT != IID OBSERVATION

MULTIPLE LEVEL EVENTS IN SAME SWEEP CLUSTER =
DEPENDENT BY CONSTRUCTION

MULTIPLE EVENTS IN SAME TARGET WEEK =
DEPENDENT

DEPENDENCE / PROVENANCE KEYS =
sweep_cluster_id
target_week_id
```

## 7. Interpretation

```text
RESULT TYPE =
EVENT_CONDITIONAL_HISTORICAL_FIXED_CORPUS_TAKE_TIMING_DISTRIBUTION

TAKE-DAY CONDITIONAL DISTRIBUTION
!=
PRE-EVENT OCCURRENCE CONTEXT

M05 GENERALIZATION UNCERTAINTY =
BLOCKED
```

## 8. Explicit prohibitions

Not authorized:

```text
occurrence rate by take day
LEVEL_WEEK_OPPORTUNITY as take-day denominator
Monday/other-day future sweep probability
TAKE DAY × SIDE
TAKE DAY × MONTH
TAKE DAY × YEAR
TAKE DAY × EARLY/LATE
TAKE DAY × LEVEL AGE
any other cross-product
ranking
best/worst
subgroup selection
significance testing
p-values
generalization interval
bootstrap
M05 activation
causal interpretation
predictive interpretation
Response Map
Occurrence × Response
edge
strategy
backtest / PnL / sizing
paper / broker / live / capital
```

## 9. Fail-closed sequence

Before result exposure:

- replay BEPD-03A, BEPD-03B, BEPD-03C and BEPD-03D breakers;
- freeze BEPD-03E implementation semantics;
- freeze BEPD-03E breaker without encoding discovered market values.

After calculation:

- independently recompute all six categories from EVENT_LEDGER;
- verify timezone and DST behavior;
- fail closed on missing/invalid timestamp or Saturday;
- verify all events are accounted for exactly once;
- verify total category event count equals EVENT_LEDGER row count;
- verify conditional shares reconcile to 1 under the frozen precision rule;
- verify no opportunity denominator, cross-product, ranking or inference;
- persist only after PASS;
- re-break persisted HEAD;
- STOP.

No Response Map, Occurrence × Response or strategy analysis is authorized.
