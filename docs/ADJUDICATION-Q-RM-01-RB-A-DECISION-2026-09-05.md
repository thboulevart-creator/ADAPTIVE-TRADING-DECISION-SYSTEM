# ADJUDICATION DECISION — Q-RM-01 RECORD BOUNDARY / RB-A

**Date:** 5 septembre 2026  
**Scope:** Q-RM-01 — Record Boundary  
**Reference decision:** `ADJUDICATION-RECORD-BOUNDARY-CARDINALITY-DECISION-2026-09-05.md`  
**Status:** **DECISION TAKEN — RB-A VALIDATED**

---

## 1. QUESTION

Pour une représentation physique déclarée et une version donnée du binding, quelle sémantique normative détermine exactement les frontières d'une occurrence logique ?

La décision doit garantir que deux implémentations conformes recevant la même représentation déclarée et la même version normative déterminent les mêmes frontières logiques et donc le même ensemble d'occurrences candidates.

---

## 2. CANDIDATURE VALIDÉE

**RB-A — modèle sémantique universel avec bindings explicites par format.**

Le contrat définit une notion abstraite normative de record logique. Chaque représentation/format d'acquisition déclaré fournit un binding explicite et versionné vers cette sémantique.

RB-A ne sélectionne aucun primitive physique particulier comme définition universelle du record.

---

## 3. FORMALISATION

Soit :

```text
R = représentation d'acquisition déclarée
V = version normative du record model / binding applicable
Q = règles de qualification applicables
```

Le mapping normatif est une fonction sémantique déterministe :

```text
M(R, V, Q) → séquence/ensemble d'occurrences logiques candidates
```

avec, pour chaque occurrence candidate, une frontière sémantiquement déterminée par le binding applicable.

Une implémentation conforme ne peut pas substituer à cette fonction :

- un choix de parser ;
- un comportement de bibliothèque ;
- un ordre de traversal runtime ;
- une convention physique non déclarée ;
- une heuristique locale.

La notion de record logique précède toute énumération canonique.

---

## 4. COMPARAISON DES OPTIONS

### RB-A

Modèle sémantique abstrait commun + binding explicite et versionné pour chaque représentation déclarée.

**Avantages normatifs :**

- sépare la sémantique du record de sa représentation physique ;
- permet de traiter plusieurs formats sans faire d'un format particulier la définition universelle ;
- rend explicite toute différence de frontières ou de cardinalité introduite par un format ;
- permet la versionation lorsque l'évolution du format modifie l'univers logique ;
- reste indépendant de la future énumération canonique ;
- préserve l'identité fondée sur l'occurrence plutôt que sur le contenu.

### RB-B

Classes de cardinalité déclarées au niveau du modèle.

**Faiblesse :** la cardinalité seule ne suffit pas à définir les frontières sémantiques d'un record. Deux représentations peuvent toutes deux être de cardinalité « plusieurs » tout en ayant des règles d'individuation différentes. RB-B risque donc de déplacer la difficulté sans fournir une abstraction suffisante pour le boundary contract.

### RB-C

Ouverte par construction. Elle ne peut être préférée à RB-A que si elle apporte une propriété normative supplémentaire sans réintroduire de dépendance à une primitive physique, à l'implémentation ou à l'énumération canonique.

Aucune telle propriété n'est démontrée dans le corpus actuel.

---

## 5. CASSAGE ADVERSARIAL

### A-01 — Une unité physique contient plusieurs observations

Une ligne, objet ou paquet peut contenir plusieurs observations logiques.

**Résultat :** RB-A ne force pas « une unité physique = un record ». Le binding doit déclarer la frontière sémantique appropriée. L'attaque ne casse donc pas RB-A.

### A-02 — Plusieurs unités physiques constituent une seule occurrence

Un record logique peut être réparti sur plusieurs unités physiques.

**Résultat :** RB-A ne confond pas unité physique et record logique. Le binding peut définir une frontière couvrant plusieurs unités. L'attaque ne casse donc pas RB-A.

### A-03 — Même contenu, occurrences distinctes

Deux occurrences strictement identiques sont présentes dans l'acquisition.

**Résultat :** RB-A ne définit pas l'individuation par contenu. La qualification peut retenir deux occurrences distinctes. L'attaque ne casse pas l'invariant d'individualité.

### A-04 — Deux formats différents pour les mêmes observations

Deux formats ont des frontières physiques différentes.

**Résultat :** chaque format peut avoir son binding explicite et versionné. Aucune identité ou frontière physique n'est implicitement transférée d'un format à l'autre. L'attaque ne casse pas RB-A.

### A-05 — Parser A et parser B produisent des segmentations différentes

Les deux implémentations utilisent des bibliothèques différentes.

**Résultat :** leur comportement de parser n'est pas la règle normative. La conformité est évaluée contre le binding sémantique versionné. Une divergence de parser constitue une non-conformité d'implémentation, pas une divergence autorisée du modèle. L'attaque ne casse pas RB-A.

### A-06 — Réordonnancement runtime

Traversal séquentiel, parallèle ou reprise après interruption.

**Résultat :** le traversal intervient après/indépendamment de la détermination normative de l'univers logique. Il ne peut pas modifier les frontières. L'attaque ne casse pas RB-A.

### A-07 — Binding insuffisamment précis

Un binding dit seulement « ce format contient des observations » sans définir les frontières dans les cas ambigus.

**Résultat :** RB-A est alors correctement BLOCKED au niveau du binding ; cela ne constitue pas un échec du modèle universel. La conséquence est que le binding concerné doit être précisé/versionné avant qualification normative.

### A-08 — Évolution du format

Une nouvelle version du format change la segmentation ou l'interprétation.

**Résultat :** la version du binding permet de distinguer les deux sémantiques. Une variation susceptible de changer l'univers logique ne peut pas être masquée comme détail d'implémentation.

### A-09 — Introduction d'une primitive physique comme pseudo-règle

Une implémentation propose row number, byte offset, source ordinal, provider ID ou hash comme définition du record.

**Résultat :** RB-A ne l'autorise pas. Une primitive physique peut éventuellement servir de donnée de localisation/provenance dans un contrat ultérieur, mais elle ne devient pas la sémantique du record par préférence d'implémentation.

---

## 6. RE-CASSAGE

La principale faiblesse résiduelle est la suivante : **RB-A est une architecture normative de liaison, pas encore le contenu concret des bindings.**

Cela signifie qu'adopter RB-A ne rend pas automatiquement Q-RM-01 opérationnel pour tous les formats.

Le modèle reste insuffisant si un binding concret ne définit pas, de façon déterministe et versionnée :

```text
- unité(s) physique(s) pertinentes ;
- frontière de début ;
- frontière de fin ;
- règles de regroupement/séparation ;
- traitement du contenu non-observationnel ;
- traitement des cas ambigus/malformés ;
- relation avec la qualification ;
- version applicable.
```

Cette limite est compatible avec la décision RB-A et devient précisément une obligation de fermeture des décisions Q-RM-02 à Q-RM-07 et des bindings concrets.

---

## 7. CORRECTION / RÉPONSE ROBUSTE

La formulation normative retenue est :

> **Le Record Boundary Contract est défini selon un modèle sémantique universel abstrait. Pour chaque représentation d'acquisition déclarée, un binding explicite et versionné détermine comment cette représentation est interprétée comme une ou plusieurs occurrences logiques, notamment leurs frontières. La représentation physique et les primitives de localisation ne constituent pas, par elles-mêmes, la définition normative d'un record. Toute ambiguïté non résolue au niveau du binding empêche la qualification normative ; elle ne peut être résolue par préférence d'implémentation.**

Cette formulation conserve les invariants déjà acquis et ne préjuge ni de l'énumération canonique, ni de l'ordre temporel, ni d'un primitive physique d'identité.

---

## 8. CONSÉQUENCES SUR Q-RM-02

RB-A permet explicitement les cardinalités :

```text
0 occurrence
1 occurrence
N occurrences
```

mais ne choisit pas encore les règles concrètes de chaque classe de représentation.

Q-RM-02 doit maintenant déterminer la cardinalité normative par binding, en conservant la contrainte :

```text
même représentation déclarée
+ même version normative
+ mêmes règles de qualification
→ même univers logique
```

La décision RB-A ne doit donc pas être interprétée comme une résolution automatique de Q-RM-02.

---

## 9. VERDICT

```text
Q-RM-01 = PASS — RB-A VALIDATED
```

**Important :** PASS porte sur le choix de la famille sémantique normative RB-A. Il ne signifie pas que tous les bindings concrets sont déjà spécifiés ou que Q-RM-02 à Q-RM-07 sont résolus.

---

## 10. GATE SUIVANT

Le prochain bloc est **Q-RM-02 — Physical→Logical Cardinality**.

Il devra être audité contre RB-A et déterminer, pour les représentations déclarées, les conditions normatives produisant zéro, une ou plusieurs occurrences.

Aucune définition de `CANONICAL_RECORD_POSITION` ne doit commencer avant la fermeture des bloqueurs du package initial.
