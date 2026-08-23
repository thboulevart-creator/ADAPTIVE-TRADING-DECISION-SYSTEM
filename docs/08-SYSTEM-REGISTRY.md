# 08 — SYSTEM REGISTRY

**Version:** 0.2 — FACTUAL REGISTRY / PROVISIONAL  
**Date:** 23 août 2026  
**Status:** cartographie structurée issue des documents existants ; aucune nouvelle règle normative n'est créée ici.  
**Purpose:** rendre explicites les concepts, propriétaires, producteurs, dépositaires, consommateurs et interfaces déjà observables dans le système.

---

## 0. Règle de lecture

Ce registre ne redéfinit aucun concept de `04` ou `05`.

Il distingue obligatoirement :

- **Définiteur** — document autorisé à définir la sémantique du concept.
- **Définiteur proposé** — document qui porte une définition candidate mais dont l'autorité normative n'est pas en vigueur.
- **Producteur** — composant qui calcule ou produit la valeur.
- **Dépositaire** — emplacement faisant foi pour la valeur ou l'enregistrement.
- **Consommateur** — composant qui utilise le concept.

**Principe :** produire une donnée ne donne jamais le droit d'en redéfinir la sémantique.

**Règle de statut ajoutée pour lever CTR-02 :** lorsqu'un document source est explicitement indiqué comme proposition/non validé, son rôle dans ce registre est enregistré comme **Définiteur proposé**, jamais comme autorité normative en vigueur. Une telle inscription ne crée aucune règle normative et ne permet pas à elle seule l'application opérationnelle du concept.

---

# 1. Documents actuellement cartographiés

| ID | Document | Version | Statut observé | Autorité |
|---|---|---|---|---|
| DOC-04 | `04-VALIDATION-CRITERIA.md` | 0.6.1 | Candidat au gel / référence méthodologique | Haute |
| DOC-05 | `05-DATA-CONTRACT.md` | 0.1 | Proposition, non validée | Aucune règle en vigueur |

`04` indique explicitement ses interfaces inter-documents au §9. `05` indique explicitement qu'il est soumis à arbitrage et qu'aucune de ses règles n'est actuellement en vigueur.

---

# 2. Ownership Registry — concepts

| Concept ID | Concept | Définition / propriété | Producteur | Dépositaire | Consommateurs | Statut |
|---|---|---|---|---|---|---|
| CON-001 | Niveau de preuve N0–N4 | `04 §7` | Validation / promotion | Registre de recherche / journal de décision à définir | Recherche, décision de capital | Défini dans 04 |
| CON-002 | Statut probatoire du juge | `04 §4.1–4.3` | Procédure de consultation / juge | Registre `04 §4.6` | Promotion / validation | Défini dans 04 |
| CON-003 | Conditions de validation / promotion | `04 §5.1–5.6` | Contrôles de validation | Registre de recherche | Promotion | Défini dans 04 |
| CON-004 | `N_budget` | `04 §2.A` | Plan de recherche | Charte / registre de recherche | Tests confirmatoires | Défini dans 04 |
| CON-005 | `N_famille` | `04 §2.B.1` | Famille de recherche | Registre de famille | Correction de multiplicité | Défini dans 04 |
| CON-006 | Continuité temporelle | `05 §1` | Contrôle qualité des données | Rapport de couverture / dataset | Moteurs de recherche | **Défini proposé dans 05 — non normatif en vigueur** |
| CON-007 | Rapport de couverture | `05 §2` | Pipeline de contrôle qualité | Livrable attaché au résultat | Validation / audit | **Défini proposé dans 05 — non normatif en vigueur** |
| CON-008 | Identité d'un jeu de données | `05 §3` | Pipeline de transformation / acquisition | Registry de datasets à créer | Moteurs / recherche | **Défini proposé dans 05 — non normatif en vigueur** |
| CON-009 | Parenté d'un dataset | `05 §3.3` | Pipeline de transformation | Registry de datasets à créer | Audit / reproductibilité | **Défini proposé dans 05 — non normatif en vigueur** |
| CON-010 | Convention temporelle par instrument | `05 §4` | Asset Profile / gouvernance instrument | Asset Profile | Tous moteurs | **Défini proposé dans 05 — non normatif en vigueur** |
| CON-011 | Parité entre implémentations | `05 §5` | Procédure de parité | Rapport de parité | Recherche / validation | **Défini proposé dans 05 — non normatif en vigueur** |
| CON-012 | Format canonique de série | `05 §6.1` | Gouvernance technique | Contrat de données | Tous moteurs | **Choix proposé dans 05 — non normatif en vigueur** |
| CON-013 | Modèle de coûts par instrument | `05 §7` | Asset Profile / gouvernance instrument | Asset Profile | Recherche / validation / exécution | **Défini proposé dans 05 — non normatif en vigueur** |

**Clarification CTR-02 :** les huit concepts CON-006 à CON-013 ne sont pas enregistrés comme ayant `05` pour autorité normative en vigueur. `05` est leur **source de définition proposée** tant que son statut n'a pas été arbitré/adopté.

---

# 3. Interface Registry

| Interface ID | Source | Objet | Contrat | Version | Destination | Point-in-time | Provenance | Impact 04 | Failure mode | Statut |
|---|---|---|---|---|---|---|---|---|---|---|
| IF-001 | Données / contrôle qualité | Qualité et continuité | Principe rappelé par `04 §9`, détail proposé `05 §1–2` | 04 v0.6.1 / 05 v0.1 | Validation | À définir | Rapport de couverture | Bloquant pour conditions concernées | Série discontinue ou couverture incomplète | Partiellement défini ; détail 05 non en vigueur |
| IF-002 | Dataset validé | Coûts complets | `04 §5.3 c.4` + détail proposé `05 §7` | 04 v0.6.1 / 05 v0.1 | Validation | Historique de marché | Modèle de coûts | **Référence d'interface ; détail 05 non en vigueur** | Coûts absents / incohérents | Interface à finaliser |
| IF-003 | Pipeline technique | Gel technique | `04 §3.4` + `05` ou document technique | Partiellement défini | Recherche | À définir | Journal de configuration | Bloquant selon contrôle | Configuration modifiée / non traçable | Partiellement défini |
| IF-004 | Asset Profile | Capacité / liquidité / impact / exposition / levier | Explicitement hors `04`, relève de `05` ou risque | Non défini | Validation / risque | Historique + contexte | Asset Profile / Risk | Potentiellement bloquant | Contrainte absente | Non défini |
| IF-005 | Dataset transformé | Identité + limites d'usage | `05 §3` | 0.1 proposition | Moteur | À définir | Provenance parent | Potentiellement bloquant | Transformation non déclarée | Non normatif en vigueur |
| IF-006 | Moteur A | Moteur B | Parité d'implémentation | 0.1 proposition | Moteur de référence / portage | Même données | Rapport de parité | Condition de confiance | Divergence inexpliquée | Non normatif en vigueur |

**Règle de lecture des interfaces :** une interface faisant référence à `05` ne vaut pas adoption de `05`. Tant que `05` n'est pas validé, ses détails restent proposés et ne peuvent être présentés comme une règle normative en vigueur.

---

# 4. Source of Truth

À ce stade, les sources de vérité suivantes sont observables :

| Domaine | Source de vérité actuelle | Niveau |
|---|---|---|
| Critères de validation | `04-VALIDATION-CRITERIA.md` | Référence méthodologique |
| Niveaux de preuve | `04 §7` | Référence |
| Interfaces explicitement déclarées | `04 §9` | Référence |
| Contrat de données | `05-DATA-CONTRACT.md` | Proposition seulement |
| Données / datasets réels | Non encore enregistré dans un registry canonique | Lacune |
| Asset Profile | Non encore enregistré comme contrat canonique | Lacune |
| Contradictions | Aucun registre générique identifié | Lacune |
| Arbitrages | Journal de versions dans les documents concernés, mais pas de registre transverse | Lacune |

---

# 5. Modèle temporel — état actuel

Le système doit désormais distinguer deux dimensions :

```text
VALIDITÉ MONDE
  valide_du
  valide_au

VALIDITÉ CONNAISSANCE
  connu_depuis
```

**État factuel :** cette structure n'est pas encore un contrat gelé dans `04` ou `05`.
Elle est donc enregistrée ici comme **besoin architectural**, pas comme règle déjà en vigueur.

---

# 6. Contradiction Registry — état actuel

Aucun objet transverse de contradiction n'est actuellement défini.

Architecture cible à spécifier ultérieurement :

```text
CONTRADICTION
    ↓
ANALYSE
    ↓
ARBITRAGE
    ↓
DÉCISION
    ↓
RAISON
    ↓
VERSION
```

La conservation de l'historique est une exigence d'architecture cible, mais cette section ne constitue pas encore un contrat normatif.

---

# 7. Upward Challenge — état actuel

`04` est une référence méthodologique mais aucun protocole transverse de contestation ascendante n'est actuellement formalisé.

Architecture cible :

```text
Brique aval
    ↓
POINT DE CONTESTATION
    ↓
Concept / section contesté
    ↓
Justification
    ↓
Impact
    ↓
Audit
    ↓
Arbitrage
    ↓
Nouvelle version éventuelle
```

**Principe à préserver :** gel ≠ intouchable.

---

# 8. Criticality Map

| Niveau | Définition | Audit attendu |
|---|---|---|
| C3 | Nouveau concept normatif ou architecture centrale | Complet |
| C2 | Nouvelle brique consommant des contrats existants | Intermédiaire |
| C1 | Extension sans changement sémantique | Léger |

Cette classification est enregistrée comme **architecture de gouvernance proposée** et devra être arbitrée avant de devenir normative.

---

# 9. Contradictions détectées pendant la cartographie

### C-01 — Gel de `04` vs interfaces externes incomplètes

`04` se présente comme complet sous réserve explicite, tout en laissant plusieurs sujets à des documents externes non encore définis.

**Action :** ne pas modifier `04` dans ce registre. Vérifier les dépendances avant tout gel final.

### C-02 — `04` dépend d'un `05` non validé

`04 §9` attribue plusieurs responsabilités à `05`, tandis que `05` est explicitement une proposition non validée.

**Action :** l'interface doit être formalisée avant de considérer la chaîne complète comme gelée. Cette entrée ne transforme pas `05` en autorité normative.

### C-03 — Format canonique encore indéterminé

`05 §6.1` impose l'existence d'un format canonique mais laisse le choix du format ouvert.

**Action :** décision technique séparée ; ne pas l'inventer dans le registry.

### C-04 — Bitemporalité non contractualisée

Les documents actuels ne fournissent pas encore un contrat transverse `valide_du / valide_au / connu_depuis`.

**Action :** construire le contrat temporel avant les briques dépendantes de l'historicité documentaire.

### C-05 — Contradiction ledger absent

Les arbitrages sont historisés dans les journaux de versions des documents, mais aucun registre transverse n'a été identifié.

**Action :** concevoir le registre d'arbitrage.

### C-06 — Contestation ascendante absente

Aucune interface standard ne permet actuellement à une brique aval de soumettre une contestation structurée d'un contrat amont.

**Action :** concevoir l'interface `UPWARD-CHALLENGE`.

---

# 10. Règle de construction pour les prochaines briques

Avant toute nouvelle brique, le dossier doit répondre :

1. Concepts consommés.
2. Définiteur de chaque concept.
3. Producteur de chaque donnée.
4. Dépositaire de chaque donnée.
5. Contrat et version consommés.
6. Données consultées.
7. Point-in-time applicable.
8. Contraintes consommées.
9. Contraintes créées.
10. Impact sur `04`.
11. Impact sur `05`.
12. Briques impactées.
13. Failure modes.
14. Criticité C1/C2/C3.
15. Possibilité de contestation ascendante.

**Aucune nouvelle brique normative ne doit être considérée comme intégrée tant que cette fiche n'est pas renseignée.**

---

# 11. Prochaine construction

Le prochain objet n'est pas encore `Asset Mechanics`.

Ordre de construction recommandé :

```text
08 SYSTEM REGISTRY                  ← présent document
        ↓
09 DATASET / PROVENANCE REGISTRY
        ↓
10 TEMPORAL / POINT-IN-TIME CONTRACT
        ↓
11 CONTRADICTION & ARBITRATION REGISTRY
        ↓
12 UPWARD CHALLENGE PROTOCOL
        ↓
13 CRITICALITY / AUDIT PROTOCOL
        ↓
AUDIT ADVERSARIAL
        ↓
ASSET PROFILE
        ↓
ASSET MECHANICS
```

**Important :** cet ordre est une décision de construction proposée à partir de la cartographie ; il ne modifie pas rétroactivement `04` ou `05`.
