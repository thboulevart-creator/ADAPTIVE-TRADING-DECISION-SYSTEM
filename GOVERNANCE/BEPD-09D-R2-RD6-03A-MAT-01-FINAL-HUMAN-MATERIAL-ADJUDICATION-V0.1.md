# HUMAN MATERIAL ADJUDICATION — BEPD-09D-R2-RD6-03A-MAT-01

## H-MAT-01 THROUGH H-MAT-05 — SYNTHETIC TRUST-LAB PARAMETER FREEZE V0.1

**PROPOSED DECISION = ADOPT_SYNTHETIC_MATERIAL_PARAMETERS_WITH_BOUNDARIES**

J'adopte, exclusivement pour la préparation d'un futur laboratoire synthétique RD6-03B, les paramètres matériels définis ci-dessous.

Cette décision ne modifie pas les contrats scientifiques, n'autorise aucune lecture de données réelles et n'ouvre pas RD6-03B.

Elle fixe les choix matériels nécessaires pour qu'une future demande d'autorisation d'implémentation soit déterministe, vérifiable et indépendante des résultats observés.

---

## 1. CANONICAL BINDING

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

EXPECTED_HEAD =
a51f046dbaaa13c10705386358680cd5ca226e4b

EXPECTED_TREE =
994ef272a5d73fce78faad16f5aaa44ea1143543

RD6_03A_ADOPTION_DECISION_BLOB =
fad19720c33f58f9163f1ac91859277605eba970

RD6_03A_ADOPTION_RECEIPT_BLOB =
b087a557f02f76db5efebbf0b5a84ae3a65ffa08

RD6_03A =
HUMAN_ADOPTED_WITH_AMENDMENTS
DOCUMENTARY_SCOPE_ONLY
CLOSED

SOURCE_OF_TRUTH =
GITHUB

FORCE =
FALSE

FAIL_CLOSED =
MANDATORY
```

Toute persistence exigera une vérification fraîche du HEAD/TREE et des artefacts RD6-03A. Aucun rebind automatique n'est permis.

## 2. H-MAT-01 — CANONICAL SERIALIZATION AND TYPE RULES

### HUMAN SELECTION

```text
H-MAT-01 =
SELECT_A

MANIFEST_CANONICALIZATION =
RFC8785_JCS_UTF8

VIEW_FORMAT =
CANONICAL_JSONL_UTF8_LF

VIEW_ROW_CANONICALIZATION =
RFC8785_JCS_PER_ROW

JSON_DUPLICATE_KEYS =
REJECT

JSON_UNKNOWN_FIELDS =
REJECT

NONFINITE_NUMBERS =
REJECT

UNPAIRED_UNICODE_SURROGATES =
REJECT

NEGATIVE_ZERO_INPUT =
REJECT

MANIFEST_FLOAT_FIELDS =
FORBIDDEN
```

Je retiens les règles suivantes.

**Manifestes**

- Exactement les 30 champs preregistrés par RD6-03A-C.
- Aucun champ supplémentaire, manquant ou dupliqué.
- Nombres entiers uniquement dans les champs numériques du manifeste.
- Les entiers doivent rester représentables sans ambiguïté dans le domaine sûr d'interopérabilité JSON.
- Tous les digests SHA-256 sont représentés par 64 caractères hexadécimaux minuscules.
- Toute signature et tout identifiant doivent respecter leur encodage preregistré.

**Vues synthétiques**

- Un objet JSON canonique par ligne.
- Encodage UTF-8 strict.
- Séparateur LF.
- Une ligne terminée par LF pour chaque événement.
- Ordre croissant selon `target_week_id`, puis `event_id`.
- Exactement les dix champs de la fixture RD5, avec leurs types scientifiques originaux.
- Aucun arrondi scientifique supplémentaire ni transformation des features.
- Aucune donnée de test du fold courant.

Les valeurs numériques finies de la fixture seront sérialisées selon JCS, avec qualification d'interopérabilité par vecteurs de référence indépendants.

**Identifiants sans dépendance circulaire**

```text
VIEW_CONTENT_DIGEST =
SHA256(EXACT_VIEW_BYTES)

VIEW_ID =
SHA256(
  DOMAIN_SEPARATED_CANONICAL_VIEW_BINDING
)

VIEW_BINDING_INPUTS =
FOLD_ID
+
ORDERED_TRAIN_WEEK_IDS
+
VIEW_CONTENT_DIGEST
+
RECEIVER_IDENTITY
+
VIEW_NONCE
```

Le domaine de calcul du `VIEW_ID` devra être fixe, explicite et distinct de celui utilisé pour signer le manifeste. Le `VIEW_ID` ne devra jamais dépendre de lui-même.

Les champs `signature` et `signed_payload_digest` sont exclus du payload signé ; tous les autres champs du manifeste, y compris `view_id` et `audit_receipt_id`, restent signés.

Les détails de sérialisation devront être démontrés par tests d'interopérabilité avant tout GREEN.

```text
H-MAT-01_STATUS =
SELECTED_FOR_SYNTHETIC_QUALIFICATION

REAL_DATA_SERIALIZATION_AUTHORITY =
NONE
```

---

## 3. H-MAT-02 — SIGNATURE, TRUST ROOT AND DELEGATION

### HUMAN SELECTION

```text
H-MAT-02 =
SELECT_A

SIGNATURE_ALGORITHM =
ED25519_RFC8032

SIGNED_PAYLOAD_CANONICALIZATION =
RFC8785_JCS

DIGEST_ALGORITHM =
SHA256

SIGNATURE_ENCODING =
BASE64URL_NO_PADDING

PUBLIC_KEY_SIZE =
32_BYTES

SIGNATURE_SIZE =
64_BYTES

TRUST_ROOT =
EPHEMERAL_SYNTHETIC_ONLY

PRODUCTION_KEY_REUSE =
FORBIDDEN
```

**Construction du message signé**

```text
SIGNED_MESSAGE =
UTF8(DOMAIN_SEPARATOR)
||
JCS(UNSIGNED_MANIFEST)

DOMAIN_SEPARATOR =
ATDS/RD6-03A/TRAIN_VIEW_MANIFEST/V1
FOLLOWED_BY_ONE_0x00_BYTE

SIGNED_PAYLOAD_DIGEST =
SHA256(SIGNED_MESSAGE)
```

L'Ed25519 retenu est la variante pure de RFC 8032. Aucune substitution implicite par Ed25519ph ou Ed25519ctx n'est permise.

Le signataire synthétique est identifié par une clé publique de test explicitement inscrite dans le registre de confiance synthétique.

```text
TRUST_ROOT_ID =
SHA256(RAW_32_BYTE_PUBLIC_KEY)

SIGNER_DELEGATION =
EXACT_SYNTHETIC_PRODUCER
+
EXACT_FOLD_SCOPE
+
EXACT_RECEIVER
+
EXACT_VALIDITY_WINDOW
```

**Conditions d'acceptation**

- Signature vérifiée avec la clé publique attendue.
- Identité du signataire connue.
- Délégation valide pour le producteur, le fold et le récepteur exacts.
- Aucune clé révoquée, expirée ou inconnue.
- Aucune acceptation fondée seulement sur un marqueur `PROVENANCE`.
- Aucun fallback cryptographique.

Les cas de révocation et de rotation de clés pourront être testés avec des registres de confiance synthétiques prédéfinis. Aucune rotation opérationnelle de clés de production n'est autorisée.

Les secrets de test seront générés ou dérivés exclusivement dans le laboratoire synthétique, jamais à partir de secrets réels, et ne devront pas être persistés sur GitHub.

```text
H-MAT-02_STATUS =
SELECTED_FOR_SYNTHETIC_QUALIFICATION

REAL_PRODUCER_ATTESTATION =
NOT_ESTABLISHED

REAL_TRUST_ROOT =
NOT_ADOPTED
```

---

## 4. H-MAT-03 — SYNTHETIC PROCESS AND FILESYSTEM CAPABILITIES

### HUMAN SELECTION

```text
H-MAT-03 =
SELECT_A

EXECUTION_ENVIRONMENT =
ISOLATED_SYNTHETIC_WORKSPACE

DATA_SOURCE =
GENERATED_RD5_SYNTHETIC_FIXTURES_ONLY

REAL_LEDGER_MOUNT =
FORBIDDEN

REAL_DATA_PATH_ACCESS =
FORBIDDEN

NETWORK_EGRESS =
FORBIDDEN

EXTERNAL_CREDENTIALS =
FORBIDDEN

SHARED_PRODUCTION_PROCESS =
FORBIDDEN
```

Je retiens une architecture de test à processus distincts.

```text
SYNTHETIC_FIXTURE_GENERATOR
        |
        v
SYNTHETIC_VIEW_PRODUCER
        |
        v
SYNTHETIC_AUTHENTICATOR
        |
        v
BOUNDED_TRAIN_VIEW_VALIDATOR
        |
        v
REDACTED_TEST_RECEIPT
```

**Autorisations futures candidates**

- Génération de fixtures RD5 synthétiques en mémoire.
- Écriture uniquement dans un répertoire temporaire de laboratoire explicitement isolé.
- Lecture uniquement des fichiers synthétiques autorisés.
- Utilisation d'une clé de signature exclusivement synthétique.
- Exécution de tests à processus séparés, si le mécanisme d'isolation est qualifié.

**Interdictions permanentes pour RD6-03B**

- Lecture du ledger historique réel, y compris pour calculer un hash.
- Accès aux shards réels, caches réels ou chemins de données historiques.
- Réutilisation du harness réel existant.
- Import ou exécution d'un chemin produisant des prédictions ou scores sur le fold de test.
- Héritage de descripteurs vers des fichiers interdits.
- Transmission réseau de données ou secrets.
- Écriture dans une surface de production.

Les contrôles d'isolation devront inclure des tests d'accès refusé, de symlinks, de fichiers temporaires, d'héritage de descripteurs et de modifications d'état global.

**Limite essentielle :** un mock refusant une opération ne démontre pas une interdiction réelle au niveau du système d'exploitation. Le résultat devra être classifié comme `SYNTHETIC_MOCK_PASS` tant qu'une isolation effective n'aura pas été indépendamment vérifiée.

```text
H-MAT-03_STATUS =
SELECTED_FOR_SYNTHETIC_LAB_ONLY

REAL_OS_ISOLATION =
NOT_ASSESSABLE

REAL_FILESYSTEM_DENY_PROOF =
BLOCKED
```

---

## 5. H-MAT-04 — EXPIRY, NONCE ATOMICITY AND RESOURCE BOUNDS

### HUMAN SELECTION

```text
H-MAT-04 =
SELECT_A

TIME_SOURCE =
INJECTED_DETERMINISTIC_UTC_CLOCK

SYNTHETIC_VIEW_TTL =
300_SECONDS

CLOCK_SKEW_TOLERANCE =
0_SECONDS

NONCE_SIZE =
192_BITS

NONCE_POLICY =
ATOMIC_SINGLE_USE

AUTOMATIC_RETRY =
FORBIDDEN
```

Le laboratoire synthétique devra tester les frontières temporelles exactes.

```text
ADMISSIBLE_IF =
ISSUED_AT <= NOW
AND
NOW < EXPIRES_AT

EXPIRES_AT - ISSUED_AT =
300_SECONDS

INVALID_CLOCK =
STOP
```

L'horloge injectée sert exclusivement aux tests déterministes. Elle ne constitue pas une source de temps fiable pour une future admission réelle.

**Protection anti-rejeu**

La clé logique de consommation unique est :

```text
REPLAY_KEY =
TRUST_ROOT_ID
+
SIGNER_ID
+
RECEIVER_IDENTITY
+
FOLD_ID
+
VIEW_NONCE
```

La réservation de cette clé doit être atomique.

Deux consommateurs concurrents ne doivent jamais pouvoir obtenir simultanément une admission valide pour une même clé.

Une réservation dont l'état de commit ou de rollback est inconnu doit entraîner STOP.

Les tests synthétiques devront couvrir le double appel simultané, la réutilisation du nonce, l'échec après réservation et les cas de reprise. La stratégie de restauration ne doit jamais créer une seconde admission.

**Limites de ressources candidates**

```text
MAX_SYNTHETIC_VIEW_BYTES =
2097152

MAX_SYNTHETIC_MANIFEST_BYTES =
65536

MAX_SYNTHETIC_ROWS_PER_VIEW =
1500

MAX_FOLDS =
5

MAX_TEST_INVOCATIONS_PER_AUTHORIZED_RUN =
120

MAX_TEST_CASE_DURATION =
5_SECONDS

MAX_TOTAL_SYNTHETIC_RUN_DURATION =
180_SECONDS

REAL_FIT_BUDGET =
0

EXTERNAL_SPENDING_BUDGET =
0
```

Ces limites sont des budgets d'ingénierie proposés pour le futur laboratoire, et non des paramètres scientifiques de RD3 ni des ressources actuellement autorisées.

Si une limite ne peut être respectée sans changement scientifique, la procédure doit s'arrêter et demander une adjudication distincte.

```text
H-MAT-04_STATUS =
SELECTED_FOR_SYNTHETIC_LAB_ONLY

EXECUTION_BUDGET_CURRENTLY_AUTHORIZED =
0

PRODUCTION_TIME_AND_NONCE_POLICY =
NOT_QUALIFIED
```

---

## 6. H-MAT-05 — TEST-FIRST RED/GREEN AND SOURCE SCOPE

### HUMAN SELECTION

```text
H-MAT-05 =
SELECT_A

DEVELOPMENT_STRATEGY =
STRICT_TEST_FIRST_RED_THEN_GREEN

NEGATIVE_TEST_MATRIX =
RD6_03A_E_FROZEN

BREAKER_MATRIX =
RD6_03A_F_FROZEN

IN_SCOPE_NEGATIVE_TESTS =
23

CROSS_LANE_TESTS =
11_BLOCKED

RD6_04_RESERVED_TESTS =
3_BLOCKED

POSITIVE_SYNTHETIC_FIXTURES =
7

EXECUTION_AUTHORITY =
NOT_YET_GRANTED
```

La future implémentation doit utiliser les tests RED avant les modifications nécessaires pour obtenir GREEN.

### Candidate executable paths

Les fichiers candidats à une future autorisation RD6-03B sont :

```text
tools/bepd09d_r2_rd6_03b_view_producer.py

tools/bepd09d_r2_rd6_03b_view_authenticator.py

tools/bepd09d_r2_rd6_03b_view_validator.py

tools/bepd09d_r2_rd6_03b_redacted_exporter.py

tests/test_bepd09d_r2_rd6_03b_manifest.py

tests/test_bepd09d_r2_rd6_03b_fold_scope.py

tests/test_bepd09d_r2_rd6_03b_security.py

tests/test_bepd09d_r2_rd6_03b_exporter.py
```

Ces chemins sont des candidats figés pour une future demande d'autorisation. **Leur création ou leur modification n'est pas autorisée par la présente adjudication.**

Aucun fichier RD3, RD5, RD6-01 ou RD6-02 ne peut être modifié implicitement.

### Required RED evidence

Un RED recevable devra :

1. Utiliser une fixture synthétique identifiable.
2. Vérifier un oracle préalablement gelé.
3. Démontrer l'échec réel du comportement de sécurité attendu sur une implémentation bornée ou un contrôle encore absent.
4. Ne pas considérer une simple erreur d'import, une exception artificielle ou un échec forcé comme preuve de vulnérabilité.
5. Enregistrer le test, l'oracle, le breaker attendu et le résultat réel.
6. Ne jamais accéder aux données historiques.
7. Conserver tout test impossible à qualifier comme BLOCKED.

### Required GREEN evidence

Un GREEN recevable devra démontrer :

- la vérification de la signature synthétique ;
- l'admission des fixtures positives autorisées ;
- le rejet déterministe des fixtures négatives pertinentes ;
- le déclenchement du breaker attendu ;
- l'absence d'effet secondaire interdit ;
- l'absence de fuite dans les receipts ;
- le respect des limites de ressources ;
- la conservation exacte des invariants scientifiques ;
- la répétabilité des résultats.

Les tests transversaux et les tests RD6-04 restent hors du dénominateur de qualification RD6-03B.

Une future qualification ne pourra recevoir PASS que si les tests in-scope exigés ont été exécutés, ont satisfait leurs oracles et ne présentent aucun blocker non résolu.

### Required evidence outputs

```text
RED_PHASE_RECEIPT

GREEN_PHASE_RECEIPT

NEGATIVE_TEST_COVERAGE_MATRIX

BREAKER_TRIGGER_MATRIX

SOURCE_IDENTITY_RECEIPT

SYNTHETIC_FIXTURE_DIGESTS

NO_REAL_DATA_ACCESS_EVIDENCE

REGRESSION_REPORT

HUMAN_ADJUDICATION_PACKAGE
```

Les preuves d'absence d'accès aux données réelles devront être limitées à ce qui est effectivement vérifiable. Une simulation ne pourra pas être présentée comme preuve d'isolation réelle.

```text
H-MAT-05_STATUS =
TEST_FIRST_PROTOCOL_SELECTED

TEST_EXECUTION =
NOT_AUTHORIZED

SOURCE_IMPLEMENTATION =
NOT_AUTHORIZED
```

---

## 7. GOVERNANCE LIMITS — H-MAT-06 AND H-MAT-07

La présente décision ne tranche pas :

```text
H-MAT-06 =
RD3_REMEDIATION_AND_REFERENCE_PARITY_OWNERSHIP
STATUS = RESERVED_FOR_SEPARATE_HUMAN_DECISION

H-MAT-07 =
REAL_SOURCE_OWNER_ATTESTATION
STATUS = RESERVED_FOR_SEPARATE_HUMAN_DECISION
```

Les défauts RD3, la parité numérique RD6-04 et toute exposition physique de données réelles restent soumis à leurs autorités indépendantes.

---

## 8. PRESERVED SCIENTIFIC AND SECURITY STATUS

```text
RD5_SYNTHETIC_PRIOR =
29/29_PASS_PRESERVED

RD3_EXCEPTION_MASKING =
FAIL_UNRESOLVED

RD3_LP_STATUS_HANDLING =
FAIL_UNRESOLVED

P0.4 =
FAIL_UNRESOLVED

P0.6 =
FAIL_UNRESOLVED

RED_TESTS_EXECUTED_RD6_03B =
0

GREEN_TESTS_EXECUTED_RD6_03B =
0

INDEPENDENT_EXTERNAL_REVIEW =
NOT_COMPLETED

REAL_SOURCE_PROVENANCE =
NOT_ESTABLISHED

REAL_LEDGER_READ =
FORBIDDEN

REAL_TRAINING_MATERIALIZATION =
FORBIDDEN

REAL_PRIMARY_FIT =
FORBIDDEN

REAL_REFERENCE_FIT =
FORBIDDEN

TEST_SCORING =
FORBIDDEN

TRADING_AUTHORITY =
NONE
```

L'adoption des paramètres H-MAT ne peut pas transformer une qualification synthétique future en qualification réelle.

## 9. AUTHORIZED DOCUMENTARY PERSISTENCE

J'autorise exclusivement la persistence documentaire de cette adjudication matérielle et de son receipt, sous les chemins :

```text
GOVERNANCE/BEPD-09D-R2-RD6-03A-MAT-01-FINAL-HUMAN-MATERIAL-ADJUDICATION-V0.1.md

GOVERNANCE/BEPD-09D-R2-RD6-03A-MAT-01-HUMAN-ADOPTION-RECEIPT-V0.1.json
```

La persistence est conditionnée à :

```text
FRESH_HEAD_AND_TREE =
REQUIRED

RD6_03A_ADOPTED_BLOBS =
UNCHANGED

SCIENCE_AND_RUNTIME_BLOBS =
UNCHANGED

NEW_FILES =
EXACTLY_2

EXISTING_FILES_MODIFIED =
0

EXPECTED_SHA =
REQUIRED

FORCE =
FALSE

POST_PERSISTENCE_READBACK =
REQUIRED

AUTOMATIC_RETRY =
FORBIDDEN

STOP =
MANDATORY
```

Tout drift ou conflit matériel non qualifié entraîne STOP, sans rebind automatique.

La publication documentaire ne peut créer aucun fichier exécutable, workflow, jeu de données ou artefact de qualification.

## 10. MAXIMUM AUTHORIZED FINAL STATE

```text
RD6_03A_MAT_01 =
HUMAN_MATERIAL_PARAMETERS_SELECTED
SYNTHETIC_SCOPE_ONLY

H-MAT-01 =
SELECTED

H-MAT-02 =
SELECTED

H-MAT-03 =
SELECTED

H-MAT-04 =
SELECTED

H-MAT-05 =
SELECTED

H-MAT-06 =
RESERVED

H-MAT-07 =
RESERVED

RD6-03B =
NOT_AUTHORIZED

RD6-04 =
NOT_AUTHORIZED

REAL_TRAINING_READINESS =
BLOCKED

AUTOMATIC_NEXT_STAGE =
FORBIDDEN

STOP =
MANDATORY
```

## FINAL HUMAN DECISION

```text
CONTROL =
BEPD-09D-R2-RD6-03A-MAT-01

PROPOSED_DECISION =
ADOPT_SYNTHETIC_MATERIAL_PARAMETERS_WITH_BOUNDARIES

AUTHORIZED_SCOPE =
H-MAT-01
+
H-MAT-02
+
H-MAT-03
+
H-MAT-04
+
H-MAT-05

EXECUTABLE_IMPLEMENTATION =
FORBIDDEN

SYNTHETIC_TEST_EXECUTION =
FORBIDDEN

REAL_DATA_ACCESS =
FORBIDDEN

GITHUB_PERSISTENCE =
TWO_DOCUMENTS_ONLY

FORCE =
FALSE

FAIL_CLOSED =
MANDATORY

STOP =
MANDATORY
```

**J'adopte les cinq sélections matérielles H-MAT-01 à H-MAT-05 exclusivement comme paramètres gelés du futur laboratoire synthétique. J'autorise uniquement leur persistence documentaire contrôlée et leur readback, sans ouvrir RD6-03B.**