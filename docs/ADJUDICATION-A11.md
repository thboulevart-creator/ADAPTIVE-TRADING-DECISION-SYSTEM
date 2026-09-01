# A-11 — ADJUDICATION FORMELLE

**Statut : REPORTÉ**  
**Référence :** `AUDIT-ADVERSARIAL-V7.md` — A-11  
**Base corpus :** commit `cb5071f`  
**Portée :** déterminer si le domaine d'entrée permet d'établir que `H-04` est suffisant ou nécessite une extension normative.

## 1. Question

`1.1.1` peut-il légalement produire, comme dataset admissible transmis à `1.1.2`, une séquence d'observations dont les relations d'ordre constituent un ordre partiel non représentable par la structure `H-04` sans perte ni invention ?

## 2. Conclusion

**REPORTÉ.**

Le corpus ne permet ni de démontrer que `1.1.1` peut produire un ordre partiel non stratifié, ni de démontrer qu'il l'exclut. Il est donc interdit de conclure que `H-04` est soit suffisant, soit insuffisant sur cette seule base.

## 3. Constats déterminants

### 3.1 Domaine de `1.1.1`

Le corpus décrit `1.1.1` comme un inventaire documentaire des données : source, actif, timeframe, période, timezone et format. Aucune disposition trouvée ne définit le régime d'ordre des observations, la fusion de sous-séquences ou la combinaison de plusieurs sources.

### 3.2 Contrat d'identité manquant

`V7 §4.1` renvoie à un « contrat d'identité applicable à `1.1.1` » et à une « composition d'identité normative applicable ». Aucun document correspondant n'est présent dans le corpus examiné au commit `cb5071f`.

### 3.3 Critère d'établissement de l'ordre manquant

`V7 §4.3` exige de conserver l'ordre lorsqu'il « peut être établi normativement » et de conserver `order_status = UNKNOWN` lorsqu'il ne peut pas l'être, mais le corpus ne définit pas le critère normatif permettant d'établir cet ordre.

### 3.4 Régime de combinaison de sources manquant

Aucune disposition examinée n'autorise ou n'interdit explicitement la fusion de plusieurs sous-séquences ordonnées ou de plusieurs sources de manière susceptible de produire un ordre partiel non stratifié.

## 4. Capacité réelle de `H-04`

`H-04` définit `ordered_ticks` comme une séquence de groupes d'ordre : l'ordre entre groupes est établi et l'ordre interne d'un groupe est `UNKNOWN`. Cette structure couvre les ordres stratifiés par classes d'équivalence.

Contre-exemple :

```text
A < B
C < D
A ? C
A ? D
B ? C
B ? D
```

Aucune partition ordonnée en groupes ne représente ce cas sans perte ni invention de relations. `H-04` n'est donc pas expressivement complet pour les ordres partiels quelconques.

Ce constat ne suffit toutefois pas à exiger une extension, puisque le corpus ne démontre pas que ce cas peut atteindre `1.1.2`.

## 5. Manques documentaires

- **M-1** — contrat d'identité applicable à `1.1.1` absent/non identifié.
- **M-2** — critère normatif d'établissement de l'ordre absent/non défini. **Déterminant pour la reprise de l'adjudication.**
- **M-3** — régime normatif de combinaison/fusion de sources ou sous-séquences absent/non défini.

## 6. Classification

**REPORT** — aucune extension de `H-04` n'est autorisée sur la seule base de l'existence du contre-exemple conceptuel.

## 7. Obligatoire

Aucune nouvelle exigence normative n'est créée par ce report.

Le finding doit rester ouvert jusqu'à détermination du domaine d'entrée pertinent, avec au minimum levée de `M-2`.

## 8. Interdit

- Conclure que `H-04` est suffisant sans preuve que le flux entrant est confiné à son domaine représentable.
- Conclure que `H-04` est insuffisant sans preuve que le flux entrant peut contenir un ordre non stratifié.
- Étendre `H-04` sans adjudication distincte.
- Restreindre unilatéralement le domaine d'entrée de `1.1.1` depuis `1.1.2`.

## 9. Impact

**V7 : aucun.**  
**H-04 : aucun.**  
**DR-1 → DR-9 : aucun.**  
**R-01 → R-07 : aucun.**

## 10. Condition de reprise

La question A-11 pourra être réouverte lorsque le corpus déterminera le critère d'établissement de l'ordre (`M-2`) et permettra de vérifier si le flux entrant peut ou non produire un ordre partiel non stratifié.

## 11. Décision Register

Cette adjudication est enregistrée comme **REPORT**, et non comme nouvelle décision normative.
