# HUMAN DECISION — BEPD-09D-R2-RD4

## DOCUMENTARY PREREGISTRATION AND STATIC READINESS — HUMAN ADJUDICATION V0.1

**DECISION = ADOPT_WITH_AMENDMENTS**

J'adopte humainement le package documentaire RD4, exclusivement comme base d'architecture et de preregistration pour une future requalification numérique training-only.

### 1. CANONICAL BINDING
```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

EXPECTED_HEAD =
6b60b70a3c033596074b0ceb3e9a2b6b2bfde69a

EXPECTED_TREE =
bd04b0a88bd20a7bf0e4444a9d8c23a9b5093d7d

SOURCE_OF_TRUTH =
GITHUB

FORCE =
FALSE
```

Avant persistence de la présente décision, vérifier à nouveau le HEAD, TREE, les identités RD4 et l'absence de drift matériel.

### 2. EVIDENCE ADJUDICATION

J'accepte les conclusions documentaires bornées :
```text
DOCUMENTARY_GATE_RESULTS =
10 PASS
1 FAIL
7 BLOCKED

RD4_DOCUMENTARY_BASIS =
ADOPTED_WITH_AMENDMENTS

RD4_REAL_EXECUTION_READINESS =
BLOCKED

RD4_EXECUTABLE_QUALIFICATION =
NOT_PERFORMED
```

Le FAIL relatif au protocole historique confirme que celui-ci ne peut pas être réutilisé tel quel pour une exécution training-only.

Il ne constitue pas un échec de la qualification synthétique Candidate B adoptée sous RD3.

### 3. HUMAN AMENDMENTS

**AMENDMENT A — TRAINING DATA ISOLATION**

J'adopte la séparation des données par fold courant. Un bloc historiquement utilisé comme test peut devenir une partie de l'entraînement d'un fold chronologiquement ultérieur, conformément aux partitions gelées.

Toute lecture de réponses de test hors du périmètre training du fold courant reste interdite.

Le traitement physique du ledger et les garanties d'isolation doivent être spécifiés et autorisés séparément.

**AMENDMENT B — CONTROLLED ADAPTER**

J'adopte le principe d'un nouvel adaptateur isolé, conçu exclusivement pour construire les matrices d'entraînement et invoquer le runtime Candidate B.
```text
LEGACY_RUN_PROTOCOL_REUSE =
REJECTED_FOR_TRAINING_ONLY

RD3_RUNTIME_MODIFICATION =
FORBIDDEN

NEW_ADAPTER_IMPLEMENTATION =
NOT_YET_AUTHORIZED
```

**AMENDMENT C — FAIL-CLOSED NUMERICS**

Tout échec ou état inconnu du détecteur de séparation doit conduire à un arrêt, et non être interprété comme l'absence prouvée de séparation.

La correction doit être traitée à une nouvelle frontière contrôlée, sans modifier silencieusement le runtime adopté.

**AMENDMENT D — INDEPENDENT REFERENCE**

Le solveur référence conserve uniquement un rôle de vérification numérique indépendante.

La métrique de parité training-only et sa tolérance devront être preregistrées et humainement adoptées avant utilisation réelle.

**AMENDMENT E — EXECUTION BUDGET**

Le budget proposé de dix fits primary et dix fits reference au maximum reste non adopté.

L'ordre des opérations, les limites de temps, les coûts admissibles et la politique d'arrêt devront faire l'objet d'une décision distincte.

### 4. CLOSED BOUNDARIES
```text
REAL_DATA_ROW_READ =
NOT_AUTHORIZED

REAL_TRAINING_FIT =
NOT_AUTHORIZED

REAL_FOLD3_REPLAY =
NOT_AUTHORIZED

REAL_REFERENCE_FIT =
NOT_AUTHORIZED

TEST_SCORING =
FORBIDDEN

C1_SCIENTIFIC_RESULT =
NONE

FRESH_OOS =
CLOSED

TRADING_AUTHORITY =
NONE
```

### 5. AUTHORIZED CLOSURE

J'autorise uniquement la persistence documentaire de cette adjudication, avec readback exact, contrôle du delta, protection concurrente `expected_sha` et `force=false`.

Aucune implémentation ni exécution ne découle de cette closure.

### 6. NEXT FRONTIER
```text
NEXT =
CONTROLLED_TRAINING_ONLY_ADAPTER
TEST_FIRST_SYNTHETIC_DESIGN
AND_IMPLEMENTATION_AUTHORIZATION

STATUS =
NOT_AUTHORIZED

REAL_EXECUTION =
FORBIDDEN
```

La future autorisation devra traiter les blockers RD4, implémenter le raccordement isolé et établir des tests synthétiques adversariaux avant toute nouvelle exposition aux données réelles.

### FINAL DECISION
```text
DECISION =
ADOPT_WITH_AMENDMENTS

ADOPTION_SCOPE =
RD4_DOCUMENTARY_DESIGN_BASIS_ONLY

RD4_REAL_READINESS =
BLOCKED

RD4_HUMAN_CLOSURE_PERSISTENCE =
CONDITIONALLY_AUTHORIZED

AUTOMATIC_NEXT_STAGE =
FORBIDDEN

FAIL_CLOSED =
MANDATORY

FORCE =
FALSE
```

**J'autorise exclusivement la closure canonique de cette adjudication, puis STOP.**

---

*Source de l'autorité : décision humaine explicite du 9 octobre 2026 transmise dans la conversation gouvernée. Ce document reproduit la décision; il ne prétend pas être une signature cryptographique de son auteur.*
