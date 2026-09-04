# Q1 — AUDIT ADVERSARIAL DES CANDIDATS DE CONSTRUCTION DE L'IDENTITÉ OBSERVATIONNELLE

**Date:** 4 septembre 2026
**Scope:** déterminer, après fermeture de la portée de stabilité à la lignée d'acquisition, quels mécanismes peuvent encore fournir une identité observationnelle déterministe et reproductible.
**Reference HEAD:** `7af54558c490620f7b526cd121bb1e997cbbf915`
**Status:** **AUDIT — CANDIDATS ÉLIMINÉS / PRIMITIVE CANONIQUE NON ENCORE GELÉE**

---

## 1. ÉTAT D'ENTRÉE

La portée de stabilité a été arbitrée à l'échelle de la lignée d'acquisition :

```text
observation_identity
    = identity of an observation admitted in one qualified dataset lineage
```

Cette décision n'implique pas encore la composition concrète de l'identité.

Le corpus actuellement vérifié ne contient pas de définition normative complète de l'identité individuelle du record. Les documents `09` et `05` restent explicitement non normatifs sur ce point ; `09` définit notamment l'identité du dataset et la provenance de l'acquisition, pas une primitive normative d'identité individuelle. 

`V12` exige une égalité de multisets d'identités entre les observations de `ordered_ticks` et les ticks primaires assignés à une barre. La vérifiabilité de cet invariant dépend donc toujours d'une identité individuelle effectivement définie en amont.

---

# 2. CANDIDAT 1 — POSITION DANS L'ARTEFACT SOURCE

## Définition candidate

```text
source_artifact
    ↓
record enumeration / record offset
    ↓
source_record_position
```

### Verdict

**ADMISSIBLE SOUS CONDITIONS — pas encore une primitive normative complète.**

### Pourquoi elle n'est pas éliminée

Dans une portée limitée à une acquisition, un artefact source capturé et immuable peut fournir une base déterministe d'énumération. Deux implémentations peuvent obtenir la même position si elles reçoivent exactement le même artefact et appliquent la même règle d'énumération.

La position peut être purement représentationnelle et ne pas constituer un ordre temporel.

### Conditions indispensables

Il faudrait au minimum que soient normativement définis :

- l'artefact exact constituant l'entrée ;
- son identité/intégrité ;
- la frontière d'un record ;
- la règle d'énumération ;
- le point auquel la position est attribuée ;
- l'immutabilité de l'attribution ;
- la sémantique des doublons ;
- la relation entre plusieurs fichiers/objets d'une même acquisition.

### Failles

Une simple notion de « ligne du fichier » ou « offset » n'est pas suffisante si le fichier n'est pas lui-même l'entrée normative exacte ou si le format permet plusieurs interprétations de record boundaries.

**Classification : [ARCHITECTURE PROPOSÉE] / [CONSÉQUENCE NÉCESSAIRE pour les conditions de stabilité].**

---

# 3. CANDIDAT 2 — POSITION ATTRIBUÉE LORS DE LA QUALIFICATION

## Définition candidate

```text
qualified dataset
    ↓
canonical enumeration
    ↓
position assigned once
```

### Verdict

**ADMISSIBLE EN THÉORIE — insuffisant en l'état.**

### Point positif

Le fait d'attribuer la position une seule fois en amont résout la dérive sous les transformations avales et les réordonnancements runtime.

### Failles

« Position attribuée lors de la qualification » ne constitue pas encore une règle de détermination. Il faut savoir comment l'énumération est produite.

Si l'énumération dépend de l'ordre de traversal d'un programme, elle n'est pas normative.

Si elle dépend d'un tri temporel, elle risque de transformer la position en substitut de l'ordre temporel.

Si elle dépend uniquement du contenu, les doublons stricts ne peuvent pas être distingués.

### Conclusion

Le lieu d'attribution est correct, mais il ne résout pas à lui seul le problème du critère d'énumération.

**Classification : [CONSÉQUENCE NÉCESSAIRE] pour l'attribution unique ; [ARCHITECTURE PROPOSÉE] pour son emplacement exact.**

---

# 4. CANDIDAT 3 — IDENTIFIANT FOURNI PAR LE DATASET / LA SOURCE

### Verdict

**NON PROUVÉ — NON ADOPTABLE COMME PRIMITIVE NORMATIVE À CE STADE.**

Le corpus actuel ne démontre pas l'existence d'un identifiant individuel fourni par la source qui soit simultanément :

- présent pour chaque record pertinent ;
- unique dans l'acquisition ;
- stable pendant toute la lignée ;
- préservé lors des transformations ;
- déterministe entre implémentations ;
- suffisamment défini pour les doublons stricts.

L'absence de preuve n'est pas une preuve d'absence, mais elle interdit de transformer cette possibilité en règle normative.

**Classification : [ABSENCE DE PREUVE].**

---

# 5. CANDIDAT 4 — COMBINAISON PROVENANCE + POSITION

## Définition candidate

```text
(provenance_domain, local_position)
```

### Verdict

**FAMILLE ARCHITECTURALE LA PLUS SOLIDE — mais dépendante d'une position locale elle-même déterministe.**

La provenance fournit le domaine de l'identité ; la position distingue les records au sein de ce domaine.

La portée désormais arbitrée rend cette construction cohérente :

```text
acquisition lineage
    ↓
local record position
    ↓
observation identity
```

Elle résout notamment :

- l'unicité entre acquisitions différentes ;
- la distinction des doublons stricts au sein d'une même acquisition ;
- la stabilité après réordonnancement aval ;
- la séparation entre identité observationnelle et ordre temporel.

### Failles résiduelles

La combinaison n'est pas une règle d'énumération. Elle ne devient déterministe que si `local_position` est attribuée selon une règle normative déterministe.

Il faut également définir si `provenance_domain` est :

- le dataset qualifié ;
- l'artefact source ;
- un sous-flux ;
- ou une autre unité déjà définie dans le corpus.

**Classification : [ARCHITECTURE PROPOSÉE] avec plusieurs conséquences nécessaires déjà établies.**

---

# 6. CANDIDAT 5 — AUTRE PRIMITIVE DÉJÀ PRÉSENTE DANS LE CORPUS

Les primitives vérifiées dans le corpus sont principalement de niveau dataset/provenance et temporel. `09` fournit notamment `dataset_id`, `dataset_version`, `content_hash`, source/acquisition et lineage, mais ne définit pas une identité individuelle normative du record.

### Verdict

**AUCUNE PRIMITIVE INDIVIDUELLE DÉJÀ PROUVÉE DANS LE CORPUS.**

`dataset_id` seul ne suffit pas : tous les records du dataset partageraient le même identifiant.

`dataset_version` seul ne suffit pas.

`content_hash` du dataset seul ne suffit pas à distinguer deux records.

Les timestamps et prix ne suffisent pas pour les doublons stricts.

`ordered_ticks` ne peut pas être utilisé comme primitive d'identité : il est une représentation aval de l'ordre temporel et dépend précisément de l'identité qu'il doit préserver.

**Classification : [ABSENCE DE PREUVE] / [CONSÉQUENCE NÉCESSAIRE].**

---

# 7. MATRICE D'ÉLIMINATION

| Candidat | Déterminisme | Doublons | Réordonnancement aval | Inter-acquisition | Risque ordre temporel | Statut |
|---|---|---|---|---|---|---|
| 1. Position artefact source | possible | oui | oui si capturée | non requis | faible si sémantique explicite | admissible sous conditions |
| 2. Position qualification | possible | oui | oui | non requis | faible si critère séparé | admissible mais critère manquant |
| 3. ID source | non prouvé | non prouvé | non prouvé | non requis | faible | non adoptable faute de preuve |
| 4. Provenance + position | oui si position déterministe | oui | oui | non requis | faible | meilleure famille candidate |
| 5. autre primitive corpus | aucune prouvée | non | non | non | variable | éliminée faute de primitive |

---

# 8. POINT CRITIQUE

Les candidats 1 et 2 ne sont pas réellement deux primitives concurrentes indépendantes.

Le candidat 1 définit **où la séquence existe** : l'artefact d'acquisition.

Le candidat 2 définit **quand l'attribution devient immuable** : à la qualification.

Une construction robuste peut donc combiner les deux :

```text
IMMUTABLE ACQUISITION ARTIFACT
        ↓
DETERMINISTIC RECORD ENUMERATION
        ↓
POSITION ASSIGNED ONCE AT QUALIFICATION
        ↓
(PROVENANCE DOMAIN, POSITION)
        ↓
OBSERVATION IDENTITY
```

Cette combinaison n'est toutefois pas encore une décision normative : la règle exacte d'énumération reste à établir.

---

# 9. TESTS D'ÉLIMINATION À APPLIQUER À LA PRIMITIVE RETENUE

La prochaine définition candidate devra passer au minimum :

1. même artefact → même identité ;
2. traversal runtime différent → même identité ;
3. réordonnancement aval → même identité ;
4. doublons stricts → identités distinctes ;
5. timestamp identique → aucune identité forcée par le timestamp ;
6. ordre temporel `UNKNOWN` → aucune résolution par identité ;
7. multi-fichier → résultat déterministe ;
8. même dataset lineage → même identité ;
9. acquisition différente → identité potentiellement différente, sans anomalie ;
10. sérialisation H-04/A-09 → identité comparable et stable ;
11. aucune collision ;
12. aucune dépendance à timezone/locale/parallélisme ;
13. aucune dépendance à une mémoire runtime non reconstructible.

---

# 10. CONCLUSION D'AUDIT

L'audit élimine comme primitives normatives autonomes :

- l'identifiant source, faute de preuve corpus ;
- les primitives déjà présentes au niveau dataset, car elles ne distinguent pas les records ;
- une simple « position de qualification » sans règle d'énumération.

La famille qui reste la plus cohérente est :

```text
ACQUISITION-SCOPED PROVENANCE + DETERMINISTIC LOCAL RECORD POSITION
```

Mais cette conclusion ne gèle pas encore une primitive.

Le bloc suivant doit déterminer une seule chose :

> **quelle règle normative permet d'énumérer les records d'un artefact d'acquisition de façon déterministe, sans utiliser cette énumération comme ordre temporel ?**

Cette question est distincte de la portée de stabilité désormais fermée.

**Statut final :**

```text
Q-2 → CLOSED
Q-1 SCOPE → CLOSED
Q-1 CONCRETE ENUMERATION RULE → OPEN
OBSERVATION IDENTITY → BLOCKED
1.1.2 → NOT CLOSED
```
