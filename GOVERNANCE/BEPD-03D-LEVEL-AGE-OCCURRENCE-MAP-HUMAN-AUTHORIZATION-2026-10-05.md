# BEPD-03D — LEVEL AGE OCCURRENCE MAP V0.1 — HUMAN AUTHORIZATION — 2026-10-05

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Authorization parent HEAD:** `ebf4c2ab996146582bf8f8b06f03095060a9415e`  
**Authorization parent TREE:** `3a39d0ffe443065e89c4a0d523cd4919e09d23f8`

## 1. Human authorization

```text
BEPD-03D — LEVEL AGE OCCURRENCE MAP V0.1

STATUS =
HUMAN_AUTHORIZED
```

Authorized question:

> How does the historical fixed-corpus Weekly sweep occurrence proportion distribute descriptively according to level age at the start of the target week?

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

BEPD-03C RESULT =
809fa76f82bbbe0311a6c538378eed2a22c77fe0

BEPD-03C RUN MANIFEST =
02acd5a81808119c9bb3896f4be34ca977eb3839

BEPD-03C QUALIFICATION =
fd3b0caa97361e61e81510a2e69f0fbeb25cbe12
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

## 4. Authorized dimension only

```text
V05 — LEVEL_AGE_BAND

SOURCE VARIABLE =
level_age_weeks
```

Frozen categories and boundaries:

```text
AGE_1       = 1
AGE_2       = 2
AGE_3_4     = 3..4
AGE_5_8     = 5..8
AGE_9_16    = 9..16
AGE_17_32   = 17..32
AGE_33_64   = 33..64
AGE_65_PLUS = >=65
```

No category may be added, removed, merged, split or redefined after result exposure.

## 5. Authorized cell outputs

For every preregistered age bin:

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

All eight bins must be emitted, including zero-event and low-support bins.

## 6. Interpretation and dependence

```text
RESULT TYPE =
HISTORICAL_FIXED_CORPUS_DESCRIPTIVE_AGE_HETEROGENEITY

OPPORTUNITY ROW != IID OBSERVATION

DEPENDENCE KEY =
target_week_id

MULTIPLE ACTIVE LEVELS IN SAME TARGET WEEK =
STRUCTURALLY DEPENDENT

SAME LEVEL ACROSS MULTIPLE TARGET WEEKS =
TEMPORAL REPEATED MEASURE

M05 GENERALIZATION UNCERTAINTY =
BLOCKED
```

## 7. Canonical ordering

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

Result-based sorting is forbidden.

## 8. Explicit prohibitions

Not authorized:

```text
age-bin modification
new age thresholds
ranking
best/worst
AGE × SIDE
AGE × MONTH
AGE × YEAR
AGE × EARLY/LATE
AGE × TAKE DAY
any cross-product
reopening/modifying BEPD-03C calendar results
significance tests
p-values
generalization intervals
bootstrap
M05 activation
causal interpretation
predictive interpretation
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

- replay BEPD-03A, BEPD-03B and BEPD-03C breakers;
- freeze BEPD-03D implementation semantics;
- freeze BEPD-03D qualification breaker without encoding discovered age-bin market values.

After calculation:

- independently recompute all eight bins from the bound opportunity ledger;
- verify exact boundary semantics;
- verify no age <= 0;
- verify complete row accounting and baseline reconciliation;
- verify no unauthorized dimensions or inference;
- persist only after PASS;
- re-break persisted HEAD;
- STOP.

No TAKE DAY, Response Map, Occurrence × Response or strategy analysis is authorized.
