# DECISION REGISTER — A-11

## A-11 — CANONICAL REPRESENTATION OF TICK ORDER

**Statut : DECISION EXPLICITE — ADOPTÉE**

**Périmètre :** `1.1.2 — DATA NORMALIZATION & OBSERVATION CONTRACT`

**Origine :** adjudication adversariale du finding A-11 identifié dans l'Audit V8.

### Question

Comment représenter de manière canonique l'ordre des observations primaires lorsque l'ordre peut être total, partiel ou inconnu, sans perdre une relation établie ni inventer une relation non établie ?

### Décision

`ordered_ticks` demeure l'unique champ normatif portant la représentation de l'ordre des observations primaires.

Sa sémantique normative est une représentation complète des relations d'ordre établies entre les observations de la barre.

Chaque relation :

```text
[A, B]
```

signifie :

```text
A précède B
```

Toutes les relations d'ordre normativement établies doivent être représentées, y compris leurs conséquences transitives lorsqu'elles sont établies par la relation temporelle normative.

Aucune relation non établie ne peut être ajoutée.

L'absence d'une relation dans `ordered_ticks` ne constitue pas, à elle seule, une preuve d'incomparabilité.

La sérialisation de `ordered_ticks` doit être déterministe selon l'identité stable des observations. L'ordre de sérialisation est purement représentationnel et ne constitue jamais une relation temporelle supplémentaire.

### Rescopage de H-04 et A-08

Les principes suivants de H-04 et A-08 restent applicables :

- conservation de toute relation d'ordre établie ;
- interdiction d'inventer un ordre ;
- conservation explicite de l'incertitude ;
- déterminisme de la représentation ;
- absence d'interprétation temporelle fondée uniquement sur la sérialisation.

En revanche, leur structure spécifique par groupes :

```text
ordered + unordered_groups
```

n'est plus la représentation normative générale de `ordered_ticks` pour `1.1.2`.

Cette structure est donc supersédée, dans ce périmètre, par la représentation canonique décidée par A-11.

Aucun second champ normatif `order_relations` n'est créé. `order_relations` désigne uniquement la sémantique de `ordered_ticks`.

### Justification

La représentation par groupes ne permet pas de représenter sans perte tous les ordres partiels possibles. Elle peut soit perdre une relation établie, soit imposer une structure ne correspondant pas à l'information réellement disponible.

La représentation complète des relations établies évite ces deux défauts tout en conservant l'interdiction d'inventer un ordre.

### Effet

La spécification `1.1.2` doit être corrigée de manière minimale afin que :

1. `ordered_ticks` reste le champ normatif unique ;
2. sa sémantique soit celle des relations d'ordre établies ;
3. H-04/A-08 soient explicitement rescopés quant à leur structure ;
4. `BAR_CLOSED` et `BAR_IN_PROGRESS` utilisent la même sémantique normative de `ordered_ticks`.

Cette décision n'étend pas `1.1.2` à la logique de stratégie ou d'exécution.
