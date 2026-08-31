# ADVERSARIAL CONFORMANCE AUDIT V6 — CIBLÉ REPRÉSENTATIONS

## Statut
AUDIT CIBLÉ — FINDINGS OUVERTS

## Périmètre
Audit du texte réellement enregistré de `1.1.2 V6 — CANDIDATE`, limité aux ambiguïtés de représentation susceptibles de permettre à deux implémentations conformes de produire des représentations normatives différentes.

Aucune correction de V6 n'est appliquée par ce document.

---

## A-08 — Représentation incomplète lorsque l'ordre inter-groupes est UNKNOWN

**Niveau : CRITIQUE**

**Références : §4.3, §6.4, §7.3, Test M**

### Constat
V6 définit `ordered_ticks` comme une séquence de groupes et impose que l'ordre entre groupes soit normativement établi. Elle prévoit ensuite le cas où une relation inter-groupes ne peut pas être établie, mais renvoie alors à « un mécanisme d'incertitude applicable » sans définir la structure normative de ce cas.

### Scénario
Ticks A, B et C appartiennent à la même barre. Les relations A-B et B-C sont inconnues et aucune relation inter-groupes totale ne peut être établie.

Implémentation 1 peut produire un seul groupe `{A,B,C}`.
Implémentation 2 peut produire deux groupes `{A,B}` puis `{C}` avec relation partiellement inconnue.
Implémentation 3 peut utiliser une structure de graphe partiel.

Aucune représentation n'est prescrite pour ce cas.

### Risque
La conformité ne détermine pas une représentation unique de l'incertitude d'ordre. Une couche aval ou un hash de représentation peut donc diverger.

### Statut
OUVERT — nécessite adjudication ou rattachement explicite à une décision existante.

---

## A-09 — Ordre de sérialisation des tick_ids facultatif dans une structure normative

**Niveau : MAJEUR**

**Références : §6.4, §13.3, §16**

### Constat
V6 indique que les identifiants d'un groupe « peuvent être placés dans un ordre canonique de représentation ».

Le terme « peuvent » rend cette canonisation optionnelle.

### Scénario
Deux implémentations représentent le même groupe d'ordre UNKNOWN :

```text
{ tick_ids: [A, B, C] }
```

et :

```text
{ tick_ids: [C, A, B] }
```

Les deux respectent l'absence d'ordre temporel et peuvent considérer l'ordre choisi comme purement représentationnel.

Si cette structure entre dans une trace ou un `result_hash`, les représentations divergent malgré des entrées et une configuration identiques.

### Risque
La distinction entre ordre temporel UNKNOWN et ordre de sérialisation n'est pas suffisamment verrouillée pour les productions normatives sérialisées.

### Statut
OUVERT — nécessite une formulation normative déterminant si et quand la canonisation est obligatoire.

---

## A-10 — `BAR_CLOSED` autorise un schéma minimal sans définir la représentation normative complète

**Niveau : MAJEUR**

**Références : §7.2, §13.3, §16, §17.4**

### Constat
§7.2 impose à `BAR_CLOSED` de conserver « au minimum » neuf champs, puis ajoute que l'identité et la provenance doivent être établissables conformément au mécanisme applicable.

Le contrat ne distingue pas explicitement :

1. les champs obligatoires de la représentation normative ;
2. les champs optionnels non normatifs ;
3. les champs supplémentaires qui deviennent déterminants s'ils sont présents.

### Scénario
Implémentation A expose uniquement les neuf champs minimaux.
Implémentation B expose les neuf champs plus `dataset_id`, `source_record_ids` et `result_hash`.

Si une couche aval ou une comparaison de trace considère la structure complète comme représentation normative, les deux implémentations peuvent diverger tout en respectant le « au minimum ».

### Risque
La frontière entre schéma minimal contractuel et représentation normative comparable n'est pas complètement déterminée.

### Statut
OUVERT — nécessite clarification normative de la portée du schéma minimal.

---

# VERDICT CIBLÉ

`V6` ne peut pas encore être considéré comme exempt d'ambiguïtés de représentation.

Les trois points sont distincts :

- **A-08** porte sur la représentation d'une incertitude d'ordre non totale ;
- **A-09** porte sur la canonisation de la représentation sérialisée ;
- **A-10** porte sur la frontière entre schéma minimal et représentation normative complète.

Aucune modification de V6 n'est autorisée sur la base de ce seul audit : les points doivent d'abord être confrontés aux registres et décisions existants, puis adjud iqués s'ils ne sont pas déjà couverts.

## Prochaine chaîne automatique

```text
A-08 → registres / corpus → adjudication
A-09 → registres / corpus → adjudication
A-10 → registres / corpus → adjudication
        ↓
corrections déterminées
        ↓
V7 si nécessaire
        ↓
audit adversarial complet
```
