# DECISION REGISTER — T-03

**Version:** 0.1  
**Date:** 2026-08-31  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Status:** FROZEN  
**Scope:** Adjudication formelle de T-03 issu de l'audit adversarial `1.1.2 V4`.  

> Cette décision tranche uniquement la question de préséance entre `§9` et `§10` de `1.1.2` concernant la représentation des périodes sans données. Elle ne tranche pas à nouveau la politique « série creuse » ou « série continue » elle-même. Elle ne réouvre pas `DR-1 → DR-9`, `R-01 → R-07`, H-02 ou H-04. Toute extension de portée nécessite une nouvelle décision.

---

## 1. Question

Que doit faire `1.1.2` lorsque `§9` renvoie à une décision normative déjà arrêtée pour une série alors que `§10` formule une règle générale sur la représentation des périodes sans données ?

L'objectif est d'établir une règle de préséance unique afin que deux implémentations conformes, recevant les mêmes entrées et la même configuration normative, ne puissent pas choisir des représentations différentes.

---

## 2. Finding d'origine

L'audit adversarial de `1.1.2 V4` a identifié une contradiction entre :

- `§9`, qui indique que la représentation exacte des périodes sans données reste soumise à la décision normative déjà arrêtée pour la série concernée ;
- `§10`, qui énonce qu'une série reste creuse lorsqu'aucune observation normative ne permet de constituer la barre correspondante.

Sans règle de préséance, une implémentation peut appliquer `§10` tandis qu'une autre applique une décision spécifique mentionnée par `§9`, chacune pouvant prétendre être conforme au contrat.

**Finding concerné : H-03.**

---

## 3. Éléments du corpus / preuves

1. `1.1.2 V4 §9` — renvoi à la décision normative déjà arrêtée pour la série concernée.
2. `1.1.2 V4 §10` — règle générale de représentation de la série lorsqu'aucune observation normative ne permet de constituer une barre.
3. Audit adversarial `1.1.2 V4`, finding **H-03** — absence de préséance explicite entre `§9` et `§10`.
4. Le principe général de déterminisme de `1.1.2 §2.2` — une même configuration normative ne doit pas permettre des résultats normatifs divergents.

---

## 4. Options examinées

### Option A — `§10` prévaut toujours

La règle générale de `§10` écrase toute politique particulière éventuellement référencée par `§9`.

**Rejetée.** Cette option rendrait le renvoi de `§9` sans effet lorsque la décision spécifique prévoit une représentation différente et pourrait neutraliser une décision normative déjà gelée.

### Option B — Une décision normative spécifique applicable prévaut sur `§10`

Une décision explicitement gelée et applicable à la série constitue la règle de référence. `§10` constitue la règle par défaut uniquement lorsqu'aucune décision spécifique applicable ne couvre le cas.

**Retenue.** Cette option donne une hiérarchie déterministe sans créer de nouvelle politique « creuse/continue ».

### Option C — Aucune préséance ; choix laissé à l'implémentation

Chaque implémentation pourrait interpréter elle-même la relation entre `§9` et `§10`.

**Rejetée.** Elle maintient précisément l'ambiguïté détectée par H-03.

### Option D — Report

Ne pas trancher la préséance et conserver l'incohérence jusqu'à une décision ultérieure.

**Rejetée.** La préséance est nécessaire pour rendre le contrat déterministe avant V5.

---

## 5. Décision retenue

**T-03 : OPTION B — PRÉSÉANCE DE LA DÉCISION NORMATIVE SPÉCIFIQUE APPLICABLE.**

Une **décision normative explicitement gelée et applicable à la série prévaut sur la règle générale de `§10`**.

`§10` constitue la **règle générale par défaut** lorsqu'aucune décision normative spécifique applicable n'existe.

`§9` ne constitue donc pas une permission de choisir librement entre plusieurs représentations. Il impose l'application de la décision gelée lorsqu'une telle décision existe et est applicable.

Cette décision ne détermine pas si une série particulière doit être creuse, continue ou représentée selon une autre politique. Elle détermine uniquement **l'autorité applicable en cas de coexistence entre une décision spécifique et la règle générale de `§10`**.

---

## 6. Autorisations / interdictions

### Autorisé

- appliquer la décision normative spécifique lorsqu'elle est explicitement gelée et applicable à la série ;
- appliquer `§10` comme règle par défaut lorsqu'aucune décision spécifique applicable ne couvre le cas ;
- reporter explicitement un cas réellement non couvert plutôt que d'inventer une nouvelle politique ;
- conserver la traçabilité de la décision normative effectivement appliquée.

### Interdit

- choisir arbitrairement entre `§9` et `§10` ;
- laisser `§10` écraser une décision spécifique déjà FROZEN et applicable ;
- ignorer une décision spécifique applicable au motif que `§10` formule une règle générale ;
- inventer une troisième politique lorsque ni une décision spécifique ni la règle générale applicable ne permettent de déterminer le comportement ;
- permettre à deux implémentations de choisir des politiques différentes pour la même configuration normative.

---

## 7. Report éventuel

**Report : NON pour la règle de préséance.**

La hiérarchie d'autorité est tranchée par T-03.

**Report éventuel séparé :** la présente décision ne crée aucune valeur concrète de politique de représentation. Si une série ne dispose pas encore d'une décision spécifique propriétaire, aucune nouvelle politique particulière n'est créée par T-03 ; `§10` s'applique comme règle générale par défaut selon le contrat.

---

## 8. Impact sur `1.1.2 V5`

V5 devra intégrer cette règle de préséance explicitement afin que :

1. `§9` et `§10` ne puissent plus être interprétés comme deux autorités concurrentes ;
2. une décision spécifique FROZEN soit reconnue comme prioritaire lorsqu'elle est applicable ;
3. `§10` soit explicitement présenté comme règle générale par défaut ;
4. aucune nouvelle décision « série creuse/continue » ne soit introduite silencieusement par la rédaction de V5.

---

## 9. Règle de non-régression

Toute future version de `1.1.2` doit démontrer explicitement :

1. que la préséance de la décision normative spécifique applicable est conservée ;
2. que `§10` reste la règle générale par défaut en l'absence de décision spécifique applicable ;
3. qu'aucune formulation ne réintroduit une concurrence d'autorité entre `§9` et `§10` ;
4. que toute modification de cette hiérarchie fait l'objet d'une nouvelle adjudication.

---

## 10. Statut final

**ARBITRATED — FROZEN**

**T-03 est officiellement gelée et devient une source normative autorisée pour la rédaction de `1.1.2 V5`.**
