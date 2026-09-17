# CONTRE-EXPERTISE CLAUDE — P1.1 DECISION → ACTION AUTHORIZATION

**Statut :** EXTERNAL COUNTER-EXPERTISE REQUIRED — READ-ONLY  
**Repository :** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branche gouvernée :** `integration/system-v1`  
**CANDIDAT CODE À AUDITER :** `2777025fefb1a7edcd5f9017c5e8b6dff13972bf`  
**Base de formalisation P1.1 :** `8ed66310937fac6bf7305081ba6d230459cff5d2`

## 1. Rôle de Claude

Tu interviens comme **contre-expert code indépendant**, pas comme auteur de la prochaine architecture.

Ta mission est de chercher ce que le contrat et les cassages existants ont pu manquer dans le candidat P1.1 corrigé.

**Ne modifie aucun fichier. Ne commit rien. Ne pousse rien. Ne propose aucune correction avant d'avoir produit ton diagnostic adversarial.**

Le commit cible ci-dessus est la source de vérité pour le code candidat. Ne reconstruis pas l'état depuis un résumé conversationnel.

### Règle d'indépendance importante

Le dépôt contient désormais une contre-expertise Grok et une adjudication interne postérieures au candidat.

**Pour ta première passe, ne lis pas ces deux documents :**

- `docs/COUNTER-EXPERTISE-GROK-P1-1-DECISION-ACTION-AUTHORIZATION-2026-09-17.md`
- `docs/ADJUDICATION-P1-1-GROK-COUNTER-EXPERTISE-2026-09-17.md`

Produis d'abord tes propres findings depuis le code/contrat/tests. Tu pourras ensuite, seulement après avoir figé tes findings indépendants, comparer si nécessaire avec les attaques G0–G4 présentes dans le test de contre-expertise.

## 2. Question centrale

Le candidat P1.1 prétend garantir :

`qualified producer-created Decision → identity/content verification → authorization constraints → BLOCKED`

Il est volontairement **block-only** : aucun chemin positif `AUTHORIZED` n'est gouverné.

Question à casser :

> **Existe-t-il une manière réaliste de faire reconnaître comme admissible une Decision/AuthorizationConstraints non qualifiée, d'émettre ou forger un verdict positif, de préserver abusivement une attestation, de contourner le fail-closed, ou de préparer un bypass qui deviendrait critique dès l'ouverture d'un chemin AUTHORIZED ?**

## 3. Corpus exact à lire au commit `2777025f...`

Lire intégralement :

1. `04-REFERENCE/DECISION-ACTION-AUTHORIZATION-BOUNDARY-CONTRACT.md`
2. `src/decision.py`
3. `src/decision_action_authorization.py`
4. `tests/test_decision_action_authorization_tier_a.py`
5. `tests/test_decision_action_authorization_counterexpertise.py`
6. `.github/workflows/p1-1-decision-action-authorization.yml`
7. `src/research_run_evidence.py`
8. `tests/test_research_to_decision_boundary.py`
9. `src/context.py`
10. `src/decision_trace.py`
11. `src/promotion_gate.py`

Comparer aussi :

`8ed66310937fac6bf7305081ba6d230459cff5d2...2777025fefb1a7edcd5f9017c5e8b6dff13972bf`

N'élargis pas l'audit à toute l'architecture.

## 4. État de preuve à ne pas prendre comme autorité

Le candidat corrigé a un re-break vert :

- HEAD : `2777025fefb1a7edcd5f9017c5e8b6dff13972bf`
- workflow : `P1.1 Decision-Action Authorization Tier-A`
- run/job : `35201771267 / 105137965680`
- résultat : `SUCCESS`

Ce run couvre :

- persisted HEAD / P0.6 ancestry ;
- bounded / side-effect-free surface ;
- environnement P0.6 ;
- protected `RESEARCH → DECISION` ;
- A0–F5 ;
- attaques externes G0–G4 ;
- worktree propre.

**Ce vert ne vaut pas autorité sur ta contre-expertise.** Cherche à produire un nouveau rouge justifié.

## 5. Axes obligatoires

### A. Attestation Decision / constraints

Examiner :

- `id(...)` + weakref registry ;
- GC / cleanup / id reuse ;
- copy / replace / pickle / unpickle ;
- reload / module duplication ;
- process/sub-interpreter boundary ;
- closure/cell introspection ;
- capacité à altérer le registry ;
- mismatch entre preuve d'origine et simple preuve d'identité en mémoire.

Distinguer explicitement :

1. `CURRENT_BYPASS` ;
2. `FALSE_NEGATIVE_ONLY` ;
3. `IN_PROCESS_LIMIT` ;
4. `FUTURE_AUTHORIZED_RISK`.

### B. Verdict d'autorisation

Auditer particulièrement :

- `AuthorizationVerdict` ;
- validation runtime du statut ;
- reconstruction/copie ;
- monkeypatch de constantes/classes/helpers ;
- possibilité de fabriquer un objet ressemblant à un verdict positif ;
- provenance/non-forgeabilité nécessaire pour un futur consommateur ACTION ;
- confusion entre valeur textuelle `AUTHORIZED` et autorisation gouvernée.

### C. Binding cryptographique / identité

Vérifier :

- contenu exact de `decision_id` ;
- contenu exact de `constraint_id` ;
- troncature SHA-256 ;
- binding au payload ;
- replay / stale constraints ;
- version drift ;
- pertinence du chemin `__binding_only__` et de tout fallback/redondance.

### D. Monkeypatch / runtime mutation

Tester conceptuellement et, si utile, reproduire :

- verifier importé ;
- `BLOCKED`, `AUTHORIZED`, `CONSTRAINT_POLICY`, `CONTRACT` ;
- `_blocked`, `_stable_hash`, `_constraint_id` ;
- `Decision`, `AuthorizationConstraints`, `AuthorizationVerdict` ;
- `__globals__`, `__closure__`, cells.

Ne classe pas automatiquement toute introspection Python comme bug : explicite le threat model qui rend le scénario pertinent.

### E. Contrat / code / tests / workflow

Chercher :

- invariant contractuel non testé ;
- test qui prouve seulement l'implémentation ;
- rejet pour mauvaise raison ;
- dépendance de confiance non surveillée ;
- path CI manquant ;
- possibilité de changement silencieux d'une dépendance ;
- surface critique non incluse dans le re-break.

### F. Avant tout futur `AUTHORIZED`

Sans concevoir la politique positive, produire la liste fermée de ce qui doit être corrigé/qualifié **avant qu'un seul verdict positif puisse être consommé par ACTION**.

## 6. Interdictions

- ne pas construire ACTION ;
- ne pas ajouter moteur RISK ;
- ne pas coder sizing/levier/SL/TP ;
- ne pas ouvrir acquisition USATECH ;
- ne pas autoriser backtest réel ;
- ne pas autoriser live ;
- ne pas modifier le dépôt ;
- ne pas déclarer PASS uniquement parce que CI est verte.

## 7. Format obligatoire

### 1. VERDICT

Un seul :

- `PASS — no material bypass found in current block-only scope`
- `FAIL — material bypass found`
- `BLOCKED — insufficient evidence to conclude`

### 2. FINDINGS

Pour chaque finding :

- ID : `CLAUDE-P1.1-XX`
- sévérité : `CRITICAL / HIGH / MEDIUM / LOW / NOTE`
- catégorie : `CURRENT_BYPASS / FUTURE_AUTHORIZED_RISK / FALSE_NEGATIVE_ONLY / IN_PROCESS_LIMIT / TEST_GAP / WORKFLOW_GAP / CONTRACT_GAP`
- fichier + symbole ;
- mécanisme ;
- scénario reproductible ;
- impact ;
- couvert par A0–F5/G0–G4 : `YES / PARTIAL / NO`.

### 3. ADDITIONAL ATTACKS REQUIRED

Pour chaque attaque : précondition, manipulation, comportement fail-closed attendu, test minimal.

### 4. MUST-FIX BEFORE ANY AUTHORIZED PATH

Liste fermée.

### 5. SAFE TO DEFER

Éléments réellement hors scope block-only.

### 6. MINIMAL CORRECTION ORDER

Ordre minimal, sans patch complet sauf nécessité pour démontrer le finding.

## 8. Fin

Arrête-toi après le rapport adversarial. **Ne modifie rien.**

Le rapport sera ensuite vérifié, comparé aux preuves exécutables, puis adjudiqué avant toute extension de P1.1.
