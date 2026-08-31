# ADVERSARIAL CONFORMANCE AUDIT V7

## Statut
AUDIT — FINDINGS OUVERTS

## Périmètre
Audit du texte réellement enregistré `1.1.2 V7 — CANDIDATE` contre le test central : deux implémentations conformes, mêmes entrées et même configuration normative, peuvent-elles produire des résultats normatifs différents ?

Le présent audit ne modifie pas V7.

---

## A-11 — A-08 ne représente pas tous les ordres partiels entre composants internes

**Niveau : CRITIQUE**

**Références : §6.4, H-04, A-08, Test M**

### Constat
A-08 impose une structure :

```text
ordered: [...]
unordered_groups: [...]
```

Cette structure distingue des groupes entièrement ordonnés dans une séquence et des groupes sans relation d'ordre entre eux. Elle ne représente cependant pas explicitement le cas où plusieurs composants possèdent chacun un ordre interne établi, mais où les relations entre ces composants sont partiellement inconnues.

### Scénario
Quatre ticks A, B, C, D :

- A < B est établi ;
- C < D est établi ;
- aucune relation entre {A,B} et {C,D} n'est établie.

Implémentation 1 peut placer `{A,B}` et `{C,D}` dans `unordered_groups`, mais cette structure ne précise pas que A<B et C<D.

Implémentation 2 peut conserver deux séquences ordonnées séparées et ajouter une relation d'incomparabilité entre elles.

Les deux conservent correctement l'absence d'ordre inter-composants, mais produisent des représentations différentes et la première perd une information d'ordre pourtant établissable.

### Risque
La représentation normative ne couvre pas tous les posets d'ordre partiel. Une implémentation peut perdre ou encoder différemment des relations d'ordre établies tout en prétendant respecter A-08.

### Statut
OUVERT — nécessite adjudication ou décision complémentaire.

---

## A-12 — Le schéma de `BAR_CLOSED` reste ambigu sur l'emplacement de l'identité et de la provenance

**Niveau : MAJEUR**

**Références : §7.2, §3.1, §16, A-10**

### Constat
V7 fixe les neuf champs du noyau `BAR_CLOSED`, mais §7.2 exige également que l'identité et la provenance normative soient établissables. Le contrat ne détermine pas si ces éléments font partie de la représentation normative de la barre, d'une enveloppe externe, ou d'une structure de métadonnées séparée.

### Scénario
Implémentation A représente :

```text
BAR_CLOSED = { noyau + dataset_id + source_record_ids }
```

Implémentation B représente :

```text
BAR_CLOSED = { noyau }
metadata = { dataset_id, source_record_ids }
```

Les deux rendent l'identité et la provenance « établissables », mais la structure observable n'est pas la même. Si la trace ou un consommateur attend la représentation de barre elle-même, les implémentations divergent.

### Risque
La séparation entre noyau, métadonnées de provenance et enveloppe de transport n'est pas normativement définie.

### Statut
OUVERT — nécessite adjudication ou rattachement explicite à un contrat d'identité/provenance existant.

---

## A-13 — `ordered_ticks` n'est pas entièrement défini pour une barre totalement ordonnée

**Niveau : MAJEUR**

**Références : §4.3, §6.4, §7.2, §7.3, Test M**

### Constat
Le schéma A-08 montre `ordered_ticks` avec `ordered` et `unordered_groups`, mais ne précise pas explicitement les règles de représentation lorsque toutes les relations d'ordre sont établies : faut-il utiliser une suite de groupes unitaires, un groupe contenant tous les ticks, ou une autre forme ?

### Scénario
Pour A < B < C, une implémentation produit :

```text
ordered_ticks = {
  ordered: [{tick_ids:[A]}, {tick_ids:[B]}, {tick_ids:[C]}],
  unordered_groups: []
}
```

Une autre produit :

```text
ordered_ticks = {
  ordered: [{tick_ids:[A,B,C]}],
  unordered_groups: []
}
```

Les deux peuvent prétendre représenter exactement le même ordre temporel selon la rédaction actuelle, mais la structure sérialisée diffère.

### Risque
Une représentation normative destinée à la trace ou au hash peut diverger même lorsque l'ordre temporel est entièrement connu.

### Statut
OUVERT — nécessite clarification normative.

---

## A-14 — « champs supplémentaires » de `BAR_CLOSED` et comparabilité normative encore dépendante du protocole

**Niveau : MAJEUR**

**Références : §7.2, §13.2, §13.3, §16, A-10**

### Constat
V7 permet des champs supplémentaires s'ils sont non normatifs ou régis par un contrat/décision applicable. La phrase « lorsqu'un champ supplémentaire est déterminant pour un protocole normatif » renvoie cependant au protocole sans exiger que la classification d'un champ soit déterminée avant la production de la barre.

### Scénario
Implémentation A ajoute `dataset_id` et le classe non normatif.
Implémentation B ajoute le même champ et le classe déterminant pour un protocole de trace différent.

Sans contrat de classification explicite, la même structure physique peut avoir deux statuts normatifs selon le consommateur.

### Risque
La frontière entre extension non normative et extension normative peut rester contextuelle au lieu d'être déterminée à la source.

### Statut
OUVERT — clarification nécessaire sur le moment et l'autorité qui qualifient une extension.

---

# VERDICT

## PARTIAL

V7 intègre correctement les décisions A-08, A-09 et A-10, mais le test central n'est pas encore satisfait sans ambiguïté.

Les findings ouverts sont :

- **A-11 CRITIQUE** — couverture incomplète des ordres partiels composés ;
- **A-12 MAJEUR** — emplacement normatif de l'identité/provenance non fixé ;
- **A-13 MAJEUR** — représentation non canonisée du cas totalement ordonné ;
- **A-14 MAJEUR** — classification des extensions encore dépendante du protocole.

Aucune correction n'est appliquée à V7 par cet audit.

## Prochaine chaîne

```text
A-11 → registres / corpus → adjudication
A-12 → registres / corpus → adjudication
A-13 → registres / corpus → adjudication
A-14 → registres / corpus → adjudication
        ↓
corrections déterminées
        ↓
V8 si nécessaire
        ↓
audit adversarial complet
```
