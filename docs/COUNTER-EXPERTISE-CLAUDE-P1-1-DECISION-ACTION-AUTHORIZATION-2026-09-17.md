# CONTRE-EXPERTISE CLAUDE — P1.1 DECISION → ACTION AUTHORIZATION

**Statut :** EXTERNAL COUNTER-EXPERTISE REQUIRED — READ-ONLY  
**Repository :** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branche gouvernée :** `integration/system-v1`  
**HEAD À AUDITER :** `304bf0c370c422b6cb8ea9159cbaf1c282ec01f9`  
**Base de formalisation P1.1 :** `8ed66310937fac6bf7305081ba6d230459cff5d2`

## 1. Rôle de Claude

Tu interviens comme **contre-expert code indépendant**, pas comme auteur de la prochaine architecture.

Ta mission est de chercher ce que l'audit interne et le catalogue A0–F5 ont pu manquer dans le candidat P1.1 actuel.

**Ne modifie aucun fichier du dépôt. Ne commit rien. Ne pousse rien. Ne propose aucune correction avant d'avoir produit ton diagnostic adversarial.**

Le dépôt et le commit exact ci-dessus sont la source de vérité. Ne reconstruis pas l'état depuis un résumé conversationnel.

## 2. Question centrale

Le candidat P1.1 prétend garantir ceci :

`qualified producer-created Decision → identity/content verification → authorization constraints → BLOCKED`

Le candidat est volontairement **block-only** : aucun chemin `AUTHORIZED` n'existe encore.

La question à casser est :

> **Existe-t-il une manière réaliste, dans le modèle Python et dans les frontières actuelles du dépôt, de faire reconnaître comme downstream-admissible une Decision ou des AuthorizationConstraints qui ne devraient pas l'être, de préserver abusivement une attestation, de contourner le fail-closed, ou de préparer un futur bypass qui deviendrait critique dès l'ouverture d'un chemin AUTHORIZED ?**

## 3. Corpus exact à lire au commit `304bf0c...`

Lire intégralement :

1. `04-REFERENCE/DECISION-ACTION-AUTHORIZATION-BOUNDARY-CONTRACT.md`
2. `src/decision.py`
3. `src/decision_action_authorization.py`
4. `tests/test_decision_action_authorization_tier_a.py`
5. `.github/workflows/p1-1-decision-action-authorization.yml`
6. `src/research_run_evidence.py`
7. `tests/test_research_to_decision_boundary.py`
8. `src/decision_trace.py`
9. `src/promotion_gate.py`

Comparer aussi :

`8ed66310937fac6bf7305081ba6d230459cff5d2...304bf0c370c422b6cb8ea9159cbaf1c282ec01f9`

L'objectif est d'auditer **uniquement le candidat P1.1 et ses dépendances de confiance immédiates**, pas de réauditer toute l'architecture.

## 4. État de preuve déjà obtenu

### Premier cassage

HEAD : `a53e97e76e03a029cc7feace4f3875b826ea0662`  
Workflow : `P1.1 Decision-Action Authorization Tier-A`  
Run/job : `35199357246 / 105130119698`  
Résultat : **FAIL**

Le FAIL observé venait du harness : deux tests D2/D3 utilisaient un helper `reconstruct(decision, ...)` dont le nom du premier paramètre entrait en collision avec le champ `decision="SELL"`.

Il ne constituait pas un défaut fonctionnel du candidat.

### Re-cassage propre

HEAD : `304bf0c370c422b6cb8ea9159cbaf1c282ec01f9`  
Workflow : `P1.1 Decision-Action Authorization Tier-A`  
Run/job : `35199458494 / 105130448050`  
Résultat : **SUCCESS**

Éléments verts :

- exact persisted HEAD / ancestry ;
- candidate bounded and side-effect free ;
- environnement P0.6 verrouillé ;
- `RESEARCH → DECISION` protégé ;
- attaques A0–F5 ;
- worktree propre.

Ce vert ne vaut pas autorité sur ta contre-expertise.

## 5. Points à attaquer explicitement

Tu dois au minimum examiner les familles suivantes.

### A. Registres d'attestation weakref / identité Python

- réutilisation éventuelle de `id(...)` ;
- GC / destruction / timing de cleanup ;
- référence faible devenue morte ;
- collisions d'identité d'objet ;
- comportement après `importlib.reload` ;
- duplication de module sous un autre chemin d'import ;
- sous-interpréteurs / process séparés ;
- pickle / unpickle ;
- multiprocessing ;
- copie via mécanismes autres que `copy.copy/deepcopy` ;
- possibilité de récupérer ou influencer l'état fermé du registry via introspection Python.

Distingue soigneusement :

1. bypass positif réel ;
2. simple faux négatif / perte d'attestation ;
3. limitation volontaire in-process ;
4. problème futur à traiter avant persistence/inter-process.

### B. `Decision` et binding cryptographique

Vérifier si :

- `decision_id` est réellement lié à tous les champs qui devraient conditionner l'admissibilité downstream ;
- la troncature SHA-256 à 16 hex est acceptable pour cette frontière ou constitue un risque évitable ;
- une mutation/reconstruction peut conserver un couple `decision_id` / contenu accepté ;
- le lien vers `ResearchRunEvidence` est suffisant ou perd une provenance critique ;
- un objet produit avant un reload/version drift peut être mal interprété après changement de code.

### C. `AuthorizationConstraints`

Auditer :

- le `constraint_id` et son contenu exact ;
- la logique de `is_factory_attested_constraints()` ;
- toute redondance ou condition qui paraît correcte uniquement parce que le candidat est block-only ;
- la reconstruction interne d'un `Decision(..., decision="__binding_only__")` ;
- l'absence du payload `decision` dans `_constraint_id()` autrement que via `decision_id` ;
- possibilités de stale constraints / replay / rebinding ;
- module reload et registry reset ;
- possibilité qu'un futur chemin `AUTHORIZED` transforme un détail actuellement bénin en fail-open.

### D. Surface publique / monkeypatch / introspection

Examiner notamment :

- monkeypatch de `is_factory_attested_decision` importé dans `decision_action_authorization.py` ;
- monkeypatch de fonctions publiques ou constantes ;
- `__globals__`, closures, `__closure__`, cellules de closure, introspection de fonction ;
- possibilité de récupérer ou modifier le dictionnaire `registry` depuis une closure ;
- altération de `CONSTRAINT_POLICY`, `BLOCKED`, `AUTHORIZED`, `_stable_hash`, `_constraint_id` après import ;
- classe `Decision` / `AuthorizationConstraints` remplacée ou monkeypatchée.

Ne considère pas automatiquement toute capacité d'introspection Python comme un bug : définis d'abord le **threat model** nécessaire. Mais tout bypass possible sous le threat model actuel doit être signalé.

### E. Contrat vs code vs tests

Chercher :

- invariants contractuels non testés ;
- tests qui prouvent seulement un détail d'implémentation ;
- attaques A0–F5 qui peuvent passer sans prouver la propriété annoncée ;
- chemins refusés pour la mauvaise raison ;
- propriétés non couvertes par le workflow ;
- fichier critique absent des `paths:` du workflow ;
- dépendance de confiance modifiable sans déclencher P1.1.

### F. Futur chemin `AUTHORIZED`

Sans le concevoir ni l'implémenter, identifier précisément ce qui **doit impérativement être corrigé ou requalifié avant qu'un seul `AUTHORIZED` puisse exister**.

Cette partie est importante : un mécanisme peut être acceptable en block-only mais dangereux dès qu'il devient autorisant.

## 6. Contraintes de contre-expertise

Interdictions :

- ne pas construire ACTION ;
- ne pas introduire un moteur RISK autonome ;
- ne pas proposer sizing / levier / SL / TP ;
- ne pas ouvrir acquisition native USATECH ;
- ne pas autoriser backtest réel ;
- ne pas autoriser live ;
- ne pas déclarer P1.1 PASS simplement parce que les tests existants sont verts ;
- ne pas modifier le code pendant cette phase.

## 7. Format de restitution obligatoire

Rends une réponse structurée avec exactement ces sections :

### 1. VERDICT

Un seul parmi :

- `PASS — no material bypass found in current block-only scope`
- `FAIL — material bypass found`
- `BLOCKED — insufficient evidence to conclude`

### 2. FINDINGS

Pour chaque finding :

- ID : `CLAUDE-P1.1-XX`
- sévérité : `CRITICAL / HIGH / MEDIUM / LOW / NOTE`
- catégorie : `CURRENT_BYPASS / FUTURE_AUTHORIZED_RISK / FALSE_NEGATIVE_ONLY / IN_PROCESS_LIMIT / TEST_GAP / WORKFLOW_GAP / CONTRACT_GAP`
- fichier + symbole précis ;
- mécanisme ;
- scénario reproductible ;
- impact exact ;
- déjà couvert par A0–F5 : `YES / PARTIAL / NO`.

### 3. ADDITIONAL ATTACKS REQUIRED

Proposer seulement les attaques réellement justifiées qui manquent au catalogue actuel.

Pour chaque attaque :

- précondition ;
- manipulation ;
- comportement attendu fail-closed ;
- test minimal proposé.

### 4. MUST-FIX BEFORE ANY AUTHORIZED PATH

Liste fermée des défauts qui doivent être corrigés **avant** toute future émission de `AUTHORIZED`.

### 5. SAFE TO DEFER

Éléments réellement hors P1.1 actuel ou acceptables tant que le candidat reste block-only.

### 6. MINIMAL CORRECTION ORDER

Si correction requise, donner l'ordre minimal de correction. Ne fournis pas encore de patch complet sauf si indispensable pour expliquer un finding.

## 8. Règle d'indépendance

Ne cherche pas à confirmer le design existant. Cherche à le casser.

Ne traite pas les tests actuels comme une spécification suffisante : le contrat est la norme, le code est le candidat, les tests sont seulement une tentative de cassage.

Si tu trouves une faiblesse qui ne devient exploitable qu'après ouverture d'un chemin positif, classe-la explicitement `FUTURE_AUTHORIZED_RISK` au lieu de la présenter comme bypass actuel.

## 9. Fin de tâche

Arrête-toi après le rapport adversarial. **Ne modifie rien.**

Le rapport sera ensuite confronté au code réel et adjudiqué avant toute correction ou extension de P1.1.
