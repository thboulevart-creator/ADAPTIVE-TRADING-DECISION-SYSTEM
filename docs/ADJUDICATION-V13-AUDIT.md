# 1.1.2 — V13 AUDIT ADJUDICATION

**Statut : DECISION EXPLICITE — POST-AUDIT V13**

**Audit :** `AUDIT-ADVERSARIAL-V13.md`, commit `f1bbdeff5eaa7590c44b3ad4bff00bffa37a6615`.

## V13-01 — Injectivité de l'identité

**Décision : ACCEPTÉ COMME PRÉCONDITION DE TEST, SANS CRÉER UNE NOUVELLE IDENTITÉ.**

Le couple `count + multiset(identity(...))` ne démontre pas à lui seul qu'une identité collisionnelle est impossible. Le test doit donc distinguer :

1. l'égalité exacte de correspondance ;
2. la propriété du mécanisme d'identité applicable garantissant qu'une même identité ne représente pas plusieurs observations primaires distinctes.

Cette seconde propriété appartient au mécanisme d'identité applicable en amont et ne doit pas être redéfinie dans `1.1.2`.

Tant que cette propriété n'est pas démontrée par le corpus ou par le contrat d'identité applicable, le Test R reste `BLOCKED` sur cette dimension.

**Statut normatif : [CONSÉQUENCE NÉCESSAIRE]**

## V13-02 — `event_time` / `availability_time`

**Décision : REPORTÉ / QUESTION NON RÉSOLUE.**

Aucune nouvelle sémantique temporelle n'est créée. V13 doit seulement empêcher qu'un test dépendant de cette distinction soit déclaré PASS par choix implicite.

**Statut normatif : [QUESTION NON RÉSOLUE]**

## V13-03 — Late ticks

**Décision : REPORTÉ / QUESTION NON RÉSOLUE.**

La formulation V13 ne doit pas choisir inclusion, exclusion, réouverture ou recalcul d'une barre close après arrivée tardive.

**Statut normatif : [QUESTION NON RÉSOLUE]**

## Résultat

Une correction minimale V14 est autorisée uniquement pour rendre le Test R explicitement conditionné à la propriété d'identité applicable, sans créer de mécanisme d'identité nouveau.

Aucune correction n'est autorisée sur :

```text
event_time / availability_time
late ticks
contradictions / cycles
```

**Verdict :**

```text
V13
→ BLOCKED
Correction minimale autorisée → V14 candidate
```
