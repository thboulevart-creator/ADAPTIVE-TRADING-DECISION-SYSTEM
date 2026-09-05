# ADJUDICATION PACKAGE — RECORD BOUNDARY & PHYSICAL→LOGICAL CARDINALITY

**Date:** 5 septembre 2026  
**Reference HEAD:** `51dc9949bad2a420ffc9443a0243f63916916f34`  
**Scope:** normative logical record model — record boundaries and physical→logical cardinality only  
**Status:** **DECISION REQUIRED — NO DECISION TAKEN**

---

## 1. PURPOSE

Le précédent audit `ADJUDICATION-PHYSICAL-TO-LOGICAL-RECORD-MAPPING-AUDIT-V1-2026-09-05` a établi que le modèle logique candidat est correctement orienté mais ne peut pas encore être gelé.

Les bloqueurs sont notamment :

- `B-RM-01` — Record Boundary Contract ;
- `B-RM-02` — Physical-to-Logical Cardinality ;
- `B-RM-03` — Non-observation Material ;
- `B-RM-04` — Malformed / Ambiguous Input ;
- `B-RM-05` — Acquisition Domain ;
- `B-RM-06` — Format Binding / Versioning ;
- `B-RM-07` — Qualification Freeze.

Ce document ne choisit aucun mécanisme physique d'identité ou d'énumération.

Il ne définit pas :

- `CANONICAL_RECORD_POSITION` ;
- un ordre canonique ;
- un row number ;
- un byte offset ;
- un source ordinal ;
- un provider ID ;
- un hash d'identité ;
- `ordered_ticks` ;
- une règle temporelle.

---

## 2. QUESTION DE DÉCISION

La décision requise est :

> **Quelle sémantique normative doit déterminer, pour chaque représentation d'acquisition déclarée, ce qui constitue une occurrence logique primaire et combien d'occurrences logiques peuvent être produites par une unité physique donnée ?**

La décision doit rester sémantique et indépendante de tout primitive physique particulier.

---

## 3. INVARIANTS DÉJÀ ACQUIS — À NE PAS ROUVRIR

Les points suivants sont déjà établis et ne constituent pas des choix ouverts dans cette décision :

1. une occurrence logique est une occurrence individuellement retenue dans l'univers primaire qualifié ;
2. l'individualité est fondée sur l'occurrence, non sur le contenu ;
3. deux occurrences strictement identiques peuvent être deux occurrences distinctes ;
4. le record model appartient au contrat normatif upstream ;
5. le record model est versionné ;
6. la qualification détermine l'appartenance à l'univers retenu ;
7. le record model ne définit pas la précédence temporelle ;
8. l'énumération canonique est une étape ultérieure ;
9. aucun primitive physique n'est actuellement sélectionné ;
10. une ambiguïté non résolue ne peut pas être tranchée par préférence d'implémentation.

---

## 4. DÉCISION Q-RM-01 — RECORD BOUNDARY

### Question

Pour une représentation physique déclarée et une version donnée du binding, quelle règle détermine exactement les frontières d'une occurrence logique ?

### Propriété minimale exigée

La règle doit permettre à deux implémentations conformes, recevant la même représentation déclarée et la même version normative, de déterminer :

```text
mêmes frontières logiques
→ même ensemble d'occurrences candidates
```

### Interdit

Aucune frontière ne peut être choisie uniquement selon :

- préférence du parser ;
- comportement implicite d'une bibliothèque ;
- ordre de traversal runtime ;
- heuristique non déclarée ;
- convention physique non qualifiée comme normative.

### Décision humaine requise

Déterminer le niveau de précision sémantique attendu pour le record boundary :

**Option RB-A — modèle sémantique universel**  
Le contrat définit une notion abstraite de record et chaque format déclaré fournit un binding explicite vers cette notion.

**Option RB-B — modèle sémantique avec classes de cardinalité déclarées**  
Le contrat définit directement les classes de représentations physiques susceptibles de produire zéro/une/plusieurs occurrences, sans sélectionner leur primitive physique.

**Option RB-C — autre formulation**  
Une autre sémantique peut être retenue si elle conserve les invariants du §3 et reste indépendante de l'énumération canonique.

Aucune option n'est sélectionnée dans ce document.

---

## 5. DÉCISION Q-RM-02 — PHYSICAL→LOGICAL CARDINALITY

### Question

Une unité physique donnée peut-elle correspondre à :

```text
0 occurrence
1 occurrence
N occurrences
```

et, si oui, dans quelles conditions normatives ?

### Cas à couvrir

Au minimum :

| Cas physique | Question normative |
|---|---|
| header seul | 0 occurrence ou autre traitement ? |
| métadonnée | 0 occurrence ou partie du record ? |
| observation simple | 1 occurrence ? |
| conteneur multi-observations | N occurrences ? |
| record vide | 0 occurrence ou invalidité ? |
| record malformé | rejet, unknown, invalidité de l'acquisition ou autre ? |
| représentation ambiguë | résultat déterministe requis ; choix d'implémentation interdit |
| doublon strict | 1 occurrence par occurrence retenue, jamais collapse implicite |

### Propriété minimale exigée

La cardinalité doit être déterminable à partir de la représentation déclarée, du record-model version et des règles de qualification applicables.

Elle ne peut pas dépendre du parcours runtime.

---

## 6. DÉCISION Q-RM-03 — NON-OBSERVATION MATERIAL

Le contrat doit déterminer comment sont classés :

- headers ;
- commentaires ;
- métadonnées ;
- séparateurs ;
- enveloppes techniques ;
- contenu non observationnel ;
- contenu mixte observation + métadonnée.

### Invariant

Un contenu non-observationnel ne peut pas entrer silencieusement dans l'univers primaire.

### Point à décider

La classification doit-elle être :

- définie par le modèle général ;
- définie par chaque format binding ;
- ou répartie entre les deux avec une règle de priorité explicite ?

Aucune réponse n'est choisie ici.

---

## 7. DÉCISION Q-RM-04 — MALFORMED / AMBIGUOUS INPUT

### Question

Que doit produire la qualification lorsqu'une représentation ne permet pas une individuation non ambiguë ?

### Invariants déjà établis

- pas de réparation silencieuse ;
- pas de réinterprétation silencieuse ;
- pas de choix dépendant de l'implémentation ;
- pas de création artificielle d'occurrences.

### Point à décider

Le contrat doit déterminer explicitement la frontière entre :

```text
record rejeté
acquisition rejetée
état UNKNOWN / qualification bloquée
autre résultat normatif explicitement défini
```

Aucune réponse n'est choisie ici.

---

## 8. DÉCISION Q-RM-05 — ACQUISITION DOMAIN

Pour une acquisition répartie sur plusieurs fichiers, objets ou partitions, le contrat doit déterminer l'unité sémantique à laquelle s'applique le record model.

Le choix doit distinguer :

```text
acquisition domain
≠
ordre physique
≠
ordre temporel
≠
canonical enumeration
```

Aucun global ordinal n'est créé par cette décision.

### Point à décider

Le domaine logique est-il :

- l'acquisition complète déclarée ;
- une partition déclarée ;
- une autre unité explicitement qualifiée ?

Aucune réponse n'est choisie ici.

---

## 9. DÉCISION Q-RM-06 — FORMAT BINDING / VERSIONING

Lorsqu'un format particulier peut modifier :

- frontières ;
- cardinalité ;
- interprétation des champs ;
- individuation ;
- appartenance à l'univers qualifié ;

le binding correspondant doit être identifiable et versionné.

### Invariant

Un changement susceptible de modifier l'univers logique ne peut pas être présenté comme une variation invisible d'implémentation.

### Point à décider

Déterminer la granularité normative des bindings et leur relation avec la version du record model général.

Aucune matrice concrète n'est choisie ici.

---

## 10. DÉCISION Q-RM-07 — QUALIFICATION FREEZE

Le mapping physique→logique devient immuable à un point normatif de qualification.

Après ce point, les opérations suivantes ne peuvent pas changer l'univers logique :

- traversal ;
- cache ;
- parallélisme ;
- restart ;
- sérialisation ;
- réordonnancement runtime.

### Point à décider

Le contrat doit nommer le point exact où cette immutabilité prend effet et quelles entrées normatives constituent la référence de reconstruction.

Aucune nouvelle mécanique de restart n'est créée ici.

---

## 11. TEST DE DÉCISION — DEUX IMPLÉMENTATIONS

Une décision est insuffisante si elle permet encore :

### Implémentation A

```text
unité physique → une occurrence
```

### Implémentation B

```text
même unité physique → plusieurs occurrences
```

sans critère normatif permettant de départager les deux.

La même exigence s'applique à la classification du contenu non-observationnel et au traitement des entrées malformées/ambiguës.

---

## 12. GATE AVANT CANONICAL ENUMERATION

Aucune définition de `CANONICAL_RECORD_POSITION` ne doit commencer avant que les propriétés suivantes soient déterminées :

```text
record boundary
physical→logical cardinality
non-observation material
malformed/ambiguous input
acquisition domain
format binding/versioning
qualification freeze
```

Le passage à l'énumération exige ensuite un audit séparé de stabilité de séquence.

---

## 13. STATUT

```text
ARCHITECTURE FAMILY              = RESOLVED
IDENTITY OWNERSHIP               = RESOLVED UPSTREAM
IDENTITY SCOPE                   = ACQUISITION-SCOPED
LOGICAL RECORD SEMANTICS        = CANDIDATE DEFINED
BOUNDARY/CARDINALITY             = DECISION REQUIRED
CANONICAL ENUMERATION            = NOT TOUCHED
1.1.2                            = BLOCKED
```

**Conclusion :** le prochain bloc n'est pas une correction de `1.1.2` ni une définition de l'énumération. C'est une **décision humaine amont ciblée sur la sémantique du record model**, principalement `Q-RM-01` et `Q-RM-02`, avec les conséquences nécessaires `Q-RM-03` à `Q-RM-07`.

## FIN
