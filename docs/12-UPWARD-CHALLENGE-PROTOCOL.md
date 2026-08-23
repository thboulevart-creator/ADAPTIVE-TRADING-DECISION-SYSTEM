# 12 — UPWARD CHALLENGE PROTOCOL

**Version:** 0.1 — ARCHITECTURE PROPOSAL / PROVISIONAL  
**Date:** 23 août 2026  
**Status:** proposition de garde-fou transverse ; non normative tant qu'elle n'est pas auditée et arbitrée.  

---

## 0. Purpose

Le protocole `UPWARD CHALLENGE` permet à une brique aval de contester formellement un concept, une règle, un contrat, une interface ou une contrainte amont lorsqu'une preuve montre qu'il est potentiellement :

- incohérent ;
- incomplet ;
- impraticable ;
- ambigu ;
- temporellement invalide ;
- incompatible avec un contrat plus prioritaire ;
- ou susceptible de produire une décision non valide.

**Principe fondamental :**

> Une brique aval peut contester une autorité amont sans acquérir automatiquement le droit de la modifier.

Le protocole sépare donc strictement :

```text
CONTESTER
   ≠
MODIFIER
   ≠
ARBITRER
```

---

# 1. Pourquoi ce protocole existe

Le gel d'un document protège contre les modifications opportunistes, mais peut créer un risque inverse : considérer un document gelé comme définitivement infaillible.

Le protocole introduit donc :

```text
CONTRAT AMONT GELÉ
        ↓
UTILISATION PAR AVAL
        ↓
FAILURE / CONTRADICTION / CONTRAINTE IMPOSSIBLE
        ↓
UPWARD CHALLENGE
        ↓
AUDIT
        ↓
ARBITRATION
        ↓
MAINTIEN / CORRECTION / VERSION NOUVELLE
```

**Gel ≠ intouchable.**

Mais :

**Challenge ≠ modification automatique.**

---

# 2. Non-goals

Ce protocole ne permet pas à une brique aval de :

- modifier directement `04` ;
- redéfinir un concept dont elle n'est pas propriétaire ;
- contourner un contrat en déclarant simplement celui-ci « impraticable » ;
- transformer une préférence d'implémentation en contradiction normative ;
- annuler un arbitrage sans nouvelle procédure ;
- faire disparaître l'historique d'une décision.

---

# 3. Qui peut émettre un challenge ?

Tout composant enregistré comme consommateur d'un contrat peut émettre un challenge lorsqu'il dispose d'éléments vérifiables.

Peuvent notamment challenger :

- une brique de recherche ;
- un moteur d'analyse ;
- un validateur ;
- un composant de risque ;
- un pipeline de données ;
- une couche d'exécution ;
- un audit indépendant.

Un agent IA peut **détecter et rédiger** un challenge, mais l'origine du signal doit rester identifiable :

```text
DETECTOR
SOURCE OF EVIDENCE
HUMAN / SYSTEM / AI
```

Une sortie d'IA n'est pas, à elle seule, une décision d'arbitrage.

---

# 4. Quand un challenge est légitime

Un challenge doit reposer sur au moins un des motifs suivants :

| Code | Motif |
|---|---|
| `SEMANTIC` | définition ambiguë ou contradictoire |
| `CONTRACT` | contrat impossible à satisfaire |
| `INTERFACE` | interface insuffisante ou incompatible |
| `TEMPORAL` | risque de look-ahead / mauvaise temporalité |
| `DATA` | donnée ou provenance incompatible |
| `IMPLEMENTATION` | impossibilité de respecter le contrat dans une implémentation conforme |
| `EVIDENCE` | preuve nouvelle ou contradiction probante |
| `SCOPE` | règle utilisée hors de son périmètre |
| `OWNERSHIP` | conflit d'autorité conceptuelle |
| `SAFETY` | risque de violation d'une contrainte fondamentale du système |

Un simple désaccord esthétique ou une préférence personnelle n'est pas suffisant.

---

# 5. Challenge Record

Chaque challenge reçoit un identifiant stable :

```text
CHAL-<domaine>-<numéro>
```

Exemples :

```text
CHAL-TEMPORAL-001
CHAL-CONTRACT-002
```

L'identifiant n'est jamais réutilisé.

---

# 6. Champs obligatoires

| Champ | Obligation |
|---|---|
| `challenge_id` | obligatoire |
| `revision` | obligatoire |
| `status` | obligatoire |
| `challenger` | obligatoire |
| `challenger_role` | obligatoire |
| `detected_at` | obligatoire |
| `target_component` | obligatoire |
| `target_contract` | obligatoire |
| `target_version` | obligatoire |
| `target_owner` | obligatoire si connu |
| `challenge_type` | obligatoire |
| `claim` | obligatoire |
| `observed_failure` | obligatoire |
| `evidence` | obligatoire |
| `reproduction` | obligatoire si reproductible |
| `scope` | obligatoire |
| `temporal_scope` | obligatoire si applicable |
| `severity` | obligatoire |
| `downstream_impact` | obligatoire |
| `proposed_resolution` | facultatif |
| `upstream_impact` | obligatoire avant arbitrage |
| `linked_contradiction` | obligatoire après qualification si contradiction |
| `decision` | obligatoire après arbitrage |
| `decision_reason` | obligatoire après arbitrage |
| `decision_version` | obligatoire si contrat modifié |

---

# 7. Cycle de vie

```text
DRAFT
  ↓
SUBMITTED
  ↓
SCREENED
  ↓
QUALIFIED
  ↓
UNDER_REVIEW
  ↓
READY_FOR_ARBITRATION
  ↓
ARBITRATED
  ↓
ACCEPTED / REJECTED / DEFERRED
```

Un challenge accepté peut conduire à :

```text
NO CHANGE
CLARIFICATION
CONTRACT PATCH
NEW VERSION
OWNERSHIP REASSIGNMENT
NEW CONSTRAINT
```

Un challenge rejeté reste enregistré avec sa raison de rejet.

---

# 8. Gate de recevabilité

Un challenge ne doit pas être envoyé directement à l'auteur du contrat avec un simple message du type :

> « Cette règle ne marche pas. »

Il doit d'abord démontrer :

1. quelle règle est contestée ;
2. quelle version est contestée ;
3. quelle brique l'utilise ;
4. dans quelles conditions ;
5. quel échec est observé ;
6. quelle preuve permet de reproduire ou vérifier l'échec ;
7. quelle conséquence l'échec produit ;
8. si l'échec est local ou systémique.

Un challenge insuffisamment documenté peut être `REJECTED — INSUFFICIENT EVIDENCE` sans modifier le contrat amont.

---

# 9. Prohibition de contournement

Lorsqu'un challenge est ouvert, la brique aval doit continuer à respecter le contrat contesté **sauf si une règle de sécurité ou d'arrêt explicitement autorisée impose une suspension**.

Interdit :

```text
Contrat A
  ↓
Je le conteste
  ↓
Je l'ignore
  ↓
Je crée implicitement le contrat B
```

Autorisé :

```text
Contrat A
  ↓
Challenge
  ↓
Analyse
  ↓
Décision
  ↓
A ou nouvelle version de A
```

---

# 10. Exception — impossibilité critique

Si le respect du contrat amont crée un risque critique identifié, le consommateur peut déclencher une **SAFE HOLD**.

La SAFE HOLD :

- ne modifie pas le contrat ;
- bloque ou suspend l'utilisation concernée ;
- crée obligatoirement un challenge ;
- exige une justification ;
- doit être auditée ;
- doit être levée ou transformée en décision formelle.

```text
CONTRAT
  ↓
RISQUE CRITIQUE
  ↓
SAFE HOLD
  ↓
UPWARD CHALLENGE
  ↓
ARBITRATION
```

La SAFE HOLD est un mécanisme de protection, pas un droit de gouvernance.

---

# 11. Ownership

Le challenge doit identifier :

```text
TARGET CONCEPT
      ↓
DEFINITEUR
      ↓
PRODUCTEUR
      ↓
DEPOSITAIRE
      ↓
CONSOMMATEUR / CHALLENGER
```

Si le challenger n'est pas propriétaire du concept, il peut démontrer un problème mais ne peut pas réécrire sa définition.

Si le challenge porte précisément sur l'ownership, il doit être qualifié `OWNERSHIP` et relié à une contradiction dans `11`.

---

# 12. Lien obligatoire avec `11`

Un challenge ne remplace pas le registre de contradiction.

Lorsque le challenge révèle une incompatibilité entre deux claims ou contrats :

```text
UPWARD CHALLENGE
       ↓
CONTRADICTION RECORD — 11
       ↓
ANALYSIS
       ↓
ARBITRATION
       ↓
DECISION
```

Le challenge conserve l'observation aval ; `11` conserve le conflit et son arbitrage.

---

# 13. Temporalité

Tout challenge concernant des données historiques doit indiquer :

- période du phénomène observé ;
- date de disponibilité de la preuve ;
- date de détection ;
- version du contrat utilisée lors de l'observation.

Une découverte faite en 2026 ne peut pas être présentée comme une information connue en 2019 simplement parce qu'elle concerne un événement de 2019.

Le protocole dépend du contrat `10` pour les règles détaillées de point-in-time.

---

# 14. Classification de criticité

Le challenge utilise la criticité de gouvernance proposée par `13` :

| Niveau | Exemple | Traitement |
|---|---|---|
| `C1` | Ambiguïté locale sans changement sémantique | revue légère |
| `C2` | Interface ou comportement de plusieurs briques | audit intermédiaire |
| `C3` | Concept normatif, preuve, temporalité ou architecture centrale | audit complet + arbitrage formel |

En cas de doute entre deux niveaux, le niveau supérieur est retenu provisoirement jusqu'à qualification.

---

# 15. Propositions du challenger

Le challenger peut proposer une résolution, mais celle-ci est explicitement étiquetée :

```text
PROPOSED — NON AUTHORITATIVE
```

Une proposition ne devient pas une règle simplement parce qu'elle est techniquement élégante ou qu'elle résout le problème local.

Le propriétaire du contrat et le processus d'arbitrage déterminent la décision finale.

---

# 16. Contestation d'un document gelé

Un document gelé peut être challengé si le challenger démontre un problème vérifiable.

Le statut `FROZEN` signifie :

> aucune modification non gouvernée.

Il ne signifie pas :

> aucune contestation possible.

Ainsi :

```text
04 FROZEN
   ↓
CHALLENGE
   ↓
AUDIT
   ↓
ARBITRATION
   ↓
04 v0.7 éventuelle
```

Une modification éventuelle doit conserver le lien :

```text
04 v0.6.1
   ↓
CHAL-XXX
   ↓
CONTR-XXX
   ↓
DECISION
   ↓
04 v0.7
```

---

# 17. Anti-patterns interdits

### A. Frozen = infallible
Refuser tout challenge uniquement parce que le document est gelé.

### B. Challenge = permission
Considérer le challenge comme une autorisation de contourner le contrat.

### C. Local workaround
Créer une règle locale incompatible sans passer par le protocole.

### D. Authority inversion
Permettre au consommateur de devenir automatiquement propriétaire du concept.

### E. AI authority
Considérer la sortie d'une IA comme arbitrage final.

### F. Evidence laundering
Transformer une découverte actuelle en connaissance historique.

### G. Silent rejection
Rejeter un challenge sans conserver la raison et les preuves examinées.

### H. Recursive dispute
Créer une chaîne infinie de challenges sans décision, sans statut et sans responsable.

---

# 18. Minimal record template

```yaml
challenge_id: CHAL-XXX-001
revision: 1
status: SUBMITTED
challenger:
challenger_role:
detected_at:
target_component:
target_contract:
target_version:
target_owner:
challenge_type:
claim:
observed_failure:
evidence: []
reproduction:
scope:
temporal_scope:
severity: C1 | C2 | C3
downstream_impact:
upstream_impact:
proposed_resolution:
linked_contradiction:
decision:
decision_reason:
decided_by:
decided_at:
decision_version:
```

---

# 19. Minimum evidence standard

Un challenge `C2/C3` doit fournir autant que possible :

```text
INPUT
VERSION
CONFIGURATION
DATASET
POINT-IN-TIME
EXPECTED BEHAVIOR
OBSERVED BEHAVIOR
REPRODUCTION
IMPACT
```

Un résultat non reproductible peut être enregistré, mais il doit être explicitement marqué comme tel.

---

# 20. Decision outcomes

L'arbitrage doit produire l'un des résultats suivants :

| Code | Signification |
|---|---|
| `CONFIRMED` | Le contrat amont reste valide |
| `CLARIFIED` | Le contrat reste valide mais doit être clarifié |
| `PATCHED` | Modification limitée et gouvernée |
| `VERSIONED` | Nouvelle version nécessaire |
| `REASSIGNED` | Ownership modifié après arbitrage |
| `SUSPENDED` | Utilisation suspendue temporairement |
| `REJECTED` | Challenge non démontré |
| `DEFERRED` | Décision reportée avec responsable et échéance |

Aucun résultat ne doit effacer le challenge original.

---

# 21. Integration with contradiction history

Le graphe de gouvernance devient :

```text
OBSERVATION
    ↓
UPWARD CHALLENGE — 12
    ↓
CONTRADICTION — 11
    ↓
ANALYSIS
    ↓
ARBITRATION
    ↓
DECISION
    ↓
VERSION EVENTUELLE
```

Cette structure protège contre deux erreurs opposées :

1. **autorité intouchable** ;
2. **autorité constamment contournée**.

---

# 22. Gate before integration

Avant intégration normative de `12`, le système doit démontrer :

1. qu'un consommateur peut contester un contrat amont ;
2. que le challenge identifie précisément sa cible et sa version ;
3. que le challenger ne peut pas modifier directement le contrat ;
4. qu'un challenge insuffisamment documenté peut être rejeté avec justification ;
5. qu'un challenge critique peut déclencher une SAFE HOLD ;
6. que les challenges sont reliés aux contradictions dans `11` lorsqu'un conflit existe ;
7. que la temporalité est conservée ;
8. que les décisions sont historisées ;
9. que `FROZEN` ne signifie pas `INCONTESTABLE` ;
10. qu'aucune sortie d'IA n'est assimilée automatiquement à une décision normative.

---

# 23. Statut

**PROPOSITION UNIQUEMENT.**

Ce document ne modifie ni `04`, ni `05`, ni aucun autre contrat existant.

Il devra être confronté aux documents existants, puis audité adversarialement avant d'être considéré comme normatif.
