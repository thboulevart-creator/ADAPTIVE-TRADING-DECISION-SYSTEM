# OPERATING PIPELINE RULE

## Statut
FROZEN — règle opérationnelle de travail

## Principe
Le travail du projet est organisé en blocs de contrôle séparés par des étapes intermédiaires automatisées autant que possible.

## Règle
Entre deux blocs de contrôle (audit externe, décision normative, validation ou enregistrement GitHub), les tâches répétitives et déterministes doivent être enchaînées automatiquement sans demander une validation humaine à chaque micro-étape.

Le pipeline doit privilégier :

```text
bloc de contrôle
    ↓
analyse / rapprochement automatique
    ↓
correction ou production déterministe
    ↓
contrôle de cohérence
    ↓
prochain bloc de contrôle
```

## Limite
L'automatisation ne doit jamais créer silencieusement une nouvelle décision normative.

Si le corpus, les registres et les décisions gelées permettent de déterminer l'action suivante, celle-ci est exécutée directement.

Si une véritable ambiguïté normative subsiste et que plusieurs décisions sont possibles sans autorité suffisante pour trancher, le flux s'arrête et la décision est explicitement soumise à adjudication humaine.

## Garde-fous
Les audits et autres blocs de contrôle restent les points de vérification de la chaîne. Toute erreur découverte à un bloc doit être retracée jusqu'à son origine et corrigée avant de poursuivre vers le bloc suivant.

## Objectif
Réduire l'intervention humaine sur les tâches mécaniques tout en augmentant la rigueur aux points de contrôle, éviter les arrêts inutiles et maintenir une traçabilité complète.
