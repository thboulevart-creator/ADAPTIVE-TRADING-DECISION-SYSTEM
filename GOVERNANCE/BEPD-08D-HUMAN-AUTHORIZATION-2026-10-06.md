J’autorise l’ouverture et l’exécution de :

`BEPD-08D — FIRST REAL INTERNAL / EXTERNAL TARGET-WEEK-CLOSE DISTANCE DISTRIBUTIONS + TECHNICAL QUALIFICATION V0.1`

sur le dépôt gouverné :

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

REFERENCE HEAD =
4b3ef2e62ae830f54abcc01e4d1b9fc6364a01b8

REFERENCE TREE =
49b1e6d22e6b5f816f5e09284d7b189629c69063
```

Cette référence est informative uniquement.

Un preflight frais reste obligatoire avant toute mutation ou exposition réelle.

## 1. FRESH PREFLIGHT

Avant toute mutation :

```text
VERIFY EXACT REPOSITORY
VERIFY EXACT BRANCH
FETCH FRESH REMOTE HEAD
VERIFY FRESH TREE
VERIFY NO MATERIAL BEPD DRIFT
VERIFY NO PRE-EXISTING BEPD-08D REAL RESULT
```

Tout drift concurrent doit être classifié :

```text
MATERIAL_TO_BEPD_08D

or

NON_MATERIAL_TO_BEPD_08D
```

Tout drift matériel non résolu :

```text
FAIL CLOSED
```

## 2. BINDING PRIOR AUTHORITY

Je reconnais comme binding :

```text
BEPD-08C FINAL HUMAN ADJUDICATION =
0cc7d4f812525bd3c4dab29490613b70f8600514

BEPD-08C DECOMPOSITION CONTRACT =
dc767d77b8f0c8cf89f6d87e9a4cd2401dd0b42e

BEPD-08C FROZEN PRE-RESULT BREAKER =
13ad7dba0d4e83036ea1f40b47f1a0a8d1f40bb8

BEPD-08C PRE-RESULT FREEZE =
e4d6ebb35147f8cb884dbe569197236ed34251da

BEPD-08C QUALIFICATION RECEIPT =
11f7f4e83ec9dd56e4fe1657000299f10edd5772

BEPD-08C QUALIFICATION REPORT =
8de5e04b5e1b27bfb9e9f279769022e9a2496c56
```

Je maintiens également comme binding :

```text
BEPD-08B FINAL HUMAN ADJUDICATION =
73ff0141c2e879ae0b3c51444d5a0af95359ba6f

BEPD-08B CANONICAL REAL D_CLOSE RESULT =
ed6e9088e06e80c21fcb6314add93268c9bc307a

BEPD-08A FINAL HUMAN ADJUDICATION =
553fedc2b538a90750839b6fce8edb9619a4dcb7

BEPD-08A ABSOLUTE DISTANCE CONTRACT =
4cfcb983ad64f31b443534d70991f8ddcb11ff8f

BEPD-05A CLOSE-DISPLACEMENT CONTRACT =
0a580920ce47885d2bd3277b879b2b888b8d4354

BEPD-05B CANONICAL SIGNED CLOSE-DISPLACEMENT RESULT =
1280156ca949fc48f00e50240aa09cdae11ba4d7

BEPD-05B FINAL HUMAN ADJUDICATION =
811b8e9f58d33cc35c45f714ea99e696d589b147

BEPD-02 EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2
```

Toute divergence :

```text
FAIL CLOSED
```

## 3. OBJECTIF EXCLUSIF

L’objectif exclusif de `BEPD-08D` est de produire les deux premières distributions historiques réelles séparées :

```text
D_INTERNAL
```

et :

```text
D_EXTERNAL
```

selon les définitions déjà adoptées.

Aucun objectif comparatif, prédictif ou de trading n’est inclus.

## 4. FROZEN CLASSIFICATION

La classification doit rester exactement :

```text
IF
close_displacement > 0

THEN
CLOSE_SIDE =
INTERNAL
```

```text
IF
close_displacement < 0

THEN
CLOSE_SIDE =
EXTERNAL
```

```text
IF
close_displacement = 0

THEN
CLOSE_SIDE =
EXACT_LEVEL
```

Avec :

```text
EXACT_LEVEL != INTERNAL
EXACT_LEVEL != EXTERNAL
```

Aucune autre variable ne peut intervenir dans la classification.

## 5. FROZEN POPULATIONS

Les populations attendues sont exactement :

```text
TOTAL N =
472

INTERNAL N =
207

EXTERNAL N =
265

EXACT_LEVEL N =
0
```

et :

```text
207 + 265 + 0 =
472
```

Tout autre compte :

```text
FAIL CLOSED
```

## 6. CRITICAL NON-EQUIVALENCE

Il est interdit d’utiliser :

```text
same_week_reintegration

reintegration_h1_close_utc

HIGH / LOW

take day

timing

excursion

context
```

pour construire les populations.

La distinction reste :

```text
same_week_reintegration =
PATH / EVENT HISTORY PROPERTY

CLOSE_SIDE =
TARGET-WEEK TERMINAL CLOSE POSITION
RELATIVE TO THE SWEPT WEEKLY LEVEL
```

Donc :

```text
SAME-WEEK REINTEGRATION
!=
TARGET-WEEK CLOSE SIDE
```

## 7. DISTANCE DEFINITIONS

Pour chaque événement :

```text
D_CLOSE =
abs(close_displacement)
```

Puis :

```text
D_INTERNAL =
D_CLOSE
CONDITIONAL ON
close_displacement > 0
```

et :

```text
D_EXTERNAL =
D_CLOSE
CONDITIONAL ON
close_displacement < 0
```

Avec :

```text
D_INTERNAL >= 0

D_EXTERNAL >= 0
```

## 8. SOURCE POLICY

La source exclusive est :

```text
BEPD-02 EVENT_LEDGER.close_displacement
```

La classification et les distances doivent être dérivées uniquement de ce champ persisté.

Donc :

```text
SOURCE POLICY =
PERSISTED FIELD ONLY

MARKET RECONSTRUCTION =
FORBIDDEN

AP0 READ =
FORBIDDEN

H1 READ =
FORBIDDEN

WEEKLY PRICE RECONSTRUCTION =
FORBIDDEN

level_price_mid RECONSTRUCTION =
FORBIDDEN

target_week_close_mid RECONSTRUCTION =
FORBIDDEN
```

## 9. REQUIRED ROW-LEVEL VALIDATIONS

Avant agrégation réelle :

```text
EVENT ROW COUNT =
472

UNIQUE event_id COUNT =
472

DUPLICATE event_id =
0

MISSING close_displacement =
0

NON-FINITE close_displacement =
0
```

La partition doit vérifier :

```text
INTERNAL N =
207

EXTERNAL N =
265

EXACT_LEVEL N =
0

OVERLAPPING MEMBERSHIP =
0

UNCLASSIFIED EVENTS =
0
```

## 10. REAL DUAL AGGREGATION SURFACE

Pour `INTERNAL`, produire exclusivement :

```text
N
MINIMUM
MAXIMUM
MEAN
MEDIAN

P01
P05
P10
P25
P50
P75
P90
P95
P99

ZERO_COUNT
ZERO_FRACTION

EMPIRICAL_CDF
```

Pour `EXTERNAL`, produire exclusivement la même surface :

```text
N
MINIMUM
MAXIMUM
MEAN
MEDIAN

P01
P05
P10
P25
P50
P75
P90
P95
P99

ZERO_COUNT
ZERO_FRACTION

EMPIRICAL_CDF
```

## 11. NUMERICAL CONTRACT

Pour les deux distributions :

```text
QUANTILE METHOD =
HYNDMAN-FAN TYPE 7

P50 =
MEDIAN

ECDF =
EXACT / UNSMOOTHED / UNBINNED

CANONICAL SCALAR OUTPUT =
18-DECIMAL ROUND_HALF_EVEN

UNIT =
USTECH_PRICE_UNITS_AS_PERSISTED
```

Les quantiles sont calculés séparément sur :

```text
N_INTERNAL =
207

N_EXTERNAL =
265
```

## 12. ECDF REQUIREMENTS

Chaque ECDF doit contenir au minimum :

```text
support_value
support_count
cumulative_count
cumulative_fraction
cumulative_decimal
```

Et vérifier :

```text
INTERNAL ECDF FINAL COUNT =
207

INTERNAL ECDF FINAL FRACTION =
1

EXTERNAL ECDF FINAL COUNT =
265

EXTERNAL ECDF FINAL FRACTION =
1
```

## 13. IMPLEMENTATION QUALIFICATION BEFORE REAL EXPOSURE

Avant toute agrégation réelle, créer et qualifier au minimum :

```text
DETERMINISTIC DUAL-DISTRIBUTION RUNNER

INDEPENDENT RECOMPUTATION IMPLEMENTATION

EXECUTABLE OR EXECUTABLE-EQUIVALENT
BEPD-08C BREAKER

SYNTHETIC TEST SUITE

RESULT SERIALIZATION

RUN MANIFEST

IMPLEMENTATION QUALIFICATION RECEIPT

IMPLEMENTATION QUALIFICATION REPORT
```

La qualification pré-résultat doit utiliser uniquement :

```text
SYNTHETIC DATA

FROZEN IDENTITIES

CONTRACTUAL METADATA
```

et doit encore vérifier :

```text
REAL INTERNAL DISTRIBUTION =
NOT EXPOSED

REAL EXTERNAL DISTRIBUTION =
NOT EXPOSED

REAL CONDITIONAL AGGREGATION =
NOT EXECUTED
```

## 14. MINIMUM SYNTHETIC TEST COVERAGE

La qualification synthétique doit couvrir au minimum :

```text
positive close_displacement → INTERNAL

negative close_displacement → EXTERNAL

zero close_displacement → EXACT_LEVEL

zero not assigned to INTERNAL

zero not assigned to EXTERNAL

positive value → positive D_INTERNAL

negative value → positive D_EXTERNAL

no negative conditional distance

INTERNAL rows retained

EXTERNAL rows retained

partition mutually exclusive

partition exhaustive including EXACT_LEVEL

same_week_reintegration ignored for classification

reintegration_h1_close_utc ignored for classification

HIGH / LOW ignored for classification

missing close_displacement → hard fail

non-finite close_displacement → hard fail

duplicate event_id → hard fail

population mismatch → hard fail

Type-7 quantile correctness

P50 = median

exact INTERNAL ECDF

exact EXTERNAL ECDF

INTERNAL terminal ECDF count

EXTERNAL terminal ECDF count

18-decimal ROUND_HALF_EVEN serialization

no comparative metric

no difference of means

no difference of medians

no ratio

no effect size

no significance test

no confidence interval

no threshold search

no TP / SL

no PnL

no prediction

no trading authority
```

## 15. BREAKER REQUALIFICATION

Les 32 failure modes gelés dans `BEPD-08C` doivent être rendus exécutables ou couverts par un équivalent exécutable.

```text
BREAKER =
32 / 32 REQUIRED
```

Aucun breaker ne peut être :

```text
REMOVED

WEAKENED

DOWNGRADED TO WARNING
```

## 16. REAL EXECUTION FREEZE

Si et seulement si l’implémentation pré-résultat est qualifiée, un freeze doit être persisté AVANT toute exposition réelle.

Il doit lier exactement :

```text
BEPD-08D HUMAN AUTHORIZATION

BEPD-08C FINAL HUMAN ADJUDICATION

BEPD-08C DECOMPOSITION CONTRACT

BEPD-08C BREAKER

BEPD-08C PRE-RESULT FREEZE

BEPD-08D RUNNER

INDEPENDENT RECOMPUTATION IMPLEMENTATION

EXECUTABLE BREAKER

SYNTHETIC TESTS

IMPLEMENTATION QUALIFICATION RECEIPT

EVENT_LEDGER IDENTITY
```

Toute divergence après freeze :

```text
FAIL CLOSED
```

## 17. FIRST REAL EXECUTION AUTHORITY

Si et seulement si :

```text
IMPLEMENTATION QUALIFICATION =
PASS

AND

REAL EXECUTION FREEZE =
EXACT
```

alors :

```text
ONE FIRST REAL DUAL CONDITIONAL EXECUTION =
AUTHORIZED
```

Cette exécution doit :

```text
READ THE 472 EVENT_LEDGER ROWS ONCE

CLASSIFY EACH EVENT ONCE

PARTITION INTO:
207 INTERNAL
265 EXTERNAL
0 EXACT_LEVEL

COMPUTE D_CLOSE =
abs(close_displacement)

PRODUCE:
ONE INTERNAL DISTRIBUTION
ONE EXTERNAL DISTRIBUTION
```

Cette autorisation ne permet pas plusieurs recherches ou variantes de partition.

## 18. INDEPENDENT RECOMPUTATION

Après le résultat réel :

```text
INDEPENDENT RECOMPUTATION =
REQUIRED
```

L’implémentation indépendante doit :

```text
NOT IMPORT THE CANONICAL RUNNER

READ THE SAME EXACT EVENT_LEDGER

REIMPLEMENT CLOSE_SIDE CLASSIFICATION

REIMPLEMENT D_CLOSE = abs(close_displacement)

REIMPLEMENT INTERNAL / EXTERNAL PARTITION

REIMPLEMENT TYPE-7 QUANTILES

REIMPLEMENT BOTH EXACT ECDFs
```

La parité doit être exacte sur les deux distributions.

Pour INTERNAL :

```text
N
MINIMUM
MAXIMUM
MEAN
MEDIAN
ALL QUANTILES
ZERO_COUNT
ZERO_FRACTION
FULL ECDF
```

Pour EXTERNAL :

```text
N
MINIMUM
MAXIMUM
MEAN
MEDIAN
ALL QUANTILES
ZERO_COUNT
ZERO_FRACTION
FULL ECDF
```

Toute divergence :

```text
FAIL CLOSED
```

## 19. DETERMINISTIC REPLAY

Le même runner doit être rejoué avec exactement les mêmes entrées uniquement comme preuve de reproductibilité.

```text
DETERMINISTIC REPLAY =
REQUIRED

EXACT CANONICAL OBJECT PARITY =
REQUIRED

REPLAY != NEW INDEPENDENT EVIDENCE
```

## 20. REQUIRED REAL-RESULT VALIDATIONS

La qualification réelle doit vérifier au minimum :

```text
EVENT_LEDGER IDENTITY =
EXACT

TOTAL EVENT ROW COUNT =
472

UNIQUE EVENT IDS =
472

MISSING close_displacement =
0

FILTERED ROWS =
0

INTERNAL N =
207

EXTERNAL N =
265

EXACT_LEVEL N =
0

INTERNAL + EXTERNAL + EXACT_LEVEL =
472

OVERLAPPING MEMBERSHIP =
0

UNCLASSIFIED EVENTS =
0

NEGATIVE D_INTERNAL =
0

NEGATIVE D_EXTERNAL =
0

D_INTERNAL =
abs(close_displacement)
FOR ALL INTERNAL EVENTS

D_EXTERNAL =
abs(close_displacement)
FOR ALL EXTERNAL EVENTS

INTERNAL P50 = INTERNAL MEDIAN =
PASS

EXTERNAL P50 = EXTERNAL MEDIAN =
PASS

TYPE-7 QUANTILES =
PASS

INTERNAL ECDF FINAL COUNT =
207

INTERNAL ECDF FINAL FRACTION =
1

EXTERNAL ECDF FINAL COUNT =
265

EXTERNAL ECDF FINAL FRACTION =
1

INDEPENDENT RECOMPUTATION =
EXACT PARITY

DETERMINISTIC REPLAY =
EXACT OBJECT PARITY
```

## 21. NO COMPARATIVE CLAIM

Même après exposition des deux distributions, il est interdit sous `BEPD-08D` de calculer ou conclure :

```text
INTERNAL > EXTERNAL

INTERNAL < EXTERNAL

DIFFERENCE OF MEANS

DIFFERENCE OF MEDIANS

RATIO OF MEANS

RATIO OF MEDIANS

DISTRIBUTION RATIO

EFFECT SIZE

DOMINANCE RATE

STATISTICAL SIGNIFICANCE

CONFIDENCE INTERVAL

BOOTSTRAP COMPARISON

PERMUTATION TEST

KS TEST

MANN-WHITNEY TEST

ANY OTHER COMPARATIVE TEST
```

Les deux distributions doivent être exposées séparément sans construire de nouveau claim comparatif.

## 22. NO OTHER SUBGROUPS

Aucun croisement n’est autorisé avec :

```text
HIGH / LOW

same_week_reintegration

TAKE DAY

LEVEL AGE

YEAR

MONTH

VOLATILITY

REGIME

TIME-TO-REINTEGRATION

MAX_REINTEGRATIVE_EXCURSION

MAX_EXTERNAL_EXCURSION

SWEEP CLUSTER SIZE

OTHER CONTEXT
```

## 23. NO THRESHOLD SEARCH

Il est interdit de rechercher après exposition :

```text
BEST INTERNAL DISTANCE

BEST EXTERNAL DISTANCE

OPTIMAL TARGET

OPTIMAL STOP

HIGH-PROBABILITY DISTANCE

BEST QUANTILE

BEST TP

BEST SL

ANY POST-HOC DISTANCE THRESHOLD
```

## 24. OUTCOME-CONDITIONING BOUNDARY

Je maintiens :

```text
CLOSE_SIDE =
OUTCOME-CONDITIONING VARIABLE

CLOSE_SIDE =
NOT KNOWN AT INITIAL SWEEP

CLOSE_SIDE != EX-ANTE PREDICTOR
```

Donc :

```text
D_INTERNAL DISTRIBUTION
!=
EX-ANTE PROFIT TARGET DISTRIBUTION

D_EXTERNAL DISTRIBUTION
!=
EX-ANTE STOP-LOSS DISTRIBUTION
```

## 25. DEPENDENCE BOUNDARY

Je maintiens :

```text
EVENT != IID OBSERVATION

DEPENDENCE KEYS =
target_week_id
sweep_cluster_id
```

Cette autorisation n’active :

```text
NO IID STANDARD ERROR

NO IID CONFIDENCE INTERVAL

NO IID BOOTSTRAP

NO GENERALIZATION INTERVAL
```

## 26. PERSISTENCE SURFACE

Si le résultat réel est qualifié, persister au minimum :

```text
CANONICAL INTERNAL / EXTERNAL RESULT

RUN MANIFEST

INDEPENDENT RECOMPUTATION RESULT

DETERMINISTIC REPLAY EVIDENCE

TECHNICAL EXECUTION RECEIPT

REAL RESULT QUALIFICATION RECEIPT

REAL RESULT QUALIFICATION REPORT

PERSISTED-HEAD VERIFICATION
```

Il est interdit de promouvoir un nouveau dataset événement-par-événement dérivé sans autorisation séparée.

## 27. SCIENTIFIC STATUS

Les deux distributions doivent rester :

```text
HISTORICAL CORPUS =
ALREADY EXPOSED

EVIDENCE STATUS =
EXPOSED_EXPLORATORY_ONLY

GENERALIZATION =
NOT_ESTABLISHED

CONFIRMATORY GENERALIZATION =
FRESH_OOS_EVIDENCE_REQUIRED

PREDICTION =
NO

CAUSATION =
NOT ESTABLISHED

EDGE =
NO

STRATEGY VALIDATION =
NO

TRADING AUTHORITY =
NONE
```

## 28. EXPLICITLY OUT OF SCOPE

Cette autorisation n’autorise PAS :

```text
INTERNAL vs EXTERNAL COMPARATIVE TEST

DIFFERENCE OF MEANS

DIFFERENCE OF MEDIANS

RATIOS

EFFECT SIZE

STATISTICAL SIGNIFICANCE

CONFIDENCE INTERVAL

BOOTSTRAP COMPARISON

PERMUTATION TEST

HIGH / LOW ANALYSIS

same_week_reintegration ANALYSIS

TIMING × DISTANCE

EXCURSION × DISTANCE

OCCURRENCE × RESPONSE

THRESHOLD SEARCH

TARGET OPTIMIZATION

TP CALIBRATION

SL CALIBRATION

TRADE ENTRY

TRADE DIRECTION

EXPECTED PNL

STRATEGY VALIDATION

OOS CONSUMPTION

PREDICTION

CAUSATION

EDGE

TRADING AUTHORITY

CAPITAL DEPLOYMENT
```

## 29. TECHNICAL TERMINAL STATE

Si l’exécution réelle, la recomputation indépendante, le replay, la qualification et la persistance sont tous PASS :

```text
BEPD-08D =
FIRST REAL INTERNAL / EXTERNAL
TARGET-WEEK-CLOSE DISTANCE DISTRIBUTIONS
TECHNICALLY QUALIFIED
```

mais :

```text
RESULT HUMAN_ADOPTED =
NO

INTERNAL vs EXTERNAL COMPARATIVE FRONTIER =
NOT OPENED

SUBGROUP FRONTIER =
NOT OPENED

THRESHOLD FRONTIER =
NOT OPENED

OOS FRONTIER =
NOT OPENED

TRADING FRONTIER =
NOT OPENED

NEXT SCIENTIFIC FRONTIER =
NOT AUTOMATICALLY OPENED
```

## 30. STOP BOUNDARY

Après :

```text
FIRST REAL DUAL EXECUTION

INDEPENDENT RECOMPUTATION

DETERMINISTIC REPLAY

TECHNICAL QUALIFICATION

PERSISTENCE

PERSISTED-HEAD VERIFICATION
```

la phase doit :

```text
STOP
```

La prochaine action doit être exclusivement :

```text
HUMAN ADJUDICATION
OF THE FIRST REAL
INTERNAL / EXTERNAL
TARGET-WEEK-CLOSE DISTANCE DISTRIBUTIONS
```

Aucun test comparatif, seuil, TP/SL, OOS ou travail de trading ne doit être ouvert automatiquement.
