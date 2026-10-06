J’autorise l’ouverture et l’exécution de :

`BEPD-08B — FIRST REAL GLOBAL ABSOLUTE LEVEL-TO-TARGET-WEEK-CLOSE DISTANCE DISTRIBUTION + TECHNICAL QUALIFICATION V0.1`

sur le dépôt gouverné :

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

REFERENCE HEAD =
72a8569077d3677207a3e8825b51472ed4bb26a2

REFERENCE TREE =
01bf649b4659e22990ebc64410a3a88704b04ab0
```

Cette référence est informative uniquement et ne dispense PAS d’un preflight frais avant toute mutation ou exécution.

## 1. FRESH PREFLIGHT OBLIGATOIRE

Avant toute mutation :

```text
VERIFY EXACT REPOSITORY
VERIFY EXACT BRANCH
FETCH REMOTE
VERIFY FRESH REMOTE HEAD
VERIFY FRESH REMOTE TREE
VERIFY LOCAL / REMOTE STATE AS APPLICABLE
VERIFY NO CONCURRENT MATERIAL BEPD DRIFT
VERIFY NO PRE-EXISTING BEPD-08B RESULT
```

Tout drift concurrent doit être classifié :

```text
MATERIAL_TO_BEPD_08B
or
NON_MATERIAL_TO_BEPD_08B
```

Tout drift matériel non résolu :

```text
FAIL CLOSED
```

## 2. BINDING PRIOR AUTHORITY

Je reconnais comme binding :

```text
BEPD-08A FINAL HUMAN ADJUDICATION =
553fedc2b538a90750839b6fce8edb9619a4dcb7

BEPD-08A ABSOLUTE DISTANCE CONTRACT =
4cfcb983ad64f31b443534d70991f8ddcb11ff8f

BEPD-08A FROZEN PRE-RESULT BREAKER =
4d6ada0758a883ab639c93a6caf388e1e11b6d99

BEPD-08A PRE-RESULT FREEZE =
1b816f5ab7031e40add1d2c515167d5fb1147843

BEPD-08A QUALIFICATION RECEIPT =
c54928c80fc753d1c4eb528781c84157676906fe

BEPD-08A QUALIFICATION REPORT =
60c405f54cc38c8a81f13eb211707a049d00b98d
```

Je reconnais également comme source canonique :

```text
BEPD-02 EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2

SOURCE FIELD =
close_displacement
```

et comme sémantique signée amont :

```text
BEPD-05A CLOSE-DISPLACEMENT CONTRACT =
0a580920ce47885d2bd3277b879b2b888b8d4354

BEPD-05B REAL GLOBAL CLOSE-DISPLACEMENT RESULT =
1280156ca949fc48f00e50240aa09cdae11ba4d7

BEPD-05B FINAL HUMAN ADJUDICATION =
811b8e9f58d33cc35c45f714ea99e696d589b147
```

Toute divergence d’identité :

```text
FAIL CLOSED
```

## 3. OBJECTIF EXCLUSIF

L’objectif exclusif de `BEPD-08B` est de produire la première distribution historique globale réelle de :

```text
D_CLOSE =
abs(close_displacement)
```

avec équivalence :

```text
D_CLOSE =
abs(target_week_close_mid - level_price_mid)
```

afin de répondre exclusivement à :

```text
AFTER A QUALIFIED WEEKLY SWEEP,

HOW FAR FROM THE FIXED SWEPT WEEKLY LEVEL
DID THE TARGET-WEEK CLOSE FINISH?
```

## 4. POPULATION

La population réelle doit être exactement :

```text
BASE_N =
472

UNIT =
ONE QUALIFIED LEVEL_SWEEP_EVENT

FILTERING =
NONE

WEIGHTING =
ONE EQUAL WEIGHT PER EVENT
```

Doivent rester inclus :

```text
POSITIVE close_displacement EVENTS

NEGATIVE close_displacement EVENTS

ZERO close_displacement EVENTS

same_week_reintegration = TRUE EVENTS

same_week_reintegration = FALSE EVENTS
```

Aucun filtrage n’est autorisé.

## 5. SOURCE POLICY

La seule source numérique autorisée est :

```text
BEPD-02 EVENT_LEDGER.close_displacement
```

La transformation doit être exclusivement :

```text
D_CLOSE =
abs(close_displacement)
```

Il est interdit de relire ou reconstruire le marché.

Donc :

```text
AP0 READ =
FORBIDDEN

H1 DATA READ =
FORBIDDEN

WEEKLY DATA RECONSTRUCTION =
FORBIDDEN

level_price_mid / target_week_close_mid RECOMPUTATION =
FORBIDDEN FOR PRIMARY EXECUTION

MARKET DATA RECONSTRUCTION =
FORBIDDEN
```

La formule d’équivalence peut être utilisée comme contrôle sémantique documentaire, mais pas pour reconstruire la valeur primaire.

## 6. ROW-LEVEL VALIDATIONS

Avant agrégation :

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

Pour chaque ligne :

```text
D_CLOSE =
abs(close_displacement)

D_CLOSE >= 0
```

Toute violation :

```text
FAIL CLOSED
```

## 7. UNIT SEMANTICS

La sortie reste :

```text
UNIT =
USTECH_PRICE_UNITS_AS_PERSISTED

SEMANTIC =
PRICE DISTANCE
```

Elle ne doit PAS être étiquetée automatiquement comme :

```text
BROKER POINTS

TICKS

PIPS

MONEY

PNL

RISK MULTIPLE
```

## 8. REAL GLOBAL AGGREGATION SURFACE

La première surface réelle autorisée est exclusivement :

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

Aucune métrique supplémentaire ne doit être ajoutée après exposition.

## 9. NUMERICAL CONTRACT

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

L’ECDF doit contenir au minimum :

```text
support_value
support_count
cumulative_count
cumulative_fraction
cumulative_decimal
```

et se terminer par :

```text
FINAL CUMULATIVE COUNT =
472

FINAL CUMULATIVE FRACTION =
1
```

## 10. ZERO SEMANTICS

Un zéro est valide uniquement si :

```text
close_displacement = 0
```

dans le champ persisté.

Il est interdit de créer des zéros via :

```text
ROUNDING

BUCKETING

THRESHOLDING

MISSING DATA

IMPUTATION
```

Le `ZERO_COUNT` de `D_CLOSE` doit être cohérent avec le nombre exact de valeurs signées nulles dans la source.

## 11. IMPLEMENTATION QUALIFICATION BEFORE REAL EXPOSURE

Avant toute agrégation réelle, la phase doit créer et qualifier au minimum :

```text
DETERMINISTIC D_CLOSE RUNNER

INDEPENDENT RECOMPUTATION IMPLEMENTATION

EXECUTABLE OR EXECUTABLE-EQUIVALENT
BEPD-08A BREAKER

SYNTHETIC TEST SUITE

RESULT SERIALIZATION

RUN MANIFEST

IMPLEMENTATION QUALIFICATION RECEIPT

IMPLEMENTATION QUALIFICATION REPORT
```

La qualification pré-résultat doit utiliser exclusivement :

```text
SYNTHETIC DATA

FROZEN IDENTITIES

CONTRACTUAL METADATA
```

et doit encore satisfaire :

```text
REAL EVENT_LEDGER D_CLOSE AGGREGATION =
NOT EXECUTED

REAL D_CLOSE DISTRIBUTION =
NOT EXPOSED
```

## 12. MINIMUM SYNTHETIC TEST COVERAGE

La qualification synthétique doit couvrir au minimum :

```text
positive close_displacement → positive absolute distance

negative close_displacement → same positive absolute distance

zero → zero

D_CLOSE never negative

all rows retained

negative rows not dropped

positive rows not dropped

zero rows not dropped

no-reintegration rows not dropped

event_id uniqueness

missing close_displacement fail closed

non-finite close_displacement fail closed

exact population integrity

Hyndman-Fan Type 7 quantiles

P50 = median

exact ECDF

ECDF terminal count

ECDF terminal fraction

zero-count semantics

18-decimal ROUND_HALF_EVEN serialization

no subgroup output

no sign-conditional output

no threshold output

no broker-point conversion

no TP / SL output

no PnL output
```

## 13. BREAKER REQUALIFICATION

Les 27 failure modes gelés de `BEPD-08A` doivent être rendus exécutables ou couverts par un équivalent exécutable.

```text
BREAKER =
27 / 27 REQUIRED
```

Aucun breaker ne peut être :

```text
REMOVED

WEAKENED

DOWNGRADED TO WARNING
```

## 14. REAL EXECUTION FREEZE

Si et seulement si l’implémentation pré-résultat est qualifiée, persister AVANT l’exposition réelle un freeze liant exactement :

```text
BEPD-08B HUMAN AUTHORIZATION

BEPD-08A FINAL HUMAN ADJUDICATION

BEPD-08A CONTRACT

BEPD-08A BREAKER

BEPD-08A PRE-RESULT FREEZE

BEPD-08B RUNNER

INDEPENDENT RECOMPUTATION IMPLEMENTATION

EXECUTABLE BREAKER

SYNTHETIC TESTS

IMPLEMENTATION QUALIFICATION RECEIPT

EVENT_LEDGER IDENTITY
```

Toute divergence après le freeze :

```text
FAIL CLOSED
```

## 15. FIRST REAL EXECUTION AUTHORITY

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
ONE FIRST REAL GLOBAL D_CLOSE EXECUTION =
AUTHORIZED
```

Cette autorisation couvre un seul calcul canonique de :

```text
D_CLOSE =
abs(close_displacement)
```

sur les 472 lignes du `EVENT_LEDGER`.

Une nouvelle exécution canonique indépendante de cette qualification nécessitera une nouvelle autorisation humaine, à l’exception du replay déterministe prévu ci-dessous.

## 16. INDEPENDENT RECOMPUTATION

Après le résultat réel :

```text
INDEPENDENT RECOMPUTATION =
REQUIRED
```

L’implémentation indépendante doit :

```text
NOT IMPORT THE CANONICAL RUNNER

READ THE SAME EXACT EVENT_LEDGER

READ THE SAME 472 ROWS

REIMPLEMENT abs(close_displacement)

REIMPLEMENT TYPE-7 QUANTILES

REIMPLEMENT THE EXACT ECDF
```

La parité doit être exacte sur :

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

## 17. DETERMINISTIC REPLAY

Une seconde exécution du même runner avec les mêmes entrées est autorisée uniquement comme preuve de reproductibilité.

```text
DETERMINISTIC REPLAY =
REQUIRED

EXACT CANONICAL OBJECT PARITY =
REQUIRED
```

et :

```text
REPLAY != NEW INDEPENDENT EVIDENCE
```

## 18. REQUIRED REAL-RESULT VALIDATIONS

La qualification réelle doit vérifier au minimum :

```text
EVENT_LEDGER IDENTITY =
EXACT

EVENT ROW COUNT =
472

UNIQUE EVENT IDS =
472

MISSING close_displacement =
0

FILTERED ROWS =
0

D_CLOSE N =
472

NEGATIVE D_CLOSE VALUES =
0

D_CLOSE = abs(close_displacement)
FOR ALL 472 =
PASS

P50 = MEDIAN =
PASS

TYPE-7 QUANTILES =
PASS

ECDF FINAL COUNT =
472

ECDF FINAL FRACTION =
1

INDEPENDENT RECOMPUTATION =
EXACT PARITY

DETERMINISTIC REPLAY =
EXACT PARITY
```

## 19. NO SIGN-CONDITIONAL DECOMPOSITION

Cette première distribution doit rester globale.

Il est interdit de produire :

```text
D_CLOSE | close_displacement > 0

D_CLOSE | close_displacement < 0

INTERNAL-SIDE DISTANCE DISTRIBUTION

EXTERNAL-SIDE DISTANCE DISTRIBUTION
```

Ces surfaces constituent une future frontière séparée.

## 20. NO SUBGROUPS

Aucune segmentation n’est autorisée par :

```text
HIGH / LOW

same_week_reintegration

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

## 21. NO THRESHOLD SEARCH

Il est interdit de rechercher après exposition un seuil optimal du type :

```text
50
100
200
300
500
1000
```

ou toute autre distance.

Aucune conclusion du type :

```text
BEST TARGET DISTANCE

OPTIMAL TP

OPTIMAL EXIT

HIGH-PROBABILITY TARGET
```

n’est autorisée par `BEPD-08B`.

## 22. DEPENDENCE BOUNDARY

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

## 23. PERSISTENCE SURFACE

Si le résultat réel est qualifié, persister au minimum :

```text
CANONICAL D_CLOSE RESULT

RUN MANIFEST

INDEPENDENT RECOMPUTATION RESULT

DETERMINISTIC REPLAY EVIDENCE

TECHNICAL EXECUTION RECEIPT

REAL RESULT QUALIFICATION RECEIPT

REAL RESULT QUALIFICATION REPORT

PERSISTED-HEAD VERIFICATION
```

Aucun nouveau dataset ligne-par-ligne dérivé des 472 événements ne doit être promu comme produit canonique sans autorisation distincte.

## 24. EVIDENCE STATUS

Le résultat doit rester :

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

## 25. EXPLICITLY OUT OF SCOPE

Cette autorisation n’autorise PAS :

```text
INTERNAL vs EXTERNAL DISTANCE DECOMPOSITION

HIGH vs LOW ANALYSIS

REINTEGRATION TRUE vs FALSE ANALYSIS

TIMING × DISTANCE

EXCURSION × DISTANCE

OCCURRENCE × RESPONSE

DISTANCE THRESHOLD SEARCH

CONTEXT RANKING

POSITIVE-RELATION SEARCH

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

## 26. TECHNICAL TERMINAL STATE

Si l’exécution réelle, la recomputation indépendante, le replay et la persistance sont tous qualifiés :

```text
BEPD-08B =
FIRST REAL GLOBAL
ABSOLUTE LEVEL-TO-TARGET-WEEK-CLOSE
DISTANCE DISTRIBUTION
TECHNICALLY QUALIFIED
```

mais :

```text
RESULT HUMAN_ADOPTED =
NO

INTERNAL / EXTERNAL DISTANCE FRONTIER =
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

## 27. STOP BOUNDARY

Après :

```text
FIRST REAL EXECUTION

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

La prochaine action requise doit être exclusivement :

```text
HUMAN ADJUDICATION
OF THE FIRST REAL GLOBAL
ABSOLUTE LEVEL-TO-TARGET-WEEK-CLOSE
DISTANCE DISTRIBUTION
```

Aucune décomposition interne/externe, aucun seuil de distance et aucune logique de trading ne doit être ouvert automatiquement.
