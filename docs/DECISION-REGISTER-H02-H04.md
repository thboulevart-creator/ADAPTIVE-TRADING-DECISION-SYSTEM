# DECISION REGISTER — H-02 / H-04

**Version:** 0.1
**Date:** 2026-08-31
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
**Status:** FROZEN
**Scope:** Adjudication formelle des findings H-02 et H-04 de l'audit adversarial `1.1.2 V4`.

> Ce registre ne réouvre pas `DR-1 → DR-9` ni `R-01 → R-07`. Il tranche uniquement les deux findings explicitement soumis à adjudication : H-02 et H-04. Toute extension de portée nécessitera une nouvelle décision.

---

## H-02 — Régime normatif des paramètres déterminants

### 1. Question

Pour les paramètres déterminants suivants :

- ordre d'agrégation ;
- timezone ;
- locale ;
- ordre de lecture ;
- parallélisme ;
- versions ;

le contrat doit-il seulement permettre une déclaration, ou ces paramètres doivent-ils être déterminés de manière normative afin qu'une même configuration normative ne puisse pas dépendre de leur comportement implicite ?

### 2. Finding d'origine

`1.1.2 V4 §12` avait supprimé l'obligation minimale présente dans V3 en renvoyant les six paramètres aux « décisions déjà gelées et exigences du corpus », alors que `§2.2` interdit les dépendances à un ordre d'agrégation non spécifié, à la timezone implicite, à la locale implicite, à l'ordre de lecture implicite et au comportement implicite du parallélisme.

Cette formulation permettait à deux implémentations de choisir des comportements différents tout en se déclarant conformes à `§12`.

### 3. Éléments du corpus / preuves

1. `1.1.2 V4 §2.2` — exigence de déterminisme et interdiction des dépendances implicites.
2. `1.1.2 V4 §12` — régime insuffisamment contraignant des paramètres déterminants.
3. Audit adversarial `1.1.2 V4`, finding **H-02** — contradiction entre `§12` et `§2.2`.
4. `docs/11-CONTRADICTION-ARBITRATION-REGISTRY.md` — une contradiction doit être analysée puis arbitrée avant correction silencieuse ; l'arbitrage doit préciser la proposition retenue, la proposition rejetée/limitée, la raison, le périmètre et l'effet de version.
5. `docs/AUDIT-SNAPSHOT-V1-V2C-2026-08-29.md` — discipline de continuation : aucune décision normative ne doit être inventée et les questions ouvertes restent ouvertes jusqu'à vérification.

### 4. Options examinées

**Option A — Déclaration suffisante.**
Chaque paramètre peut être déclaré sans être verrouillé ; les différences restent acceptables si elles sont documentées.

**Option B — Verrouillage normatif obligatoire.**
Chaque paramètre déterminant doit recevoir une valeur/règle normative déterminée et ne peut pas être laissé au comportement implicite de l'environnement, de la plateforme ou du parallélisme.

**Option C — Report.**
Ne pas trancher et conserver l'incohérence entre `§2.2` et `§12` jusqu'à une décision ultérieure.

### 5. Décision retenue

**H-02 : OPTION B — VERROUILLAGE NORMATIF OBLIGATOIRE.**

Pour tout paramètre dont la variation peut modifier un résultat normatif, le comportement doit être **déterminé normativement**. Une simple déclaration descriptive ne suffit pas.

La décision porte notamment sur les six paramètres du finding H-02. Elle ne crée pas ici les valeurs concrètes de chacun ; elle fixe leur **statut normatif obligatoire**. Les valeurs/règles concrètes seront reprises des décisions ou contrats propriétaires lorsqu'elles existent.

### 6. Autorisations / interdictions

**Autorisé :**
- définir explicitement une règle normative pour chacun des paramètres ;
- reprendre une valeur déjà fixée par un contrat ou une décision propriétaire ;
- déclarer la valeur effectivement appliquée à des fins de traçabilité, en complément de sa détermination normative.

**Interdit :**
- laisser l'ordre d'agrégation dépendre implicitement du partitionnement ou du parallélisme ;
- laisser timezone ou locale dépendre implicitement de l'environnement d'exécution ;
- laisser l'ordre de lecture dépendre implicitement du stockage, du système de fichiers, du moteur ou de l'itération ;
- considérer le parallélisme comme une liberté d'implémentation lorsqu'il peut modifier un résultat normatif ;
- utiliser une version non déterminée lorsqu'elle peut modifier un résultat normatif ;
- invoquer l'absence d'une décision concrète pour autoriser un comportement implicite.

### 7. Report éventuel

**Report : OUI, uniquement pour les valeurs/règles concrètes non encore propriétaires.**

Le présent arbitrage ne choisit pas une timezone, une locale, un ordre d'agrégation, un ordre de lecture, un modèle de parallélisme ou une version particulière. Il impose seulement que ces éléments soient déterminés avant toute implémentation normative qui en dépend.

**Aucune nouvelle valeur métier n'est créée par H-02.**

### 8. Statut

**ARBITRATED — FROZEN**

---

## H-04 — Représentation de `ordered_ticks` lorsque l'ordre est UNKNOWN

### 1. Question

Comment `BAR_IN_PROGRESS.ordered_ticks` doit-il représenter une barre dans laquelle l'ordre relatif de certains ticks ne peut pas être établi, sans inventer un ordre et sans permettre plusieurs structures conformes divergentes ?

### 2. Finding d'origine

`1.1.2 V4 §7.3` contient `ordered_ticks`, tandis que `§4.3` impose `order_status = UNKNOWN` lorsque l'ordre n'est pas établissable et que `§6.4` exige l'exposition de la séquence ordonnée par barre.

Le contrat ne définissait pas la structure de `ordered_ticks` dans le cas partiellement ou totalement UNKNOWN. Trois représentations concurrentes pouvaient donc être considérées conformes : liste totale avec marqueur, groupes non ordonnés, ou absence de séquence.

### 3. Éléments du corpus / preuves

1. `1.1.2 V4 §4.3` — l'incertitude d'ordre doit être conservée sous `order_status = UNKNOWN` lorsqu'elle est établie.
2. `1.1.2 V4 §6.4` — la séquence ordonnée par barre constitue une production normative ; l'ordre ne doit pas être inventé.
3. `1.1.2 V4 §7.3` — `BAR_IN_PROGRESS` contient `ordered_ticks`.
4. Audit adversarial `1.1.2 V4`, finding **H-04** — absence de représentation normative déterminée pour `ordered_ticks` sous `UNKNOWN`.
5. `docs/11-CONTRADICTION-ARBITRATION-REGISTRY.md` §8 — une adjudication doit indiquer la proposition retenue/rejetée, sa raison, son périmètre et son effet.

### 4. Options examinées

**Option A — Liste totale malgré UNKNOWN.**
Toujours fournir une liste linéaire et conserver `order_status = UNKNOWN` séparément.

**Option B — Séquence partielle déterministe.**
Représenter les relations d'ordre connues comme une suite de groupes ordonnés ; à l'intérieur d'un groupe, les ticks sont explicitement déclarés mutuellement non ordonnés. La sérialisation du groupe utilise un ordre canonique de représentation fondé sur l'identité stable des ticks, sans transformer cet ordre de sérialisation en ordre temporel.

**Option C — Omettre `ordered_ticks` lorsque l'ordre est UNKNOWN.**

**Option D — Report.**
Ne pas définir la structure et laisser la couche aval interpréter `UNKNOWN`.

### 5. Décision retenue

**H-04 : OPTION B — SÉQUENCE PARTIELLE DÉTERMINISTE.**

`ordered_ticks` est une **séquence de groupes d'ordre**. Chaque groupe contient les identités des ticks dont la relation d'ordre est connue comme équivalente/indistinguable dans le contrat. L'ordre entre groupes est normativement établi ; l'ordre interne d'un groupe est explicitement UNKNOWN et ne doit jamais être interprété comme un ordre temporel.

Pour rendre la représentation sérialisable et déterministe, les identifiants à l'intérieur d'un groupe doivent être sérialisés selon un **ordre canonique de représentation fondé sur l'identité stable du tick**. Cet ordre de sérialisation est purement représentationnel et ne constitue pas une information temporelle.

Exemple conceptuel :

```text
ordered_ticks = [
  { tick_ids: [T1] },
  { tick_ids: [T2, T3] }
]
order_status = UNKNOWN
```

Ici, `T1` précède le groupe `{T2,T3}`, mais aucune relation normative `T2 < T3` ou `T3 < T2` n'est créée.

### 6. Autorisations / interdictions

**Autorisé :**
- exposer une séquence partielle lorsque certaines relations d'ordre sont connues ;
- exposer un groupe contenant plusieurs ticks lorsque leur ordre relatif est UNKNOWN ;
- utiliser l'identité stable uniquement pour canoniser la représentation sérialisée d'un groupe.

**Interdit :**
- inventer un ordre temporel entre deux ticks déclarés UNKNOWN ;
- convertir arbitrairement UNKNOWN en une liste temporelle totale ;
- omettre l'information d'incertitude tout en exposant une liste qui semble totalement ordonnée ;
- laisser chaque implémentation choisir librement entre liste totale, groupes, omission ou autre structure ;
- utiliser l'ordre canonique de sérialisation comme preuve d'un ordre temporel.

### 7. Report éventuel

**Report : NON pour la structure.**

La structure normative de représentation est tranchée par H-04.

**Report éventuel séparé :** si le corpus propriétaire définit ultérieurement une sémantique plus fine des relations d'ordre (par exemple une granularité supplémentaire entre événements simultanés), cette sémantique pourra faire l'objet d'une nouvelle décision. Elle ne doit pas invalider silencieusement H-04.

### 8. Statut

**ARBITRATED — FROZEN**

---

# 3. Impact et portée commune

Les décisions H-02 et H-04 :

- ne modifient pas rétroactivement les faits du corpus historique ;
- ne réouvrent pas `DR-1 → DR-9` ;
- ne réécrivent pas `R-01 → R-07` ;
- constituent deux décisions nouvelles, explicitement identifiées comme telles ;
- doivent être intégrées à la prochaine version normative de `1.1.2` avant toute déclaration de conformité complète.

## 4. Règle de non-régression

Toute future version de `1.1.2` doit démontrer explicitement :

1. que H-02 est conservée sans réintroduire une simple déclaration comme substitut au verrouillage normatif ;
2. que H-04 conserve la représentation déterministe de l'incertitude d'ordre ;
3. qu'aucune formulation plus permissive n'est ajoutée à côté de la règle gelée ;
4. que toute modification de portée fait l'objet d'une nouvelle adjudication.

**État final : H-02 FROZEN — H-04 FROZEN.**
