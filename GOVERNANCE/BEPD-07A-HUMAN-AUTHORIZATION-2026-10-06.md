J’autorise l’ouverture et l’exécution de :

`BEPD-07A — SAME-WEEK POST-SWEEP PATH GEOMETRY + BEHAVIORAL EXCURSION SEMANTICS (MFE/MAE) + PRE-RESULT FREEZE V0.1`

sur le dépôt gouverné :

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

REFERENCE HEAD =
26e9f268a1ba2909700a41855654e70ac0936740

REFERENCE TREE =
99709a877fb9f97f52b2f474cd00fb3ef77bc84f
```

Cette référence ne dispense PAS d’un preflight frais avant toute mutation.

## 1. BINDING INPUTS

Je reconnais comme sources et autorités préalables :

```text
BEPD-00 CONDENSED DESIGN =
e4317da4e93a0dc652f84c38fafb794c825bef9f

BEPD-01D HISTORICAL LEDGER SCHEMA =
85f5cdda60397fce59efc1e5d36c1128cf9cc185

BEPD-02 EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2

BEPD-06B FINAL HUMAN ADJUDICATION =
539282a1ab6740b4dbbbfa774d780b7eff08f386

AP0 USTECH PROFILE MINUTE CORE ADJUDICATION =
94bba3315e3569993623b8cd2a2bf4264f4ab6f8

AP0 MANIFEST SHA256 =
62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce

AP0 TRANSFORMATION IMPLEMENTATION =
42fcb38809a1cc0365cd4027fae5154e1d6d3b4f

BEPD-02 HISTORICAL LEDGER BUILD ENGINE =
99279c2bf252105744a18eb721f2fefe9ef883e8
```

Toute divergence matérielle d’identité doit produire :

```text
FAIL CLOSED
```

## 2. OBJECTIF EXCLUSIF

L’objectif exclusif de `BEPD-07A` est de définir, qualifier et geler **avant toute exposition d’excursion réelle** la géométrie canonique de la trajectoire post-sweep permettant ultérieurement de mesurer :

```text
MAX_REINTEGRATIVE_EXCURSION

MAX_EXTERNAL_EXCURSION
```

Ces mesures correspondent conceptuellement à un MFE/MAE comportemental mais ne constituent PAS des métriques de trade.

`BEPD-07A` ne doit calculer aucune excursion réelle sur les 472 événements.

## 3. PRIMARY POPULATION

La population primaire candidate doit rester :

```text
ALL QUALIFIED BEPD-02 EVENT_LEDGER EVENTS

EXPECTED N =
472

UNIT =
ONE QUALIFIED LEVEL_SWEEP_EVENT

FILTERING =
NONE
```

Aucun conditionnement sur :

```text
same_week_reintegration

close_displacement

HIGH / LOW

take day

age

month

year

regime
```

n’est autorisé pour la première surface globale.

## 4. CAUSAL / POST-EVENT ANCHOR

L’ancre de prix primaire doit être :

```text
ANCHOR =
take_h1_close_mid
```

et le temps de disponibilité de départ :

```text
EVENT CONFIRMATION TIME =
take_h1_close_utc
```

La raison sémantique est :

```text
POST-SWEEP RESPONSE
MUST BEGIN AFTER
THE QUALIFYING H1 SWEEP CONFIRMATION
```

Par conséquent :

```text
level_price_mid
!=
PRIMARY EXCURSION ANCHOR
```

dans cette première analyse.

L’utilisation de `level_price_mid` comme ancre d’excursion nécessiterait une décision humaine distincte.

## 5. PATH START

Afin de préserver la frontière d’ambiguïté intrabar déjà reconnue par BEPD-00 :

```text
PATH START =
FIRST QUALIFIED AP0 MINUTE
STRICTLY AFTER take_h1_close_utc
```

La minute appartenant au H1 ayant confirmé le sweep ne doit PAS contribuer aux excursions post-événement.

Donc :

```text
TAKE H1 INTERNAL PATH =
EXCLUDED

SAME-H1 EXCURSION =
FORBIDDEN
```

## 6. PATH END

Pour chacun des 472 événements :

```text
PATH END =
END OF THE SAME CANONICAL TARGET WEEK
```

La borne doit être reconstruite exclusivement selon les sémantiques de semaine déjà utilisées par le moteur historique BEPD-02.

La semaine canonique reste fondée sur :

```text
SESSION WEEK START =
SUNDAY 18:00
America/New_York

TARGET WEEK END =
START + 7 DAYS

INTERVAL =
[start_utc, end_utc)
```

La trajectoire candidate utilise donc :

```text
minute_start_ms_utc > take_h1_close_utc

AND

minute_start_ms_utc < target_week_end_utc
```

sur les observations AP0 qualifiées.

Aucune borne dépendant du résultat de réintégration n’est autorisée dans cette première analyse.

En particulier :

```text
PATH END
!=
reintegration_h1_close_utc
```

Cette première surface mesure donc :

```text
SAME-WEEK POST-SWEEP PATH
```

et non :

```text
PRE-REINTEGRATION PATH
```

## 7. EMPTY PATH HANDLING

Si un événement ne possède aucune observation AP0 strictement postérieure à `take_h1_close_utc` avant la fin de semaine cible :

```text
FAIL CLOSED
```

Il est interdit de lui attribuer silencieusement :

```text
ZERO EXCURSION

NULL-AS-ZERO

ARTIFICIAL PATH

FORWARD-FILLED PATH
```

Une telle situation nécessiterait une adjudication séparée.

## 8. QUALIFIED PRICE PRIMITIVES

Les seules primitives autorisées pour les extrema sont les champs AP0 qualifiés :

```text
mid_high
mid_low
```

dont la provenance reste :

```text
mid =
(bid_price + ask_price) / 2
```

et :

```text
MID PRICE =
DESCRIPTIVE ONLY

MID PRICE != EXECUTION PRICE
```

Il est interdit de substituer :

```text
BID-ONLY EXTREMA

ASK-ONLY EXTREMA

EXECUTION PRICE

BAR CLOSE ONLY

H1 HIGH / LOW RECONSTRUCTION

INTERPOLATED PRICES
```

sans nouvelle autorisation.

## 9. CANONICAL BEHAVIORAL DIRECTIONS

Les directions doivent être orientées par rapport à la logique comportementale de réintégration du niveau sweepé.

Pour un événement :

```text
SIDE = HIGH
```

la direction réintégrative est :

```text
DOWN
```

et la direction externe est :

```text
UP
```

Pour :

```text
SIDE = LOW
```

la direction réintégrative est :

```text
UP
```

et la direction externe est :

```text
DOWN
```

Ces termes décrivent une géométrie de prix.

Ils ne signifient PAS :

```text
LONG
SHORT
PROFIT
LOSS
WIN
RISK/REWARD
```

## 10. MAX REINTEGRATIVE EXCURSION

La première métrique canonique candidate est :

```text
MAX_REINTEGRATIVE_EXCURSION
```

toujours non négative.

Pour :

```text
HIGH
```

elle doit être définie comme :

```text
MAX_REINTEGRATIVE_EXCURSION =
max(
    0,
    take_h1_close_mid
    -
    minimum observed AP0 mid_low
    within the frozen post-sweep path window
)
```

Pour :

```text
LOW
```

elle doit être :

```text
MAX_REINTEGRATIVE_EXCURSION =
max(
    0,
    maximum observed AP0 mid_high
    within the frozen post-sweep path window
    -
    take_h1_close_mid
)
```

## 11. MAX EXTERNAL EXCURSION

La seconde métrique canonique candidate est :

```text
MAX_EXTERNAL_EXCURSION
```

toujours non négative.

Pour :

```text
HIGH
```

elle doit être :

```text
MAX_EXTERNAL_EXCURSION =
max(
    0,
    maximum observed AP0 mid_high
    within the frozen post-sweep path window
    -
    take_h1_close_mid
)
```

Pour :

```text
LOW
```

elle doit être :

```text
MAX_EXTERNAL_EXCURSION =
max(
    0,
    take_h1_close_mid
    -
    minimum observed AP0 mid_low
    within the frozen post-sweep path window
)
```

## 12. MFE / MAE NAMING BOUNDARY

Pour éviter tout laundering vers des métriques de trading :

```text
CANONICAL NAME 1 =
MAX_REINTEGRATIVE_EXCURSION

CANONICAL NAME 2 =
MAX_EXTERNAL_EXCURSION
```

Les termes :

```text
MFE
MAE
```

peuvent uniquement être utilisés comme raccourcis explicatifs précédés de :

```text
BEHAVIORAL
```

et doivent conserver :

```text
BEHAVIORAL MFE
!=
TRADE MFE

BEHAVIORAL MAE
!=
TRADE MAE
```

Aucune position ou direction de trade n’existe dans `BEPD-07A`.

## 13. GAP SEMANTICS

Le corpus AP0 est gap-aware.

Il est interdit de :

```text
FORWARD FILL

BACKFILL

INTERPOLATE

SYNTHESIZE UNOBSERVED EXTREMA
```

La sémantique doit donc rester :

```text
OBSERVED MAX REINTEGRATIVE EXCURSION

OBSERVED MAX EXTERNAL EXCURSION
```

et non :

```text
TRUE CONTINUOUS-MARKET MAXIMUM
```

Toute future exécution doit préserver les diagnostics de gap nécessaires à la qualification.

```text
UNOBSERVED PATH
!=
OBSERVED FLAT PATH
```

## 14. FIRST REAL AGGREGATION SURFACE

Pour chacune des deux métriques :

```text
MAX_REINTEGRATIVE_EXCURSION

MAX_EXTERNAL_EXCURSION
```

la première surface globale candidate à geler est exclusivement :

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

ZERO COUNT

ZERO FRACTION

EMPIRICAL CDF
```

avec :

```text
QUANTILE METHOD =
HYNDMAN-FAN TYPE 7

P50 =
MEDIAN

ECDF =
EXACT / UNSMOOTHED / UNBINNED
```

Aucune relation entre les deux excursions ne doit encore être calculée.

## 15. NO JOINT / DERIVED METRICS

La première exécution future ne doit PAS produire :

```text
MFE / MAE RATIO

REINTEGRATIVE / EXTERNAL RATIO

NET EXCURSION

EXCURSION DIFFERENCE

PATH EFFICIENCY

REVERSAL SCORE

RISK/REWARD

STOP DISTANCE

TARGET DISTANCE

TP

SL

RETURN

PNL
```

Ces transformations nécessitent une décision humaine distincte.

## 16. NO SUBGROUPS

Aucune segmentation n’est autorisée par :

```text
HIGH / LOW

SAME_WEEK_REINTEGRATION TRUE / FALSE

CLOSE_DISPLACEMENT SIGN

CLOSE_DISPLACEMENT MAGNITUDE

TIME-TO-REINTEGRATION

LEVEL AGE

TAKE DAY

MONTH / YEAR

VOLATILITY

REGIME

SWEEP CLUSTER SIZE

OTHER CONTEXT

INTERACTIONS
```

## 17. DEPENDENCE

Le contrat doit maintenir :

```text
EVENT != IID OBSERVATION

DEPENDENCE KEYS INCLUDE =
target_week_id
sweep_cluster_id
```

La première surface restera descriptive.

Aucune méthode d’incertitude IID ne doit être ajoutée implicitement.

## 18. REQUIRED BREAKER COVERAGE

Un frozen adversarial breaker doit au minimum faire échouer :

```text
wrong AP0 identity

wrong EVENT_LEDGER identity

using level_price_mid as primary anchor

including the sweep-confirming H1 path

starting before or at take_h1_close_utc

outcome-dependent path endpoint

ending at reintegration_h1_close_utc

using a fixed horizon selected post-hoc

using bid-only or ask-only extrema

using mid_close instead of mid_high / mid_low for extrema

HIGH / LOW direction inversion

reintegrative / external semantic inversion

negative excursion output

dropping no-reintegration events

conditioning on same_week_reintegration

gap interpolation

forward fill across gaps

unobserved-path → zero-excursion laundering

observed extrema → continuous-market extrema laundering

mid-price → execution-price laundering

behavioral MFE/MAE → trade MFE/MAE laundering

subgroup introduction

joint MFE/MAE ratio introduction

post-hoc threshold selection

IID laundering

excursion distribution → prediction laundering

excursion distribution → edge laundering

excursion distribution → strategy validation laundering

excursion distribution → PnL laundering

excursion distribution → trading-authority laundering
```

## 19. EXPLICITLY OUT OF SCOPE

`BEPD-07A` n’autorise PAS :

```text
REAL EXCURSION CALCULATION

REAL MFE / MAE DISTRIBUTION EXPOSURE

EVENT-LEVEL DERIVED PATH LEDGER
AS A NEW CANONICAL PRODUCT

PRE-REINTEGRATION-SPECIFIC EXCURSION

FIXED-HORIZON EXCURSION

MFE × MAE ANALYSIS

TIMING × EXCURSION

CLOSE-DISPLACEMENT × EXCURSION

HIGH / LOW SEGMENTATION

REINTEGRATION TRUE / FALSE SEGMENTATION

SURVIVAL ANALYSIS

OCCURRENCE × RESPONSE

THRESHOLD SEARCH

PARAMETER OPTIMIZATION

OOS CONSUMPTION

PREDICTION

CAUSATION

EDGE

STRATEGY VALIDATION

TP / SL

PNL

TRADING AUTHORITY

CAPITAL DEPLOYMENT
```

## 20. SCIENTIFIC STATUS

Le contrat doit préserver :

```text
HISTORICAL CORPUS =
ALREADY EXPOSED

ANALYSIS STATUS =
EXPLORATORY_ONLY

PRICE SURFACE =
MID / DESCRIPTIVE_ONLY

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

## 21. REQUIRED QUALIFICATION

Avant toute première exécution réelle d’excursion :

```text
SOURCE IDENTITIES =
EXACT

BASE POPULATION =
472 / FROZEN

ANCHOR =
take_h1_close_mid / FROZEN

PATH START =
STRICTLY AFTER take_h1_close_utc / FROZEN

PATH END =
TARGET WEEK END / FROZEN

PRICE PRIMITIVES =
AP0 mid_high + mid_low / FROZEN

REINTEGRATIVE DIRECTION =
FROZEN

EXTERNAL DIRECTION =
FROZEN

GAP SEMANTICS =
OBSERVED ONLY / FROZEN

MFE / MAE TRADE SEMANTICS =
FORBIDDEN

AGGREGATION SURFACE =
FROZEN

SUBGROUP AUTHORITY =
NONE

OOS AUTHORITY =
NONE

PREDICTION AUTHORITY =
NONE

EDGE AUTHORITY =
NONE

TRADING AUTHORITY =
NONE

NEW REAL PATH ANALYTICS EXECUTED =
NO
```

Le breaker doit être qualifié avant toute exposition réelle.

## 22. STOP BOUNDARY

Si la sémantique, la fenêtre, les directions, la gestion des gaps, la surface d’agrégation et le breaker sont qualifiés :

```text
BEPD-07A =
QUALIFIED_FOR_HUMAN_ADOPTION
```

mais :

```text
HUMAN ADOPTION =
NOT AUTOMATIC

REAL EXCURSION EXECUTION =
NOT AUTHORIZED

REAL MFE / MAE RESULT =
NOT PRODUCED
```

La prochaine action requise doit être exclusivement :

```text
HUMAN ADJUDICATION OF BEPD-07A
```

et seulement après cette adjudication pourra être préparée une autorisation distincte pour la première exécution réelle globale des excursions.

```text
STOP.
```
