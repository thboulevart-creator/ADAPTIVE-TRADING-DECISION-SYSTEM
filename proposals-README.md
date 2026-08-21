# Propositions en cours d'arbitrage

**Aucun document de ce dossier n'est en vigueur.**

Ces documents sont des propositions soumises à audit et arbitrage. Ils ne font pas partie du protocole
tant qu'ils n'ont pas été validés et déplacés dans `docs/`.

---

## Contexte

Le 20 août 2026, la stratégie **Sweep + MSS NAS100** a été invalidée. Son rapport v3 annonçait un SQN
hors échantillon de 2,50 ; sur données réellement continues, ce SQN vaut 0,27.

**Cause :** le jeu de données de recherche était un extrait par fenêtres — 60 barres avant chaque
signal, 300 après. Le moteur parcourant les barres par index et non par horodatage, 47 % des
transactions poursuivaient leur simulation sur les barres d'un autre signal, parfois plusieurs jours
plus tard. Ces transactions corrompues portaient la totalité du résultat annoncé.

Un audit du socle a établi qu'**aucune règle du protocole d'alors n'aurait permis de détecter cet
artefact**. Ces propositions visent à combler cette lacune avant toute nouvelle recherche.

Dépôt de l'invalidation : `sweep-mss-nas100`

---

## Documents soumis

| Document | Objet | Statut |
|---|---|---|
| `04-VALIDATION-CRITERIA-v0.1-PROPOSITION.md` | Ce qui constitue une preuve suffisante | PROPOSÉ |
| `05-DATA-CONTRACT-v0.1-PROPOSITION.md` | Conditions de validité d'un jeu de données | PROPOSÉ |
| `DIFF-PROPOSE-00-MASTER-EXECUTION-CHECKLIST.md` | Neuf modifications isolées de la checklist | PROPOSÉ |

---

## Convention de statut employée

| Statut | Signification |
|---|---|
| **NORMATIF** | Règle méthodologique universelle ou dérivation mathématique. Verrouillable immédiatement. Ne dépend d'aucune préférence. |
| **PARAMÈTRE À DÉCIDER** | Valeur dépendant de la philosophie de recherche ou de la tolérance au risque. La méthode de détermination est proposée, jamais la valeur. |
| **RECOMMANDATION** | Aide à la décision, non contraignante. |

**Un nombre au statut NORMATIF résulte d'un calcul reproductible. Un nombre au statut PARAMÈTRE À
DÉCIDER est un exemple d'illustration, jamais une valeur adoptée.**

---

## Points appelant particulièrement l'audit

**`04` §2.3 — la correction pour tests multiples n'aurait pas suffi.** Avec 7 400 combinaisons
évaluées, le seuil de Bonferroni valait 4,35 ; la configuration retenue affichait 5,04 en conception.
Elle aurait franchi le seuil. Ce constat est écrit dans le document plutôt que dissimulé : la règle est
nécessaire mais non suffisante.

**`04` §5.3 — un critère de dégradation relative est manipulable.** Sur données propres, l'espérance
passait de +0,045 à +0,023 R, soit 49 % de dégradation — apparemment comparable aux 36 % annoncés sur
données corrompues, alors que les niveaux absolus n'ont rien de commun. Un critère relatif doit être
conditionné à un niveau absolu minimal.

**`05` §3.2 — la déclaration des limites d'usage est le maillon décisif.** Identifier un jeu transformé
ne suffit pas si sa condition de validité n'est écrite nulle part. Dans le cas de Sweep + MSS, la limite
« transactions strictement inférieures à 220 barres » n'existait que dans l'intention de celui qui
avait dimensionné la fenêtre.

**`DIFF` D8 — arbitrage de périmètre non tranché.** L'analyse multi-horizon figure dans la vision
`01` mais n'apparaît dans aucune phase de la checklist. Deux options sont présentées sans
recommandation : l'intégrer, ou la déclarer hors périmètre V1.

---

## Ce que ces documents ne contiennent pas

- aucune valeur numérique de décision ;
- aucune suppression de phase ou d'étape existante ;
- aucune modification des documents `01`, `02` et `03` ;
- aucun changement de la doctrine du projet.

---

## Correction technique appliquée séparément

`docs/00-MASTER-EXECUTION-CHECKLIST.md` présentait un BOM UTF-8 et un double encodage
**cp1252 → UTF-8**, produisant 422 occurrences de caractères corrompus — « PHASE 1 — DONNÃ‰ES ».

Le fichier a été réenregistré en UTF-8 sans BOM. **Contenu strictement identique, seul l'encodage
change.** Cette correction relève de la maintenance technique et non d'un arbitrage méthodologique.

---

## Suite du processus

```
Propositions déposées          ← état actuel
        ↓
Audit méthodologique
        ↓
Arbitrage : validation, modification ou rejet, document par document
        ↓
Arbitrage des paramètres ouverts (04 §8 — neuf paramètres)
        ↓
Déplacement des documents validés vers docs/
        ↓
Application des modifications retenues à la checklist
        ↓
Levée du gel sur la recherche
```

**La recherche de nouvelles stratégies est gelée jusqu'à la fin de ce processus.**
