# PLAN MAÃŽTRE D'EXÃ‰CUTION â€” ADAPTIVE TRADING DECISION SYSTEM

**Version :** 1.0  
**Date :** 20 aoÃ»t 2026  
**Statut :** Document de pilotage opÃ©rationnel  

> **RÃ¨gle :** `[ ]` = non fait Â· `[x]` = fait et validÃ©.

Ce fichier est notre **tableau de bord permanent**. Une case n'est cochÃ©e qu'aprÃ¨s validation du rÃ©sultat correspondant.

## RÃ¨gle de gouvernance

**Action â†’ RÃ©sultat â†’ Validation â†’ GO / NO-GO â†’ prochaine action.**

Aucune phase ne passe Ã  la suivante sans validation explicite de la prÃ©cÃ©dente.

---

# PHASE 0 â€” CADRAGE

## Ã‰tape 0.1 â€” Figer le pÃ©rimÃ¨tre V1

### Sous-Ã©tape 0.1.1 â€” DÃ©finir le systÃ¨me
- [ ] **Objectif :** confirmer que le projet est un systÃ¨me de dÃ©cision adaptatif et non un oracle prÃ©dictif.
- **Action :** utiliser `01-SYSTEM-VISION.md` comme rÃ©fÃ©rence.
- **Validation :** architecture et finalitÃ© comprises et acceptÃ©es.
- **GO / NO-GO :** GO lorsque le pÃ©rimÃ¨tre est figÃ©.

### Sous-Ã©tape 0.1.2 â€” DÃ©finir les exclusions V1
- [ ] **Objectif :** empÃªcher la complexification prÃ©maturÃ©e.
- **Action :** exclure de V1 le rÃ©entraÃ®nement automatique, les MoE complexes, les centaines de features et l'optimisation massive.
- **Validation :** chaque nouvelle idÃ©e peut Ãªtre classÃ©e V1 ou Â« plus tard Â».
- **GO / NO-GO :** GO.

### Sous-Ã©tape 0.1.3 â€” Figer la gouvernance
- [ ] **Objectif :** empÃªcher les modifications incontrÃ´lÃ©es.
- **Action :** appliquer `Pourquoi â†’ Comment â†’ Exemple â†’ Test` et `Action â†’ RÃ©sultat â†’ Validation â†’ GO/NO-GO`.
- **Validation :** rÃ¨gles utilisÃ©es pour les travaux suivants.
- **GO / NO-GO :** GO.

---

# PHASE 1 â€” DONNÃ‰ES

## Ã‰tape 1.1 â€” DÃ©finir les sources

### Sous-Ã©tape 1.1.1 â€” Inventaire des donnÃ©es
- [ ] **Objectif :** savoir exactement quelles donnÃ©es alimentent le systÃ¨me.
- **Action :** documenter source, actif, timeframe, pÃ©riode, timezone et format.
- **Validation :** chaque dataset possÃ¨de une fiche d'identitÃ©.
- **GO / NO-GO :** GO si aucun dataset critique n'est ambigu.

### Sous-Ã©tape 1.1.2 â€” ContrÃ´le qualitÃ©
- [ ] **Objectif :** Ã©viter de construire sur des donnÃ©es dÃ©fectueuses.
- **Action :** dÃ©tecter trous, doublons, timestamps incohÃ©rents et anomalies.
- **Validation :** rapport qualitÃ© produit et anomalies traitÃ©es ou documentÃ©es.
- **GO / NO-GO :** GO si qualitÃ© acceptable.

### Sous-Ã©tape 1.1.3 â€” IntÃ©gritÃ© temporelle
- [ ] **Objectif :** empÃªcher le futur d'entrer dans le passÃ©.
- **Action :** dÃ©finir et tester les rÃ¨gles anti-look-ahead / leakage.
- **Validation :** chaque variable est justifiable comme disponible au moment de la dÃ©cision.
- **GO / NO-GO :** GO.

---

# PHASE 2 â€” ASSET PROFILE DATABASE

## Ã‰tape 2.1 â€” DÃ©finir l'univers V1

### Sous-Ã©tape 2.1.1 â€” SÃ©lection initiale
- [ ] **Objectif :** travailler sur un univers petit mais reprÃ©sentatif.
- **Action :** sÃ©lectionner un premier groupe d'actifs, par exemple NAS100, XAUUSD, EURUSD et BTCUSD.
- **Validation :** univers documentÃ© avant les tests de performance.
- **GO / NO-GO :** GO.

## Ã‰tape 2.2 â€” Construire les profils

### Sous-Ã©tape 2.2.1 â€” Profil comportemental
- [ ] **Objectif :** connaÃ®tre le comportement historique de chaque actif.
- **Action :** renseigner volatilitÃ©, ATR, sessions, structure, liquiditÃ©, coÃ»ts, corrÃ©lations et rÃ©gimes.
- **Validation :** chaque actif possÃ¨de une fiche conforme Ã  `02-ASSET-PROFILE-DATABASE.md`.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 2.2.2 â€” ContrÃ´le de cohÃ©rence
- [ ] **Objectif :** Ã©viter les profils construits sur des conventions incohÃ©rentes.
- **Action :** vÃ©rifier que les mÃ©triques utilisent les mÃªmes conventions.
- **Validation :** comparaison reproductible entre actifs.
- **GO / NO-GO :** GO.

---

# PHASE 3 â€” BASELINES

## Ã‰tape 3.1 â€” Expert Momentum

### Sous-Ã©tape 3.1.1 â€” DÃ©finition V1
- [ ] **Objectif :** disposer d'un expert simple de tendance/momentum.
- **Action :** dÃ©finir une rÃ¨gle dÃ©terministe minimale.
- **Validation :** rÃ¨gle Ã©crite, reproductible et sans optimisation massive.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 3.1.2 â€” Backtest baseline
- [ ] **Objectif :** mesurer le comportement brut.
- **Action :** tester sur les donnÃ©es dÃ©finies avec coÃ»ts rÃ©alistes.
- **Validation :** rÃ©sultats documentÃ©s.
- **GO / NO-GO :** GO.

## Ã‰tape 3.2 â€” Expert Breakout

### Sous-Ã©tape 3.2.1 â€” DÃ©finition V1
- [ ] **Objectif :** disposer d'un expert de cassure simple.
- **Action :** dÃ©finir une rÃ¨gle dÃ©terministe minimale.
- **Validation :** rÃ¨gle reproductible.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 3.2.2 â€” Backtest baseline
- [ ] **Objectif :** mesurer le comportement brut.
- **Action :** tester avec coÃ»ts rÃ©alistes.
- **Validation :** rapport produit.
- **GO / NO-GO :** GO.

## Ã‰tape 3.3 â€” Expert Mean Reversion

### Sous-Ã©tape 3.3.1 â€” DÃ©finition V1
- [ ] **Objectif :** disposer d'un expert de retour vers la moyenne.
- **Action :** dÃ©finir une rÃ¨gle dÃ©terministe minimale.
- **Validation :** rÃ¨gle reproductible.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 3.3.2 â€” Backtest baseline
- [ ] **Objectif :** mesurer le comportement brut.
- **Action :** tester avec coÃ»ts rÃ©alistes.
- **Validation :** rapport produit.
- **GO / NO-GO :** GO.

## Ã‰tape 3.4 â€” RÃ©fÃ©rence commune

### Sous-Ã©tape 3.4.1 â€” MÃ©triques communes
- [ ] **Objectif :** comparer les trois experts sur une base identique.
- **Action :** figer rendement, drawdown, expectancy, nombre de trades, coÃ»ts et stabilitÃ©.
- **Validation :** tableau comparatif commun.
- **GO / NO-GO :** GO.

---

# PHASE 4 â€” MOTEUR DE RÃ‰GIME

## Ã‰tape 4.1 â€” DÃ©finir les rÃ©gimes V1

### Sous-Ã©tape 4.1.1 â€” Taxonomie
- [ ] **Objectif :** dÃ©finir un vocabulaire simple du marchÃ©.
- **Action :** TENDANCE / RANGE / BREAKOUT / STRESS.
- **Validation :** dÃ©finitions comprÃ©hensibles sans modÃ¨le opaque.
- **GO / NO-GO :** GO.

## Ã‰tape 4.2 â€” Construire le dÃ©tecteur

### Sous-Ã©tape 4.2.1 â€” ADX
- [ ] **Objectif :** mesurer la force directionnelle.
- **Action :** intÃ©grer ADX sans l'utiliser comme prÃ©diction de direction.
- **Validation :** calcul reproductible.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 4.2.2 â€” ATR / volatilitÃ©
- [ ] **Objectif :** mesurer amplitude et expansion de volatilitÃ©.
- **Action :** intÃ©grer ATR et une mesure de volatilitÃ© simple.
- **Validation :** calcul reproductible.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 4.2.3 â€” Classification V1
- [ ] **Objectif :** transformer les variables en rÃ©gime explicable.
- **Action :** Ã©crire les rÃ¨gles de classification avant l'Ã©valuation finale.
- **Validation :** chaque rÃ©gime peut Ãªtre expliquÃ©.
- **GO / NO-GO :** GO.

## Ã‰tape 4.3 â€” Tester le rÃ©gime

### Sous-Ã©tape 4.3.1 â€” StabilitÃ©
- [ ] **Objectif :** Ã©viter les changements de rÃ©gime absurdes et excessifs.
- **Action :** analyser durÃ©e et frÃ©quence des rÃ©gimes.
- **Validation :** comportement temporel cohÃ©rent.
- **GO / NO-GO :** GO ou retour en conception.

### Sous-Ã©tape 4.3.2 â€” Valeur informative
- [ ] **Objectif :** vÃ©rifier que les rÃ©gimes diffÃ©rencient rÃ©ellement les environnements.
- **Action :** mesurer volatilitÃ©, performance et caractÃ©ristiques par rÃ©gime.
- **Validation :** rÃ©gimes statistiquement descriptifs.
- **GO / NO-GO :** GO si information utile dÃ©montrÃ©e.

---

# PHASE 5 â€” EXPERTS CONDITIONNELS

## Ã‰tape 5.1 â€” Performance par rÃ©gime

### Sous-Ã©tape 5.1.1 â€” Momentum Ã— rÃ©gimes
- [ ] **Objectif :** mesurer oÃ¹ Momentum fonctionne.
- **Action :** ventiler les trades par rÃ©gime.
- **Validation :** matrice complÃ¨te.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 5.1.2 â€” Breakout Ã— rÃ©gimes
- [ ] **Objectif :** mesurer oÃ¹ Breakout fonctionne.
- **Action :** ventiler les trades par rÃ©gime.
- **Validation :** matrice complÃ¨te.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 5.1.3 â€” Mean Reversion Ã— rÃ©gimes
- [ ] **Objectif :** mesurer oÃ¹ Mean Reversion fonctionne.
- **Action :** ventiler les trades par rÃ©gime.
- **Validation :** matrice complÃ¨te.
- **GO / NO-GO :** GO.

## Ã‰tape 5.2 â€” Comparaison

### Sous-Ã©tape 5.2.1 â€” Matrice expert/rÃ©gime
- [ ] **Objectif :** savoir si les experts ont rÃ©ellement des spÃ©cialitÃ©s conditionnelles.
- **Action :** construire la matrice complÃ¨te.
- **Validation :** relation rÃ©gime â†’ expert mesurable et robuste.
- **GO / NO-GO :** GO uniquement si l'effet est suffisamment stable.

---

# PHASE 6 â€” COMPARATEUR

## Ã‰tape 6.1 â€” Baseline vs conditionnel

### Sous-Ã©tape 6.1.1 â€” Comparaison brute
- [ ] **Objectif :** mesurer la valeur ajoutÃ©e du contexte.
- **Action :** comparer chaque expert globalement Ã  sa version conditionnÃ©e.
- **Validation :** comparaison homogÃ¨ne.
- **GO / NO-GO :** GO si amÃ©lioration robuste, sinon abandon ou modification de l'hypothÃ¨se.

### Sous-Ã©tape 6.1.2 â€” CoÃ»ts
- [ ] **Objectif :** vÃ©rifier que l'avantage survit aux coÃ»ts.
- **Action :** intÃ©grer spread, commission et slippage.
- **Validation :** avantage net des coÃ»ts.
- **GO / NO-GO :** GO.

---

# PHASE 7 â€” ROUTEUR

## Ã‰tape 7.1 â€” Routeur V1

### Sous-Ã©tape 7.1.1 â€” RÃ¨gles dÃ©terministes
- [ ] **Objectif :** sÃ©lectionner l'expert adaptÃ© sans IA opaque.
- **Action :** Ã©crire les rÃ¨gles rÃ©gime â†’ expert.
- **Validation :** chaque dÃ©cision est explicable.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 7.1.2 â€” Stress
- [ ] **Objectif :** protÃ©ger le capital plutÃ´t que forcer un trade.
- **Action :** dÃ©finir rÃ©duction d'exposition / absence de trade.
- **Validation :** le routeur peut refuser une opÃ©ration.
- **GO / NO-GO :** GO.

## Ã‰tape 7.2 â€” Tester le routage

### Sous-Ã©tape 7.2.1 â€” Routeur vs experts seuls
- [ ] **Objectif :** dÃ©montrer une valeur Ã©conomique rÃ©elle.
- **Action :** comparer le systÃ¨me routÃ© aux baselines.
- **Validation :** rÃ©sultats robustes hors Ã©chantillon.
- **GO / NO-GO :** GO / NO-GO selon rÃ©sultats.

---

# PHASE 8 â€” RISQUE & PORTEFEUILLE

## Ã‰tape 8.1 â€” Risk Engine

### Sous-Ã©tape 8.1.1 â€” Limites
- [ ] **Objectif :** dÃ©finir l'exposition maximale acceptable.
- **Action :** risque par trade, risque global, drawdown, levier, concentration et corrÃ©lations.
- **Validation :** rÃ¨gles Ã©crites et testables.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 8.1.2 â€” Kill Switch
- [ ] **Objectif :** empÃªcher le systÃ¨me de continuer dans des conditions dangereuses.
- **Action :** dÃ©finir les conditions de HALT.
- **Validation :** chaque condition provoque le comportement attendu.
- **GO / NO-GO :** GO.

## Ã‰tape 8.2 â€” Portfolio Engine

### Sous-Ã©tape 8.2.1 â€” Exposition multi-actifs
- [ ] **Objectif :** gÃ©rer plusieurs dÃ©cisions simultanÃ©ment.
- **Action :** intÃ©grer corrÃ©lation, concentration et budget de risque.
- **Validation :** exposition globale calculable avant exÃ©cution.
- **GO / NO-GO :** GO.

---

# PHASE 9 â€” EXÃ‰CUTION

## Ã‰tape 9.1 â€” CoÃ»t d'exÃ©cution

### Sous-Ã©tape 9.1.1 â€” ModÃ¨le de coÃ»ts
- [ ] **Objectif :** transformer l'alpha brut en dÃ©cision Ã©conomique.
- **Action :** spread, commission, slippage, financement et contraintes horaires.
- **Validation :** coÃ»t estimÃ© disponible avant dÃ©cision.
- **GO / NO-GO :** GO.

## Ã‰tape 9.2 â€” Python â†’ MT5

### Sous-Ã©tape 9.2.1 â€” SpÃ©cification
- [ ] **Objectif :** sÃ©parer recherche et exÃ©cution.
- **Action :** figer les rÃ¨gles avant implÃ©mentation MQL5.
- **Validation :** spÃ©cification traÃ§able.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 9.2.2 â€” Validation MT5
- [ ] **Objectif :** vÃ©rifier que l'implÃ©mentation respecte la logique validÃ©e.
- **Action :** tester sur MT5 avec des paramÃ¨tres rÃ©alistes.
- **Validation :** paritÃ© fonctionnelle suffisante avec la rÃ©fÃ©rence Python.
- **GO / NO-GO :** GO.

---

# PHASE 10 â€” VALIDATION WALK-FORWARD

## Ã‰tape 10.1 â€” Protocole temporel

### Sous-Ã©tape 10.1.1 â€” Train / Validation / OOS
- [ ] **Objectif :** protÃ©ger l'indÃ©pendance des tests.
- **Action :** dÃ©finir les fenÃªtres temporelles.
- **Validation :** aucune information future ne traverse les frontiÃ¨res.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 10.1.2 â€” Walk-Forward
- [ ] **Objectif :** tester la robustesse dans le temps.
- **Action :** exÃ©cuter plusieurs fenÃªtres chronologiques.
- **Validation :** rÃ©sultats agrÃ©gÃ©s et distribuÃ©s dans le temps.
- **GO / NO-GO :** GO.

## Ã‰tape 10.2 â€” Audit des biais

### Sous-Ã©tape 10.2.1 â€” Checklist
- [ ] **Objectif :** Ã©viter les faux rÃ©sultats.
- **Action :** auditer look-ahead, leakage, overfitting, data snooping, survivorship, selection bias et contamination OOS.
- **Validation :** audit documentÃ© sans anomalie critique.
- **GO / NO-GO :** GO / NO-GO.

## Ã‰tape 10.3 â€” Robustesse

### Sous-Ã©tape 10.3.1 â€” Stress tests
- [ ] **Objectif :** vÃ©rifier que le rÃ©sultat ne dÃ©pend pas d'une condition fragile.
- **Action :** varier raisonnablement coÃ»ts, paramÃ¨tres, pÃ©riodes et actifs.
- **Validation :** comportement robuste.
- **GO / NO-GO :** GO / NO-GO.

---

# PHASE 11 â€” MONITORING & DRIFT

## Ã‰tape 11.1 â€” Monitoring production

### Sous-Ã©tape 11.1.1 â€” Performance
- [ ] **Objectif :** surveiller la santÃ© du systÃ¨me.
- **Action :** suivre performance, drawdown, expectancy et stabilitÃ©.
- **Validation :** mÃ©triques disponibles rÃ©guliÃ¨rement.
- **GO / NO-GO :** GO.

### Sous-Ã©tape 11.1.2 â€” Data / regime / execution drift
- [ ] **Objectif :** dÃ©tecter les changements de comportement.
- **Action :** surveiller donnÃ©es, rÃ©gimes et coÃ»ts d'exÃ©cution.
- **Validation :** seuils d'alerte dÃ©finis.
- **GO / NO-GO :** GO.

---

# PHASE 12 â€” CHAMPION / CHALLENGER

## Ã‰tape 12.1 â€” DÃ©tection d'une dÃ©gradation

### Sous-Ã©tape 12.1.1 â€” DÃ©clencheur d'analyse
- [ ] **Objectif :** lancer une analyse sans rÃ©entraÃ®ner automatiquement.
- **Action :** dÃ©finir les conditions de dÃ©gradation significative.
- **Validation :** alerte gÃ©nÃ©rÃ©e sans modification de production.
- **GO / NO-GO :** GO.

## Ã‰tape 12.2 â€” Nouveau modÃ¨le

### Sous-Ã©tape 12.2.1 â€” Proposition Challenger
- [ ] **Objectif :** crÃ©er une hypothÃ¨se alternative contrÃ´lÃ©e.
- **Action :** dÃ©finir et documenter le challenger.
- **Validation :** challenger reproductible et isolÃ© du champion.
- **GO / NO-GO :** GO vers validation.

### Sous-Ã©tape 12.2.2 â€” Validation Challenger
- [ ] **Objectif :** empÃªcher une promotion basÃ©e sur une simple amÃ©lioration historique.
- **Action :** appliquer le protocole complet de validation.
- **Validation :** challenger supÃ©rieur selon les critÃ¨res dÃ©finis.
- **GO / NO-GO :** GO vers comparaison finale ou rejet.

## Ã‰tape 12.3 â€” Promotion

### Sous-Ã©tape 12.3.1 â€” Champion â†’ Challenger
- [ ] **Objectif :** promouvoir uniquement une amÃ©lioration dÃ©montrÃ©e.
- **Action :** comparer champion et challenger selon le protocole officiel.
- **Validation :** tous les critÃ¨res de promotion sont rÃ©unis.
- **GO / NO-GO :** GO = promotion ; NO-GO = champion conservÃ©.

---

# PHASE 13 â€” PRODUCTION

## Ã‰tape 13.1 â€” Mise en production

### Sous-Ã©tape 13.1.1 â€” Checklist production
- [ ] **Objectif :** vÃ©rifier que tout est prÃªt avant exposition rÃ©elle.
- **Action :** contrÃ´ler donnÃ©es, modÃ¨le, risque, exÃ©cution, monitoring et kill switch.
- **Validation :** checklist complÃ¨te.
- **GO / NO-GO :** GO uniquement si aucun point critique n'est ouvert.

### Sous-Ã©tape 13.1.2 â€” PremiÃ¨re pÃ©riode contrÃ´lÃ©e
- [ ] **Objectif :** observer le comportement rÃ©el sans supposer que le backtest suffit.
- **Action :** dÃ©marrer avec exposition contrÃ´lÃ©e et monitoring renforcÃ©.
- **Validation :** comportement conforme aux attentes.
- **GO / NO-GO :** GO vers fonctionnement normal ou retour en analyse.

---

# RÃˆGLE DE FIN DE SESSION

Ã€ la fin de chaque session :

```text
1. Identifier la phase actuelle.
2. Identifier l'Ã©tape et la sous-Ã©tape actuelle.
3. Cocher uniquement les actions rÃ©ellement terminÃ©es.
4. Documenter tout rÃ©sultat important.
5. DÃ©clarer GO / NO-GO.
6. Identifier UNE prochaine action prioritaire.
```

## Format de compte rendu

```text
PHASE : X
Ã‰TAPE : X.X
SOUS-Ã‰TAPE : X.X.X

FAIT :
- ...

RÃ‰SULTAT :
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

> **Comprendre â†’ mesurer â†’ comparer â†’ adapter â†’ contrÃ´ler â†’ valider â†’ produire.**

> **La complexitÃ© est une rÃ©compense de la preuve, jamais un point de dÃ©part.**

