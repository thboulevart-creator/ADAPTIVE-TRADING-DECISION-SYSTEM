# ADJUDICATION — A-01 → A-07 — `1.1.2 V5`

**Date:** 2026-08-31  
**Source:** nouvel Adversarial Conformance Audit réalisé sur le texte intégral de `1.1.2 V5` fourni dans la conversation.  
**Important:** A-01 → A-07 ne sont pas un ancien registre retrouvé ; ce sont les findings du présent audit.

## A-01 — Hiérarchie des sources déterminantes

**Finding:** risque supposé de divergence lorsque plusieurs sources donnent une valeur différente à un paramètre déterminant.

**Confrontation:** H-02 impose déjà que tout paramètre dont la variation peut modifier un résultat normatif soit déterminé normativement. Deux valeurs différentes constituent donc des configurations normatives différentes ; une valeur environnementale utilisée à la place d'une valeur normative viole H-02.

**Décision:** `DÉJÀ COUVERT — H-02`.

**Effet:** aucune nouvelle règle de hiérarchie n'est nécessaire pour fermer ce finding. Une future implémentation doit néanmoins identifier sans ambiguïté la valeur normative applicable.

---

## A-02 — `ordered_ticks` et groupes UNKNOWN

**Finding:** risque supposé de divergence si la relation d'ordre entre groupes était elle-même inconnue.

**Confrontation:** H-04 a explicitement retenu une séquence de groupes d'ordre et impose que l'ordre entre groupes soit normativement établi, tandis que l'ordre interne d'un groupe reste UNKNOWN. Le cas d'une relation inter-groupes non établissable ne peut donc pas être librement représenté par plusieurs implémentations conformes : il est hors de la structure normative retenue et doit rester non ordonné plutôt que d'être inventé.

**Décision:** `DÉJÀ COUVERT — H-04`, avec clarification rédactionnelle possible dans V6 pour rendre l'impossibilité d'un ordre inter-groupes explicitement bloquante plutôt que seulement implicite.

**Effet:** aucune nouvelle décision normative requise.

---

## A-03 — Identité normative de `BAR_CLOSED`

**Finding:** `BAR_CLOSED` exige que l'identité et la provenance soient établissables sans définir explicitement leur composition.

**Confrontation:** le registre de provenance `09` définit l'identité stable des datasets et la traçabilité des transformations, mais ne définit pas une identité normative de barre. V5 distingue correctement les identités dataset/source/dérivée/résultat, sans spécifier la composition de l'identité de `BAR_CLOSED`.

**Décision:** `CORRECTION RÉDACTIONNELLE` si V5 renvoie explicitement à un mécanisme d'identité déjà applicable ; à défaut, ce point devient une `NOUVELLE DÉCISION` avant fermeture normative de l'identité de barre.

**Effet V6:** supprimer l'ambiguïté sans choisir silencieusement une nouvelle formule d'identité.

---

## A-04 — Politique des périodes sans données

**Finding:** V5 renvoie à la politique normative applicable sans définir cette politique dans `1.1.2`.

**Confrontation:** T-03 a précisément supprimé le choix arbitraire entre série creuse et série continue. V5 §9–§10 respecte cette contrainte : aucune politique nouvelle n'est inventée. Les documents disponibles ne fournissent pas ici une décision propriétaire identifiée qui fixe une politique universelle pour toutes les séries.

**Décision:** `REPORT` — dépendance externe à une politique normative de série lorsqu'elle est nécessaire.

**Effet:** aucune nouvelle règle ne doit être inventée dans V6. Si une série ciblée requiert une politique et qu'aucune décision applicable n'existe, cette décision doit être créée avant son implémentation normative.

---

## A-05 — Couverture incomplète du Test N

**Finding:** Test N ne reprend pas explicitement toutes les dimensions interdites par §2.2.

**Décision:** `CORRECTION RÉDACTIONNELLE / TEST`.

**Effet V6:** Test N couvrira explicitement ordre d'itération, version pertinente et comportement de plateforme pertinent, en plus des dimensions déjà citées.

---

## A-06 — Égalité de l'état observable

**Finding:** le mécanisme d'égalité utilisé par Test O n'est pas défini.

**Décision:** `CORRECTION RÉDACTIONNELLE / TEST`.

**Effet V6:** comparer les productions normatives selon une représentation/canonisation normative déterminée ; ne jamais utiliser un ordre de sérialisation comme ordre temporel.

---

## A-07 — Checkpoints de comparaison de trace

**Finding:** Test K ne définit pas explicitement les points normatifs de comparaison.

**Décision:** `CORRECTION RÉDACTIONNELLE / TEST`.

**Effet V6:** les checkpoints porteront sur les états et productions normatifs observables ; les détails internes non normatifs restent hors comparaison.

---

# Synthèse

| Finding | Décision |
|---|---|
| A-01 | DÉJÀ COUVERT — H-02 |
| A-02 | DÉJÀ COUVERT — H-04 |
| A-03 | CORRECTION RÉDACTIONNELLE ; nouvelle décision seulement si aucune identité de barre applicable n'existe |
| A-04 | REPORT |
| A-05 | CORRECTION RÉDACTIONNELLE / TEST |
| A-06 | CORRECTION RÉDACTIONNELLE / TEST |
| A-07 | CORRECTION RÉDACTIONNELLE / TEST |

**Conclusion:** aucune nouvelle décision normative n'est créée par cette adjudication. V5 peut évoluer vers une V6 de correction sans réouvrir H-02/H-04. A-04 reste explicitement reporté et ne doit pas être résolu par invention.
