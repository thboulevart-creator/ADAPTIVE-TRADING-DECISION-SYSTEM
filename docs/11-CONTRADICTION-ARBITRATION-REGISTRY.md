# 11 — CONTRADICTION & ARBITRATION REGISTRY

**Version:** 0.1 — ARCHITECTURE PROPOSAL / PROVISIONAL  
**Date:** 23 août 2026  
**Status:** proposition de garde-fou transverse ; aucune modification rétroactive de `04` ou `05`.  

---

## 0. Purpose

Ce registre existe pour empêcher qu'une contradiction soit simplement corrigée, supprimée ou contournée puis oubliée.

Toute contradiction matériellement pertinente doit conserver une trace de :

```text
CONTRADICTION
    ↓
DÉTECTION
    ↓
QUALIFICATION
    ↓
ANALYSE
    ↓
ARBITRAGE
    ↓
DÉCISION
    ↓
RAISON
    ↓
VERSION / EFFECTIVITÉ
```

**Principe fondamental :** une contradiction résolue n'est pas une contradiction inexistante. Son historique doit rester auditable.

---

# 1. Non-goals

Ce registre :

- ne redéfinit pas les concepts de `04` ou `05` ;
- ne tranche pas automatiquement les désaccords ;
- ne transforme pas une proposition en règle normative ;
- ne supprime jamais une contradiction pour faire disparaître un conflit historique ;
- ne remplace pas l'autorité du document propriétaire du concept.

---

# 2. Types de contradiction

Une contradiction doit être qualifiée avant arbitrage.

| Type | Description |
|---|---|
| `SEMANTIC` | Deux définitions incompatibles d'un même concept |
| `CONTRACT` | Deux contrats imposent des contraintes incompatibles |
| `OWNERSHIP` | Deux briques revendiquent une même autorité sémantique |
| `TEMPORAL` | Les contraintes temporelles sont incompatibles ou insuffisantes |
| `DATA` | Deux sources/datasets fournissent des valeurs incompatibles |
| `PROCEDURAL` | Deux procédures prescrivent des traitements incompatibles |
| `VERSION` | Deux versions actives ou référencées créent une ambiguïté |
| `IMPLEMENTATION` | Deux implémentations divergent malgré un même contrat |
| `EVIDENCE` | Deux éléments de preuve produisent des conclusions incompatibles |
| `SCOPE` | Une règle est appliquée hors de son périmètre déclaré |

Un même événement peut recevoir plusieurs types.

---

# 3. Identité d'une contradiction

Chaque contradiction reçoit un identifiant stable :

```text
CONTR-<domaine>-<numéro>
```

Exemple :

```text
CONTR-DATA-001
CONTR-TEMPORAL-002
```

L'identifiant ne doit pas être réutilisé, même après résolution.

---

# 4. Contradiction Record

Chaque entrée doit au minimum contenir :

| Champ | Obligation |
|---|---|
| `contradiction_id` | obligatoire |
| `detected_at` | obligatoire |
| `detected_by` | obligatoire |
| `status` | obligatoire |
| `type` | obligatoire |
| `scope` | obligatoire |
| `claim_a` | obligatoire |
| `claim_b` | obligatoire |
| `source_a` | obligatoire |
| `source_b` | obligatoire |
| `versions_a_b` | obligatoire |
| `concept_owner` | obligatoire si concept identifiable |
| `temporal_scope` | obligatoire si applicable |
| `impact` | obligatoire |
| `severity` | obligatoire |
| `analysis` | obligatoire avant arbitrage |
| `decision` | obligatoire après arbitrage |
| `decision_reason` | obligatoire après arbitrage |
| `decided_by` | obligatoire après arbitrage |
| `decided_at` | obligatoire après arbitrage |
| `effective_version` | obligatoire si la décision modifie un contrat |
| `supersedes` | obligatoire si une version précédente est remplacée |
| `evidence` | obligatoire |

---

# 5. Statuts

Une contradiction suit un cycle explicite :

```text
DETECTED
   ↓
QUALIFIED
   ↓
UNDER_ANALYSIS
   ↓
READY_FOR_ARBITRATION
   ↓
ARBITRATED
   ↓
RESOLVED / ACCEPTED / REJECTED / DEFERRED
```

### Définitions

- **DETECTED** — conflit signalé mais pas encore qualifié.
- **QUALIFIED** — nature, périmètre et sources identifiés.
- **UNDER_ANALYSIS** — investigation en cours.
- **READY_FOR_ARBITRATION** — éléments suffisants pour décision.
- **ARBITRATED** — décision formellement prise.
- **RESOLVED** — contradiction supprimée par modification/version validée.
- **ACCEPTED** — contradiction reconnue mais maintenue volontairement avec justification.
- **REJECTED** — signal considéré comme non valide après analyse.
- **DEFERRED** — décision reportée explicitement.

Un statut terminal ne supprime jamais l'enregistrement.

---

# 6. Qualification avant correction

**Interdiction de corriger immédiatement une contradiction normative sans créer d'abord son enregistrement.**

Séquence obligatoire :

```text
DÉTECTER
   ↓
ENREGISTRER
   ↓
QUALIFIER
   ↓
ANALYSER
   ↓
ARBITRER
   ↓
MODIFIER SI NÉCESSAIRE
```

Cela empêche une correction silencieuse de détruire la preuve du conflit initial.

---

# 7. Ownership et autorité

L'arbitrage doit identifier le **Définiteur** du concept concerné.

Règle :

> Le producteur d'une donnée n'acquiert jamais automatiquement l'autorité pour arbitrer la sémantique de cette donnée.

Si la contradiction concerne l'autorité elle-même, elle devient `OWNERSHIP` et doit être arbitrée avant toute modification sémantique.

---

# 8. Arbitrage

Un arbitrage doit répondre explicitement à :

1. Quelle proposition est retenue ?
2. Quelle proposition est rejetée ou limitée ?
3. Pourquoi ?
4. Quelle autorité possède le concept ?
5. Quelles preuves ont été utilisées ?
6. Quel périmètre est concerné ?
7. Quelle version devient applicable ?
8. À partir de quand ?
9. Quelles briques sont impactées ?
10. Faut-il créer un point de contestation ascendante ?

Aucune décision ne doit être enregistrée uniquement sous la forme « corrigé » ou « harmonisé ».

---

# 9. Temporalité de la décision

Une décision d'arbitrage possède elle-même une temporalité.

Elle doit distinguer :

```text
DECISION FACT
    decision_at

EFFECTIVE RULE
    effective_from
    effective_to

KNOWLEDGE / PUBLICATION
    known_from
```

Une décision prise aujourd'hui ne doit pas être présentée automatiquement comme si elle avait toujours été connue.

Lorsqu'une correction concerne une recherche historique, le registre doit permettre de distinguer :

> ce qui était vrai à l'époque ;

> ce qui était connu à l'époque ;

> ce qui a été décidé ultérieurement.

Cette règle dépend du contrat temporel `10` et ne le remplace pas.

---

# 10. Impact assessment

Avant clôture, l'arbitrage doit rechercher les impacts sur :

```text
04 — Validation Criteria
05 — Data Contract
08 — System Registry
09 — Dataset / Provenance Registry
10 — Temporal / Point-in-Time Contract
12 — Upward Challenge Protocol
13 — Criticality / Audit Protocol
Asset Profile
Asset Mechanics
Research engines
Risk / decision layers
```

Un impact non évalué doit être explicitement marqué `UNKNOWN`, jamais supposé nul.

---

# 11. Réouverture

Une contradiction résolue peut être **réouverte** si :

- une nouvelle preuve invalide la décision ;
- une nouvelle version du contrat change le contexte ;
- une brique aval démontre une contrainte impraticable ;
- une nouvelle contradiction dépendante apparaît ;
- une erreur dans l'arbitrage initial est identifiée.

La réouverture conserve le même identifiant et crée une nouvelle révision de l'enregistrement.

```text
CONTR-XXX-001 R1
        ↓
     décision
        ↓
CONTR-XXX-001 R2 — reopened
```

---

# 12. Upward Challenge compatibility

Le registre est conçu pour fonctionner avec le futur `12 — UPWARD CHALLENGE PROTOCOL`.

Une contestation ascendante ne modifie pas directement un contrat amont.

Elle crée :

```text
UPWARD CHALLENGE
      ↓
CONTRADICTION RECORD
      ↓
ANALYSIS
      ↓
ARBITRATION
      ↓
VERSION EVENTUELLE
```

Ainsi, une brique aval peut contester sans obtenir automatiquement le pouvoir de redéfinir le concept.

---

# 13. Criticité provisoire

La criticité de la contradiction doit être séparée de la criticité de la brique (`C1/C2/C3`).

| Niveau | Signification |
|---|---|
| `K1` | Impact documentaire/local |
| `K2` | Impact sur une interface ou plusieurs briques |
| `K3` | Impact sur un concept normatif, une preuve ou l'architecture centrale |

Une contradiction `K3` ne peut pas être clôturée par simple modification documentaire locale.

La grille finale sera coordonnée avec `13 — CRITICALITY / AUDIT PROTOCOL`.

---

# 14. Anti-patterns interdits

Les comportements suivants sont explicitement considérés comme des défauts de gouvernance :

### A. Silent fix
Modifier un document sans enregistrer le conflit initial.

### B. Authority by implementation
Laisser le producteur d'une donnée redéfinir sa sémantique.

### C. Latest-version fallacy
Considérer automatiquement la dernière version comme historiquement vraie.

### D. Consensus without owner
Résoudre un conflit par consensus entre IA sans identifier l'autorité du concept.

### E. Deletion as resolution
Supprimer une entrée contradictoire pour faire disparaître le problème.

### F. Backdated arbitration
Présenter une décision actuelle comme si elle avait été connue au moment historique étudié.

### G. Scope laundering
Résoudre une contradiction en changeant implicitement le périmètre de la règle.

---

# 15. Minimal record template

```yaml
contradiction_id: CONTR-XXX-001
revision: 1
status: DETECTED
type:
  - CONTRACT
detected_at:
detected_by:
scope:
claim_a:
source_a:
version_a:
claim_b:
source_b:
version_b:
concept_owner:
temporal_scope:
severity: K1 | K2 | K3
impact:
evidence: []
analysis:
decision:
decision_reason:
decided_by:
decided_at:
effective_from:
effective_to:
effective_version:
supersedes:
impacted_components: []
upward_challenge: null
reopen_of: null
```

---

# 16. Current registry

Aucune contradiction transverse n'est créée artificiellement dans ce document.

Les contradictions déjà identifiées dans `08 — SYSTEM REGISTRY` doivent être migrées dans ce registre lors de l'étape d'intégration, notamment :

- `C-01` — gel de `04` vs interfaces externes incomplètes ;
- `C-02` — dépendance de `04` envers un `05` non validé ;
- `C-03` — format canonique indéterminé ;
- `C-04` — bitemporalité non contractualisée ;
- `C-05` — contradiction ledger absent ;
- `C-06` — contestation ascendante absente.

**Important :** leur présence dans `08` constitue l'état de la cartographie ; leur migration dans `11` sera une opération de gouvernance distincte.

---

# 17. Gate before next normative brick

Avant de considérer `12` comme intégré, `11` doit permettre de démontrer :

1. qu'une contradiction possède un identifiant stable ;
2. qu'elle ne peut pas disparaître silencieusement ;
3. que ses sources et versions sont conservées ;
4. que son propriétaire conceptuel est identifié ;
5. que l'analyse précède l'arbitrage ;
6. que la décision possède une raison explicite ;
7. que l'effet de version est traçable ;
8. que la temporalité de la décision est conservée ;
9. que les impacts sont évalués ;
10. qu'une décision peut être contestée ou rouverte sans détruire l'historique.

**Statut de ce document : PROPOSITION. Il ne devient pas un contrat normatif tant qu'il n'a pas passé la procédure d'audit et d'arbitrage prévue par l'architecture du système.**
