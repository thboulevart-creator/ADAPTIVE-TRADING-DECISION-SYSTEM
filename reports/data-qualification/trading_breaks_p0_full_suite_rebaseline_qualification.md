# Trading Breaks — P0 Full-Suite Rebaseline Qualification

**Date:** 16 septembre 2026  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `feat/multi-year-dukascopy-acquisition`  
**Qualified cleaned HEAD:** `77e02094de76a4c02c9face507c4875dec382b12`  
**Verdict:** **PASS — `P0_FULL_SUITE_REBASELINE_PERSISTED_HEAD_REBREAK_CONFIRMS_CURRENT_AND_HISTORICAL_REGRESSION_CORPUS`**

## 1. Objet

Ce rapport ferme le bloc P0.0 demandé après la clôture du calendrier Trading Breaks.

Le problème à corriger n'était pas une régression du calendrier courant mais une contradiction de temporalité dans le corpus de tests : des tests construits pour des états historiques pré-intégration continuaient à être exécutés comme s'ils décrivaient l'état courant post-clôture.

Avant correction, la suite complète exposait `115 failed / 537 passed`.

La qualification devait donc restaurer une seule propriété :

> **la suite complète doit continuer à casser tout défaut réel, tout en distinguant explicitement les invariants historiques des invariants du HEAD courant.**

Aucun PASS ne pouvait être obtenu par suppression de test, `skip`, `xfail`, affaiblissement d'assertion ou reconstruction manuelle d'un ancien état.

## 2. Rebaseline historique fail-closed

Le rebaseline conserve exactement :

- `115` node IDs historiques ;
- répartis sur `42` fichiers de tests ;
- versionnés dans `tests/historical_regression_baselines.json` ;
- chaque node ID lié à un commit Git historiquement vérifié comme vert pour le fichier concerné.

Le mécanisme de replay est porté par `tests/conftest.py`.

Il est fail-closed :

1. un node ID historique absent de la collection courante provoque un échec ;
2. un SHA de baseline mal formé ou indisponible provoque un échec ;
3. le fichier historique est rejoué dans un worktree Git détaché sur son commit épinglé ;
4. si le replay historique échoue, le test courant échoue ;
5. aucun `skip`, `xfail` ou effacement de test n'est utilisé ;
6. les worktrees temporaires sont retirés après la session.

Le manifeste historique a été persisté au commit `e1f0b16b79297b9ab1b4d3c872a9452a897ad003`.

Le raccord de replay et les assertions de vérité courante ont été persistés au commit `5c9ab2c82d9793f8029d18f2a8cd395624e9a972`.

## 3. Vérité courante séparée de l'histoire

La suite courante certifie explicitement l'état post-clôture au lieu de l'inférer depuis les anciens tests.

État courant qualifié :

### Global

- candidates: `111`
- resolved: `91`
- unresolved: `20`
- special-session evidence dates: `88`
- no-special-change evidence dates: `3`
- coverage verdict: **BLOCKED**
- orphan special evidence: `0`
- contradictory evidence dates: `0`
- evidence-shape errors: `0`

Les `20` dates globalement non résolues sont toutes antérieures au début de la fenêtre d'exécution candidate.

### Fenêtre candidate `2021-08-14 → 2026-08-14`

- candidates: `68`
- resolved: `68`
- unresolved: `0`
- FAIL: `0`
- coverage verdict: **PASS**

### Recovery / progression

- attempt ledger: `73`
- material capability changes: `1`
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- current fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`
- recovery queue: empty
- progression decisions: empty
- eligible recovery queue: empty

### Negative evidence intégrée

`NO_SPECIAL_CHANGE_EVIDENCE` contient exactement :

1. `2021-12-31`
2. `2022-07-01`
3. `2026-07-02`

Chaque entrée est liée à `TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1`, avec le verdict factuel `NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY` et sa provenance persistée.

## 4. Gouvernance P0.0

Le corpus de gouvernance autoritatif de la branche a été restauré depuis `main` avant le rebaseline.

Le contrat `GOVERNANCE_RELAXATION_COOLING_OFF_V1` a ensuite été appliqué par le finalizer.

Le commit produit par ce finalizer est :

`102835db477c92d161fb7a4004b287d28dd54010`

Son parent direct est :

`965c031020883d0c6517183b073dddf0e7c2e7dc`

Il modifie exactement trois fichiers :

- `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`
- `GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md`
- `tests/test_governance_relaxation_cooling_off_contract.py`

Aucune autre surface n'a été modifiée par ce finalizer.

Le contrat impose notamment une carence minimale de `30 jours` avant un assouplissement de gouvernance causalement lié à un incident, une perte, une opportunité manquée ou une contrainte opérationnelle ; un événement de même cause réinitialise la carence. Il conserve aussi l'asymétrie : le système peut devenir plus restrictif seul, jamais plus permissif seul.

## 5. Nettoyage du véhicule temporaire

Après application de la gouvernance :

- `.github/workflows/governance-p0-repair.yml` a été restauré en re-break permanent **read-only** au commit `5a1dcd4b9030396ff46db6c1e660d0c20a342214` ;
- le workflow jetable `.github/workflows/p0-governance-finalize-once.yml` a été supprimé au commit `77e02094de76a4c02c9face507c4875dec382b12`.

Le HEAD `77e02094de76a4c02c9face507c4875dec382b12` est donc le HEAD nettoyé utilisé pour la qualification finale.

## 6. Suite complète — preuve finale

### Full Suite Regression

- workflow: `Full Suite Regression`
- run/job: `35120428859 / 104876523965`
- HEAD: `77e02094de76a4c02c9face507c4875dec382b12`
- conclusion: **success**
- résultat: **`659 passed in 17.65s`**
- worktree final: clean
- permissions observées: `contents: read`, `metadata: read`

### Persisted-HEAD re-break indépendant

- workflow: `P0 Full Suite Persisted HEAD Rebreak`
- run/job: `35120428855 / 104876523450`
- HEAD vérifié: `77e02094de76a4c02c9face507c4875dec382b12`
- exact persisted-HEAD checkout: **PASS**
- manifeste `115 node IDs / 42 fichiers`: **PASS**
- conclusion: **success**
- résultat: **`659 passed in 14.47s`**
- worktree final: clean
- permissions observées: `contents: read`, `metadata: read`

Les deux exécutions sont indépendantes et portent sur le même SHA nettoyé.

## 7. Ce que ce PASS autorise — et ce qu'il n'autorise pas

Ce PASS ferme uniquement P0.0 : le corpus de régression complet est de nouveau cohérent, vert, reproductible et fail-closed sur la distinction passé / présent.

Il ne signifie pas :

- `DECLARE_GLOBAL_COVERAGE_PASS` ;
- que les `20` gaps globaux ont disparu ;
- que la fenêtre candidate est déjà formellement gelée ;
- que `BoundaryState` est déjà dérivé de preuves ;
- que l'acquisition `.bi5` est autorisée ;
- qu'un backtest réel est autorisé ;
- que la jonction `src/research/ ↔ research_run_evidence` est qualifiée ;
- que l'attestation inter-processus est qualifiée.

`BLOCKED` n'est jamais `PASS`.

## 8. Verdict

**PASS — `P0_FULL_SUITE_REBASELINE_PERSISTED_HEAD_REBREAK_CONFIRMS_CURRENT_AND_HISTORICAL_REGRESSION_CORPUS`**

Le corpus historique reste exécutable et falsifiable, la vérité post-clôture est testée séparément, la gouvernance temporaire a été nettoyée, et les deux suites complètes indépendantes sont vertes sur le même HEAD nettoyé.

## 9. Prochaine action gouvernée unique

**P0.1 — construire un `BoundaryState` dérivé exclusivement des preuves versionnées, le casser adversarialement, puis seulement évaluer `FREEZE_EXECUTION_WINDOW`.**

Ne pas geler la fenêtre par déclaration.  
Ne pas déclarer la couverture globale PASS.  
Ne pas acquérir `.bi5`.  
Ne pas lancer de backtest réel.
