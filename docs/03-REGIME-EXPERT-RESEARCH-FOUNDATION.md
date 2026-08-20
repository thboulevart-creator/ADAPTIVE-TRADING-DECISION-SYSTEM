# Fondation de recherche — Régimes, experts et validation

**Version :** 1.0  
**Date :** 20 août 2026  
**Statut :** Document fondateur de recherche V1

---

# 1. Pourquoi ce document existe

Ce document transforme la vision générale du système en un premier laboratoire de recherche volontairement simple.

L'objectif n'est pas de construire immédiatement une IA complexe.

L'objectif est de démontrer, avec des composants compréhensibles et mesurables, le mécanisme :

```text
MARCHÉ
  ↓
RÉGIME
  ↓
EXPERT ADAPTÉ
  ↓
SIGNAL
  ↓
RISQUE
  ↓
DÉCISION
```

Nous voulons savoir si cette logique apporte réellement quelque chose par rapport à une stratégie qui applique le même comportement partout.

> **Principe : aucune complexification sans preuve de valeur.**

---

# 2. Règle de travail : Pourquoi → Comment → Exemple → Test

Chaque composant du système doit être étudié avec quatre questions.

## Pourquoi ?

Quel problème cherche-t-il à résoudre ?

## Comment ?

Quel est son fonctionnement concret ?

## Exemple

Que ferait-il face à une situation réelle de marché ?

## Test

Comment vérifier objectivement qu'il apporte une amélioration ?

Cette structure doit rester notre méthode de compréhension tout au long du projet.

---

# 3. Le problème que nous cherchons à résoudre

Une stratégie peut être performante dans un environnement et mauvaise dans un autre.

Exemple imagé :

```text
MARCHÉ A
Tendance forte
     ↓
Momentum fonctionne bien

MARCHÉ B
Range
     ↓
Momentum peut se faire retourner plusieurs fois

MARCHÉ C
Compression → cassure
     ↓
Breakout devient plus pertinent
```

La question n'est donc pas seulement :

> « Quelle stratégie est la meilleure ? »

Mais :

> **« Quelle stratégie est la plus adaptée au contexte actuel ? »**

---

# 4. Le moteur de régime V1

## Pourquoi ?

Le moteur de régime sert à décrire l'environnement du marché avant de choisir un expert.

Il ne cherche pas à prédire le prix.

Il cherche à répondre à :

> **« Dans quel type d'environnement sommes-nous actuellement ? »**

## Régimes V1

Nous commençons volontairement avec quatre catégories :

```text
TENDANCE
RANGE
BREAKOUT
STRESS
```

Une catégorie supplémentaire de transition pourra être utilisée plus tard si les tests montrent qu'elle est nécessaire.

---

# 5. ADX et ATR : pourquoi commencer simplement

## ADX

L'ADX peut servir d'information sur la force directionnelle du marché.

Il ne doit pas être interprété comme une prédiction automatique de hausse ou de baisse.

Exemple :

```text
ADX faible
   ↓
faible force directionnelle
   ↓
contexte potentiellement plus proche d'un range
```

ou :

```text
ADX élevé
   ↓
force directionnelle élevée
   ↓
contexte potentiellement plus favorable aux stratégies de tendance
```

## ATR

L'ATR sert à mesurer l'amplitude/volatilité récente.

Exemple :

```text
ATR faible → marché comprimé
ATR en forte hausse → expansion de volatilité
ATR très élevé → conditions potentiellement stressées
```

## Pourquoi ces deux outils ?

Parce qu'ils sont :

- simples ;
- explicables ;
- faciles à calculer ;
- faciles à tester ;
- suffisamment différents pour fournir une première description du marché.

Ils ne sont pas considérés comme « la meilleure combinaison possible ».

Ils sont notre **point de départ minimal**.

---

# 6. Détecteur de régime V1 — logique conceptuelle

La logique exacte devra être calibrée sur les données, mais l'idée générale est :

```text
                 MARCHÉ
                    ↓
              ADX + ATR
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
     direction   volatilité   expansion
        ↓           ↓           ↓
        └───────────┼───────────┘
                    ↓
                  RÉGIME
```

Exemple conceptuel :

```text
ADX élevé
+ volatilité normale/élevée
+ structure directionnelle
        ↓
TENDANCE
```

```text
ADX faible
+ volatilité faible
+ absence de direction claire
        ↓
RANGE
```

```text
Compression
+ expansion rapide de volatilité
+ sortie d'une zone
        ↓
BREAKOUT
```

```text
Volatilité extrêmement élevée
+ conditions d'exécution dégradées
        ↓
STRESS
```

Ces règles ne sont pas des vérités définitives. Elles constituent des hypothèses à tester.

---

# 7. Exemple imagé — NAS100

Imaginons le NAS100 à 15h30.

Le système observe :

```text
ADX élevé
ATR en hausse
structure de prix directionnelle
```

Il produit :

```text
RÉGIME = TENDANCE
```

Il ne produit pas encore :

```text
BUY NAS100
```

Le régime ne fait que décrire l'environnement.

La décision vient ensuite des experts, du risque, du portefeuille et de l'exécution.

---

# 8. Pourquoi comparer des experts simples

Nous voulons tester trois comportements élémentaires :

```text
1. Momentum / Tendance
2. Breakout
3. Mean Reversion
```

Le but n'est pas de construire trois stratégies sophistiquées.

Le but est de vérifier une hypothèse fondamentale :

> **Les performances relatives des experts changent-elles réellement selon le régime ?**

Si la réponse est non, le routage par régime perd une grande partie de son intérêt.

---

# 9. Expert Momentum / Tendance

## Pourquoi ?

Il cherche à exploiter la continuation d'un mouvement.

## Comment ?

La définition V1 doit rester simple et déterministe.

Elle peut par exemple utiliser une mesure de direction ou de momentum sur un horizon défini.

La formule exacte est une hypothèse de recherche, pas une décision permanente.

## Exemple

```text
NAS100

Prix monte
Momentum positif
Contexte TENDANCE

        ↓
Momentum autorisé
```

## Test

Comparer sa performance :

```text
Momentum sans filtre de régime
        VS
Momentum uniquement dans les régimes favorables
```

---

# 10. Expert Breakout

## Pourquoi ?

Il cherche à exploiter une sortie d'une zone de compression ou d'une structure définie.

## Comment ?

Une définition V1 peut partir d'une cassure d'un niveau/range historique avec confirmation minimale.

## Exemple

```text
Prix enfermé dans un range
        ↓
Compression
        ↓
Cassure
        ↓
Breakout
```

## Test

Mesurer la performance du Breakout selon :

- régime ;
- volatilité ;
- session ;
- horizon ;
- coûts.

---

# 11. Expert Mean Reversion

## Pourquoi ?

Il cherche à exploiter les situations où le prix revient vers une référence après un éloignement significatif.

## Comment ?

La définition V1 doit rester simple : identifier un éloignement puis tester statistiquement la fréquence et l'amplitude du retour.

## Exemple

```text
RANGE

Prix → extrême haut
        ↓
Éloignement
        ↓
Retour vers la moyenne
```

## Test

Comparer notamment son comportement :

- en range ;
- en tendance ;
- en stress ;
- pendant les expansions de volatilité.

---

# 12. Comparateur d'experts

Le comparateur est l'un des premiers outils de recherche du projet.

Il doit permettre de produire une matrice du type :

| Régime | Momentum | Breakout | Mean Reversion |
|---|---:|---:|---:|
| Tendance | résultat | résultat | résultat |
| Range | résultat | résultat | résultat |
| Breakout | résultat | résultat | résultat |
| Stress | résultat | résultat | résultat |

Les résultats doivent être calculés, jamais supposés.

---

# 13. Ce que nous voulons découvrir

Nous cherchons une relation du type :

```text
RÉGIME
   ↓
EXPERT
   ↓
PERFORMANCE CONDITIONNELLE
```

Par exemple, si les données montrent :

```text
Tendance → Momentum supérieur
Range → Mean Reversion supérieure
Breakout → Breakout supérieur
```

alors l'idée d'un routeur devient intéressante.

Mais si les résultats sont aléatoires ou instables :

> **nous devons l'accepter et ne pas forcer la théorie.**

---

# 14. Le routeur V1

## Pourquoi ?

Le routeur transforme le contexte en sélection ou pondération d'experts.

## Comment ?

V1 doit être **déterministe et explicable**.

Exemple conceptuel :

```text
SI TENDANCE
    Momentum prioritaire

SI BREAKOUT
    Breakout prioritaire

SI RANGE
    Mean Reversion prioritaire

SI STRESS
    exposition réduite ou aucun trade
```

Il peut évoluer plus tard vers des pondérations.

---

# 15. Exemple de routage

Imaginons :

```text
NAS100
Régime = TENDANCE
```

Le routeur peut produire :

```text
Momentum       → prioritaire
Breakout       → secondaire
Mean Reversion → faible / désactivé
```

Puis :

```text
Gold
Régime = RANGE
```

Le routeur peut produire :

```text
Mean Reversion → prioritaire
Momentum       → faible
Breakout       → faible
```

Encore une fois : ces priorités sont des hypothèses à valider.

---

# 16. Pourquoi Python d'abord

Python constitue notre environnement de recherche.

Il permet de :

- charger les données ;
- calculer les variables ;
- détecter les régimes ;
- tester les experts ;
- comparer les résultats ;
- réaliser les walk-forward ;
- analyser les biais ;
- produire les rapports.

L'objectif n'est pas de faire de Python un système de production complet dès le départ.

---

# 17. Rôle de MetaTrader 5

MetaTrader 5 intervient ensuite pour la validation de l'implémentation et l'exécution dans un environnement de trading réel/simulé.

Le principe est :

```text
Python
Recherche / analyse / validation
        ↓
Spécification claire
        ↓
MQL5 / MT5
Implémentation / exécution / test
```

Il faut éviter de faire évoluer simultanément la logique de recherche et le code d'exécution sans traçabilité.

---

# 18. GARCH : pourquoi ne pas le mettre au centre de V1

GARCH peut être intéressant pour modéliser la volatilité conditionnelle.

Mais nous avons déjà une mesure simple :

```text
ATR
+
volatilité réalisée
```

La bonne question est donc :

> **GARCH apporte-t-il une amélioration robuste par rapport à une mesure de volatilité simple ?**

Pas :

> « GARCH est plus sophistiqué, donc il doit être meilleur. »

Architecture de recherche :

```text
V1
ATR / volatilité réalisée
        ↓
BASELINE
        ↓
V2
GARCH
        ↓
COMPARAISON
        ↓
Valeur démontrée ?
   ↙             ↘
 OUI             NON
  ↓               ↓
Conserver       Retirer
```

---

# 19. Walk-Forward

## Pourquoi ?

Un backtest unique peut donner une illusion de robustesse.

Le Walk-Forward cherche à reproduire le processus de recherche dans le temps.

Conceptuellement :

```text
TRAIN → TEST
   ↓
   déplacement
   ↓
TRAIN → TEST
   ↓
   déplacement
   ↓
TRAIN → TEST
```

Les périodes doivent respecter la chronologie.

---

# 20. Exemple Walk-Forward

Exemple simplifié :

```text
2018 ───── 2021
     TRAIN

2022 ───── TEST
```

Puis :

```text
2019 ───── 2022
     TRAIN

2023 ───── TEST
```

Puis :

```text
2020 ───── 2023
     TRAIN

2024 ───── TEST
```

Et ainsi de suite.

Les paramètres exacts dépendront de la quantité et de la nature des données.

---

# 21. Biais critiques à éviter

## Look-ahead bias

Utiliser une information qui n'était pas disponible au moment de la décision.

### Exemple

Utiliser le high ou low de la journée entière pour prendre une décision à 10h.

Impossible : le futur n'était pas encore connu.

---

## Data leakage

Une information du futur se retrouve indirectement dans l'apprentissage ou les variables.

### Exemple

Normaliser toutes les données avec une moyenne calculée sur 2018–2026 avant de tester 2025.

La période future a contaminé l'information disponible dans le passé.

---

## Overfitting

Adapter trop précisément les paramètres à l'historique.

### Exemple

Tester 2 000 combinaisons puis choisir celle qui donne le meilleur résultat historique.

Le meilleur résultat peut simplement être le produit du hasard.

---

## Data snooping

Tester suffisamment d'hypothèses jusqu'à trouver une relation apparemment rentable.

### Exemple

Tester :

```text
20 indicateurs
×
15 périodes
×
10 actifs
×
8 horizons
```

Puis conserver uniquement la combinaison gagnante.

---

## Survivorship bias

Tester uniquement les actifs qui existent encore ou qui ont survécu à une période historique.

Cela peut embellir les résultats.

---

## Selection bias

Choisir les actifs ou périodes après avoir vu les résultats.

### Exemple

Tester 30 actifs puis ne présenter que les 5 meilleurs comme univers initial.

Le processus de sélection doit être défini avant l'évaluation finale.

---

## Optimisation de l'OOS

Une période hors échantillon cesse d'être réellement hors échantillon si elle est utilisée pour modifier le modèle puis réévaluée comme preuve indépendante.

### Règle

```text
OOS observé
    ↓
Modification du modèle
    ↓
Cette période n'est plus une validation indépendante
```

---

# 22. Coûts et réalisme

Toutes les comparaisons doivent intégrer autant que possible :

- spread ;
- commission ;
- slippage ;
- financement ;
- contraintes horaires ;
- règles d'exécution.

Exemple :

```text
Alpha brut        +0,18 %
Spread             0,06 %
Commission         0,03 %
Slippage           0,05 %
------------------------
Résultat net       +0,04 %
```

Une stratégie peut donc être intéressante statistiquement mais peu intéressante économiquement.

---

# 23. Le baseline est obligatoire

Avant d'ajouter un routeur, nous devons connaître la performance des stratégies sans adaptation.

Nous devons donc comparer au minimum :

```text
BASELINE
Expert appliqué partout

VS

ADAPTATIF
Expert sélectionné selon le régime
```

Sans baseline, nous ne savons pas si le moteur de régime apporte réellement quelque chose.

---

# 24. Test minimal de la valeur du régime

Le test fondamental est :

```text
Stratégie simple
       ↓
Performance globale

VS

Même stratégie
       ↓
Filtre / routage par régime
       ↓
Performance conditionnelle
```

Nous devons regarder :

- rendement ;
- expectancy ;
- drawdown ;
- stabilité ;
- nombre de trades ;
- coûts ;
- performance par période ;
- performance par régime.

---

# 25. Ne pas confondre précision et valeur économique

Un détecteur de régime peut avoir une classification imparfaite et néanmoins améliorer la décision.

Inversement, un détecteur de régime très précis peut ne rien apporter au portefeuille.

La métrique finale n'est donc pas :

> « Le régime est-il prédit correctement ? »

mais :

> **« Le fait de connaître ce régime améliore-t-il une décision de trading nette des coûts et du risque ? »**

---

# 26. Stress : cas particulier

Le régime STRESS doit être traité différemment des autres.

Il peut ne pas servir à choisir un expert.

Il peut servir à dire :

```text
STRESS
 ↓
réduire le risque
ou
ne pas trader
```

Exemple :

```text
Volatilité extrême
+
Spread inhabituel
+
Slippage élevé

        ↓

STRESS
        ↓

TRADING REDUIT / HALT
```

Cela relie directement le moteur de régime au Risk & Safety Framework.

---

# 27. Ce que nous ne ferons pas en V1

Nous n'allons pas commencer par :

- réseau neuronal complexe ;
- Mixture of Experts appris ;
- GARCH partout ;
- centaines de features ;
- optimisation massive ;
- routeur auto-apprenant ;
- réentraînement automatique ;
- modèle qui modifie ses règles en production.

Nous devons d'abord démontrer le mécanisme avec une architecture lisible.

---

# 28. Évolution possible après validation

Seulement si les résultats le justifient :

```text
V1
Régime simple
+
3 experts
+
routeur à règles

        ↓

V2
Volatilité avancée / GARCH

        ↓

V3
Routeur pondéré

        ↓

V4
Routeur appris

        ↓

V5
Architecture multi-actifs / experts avancés
```

Chaque étape doit être comparée à la précédente.

Une version plus complexe qui n'améliore pas robustement la précédente doit être rejetée.

---

# 29. Ordre de recherche recommandé

```text
1. Vérifier les données
        ↓
2. Construire les baselines
        ↓
3. Définir le détecteur de régime V1
        ↓
4. Tester la stabilité des régimes
        ↓
5. Construire Momentum
        ↓
6. Construire Breakout
        ↓
7. Construire Mean Reversion
        ↓
8. Comparer les experts par régime
        ↓
9. Construire le routeur simple
        ↓
10. Comparer routeur vs baseline
        ↓
11. Ajouter coûts réalistes
        ↓
12. Walk-Forward
        ↓
13. Stress tests / robustesse
        ↓
14. Seulement ensuite envisager GARCH ou davantage de complexité
```

---

# 30. Critère de réussite V1

V1 n'a pas besoin d'être une machine à rendement maximal.

Elle doit démontrer que nous pouvons :

1. identifier un contexte de marché de manière reproductible ;
2. mesurer les performances des experts dans ce contexte ;
3. router les experts de manière explicable ;
4. comparer le système adaptatif à une baseline ;
5. intégrer les coûts ;
6. réaliser un Walk-Forward propre ;
7. mesurer la robustesse ;
8. comprendre pourquoi le système gagne ou perd.

Si ces huit points sont maîtrisés, nous aurons un véritable socle pour la suite.

---

# 31. Règle d'or du laboratoire

> **Nous ne cherchons jamais à prouver que notre idée est bonne. Nous cherchons à savoir si les données nous donnent une raison suffisante de la conserver.**

Cela signifie :

```text
Hypothèse
   ↓
Test
   ↓
Résultat
   ↓
Interprétation
   ↓
Décision
```

et non :

```text
Idée
 ↓
Optimisation jusqu'à obtenir un beau backtest
 ↓
Confirmation
```

---

# 32. Position de ce document dans le projet

Ce document se situe entre la vision du système et les futures spécifications techniques.

```text
01 SYSTEM VISION
       ↓
02 ASSET PROFILE DATABASE
       ↓
03 REGIME / EXPERT RESEARCH FOUNDATION
       ↓
FUTURS DOCUMENTS
       ↓
PLAN D'ACTION
       ↓
IMPLÉMENTATION
```

Il constitue notre **carte de recherche V1**.

Il ne remplace pas les futurs documents spécialisés sur les données, le risque, le contrat de décision, la validation, le monitoring ou le registre des modèles.

---

# 33. Conclusion

Notre première ambition n'est pas de créer une intelligence artificielle impressionnante.

Notre première ambition est beaucoup plus simple :

> **Construire un système dont nous comprenons chaque étape et démontrer progressivement que chaque couche ajoute réellement de la valeur.**

Le chemin commence par :

```text
RÉGIME
 ↓
EXPERT
 ↓
ROUTAGE
 ↓
RISQUE
 ↓
DÉCISION
 ↓
MESURE
 ↓
VALIDATION
```

Puis seulement, si nécessaire :

```text
COMPLEXIFICATION
```

**La complexité est une récompense de la preuve, jamais un point de départ.**
