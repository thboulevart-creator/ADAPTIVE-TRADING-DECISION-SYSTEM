# BEPD-06B — HUMAN AUTHORIZATION — 2026-10-06

## Governed target

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

CONTROL =
BEPD-06B — FIRST REAL CONDITIONAL TIME-TO-FIRST-REINTEGRATION DISTRIBUTION + TECHNICAL QUALIFICATION V0.1

HUMAN AUTHORIZATION =
AUTHORIZED
```

Reference observed when this authorization was issued:

```text
REFERENCE HEAD =
a18415170040e83ea98328d6f943d7a41f3301d9

REFERENCE TREE =
41cfa10d51d2424355d34bb83f0242306f619514
```

A fresh preflight is mandatory before mutation or execution.

## Binding prior authority

```text
BEPD-06A FINAL HUMAN ADJUDICATION =
86d67aa938c8b6871528f085e76e9a82632fa53b

BEPD-06A CONDITIONAL TIMING CONTRACT =
a15278a9491e75096585ab576b548b965ee6a0e6

BEPD-06A FROZEN PRE-RESULT BREAKER =
02a64983b4ce75b0f798f1b9639bf8d1a4c41605

BEPD-06A PRE-RESULT FREEZE =
6cb6b5bac0848d8b24f035a1527216bf71843bbd

BEPD-02 EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2
```

Any material identity divergence = FAIL CLOSED.

## Authorized real estimand

One first real conditional timing distribution only:

```text
BASE POPULATION = 472
SAME_WEEK_REINTEGRATION TRUE = 370
SAME_WEEK_REINTEGRATION FALSE = 102
TIMING POPULATION = 370
CONDITION = same_week_reintegration = TRUE
T0 = take_h1_close_utc
T1 = reintegration_h1_close_utc
T1 > T0 REQUIRED
elapsed_utc_hours = (T1 - T0) / 1 hour
CLOCK = UTC ELAPSED HOURS
```

The 102 non-reintegration events remain provenance-only as NOT_OBSERVED_WITHIN_TARGET_WEEK and receive no duration.

Authorized future real result surface:

```text
BASE_N
REINTEGRATION_TRUE_N
NO_REINTEGRATION_WITHIN_TARGET_WEEK_N
N_TIMING
MINIMUM_ELAPSED_UTC_HOURS
MAXIMUM_ELAPSED_UTC_HOURS
MEAN
MEDIAN
P01 P05 P10 P25 P50 P75 P90 P95 P99
EMPIRICAL_CDF OF ELAPSED_UTC_HOURS
```

Numerical contract:

```text
QUANTILE METHOD = HYNDMAN-FAN TYPE 7
P50 = MEDIAN
ECDF = EXACT / UNSMOOTHED / UNBINNED
CANONICAL SCALAR OUTPUT = 18-DECIMAL ROUND_HALF_EVEN
```

Implementation must first qualify on synthetic/contractual evidence with no real timing-result exposure. Only after PASS may one real canonical execution occur. Independent recomputation and deterministic replay are required with exact parity.

No event-level derived timing ledger may become a new canonical data product.

## Boundaries

```text
EVENT != IID OBSERVATION
DEPENDENCE KEYS = target_week_id, sweep_cluster_id

KAPLAN-MEIER = NOT ACTIVATED
SURVIVAL FUNCTION = NOT ACTIVATED
HAZARD FUNCTION = NOT ACTIVATED
CENSORING MODEL = NOT ACTIVATED

SUBGROUPS = NONE
OOS CONSUMPTION = NONE
PREDICTION = NO
CAUSATION = NOT ESTABLISHED
EDGE = NO
STRATEGY VALIDATION = NO
TRADING AUTHORITY = NONE
```

Explicitly forbidden: MFE, MAE, post-sweep path analysis, close-displacement segmentation, timing interactions, Occurrence × Response, post-hoc time-threshold search, parameter optimization, survival estimation, PnL, trading authority, capital deployment.

Evidence status of the real result must remain:

```text
EXPOSED_EXPLORATORY_ONLY
HISTORICAL CORPUS = ALREADY EXPOSED
GENERALIZATION = NOT_ESTABLISHED
CONFIRMATORY GENERALIZATION = FRESH_OOS_EVIDENCE_REQUIRED
```

If the real result is technically qualified and persisted:

```text
RESULT HUMAN_ADOPTED = NO
SURVIVAL FRONTIER = NOT OPENED
SUBGROUP FRONTIER = NOT OPENED
MFE / MAE FRONTIER = NOT OPENED
NEXT SCIENTIFIC FRONTIER = NOT AUTOMATICALLY OPENED
NEXT ACTION = HUMAN ADJUDICATION OF THE FIRST REAL CONDITIONAL TIME-TO-FIRST-REINTEGRATION RESULT
STOP
```
