# Diff logique proposé — `00-MASTER-EXECUTION-CHECKLIST.md`

**Version :** 0.1 — PROPOSITION, non appliquée
**Date :** 20 août 2026
**Statut :** aucune modification n'a été effectuée sur le dépôt

> Ce document décrit **ce qui serait modifié** si la proposition était validée. Il ne modifie rien.
> Chaque changement est isolé, numéroté, et peut être accepté ou rejeté indépendamment des autres.

---

## Récapitulatif

| # | Nature | Portée | Dépend de |
|---|---|---|---|
| **D1** | Correction technique | Encodage du fichier | — |
| **D2** | Ajout de phase | Nouvelle phase 1.2 — contrat de données | `05` validé |
| **D3** | Ajout d'étape | Cadrage de recherche en phase 0 | `04` validé |
| **D4** | Déplacement | Phase 9.2 déplacée après la phase 10 | — |
| **D5** | Ajout de branche | Sortie NO-GO en phase 4.3.2 | — |
| **D6** | Ajout d'étape | Registre de consommation d'échantillon | `04` validé |
| **D7** | Clarification | Modèle de coûts unifié | `05` validé |
| **D8** | Arbitrage requis | Multi-horizon : intégré ou hors V1 | décision |
| **D9** | Clarification | Régime STRESS vs kill switch | décision |

---

# D1 — Correction de l'encodage

## Constaté

Le fichier porte un BOM UTF-8 et présente un double encodage sur l'ensemble des caractères accentués.

```
Lu actuellement : # PHASE 1 â€" DONNÃ‰ES
                  ### Ã‰tape 0.1.1 â€" DÃ©finir le systÃ¨me
Attendu         : # PHASE 1 — DONNÉES
                  ### Étape 0.1.1 — Définir le système
```

Les documents `01`, `02` et `03` ne présentent pas ce défaut.

## Proposé

Réenregistrer le fichier en UTF-8 sans BOM, contenu inchangé.

## Justification

Le document de pilotage doit être lisible. Le défaut provient vraisemblablement d'un enregistrement
via Bloc-notes ou PowerShell avec un encodage par défaut.

## Impact

Aucun sur le fond. Purement technique.

## Statut

**Correction technique — ne relève pas d'un arbitrage méthodologique.**

---

# D2 — Nouvelle étape 1.2 : contrat de données

## Constaté

La phase 1 comporte trois sous-étapes : inventaire, contrôle qualité, intégrité temporelle. Elle
valide un jeu de données **à l'entrée du projet**.

Aucune règle ne se redéclenche lorsqu'un jeu validé est ensuite transformé — extrait, filtré, agrégé,
converti. La validation initiale se transmet implicitement par héritage.

## Proposé

Ajouter une étape 1.2 après le contrôle qualité existant.

```
## Étape 1.2 — Contrat de données

### Sous-étape 1.2.1 — Contrôle de continuité
- [ ] Objectif : garantir qu'aucun moteur ne parcourt par index une série discontinue.
- Action : produire le verdict de continuité (05 §1.2) pour chaque jeu.
- Validation : verdict SÉRIE CONTINUE, ou moteur parcourant par horodatage.
- GO / NO-GO : NO-GO tant qu'un jeu discontinu est parcouru par index.

### Sous-étape 1.2.2 — Rapport de couverture
- [ ] Objectif : rendre tout résultat interprétable.
- Action : produire le rapport de couverture (05 §2.2), vérifié sur le contenu (05 §2.3).
- Validation : rapport joint à chaque jeu.
- GO / NO-GO : GO si aucun mois anormal non expliqué.

### Sous-étape 1.2.3 — Déclaration des jeux transformés
- [ ] Objectif : empêcher qu'une limite d'usage se perde en cours de projet.
- Action : pour chaque transformation, produire identifiant, rapport de couverture
  et déclaration de limites d'usage (05 §3.2).
- Validation : chaîne de traçabilité reconstituable de la source brute au jeu utilisé.
- GO / NO-GO : NO-GO si un jeu est employé sans déclaration.

### Sous-étape 1.2.4 — Outillage du contrôle
- [ ] Objectif : rendre le contrôle systématique plutôt que déclaratif.
- Action : implémenter un outil réutilisable produisant les contrôles 8.2 du document 05.
- Validation : outil exécutable, sortie reproductible.
- GO / NO-GO : GO.
```

## Justification

Le rapport v3 de Sweep + MSS annonçait un SQN hors échantillon de 2,50. Sur données continues il
vaut 0,27. Le jeu de recherche était un extrait par fenêtres dont la limite d'usage n'avait jamais été
écrite. **47 % des transactions traversaient une discontinuité artificielle.**

Le contrôle qualité de la phase 1 actuelle **n'aurait pas détecté cet artefact**, puisque le jeu source
était valide et que la transformation est intervenue plus tard.

## Impact

Ajoute une condition NO-GO bloquante avant toute recherche. Allonge la phase 1.

## Statut

**PROPOSÉ — conditionné à la validation du document `05`.**

---

# D3 — Nouvelle étape 0.2 : cadrage de recherche

## Constaté

La phase 0 fige le périmètre, les exclusions et la gouvernance. Elle ne fige **aucun critère de
décision**.

La phase 12.3.1 conclut : « tous les critères de promotion sont réunis ». Ces critères ne sont définis
dans aucun document du dépôt.

## Proposé

Ajouter une étape 0.2, à exécuter avant toute recherche sur un actif donné.

```
## Étape 0.2 — Cadrage de la recherche

### Sous-étape 0.2.1 — Effet minimal et taille d'échantillon
- [ ] Objectif : savoir avant de commencer si l'échantillon peut porter une conclusion.
- Action : fixer d visé (04 §1.2), calculer n_min (04 §1.1), vérifier la disponibilité.
- Validation : n_min ≤ échantillon disponible.
- GO / NO-GO : NO-GO si n_min dépasse l'échantillon — la piste est écartée au cadrage.

### Sous-étape 0.2.2 — Budget d'hypothèses
- [ ] Objectif : rendre la correction pour tests multiples calculable.
- Action : déclarer N, la méthode de correction (04 §2.3) et le seuil corrigé.
- Validation : budget écrit et daté avant le premier calcul.
- GO / NO-GO : GO.

### Sous-étape 0.2.3 — Frontières temporelles
- [ ] Objectif : empêcher le redécoupage opportuniste.
- Action : inscrire les dates exactes train / validation / OOS (04 §3.1).
- Validation : dates gelées, justification indépendante des résultats.
- GO / NO-GO : GO.

### Sous-étape 0.2.4 — Critères de promotion et d'abandon
- [ ] Objectif : définir la conclusion avant de connaître le résultat.
- Action : instancier les sept conditions du 04 §5.1 et les conditions d'abandon du 04 §6.2.
- Validation : critères écrits, valeurs des paramètres arbitrées.
- GO / NO-GO : NO-GO tant que les paramètres du 04 §8 ne sont pas arbitrés.
```

## Justification

Sur Sweep + MSS, aucun de ces quatre éléments n'existait. Conséquences mesurées :

- l'effet réel exigeait plus de 12 000 transactions ; la validation en comptait 230 ;
- 7 400 combinaisons ont été évaluées sans budget déclaré ;
- une frontière temporelle a été déplacée en cours de projet sans traçabilité ;
- trois conditions d'abandon étaient réunies dès le rapport v2 sans qu'aucune ne soit formulée.

## Impact

Introduit une condition NO-GO au cadrage susceptible d'écarter une piste **avant tout backtest**.
C'est l'effet recherché.

## Statut

**PROPOSÉ — conditionné à la validation du document `04` et à l'arbitrage de ses paramètres ouverts.**

---

# D4 — Déplacement de l'étape 9.2 après la phase 10

## Constaté

Ordre actuel :

```
PHASE 9  — EXÉCUTION
  9.1 Modèle de coûts
  9.2 Python → MT5        ← spécification et validation MT5
PHASE 10 — VALIDATION WALK-FORWARD
  10.1 Protocole temporel
  10.2 Audit des biais
  10.3 Robustesse
```

L'implémentation MT5 précède donc la démonstration de robustesse temporelle et l'audit des biais.

## Proposé

Ordre modifié :

```
PHASE 9  — COÛTS D'EXÉCUTION
  9.1 Modèle de coûts

PHASE 10 — VALIDATION WALK-FORWARD
  10.1 Protocole temporel
  10.2 Audit des biais
  10.3 Robustesse

PHASE 10bis — IMPLÉMENTATION MT5          ← anciennement 9.2
  10bis.1 Spécification figée
  10bis.2 Parité fonctionnelle avec la référence
  GO / NO-GO : NO-GO tant que la phase 10 n'est pas validée.
```

## Justification

Sur Sweep + MSS, une spécification d'implémentation MQL5 a été rédigée pour une stratégie dont la
validation reposait sur des données corrompues. Un audit technique de cette spécification avait été
engagé avant que l'invalidation ne soit découverte.

Coder une implémentation avant d'avoir démontré la robustesse revient à investir dans un objet dont
la valeur n'est pas établie.

## Impact

Aucune perte de contenu. La numérotation de la phase change.

**Variante possible :** conserver la numérotation actuelle et ajouter une condition d'entrée à la
sous-étape 9.2.1 — « NO-GO tant que la phase 10 n'est pas validée ». Moins clair structurellement,
mais sans renumérotation.

## Statut

**PROPOSÉ — arbitrage requis sur la forme : déplacement ou condition d'entrée.**

---

# D5 — Branche NO-GO en phase 4.3.2

## Constaté

```
### Sous-étape 4.3.2 — Valeur informative
- GO / NO-GO : GO si information utile démontrée.
```

Aucune suite n'est prévue en cas de NO-GO. Or le document `03` §13 énonce explicitement : « si les
résultats sont aléatoires ou instables, nous devons l'accepter et ne pas forcer la théorie ».

## Proposé

Expliciter la branche :

```
- GO / NO-GO :
    GO    → poursuite vers la phase 5.
    NO-GO → les régimes ne discriminent pas. Deux voies seulement :
            (a) redéfinir la taxonomie des régimes, en comptabilisant
                cette redéfinition dans le budget d'hypothèses (04 §2.4) ;
            (b) abandonner la couche régime et conserver les experts
                inconditionnels comme système de référence.
            Aucune autre voie n'est recevable.
```

## Justification

Sans branche explicite, un NO-GO en phase 4 conduit en pratique à ajuster la définition des régimes
jusqu'à obtenir un GO — sans que ces ajustements soient comptés comme des hypothèses testées.

C'est le mécanisme exact qui a produit les 7 400 combinaisons de Sweep + MSS.

## Impact

Rend le NO-GO praticable et comptabilise ses conséquences.

## Statut

**PROPOSÉ.**

---

# D6 — Registre de consommation d'échantillon

## Constaté

Aucune étape ne trace les lectures des périodes hors échantillon. Rien n'empêche de relire une période
déjà consultée.

## Proposé

Ajouter une sous-étape en phase 10.

```
### Sous-étape 10.1.3 — Registre de consommation
- [ ] Objectif : empêcher qu'une période hors échantillon serve deux fois de juge.
- Action : tenir le registre défini au 04 §4.2 pour chaque actif.
- Validation : registre à jour avant et après chaque lecture.
- GO / NO-GO : NO-GO si la période de validation est marquée CONSOMMÉE.
```

## Justification

Sur Sweep + MSS, la période 2024-2026 a été lue trois fois. Dès la deuxième lecture, aucun juge
indépendant n'existait plus, ce qui n'a été constaté qu'après coup.

## Impact

Peut bloquer une validation et contraindre à l'attente de données futures. C'est l'effet recherché.

## Statut

**PROPOSÉ — conditionné à la validation du document `04`.**

---

# D7 — Modèle de coûts unifié

## Constaté

Les coûts apparaissent en trois endroits sans modèle commun imposé :

```
6.1.2 — intégrer spread, commission et slippage
9.1.1 — spread, commission, slippage, financement et contraintes horaires
10.3.1 — varier raisonnablement coûts, paramètres, périodes et actifs
```

Rien n'empêche que ces trois usages emploient des modèles différents.

## Proposé

Faire référencer par les trois sous-étapes le modèle unique défini au document `05` §7, lui-même
instancié dans l'Asset Profile de chaque instrument.

## Justification

Sur Sweep + MSS, le stop avait été converti en pourcentage du prix pour corriger le biais lié à la
hausse de l'instrument. **Le spread est resté figé à 1,4 point** sur une période où le prix a
quadruplé. L'incohérence n'a jamais été résolue.

## Impact

Aucune modification structurelle. Ajout de références croisées.

## Statut

**PROPOSÉ — conditionné à la validation du document `05`.**

---

# D8 — Multi-horizon : arbitrage requis

## Constaté

Le document `01` présente l'analyse multi-horizon comme une couche majeure de l'architecture, avec un
exemple détaillé sur trois échelles — 15 minutes, 1 heure, 4 heures.

**Cette couche n'apparaît dans aucune phase du document `00`.**

## Proposé

Deux options, à arbitrer.

**Option A — intégrer.** Ajouter une étape en phase 5 ou 7 traitant l'agrégation multi-horizon et sa
contribution mesurable.

**Option B — déclarer hors V1.** Ajouter le multi-horizon à la liste des exclusions de la sous-étape
0.1.2, et une note au document `01` renvoyant à V2.

## Justification

Une couche présente dans la vision mais absente du plan d'exécution finit soit oubliée, soit ajoutée
sans cadrage. Les deux issues sont mauvaises.

## Impact

Option A : allonge V1.
Option B : réduit le périmètre et clarifie la vision.

## Statut

**ARBITRAGE REQUIS — je ne recommande pas d'option, le choix relève du périmètre V1.**

---

# D9 — Régime STRESS et kill switch

## Constaté

Le terme « stress » désigne deux objets distincts :

```
Document 03 §26  : STRESS comme régime de marché, au même titre que
                   TENDANCE, RANGE, BREAKOUT
Phase 8.1.2      : conditions de HALT du système
Phase 7.1.2      : « protéger le capital plutôt que forcer un trade »
```

La relation entre le régime STRESS et les conditions de HALT n'est établie nulle part.

## Proposé

Clarifier la distinction dans le document `00`, par exemple :

```
STRESS (régime de marché)     → détecté par le Context Engine.
                                Conséquence : le routeur réduit l'exposition
                                ou refuse le trade (7.1.2).
                                Le système continue de fonctionner.

HALT (état du système)        → déclenché par le Risk Engine sur conditions
                                définies en 8.1.2.
                                Conséquence : arrêt de toute prise de position.
                                Le système cesse de fonctionner.
```

## Justification

Un même terme désignant deux mécanismes de gravité différente produit des malentendus au moment
précis où la clarté importe le plus.

## Impact

Purement clarificateur.

## Statut

**PROPOSÉ — arbitrage requis sur la formulation retenue.**

---

# Dépendances entre changements

```
D1  indépendant — applicable immédiatement

D4  indépendant — ne dépend d'aucun document
D5  indépendant
D8  indépendant — arbitrage de périmètre
D9  indépendant — clarification

D2  ← document 05 validé
D7  ← document 05 validé

D3  ← document 04 validé ET paramètres du 04 §8 arbitrés
D6  ← document 04 validé
```

**Quatre changements sont applicables sans dépendance : D1, D4, D5, D9.**
**Deux exigent un arbitrage de fond : D8, et la forme de D4.**
**Trois sont conditionnés à la validation des documents 04 et 05 : D2, D3, D6, D7.**

---

# Ce que ce diff ne propose pas

- aucune suppression de phase, d'étape ou de sous-étape existante ;
- aucune modification du contenu des documents `01`, `02` et `03` ;
- aucune valeur numérique de décision ;
- aucun changement de la doctrine ou de la boussole du projet.

---

# Journal des versions

| Version | Date | Statut | Changement |
|---|---|---|---|
| 0.1 | 20/08/2026 | PROPOSITION | Rédaction initiale, aucune modification appliquée |
