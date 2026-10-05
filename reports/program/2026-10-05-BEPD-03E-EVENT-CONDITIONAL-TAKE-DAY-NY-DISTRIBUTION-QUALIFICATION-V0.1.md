# BEPD-03E — EVENT-CONDITIONAL TAKE-DAY NY DISTRIBUTION — QUALIFICATION V0.1

**Date:** 2026-10-05  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Qualification persistence parent HEAD:** `8df7cb60b98a36d6c9585409c89b4e5e0cc82c87`  
**Qualification persistence parent TREE:** `bf58319ceca01367a58b679fb4d1bd30a863bd0e`  
**Status:** QUALIFIED / COMPLETE / EVENT_CONDITIONAL_HISTORICAL_FIXED_CORPUS_ONLY

## 1. Verdict

```text
BEPD-03E EVENT-CONDITIONAL TAKE-DAY NY DISTRIBUTION =
PASS

RESULT =
PERSISTED

BEPD-03E INDEPENDENT BREAKER =
PASS

BEPD-03D REGRESSION =
PASS

BEPD-03C REGRESSION =
PASS

BEPD-03B REGRESSION =
PASS

BEPD-03A REGRESSION =
PASS

M05 GENERALIZATION UNCERTAINTY =
BLOCKED
```

No occurrence-rate interpretation, cross-product, ranking, significance test, bootstrap, predictive interpretation or response analysis was executed.

## 2. Exact pre-result execution identity

```text
EXECUTED HEAD =
c7e81ed7725c507fb1cfddfaf4e472ea552fb052

EXECUTED TREE =
3ccd855ec200ef3d1a7b2e1fbf26a76c09cfca68

RUN_ID =
7e084afff3db600ec1e10ec83274fb7c54fdacae16dc0d75f59fbfe98e43449f
```

Source BEPD-02 run:

```text
68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821
```

## 3. Bound implementation identities

```text
HUMAN AUTHORIZATION =
e6e91abc1449ecc55f2241446e80da657148ca8f

IMPLEMENTATION CONTRACT =
5a4aa7f22abd68e47fe67b888314a33d0128530a

CALCULATOR =
98e025b430a051fa0b6eb7c55dd72dbfddd276eb

FROZEN BREAKER CONTRACT =
abb40d40299452fd6104690d640689c716973fd9

EXECUTABLE BREAKER =
c10c3c052ac28bf14491c3b4cd5dba3dd2c377ea
```

## 4. Persisted result identities

```text
RESULT.json
Git blob =
705eb9270b7926184cca44b6eaa40905cf9bd91c

SHA256 =
0b38561f0ff5a175f0860a84b77885f71919b9a63ef44b4020c4de338ae539be

BYTES =
2489
```

```text
RUN_MANIFEST.json
Git blob =
a10943768e373da08f36315cec88ee00fcecd953

SHA256 =
5fb1fb13901355fdd16f08e87b8223f18996e3470d9ef29a40610ded28b15333

BYTES =
1782
```

Persistence commits:

```text
RESULT COMMIT =
95c7ead92269ae096f25f9d4ccf692d5e75f2b88

MANIFEST COMMIT =
8df7cb60b98a36d6c9585409c89b4e5e0cc82c87
```

Concurrent non-BEPD branch activity occurred during local push attempts. Every retry was preceded by fresh BEPD identity checks. The final canonical result and manifest were persisted through GitHub without changing their qualified bytes.

## 5. Population and denominator

```text
POPULATION =
qualified EVENT_LEDGER rows

UNIT =
one LEVEL_SWEEP_EVENT

CONDITION =
sweep already observed

TOTAL SWEEP EVENTS =
472

DENOMINATOR =
472 EVENT_LEDGER events

LEVEL_WEEK_OPPORTUNITY DENOMINATOR =
NOT USED
```

This is not an occurrence rate.

## 6. V06 — TAKE_DAY_NY

Canonical preregistered order only:

```text
SUNDAY_OPEN
event_count = 70
conditional fraction = 70/472
conditional event share = 0.148305084745762712

MONDAY
event_count = 140
conditional fraction = 140/472
conditional event share = 0.296610169491525424

TUESDAY
event_count = 73
conditional fraction = 73/472
conditional event share = 0.154661016949152542

WEDNESDAY
event_count = 75
conditional fraction = 75/472
conditional event share = 0.158898305084745763

THURSDAY
event_count = 59
conditional fraction = 59/472
conditional event share = 0.125000000000000000

FRIDAY
event_count = 55
conditional fraction = 55/472
conditional event share = 0.116525423728813559
```

These are event-conditional shares only.

They do not estimate the probability that a sweep will occur on a given day.

## 7. Reconciliation

```text
70 + 140 + 73 + 75 + 59 + 55 =
472

TOTAL EVENT_LEDGER EVENTS =
472

SUM EXACT CONDITIONAL FRACTIONS =
1

SUM 18-DECIMAL SHARES =
1.000000000000000000

ABSOLUTE DECIMAL ERROR =
0.000000000000000000

FROZEN TOLERANCE =
0.000000000000000003
```

No event was suppressed or duplicated.

## 8. Timezone and DST qualification

```text
TIMESTAMP SOURCE =
take_h1_close_utc

TIMEZONE =
America/New_York

RUNTIME =
zoneinfo
```

The breaker independently verified DST transition probes for:

```text
2024-03-10 spring-forward
2024-11-03 fall-back
```

and verified the frozen mapping:

```text
Sunday   → SUNDAY_OPEN
Monday   → MONDAY
Tuesday  → TUESDAY
Wednesday→ WEDNESDAY
Thursday → THURSDAY
Friday   → FRIDAY

Saturday →
FAIL CLOSED
```

All real EVENT_LEDGER rows mapped into the six preregistered categories.

## 9. Dependence semantics

```text
EVENT != IID OBSERVATION

sweep_cluster_id =
DEPENDENCE / PROVENANCE KEY

target_week_id =
DEPENDENCE / PROVENANCE KEY

MULTIPLE LEVEL EVENTS IN SAME SWEEP CLUSTER =
DEPENDENT BY CONSTRUCTION

MULTIPLE EVENTS IN SAME TARGET WEEK =
DEPENDENT
```

No IID inference was performed.

## 10. Persisted-head qualification evidence

From a clean checkout with `core.autocrlf=false` at the persisted result/manifest HEAD:

```text
BEPD_03E_TAKE_DAY_NY_DISTRIBUTION_BREAKER_PASS
BEPD_03D_LEVEL_AGE_OCCURRENCE_MAP_BREAKER_PASS
BEPD_03C_CALENDAR_OCCURRENCE_MAP_BREAKER_PASS
BEPD_03B_GLOBAL_OCCURRENCE_BASELINE_BREAKER_PASS
BEPD_03A_OCCURRENCE_MEASUREMENT_BREAKER_PASS

BEPD03E_PERSISTED_HEAD_REBREAK_PASS
```

Canonical byte identities were reverified:

```text
RESULT SHA256 =
0b38561f0ff5a175f0860a84b77885f71919b9a63ef44b4020c4de338ae539be

RUN_MANIFEST SHA256 =
5fb1fb13901355fdd16f08e87b8223f18996e3470d9ef29a40610ded28b15333
```

## 11. Explicit non-claims

BEPD-03E does not establish:

```text
an occurrence rate by weekday
a future sweep probability by weekday
a best day
an optimal trading day
statistical significance
stationarity
predictive information
causation
weekday edge
strategy validity
PnL
trading authority
```

Observed differences remain event-conditional historical timing shares only.

## 12. Authority boundary

```text
BEPD-03E V06 TAKE_DAY_NY =
QUALIFIED / COMPLETE

BEPD-03A PREREGISTERED DESCRIPTIVE VIEW SET V00–V06 =
MEASURED FOR CURRENT SCOPE

TAKE-DAY CROSS-PRODUCTS =
NOT AUTHORIZED

M05 =
BLOCKED

RESPONSE MAP =
NOT AUTHORIZED

OCCURRENCE × RESPONSE =
NOT AUTHORIZED

PREDICTIVE TEST =
NOT AUTHORIZED

EDGE / STRATEGY / BACKTEST / PNL =
NOT AUTHORIZED
```

STOP.

Any Response Map, Occurrence × Response analysis, predictive claim or strategy research requires a distinct human authorization.
