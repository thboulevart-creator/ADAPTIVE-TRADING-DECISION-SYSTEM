# ADJUDICATION — Q-RM-02 PHYSICAL → LOGICAL CARDINALITY

**Date:** 5 septembre 2026  
**Scope:** normative semantic cardinality under validated RB-A / Q-RM-01  
**Status:** **CANDIDATE — ADVERSARIAL REVIEW COMPLETED; CONCRETE FORMAT BINDINGS REMAIN OPEN**  
**Exclusions:** no `CANONICAL_RECORD_POSITION`, no canonical enumeration, no temporal ordering, no physical identity primitive.

---

## 1. QUESTION

Pour une unité physique appartenant à une représentation d'acquisition déclarée et interprétée par un binding RB-A versionné, dans quelles conditions cette unité produit-elle :

```text
0 occurrence logique primaire
1 occurrence logique primaire
N occurrences logiques primaires
```

La règle doit être indépendante du parser, du runtime traversal, du parallélisme, du cache et de toute primitive physique choisie pour l'énumération ultérieure.

---

## 2. BASE NORMATIVE

Q-RM-01 a retenu **RB-A — modèle sémantique universel avec bindings explicites et versionnés par représentation déclarée**.

Le modèle déjà établi définit une occurrence logique primaire comme une occurrence individuellement retenue dans l'univers primaire qualifié, correspondant pour le dataset tick-oriented à une observation de marché primaire.

L'individualité est occurrence-based et non content-based : deux occurrences strictement identiques restent deux occurrences si elles sont toutes deux retenues.

Le record model précède la canonical enumeration et ne définit aucune précédence temporelle.

---

## 3. FORMALISATION

Pour une représentation déclarée `R` et un binding versionné `B`, une unité physique `u` est soumise à une interprétation normative déterministe :

```text
I_B(u) → interpretation outcome
```

L'outcome distingue obligatoirement **cardinalité** et **admissibilité de l'interprétation**.

Une cardinalité numérique n'est définie que lorsque l'interprétation est déterminée sans ambiguïté.

Pour une interprétation valide :

```text
C_B(u) = nombre d'occurrences logiques primaires
         déterminées par le binding B pour u
```

avec :

```text
C_B(u) = 0  → aucune occurrence primaire n'est produite
C_B(u) = 1  → exactement une occurrence primaire est produite
C_B(u) = N  → plusieurs occurrences primaires distinctes sont produites
             avec N > 1
```

La valeur `0` signifie **zéro occurrence résultant d'une interprétation valide**. Elle ne signifie jamais « erreur », « ambiguïté » ou « information inconnue ».

Ainsi :

```text
INVALID ≠ 0
AMBIGUOUS ≠ 0
```

Une entrée invalide ou ambiguë produit un résultat de qualification distinct et ne peut être transformée artificiellement en zéro occurrence.

---

## 4. RÈGLE NORMATIVE CANDIDATE

Sous RB-A :

> **La cardinalité physique→logique d'une unité est le nombre d'occurrences primaires que le binding format-spécifique, déclaré et versionné, détermine explicitement dans cette unité après segmentation sémantique déterministe et avant toute énumération canonique.**

Le binding doit donc déterminer, pour chaque classe de représentation supportée :

1. quelles parties de l'unité sont du contenu primaire ;
2. quelles parties sont non-observationnelles ;
3. comment les observations sont segmentées ;
4. combien d'occurrences primaires cette segmentation produit ;
5. comment une anomalie empêche, ou non, cette détermination.

La cardinalité n'est jamais déduite d'une convention physique générale telle que :

```text
1 ligne = 1 occurrence
1 fichier = 1 occurrence
1 objet = 1 occurrence
1 paquet = 1 occurrence
1 payload hash = 1 occurrence
```

sauf si le binding applicable établit explicitement cette relation pour la représentation concernée.

---

## 5. CLASSES NORMATIVES 0 / 1 / N

### 5.1 ZERO — `C = 0`

Une unité produit zéro occurrence lorsque, sous le binding applicable, elle est **validement interprétée comme ne contenant aucune observation primaire**.

Exemples conceptuels :

- header seul ;
- commentaire seul ;
- métadonnée seule ;
- séparateur ou enveloppe technique ne contenant aucune observation primaire ;
- unité vide lorsque le binding la définit comme représentation valide sans observation.

Important : le fait qu'un exemple soit intuitivement « non-observationnel » ne suffit pas à le rendre normatif. La classification exacte appartient au binding déclaré.

### 5.2 ONE — `C = 1`

Une unité produit exactement une occurrence lorsque le binding détermine une et une seule observation primaire complète dans cette unité.

La relation physique→logique peut être 1:1, mais elle n'est normative que parce que le binding la spécifie.

### 5.3 MANY — `C = N`, `N > 1`

Une unité produit plusieurs occurrences lorsque le binding détermine plusieurs observations primaires distinctes dans cette même unité.

Chaque observation ainsi déterminée constitue une occurrence logique distincte.

Une représentation multi-observations ne doit donc pas être artificiellement aplatie en une seule occurrence simplement parce qu'elle est contenue dans un seul objet physique.

Inversement, un objet contenant plusieurs champs appartenant à **une seule observation** ne doit pas être artificiellement découpé en plusieurs occurrences.

La frontière entre « plusieurs champs d'une observation » et « plusieurs observations » doit être déterminée par le binding sémantique versionné.

---

## 6. CAS MIXTES

Une unité peut contenir à la fois :

```text
non-observation material + observation(s)
```

Dans ce cas, le matériel non-observationnel ne contribue pas à la cardinalité primaire, sauf si le binding déclare explicitement qu'il fait partie du payload d'une observation.

Ainsi :

```text
header + observation → C = 1
metadata + 3 observations → C = 3
commentaire + aucun observation → C = 0
```

Ces exemples illustrent la règle sémantique ; les formes physiques concrètes doivent être fixées par les bindings.

---

## 7. MALFORMED / AMBIGUOUS — HORS CARDINALITÉ

Une représentation malformée ou ambiguë ne doit pas être convertie en cardinalité `0` simplement parce que le parseur n'a pas réussi à produire d'observation.

La distinction normative est :

```text
VALID + no primary observation     → C = 0
VALID + one primary observation    → C = 1
VALID + multiple observations      → C = N
INVALID                            → qualification outcome distinct
AMBIGUOUS                          → qualification outcome distinct
```

Cette séparation est nécessaire pour empêcher qu'une erreur de lecture fasse disparaître silencieusement des données de l'univers primaire.

Le traitement précis `REJECT RECORD` / `REJECT ACQUISITION` / `QUALIFICATION BLOCKED` reste traité dans Q-RM-04 et ne doit pas être inventé par Q-RM-02.

---

## 8. DOUBLONS STRICTS

Si un binding détermine deux occurrences distinctes ayant exactement le même payload :

```text
R1.payload = R2.payload
```

alors :

```text
C = 2
```

si les deux occurrences sont toutes deux des observations primaires distinctes selon le binding et sont retenues par qualification.

Aucune déduplication basée uniquement sur le contenu ne peut réduire :

```text
N occurrences → 1 occurrence
```

---

## 9. QUALIFICATION

Q-RM-02 distingue :

```text
physical unit
    ↓
valid deterministic logical interpretation
    ↓
0 / 1 / N candidate primary occurrences
    ↓
qualification membership
    ↓
retained logical universe
```

Une occurrence déterminée par le record model mais exclue par qualification ne devient pas une occurrence retenue.

Inversement, l'absence de rétention ne doit pas être confondue avec une cardinalité physique de zéro.

Cette distinction évite de mélanger :

```text
cardinality of interpretation
```

avec :

```text
qualification membership
```

---

## 10. TEST DES DEUX IMPLÉMENTATIONS

### Attaque A

Implémentation A considère chaque objet physique comme une occurrence.

### Attaque B

Implémentation B segmente l'objet en plusieurs observations.

### Résultat

Sous RB-A, aucune des deux n'est conforme par préférence d'implémentation.

La conformité dépend du binding versionné applicable. Si celui-ci définit que l'objet contient trois observations :

```text
C = 3
```

et une implémentation qui produit `C = 1` est non conforme.

Si le binding définit une seule observation contenant plusieurs champs :

```text
C = 1
```

et une implémentation qui produit `C = 3` est non conforme.

La cardinalité est donc déterminée sémantiquement par le binding, pas par la granularité physique choisie par le runtime.

---

## 11. CASSAGE ADVERSARIAL

### C-01 — « Tout ce qui n'est pas observation = 0 »

**Problème :** cela pourrait convertir un record malformé en zéro occurrence.

**Correction :** `0` n'est permis que pour une interprétation valide déterminant explicitement l'absence d'observation. `INVALID` et `AMBIGUOUS` sont des outcomes distincts.

### C-02 — « N observations dans un objet = N occurrences »

**Problème :** le mot « observation » pourrait lui-même être interprété différemment selon les implémentations.

**Correction :** le binding versionné doit définir la segmentation sémantique qui détermine ce qu'est une observation primaire. Le runtime ne peut pas inventer cette segmentation.

### C-03 — « Les champs internes créent plusieurs occurrences »

**Problème :** une observation peut contenir plusieurs champs.

**Correction :** cardinalité porte sur les observations primaires, pas sur le nombre de champs, tokens ou attributs.

### C-04 — « Déduplication des occurrences identiques »

**Problème :** cela détruit l'individualité occurrence-based.

**Correction :** chaque occurrence distincte déterminée par le binding reste distincte, même avec payload identique.

### C-05 — « Parser failure = zéro »

**Problème :** cela masque les pertes de données et confond erreur et absence d'observation.

**Correction :** invalidité/ambiguïté restent hors de la cardinalité numérique.

### C-06 — « Qualification exclusion = zéro »

**Problème :** cela confond interprétation et membership.

**Correction :** la cardinalité est déterminée avant la décision finale de membership ; une occurrence candidate peut ensuite être exclue par qualification.

### C-07 — « Physical order determines N »

**Problème :** le nombre d'occurrences deviendrait dépendant du traversal runtime.

**Correction :** le binding détermine la segmentation et la cardinalité avant l'énumération et indépendamment du traversal.

---

## 12. RE-CASSAGE

### RC-01 — Binding insuffisamment spécifié

Si un binding dit seulement :

```text
« parser ce format et extraire les observations »
```

sans définir ce qui constitue une observation ou comment segmenter une unité multi-observations, alors deux implémentations peuvent diverger.

**Conséquence :** ce binding est normativement insuffisant et ne peut pas être déclaré conforme simplement parce que les deux implémentations « semblent raisonnables ».

### RC-02 — Format physiquement ambigu

Si aucune version de binding ne permet une segmentation unique :

```text
u → interpretation A
u → interpretation B
```

alors aucune cardinalité numérique ne peut être choisie par préférence d'implémentation.

**Conséquence :** Q-RM-02 ne force pas un faux `0`, `1` ou `N`; l'entrée bascule dans le traitement d'ambiguïté de Q-RM-04.

### RC-03 — Changement futur du binding

Si une nouvelle version transforme :

```text
C = 1 → C = 2
```

pour une même représentation physique, ce changement peut modifier l'univers logique.

**Conséquence :** le changement doit être versionné et ne peut pas être masqué comme simple évolution du parser.

---

## 13. RÉPONSE ROBUSTE

La règle robuste est donc :

```text
Pour une représentation déclarée R et un binding versionné B,

1. B détermine une interprétation sémantique déterministe de l'unité u.
2. Si cette interprétation est valide, B segmente u en observations primaires.
3. La cardinalité C_B(u) est le nombre d'observations primaires ainsi déterminées.
4. C_B(u) ∈ {0, 1, N | N > 1}.
5. C = 0 signifie absence valide d'observation, jamais erreur ou ambiguïté.
6. INVALID et AMBIGUOUS ne sont pas des cardinalités.
7. Chaque observation primaire distincte reste une occurrence distincte.
8. Le contenu, le nombre de champs et le choix du parser ne déterminent pas à eux seuls la cardinalité.
9. Le traversal, le parallélisme, le cache et l'énumération canonique ne peuvent pas modifier C.
10. Tout binding qui ne permet pas de déterminer C de manière unique est normativement insuffisant.
```

---

## 14. VERDICT

```text
Q-RM-02 SEMANTIC RULE = PASS
CONCRETE FORMAT BINDINGS = BLOCKED
```

La sémantique générale de cardinalité est désormais suffisamment déterminée sous RB-A :

```text
VALID + aucune observation → 0
VALID + une observation    → 1
VALID + plusieurs          → N
INVALID                    → hors cardinalité
AMBIGUOUS                  → hors cardinalité
```

Ce PASS ne signifie **pas** que le record model global est gelé. Les bindings concrets doivent encore fournir les règles de segmentation et de classification nécessaires pour rendre cette cardinalité exécutable pour chaque représentation supportée.

---

## 15. GOUVERNANCE

Ce bloc n'autorise :

- aucune définition de `CANONICAL_RECORD_POSITION` ;
- aucune définition d'ordre canonique ;
- aucun primitive physique d'identité ;
- aucune modification de `1.1.2` ;
- aucune règle temporelle.

Le prochain travail reste dans le record model : Q-RM-03, puis Q-RM-04, avec réévaluation des dépendances Q-RM-05 à Q-RM-07.

## FIN
