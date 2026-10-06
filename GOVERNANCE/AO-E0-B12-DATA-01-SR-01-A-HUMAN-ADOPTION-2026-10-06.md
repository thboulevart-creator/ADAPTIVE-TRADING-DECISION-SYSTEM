J’adopte par décision humaine distincte la relation sémantique qualifiée :

`AO-E0-B12-DATA-01-SR-01 — PATH A — EXACT DETERMINISTIC SOURCE-B ↔ DUKASCOPY SEMANTIC RECONCILIATION`

avec une portée strictement limitée à l’adoption de la relation sémantique démontrée et qualifiée par `SR-01`.

```text
HUMAN_DECISION =
ADOPT

HUMAN_ADJUDICATION =
ADOPT_EXACT_SR01_A_SEMANTIC_RECONCILIATION
```

---

# 1. EXACT ADOPTED STATUS

```text
SR01_A =
HUMAN_ADOPTED / BINDING / FROZEN

SELECTED_PATH =
A

B_PHASE =
NOT_OPENED
```

La branche B n’est pas exécutée, car la condition prospective permettant son ouverture n’a pas été satisfaite.

```text
A =
QUALIFIED_AND_HUMAN_ADOPTED

A_REJECTED_NOT_RECONCILABLE =
FALSE

AUTOMATIC_A_TO_B_TRIGGER =
NOT_TRIGGERED

B =
NOT_OPENED
```

---

# 2. EXACT QUALIFICATION PACKAGE

L’adoption est liée aux artefacts exacts suivants :

```text
SR01_CONTRACT_BLOB =
879843acb871461d357708ee8933282ac3c8a95b

SR01_FROZEN_BREAKERS_BLOB =
497338d9a109701f3481454f2fdebea65db0aedf

SR01_HUMAN_AUTHORIZATION_RECEIPT_BLOB =
60d0c44515fa408200f9e76f017183b64315a0c2

A_TRANSFORMATION_FREEZE_BLOB =
4012c9d101ce2ced09b0efb2914c55385d591fba

A_DISCOVERY_BLOB =
9962165b53253df25858d277f3194a94f471be6b

A_VALIDATION_BLOB =
cca6e91294247d91b4fb15209b2e8e28c19dd2bb

A_FULL_REBREAK_BLOB =
b0ee12b81d9f1bb811dd1eedf61e48f99baaad3a

A_PROVENANCE_RECONCILIATION_BLOB =
aad5897c817571c47f1c0efe09e08f03fc1b4223

A_QUALIFICATION_REPORT_BLOB =
18bce565b1f06d4a89e5bb7377bba50b67ba9852

A_QUALIFICATION_RECEIPT_BLOB =
ad0afe9ed793a06b0265a13e761fc47521f0c073

A_HUMAN_DECISION_PACKET_BLOB =
72b3beb5b6a6f288145e52609f20e8727b720b85
```

---

# 3. HISTORICAL ACQ-01 PRESERVATION

L’adoption de SR-01 A ne réécrit PAS le résultat historique de `ACQ-01`.

```text
ACQ01 =
BLOCKED

EXACT_BLOCKER =
BLOCKED_SOURCE_CONTINUATION_NOT_EXACT
```

Exact blocker historique :

```text
ACQ01_BLOCKER_BLOB =
297e9d6ebbd44cf3a8dd3fabfce942ec5a418bee
```

Ce résultat reste valide dans le domaine de comparaison exact qui l’a produit.

```text
ACQ01_HISTORICAL_RESULT_REWRITTEN =
FALSE
```

```text
ACQ01_BLOCKED
!=
RETROACTIVE_PASS
```

SR-01 constitue une qualification ultérieure et distincte de la **relation sémantique**, fondée sur une représentation numérique canonique preregistrée et validée.

---

# 4. EXACT ADOPTED TRANSFORMATION

J’adopte l’exacte transformation qualifiée :

```text
TRANSFORMATION_ID =
DUKASCOPY_CANONICAL_DECODE_IDENTITY_V0_1

TRANSFORMATION_VERSION =
V0.1
```

Exact transformation code :

```text
TRANSFORMATION_CODE_BLOB =
e60fd260642f1a3dfb88b7cce4b6c4f5defc3131
```

Exact transformation tests :

```text
TRANSFORMATION_TEST_BLOB =
54837800f16f60b56328ddc818d0f9e2b2b01c1d
```

Numeric semantics :

```text
INPUT_UNIT =
0.001 PRICE UNIT

OUTPUT_UNIT =
0.001 PRICE UNIT

NUMERIC_REPRESENTATION =
EXACT_INTEGER_MILLI_PRICE

ROUNDING_MODE =
NONE

EPSILON =
0

ROW_REMOVAL =
0
```

La transformation est adoptée comme :

```text
DETERMINISTIC =
TRUE

TIME_INVARIANT =
TRUE

STRATEGY_INDEPENDENT =
TRUE

PERFORMANCE_INDEPENDENT =
TRUE

ROW_SPECIFIC_LOOKUP =
FALSE

POST_HOC_TOLERANCE =
FALSE

DROPPED_QUOTES =
FALSE

INTERPOLATION =
FALSE

FUTURE_DATA_USED =
FALSE
```

---

# 5. DISCOVERY EVIDENCE

La phase discovery reste liée à :

```text
DISCOVERY_WINDOW =
2026-05-18T00:00:00Z
→
2026-05-21T23:59:59.999Z

DISCOVERY_ROWS =
1698188
```

Résultat :

```text
DISCOVERY_TIMESTAMP_MISMATCH_COUNT =
0

DISCOVERY_BID_MISMATCH_COUNT =
0

DISCOVERY_ASK_MISMATCH_COUNT =
0
```

Aucune information issue du holdout n’a servi à sélectionner la transformation.

```text
VALIDATION_DETAIL_OBSERVED_BEFORE_FREEZE =
FALSE
```

---

# 6. HOLDOUT VALIDATION

Après gel de la transformation, le holdout indépendant a produit :

```text
VALIDATION_WINDOW =
2026-05-22T00:00:00Z
→
2026-05-24T23:59:59.963Z

VALIDATION_ROWS =
360754
```

Résultat exact :

```text
VALIDATION_TIMESTAMP_MISMATCH_COUNT =
0

VALIDATION_BID_MISMATCH_COUNT =
0

VALIDATION_ASK_MISMATCH_COUNT =
0

VALIDATION_STATUS =
PASS_EXACT
```

Aucune tolérance n’a été appliquée.

```text
EPSILON =
0

ROW_REMOVAL =
0
```

---

# 7. FULL-WINDOW REBREAK

Le rebreak complet sur la fenêtre historique figée a produit :

```text
FULL_REFERENCE_ROWS =
2058942

FULL_CANDIDATE_ROWS =
2058942

FULL_TIMESTAMP_MISMATCH_COUNT =
0

FULL_BID_MISMATCH_COUNT =
0

FULL_ASK_MISMATCH_COUNT =
0
```

Candidate Dukascopy representation :

```text
CANDIDATE_MULTIPLIER =
0.001
```

Le résultat exact est :

```text
FULL_REBREAK_STATUS =
PASS_EXACT_DETERMINISTIC_RECONCILIATION
```

---

# 8. PROVENANCE

La lignée historique Source-B reste :

```text
REFERENCE_LINEAGE =
CarlosSilva1/ustech-ticks

DOCUMENTED_PUBLISHER_PROVENANCE =
Dukascopy via Tickstory
```

Les champs de prix Source-B sont :

```text
BID_PRICE_TYPE =
double

ASK_PRICE_TYPE =
double
```

La lignée candidate qualifiée est :

```text
PROVIDER =
DUKASCOPY

TRANSPORT =
JETTA_DUKASCOPY_TICKS_API

INSTRUMENT =
USATECH.IDX-USD

CANONICAL_MULTIPLIER =
0.001
```

---

# 9. EXACT SEMANTIC RELATION

J’adopte la distinction suivante comme binding :

```text
RAW_DUKASCOPY_BYTES
!=
HISTORICAL_SOURCE_B_BYTES
```

Aucune identité byte-for-byte entre les deux surfaces brutes n’est prétendue.

En revanche :

```text
TRANSFORMED_DUKASCOPY_SEMANTICS
=
SOURCE_B_PRICE_CORE_SEMANTICS
```

dans le domaine exact qualifié.

Classification :

```text
RECONCILIATION_CLASS =
NUMERIC_REPRESENTATION_RECONCILIATION

SEMANTIC_RELATION =
EXACT_DETERMINISTIC_RECONCILIATION
```

Cette relation est fondée sur la transformation canonique gelée, et non sur une tolérance.

---

# 10. FLOAT64 OPERATIONAL EQUIVALENCE

La vérification opérationnelle complète reste binding :

```text
candidate_milli / 1000.0
vs
Source-B float64
```

Résultat :

```text
BID_MISMATCH_COUNT =
0

ASK_MISMATCH_COUNT =
0

MAX_ABS_BID_DIFFERENCE =
0.0

MAX_ABS_ASK_DIFFERENCE =
0.0
```

Ainsi :

```text
OPERATIONAL_PRICE_CORE_EQUIVALENCE =
EXACT
```

pour la surface qualifiée.

---

# 11. CI QUALIFICATION

La qualification indépendante GitHub reste partie intégrante de l’adoption :

```text
CI_RUN =
37487829975

CI_JOB =
112352422251

CI_CONCLUSION =
SUCCESS
```

Résultats :

```text
SR01_FROZEN_BREAKERS =
6 / 6 PASS

A_TRANSFORM_TESTS =
3 / 3 PASS

A_EVIDENCE_TESTS =
10 / 10 PASS

ACQ01_HISTORICAL_BLOCKER_EXACT =
PASS
```

---

# 12. PATH B CLOSED

Puisque A a satisfait les critères gelés :

```text
A =
HUMAN_ADOPTED / BINDING / FROZEN
```

la branche B reste :

```text
B_PHASE =
NOT_OPENED

B_NEW_LINEAGE_QUALIFICATION =
NOT_EXECUTED

B_HUMAN_ADOPTION =
NOT_APPLICABLE_TO_CURRENT_PATH
```

Aucune nouvelle lignée distincte :

```text
DATA01_FORWARD_SOURCE_DUKASCOPY_V0_1
```

n’est créée ou adoptée par cette décision.

---

# 13. EFFECT ON SOURCE CONTINUATION

À partir de cette adoption, le chemin de continuation autorisé pour une future acquisition structurelle peut utiliser :

```text
DUKASCOPY JETTA RAW TICKS
→
CANONICAL DUKASCOPY DECODE
→
EXACT INTEGER MILLI-PRICE SEMANTICS
→
SOURCE_B PRICE-CORE SEMANTICS
```

sous réserve des autres gates DATA-01.

Cette adoption ne signifie PAS :

```text
RAW_DUKASCOPY =
SOURCE_B_RAW_BYTES
```

Elle signifie uniquement :

```text
QUALIFIED_CANONICAL_DUKASCOPY_PRICE_SEMANTICS
=
SOURCE_B_PRICE_CORE_SEMANTICS
```

---

# 14. DATA-01 PRESERVATION

La règle DATA-01 reste :

```text
DATA01 =
HUMAN_ADOPTED / BINDING / FROZEN
```

Exact adoption receipt :

```text
DATA01_HUMAN_ADOPTION_RECEIPT =
290065c68a7d37a43d9c80e326575d9eddcfd088
```

Cette décision ne modifie pas la règle temporelle DATA-01.

```text
FORWARD_EVIDENCE_START =
2026-10-06T11:00:00Z
```

reste inchangé.

---

# 15. PIPE-01 PRESERVATION

```text
PIPE01 =
HUMAN_ADOPTED / BINDING / FROZEN
```

Exact receipt :

```text
PIPE01_HUMAN_ADOPTION_RECEIPT =
4ac1555b846ecd205ed1ad682d1fa165e38a9a3d
```

Cette décision n’invoque pas PIPE-01.

```text
PIPE01_FIRST_READ =
NOT_INVOKED
```

---

# 16. OWNER-02 / B11 V0.2 PRESERVATION

```text
OWNER02 =
HUMAN_ADOPTED / BINDING / FROZEN

B11_V0_2_CAPABILITY =
HUMAN_ADOPTED / BINDING / FROZEN
```

Exact adoption receipt :

```text
OWNER02_B11_V0_2_HUMAN_ADOPTION_RECEIPT =
0e3b36944098b6602852072fd42eb4011c4a76b2
```

Aucune modification owner n’est créée par SR-01 A.

---

# 17. B8 / DR-01 PRESERVATION

```text
B8 =
CLOSED / HUMAN_ADOPTED / BINDING / FROZEN

DR01 =
HUMAN_ADOPTED / BINDING / FROZEN
```

Aucune réouverture ou modification de ces surfaces n’est autorisée par cette adoption.

---

# 18. B12 FIREWALL

Cette décision n’ouvre PAS B12.

```text
B12 =
CLOSED

B12_HUMAN_OPENING_RECEIPT =
ABSENT
```

Et :

```text
SR01_A_HUMAN_ADOPTION
!=
B12_OPENING
```

```text
SOURCE_SEMANTIC_RECONCILIATION
!=
FORWARD_PERFORMANCE_AUTHORITY
```

---

# 19. OCTOBER FORWARD FIREWALL

À la date de cette adoption :

```text
OCTOBER_FORWARD_DATA =
UNTOUCHED

OCTOBER_FORWARD_ACQUISITION =
NOT_YET_AUTHORIZED
```

Cette adoption ne déclenche PAS automatiquement l’acquisition des données forward.

```text
SOURCE_RELATION_ADOPTION
!=
FORWARD_ACQUISITION
```

Une phase distincte doit encore matérialiser la tranche forward selon la lignée désormais adoptée.

---

# 20. NO PERFORMANCE OBSERVATION

```text
PERFORMANCE_BEARING_READ =
FALSE

FORWARD_PERFORMANCE_OBSERVATION =
FALSE

OOS_CONSUMPTION =
FALSE

REAL_PNL_OBSERVED =
FALSE

REAL_EXPECTANCY_OBSERVED =
FALSE

REAL_CI_OBSERVED =
FALSE

SUPPORT_REFUTE_INCONCLUSIVE_OBSERVED =
FALSE

REAL_AO_E0_RESULT =
FALSE
```

---

# 21. CURRENT SCIENTIFIC STATE

```text
STRATEGY_QUALIFIED =
NO CLAIM
```

Cette décision porte sur une **source-data semantic relation**, pas sur la performance de la stratégie.

```text
SOURCE_RECONCILIATION
!=
STRATEGY_QUALIFICATION
```

---

# 22. EXACT FORWARD INSTANCE

```text
EXACT_FORWARD_INSTANCE =
NOT_YET_AVAILABLE

DATA01_INSTANCE_STATE =
WAIT_NOT_READY
```

Cette décision ne matérialise pas l’instance forward finale.

Elle ne crée pas :

```text
raw_forward_manifest_sha256
raw_forward_inventory_digest
ap0_forward_manifest_sha256
h1_forward_stream_sha256
exact_terminal_decision_time
exact_closed_trade_count
instance_digest
```

pour la future tranche complète.

---

# 23. NEXT GOVERNANCE FRONTIER

Après cette adoption, `SR-01` est fermé sur la branche A.

La prochaine frontière logique devient :

```text
AO-E0-B12-DATA-01-ACQ-02 —
ADOPTED SOURCE-CONTINUATION
BLIND FORWARD ACQUISITION
+ APPEND-ONLY RAW LEDGER
+ AP0/H1 STRUCTURAL MATERIALIZATION
+ ROLLING DATA-01 INSTANCE READINESS
```

Cette prochaine phase pourra utiliser la relation sémantique désormais adoptée pour acquérir et matérialiser les données post-cutover.

Elle devra conserver :

```text
B12 =
CLOSED
```

et :

```text
PERFORMANCE_BEARING_READ =
FORBIDDEN
```

---

# 24. ACQ-02 MAY NOT AUTO-OPEN B12

Même si ACQ-02 réussit à matérialiser une future instance DATA-01 :

```text
DATA01_INSTANCE_READY
!=
B12_OPEN
```

B12 devra toujours faire l’objet d’une décision humaine distincte immédiatement avant le premier `performance-bearing read`.

---

# 25. NON-AUTHORIZATIONS

Cette décision n’autorise PAS :

- la réécriture de l’historique ACQ-01 ;
- l’ouverture de la branche B ;
- la création d’une nouvelle lignée B ;
- l’ouverture de B12 ;
- la lecture de performance ;
- la consommation OOS ;
- le calcul de PnL ;
- le calcul d’expectancy ;
- le calcul de CI ;
- l’exécution réelle du SMF ;
- SUPPORT / REFUTE / INCONCLUSIVE ;
- la qualification de la stratégie ;
- la modification des paramètres ;
- la modification de la stratégie ;
- le trading ;
- l’exécution broker ;
- le déploiement de capital.

---

# 26. FINAL STATE AFTER ADOPTION

```text
SR01 =
HUMAN_ADOPTED / BINDING / FROZEN

SR01_PATH =
A

SEMANTIC_RELATION =
EXACT_DETERMINISTIC_RECONCILIATION

DUKASCOPY_CANONICAL_DECODE_IDENTITY_V0_1 =
HUMAN_ADOPTED / BINDING / FROZEN

B_PHASE =
NOT_OPENED

DATA01 =
HUMAN_ADOPTED / BINDING / FROZEN

PIPE01 =
HUMAN_ADOPTED / BINDING / FROZEN

OWNER02 =
HUMAN_ADOPTED / BINDING / FROZEN

B11_V0_2_CAPABILITY =
HUMAN_ADOPTED / BINDING / FROZEN

B8 =
CLOSED

B12 =
CLOSED

OCTOBER_FORWARD_DATA =
UNTOUCHED

OCTOBER_FORWARD_ACQUISITION =
NOT_YET_AUTHORIZED

EXACT_FORWARD_INSTANCE =
NOT_YET_AVAILABLE

DATA01_INSTANCE_STATE =
WAIT_NOT_READY

PERFORMANCE_BEARING_READ =
FALSE

STRATEGY_QUALIFIED =
NO CLAIM

TRADING =
NOT_AUTHORIZED

BROKER_EXECUTION =
NOT_AUTHORIZED

CAPITAL_DEPLOYMENT =
NOT_AUTHORIZED
```

---

```text
HUMAN_DECISION =
ADOPT

HUMAN_ADJUDICATION =
ADOPT_EXACT_SR01_A_SEMANTIC_RECONCILIATION

SR01_A =
HUMAN_ADOPTED / BINDING / FROZEN

SEMANTIC_RELATION =
EXACT_DETERMINISTIC_RECONCILIATION

B_PHASE =
NOT_OPENED

B12 =
CLOSED

EXACT_FORWARD_INSTANCE =
NOT_YET_AVAILABLE

DATA01_INSTANCE_STATE =
WAIT_NOT_READY

FORWARD_ACQUISITION =
NOT_YET_AUTHORIZED

PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

STRATEGY_QUALIFIED =
NO CLAIM

FORCE =
FALSE

STOP =
SR-01 A SEMANTIC RECONCILIATION HUMAN ADOPTION REACHED
```