# 14 — AUDIT FINDINGS REGISTER

**Version:** 0.1 — AUDIT OUTPUT / CONTROLLED WORKING REGISTER  
**Date:** 23 août 2026  
**Source:** Audit final adversarial du corpus réel, commit audité `1b24c9c`.  
**Status:** registre de sortie d'audit ; aucune nouvelle règle normative n'est créée ici.  

---

## 0. Purpose

Ce registre transforme les constats de l'audit adversarial en unités de traitement traçables.

Chaîne de contrôle :

```text
AUDIT FINAL
    ↓
FINDING
    ↓
CLASSIFICATION
    ↓
ACTION
    ↓
OWNER
    ↓
ARBITRATION REQUIRED
    ↓
STATUS
    ↓
RETEST
```

**Règle fondamentale :** un finding ne disparaît jamais parce qu'un document a été modifié. Il reste ouvert jusqu'à ce que son traitement et, lorsque requis, son re-test soient enregistrés.

**Important :** ce registre est un artefact de pilotage d'audit. Les champs `OWNER`, `ARBITRATION_REQUIRED`, `ACTION` et `STATUS` décrivent le traitement du finding ; ils ne constituent pas à eux seuls des règles normatives du système.

---

## 1. Corpus et réserves de périmètre

### R-01 — Écart de nomenclature `02/03`

- **Classification:** NON ÉTABLI
- **Severity:** —
- **Source:** Audit R-01
- **Finding:** la mission annonçait `02-ARCHITECTURE.md` et `03-DECISION-FLOW.md`, tandis que le dépôt réel contient `02-ASSET-PROFILE-DATABASE.md` et `03-REGIME-EXPERT-RESEARCH-FOUNDATION.md`.
- **Action:** clarifier et figer la nomenclature réelle du corpus.
- **Owner:** TBD — pilotage documentaire
- **Arbitration required:** NON
- **Decision ref:** —
- **Status:** OPEN
- **Retest required:** OUI
- **Retest result:** —

### R-02 — D1→D7 absentes du corpus audité

- **Classification:** NON ÉTABLI
- **Severity:** —
- **Source:** Audit R-02
- **Finding:** les textes normatifs D1 à D7 ne figurent pas dans le corpus audité ; l'audit ne peut donc pas établir leur contenu ni leur conformité directe.
- **Action:** publier/identifier les textes D1→D7 avant leur analyse normative.
- **Owner:** TBD — gouvernance
- **Arbitration required:** OUI
- **Decision ref:** D1–D7
- **Status:** OPEN
- **Retest required:** OUI
- **Retest result:** —

### R-03 — Documents de travail non normatifs

- **Classification:** NON ÉTABLI / INFORMATION
- **Severity:** —
- **Source:** Audit R-03
- **Finding:** `AUDIT-08-13-INTERFACE-MAP.md` et `COUNTER-EXPERTISE-PACKAGE-08-13.md` sont explicitement non normatifs.
- **Action:** conserver la distinction entre cartographie de travail et source normative.
- **Owner:** TBD — gouvernance documentaire
- **Arbitration required:** NON
- **Decision ref:** —
- **Status:** OPEN
- **Retest required:** NON
- **Retest result:** —

---

## 2. Contradictions structurelles — Phase A prioritaire

### CTR-01 — Condition bloquante de `04` dépendant de `05` sans effet normatif

- **Classification:** CONTRADICTION
- **Severity:** G4
- **Source:** Audit §1.1
- **Evidence:** `04 §5.3` condition 4 + `04 §9` + statut de `05`.
- **Finding:** une condition bloquante de validation exige la survie aux coûts complets de `05`, alors que `05` indique qu'aucune de ses règles n'est en vigueur.
- **Action:** corriger objectivement le statut/référencement de `05` afin que `04` ne dépende pas d'une exigence inévaluable. Ne pas inventer une nouvelle règle métier.
- **Owner:** TBD — documentation/architecture
- **Arbitration required:** NON pour la correction factuelle ; OUI si la correction modifie le fond normatif.
- **Decision ref:** D4 potentiel
- **Status:** OPEN — PHASE A
- **Retest required:** OUI
- **Retest result:** —

### CTR-02 — `05` simultanément sans autorité et définiteur de concepts dans `08`

- **Classification:** CONTRADICTION
- **Severity:** G4
- **Source:** Audit §1.1 / §6.2
- **Evidence:** `08 §1` et `08 §2`.
- **Finding:** le registre désigne `05` comme définiteur de huit concepts tout en l'enregistrant comme document sans règle en vigueur.
- **Action:** distinguer explicitement propriété sémantique proposée et autorité normative en vigueur ; corriger l'enregistrement manifeste.
- **Owner:** TBD — registry/documentation
- **Arbitration required:** NON pour la correction de registre ; OUI si une autorité normative nouvelle doit être adoptée.
- **Decision ref:** D4 potentiel
- **Status:** OPEN — PHASE A
- **Retest required:** OUI
- **Retest result:** —

---

## 3. Lacunes bloquantes d'implémentation

### LAC-16 — Transitions CHAL sans acteurs ni conditions

- **Classification:** LACUNE
- **Severity:** G5
- **Source:** Audit §11.1
- **Finding:** six transitions sur sept de la machine CHAL n'ont pas d'acteur désigné ; la transition `READY_FOR_ARBITRATION → ARBITRATED` n'est pas déterministe.
- **Action:** définir les acteurs, conditions et autorisations de transition.
- **Owner:** TBD — gouvernance de décision
- **Arbitration required:** OUI
- **Decision ref:** D1
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

### LAC-16b — Transitions CONTR sans acteurs

- **Classification:** LACUNE
- **Severity:** G5
- **Source:** Audit §11.2
- **Finding:** les transitions de `CONTR` ne disposent pas d'un modèle déterministe d'acteur/autorité.
- **Action:** définir acteurs, conditions, droits de transition et état terminal.
- **Owner:** TBD — gouvernance de décision
- **Arbitration required:** OUI
- **Decision ref:** D1
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

---

## 4. Findings G4 liés aux décisions D1→D7

### LAC-01 — Politique de blocage différée

- **Classification:** LACUNE
- **Severity:** G4
- **Source:** Audit §1.2
- **Finding:** `09 §14` et `10 §5` renvoient à une décision future/arbitrage avec `04`, sans mécanisme actuellement opérant.
- **Action:** définir la politique de blocage et sa relation avec `04`.
- **Owner:** TBD — gouvernance temporelle
- **Arbitration required:** OUI
- **Decision ref:** D3
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

### LAC-08 — Absence de détection cumulative des changements

- **Classification:** LACUNE
- **Severity:** G4
- **Source:** Audit §4.2
- **Finding:** `13 §10` interdit le fractionnement matériel, mais aucun mécanisme ne détecte le cumul de changements successifs.
- **Action:** définir un mécanisme de détection/agrégation des changements apparentés.
- **Owner:** TBD — gouvernance du changement
- **Arbitration required:** OUI
- **Decision ref:** D2
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

### LAC-10 — Adoption normative et application non attribuées

- **Classification:** LACUNE
- **Severity:** G4
- **Source:** Audit §6.1
- **Finding:** propriété sémantique, adoption normative, registre et application opérationnelle ne sont pas tous attribués.
- **Action:** séparer explicitement les rôles et attribuer les fonctions manquantes.
- **Owner:** TBD — gouvernance
- **Arbitration required:** OUI
- **Decision ref:** D4
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

### LAC-11 — Statut des limites d'usage indéterminé

- **Classification:** LACUNE
- **Severity:** G4
- **Source:** Audit §6.3
- **Finding:** le corpus ne détermine pas clairement si les limites d'usage sont immuables, modifiables ou soumises à un mécanisme spécifique de versionnement.
- **Action:** classifier le statut des usage limits et définir leur traçabilité.
- **Owner:** TBD — gouvernance des données
- **Arbitration required:** OUI
- **Decision ref:** D4
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

### LAC-12 — Aucun déclencheur lié au changement de consommateur

- **Classification:** LACUNE
- **Severity:** G4
- **Source:** Audit §7
- **Finding:** `09 §12` déclenche une réévaluation lorsqu'un dataset change, mais aucun mécanisme équivalent n'est défini lorsqu'un consommateur ou son usage change.
- **Action:** définir les changements de consommateur nécessitant réévaluation et leur déclenchement.
- **Owner:** TBD — gouvernance data/consumer
- **Arbitration required:** OUI
- **Decision ref:** D5
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

### LAC-14 — Champs temporels non obligatoires

- **Classification:** LACUNE
- **Severity:** G4
- **Source:** Audit §10.2
- **Finding:** `10 §21` renvoie à une matrice de champs obligatoires encore non arbitrée.
- **Action:** définir la matrice minimale des champs temporels obligatoires avant implémentation.
- **Owner:** TBD — gouvernance temporelle
- **Arbitration required:** OUI
- **Decision ref:** D3
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

### LAC-17 — SAFE HOLD sans acteur de maintien/levée ni durée

- **Classification:** LACUNE
- **Severity:** G4
- **Source:** Audit §9 / §11.3
- **Finding:** le déclenchement est attribué au consommateur, mais audit, maintien, résolution, levée, durée maximale et recours ne sont pas attribués.
- **Action:** définir le cycle de vie complet de SAFE HOLD.
- **Owner:** TBD — gouvernance challenge/arbitrage
- **Arbitration required:** OUI
- **Decision ref:** D7
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

### LAC-18 — Indépendance des sources IA non définie

- **Classification:** LACUNE
- **Severity:** G4
- **Source:** Audit §13
- **Finding:** le corpus distingue recommandation IA et décision d'arbitrage mais ne définit pas l'indépendance des sources ou des analyses multi-agents.
- **Action:** définir les exigences minimales d'indépendance, provenance et diversité des sources d'analyse.
- **Owner:** TBD — gouvernance IA
- **Arbitration required:** OUI
- **Decision ref:** D1 potentiel
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

### LAC-06 — Cumuls de rôles non traités

- **Classification:** LACUNE
- **Severity:** G4
- **Source:** Audit §2.2
- **Finding:** huit cumuls de rôles sur neuf ne sont ni autorisés ni interdits.
- **Action:** établir la matrice des incompatibilités/cumuls de rôles.
- **Owner:** TBD — gouvernance
- **Arbitration required:** OUI
- **Decision ref:** D1/D2
- **Status:** OPEN — PHASE B
- **Retest required:** OUI
- **Retest result:** —

---

## 5. Findings G3 et G2 — traitement coordonné

### LAC-03 — Correspondance K1/K2/K3 ↔ criticité absente

- **Classification:** LACUNE
- **Severity:** G3
- **Action:** établir la correspondance entre l'échelle de contradiction et l'échelle de criticité, ou supprimer la dépendance.
- **Owner:** TBD — gouvernance classification
- **Arbitration required:** OUI
- **Decision ref:** —
- **Status:** OPEN
- **Retest required:** OUI

### LAC-04 — Domaine de `severity` non défini

- **Classification:** LACUNE
- **Severity:** G2
- **Action:** définir le domaine de valeurs de `severity` et sa relation avec la criticité.
- **Owner:** TBD — gouvernance classification
- **Arbitration required:** OUI
- **Decision ref:** —
- **Status:** OPEN
- **Retest required:** OUI

### LAC-05 — Dépendance circulaire de criticité

- **Classification:** LACUNE
- **Severity:** G1
- **Action:** rendre la détermination de criticité unidirectionnelle et non circulaire.
- **Owner:** TBD — gouvernance classification
- **Arbitration required:** OUI
- **Decision ref:** —
- **Status:** OPEN
- **Retest required:** OUI

### LAC-02 — Entité `Dataset governance` non identifiée

- **Classification:** LACUNE
- **Severity:** G3
- **Action:** identifier l'entité réelle responsable de la déclaration d'usage.
- **Owner:** TBD — gouvernance data
- **Arbitration required:** OUI
- **Decision ref:** D4
- **Status:** OPEN
- **Retest required:** OUI

### LAC-07 — Vérificateur de classification non désigné

- **Classification:** LACUNE
- **Severity:** G3
- **Action:** désigner l'acteur ou mécanisme chargé de vérifier la classification.
- **Owner:** TBD — gouvernance classification
- **Arbitration required:** OUI
- **Decision ref:** D2/D6
- **Status:** OPEN
- **Retest required:** OUI

### LAC-09 — Absence de préséance entre `04 §4.3` et `10 §5`

- **Classification:** LACUNE
- **Severity:** G3
- **Action:** définir la règle de résolution lorsque statut probatoire et admissibilité temporelle divergent.
- **Owner:** TBD — gouvernance temporelle
- **Arbitration required:** OUI
- **Decision ref:** D3
- **Status:** OPEN
- **Retest required:** OUI

### LAC-13 — `13` non explicitement désigné comme objet de sa propre grille

- **Classification:** LACUNE
- **Severity:** G3
- **Action:** clarifier le périmètre d'application de la grille de `13` à `13` lui-même.
- **Owner:** TBD — gouvernance classification
- **Arbitration required:** OUI
- **Decision ref:** D6
- **Status:** OPEN
- **Retest required:** OUI

### LAC-15 — Détecteur de contradiction non désigné

- **Classification:** LACUNE
- **Severity:** G3
- **Action:** désigner le producteur de `detected_by` et le mécanisme de détection.
- **Owner:** TBD — gouvernance contradiction
- **Arbitration required:** OUI
- **Decision ref:** —
- **Status:** OPEN
- **Retest required:** OUI

---

## 6. Risques adversariaux à conserver jusqu'au re-test

### RSQ-03 — Fractionnement de changement

- **Classification:** RISQUE
- **Severity:** G4
- **Action:** traiter via LAC-08 ; aucun contournement ne doit être déclaré fermé avant test cumulatif.
- **Owner:** TBD — gouvernance du changement
- **Arbitration required:** OUI
- **Decision ref:** D2
- **Status:** OPEN
- **Retest required:** OUI

### RSQ-05 — Proposition normative acquérant un effet par enregistrement

- **Classification:** RISQUE
- **Severity:** G4
- **Action:** traiter via CTR-02/LAC-10 ; séparer ownership sémantique et autorité normative.
- **Owner:** TBD — gouvernance documentaire
- **Arbitration required:** OUI
- **Decision ref:** D4
- **Status:** OPEN
- **Retest required:** OUI

### RSQ-06 — Changement de consommateur + élargissement d'usage

- **Classification:** RISQUE
- **Severity:** G4
- **Action:** traiter via LAC-11/LAC-12 et re-jouer le scénario historique.
- **Owner:** TBD — gouvernance data/consumer
- **Arbitration required:** OUI
- **Decision ref:** D5
- **Status:** OPEN
- **Retest required:** OUI

### RSQ-07 — Modification de règle après observation

- **Classification:** RISQUE
- **Severity:** G4
- **Action:** définir l'antériorité obligatoire entre observation, challenge, classification, arbitrage et modification.
- **Owner:** TBD — gouvernance changement
- **Arbitration required:** OUI
- **Decision ref:** D1
- **Status:** OPEN
- **Retest required:** OUI

### RSQ-01 — Deux registres d'interfaces divergents

- **Classification:** RISQUE
- **Severity:** G3
- **Action:** aligner ou hiérarchiser explicitement `04 §9` et `08 §3`.
- **Owner:** TBD — architecture/documentation
- **Arbitration required:** OUI si hiérarchie normative ; sinon correction documentaire.
- **Decision ref:** —
- **Status:** OPEN
- **Retest required:** OUI

### RSQ-04 — Élargissement d'une permission par couche concurrente

- **Classification:** RISQUE
- **Severity:** G3
- **Action:** traiter avec LAC-09 et définir une préséance unique.
- **Owner:** TBD — gouvernance temporelle
- **Arbitration required:** OUI
- **Decision ref:** D3
- **Status:** OPEN
- **Retest required:** OUI

### RSQ-02 — Homonymies de concepts

- **Classification:** RISQUE
- **Severity:** G2
- **Action:** établir un glossaire canonique et distinguer les dimensions de confiance/admissibilité/severity.
- **Owner:** TBD — gouvernance documentaire
- **Arbitration required:** OUI si modification de sens ; NON pour simple clarification lexicale.
- **Decision ref:** —
- **Status:** OPEN
- **Retest required:** OUI

### INF-01 — Arbitrage implicitement assimilé à adoption normative

- **Classification:** INFERENCE
- **Severity:** G3
- **Action:** ne pas traiter comme violation. Clarifier séparément le mécanisme d'adoption si nécessaire.
- **Owner:** TBD — gouvernance
- **Arbitration required:** OUI
- **Decision ref:** D1
- **Status:** OPEN
- **Retest required:** OUI

---

## 7. Scénarios adversariaux de re-test

Les scénarios suivants deviennent des tests de non-régression obligatoires après correction des findings associés.

| Test | Scénario | Findings associés | Résultat attendu |
|---|---|---|---|
| S-01 | Fractionnement d'un changement matériel en plusieurs petits changements | LAC-08 / RSQ-03 | Le cumul matériel est détecté et reclassifié correctement. |
| S-02 | Changement de consommateur avec dataset inchangé | LAC-12 / RSQ-06 | Une réévaluation est déclenchée lorsque le changement est matériel. |
| S-03 | Élargissement d'une enveloppe d'usage après violation | LAC-11 / RSQ-06 | L'élargissement est tracé, autorisé selon le mécanisme adopté et ne rétro-valide pas l'usage passé. |
| S-04 | Dataset sans provenance temporelle obligatoire | LAC-14 / LAC-01 | L'objet est bloqué avant consommation lorsque les champs obligatoires manquent. |
| S-05 | `05` consommé comme autorité via `08` | CTR-02 / RSQ-05 | Ownership sémantique proposé et autorité normative sont distincts. |
| S-06 | Modification d'une règle après résultat défavorable | RSQ-07 | L'ordre temporel et l'autorité de modification sont traçables et contrôlés. |
| S-07 | SAFE HOLD sans auditeur disponible | LAC-17 | Un comportement déterministe de maintien/escalade/expiration existe. |
| S-08 | Trois IA partageant la même source initiale | LAC-18 | Le système distingue analyse indépendante et simple duplication. |
| S-09 | Correction silencieuse d'une contradiction | LAC-15 | La contradiction est détectée, enregistrée et ne peut pas être silencieusement écrasée. |
| S-10 | Divergence `04 §4.3` / `10 §5` | LAC-09 / RSQ-04 | Une règle de préséance unique produit un verdict déterministe. |

---

## 8. Priorisation d'exécution

### Phase A — Corrections objectives immédiates

- [ ] CTR-01 — corriger le statut/référencement de `05`.
- [ ] CTR-02 — corriger l'ownership contradictoire de `05` dans `08`.
- [ ] [ ] R-01 — clarifier la nomenclature réelle `02/03`.
- [ ] [ ] Corriger les incohérences documentaires manifestes découvertes lors de ces corrections.
- [ ] [ ] Rejouer les tests CTR-01 / CTR-02.

### Phase B — Arbitrages D1→D7

- [ ] D1 — autorité d'arbitrage, acteurs des transitions, indépendance et gouvernance IA.
- [ ] D2 — classification C3, cumul des changements, vérification et séparation des rôles.
- [ ] D3 — temporalité, `usable_from/usable_to`, préséance avec `04`, champs obligatoires et blocage.
- [ ] D4 — ownership/application, adoption normative, usage limits et gouvernance dataset.
- [ ] D5 — changement matériel du consommateur et déclenchement de réévaluation.
- [ ] D6 — modification de `13`, auto-application et contrôle de classification.
- [ ] D7 — cycle de vie complet de SAFE HOLD.

### Phase C — Contre-expertise et re-test adversarial

- [ ] Rejouer S-01 → S-10.
- [ ] Vérifier que les corrections n'introduisent pas de nouvelles contradictions.
- [ ] Vérifier que chaque nouvelle règle possède un owner et une autorité d'adoption.
- [ ] Vérifier que les machines d'état sont déterministes.
- [ ] Recalculer le verdict global GO / GO sous réserve / NO-GO.

---

## 9. Règles de clôture d'un finding

Un finding ne peut passer à `RESOLVED` que si :

1. l'action a été exécutée ;
2. l'owner est identifié ;
3. l'arbitration requirement a été satisfait lorsqu'il est `OUI` ;
4. la modification est traçable ;
5. le test de revalidation requis a été exécuté ;
6. le résultat du re-test est enregistré ;
7. aucun finding de régression bloquant n'a été créé par la correction.

Les états autorisés sont :

```text
OPEN
IN_PROGRESS
PENDING_ARBITRATION
PENDING_RETEST
RESOLVED
DEFERRED
REJECTED
```

`DEFERRED` ne signifie pas `RESOLVED`.

---

## 10. État initial du registre

**Verdict hérité de l'audit adversarial : `NO-GO`.**

Le registre ne modifie pas ce verdict. Il organise son traitement.

Les deux contradictions `CTR-01` et `CTR-02` constituent la priorité immédiate de **Phase A**. Les lacunes G5 `LAC-16` et `LAC-16b` restent bloquantes et seront traitées dans **Phase B**, car leur résolution nécessite une décision de gouvernance/autorité.

**Aucune décision D1→D7 ne doit être inventée dans ce registre.** Lorsqu'un finding exige une décision normative, le champ `ARBITRATION_REQUIRED` reste `OUI` jusqu'à ce que la décision correspondante soit explicitement adoptée et enregistrée.
