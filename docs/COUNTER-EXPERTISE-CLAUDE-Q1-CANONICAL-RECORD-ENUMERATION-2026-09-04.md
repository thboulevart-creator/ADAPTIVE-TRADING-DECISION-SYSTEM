# CONTRE-EXPERTISE CLAUDE — Q1 — ÉNUMÉRATION CANONIQUE DES RECORDS

## Objet

Nous avons maintenant fermé la portée de stabilité de l'identité observationnelle à la **lignée d'acquisition / dataset qualifié**.

La question restante est Q1 : **comment déterminer exactement l'identité individuelle d'un record de manière déterministe, sans transformer la provenance en ordre temporel ?**

Une première élimination adversariale a été réalisée.

### Candidats éliminés ou insuffisants

1. **Position seule dans l'artefact source** : admissible sous conditions, mais insuffisante tant que l'artefact exact, les frontières de records et la règle d'énumération ne sont pas normativement définis.
2. **Position attribuée lors de la qualification** : admissible comme moment d'assignation, mais « attribuée à la qualification » ne définit pas le critère d'énumération.
3. **Identifiant fourni par la source** : non prouvé dans le corpus ; non adoptable comme règle normative sans preuve.
4. **Provenance + position** : famille actuellement la plus solide, mais dépend d'une position locale déterministe.
5. **Autre primitive déjà présente dans le corpus** : aucune primitive individuelle complète n'a été démontrée.

La distinction importante est :

```text
ARTEFACT D'ACQUISITION
        ↓
RÈGLE D'ÉNUMÉRATION DES RECORDS
        ↓
POSITION LOCALE
        ↓
IDENTITÉ OBSERVATIONNELLE
```

avec :

```text
position locale ≠ ordre temporel
position locale ≠ ordre physique
position locale ≠ identité d'un événement de marché
```

## QUESTION À ARBITRER

> **Quelle règle normative peut énumérer les records d'une acquisition de façon déterministe, reproductible et stable, tout en conservant les doublons stricts et sans fabriquer d'ordre temporel ?**

Ne réponds pas simplement « utiliser la position du fichier ». Nous voulons savoir si cette proposition peut être transformée en contrat réellement vérifiable.

---

# CONTRAINTES

Le corpus déjà vérifié impose ou contient notamment :

- conservation des doublons stricts dans le RAW (`V7 §5`) ;
- distinction entre identité du dataset et identité de l'enregistrement source (`V7 §3.1`) ;
- identité stable nécessaire à la canonisation (`H-04`, `A-09`) ;
- `ordered_ticks` reste l'autorité normative pour les relations temporelles établies ;
- aucune relation temporelle non établie ne doit être inventée ;
- la portée de stabilité inter-acquisition n'est pas requise et a été fermée à la lignée d'acquisition ;
- les documents `05`, `09` et `10` actuellement présents ne constituent pas une définition normative complète de l'identité individuelle ;
- le dataset primaire ne doit pas être modifié silencieusement ;
- toute transformation avale produit une représentation traçable et ne doit pas changer l'identité d'une observation existante.

---

# HYPOTHÈSE CANDIDATE À ATTAQUER

Une construction possible est :

```text
observation_identity
    = (acquisition_lineage, source_artifact, local_record_position)
```

avec :

```text
source_artifact
    = identifiant vérifiable de l'artefact exact d'acquisition

local_record_position
    = position attribuée une seule fois selon une règle canonique
      d'énumération des records de cet artefact
```

Une variante plus compacte serait :

```text
observation_identity
    = (qualified_dataset_id, record_position)
```

si `record_position` est déjà défini comme position canonique dans le dataset qualifié.

**Nous ne savons pas encore si cette construction est suffisamment déterministe.**

---

# CAS ADVERSARIAUX

Analyse obligatoirement les cas suivants.

## C1 — un fichier, records clairement délimités

```text
file F
R1
R2
R3
```

La position physique/énumérée est-elle une base suffisante ?

## C2 — même timestamp

```text
R1 t=10
R2 t=10
R3 t=11
```

La règle doit distinguer les records sans leur attribuer un ordre temporel.

## C3 — doublons stricts

```text
R1 = R2
```

Les deux records doivent conserver des identités distinctes.

## C4 — réordonnancement runtime

Même artefact, lecture :

```text
R1 R2 R3
```

puis :

```text
R3 R1 R2
```

Les identités doivent rester inchangées.

## C5 — deux fichiers d'une même acquisition

```text
F1: R1 R2
F2: R3 R4
```

Quelle règle produit une séquence globale déterministe ?

## C6 — deux acquisitions

```text
Acquisition A: F1 F2
Acquisition B: F2 F1
```

Les identités peuvent différer entre acquisitions, conformément à la portée déjà décidée.

Mais dans une même acquisition, quelle règle rend l'énumération déterministe ?

## C7 — partition physique

Un même contenu logique est livré sous forme :

```text
file unique
```

puis :

```text
file A + file B
```

S'agit-il nécessairement du même dataset ?

Si non, explique pourquoi cela ne constitue pas un problème.

## C8 — conversion de format

Même acquisition représentée en CSV puis en binaire.

L'identité doit-elle rester identique ?

Si oui, quel mécanisme le permet sans faire de l'encodage physique une partie de l'identité ?

Si non, explique précisément pourquoi ce changement de format crée une nouvelle lignée.

## C9 — record boundary

Si la frontière entre deux records dépend d'un parser ou d'une convention de format non déclarée, la position est-elle réellement déterministe ?

## C10 — insertion/suppression

Un nouveau record est inséré dans un artefact avant R17.

```text
ancien : R1 ... R16 R17 ...
nouveau : R1 ... R16 RX R17 ...
```

Dans une nouvelle acquisition/lignée, R17 doit-il conserver la même identité ?

Ne suppose pas la réponse : analyse-la.

## C11 — duplication d'artefact

Une copie byte-for-byte de l'artefact est créée.

L'identité doit-elle être la même dans la même lignée ?

## C12 — modification d'un octet

Un octet est modifié mais le record concerné semble économiquement identique.

Que devient l'identité du dataset et des records ?

---

# QUESTION CENTRALE : QU'EST-CE QU'UNE SÉQUENCE CANONIQUE ?

Nous voulons une distinction stricte entre :

```text
canonical enumeration
```

et :

```text
temporal ordering
```

Explique si une séquence canonique peut être fondée sur :

- l'ordre physique du fichier ;
- l'ordre des fichiers dans une acquisition ;
- un offset/ordinal de record ;
- un tri lexical d'une représentation ;
- un hash ;
- timestamp + tie-break ;
- un identifiant source ;
- une règle d'énumération créée lors de la qualification.

Pour chaque possibilité, indique ce qu'elle garantit réellement et ce qu'elle ne garantit pas.

---

# POINT CRITIQUE À VÉRIFIER

Nous soupçonnons que les candidats « position dans l'artefact » et « position attribuée à la qualification » ne sont pas deux solutions indépendantes.

Ils pourraient constituer les deux étapes d'une même construction :

```text
exact acquisition artifact
        ↓
canonical record enumeration
        ↓
position assigned once at qualification
        ↓
(provenance, position)
```

Détermine si cette combinaison est :

- logiquement cohérente ;
- suffisante ;
- déterministe ;
- testable ;
- ou si elle cache encore une décision non résolue.

---

# TESTS OBLIGATOIRES

Évalue la construction candidate contre :

1. même artefact → mêmes identités ;
2. lecture dans un ordre différent → mêmes identités ;
3. doublons stricts → identités distinctes ;
4. timestamps identiques → aucune relation temporelle inventée ;
5. multi-fichier → déterminisme global ;
6. changement de format → comportement explicite ;
7. nouvelle acquisition → nouvelle lignée possible ;
8. modification du contenu → nouvelle identité dataset ;
9. duplication byte-for-byte → comportement déterministe ;
10. sérialisation H-04/A-09 ;
11. reconstruction BAR_IN_PROGRESS → BAR_CLOSED ;
12. dérivation de barres ;
13. redémarrage ;
14. deux implémentations indépendantes.

---

# CLASSIFICATION OBLIGATOIRE

Pour chaque conclusion :

```text
[NORMATIF — MASTER PLAN]
[CONSÉQUENCE NÉCESSAIRE]
[ARCHITECTURE PROPOSÉE]
[OPTION]
[ABSENCE DE PREUVE]
```

Ne transforme pas une architecture raisonnable en exigence normative.

---

# CE QUE NOUS VOULONS À LA FIN

Nous voulons savoir s'il est possible de parvenir à une construction minimale du type :

```text
qualified_dataset_lineage
        +
canonical_local_record_coordinate
        ↓
observation_identity
```

sans introduire de nouveau concept inutile.

Si oui, donne la **règle minimale exacte** permettant de rendre cette construction normative et testable.

La règle doit répondre à :

```text
1. Quel est le domaine d'identité ?
2. Quel artefact est l'entrée normative ?
3. Comment les records sont-ils énumérés ?
4. Quand la position est-elle attribuée ?
5. La position est-elle immutable ?
6. Comment les doublons sont-ils distingués ?
7. Comment plusieurs fichiers sont-ils traités ?
8. Que signifie la position ?
9. Que ne signifie-t-elle jamais ?
10. Que se passe-t-il lors d'une nouvelle acquisition ?
```

---

# RÈGLE DE DÉCISION

Ne cherche pas la solution la plus élégante.

Cherche la solution qui empêche une implémentation de produire deux identités différentes pour le même record dans le même dataset qualifié, ou la même identité pour deux records distincts, tout en empêchant toute confusion entre identité et ordre temporel.

Si une condition nécessaire n'est pas démontrée par le corpus, signale-la explicitement au lieu de l'inventer.

Si la seule manière de fermer Q1 est une nouvelle décision d'architecture, indique précisément laquelle et arrête-toi sur cette adjudication.

Aucun code.
Aucun commit.
Aucune modification du dépôt.
