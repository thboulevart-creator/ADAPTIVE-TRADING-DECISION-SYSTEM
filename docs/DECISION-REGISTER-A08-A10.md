# DECISION REGISTER — A-08 / A-09 / A-10

**Version:** 0.1
**Date:** 2026-08-31
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
**Status:** FROZEN
**Source:** `AUDIT-ADVERSARIAL-V6-REPRESENTATION-AMBIGUITIES.md`
**Scope:** adjudication ciblée des ambiguïtés de représentation A-08 à A-10.

> Aucune décision existante n'est réinterprétée au-delà de son périmètre. Lorsqu'un point est déjà couvert par une décision gelée, il est traité comme correction de conformité et non comme nouvelle décision.

---

## A-08 — Représentation lorsque l'ordre inter-groupes lui-même est inconnu

### 1. Question

Comment représenter normativement une barre lorsque certaines relations d'ordre entre ticks sont inconnues et qu'il n'est pas possible d'établir un ordre total entre les groupes, sans inventer une relation temporelle et sans laisser plusieurs structures concurrentes être conformes ?

### 2. Finding

V6 définit une séquence de groupes dans `ordered_ticks`, mais exige ensuite que l'ordre entre groupes soit établi et renvoie, si ce n'est pas possible, à un mécanisme d'incertitude non défini. Cette formulation laisse plusieurs représentations possibles.

### 3. Éléments du corpus / registres

- H-04 FROZEN : impose une séquence de groupes et interdit d'inventer l'ordre interne ; la canonisation interne est représentationnelle.
- V6 §4.3 : `UNKNOWN` doit être conservé.
- V6 §6.4 : `ordered_ticks` est une production normative.
- V6 §2.2 : un comportement déterminant ne peut rester implicite.
- Aucun document existant retrouvé ne définit une structure supplémentaire pour le cas où l'ordre entre groupes est lui-même partiellement inconnu.

### 4. Options

**A — Fusionner tout élément sans ordre total dans un seul groupe.**

**B — Autoriser une structure de graphe/poset d'ordre partiel.**

**C — Ajouter un niveau explicite de groupes non ordonnés entre eux.**

**D — Report.**

### 5. Décision retenue

**A-08 : OPTION C — STRUCTURE EXPLICITE D'INCERTITUDE INTER-GROUPES.**

`ordered_ticks` doit représenter l'ordre connu sans fabriquer un ordre inconnu. Lorsque plusieurs groupes existent mais qu'une relation temporelle entre eux ne peut pas être établie, ils doivent être placés dans une structure explicite de niveau d'incertitude, et non dans une séquence qui impliquerait leur ordre.

La forme normative retenue est :

```text
ordered_ticks = {
  ordered: [
    { tick_ids: [...] },
    { tick_ids: [...] }
  ],
  unordered_groups: [
    { tick_ids: [...] },
    { tick_ids: [...] }
  ]
}
```

`ordered` ne contient que des groupes dont la relation d'ordre est établie. `unordered_groups` contient des groupes entre lesquels aucune relation d'ordre normative n'est établie. L'ordre interne de chaque groupe reste `UNKNOWN` lorsqu'il n'est pas établi et sa sérialisation utilise l'ordre canonique fondé sur l'identité stable, sans signification temporelle.

Cette structure est la seule représentation normative de ce cas.

### 6. Autorisations / interdictions

**Autorisé :** représenter des groupes partiellement ordonnés ; conserver explicitement l'absence de relation ; canoniser uniquement la représentation interne des groupes.

**Interdit :** fusionner arbitrairement des groupes distincts uniquement pour obtenir une liste ; utiliser leur position dans une liste comme preuve d'ordre ; utiliser un graphe libre ou une autre structure non définie comme représentation normative.

### 7. Report

Aucun report sur la structure. Une future sémantique plus fine des relations d'ordre nécessitera une nouvelle décision.

### 8. Statut

**ARBITRATED — FROZEN**

---

## A-09 — Canonisation des `tick_ids`

### 1. Question

La canonisation de l'ordre de sérialisation des identifiants à l'intérieur d'un groupe UNKNOWN doit-elle être facultative ?

### 2. Finding

V6 emploie « peuvent être placés dans un ordre canonique », alors que H-04 FROZEN impose une sérialisation canonique afin d'éviter une divergence représentationnelle.

### 3. Éléments du corpus / registres

- H-04 FROZEN : « les identifiants à l'intérieur d'un groupe doivent être sérialisés selon un ordre canonique de représentation fondé sur l'identité stable du tick ».
- V6 §6.4 : formulation affaiblie par « peuvent ».
- V6 §13.3 / §16 : la représentation peut entrer dans la trace et la traçabilité.

### 4. Classification

**A-09 : DÉJÀ COUVERT PAR H-04 — RÉGRESSION RÉDACTIONNELLE.**

Aucune nouvelle décision n'est créée.

### 5. Correction déterminée

Remplacer la formulation permissive par l'obligation déjà gelée :

```text
Lors de la sérialisation, les identifiants d'un groupe doivent être placés
selon l'ordre canonique de représentation fondé sur l'identité stable du tick.
Cet ordre est purement représentationnel et ne constitue jamais un ordre temporel.
```

### 6. Autorisations / interdictions

**Autorisé :** utiliser l'identité stable uniquement pour canoniser la représentation sérialisée.

**Interdit :** choisir librement l'ordre de sérialisation ; interpréter cet ordre comme une relation temporelle.

### 7. Report

Aucun.

### 8. Statut

**COVERED BY H-04 — CORRECTION RÉDACTIONNELLE — FROZEN**

---

## A-10 — Portée normative du schéma `BAR_CLOSED`

### 1. Question

Le « au minimum » de §7.2 permet-il à deux implémentations de produire des structures normatives différentes en ajoutant librement des champs supplémentaires ?

### 2. Finding

V6 impose neuf champs minimaux mais ne distingue pas les champs constitutifs de la représentation normative, les métadonnées optionnelles et les extensions non normatives.

### 3. Éléments du corpus / registres

- T-05 : schéma de `BAR_CLOSED` explicitement défini, avec conservation de `ordered_ticks`.
- V6 §7.2 : neuf champs imposés « au minimum ».
- V6 §3.1 / §16 : identité, provenance et hash peuvent être requis par les protocoles correspondants.
- V6 §2.2 : une différence de représentation déterminante ne peut rester implicite.
- Aucun registre existant retrouvé ne définit la frontière normative entre les neuf champs du schéma de barre et des extensions supplémentaires.

### 4. Options

**A — Les neuf champs constituent le schéma normatif exact ; aucun champ supplémentaire n'est autorisé.**

**B — Les neuf champs constituent le noyau obligatoire ; les extensions sont autorisées mais doivent être explicitement qualifiées non normatives et ne peuvent entrer dans une comparaison normative sans contrat additionnel.**

**C — Toute extension présente devient automatiquement normative.**

**D — Report.**

### 5. Décision retenue

**A-10 : OPTION B — NOYAU NORMATIF FIXE + EXTENSIONS EXPLICITEMENT QUALIFIÉES.**

Les neuf champs de §7.2 constituent le **noyau obligatoire de la représentation normative `BAR_CLOSED`**. Des champs supplémentaires peuvent exister uniquement comme extensions explicitement qualifiées comme non normatives ou comme champs régis par un contrat/décision applicable.

Un champ supplémentaire ne devient pas normatif simplement parce qu'il est présent. À l'inverse, un champ déterminant pour un protocole donné doit être couvert par ce protocole et sa présence/valeur doit être déterminée normativement.

La comparaison de conformité du schéma de base porte obligatoirement sur le noyau fixé. Les extensions normatives éventuelles doivent être identifiées et régies explicitement avant de participer à une comparaison normative ou à un hash normatif correspondant.

### 6. Autorisations / interdictions

**Autorisé :** ajouter des métadonnées explicitement non normatives ; ajouter des champs normatifs uniquement lorsqu'ils sont couverts par un contrat ou une décision applicable.

**Interdit :** considérer une extension libre comme partie du schéma normatif sans qualification ; utiliser une extension non normativement définie pour produire une divergence de conformité ; exiger d'une autre implémentation un champ qui n'est pas dans le noyau ou dans un contrat applicable.

### 7. Report

Aucun report sur le noyau. La définition de champs supplémentaires spécifiques reste soumise à leurs contrats/protocoles respectifs.

### 8. Statut

**ARBITRATED — FROZEN**

---

# État final

| Finding | Classification | Décision | Statut |
|---|---|---|---|
| A-08 | Nouvelle décision | Structure explicite d'incertitude inter-groupes | FROZEN |
| A-09 | Déjà couvert | H-04 ; correction rédactionnelle | FROZEN |
| A-10 | Nouvelle décision | Noyau normatif fixe + extensions qualifiées | FROZEN |

Ces décisions doivent être intégrées dans la prochaine version de `1.1.2` avant nouvel audit adversarial complet.

**Aucune autre règle normative n'est créée par ce registre.**
