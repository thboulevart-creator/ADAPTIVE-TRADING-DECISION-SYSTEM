# PLAN MAÎTRE D'EXÉCUTION — ADAPTIVE TRADING DECISION SYSTEM

**Version :** 1.0  
**Date :** 20 août 2026  
**Statut :** Document de pilotage opérationnel  

> **Règle :** `[ ]` = non fait · `[x]` = fait et validé.

Ce fichier est notre **tableau de bord permanent**. Une case n'est cochée qu'après validation du résultat correspondant.

## Règle de gouvernance

**Action → Résultat → Validation → GO / NO-GO → prochaine action.**

Aucune phase ne passe à la suivante sans validation explicite de la précédente.

---

# PHASE 0 — CADRAGE

## Étape 0.1 — Figer le périmètre V1

### Sous-étape 0.1.1 — Définir le système
- [ ] **Objectif :** confirmer que le projet est un système de décision adaptatif et non un oracle prédictif.
- **Action :** utiliser `01-SYSTEM-VISION.md` comme référence.
- **Validation :** architecture et finalité comprises et acceptées.
- **GO / NO-GO :** GO lorsque le périmètre est figé.

### Sous-étape 0.1.2 — Définir les exclusions V1
- [ ] **Objectif :** empêcher la complexification prématurée.
- **Action :** exclure de V1 le réentraînement automatique, les MoE complexes, les centaines de features et l'optimisation massive.
- **Validation :** chaque nouvelle idée peut être classée V1 ou « plus tard ».
- **GO / NO-GO :** GO.

### Sous-étape 0.1.3 — Figer la gouvernance
- [ ] **Objectif :** empêcher les modifications incontrôlées.
- **Action :** appliquer `Pourquoi → Comment → Exemple → Test` et `Action → Résultat → Validation → GO/NO-GO`.
- **Validation :** règles utilisées pour les travaux suivants.
- **GO / NO-GO :** GO.

---

# PHASE 1 — DONNÉES

## Étape 1.1 — Définir les sources

### Sous-étape 1.1.1 — Inventaire des données
- [ ] **Objectif :** savoir exactement quelles données alimentent le système.
- **Action :** documenter source, actif, timeframe, période, timezone et format.
- **Validation :** chaque dataset possède une fiche d'identité.
- **GO / NO-GO :** GO si aucun dataset critique n'est ambigu.

### Sous-étape 1.1.2 — Contrôle qualité
- [ ] **Objectif :** éviter de construire sur des données défectueuses.
- **Action :** détecter trous, doublons, timestamps incohérents et anomalies.
- **Validation :** rapport qualité produit et anomalies traitées ou documentées.
- **GO / NO-GO :** GO si qualité acceptable.

### Sous-étape 1.1.3 — Intégrité temporelle
- [ ] **Objectif :** empêcher le futur d'entrer dans le passé.
- **Action :** définir et tester les règles anti-look-ahead / leakage.
- **Validation :** chaque variable est justifiable comme disponible au moment de la décision.
- **GO / NO-GO :** GO.

---

# PHASE 2 — ASSET PROFILE DATABASE

## Étape 2.1 — Définir l'univers V1

### Sous-étape 2.1.1 — Sélection initiale
- [ ] **Objectif :** travailler sur un univers petit mais représentatif.
- **Action :** sélectionner un premier groupe d'actifs, par exemple NAS100, XAUUSD, EURUSD et BTCUSD.
- **Validation :** univers documenté avant les tests de performance.
- **GO / NO-GO :** GO.

## Étape 2.2 — Construire les profils

### Sous-étape 2.2.1 — Profil comportemental
- [ ] **Objectif :** connaître le comportement historique de chaque actif.
- **Action :** renseigner volatilité, ATR, sessions, structure, liquidité, coûts, corrélations et régimes.
- **Validation :** chaque actif possède une fiche conforme à `02-ASSET-PROFILE-DATABASE.md`.
- **GO / NO-GO :** GO.

### Sous-étape 2.2.2 — Contrôle de cohérence
- [ ] **Objectif :** éviter les profils construits sur des conventions incohérentes.
- **Action :** vérifier que les métriques utilisent les mêmes conventions.
- **Validation :** comparaison reproductible entre actifs.
- **GO / NO-GO :** GO.

---

# PHASE 3 — BASELINES

## Étape 3.1 — Expert Momentum

### Sous-étape 3.1.1 — Définition V1
- [ ] **Objectif :** disposer d'un expert simple de tendance/momentum.
- **Action :** définir une règle déterministe minimale.
- **Validation :** règle écrite, reproductible et sans optimisation massive.
- **GO / NO-GO :** GO.

### Sous-étape 3.1.2 — Backtest baseline
- [ ] **Objectif :** mesurer le comportement brut.
- **Action :** tester sur les données définies avec coûts réalistes.
- **Validation :** résultats documentés.
- **GO / NO-GO :** GO.

## Étape 3.2 — Expert Breakout

### Sous-étape 3.2.1 — Définition V1
- [ ] **Objectif :** disposer d'un expert de cassure simple.
- **Action :** définir une règle déterministe minimale.
- **Validation :** règle reproductible.
- **GO / NO-GO :** GO.

### Sous-étape 3.2.2 — Backtest baseline
- [ ] **Objectif :** mesurer le comportement brut.
- **Action :** tester avec coûts réalistes.
- **Validation :** rapport produit.
- **GO / NO-GO :** GO.

## Étape 3.3 — Expert Mean Reversion

### Sous-étape 3.3.1 — Définition V1
- [ ] **Objectif :** disposer d'un expert de retour vers la moyenne.
- **Action :** définir une règle déterministe minimale.
- **Validation :** règle reproductible.
- **GO / NO-GO :** GO.

### Sous-étape 3.3.2 — Backtest baseline
- [ ] **Objectif :** mesurer le comportement brut.
- **Action :** tester avec coûts réalistes.
- **Validation :** rapport produit.
- **GO / NO-GO :** GO.

## Étape 3.4 — Référence commune

### Sous-étape 3.4.1 — Métriques communes
- [ ] **Objectif :** comparer les trois experts sur une base identique.
- **Action :** figer rendement, drawdown, expectancy, nombre de trades, coûts et stabilité.
- **Validation :** tableau comparatif commun.
- **GO / NO-GO :** GO.

---

# PHASE 4 — MOTEUR DE RÉGIME

## Étape 4.1 — Définir les régimes V1

### Sous-étape 4.1.1 — Taxonomie
- [ ] **Objectif :** définir un vocabulaire simple du marché.
- **Action :** TENDANCE / RANGE / BREAKOUT / STRESS.
- **Validation :** définitions compréhensibles sans modèle opaque.
- **GO / NO-GO :** GO.

## Étape 4.2 — Construire le détecteur

### Sous-étape 4.2.1 — ADX
- [ ] **Objectif :** mesurer la force directionnelle.
- **Action :** intégrer ADX sans l'utiliser comme prédiction de direction.
- **Validation :** calcul reproductible.
- **GO / NO-GO :** GO.

### Sous-étape 4.2.2 — ATR / volatilité
- [ ] **Objectif :** mesurer amplitude et expansion de volatilité.
- **Action :** intégrer ATR et une mesure de volatilité simple.
- **Validation :** calcul reproductible.
- **GO / NO-GO :** GO.

### Sous-étape 4.2.3 — Classification V1
- [ ] **Objectif :** transformer les variables en régime explicable.
- **Action :** écrire les règles de classification avant l'évaluation finale.
- **Validation :** chaque régime peut être expliqué.
- **GO / NO-GO :** GO.

## Étape 4.3 — Tester le régime

### Sous-étape 4.3.1 — Stabilité
- [ ] **Objectif :** éviter les changements de régime absurdes et excessifs.
- **Action :** analyser durée et fréquence des régimes.
- **Validation :** comportement temporel cohérent.
- **GO / NO-GO :** GO ou retour en conception.

### Sous-étape 4.3.2 — Valeur informative
- [ ] **Objectif :** vérifier que les régimes différencient réellement les environnements.
- **Action :** mesurer volatilité, performance et caractéristiques par régime.
- **Validation :** régimes statistiquement descriptifs.
- **GO / NO-GO :** GO si information utile démontrée.

---

# PHASE 5 — EXPERTS CONDITIONNELS

## Étape 5.1 — Performance par régime

### Sous-étape 5.1.1 — Momentum × régimes
- [ ] **Objectif :** mesurer où Momentum fonctionne.
- **Action :** ventiler les trades par régime.
- **Validation :** matrice complète.
- **GO / NO-GO :** GO.

### Sous-étape 5.1.2 — Breakout × régimes
- [ ] **Objectif :** mesurer où Breakout fonctionne.
- **Action :** ventiler les trades par régime.
- **Validation :** matrice complète.
- **GO / NO-GO :** GO.

### Sous-étape 5.1.3 — Mean Reversion × régimes
- [ ] **Objectif :** mesurer où Mean Reversion fonctionne.
- **Action :** ventiler les trades par régime.
- **Validation :** matrice complète.
- **GO / NO-GO :** GO.

## Étape 5.2 — Comparaison

### Sous-étape 5.2.1 — Matrice expert/régime
- [ ] **Objectif :** savoir si les experts ont réellement des spécialités conditionnelles.
- **Action :** construire la matrice complète.
- **Validation :** relation régime → expert mesurable et robuste.
- **GO / NO-GO :** GO uniquement si l'effet est suffisamment stable.

---

# PHASE 6 — COMPARATEUR

## Étape 6.1 — Baseline vs conditionnel

### Sous-étape 6.1.1 — Comparaison brute
- [ ] **Objectif :** mesurer la valeur ajoutée du contexte.
- **Action :** comparer chaque expert globalement à sa version conditionnée.
- **Validation :** comparaison homogène.
- **GO / NO-GO :** GO si amélioration robuste, sinon abandon ou modification de l'hypothèse.

### Sous-étape 6.1.2 — Coûts
- [ ] **Objectif :** vérifier que l'avantage survit aux coûts.
- **Action :** intégrer spread, commission et slippage.
- **Validation :** avantage net des coûts.
- **GO / NO-GO :** GO.

---

# PHASE 7 — ROUTEUR

## Étape 7.1 — Routeur V1

### Sous-étape 7.1.1 — Règles déterministes
- [ ] **Objectif :** sélectionner l'expert adapté sans IA opaque.
- **Action :** écrire les règles régime → expert.
- **Validation :** chaque décision est explicable.
- **GO / NO-GO :** GO.

### Sous-étape 7.1.2 — Stress
- [ ] **Objectif :** protéger le capital plutôt que forcer un trade.
- **Action :** définir réduction d'exposition / absence de trade.
- **Validation :** le routeur peut refuser une opération.
- **GO / NO-GO :** GO.

## Étape 7.2 — Tester le routage

### Sous-étape 7.2.1 — Routeur vs experts seuls
- [ ] **Objectif :** démontrer une valeur économique réelle.
- **Action :** comparer le système routé aux baselines.
- **Validation :** résultats robustes hors échantillon.
- **GO / NO-GO :** GO / NO-GO selon résultats.

---

# PHASE 8 — RISQUE & PORTEFEUILLE

## Étape 8.1 — Risk Engine

### Sous-étape 8.1.1 — Limites
- [ ] **Objectif :** définir l'exposition maximale acceptable.
- **Action :** risque par trade, risque global, drawdown, levier, concentration et corrélations.
- **Validation :** règles écrites et testables.
- **GO / NO-GO :** GO.

### Sous-étape 8.1.2 — Kill Switch
- [ ] **Objectif :** empêcher le système de continuer dans des conditions dangereuses.
- **Action :** définir les conditions de HALT.
- **Validation :** chaque condition provoque le comportement attendu.
- **GO / NO-GO :** GO.

## Étape 8.2 — Portfolio Engine

### Sous-étape 8.2.1 — Exposition multi-actifs
- [ ] **Objectif :** gérer plusieurs décisions simultanément.
- **Action :** intégrer corrélation, concentration et budget de risque.
- **Validation :** exposition globale calculable avant exécution.
- **GO / NO-GO :** GO.

---

# PHASE 9 — EXÉCUTION

## Étape 9.1 — Coût d'exécution

### Sous-étape 9.1.1 — Modèle de coûts
- [ ] **Objectif :** transformer l'alpha brut en décision économique.
- **Action :** spread, commission, slippage, financement et contraintes horaires.
- **Validation :** coût estimé disponible avant décision.
- **GO / NO-GO :** GO.

## Étape 9.2 — Python → MT5

### Sous-étape 9.2.1 — Spécification
- [ ] **Objectif :** séparer recherche et exécution.
- **Action :** figer les règles avant implémentation MQL5.
- **Validation :** spécification traçable.
- **GO / NO-GO :** GO.

### Sous-étape 9.2.2 — Validation MT5
- [ ] **Objectif :** vérifier que l'implémentation respecte la logique validée.
- **Action :** tester sur MT5 avec des paramètres réalistes.
- **Validation :** parité fonctionnelle suffisante avec la référence Python.
- **GO / NO-GO :** GO.

---

# PHASE 10 — VALIDATION WALK-FORWARD

## Étape 10.1 — Protocole temporel

### Sous-étape 10.1.1 — Train / Validation / OOS
- [ ] **Objectif :** protéger l'indépendance des tests.
- **Action :** définir les fenêtres temporelles.
- **Validation :** aucune information future ne traverse les frontières.
- **GO / NO-GO :** GO.

### Sous-étape 10.1.2 — Walk-Forward
- [ ] **Objectif :** tester la robustesse dans le temps.
- **Action :** exécuter plusieurs fenêtres chronologiques.
- **Validation :** résultats agrégés et distribués dans le temps.
- **GO / NO-GO :** GO.

## Étape 10.2 — Audit des biais

### Sous-étape 10.2.1 — Checklist
- [ ] **Objectif :** éviter les faux résultats.
- **Action :** auditer look-ahead, leakage, overfitting, data snooping, survivorship, selection bias et contamination OOS.
- **Validation :** audit documenté sans anomalie critique.
- **GO / NO-GO :** GO / NO-GO.

## Étape 10.3 — Robustesse

### Sous-étape 10.3.1 — Stress tests
- [ ] **Objectif :** vérifier que le résultat ne dépend pas d'une condition fragile.
- **Action :** varier raisonnablement coûts, paramètres, périodes et actifs.
- **Validation :** comportement robuste.
- **GO / NO-GO :** GO / NO-GO.

---

# PHASE 11 — MONITORING & DRIFT

## Étape 11.1 — Monitoring production

### Sous-étape 11.1.1 — Performance
- [ ] **Objectif :** surveiller la santé du système.
- **Action :** suivre performance, drawdown, expectancy et stabilité.
- **Validation :** métriques disponibles régulièrement.
- **GO / NO-GO :** GO.

### Sous-étape 11.1.2 — Data / regime / execution drift
- [ ] **Objectif :** détecter les changements de comportement.
- **Action :** surveiller données, régimes et coûts d'exécution.
- **Validation :** seuils d'alerte définis.
- **GO / NO-GO :** GO.

---

# PHASE 12 — CHAMPION / CHALLENGER

## Étape 12.1 — Détection d'une dégradation

### Sous-étape 12.1.1 — Déclencheur d'analyse
- [ ] **Objectif :** lancer une analyse sans réentraîner automatiquement.
- **Action :** définir les conditions de dégradation significative.
- **Validation :** alerte générée sans modification de production.
- **GO / NO-GO :** GO.

## Étape 12.2 — Nouveau modèle

### Sous-étape 12.2.1 — Proposition Challenger
- [ ] **Objectif :** créer une hypothèse alternative contrôlée.
- **Action :** définir et documenter le challenger.
- **Validation :** challenger reproductible et isolé du champion.
- **GO / NO-GO :** GO vers validation.

### Sous-étape 12.2.2 — Validation Challenger
- [ ] **Objectif :** empêcher une promotion basée sur une simple amélioration historique.
- **Action :** appliquer le protocole complet de validation.
- **Validation :** challenger supérieur selon les critères définis.
- **GO / NO-GO :** GO vers comparaison finale ou rejet.

## Étape 12.3 — Promotion

### Sous-étape 12.3.1 — Champion → Challenger
- [ ] **Objectif :** promouvoir uniquement une amélioration démontrée.
- **Action :** comparer champion et challenger selon le protocole officiel.
- **Validation :** tous les critères de promotion sont réunis.
- **GO / NO-GO :** GO = promotion ; NO-GO = champion conservé.

---

# PHASE 13 — PRODUCTION

## Étape 13.1 — Mise en production

### Sous-étape 13.1.1 — Checklist production
- [ ] **Objectif :** vérifier que tout est prêt avant exposition réelle.
- **Action :** contrôler données, modèle, risque, exécution, monitoring et kill switch.
- **Validation :** checklist complète.
- **GO / NO-GO :** GO uniquement si aucun point critique n'est ouvert.

### Sous-étape 13.1.2 — Première période contrôlée
- [ ] **Objectif :** observer le comportement réel sans supposer que le backtest suffit.
- **Action :** démarrer avec exposition contrôlée et monitoring renforcé.
- **Validation :** comportement conforme aux attentes.
- **GO / NO-GO :** GO vers fonctionnement normal ou retour en analyse.

---

# RÈGLE DE FIN DE SESSION

À la fin de chaque session :

```text
1. Identifier la phase actuelle.
2. Identifier l'étape et la sous-étape actuelle.
3. Cocher uniquement les actions réellement terminées.
4. Documenter tout résultat important.
5. Déclarer GO / NO-GO.
6. Identifier UNE prochaine action prioritaire.
```

## Format de compte rendu

```text
PHASE : X
ÉTAPE : X.X
SOUS-ÉTAPE : X.X.X

FAIT :
- ...

RÉSULTAT :
- ...

VALIDATION :
- ...

GO / NO-GO :
- GO / NO-GO

PROCHAINE ACTION :
- ...
```

---

# BOUSSOLE DU PROJET

> **Comprendre → mesurer → comparer → adapter → contrôler → valider → produire.**

> **La complexité est une récompense de la preuve, jamais un point de départ.**
