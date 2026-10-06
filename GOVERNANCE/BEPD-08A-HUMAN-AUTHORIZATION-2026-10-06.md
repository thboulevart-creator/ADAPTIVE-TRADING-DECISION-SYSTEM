J’autorise l’ouverture et l’exécution de :

`BEPD-08A — ABSOLUTE LEVEL-TO-TARGET-WEEK-CLOSE DISTANCE SEMANTICS + GLOBAL AGGREGATION CONTRACT + PRE-RESULT FREEZE V0.1`

sur le dépôt gouverné :

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

REFERENCE HEAD =
fb0d3e3aa7bc37684d499d7ba653f79cb3e6d810

REFERENCE TREE =
ec0a9994baeff21c49b21a4e24c35e850816bea5
```

Cette référence ne dispense PAS d’un preflight frais avant toute mutation.

## 1. BINDING INPUTS

Je reconnais comme sources et autorités binding :

```text
BEPD-01D HISTORICAL LEDGER SCHEMA =
85f5cdda60397fce59efc1e5d36c1128cf9cc185

BEPD-02 EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2

BEPD-05A CLOSE-DISPLACEMENT SEMANTICS CONTRACT =
0a580920ce47885d2bd3277b879b2b888b8d4354

BEPD-05B CANONICAL REAL GLOBAL CLOSE-DISPLACEMENT RESULT =
1280156ca949fc48f00e50240aa09cdae11ba4d7

BEPD-05B FINAL HUMAN ADJUDICATION =
811b8e9f58d33cc35c45f714ea99e696d589b147

BEPD-07B FINAL HUMAN ADJUDICATION / CLOSURE =
9023fe36e80030978f116c58e58fd5664e19be20
```

Toute divergence matérielle doit produire :

```text
FAIL CLOSED
```

## 2. OBJECTIF EXCLUSIF

L’objectif exclusif de `BEPD-08A` est de définir, qualifier et geler avant toute nouvelle exposition statistique la variable :

```text
ABSOLUTE_LEVEL_TO_TARGET_WEEK_CLOSE_DISTANCE
```

qui répond exclusivement à :

```text
AFTER A QUALIFIED WEEKLY LIQUIDITY SWEEP,

HOW FAR IN PRICE UNITS
IS THE TARGET-WEEK CLOSE
FROM THE FIXED SWEPT WEEKLY LEVEL?
```

`BEPD-08A` ne doit produire aucune distribution réelle nouvelle.

## 3. PRIMARY ESTIMAND

La variable canonique candidate est :

```text
D_CLOSE =
abs(close_displacement)
```

avec l’équivalence exacte :

```text
D_CLOSE =
abs(target_week_close_mid - level_price_mid)
```

Pour :

```text
SIDE = HIGH
```

le champ source reste :

```text
close_displacement =
level_price_mid - target_week_close_mid
```

Pour :

```text
SIDE = LOW
```

le champ source reste :

```text
close_displacement =
target_week_close_mid - level_price_mid
```

Dans les deux cas :

```text
D_CLOSE =
abs(close_displacement)
```

et donc :

```text
D_CLOSE >= 0
```

obligatoirement.

## 4. SOURCE POLICY

La source primaire doit être exclusivement :

```text
BEPD-02 EVENT_LEDGER.close_displacement
```

déjà qualifié et humainement adopté.

La première exécution future doit utiliser :

```text
PERSISTED FIELD ONLY

NO MARKET DATA RECONSTRUCTION

NO AP0 READ

NO H1 RECONSTRUCTION

NO WEEKLY PRICE RECONSTRUCTION
```

La relation :

```text
D_CLOSE =
abs(close_displacement)
```

doit être une transformation déterministe pure de la valeur persistée.

## 5. BASE POPULATION

La population reste :

```text
ALL QUALIFIED BEPD-02 EVENT_LEDGER ROWS =
472
```

avec :

```text
UNIT =
ONE QUALIFIED LEVEL_SWEEP_EVENT

FILTERING =
NONE

WEIGHTING =
ONE EQUAL WEIGHT PER QUALIFIED EVENT
```

Les événements :

```text
same_week_reintegration = FALSE
```

doivent rester inclus.

Aucun événement ne doit être exclu selon le signe ou la magnitude de `close_displacement`.

## 6. DISTANCE SEMANTICS

La variable répond à une question de magnitude géométrique :

```text
DISTANCE FROM FIXED SWEPT WEEKLY LEVEL
TO TARGET-WEEK CLOSE
```

Elle élimine volontairement l’information de direction.

Donc :

```text
D_CLOSE
!=
SIGNED CLOSE DISPLACEMENT
```

mais :

```text
D_CLOSE
=
ABSOLUTE VALUE OF SIGNED CLOSE DISPLACEMENT
```

Les deux surfaces doivent rester conceptuellement distinctes.

## 7. UNIT SEMANTICS

L’unité canonique doit rester :

```text
USTECH_PRICE_UNITS_AS_PERSISTED
```

Elle peut être décrite humainement comme une distance de prix.

Mais elle ne doit PAS être automatiquement assimilée à :

```text
BROKER POINTS

TICKS

PIPS

MONEY

PNL

RISK MULTIPLE
```

Toute conversion broker/execution nécessitera un contrat distinct.

## 8. SIGN INFORMATION

`BEPD-08A` ne remplace ni ne réinterprète la sémantique signée déjà adoptée :

```text
close_displacement > 0
=
TARGET-WEEK CLOSE ON
REINTEGRATED / INTERNAL SIDE

close_displacement < 0
=
TARGET-WEEK CLOSE ON
EXTERNAL SIDE
```

Mais la première distribution `D_CLOSE` doit ignorer cette direction pour mesurer exclusivement la magnitude.

## 9. FIRST REAL GLOBAL AGGREGATION SURFACE

Pour une future première exécution réelle, la surface globale autorisable doit être exclusivement :

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

avec :

```text
N =
472
```

sauf FAIL CLOSED.

## 10. NUMERICAL CONTRACT

Le contrat numérique doit rester cohérent avec BEPD-05A / BEPD-05B :

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

Pour l’ECDF :

```text
FINAL CUMULATIVE COUNT =
472

FINAL CUMULATIVE FRACTION =
1
```

## 11. ZERO SEMANTICS

Un zéro signifie exclusivement :

```text
target_week_close_mid
=
level_price_mid
```

selon la valeur persistée.

Il est interdit de créer un zéro par :

```text
ROUNDING

MISSING DATA

IMPUTATION

THRESHOLDING

BUCKETING
```

## 12. NO SIGN-CONDITIONAL DECOMPOSITION YET

`BEPD-08A` n’autorise PAS encore les distributions séparées :

```text
D_CLOSE | close_displacement > 0

D_CLOSE | close_displacement < 0
```

Autrement dit :

```text
INTERNAL-SIDE CLOSE DISTANCE DISTRIBUTION =
NOT YET AUTHORIZED

EXTERNAL-SIDE CLOSE DISTANCE DISTRIBUTION =
NOT YET AUTHORIZED
```

Ces deux distributions constituent une future frontière distincte après adjudication du résultat global absolu.

## 13. NO OTHER SUBGROUPS

Aucune segmentation n’est autorisée par :

```text
HIGH / LOW

SAME_WEEK_REINTEGRATION TRUE / FALSE

LEVEL AGE

TAKE DAY

MONTH / YEAR

VOLATILITY

REGIME

TIME-TO-REINTEGRATION

MAX_REINTEGRATIVE_EXCURSION

MAX_EXTERNAL_EXCURSION

SWEEP CLUSTER SIZE

OTHER CONTEXT
```

## 14. NO THRESHOLDS

Il est interdit de sélectionner après exposition :

```text
50 POINTS

100 POINTS

200 POINTS

500 POINTS

OR ANY OTHER DISTANCE THRESHOLD
```

comme seuil prétendument significatif.

Toute future question :

```text
P(D_CLOSE <= X)

P(D_CLOSE >= X)
```

nécessitera soit :

```text
A PRE-REGISTERED X
```

soit une utilisation purement descriptive clairement identifiée comme telle.

## 15. DEPENDENCE

Le contrat doit maintenir :

```text
EVENT != IID OBSERVATION

DEPENDENCE KEYS =
target_week_id
sweep_cluster_id
```

La première distribution absolue reste descriptive.

Aucune méthode IID d’incertitude n’est activée.

## 16. REQUIRED BREAKER COVERAGE

Un frozen adversarial breaker doit au minimum faire échouer :

```text
wrong EVENT_LEDGER identity

wrong BEPD-05A contract identity

wrong BEPD-05B adopted-result identity

market reconstruction instead of persisted close_displacement

using target_week_close_mid only

using level_price_mid only

failing to apply absolute value

retaining signed values in D_CLOSE

negative D_CLOSE output

dropping negative close_displacement rows

dropping positive close_displacement rows

dropping no-reintegration rows

filtering by HIGH / LOW

filtering by sign

internal/external subgrouping

post-hoc threshold selection

rounding-to-zero laundering

broker-points laundering

ticks laundering

PnL laundering

IID laundering

distance distribution → prediction laundering

distance distribution → edge laundering

distance distribution → TP laundering

distance distribution → SL laundering

distance distribution → strategy validation laundering

distance distribution → trading authority laundering
```

## 17. EXPLICITLY OUT OF SCOPE

Cette autorisation n’autorise PAS :

```text
REAL D_CLOSE DISTRIBUTION

REAL ABSOLUTE DISTANCE AGGREGATION

INTERNAL vs EXTERNAL DISTANCE DECOMPOSITION

HIGH vs LOW ANALYSIS

REINTEGRATION TRUE vs FALSE ANALYSIS

TIMING × DISTANCE

EXCURSION × DISTANCE

OCCURRENCE × RESPONSE

DISTANCE THRESHOLD SEARCH

TP / SL CALIBRATION

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

## 18. SCIENTIFIC STATUS

Le contrat doit préserver :

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

## 19. REQUIRED QUALIFICATION

Avant toute première agrégation réelle de `D_CLOSE` :

```text
SOURCE IDENTITIES =
EXACT

BASE POPULATION =
472 / FROZEN

SOURCE FIELD =
close_displacement / FROZEN

TRANSFORMATION =
abs(close_displacement) / FROZEN

MARKET RECONSTRUCTION =
FORBIDDEN

UNIT =
USTECH_PRICE_UNITS_AS_PERSISTED / FROZEN

D_CLOSE >= 0 =
REQUIRED

AGGREGATION SURFACE =
FROZEN

SIGN-CONDITIONAL AUTHORITY =
NONE

SUBGROUP AUTHORITY =
NONE

THRESHOLD AUTHORITY =
NONE

OOS AUTHORITY =
NONE

PREDICTION AUTHORITY =
NONE

TRADING AUTHORITY =
NONE

NEW REAL DISTANCE RESULT =
NOT PRODUCED
```

Le breaker doit être qualifié avant toute exposition réelle.

## 20. STOP BOUNDARY

Si le contrat, la transformation, l’unité, la surface d’agrégation et le breaker sont qualifiés :

```text
BEPD-08A =
QUALIFIED_FOR_HUMAN_ADOPTION
```

mais :

```text
HUMAN ADOPTION =
NOT AUTOMATIC

REAL ABSOLUTE DISTANCE EXECUTION =
NOT AUTHORIZED

REAL ABSOLUTE DISTANCE RESULT =
NOT PRODUCED
```

La prochaine action requise devra être exclusivement :

```text
HUMAN ADJUDICATION OF BEPD-08A
```

Après adoption seulement pourra être ouverte une autorisation distincte pour :

```text
BEPD-08B —
FIRST REAL GLOBAL
ABSOLUTE LEVEL-TO-TARGET-WEEK-CLOSE
DISTANCE DISTRIBUTION
```

```text
STOP.
```
