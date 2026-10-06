J’autorise l’ouverture et l’exécution de :

`BEPD-08C — INTERNAL / EXTERNAL TARGET-WEEK-CLOSE DISTANCE DECOMPOSITION SEMANTICS + DUAL AGGREGATION CONTRACT + PRE-RESULT FREEZE V0.1`

sur le dépôt gouverné :

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

REFERENCE HEAD =
abfe4326fa9d87cb14e822905c805ed34bee2314

REFERENCE TREE =
7c2c44529961d667d19034d325d492c8d9ce2d99
```

Cette référence est informative uniquement.

Un preflight frais est obligatoire avant toute mutation.

## 1. BINDING PRIOR AUTHORITY

Je reconnais comme binding :

```text
BEPD-08B FINAL HUMAN ADJUDICATION =
73ff0141c2e879ae0b3c51444d5a0af95359ba6f

BEPD-08B CANONICAL REAL D_CLOSE RESULT =
ed6e9088e06e80c21fcb6314add93268c9bc307a

BEPD-08A FINAL HUMAN ADJUDICATION =
553fedc2b538a90750839b6fce8edb9619a4dcb7

BEPD-08A ABSOLUTE DISTANCE CONTRACT =
4cfcb983ad64f31b443534d70991f8ddcb11ff8f

BEPD-05A CLOSE-DISPLACEMENT SEMANTICS CONTRACT =
0a580920ce47885d2bd3277b879b2b888b8d4354

BEPD-05B CANONICAL REAL SIGNED CLOSE-DISPLACEMENT RESULT =
1280156ca949fc48f00e50240aa09cdae11ba4d7

BEPD-05B FINAL HUMAN ADJUDICATION =
811b8e9f58d33cc35c45f714ea99e696d589b147

BEPD-02 EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2
```

Toute divergence matérielle :

```text
FAIL CLOSED
```

## 2. OBJECTIF EXCLUSIF

L’objectif exclusif de `BEPD-08C` est de définir et geler, avant toute nouvelle distribution conditionnelle réelle, la décomposition de :

```text
D_CLOSE =
abs(close_displacement)
```

selon le côté du niveau Weekly sur lequel se situe le `target_week_close_mid`.

Deux populations seulement sont concernées :

```text
CLOSE_SIDE_INTERNAL

CLOSE_SIDE_EXTERNAL
```

Aucune distribution réelle nouvelle ne doit être calculée sous `BEPD-08C`.

## 3. CLOSE-SIDE SEMANTICS

La classification doit utiliser exclusivement le signe déjà qualifié de :

```text
close_displacement
```

Définition :

```text
IF
close_displacement > 0

THEN
CLOSE_SIDE =
INTERNAL
```

avec la sémantique binding :

```text
TARGET-WEEK CLOSE
LIES ON THE REINTEGRATED / INTERNAL SIDE
OF THE SWEPT WEEKLY REFERENCE LEVEL
```

Définition :

```text
IF
close_displacement < 0

THEN
CLOSE_SIDE =
EXTERNAL
```

avec la sémantique binding :

```text
TARGET-WEEK CLOSE
LIES ON THE EXTERNAL SIDE
BEYOND THE SWEPT WEEKLY REFERENCE LEVEL
```

Et :

```text
IF
close_displacement = 0

THEN
CLOSE_SIDE =
EXACT_LEVEL
```

`EXACT_LEVEL` ne doit être assigné ni à INTERNAL ni à EXTERNAL.

## 4. CRITICAL NON-EQUIVALENCE

Il est interdit d’assimiler :

```text
CLOSE_SIDE_INTERNAL
```

à :

```text
same_week_reintegration = TRUE
```

ou :

```text
CLOSE_SIDE_EXTERNAL
```

à :

```text
same_week_reintegration = FALSE
```

La distinction binding est :

```text
same_week_reintegration =
PATH / EVENT HISTORY PROPERTY

CLOSE_SIDE =
TARGET-WEEK TERMINAL CLOSE POSITION
RELATIVE TO THE SWEPT LEVEL
```

Donc :

```text
SAME-WEEK REINTEGRATION
!=
TARGET-WEEK CLOSE SIDE
```

Aucune utilisation de `same_week_reintegration` n’est autorisée pour constituer les deux populations `08C`.

## 5. DISTANCE WITHIN EACH POPULATION

Pour chaque événement :

```text
D_CLOSE =
abs(close_displacement)
```

reste inchangé.

La décomposition future sera :

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

Les deux variables doivent rester :

```text
>= 0
```

## 6. FROZEN POPULATION COUNTS

Le corpus historique qualifié possède déjà les comptes signés exposés dans `BEPD-05B`.

Ils peuvent donc être utilisés comme invariants de population :

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

avec :

```text
207 + 265 + 0 =
472
```

et :

```text
INTERNAL FRACTION =
207 / 472
=
0.438559322033898305

EXTERNAL FRACTION =
265 / 472
=
0.561440677966101695
```

Ces comptes ne constituent pas une nouvelle exposition scientifique.

## 7. PARTITION INVARIANTS

La partition doit être :

```text
MUTUALLY EXCLUSIVE

AND

COLLECTIVELY EXHAUSTIVE
INCLUDING EXACT_LEVEL
```

Pour le corpus actuel :

```text
EXACT_LEVEL N =
0
```

donc :

```text
INTERNAL N + EXTERNAL N =
472
```

Chaque `event_id` doit appartenir à exactement une classe de close-side.

## 8. SOURCE POLICY

La source de classification doit être exclusivement :

```text
BEPD-02 EVENT_LEDGER.close_displacement
```

et la source de distance :

```text
D_CLOSE =
abs(BEPD-02 EVENT_LEDGER.close_displacement)
```

Il est interdit de reconstruire :

```text
target_week_close_mid

level_price_mid

weekly market data

H1 data

AP0 data
```

pour cette première décomposition.

Donc :

```text
PERSISTED FIELD ONLY

NO MARKET RECONSTRUCTION
```

## 9. DUAL FUTURE AGGREGATION SURFACE

Pour chacune des deux populations :

```text
INTERNAL

EXTERNAL
```

la première surface autorisable ultérieurement doit être exclusivement :

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

## 10. NUMERICAL CONTRACT

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
```

La méthode doit être appliquée indépendamment à :

```text
N_INTERNAL = 207

N_EXTERNAL = 265
```

## 11. UNIT SEMANTICS

Les deux distributions restent exprimées en :

```text
USTECH_PRICE_UNITS_AS_PERSISTED
```

Elles ne constituent PAS automatiquement :

```text
BROKER POINTS

TICKS

PIPS

MONEY

PNL

TP

SL

RISK MULTIPLE
```

## 12. WHAT THIS DECOMPOSITION MEANS

`D_INTERNAL` répond exclusivement à :

```text
WHEN THE TARGET-WEEK CLOSE
FINISHES ON THE INTERNAL SIDE
OF THE SWEPT WEEKLY LEVEL,

HOW FAR FROM THE LEVEL
DOES IT FINISH?
```

`D_EXTERNAL` répond exclusivement à :

```text
WHEN THE TARGET-WEEK CLOSE
FINISHES ON THE EXTERNAL SIDE
OF THE SWEPT WEEKLY LEVEL,

HOW FAR BEYOND THE LEVEL
DOES IT FINISH?
```

## 13. OUTCOME-CONDITIONING BOUNDARY

La variable :

```text
CLOSE_SIDE
```

est déterminée par le `target_week_close_mid`.

Elle n’est donc pas connue au moment initial du sweep.

Par conséquent :

```text
CLOSE_SIDE =
OUTCOME-CONDITIONING VARIABLE
```

et :

```text
CLOSE_SIDE
!=
EX-ANTE PREDICTOR
```

La future comparaison INTERNAL / EXTERNAL ne doit pas être interprétée comme une règle utilisable au moment du sweep sans couche prédictive séparée.

## 14. NO TRADING LAUNDERING

Il est interdit de convertir :

```text
D_INTERNAL
```

en :

```text
PROFIT TARGET
TAKE PROFIT
EXPECTED PROFIT
```

ou :

```text
D_EXTERNAL
```

en :

```text
STOP LOSS
EXPECTED LOSS
ADVERSE TRADE EXCURSION
```

Cette décomposition reste descriptive.

## 15. NO COMPARATIVE CLAIM YET

`BEPD-08C` ne doit pas encore produire ou tester :

```text
INTERNAL DISTANCE > EXTERNAL DISTANCE

INTERNAL DISTANCE < EXTERNAL DISTANCE

DIFFERENCE OF MEANS

DIFFERENCE OF MEDIANS

RATIO OF DISTANCES

EFFECT SIZE

STATISTICAL SIGNIFICANCE

CONFIDENCE INTERVAL

BOOTSTRAP

PERMUTATION TEST
```

La première étape future consiste uniquement à exposer séparément les deux distributions.

## 16. NO OTHER SUBGROUPS

Il est interdit de croiser la décomposition avec :

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

## 17. NO THRESHOLD SEARCH

Il est interdit de rechercher :

```text
BEST INTERNAL DISTANCE

BEST EXTERNAL DISTANCE

OPTIMAL TARGET

OPTIMAL STOP

HIGH-PROBABILITY DISTANCE

DISTANCE THRESHOLD
```

ou tout seuil équivalent.

## 18. DEPENDENCE

Je maintiens :

```text
EVENT != IID OBSERVATION

DEPENDENCE KEYS =
target_week_id
sweep_cluster_id
```

Aucune inférence IID n’est activée.

## 19. REQUIRED BREAKER COVERAGE

Un frozen adversarial breaker doit au minimum faire échouer :

```text
wrong EVENT_LEDGER identity

wrong BEPD-05A identity

wrong BEPD-05B identity

wrong BEPD-08A identity

wrong BEPD-08B identity

using same_week_reintegration for classification

using reintegration_h1_close_utc for classification

using HIGH / LOW for classification

reversing positive / negative sign semantics

assigning zero to INTERNAL

assigning zero to EXTERNAL

dropping INTERNAL rows

dropping EXTERNAL rows

overlapping INTERNAL / EXTERNAL membership

non-exhaustive partition

recomputing market prices

reading AP0

reading H1

negative D_CLOSE

signed values retained as conditional distance

changing Type-7 quantiles

changing ECDF semantics

subgroup cross-product

post-hoc threshold search

INTERNAL distribution → TP laundering

EXTERNAL distribution → SL laundering

outcome-side → predictor laundering

IID laundering

prediction laundering

edge laundering

strategy-validation laundering

trading-authority laundering
```

Tous les cas doivent être :

```text
HARD_FAIL
```

## 20. EXPLICITLY OUT OF SCOPE

Cette autorisation n’autorise PAS :

```text
REAL INTERNAL DISTANCE DISTRIBUTION

REAL EXTERNAL DISTANCE DISTRIBUTION

REAL CONDITIONAL AGGREGATION

INTERNAL vs EXTERNAL COMPARATIVE TEST

DIFFERENCE OF MEANS

DIFFERENCE OF MEDIANS

RATIO

EFFECT SIZE

CONFIDENCE INTERVAL

BOOTSTRAP

HIGH vs LOW

same_week_reintegration SUBGROUPS

TIMING × DISTANCE

EXCURSION × DISTANCE

OCCURRENCE × RESPONSE

THRESHOLD SEARCH

TARGET OPTIMIZATION

TP CALIBRATION

SL CALIBRATION

TRADE ENTRY

TRADE DIRECTION

PNL

OOS CONSUMPTION

PREDICTION

CAUSATION

EDGE

STRATEGY VALIDATION

TRADING AUTHORITY

CAPITAL DEPLOYMENT
```

## 21. SCIENTIFIC STATUS

Le statut reste :

```text
HISTORICAL CORPUS =
ALREADY EXPOSED

ANALYSIS STATUS =
EXPLORATORY_ONLY

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

## 22. TERMINAL REQUIREMENT

Si le contrat de décomposition, les invariants de population et le breaker sont qualifiés :

```text
BEPD-08C =
QUALIFIED_FOR_HUMAN_ADOPTION
```

mais :

```text
REAL INTERNAL DISTANCE RESULT =
NOT PRODUCED

REAL EXTERNAL DISTANCE RESULT =
NOT PRODUCED

REAL CONDITIONAL EXECUTION AUTHORITY =
NONE
```

La prochaine action doit être exclusivement :

```text
HUMAN ADJUDICATION OF BEPD-08C
```

Après adoption seulement pourra être ouverte séparément :

```text
BEPD-08D —
FIRST REAL INTERNAL / EXTERNAL
TARGET-WEEK-CLOSE DISTANCE DISTRIBUTIONS
+ TECHNICAL QUALIFICATION
```

```text
STOP.
```
