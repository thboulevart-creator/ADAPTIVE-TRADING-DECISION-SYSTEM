# ARCHITECTURE DE SORTIE DE POSITION — SÉLECTEUR DE MODES

**Statut : PRINCIPE DE CONCEPTION À TESTER**

## Objectif

Éviter l'empilement de plusieurs mécanismes de sortie qui se déclenchent indépendamment et rendent les résultats difficiles à attribuer. La gestion de position doit être structurée comme une séquence d'états avec un moteur de sortie sélectionné explicitement.

## Séquence cible

> **OUVERTURE → ARMEMENT → BASCULEMENT → SORTIE**

### 1. OUVERTURE

La position est exécutée et entre dans son état initial de gestion.

### 2. ARMEMENT

Une condition ou un seuil prédéfini est atteint. Cette étape autorise ou active le mécanisme de protection/gestion suivant.

Le break-even peut notamment servir de mécanisme d'armement lorsqu'il est retenu. Il ne doit pas être considéré comme un quatrième moteur de sortie concurrent.

### 3. BASCULEMENT

Après l'armement, la gestion est transférée à **un seul moteur de sortie sélectionné**.

### 4. SORTIE

Le moteur actif clôture la position lorsque sa condition est atteinte.

## Sélecteur de sortie

Le futur EA doit permettre de sélectionner et de comparer séparément les trois modes suivants, à logique d'entrée et cadre de risque constants :

1. **TRAILING_POINTS** — trailing mécanique basé sur une distance en points.
2. **PARABOLIC_SAR** — sortie/trailing dynamique basé sur le Parabolic SAR (Stop And Reverse), avec ses paramètres Step et Maximum.
3. **MA_CROSS** — sortie déclenchée par le croisement inverse d'une moyenne mobile rapide et d'une moyenne mobile lente.

## Règle d'exclusivité

Les trois moteurs ne doivent **pas** être empilés simultanément comme des décideurs indépendants.

Pour une configuration donnée :

```text
EXIT_MODE = TRAILING_POINTS
OU
EXIT_MODE = PARABOLIC_SAR
OU
EXIT_MODE = MA_CROSS
```

Le code doit garantir qu'un seul moteur de sortie est actif après le basculement.

## Intérêt pour la recherche

Cette séparation permet de conserver la même logique d'entrée et le même cadre de risque, puis de comparer l'effet propre de chaque gestion de sortie sur :

- rendement ;
- Profit Factor ;
- expectancy ;
- drawdown ;
- durée des trades ;
- distribution des gains et pertes ;
- stabilité par année et par régime ;
- robustesse hors échantillon.

Aucune des trois méthodes ne doit être considérée comme supérieure avant validation empirique.

## Exigence future MT5

Lors de la construction réelle de l'EA dans MetaTrader 5, intégrer le sélecteur dans les **inputs/paramètres de l'Expert Advisor** et dans la logique d'exécution. Les trois modes doivent être sélectionnables sans modifier le code source, et l'implémentation doit garantir l'exclusivité du moteur actif.

Le développement devra également prévoir des tests séparés des trois modes afin de pouvoir attribuer les différences de performance à la gestion de sortie plutôt qu'à un mélange de mécanismes.

## Rappel de gouvernance

Ce document conserve une décision architecturale de travail. Elle ne constitue pas une preuve de rentabilité. Toute supériorité d'un mode devra être démontrée par des tests suffisamment longs, robustes et, lorsque pertinent, hors échantillon.
