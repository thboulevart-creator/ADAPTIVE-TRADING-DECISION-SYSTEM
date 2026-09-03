# 1.1.2 — V12 AUDIT ADJUDICATION

**Statut : DECISION EXPLICITE — POST-AUDIT V12**

**Base auditée :** V12 candidate `d489f6eeefaf8863b9d0fef497f7235ee7537765`.

**Audit :** `AUDIT-ADVERSARIAL-V12.md`, commit `9e0fd4c33b4783bc061697f9f7bb7387c7c73576`.

## 1. V12-01 — Identité nécessaire au Test R

**Décision : ACCEPTÉ COMME BLOCAGE DE DÉPENDANCE, PAS COMME NOUVELLE ARCHITECTURE.**

Le Test R ne peut être déclaré conforme que si le mécanisme d'identité applicable en amont permet effectivement d'établir la correspondance individuelle requise par V12.

Aucune identité locale ou nouvelle règle d'identité ne doit être inventée dans `1.1.2`.

Si l'identité applicable ne permet pas une comparaison déterministe, le point reste `QUESTION NON RÉSOLUE` et bloque le PASS/CLOSED/FROZEN lorsqu'il est nécessaire à la conformité de `1.1.2`, conformément à la règle déjà adoptée en V12.

**Statut normatif : [CONSÉQUENCE NÉCESSAIRE]**

## 2. V12-02 — Continuité BAR_IN_PROGRESS → BAR_CLOSED et late ticks

**Décision : ACCEPTÉ COMME AMBIGUÏTÉ À ÉLIMINER, SANS ADJUDICER LA POLITIQUE DES LATE TICKS.**

La formulation V12 ne doit pas être interprétée comme une décision implicite sur l'inclusion, l'exclusion ou la réouverture d'une `BAR_CLOSED` lorsqu'une observation tardive est reçue.

La continuité d'univers entre `BAR_IN_PROGRESS` et `BAR_CLOSED` reste obligatoire, mais son application aux observations dont le traitement temporel est encore non adjudiqué doit rester subordonnée à la politique applicable lorsqu'elle sera explicitement décidée.

Aucune règle supplémentaire sur les late ticks n'est créée par cette adjudication.

**Statut normatif : [CONSÉQUENCE NÉCESSAIRE]**

## 3. V12-03 — Régime temporel du Test V

**Décision : ACCEPTÉ COMME DÉPENDANCE REPORTÉE, SANS RÉSOUDRE event_time / availability_time.**

Le Test V ne peut pas utiliser l'expression « régime temporel applicable » comme prétexte pour choisir implicitement une sémantique `event_time` / `availability_time`.

Tant que V11-06 reste `QUESTION NON RÉSOLUE`, toute partie du Test V dépendant de cette distinction reste non adjudicée et ne peut pas être déclarée PASS sur cette dimension.

Aucune décision temporelle nouvelle n'est créée dans `1.1.2`.

**Statut normatif : [QUESTION NON RÉSOLUE]**

## 4. V12-04 — Branche Git

**Décision : NON NORMATIF / GOUVERNANCE.**

La branche dédiée `1.1.2-v12-audit` a été créée depuis le commit V12 `d489f6eeefaf8863b9d0fef497f7235ee7537765`.

La branche `1.1.2-v12-adjudication` est créée depuis le commit contenant l'audit V12 `9e0fd4c33b4783bc061697f9f7bb7387c7c73576`.

Cette correction de workflow ne modifie aucune exigence du contrat et ne doit pas être présentée comme une correction normative.

**Statut normatif : [ARCHITECTURE PROPOSÉE / GOUVERNANCE]**

## 5. Résultat

Les findings V12 ne justifient pas une nouvelle architecture.

La correction contractuelle suivante est autorisée, et seulement celle-ci :

1. préciser que la continuité `BAR_IN_PROGRESS → BAR_CLOSED` ne tranche pas la politique des late ticks ;
2. expliciter que les points dépendant de `event_time/availability_time` restent non PASS tant que la question est reportée ;
3. ne pas modifier le mécanisme d'identité dans V12 ;
4. ne pas modifier A-11 ;
5. ne pas introduire de politique de late ticks ou de contradictions/cycles.

**Verdict de l'adjudication :**

```text
V12
→ BLOCKED

Correction minimale autorisée → V13 candidate
```

La correction V13 doit subir un nouvel audit adversarial immédiatement après sa création.
