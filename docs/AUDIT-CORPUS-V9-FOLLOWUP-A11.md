# AUDIT CORPUS — V9 FOLLOW-UP

## Verdict du bloc

```text
AUDIT CORPUS : EXECUTÉ
ADJUDICATION : PARTIELLE
```

Le corpus de référence permet de fermer les questions 1, 2, 3 et 5. Il ne permet pas de fermer normativement la politique de tick arrivant tardivement.

## 1 — Ticks isolés

**Résultat : ACCEPTÉ.**

La conservation des observations primaires et l'unicité de `ordered_ticks` imposent de représenter, dans ce champ unique, à la fois l'univers des observations de la barre et les relations d'ordre établies.

Forme conceptuelle décidée :

```text
ordered_ticks = {
  observations: [A, B, C],
  relations: [[B, C]]
}
```

Un tick sans relation reste donc identifiable sans que l'absence de relation soit interprétée comme une relation temporelle.

**Statut : [CONSÉQUENCE NÉCESSAIRE]**

## 2 — Canonisation

**Résultat : ACCEPTÉ.**

La canonisation doit imposer une occurrence unique des identités et relations, un ordre déterministe fondé sur les identités stables, une orientation sémantique `[A,B] = A précède B`, l'absence de doublons/inversions et l'absence d'interprétation temporelle de l'ordre de sérialisation.

**Statut : [CONSÉQUENCE NÉCESSAIRE]**

## 3 — Contraintes structurelles

**Résultat : ACCEPTÉ.**

La représentation normative doit rejeter les identités hors univers, doublons, relations vers des identités absentes, auto-relations, inversions simultanées, cycles de précédence, relations vers une autre barre et toute relation ajoutée pour fabriquer artificiellement un ordre total.

**Statut : [CONSÉQUENCE NÉCESSAIRE]**

## 4 — Ticks tardifs

**Résultat : NON RÉSOLU.**

La recherche du corpus ne révèle aucune décision gelée fermant explicitement le traitement d'un tick reçu après la clôture alors que son `event_time` appartient à une période antérieure.

Les invariants existants imposent néanmoins :

- `event_time` est le temps canonique de partition ;
- aucune information future ne peut influencer une représentation déjà observable ;
- une représentation déjà exposée ne peut pas être silencieusement réécrite ;
- le dataset primaire reste immuable.

Ils ne permettent pas de choisir entre rejet, différé, backfill/nouvelle version ou autre politique.

**Statut : [QUESTION NON RÉSOLUE / REPORTÉE]**

## 5 — Causalité par extension future

**Résultat : ACCEPTÉ.**

Le principe causal doit être rendu falsifiable par un test explicite comparant :

```text
RUN-A : Data ≤ t
RUN-B : Data ≤ t + futur
```

et exigeant l'identité des productions normatives jusqu'à `t`, avec isolation des caches, artefacts et états dérivés.

**Statut : [CONSÉQUENCE NÉCESSAIRE]**

## Conclusion

Aucune correction V10 n'est effectuée dans cet artefact.

```text
QUESTIONS 1/2/3/5 = FERMÉES POUR CORRECTION
QUESTION 4        = REPORTÉE
V9                = CANDIDATE
V10               = NON CRÉÉ
```
