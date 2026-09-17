# CONTRE-EXPERTISE GROK — P1.1 DECISION → ACTION AUTHORIZATION

**Source externe :** Grok  
**Statut :** SOURCE D'ANALYSE NON NORMATIVE  
**Cible auditée :** `304bf0c370c422b6cb8ea9159cbaf1c282ec01f9`  
**Date :** 2026-09-17

> Note de provenance : le rapport fourni utilisait des identifiants de finding préfixés `CLAUDE-P1.1-*`. Ils sont conservés ci-dessous comme identifiants textuels du rapport reçu, mais la source réelle de cette contre-expertise est Grok.

## Verdict externe fourni

`PASS — no material bypass found in current block-only scope`

Le rapport conclut qu'aucun bypass positif réaliste n'a été démontré dans le candidat P1.1 actuel, volontairement block-only, mais identifie plusieurs limites et risques futurs.

## Findings fournis

### CLAUDE-P1.1-01 — in-process weakref/id attestation

- Sévérité fournie : MEDIUM
- Catégorie : `IN_PROCESS_LIMIT / FUTURE_AUTHORIZED_RISK`
- Attestation purement in-process, par identité d'objet et fingerprint dans un registre weakref.
- Après GC, reload, process boundary, pickle/unpickle ou nouvelle identité objet, l'attestation est perdue.
- Impact annoncé : faux négatif aujourd'hui ; blocker de design si persistence/inter-process requis pour un futur `AUTHORIZED`.

### CLAUDE-P1.1-02 — monkeypatch / introspection

- Sévérité fournie : MEDIUM
- Catégorie : `FUTURE_AUTHORIZED_RISK / TEST_GAP`
- `evaluate_pre_action_authorization()` utilise des noms importés/module-level pouvant être monkeypatchés dans le même process.
- Les closures contenant les registries sont introspectables en CPython.
- Impact annoncé : pas de positif aujourd'hui à cause du hard block final ; fail-open potentiel si un chemin positif est ajouté sans durcissement/threat model.

### CLAUDE-P1.1-03 — identifiants tronqués SHA-256 16 hex

- Sévérité fournie : LOW
- Catégorie : `FUTURE_AUTHORIZED_RISK`
- `decision_id` / `constraint_id` utilisent 64 bits de préfixe SHA-256.
- Risque pratique faible tant qu'ils ne sont pas traités comme preuve cryptographique autonome.

### CLAUDE-P1.1-04 — binding constraints redondant

- Sévérité fournie : LOW / NOTE
- Catégorie : `CONTRACT_GAP / TEST_GAP`
- `_constraint_id()` dépend du `decision_id` plutôt que directement du payload ; la vérification comporte un double chemin `or` redondant avec reconstruction `__binding_only__`.
- Aucun bypass positif démontré.

### CLAUDE-P1.1-05 — workflow dependency gap

- Sévérité fournie : MEDIUM
- Catégorie : `WORKFLOW_GAP`
- Le workflow P1.1 ne se déclenche pas sur toutes les dépendances de confiance immédiates (`src/research_run_evidence.py`, `src/context.py`, fixtures, etc.).
- Impact : modification silencieuse possible d'une dépendance de confiance sans re-cassage P1.1.

### CLAUDE-P1.1-06 — réutilisation d'id après cleanup

- Sévérité fournie : NOTE
- Catégorie : `FALSE_NEGATIVE_ONLY / IN_PROCESS_LIMIT`
- Le callback weakref supprime l'entrée ; aucune héritage de fingerprint observé pour une nouvelle identité réutilisée.
- Impact annoncé : fail-closed uniquement.

## Attaques supplémentaires proposées par Grok

1. reload / registry reset ;
2. monkeypatch du verifier importé ;
3. introspection des closures / cellules registry ;
4. couverture des dépendances du workflow.

## Must-fix proposés avant tout chemin AUTHORIZED

1. protocole d'attestation compatible avec la durée de vie requise par le futur consommateur, ou invariant explicite strictement in-process ;
2. traitement de la surface monkeypatch/introspection avant branche positive ;
3. simplification du binding constraints ;
4. couverture CI des dépendances de confiance ;
5. décision explicite sur la troncature 16 hex avant usage persisted/cross-process.

## Safe-to-defer proposés

- troncature 16 hex tant que live-object + full fingerprint ;
- pickle/multiprocessing/sub-interpreter hors scope actuel ;
- logique quantitative risk/sizing/SL/TP ;
- politique `AUTHORIZED` ;
- signature cryptographique complète.

Ce document enregistre la source externe. Il ne vaut pas adjudication du dépôt.
