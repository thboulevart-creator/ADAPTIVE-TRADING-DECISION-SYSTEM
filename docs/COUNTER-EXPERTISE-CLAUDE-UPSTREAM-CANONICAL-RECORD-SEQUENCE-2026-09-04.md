# COUNTER-EXPERTISE REQUEST — UPSTREAM CANONICAL RECORD SEQUENCE

## Statut

**EXTERNAL COUNTER-EXPERTISE REQUIRED — CLAUDE**

Ce document constitue le prompt complet à transmettre à Claude pour une contre-expertise architecturale indépendante.

Aucune décision d'architecture ne doit être déduite de ce prompt.

---

# 1. CONTEXTE DU PROJET

Le projet est un moteur algorithmique de trading dont la chaîne de données est :

```text
SOURCE DE DONNÉES
      ↓
DATASET BRUT
      ↓
1.1.1 — DATASET QUALIFICATION
      ↓
DATASET QUALIFIÉ
      ↓
1.1.2 — DATA TRANSFORMATION & TEMPORAL REPRESENTATION
      ↓
REPRÉSENTATIONS DÉRIVÉES
      ↓
STRATEGY ENGINE
```

`1.1.2` repose sur le principe suivant :

> les données primaires restent la source de vérité ; les représentations temporelles sont dérivées, déterministes, causales, traçables et reproductibles.

Le travail actuel porte sur l'identité normative des observations primaires et, plus précisément, sur la possibilité de définir en amont une séquence canonique de records qualifiés permettant une identité stable sans transformer cette séquence en ordre temporel.

---

# 2. ÉTAT ACTUEL — CE QUI EST DÉJÀ ADJUDICÉ

## 2.1 Ownership

La responsabilité normative de définir l'identité individuelle des observations primaires appartient à la frontière amont de `1.1.1` / data-contract, et non à `1.1.2`.

`1.1.2` consomme, conserve et propage cette identité ; il ne doit pas inventer son propre mécanisme d'identité.

Décision : **OI-01 — OWNERSHIP**.

Cette décision ne fixe pas encore la composition concrète de l'identité.

---

## 2.2 Distinction fondamentale

Trois notions doivent rester strictement séparées :

```text
OBSERVATION IDENTITY
    = identité du record primaire individuel

CANONICAL POSITION
    = coordonnée déterministe d'un record dans un dataset qualifié

TEMPORAL ORDER
    = relation temporelle effectivement établie entre observations
```

Il est interdit de déduire :

```text
position(A) < position(B)
```

comme impliquant :

```text
A < B
```

sauf si la relation temporelle est indépendamment établie.

---

## 2.3 `ordered_ticks`

La structure normative retenue pour l'ordre temporel est :

```text
ordered_ticks = {
    observations: [A, B, C],
    relations: [[B, C]]
}
```

`observations` constitue l'univers exact des observations primaires affectées à la barre.

`relations` contient les relations d'ordre effectivement établies, y compris les conséquences transitives lorsqu'elles sont requises par la décision applicable.

Il ne faut jamais créer artificiellement un ordre total lorsque les données n'établissent qu'un ordre partiel.

Une absence de relation ne signifie pas automatiquement une relation physique d'incomparabilité ; elle signifie que cette relation n'est pas établie par la représentation normative.

---

## 2.4 Doublons

Les observations primaires distinctes retenues par le dataset qualifié doivent rester individuellement représentables, même si leurs champs visibles sont identiques.

Donc :

```text
O1 = O2 en contenu visible
```

n'implique pas :

```text
O1 = O2 comme record primaire
```

L'identité d'un record ne doit donc pas être confondue avec une identité de contenu ni avec une éventuelle identité économique de marché.

La question d'une éventuelle `event_identity` économique n'est pas actuellement définie et ne doit pas être inventée.

---

# 3. PROBLÈME ACTUEL

Une option architecturale plausible consiste à utiliser une identité de type :

```text
SOURCE RECORD + STABLE PROVENANCE / POSITIONAL REFERENCE
```

Mais l'audit adversarial a démontré qu'un simple numéro de ligne ou index de collection n'est pas nécessairement stable.

Une position ne pourrait être normative que si une règle amont définissait précisément une **énumération canonique et déterministe des records qualifiés**, avant leur consommation par `1.1.2`.

L'audit actuel a donc laissé ouverte la question :

> **Le contrat amont peut-il définir une énumération canonique des records primaires qualifiés, et si oui selon quelle règle exacte, sans transformer cette énumération en ordre temporel ?**

Cette question est désormais au stade d'adjudication.

---

# 4. ÉTAT DES OPTIONS AUDITÉES

## A — Séquence fournie par la source

Plausible seulement si le fournisseur garantit normativement stabilité, unicité, conservation et reproductibilité de cette séquence.

Cette garantie n'est actuellement pas établie dans le corpus du projet.

Statut : **non prouvé**.

## B — Séquence attribuée par la qualification

La qualification construirait un dataset qualifié immuable et lui attribuerait une énumération canonique déterministe.

Cette famille est architecturally compatible avec les invariants mais ses règles exactes ne sont pas définies.

Statut : **famille plausible, non gelée**.

## C — Énumération d'un artefact immuable

L'artefact qualifié capturé pourrait constituer le domaine normatif et son énumération déterministe pourrait servir de référence.

Cette approche peut fournir une provenance physique forte mais nécessite une définition normative de l'artefact, des limites de records, de l'énumération et de la stabilité.

Statut : **possible, non gelé**.

## Règles génériques rejetées comme insuffisantes

Ne sont pas acceptées seules :

- index de collection runtime ;
- ordre arbitraire du système de fichiers ;
- simple numéro de ligne sans contrat sur l'artefact ;
- tri par contenu seul ;
- tri par timestamp seul ;
- tri temporel utilisé comme substitut d'ordre physique.

---

# 5. CONTRAINTES NON NÉGOCIABLES

Ta contre-expertise doit respecter les contraintes suivantes :

1. ne pas inventer une décision déjà gelée ;
2. ne pas transformer une bonne pratique en exigence normative ;
3. distinguer strictement :
   - exigence normative ;
   - conséquence nécessaire ;
   - choix architectural ;
   - option ;
   - absence de preuve ;
   - question non résolue ;
4. ne pas créer de nouvelle règle temporelle dans `1.1.2` ;
5. ne pas transformer une position canonique en ordre temporel ;
6. préserver les doublons records distincts ;
7. ne pas imposer une identité fondée uniquement sur le contenu ;
8. ne pas supposer que l'ordre de lecture runtime est normatif ;
9. ne pas supposer qu'une réacquisition indépendante doit avoir la même identité sans décision explicite ;
10. ne pas inventer de collision handling concret si le corpus ne le permet pas ;
11. considérer que l'absence actuelle d'un mécanisme d'identité concret est une **absence de preuve**, pas une autorisation d'inventer un mécanisme dans `1.1.2`.

---

# 6. QUESTIONS D'ADJUDICATION

Analyse indépendamment les questions suivantes.

## Q-S1 — Ownership

La définition de l'identité individuelle des observations doit-elle être possédée par la couche amont de qualification plutôt que par `1.1.2` ?

Si oui, est-ce une conséquence nécessaire des frontières actuelles ou une nouvelle décision ?

## Q-S2 — Scope

Quel est le domaine exact sur lequel une éventuelle identité/position serait définie ?

Possibilités à analyser :

- dataset qualifié versionné ;
- flux source ;
- lignée de dataset ;
- autre.

Ne choisis pas une option simplement parce qu'elle semble pratique.

## Q-S3 — Membership

Qu'est-ce qui définit exactement qu'un record appartient au dataset qualifié ?

Comment la frontière de qualification affecte-t-elle l'identité ?

## Q-S4 — Enumeration

Est-il possible de définir une énumération canonique des records qualifiés qui soit :

- déterministe ;
- reproductible ;
- indépendante du runtime ;
- indépendante du parallélisme ;
- indépendante de l'ordre de lecture accidentel ;
- stable pendant la consommation par `1.1.2` ;
- distincte de l'ordre temporel ?

Si oui, quelles propriétés minimales cette règle doit-elle avoir ?

## Q-S5 — Duplicate records

Si deux records distincts sont conservés par la qualification mais ont exactement le même contenu visible, doivent-ils recevoir deux identités distinctes ?

Explique les conséquences pour toute identité positionnelle ou composite.

## Q-S6 — Equal timestamps

Comment traiter deux observations ayant exactement le même timestamp lorsque leur ordre physique n'est pas établi ?

Une énumération canonique peut-elle les distinguer sans prétendre établir une relation temporelle entre elles ?

## Q-S7 — Multi-file / multi-source

Si un dataset qualifié provient de plusieurs fichiers ou de plusieurs fragments d'une même source, une énumération globale peut-elle être normative ?

Quelles conditions seraient nécessaires pour éviter que la concaténation arbitraire des fichiers ne modifie l'identité ?

## Q-S8 — Version change

Que doit-il se passer si le dataset qualifié change de version :

- insertion d'un record ;
- suppression ;
- correction ;
- remplacement de fichier ;
- modification de qualification ?

Une identité doit-elle rester stable entre versions, ou cette propriété nécessite-t-elle une décision distincte ?

Ne suppose pas la réponse.

## Q-S9 — Re-acquisition

Deux acquisitions indépendantes du même flux fournisseur doivent-elles nécessairement produire les mêmes identités ?

Distingue :

```text
même contenu
```

et :

```text
même record/provenance
```

Indique clairement si cette question est actuellement décidée ou doit rester ouverte.

## Q-S10 — Propagation

Une identité définie en amont doit-elle rester inchangée à travers :

```text
QUALIFIED DATASET
→ 1.1.2
→ BAR_IN_PROGRESS
→ BAR_CLOSED
→ DERIVED REPRESENTATION
```

Si oui, est-ce une conséquence nécessaire de la traçabilité déjà normative ?

## Q-S11 — Independence from temporal order

Peut-on définir une position canonique sans créer implicitement un ordre temporel artificiel ?

Analyse notamment le cas :

```text
position(A) < position(B)
```

alors que :

```text
A < B
```

n'est pas établi.

---

# 7. TESTS ADVERSARIAUX À ÉVALUER

Évalue si les tests suivants suffisent et lesquels sont manquants :

### P-TEST-1 — Traversal permutation

Même dataset qualifié, parcouru dans des ordres runtime différents.

Résultat attendu : même identité normative pour chaque record.

### P-TEST-2 — Runtime collection reorder

Réordonner artificiellement la collection en mémoire après qualification.

Résultat attendu : aucune modification d'identité.

### P-TEST-3 — Strict duplicate records

Deux records distincts avec contenu visible identique.

Résultat attendu : distinction conservée.

### P-TEST-4 — Preceding insertion

Insérer un record avant un autre.

Déterminer si l'identité du record existant doit rester stable entre versions. Ne pas présumer la réponse : vérifier si cela nécessite une décision.

### P-TEST-5 — Re-acquisition

Acquérir à nouveau le même périmètre de données.

Tester séparément : même contenu, même provenance, même dataset version.

### P-TEST-6 — Multi-file combination

Partitionner/recombiner les fichiers sources sans modifier le contenu qualifié.

Vérifier si l'identité reste déterministe selon le contrat retenu.

### P-TEST-7 — Equal timestamp

Plusieurs observations au même timestamp.

Vérifier qu'aucun ordre temporel artificiel n'est créé.

---

# 8. FORMAT DE TA RÉPONSE

Tu dois être adversarial et chercher à casser les hypothèses.

Commence par :

```text
VERDICT — CANONICAL RECORD SEQUENCE
→ ACCEPTABLE
→ PARTIEL
→ INSUFFISANT
→ BLOQUÉ
```

Puis :

## 1. Findings critiques

Pour chaque finding :

```text
ID :
Problème :
Pourquoi c'est critique :
Scénario d'échec :
Décision/invariant concerné :
Classification :
Correction/adjudication nécessaire :
```

## 2. Findings majeurs

Même format.

## 3. Findings mineurs

Même format.

## 4. Adjudications recommandées

Pour Q-S1 à Q-S11, indiquer :

```text
Q-Sx :
État actuel :
Conclusion proposée :
Justification :
Ce qui est nécessaire :
Ce qui resterait une décision séparée :
```

## 5. Tests supplémentaires

Lister les tests qui manquent pour rendre la décision falsifiable.

## 6. Risque de faux sentiment de sécurité

Identifier les formulations qui pourraient sembler suffisamment précises tout en permettant plusieurs implémentations incompatibles.

## 7. Conclusion

Répondre explicitement :

> Une séquence canonique de records peut-elle être définie en amont sans introduire d'ordre temporel artificiel ?

Et surtout :

- ne décide pas à la place du projet si une décision humaine est nécessaire ;
- signale toute question qui doit rester ouverte ;
- ne propose pas de modifier `1.1.2` tant que les décisions amont ne sont pas explicitement adjudicées.

---

# 9. RAPPEL MÉTHODOLOGIQUE

Le but de cette contre-expertise n'est ni de prouver que l'architecture actuelle est correcte ni de démontrer qu'elle est incorrecte.

Le but est de déterminer, à partir des contraintes et des preuves disponibles, quelles propositions sont réellement nécessaires, lesquelles sont seulement plausibles, et où subsiste une ambiguïté susceptible de produire deux implémentations divergentes.

Une recommandation de Claude ne constitue pas automatiquement une décision normative du projet.

La décision sera prise séparément après confrontation des preuves et de la contre-expertise.

## FIN DU PROMPT DE CONTRE-EXPERTISE
