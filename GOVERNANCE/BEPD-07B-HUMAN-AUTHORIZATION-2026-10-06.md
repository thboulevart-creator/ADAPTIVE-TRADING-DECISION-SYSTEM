J’autorise l’ouverture et l’exécution de :

`BEPD-07B — FIRST REAL GLOBAL BEHAVIORAL EXCURSION DISTRIBUTIONS + TECHNICAL QUALIFICATION V0.1`

sur le dépôt gouverné :

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

REFERENCE HEAD =
377b98435cb77016893c5f8bfcff307a05c07d93

REFERENCE TREE =
28c196ab71db32d927f73109ad7785524ebeb936
```

Cette référence ne dispense PAS d’un preflight frais avant toute mutation ou exécution.

## 1. BINDING PRIOR AUTHORITY

Je reconnais comme autorités scientifiques binding :

```text
BEPD-07A FINAL HUMAN ADJUDICATION =
5b8a8c9538363f8878acfa47c75db420438582be

BEPD-07A PATH GEOMETRY + BEHAVIORAL EXCURSION CONTRACT =
d7b3aeed923a91e0e2aac530a952978c1f8fa5d6

BEPD-07A FROZEN PRE-RESULT BREAKER =
42f2a720a0904c83c45a507cfa340af30ba73ae5

BEPD-07A PRE-RESULT FREEZE =
10fa2fc9011dded1567a054efb31fbabfa6dab8a

BEPD-07A QUALIFICATION RECEIPT =
36fd2571cf5fe22d3ec0d404c6f50dbceab2b25f

BEPD-07A QUALIFICATION REPORT =
e48a5d8ad342ad057d3509935bf8daab86534cd8
```

Je reconnais comme sources binding :

```text
BEPD-02 EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2

AP0 USTECH PROFILE MINUTE CORE ADJUDICATION =
94bba3315e3569993623b8cd2a2bf4264f4ab6f8

AP0 TRANSFORMATION IMPLEMENTATION =
42fcb38809a1cc0365cd4027fae5154e1d6d3b4f

AP0 DATASET ID =
USTECH_PROFILE_MINUTE_CORE_V0_1

AP0 MANIFEST SHA256 =
62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce

BEPD-02 HISTORICAL LEDGER BUILD ENGINE =
99279c2bf252105744a18eb721f2fefe9ef883e8
```

## 2. OPERATIONAL AP0 RESOURCE BINDINGS

Je reconnais également comme bindings opérationnels de lecture :

```text
RVO-08 AP0 RESOURCE CONTRACT =
23cef7d6dcc6ca0b4e3c72bd8f3af4e91b1d6ca3

DATA-02 REAL AP0 READ-ONLY ADMISSION RECEIPT =
ccfccda676abfe7e02082a331557ffed14e1f32b
```

L’environnement qualifié a vérifié :

```text
AP0 FILE COUNT =
61

AP0 ROW COUNT =
1709180

AP0 FILE-SET DIGEST =
1ff14ab4fea11c2480088a322f5bec23ea183de14cbc65ee6c684c7ea185062a

AP0 EXACT MANIFEST =
62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce
```

Ces bindings autorisent l’accès read-only au corpus exact.

Ils ne créent PAS :

```text
NEW SCIENTIFIC AUTHORITY

TEMPORAL AUTHORITY

PREDICTION AUTHORITY

TRADING AUTHORITY
```

Toute divergence d’identité matérielle doit produire :

```text
FAIL CLOSED
```

## 3. OBJECTIF EXCLUSIF

L’objectif exclusif de `BEPD-07B` est de produire une seule première exécution réelle globale des deux métriques comportementales gelées :

```text
MAX_REINTEGRATIVE_EXCURSION

MAX_EXTERNAL_EXCURSION
```

sur :

```text
ALL 472 QUALIFIED BEPD-02 SWEEP EVENTS
```

sans filtrage ni sous-groupe.

La phase doit répondre exclusivement à :

```text
AFTER A QUALIFIED HISTORICAL SWEEP
AND AFTER ITS H1 CONFIRMATION,

HOW FAR DID THE OBSERVED MID PRICE
MOVE IN THE REINTEGRATIVE DIRECTION

AND

HOW FAR DID THE OBSERVED MID PRICE
MOVE IN THE EXTERNAL DIRECTION

BEFORE THE END OF THE SAME TARGET WEEK?
```

## 4. BASE POPULATION

La population doit être vérifiée avant tout scan réel :

```text
BASE_N =
472

UNIT =
ONE QUALIFIED LEVEL_SWEEP_EVENT

FILTERING =
NONE

WEIGHTING =
ONE EQUAL WEIGHT PER QUALIFIED EVENT
```

Il est interdit d’exclure ou de conditionner les événements selon :

```text
same_week_reintegration

close_displacement

HIGH / LOW

time-to-reintegration

take day

level age

month / year

volatility

regime

sweep cluster size
```

Les 102 événements n’ayant pas réintégré dans la semaine restent donc intégralement inclus.

## 5. ANCHOR

Pour chaque événement :

```text
PRICE ANCHOR =
take_h1_close_mid

EVENT CONFIRMATION TIME =
take_h1_close_utc
```

Il est interdit d’utiliser :

```text
level_price_mid

take_h1_open

take_h1_high

take_h1_low

execution price

bid-only price

ask-only price
```

comme ancre primaire de cette première surface.

## 6. PATH START

La trajectoire réelle commence exclusivement à :

```text
FIRST QUALIFIED AP0 MINUTE
STRICTLY AFTER take_h1_close_utc
```

donc :

```text
minute_start_ms_utc > take_h1_close_utc
```

La trajectoire interne au H1 ayant confirmé le sweep est exclue.

```text
TAKE-H1 INTERNAL PATH =
EXCLUDED

SAME-H1 EXCURSION =
FORBIDDEN
```

## 7. PATH END

La trajectoire se termine exclusivement à :

```text
END OF THE SAME CANONICAL TARGET WEEK
```

selon les sémantiques gelées :

```text
SESSION WEEK START =
SUNDAY 18:00 America/New_York

TARGET WEEK END =
SESSION WEEK START + 7 LOCAL CALENDAR DAYS

WINDOW =
[target_week_start_utc, target_week_end_utc)
```

Pour le scan post-sweep :

```text
minute_start_ms_utc > take_h1_close_utc

AND

minute_start_ms_utc < target_week_end_utc
```

La fin de trajectoire ne doit dépendre d’aucun outcome.

En particulier :

```text
PATH END
!=
reintegration_h1_close_utc
```

## 8. EMPTY PATH

Chaque événement doit posséder au moins une observation AP0 qualifiée dans sa fenêtre post-sweep.

Sinon :

```text
FAIL CLOSED
```

Il est interdit de convertir un chemin vide en :

```text
ZERO EXCURSION

NULL-AS-ZERO

ARTIFICIAL PATH

IMPUTED PATH
```

## 9. PRICE PRIMITIVES

Les extrema doivent être obtenus exclusivement à partir des primitives AP0 qualifiées :

```text
mid_high
mid_low
```

avec :

```text
mid =
(bid_price + ask_price) / 2
```

et :

```text
MID PRICE =
DESCRIPTIVE_ONLY

MID PRICE != EXECUTION PRICE
```

Il est interdit de substituer :

```text
mid_close

bid-only extrema

ask-only extrema

H1 extrema

interpolated extrema

synthetic extrema
```

## 10. DIRECTIONAL SEMANTICS

Les orientations restent exactement :

```text
HIGH:

REINTEGRATIVE =
DOWN

EXTERNAL =
UP
```

et :

```text
LOW:

REINTEGRATIVE =
UP

EXTERNAL =
DOWN
```

Ces directions décrivent une géométrie comportementale.

Elles ne constituent PAS :

```text
LONG

SHORT

TRADE DIRECTION

PROFIT

LOSS

WIN

RISK/REWARD
```

## 11. MAX_REINTEGRATIVE_EXCURSION

Pour :

```text
SIDE = HIGH
```

calculer exclusivement :

```text
MAX_REINTEGRATIVE_EXCURSION =
max(
    0,
    take_h1_close_mid
    -
    minimum observed AP0 mid_low
    within the frozen post-sweep path
)
```

Pour :

```text
SIDE = LOW
```

calculer exclusivement :

```text
MAX_REINTEGRATIVE_EXCURSION =
max(
    0,
    maximum observed AP0 mid_high
    within the frozen post-sweep path
    -
    take_h1_close_mid
)
```

## 12. MAX_EXTERNAL_EXCURSION

Pour :

```text
SIDE = HIGH
```

calculer exclusivement :

```text
MAX_EXTERNAL_EXCURSION =
max(
    0,
    maximum observed AP0 mid_high
    within the frozen post-sweep path
    -
    take_h1_close_mid
)
```

Pour :

```text
SIDE = LOW
```

calculer exclusivement :

```text
MAX_EXTERNAL_EXCURSION =
max(
    0,
    take_h1_close_mid
    -
    minimum observed AP0 mid_low
    within the frozen post-sweep path
)
```

Les deux métriques doivent toujours satisfaire :

```text
VALUE >= 0
```

## 13. GAP SEMANTICS

Le corpus AP0 doit rester utilisé tel qu’observé.

```text
FORWARD FILL =
FORBIDDEN

BACKFILL =
FORBIDDEN

INTERPOLATION =
FORBIDDEN

SYNTHETIC UNOBSERVED EXTREMA =
FORBIDDEN
```

La revendication canonique doit rester :

```text
OBSERVED MAX REINTEGRATIVE EXCURSION

OBSERVED MAX EXTERNAL EXCURSION
```

et non :

```text
TRUE CONTINUOUS-MARKET MAXIMUM
```

## 14. REQUIRED GAP / PATH DIAGNOSTICS

Pour qualifier le scan réel sans créer un nouveau ledger canonique d’événements, l’exécution doit vérifier au minimum pour chacun des 472 événements :

```text
PATH OBSERVATION COUNT > 0

PATH FIRST OBSERVED MINUTE

PATH LAST OBSERVED MINUTE

INTERNAL GAP COUNT > 60s

MAX OBSERVED INTERNAL GAP MS

SOURCE FILE BINDING
```

L’implémentation peut conserver ces valeurs transitoirement pendant l’exécution.

Mais :

```text
EVENT-LEVEL DERIVED PATH LEDGER
AS A NEW CANONICAL PRODUCT =
NOT AUTHORIZED
```

La persistance canonique doit rester limitée aux agrégats autorisés, diagnostics de qualification nécessaires et preuves de provenance.

## 15. REAL AGGREGATION SURFACE

Pour chacune des deux métriques, produire exclusivement :

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

pour chacune des deux métriques, sauf FAIL CLOSED.

## 16. NUMERICAL CONTRACT

Le contrat numérique est :

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

Pour chaque ECDF :

```text
FINAL CUMULATIVE COUNT =
472

FINAL CUMULATIVE FRACTION =
1
```

## 17. ZERO SEMANTICS

Une excursion égale à zéro est autorisée uniquement lorsque les extrema effectivement observés dans la fenêtre frozen ne dépassent pas l’ancre dans la direction correspondante.

```text
OBSERVED ZERO EXCURSION =
VALID

MISSING PATH → ZERO =
FORBIDDEN
```

`ZERO_COUNT` et `ZERO_FRACTION` doivent donc refléter uniquement de vrais zéros observés selon les formules gelées.

## 18. IMPLEMENTATION QUALIFICATION BEFORE REAL EXPOSURE

Avant tout scan réel AP0, la phase doit pouvoir construire et qualifier :

```text
DETERMINISTIC PATH SCANNER

DETERMINISTIC EXCURSION AGGREGATOR

INDEPENDENT RECOMPUTATION IMPLEMENTATION

EXECUTABLE OR EXECUTABLE-EQUIVALENT
BEPD-07A BREAKER

SYNTHETIC PATH FIXTURES

SYNTHETIC GAP FIXTURES

SYNTHETIC DST / WEEK-BOUNDARY FIXTURES

RESULT SERIALIZATION

RUN MANIFEST

TECHNICAL QUALIFICATION RECEIPT
```

La première qualification doit utiliser uniquement :

```text
SYNTHETIC DATA

CONTRACTUAL METADATA

FROZEN SOURCE IDENTITIES
```

et doit encore satisfaire :

```text
REAL AP0 PATH SCAN =
NOT EXECUTED

REAL EXCURSION STATISTICS =
NOT CALCULATED

REAL EXCURSION DISTRIBUTION EXPOSURE =
NO
```

## 19. MINIMUM SYNTHETIC TEST COVERAGE

La qualification pré-résultat doit couvrir au minimum :

```text
HIGH reintegrative formula

HIGH external formula

LOW reintegrative formula

LOW external formula

nonnegative floor at zero

strict post-take path start

same-H1 exclusion

target-week-end exclusion

America/New_York DST boundary handling

empty-path fail closed

mid_high / mid_low primitive enforcement

mid_close substitution rejection

HIGH / LOW inversion rejection

outcome-dependent endpoint rejection

gap interpolation rejection

forward-fill rejection

missing path != zero path

Type-7 quantiles

P50 = median

exact ECDF terminal count

zero-count semantics

base N integrity

no subgroup output

no joint metric output
```

## 20. FROZEN BREAKER REQUALIFICATION

Les 40 failure modes de `BEPD-07A` doivent être rendus exécutables ou couverts par une vérification exécutable équivalente.

```text
BREAKER CASES =
40 / 40 REQUIRED
```

Aucun cas ne peut être supprimé, affaibli ou transformé en warning.

## 21. EXACT REAL EXECUTION FREEZE

Si et seulement si l’implémentation pré-résultat est qualifiée, persister avant le premier scan réel un freeze liant exactement :

```text
BEPD-07B HUMAN AUTHORIZATION

BEPD-07A FINAL HUMAN ADJUDICATION

BEPD-07A CONTRACT

BEPD-07A BREAKER

BEPD-07A PRE-RESULT FREEZE

BEPD-07B RUNNER

INDEPENDENT RECOMPUTATION IMPLEMENTATION

EXECUTABLE BREAKER

SYNTHETIC TESTS

IMPLEMENTATION QUALIFICATION RECEIPT

AP0 MANIFEST IDENTITY

AP0 FILE-SET IDENTITY

BEPD-02 EVENT_LEDGER IDENTITY

BEPD-02 HISTORICAL BUILD ENGINE IDENTITY
```

Toute divergence après ce freeze entraîne :

```text
FAIL CLOSED
```

## 22. FIRST REAL EXECUTION AUTHORITY

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
ONE FIRST REAL GLOBAL
BEHAVIORAL EXCURSION EXECUTION =
AUTHORIZED
```

Cette autorisation vaut pour **un unique scan canonique** du corpus AP0 afin de produire simultanément :

```text
GLOBAL MAX_REINTEGRATIVE_EXCURSION DISTRIBUTION

GLOBAL MAX_EXTERNAL_EXCURSION DISTRIBUTION
```

sur les mêmes 472 événements.

## 23. AP0 PROVENANCE REQUALIFICATION BEFORE READ

Avant toute lecture des prix réels :

```text
AP0 DATASET ID =
USTECH_PROFILE_MINUTE_CORE_V0_1

MANIFEST SHA256 =
62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce

FILE COUNT =
61
```

doivent être exacts.

Les 61 fichiers AP0 doivent être vérifiés contre le manifest avant consommation.

Le file-set doit être compatible avec l’identité admise :

```text
FILE-SET DIGEST =
1ff14ab4fea11c2480088a322f5bec23ea183de14cbc65ee6c684c7ea185062a
```

ou, si le mécanisme de qualification reconstruit une identité canonique équivalente selon un contrat déjà adopté, cette équivalence doit être démontrée explicitement avant lecture.

Aucune réparation, tri, déduplication, interpolation ou mutation du corpus n’est autorisée.

## 24. INDEPENDENT RECOMPUTATION

Après la première exécution réelle :

```text
INDEPENDENT RECOMPUTATION =
REQUIRED
```

L’implémentation indépendante doit :

```text
NOT IMPORT THE CANONICAL RUNNER

REIMPLEMENT THE FROZEN FORMULAS

RECONSTRUCT THE FROZEN PATH WINDOWS INDEPENDENTLY

READ THE SAME EXACT AP0 IDENTITY

READ THE SAME EXACT 472 EVENTS
```

Elle doit obtenir une parité exacte sur toute la surface canonique :

```text
MAX_REINTEGRATIVE_EXCURSION AGGREGATES

MAX_EXTERNAL_EXCURSION AGGREGATES

ZERO COUNTS

ZERO FRACTIONS

ALL QUANTILES

FULL ECDFS
```

Toute divergence :

```text
FAIL CLOSED
```

## 25. DETERMINISTIC REPLAY

Une seconde exécution du **même runner, mêmes entrées, mêmes bindings** est autorisée uniquement comme preuve de reproductibilité :

```textDETERMINISTIC REPLAY =
REQUIRED
```

avec :

```text
EXACT BYTE OR EXACT CANONICAL OBJECT PARITY =
REQUIRED
```

et :

```text
REPLAY =
REPRODUCIBILITY EVIDENCE

REPLAY != NEW INDEPENDENT EVIDENCE
```

## 26. REQUIRED REAL-RESULT VALIDATIONS

La qualification du résultat réel doit vérifier au minimum :

```text
EVENT_LEDGER IDENTITY =
EXACT

AP0 MANIFEST IDENTITY =
EXACT

AP0 FILE COUNT =
61

AP0 FILE IDENTITIES =
PASS

BASE EVENT COUNT =
472

PATH EVENT COUNT =
472

DUPLICATE EVENT IDS =
0

EMPTY PATH EVENTS =
0 REQUIRED

FILTERED EVENTS =
0

ANCHOR =
take_h1_close_mid

PATH START RULE =
STRICTLY AFTER take_h1_close_utc

PATH END RULE =
TARGET WEEK END

OUTCOME-DEPENDENT ENDPOINTS =
0

mid_high / mid_low USAGE =
PASS

FORWARD FILLED VALUES =
0

INTERPOLATED VALUES =
0

NEGATIVE REINTEGRATIVE EXCURSIONS =
0

NEGATIVE EXTERNAL EXCURSIONS =
0

REINTEGRATIVE N =
472

EXTERNAL N =
472

P50 = MEDIAN =
PASS FOR BOTH

TYPE-7 QUANTILES =
PASS FOR BOTH

ECDF TERMINAL COUNT =
472 FOR BOTH

ECDF TERMINAL FRACTION =
1 FOR BOTH

INDEPENDENT RECOMPUTATION =
EXACT PARITY

DETERMINISTIC REPLAY =
EXACT PARITY
```

## 27. NO JOINT METRICS

Même si les deux métriques sont calculées événement par événement pour permettre l’agrégation, la première surface canonique ne doit pas produire :

```text
MFE / MAE RATIO

REINTEGRATIVE / EXTERNAL RATIO

EXCURSION DIFFERENCE

NET EXCURSION

PATH EFFICIENCY

REVERSAL SCORE

CORRELATION BETWEEN EXCURSIONS

JOINT DISTRIBUTION

2D HISTOGRAM

DOMINANCE RATE

RISK/REWARD
```

## 28. NO SUBGROUPS

Aucune sortie segmentée n’est autorisée pour :

```text
HIGH / LOW

REINTEGRATION TRUE / FALSE

CLOSE_DISPLACEMENT SIGN

CLOSE_DISPLACEMENT MAGNITUDE

TIME-TO-REINTEGRATION

TAKE DAY

LEVEL AGE

MONTH / YEAR

REGIME

VOLATILITY

SWEEP CLUSTER SIZE

OTHER CONTEXT
```

## 29. DEPENDENCE BOUNDARY

Le résultat demeure descriptif sur un corpus historique exposé.

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

## 30. MID / TRADING BOUNDARY

Les résultats doivent porter explicitement :

```text
PRICE SURFACE =
MID / DESCRIPTIVE_ONLY

MID PRICE != EXECUTION PRICE

BEHAVIORAL EXCURSION != TRADE EXCURSION
```

Il est interdit d’interpréter :

```text
MAX_REINTEGRATIVE_EXCURSION
```

comme profit potentiel d’un trade,

ou :

```text
MAX_EXTERNAL_EXCURSION
```

comme perte potentielle d’un trade.

Aucune entrée, direction de trade, spread, slippage, commission, TP ou SL n’est définie.

## 31. CANONICAL PERSISTENCE SURFACE

Si l’exécution réelle est qualifiée, persister au minimum :

```text
CANONICAL GLOBAL EXCURSION RESULT

RUN MANIFEST

INDEPENDENT RECOMPUTATION RESULT

DETERMINISTIC REPLAY EVIDENCE

PATH / GAP QUALIFICATION DIAGNOSTICS

TECHNICAL EXECUTION RECEIPT

REAL RESULT QUALIFICATION RECEIPT

REAL RESULT QUALIFICATION REPORT

PERSISTED-HEAD VERIFICATION
```

Il est interdit de promouvoir comme nouveau dataset canonique un fichier ligne-par-ligne des 472 excursions sans nouvelle autorisation humaine.

## 32. EVIDENCE STATUS

Tout résultat réel doit rester :

```text
EVIDENCE STATUS =
EXPOSED_EXPLORATORY_ONLY

HISTORICAL CORPUS =
ALREADY EXPOSED

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

## 33. EXPLICITLY OUT OF SCOPE

Cette autorisation n’autorise PAS :

```text
MFE × MAE ANALYSIS

MFE / MAE RATIO

TIMING × EXCURSION

CLOSE-DISPLACEMENT × EXCURSION

HIGH / LOW SEGMENTATION

REINTEGRATION TRUE / FALSE SEGMENTATION

PRE-REINTEGRATION-SPECIFIC EXCURSION

FIXED-HORIZON EXCURSION

SURVIVAL ANALYSIS

OCCURRENCE × RESPONSE

CONTEXT RANKING

POSITIVE-RELATION SEARCH

POST-HOC THRESHOLD SEARCH

PARAMETER OPTIMIZATION

OOS CONSUMPTION

PREDICTION

CAUSATION

EDGE

STRATEGY VALIDATION

TRADE ENTRY

TRADE DIRECTION

TP / SL

PNL

TRADING AUTHORITY

CAPITAL DEPLOYMENT
```

## 34. TECHNICAL TERMINAL STATE

Si l’exécution, la recomputation indépendante, le replay et la persistance sont tous qualifiés :

```text
BEPD-07B =
FIRST REAL GLOBAL
BEHAVIORAL EXCURSION DISTRIBUTIONS
TECHNICALLY QUALIFIED
```

mais :

```text
RESULT HUMAN_ADOPTED =
NO

JOINT EXCURSION FRONTIER =
NOT OPENED

SUBGROUP FRONTIER =
NOT OPENED

TIMING × EXCURSION FRONTIER =
NOT OPENED

OCCURRENCE × RESPONSE FRONTIER =
NOT OPENED

OOS FRONTIER =
NOT OPENED

NEXT SCIENTIFIC FRONTIER =
NOT AUTOMATICALLY OPENED
```

## 35. STOP BOUNDARY

Après la première exécution réelle, sa qualification, la recomputation indépendante, le replay et la vérification persisted-head :

```text
STOP
```

La prochaine action requise doit être exclusivement :

```text
HUMAN ADJUDICATION
OF THE FIRST REAL GLOBAL
BEHAVIORAL EXCURSION DISTRIBUTIONS
```

Aucune segmentation, combinaison, recherche de seuil, analyse de trade ou nouvelle question scientifique ne doit être ouverte automatiquement.
