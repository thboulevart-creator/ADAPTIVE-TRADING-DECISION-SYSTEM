# BEPD-09B — C1 CLAIM SELECTION / DESIGN-ONLY HUMAN AUTHORIZATION — 2026-10-07

## Governed surface

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

FRESH PRE-MUTATION HEAD =
13c33944ec07dadfe02cdf6099c61084fe5dfff4

FRESH PRE-MUTATION TREE =
7069c714899650d9e5a6096770d1cd568a2c5aae

CONCURRENT DRIFT CLASSIFICATION =
NON_MATERIAL_TO_BEPD_09B
```

These HEAD/TREE identities are observational pre-mutation references only and must never be imposed as future branch state.

## Human adjudication

```text
C1 SELECTION =
SELECT
```

Selected claim candidate:

```text
C1 =
T0-AVAILABLE CONTEXT
→
SAME-WEEK REINTEGRATION

T0 =
take_h1_close_utc

RESPONSE =
same_week_reintegration
```

This decision makes C1 only the next claim to design and preregister.

It creates no test result, predictive validation, statistical significance, generalization, edge, strategy validation or trading authority.

## Authorized phase

`BEPD-09B — C1 SAME-WEEK REINTEGRATION CLAIM PREREGISTRATION + EXPOSURE-TIME CONTROL DESIGN V0.1`

```text
AUTHORITY =
DESIGN_ONLY
+
PREREGISTRATION_ONLY
+
PRE_RESULT
```

The design must freeze before any real C1 analysis:
- exact estimand;
- response semantics;
- claim-scoped T0 predictor surface;
- unequal remaining observation-time treatment;
- target_week_id / sweep_cluster_id dependence handling;
- method eligibility;
- missingness / inadmissibility rules;
- anti-leakage rules;
- multiplicity / feature-selection boundary;
- exploratory historical vs confirmatory OOS boundary;
- exact future result surface;
- fail-closed breakers.

## Binding restrictions

```text
REAL EVENT_LEDGER CLAIM ANALYSIS =
NOT AUTHORIZED

C1 REAL TEST =
NOT AUTHORIZED

P-VALUE =
NOT AUTHORIZED

CONFIDENCE INTERVAL =
NOT AUTHORIZED

BOOTSTRAP =
NOT AUTHORIZED

PERMUTATION TEST =
NOT AUTHORIZED

MODEL TRAINING =
NOT AUTHORIZED

FEATURE IMPORTANCE SEARCH =
NOT AUTHORIZED

THRESHOLD OPTIMIZATION =
NOT AUTHORIZED

OOS CONSUMPTION =
NOT AUTHORIZED

TP / SL =
NOT AUTHORIZED

BACKTEST / PNL / PAPER / BROKER / LIVE / CAPITAL =
NOT AUTHORIZED

TRADING AUTHORITY =
NONE
```

```text
HISTORICAL CORPUS =
ALREADY EXPOSED

ANY LATER HISTORICAL C1 USE =
EXPLORATORY_ONLY
```

After BEPD-09B design freeze, documentary/programmatic qualification and persisted-head verification:

```text
STOP
```

Any real C1 execution requires a separate human adjudication.
