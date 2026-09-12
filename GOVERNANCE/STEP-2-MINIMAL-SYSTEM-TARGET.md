# ÉTAPE 2 — Cible minimale opérationnelle du système

**Statut :** CIBLE CANDIDATE — à geler après contrôle adversarial de l'ÉTAPE 2
**Branche :** `feat/step2-minimal-system-target`
**Base :** manifeste candidat gelé de l'ÉTAPE 1
**Périmètre :** définition de la cible minimale uniquement. Aucun nouveau composant, aucune implémentation CONTEXT, CI ou temporalité n'est autorisé par ce document.

---

## 1. Objectif de l'ÉTAPE 2

Définir le plus petit système qui permet de démontrer la chaîne de valeur du projet sans confondre :

- la cible fonctionnelle ;
- les composants techniques qui l'implémenteront plus tard ;
- les mécanismes de gouvernance ;
- les capacités futures.

La cible doit être assez complète pour permettre une reconstruction de bout en bout, mais assez minimale pour ne pas imposer prématurément une architecture.

La gouvernance impose de rechercher d'abord les mécanismes existants et de ne créer une couche que lorsqu'un manque est démontré. citeGOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL

---

## 2. Cible minimale gelable

La cible est constituée de deux boucles complémentaires.

### 2.1 Colonne vertébrale opérationnelle

**DONNÉE → CONTEXTE → RECHERCHE / EXPÉRIENCE → DÉCISION → ACTION → RÉSULTAT → TRACE**

Cette chaîne répond à la question minimale :

> **À partir de quelle information et dans quelles conditions une expérience a-t-elle conduit à une décision, quelle action en a résulté, quel résultat a été obtenu et peut-on reconstruire le chemin ?**

### 2.2 Boucle de connaissance et de gouvernance

**TRACE → MÉMOIRE → AUDIT → RÉVISION → nouvelle RECHERCHE / EXPÉRIENCE**

Cette boucle répond à la seconde question :

> **Que faisons-nous de ce qui vient de se produire, comment savons-nous si notre compréhension est fiable, et comment une révision contrôlée peut-elle produire une nouvelle expérience ?**

### 2.3 Vue globale

```text
DONNÉE
   ↓
CONTEXTE
   ↓
RECHERCHE / EXPÉRIENCE
   ↓
DÉCISION
   ↓
ACTION
   ↓
RÉSULTAT
   ↓
TRACE
   ↓
MÉMOIRE
   ↓
AUDIT
   ↓
RÉVISION
   └──────────────→ nouvelle RECHERCHE / EXPÉRIENCE
```

**Important :** `TRACE`, `MÉMOIRE`, `AUDIT` et `RÉVISION` ne sont pas quatre nouvelles architectures imposées. Ce sont quatre fonctions que la cible doit pouvoir couvrir. Leur implémentation devra réutiliser l'existant autant que possible.

---

## 3. Contrat minimal de chaque bloc

| Bloc | Question minimale | Entrée indispensable | Sortie indispensable | Ce qui n'est PAS requis à ce stade |
|---|---|---|---|---|
| DONNÉE | Qu'avons-nous réellement observé/utilisé ? | donnée identifiable + provenance | donnée admissible/identifiable | moteur de trading |
| CONTEXTE | Dans quelles conditions cette donnée est-elle interprétée ? | donnée + paramètres de contexte pertinents | contexte identifiable | indicateurs, signal, décision |
| RECHERCHE / EXPÉRIENCE | Qu'avons-nous voulu tester/apprendre ? | contexte + hypothèse/objectif + conditions | expérience identifiable + résultat de recherche | moteur d'adaptation autonome |
| DÉCISION | Quelle décision a été prise et sur quelle base ? | expérience/connaissances disponibles + contraintes | décision identifiable | performance future supposée |
| ACTION | Qu'a fait le système à la suite de la décision ? | décision | action identifiable | exécution broker complète à ce stade |
| RÉSULTAT | Qu'est-il effectivement arrivé ? | action + observation du résultat | résultat identifiable | interprétation automatique de la cause |
| TRACE | Peut-on reconstruire le chemin ? | identités des éléments disponibles | trace reconstructible | nouvelle logique métier |
| MÉMOIRE | Qu'est-ce qui doit être conservé pour apprendre ? | trace + expérience + résultat + preuve pertinente | mémoire d'expérience/connaissance | apprentissage autonome non contrôlé |
| AUDIT | Le chemin et ses conclusions résistent-ils à la contestation ? | trace + mémoire + règles/preuves | constat/verdict + anomalies | autorisation implicite de modification |
| RÉVISION | Que peut-on modifier et pourquoi ? | audit + preuve + décision de révision | nouvelle hypothèse/expérience ou maintien | modification silencieuse du comportement |

---

## 4. Identité : une propriété transversale, pas un bloc supplémentaire

Chaque bloc doit pouvoir être distingué de ses voisins et relié à eux par des identifiants appropriés.

Mais `IDENTITÉ` n'est **pas** ajoutée comme onzième bloc.

Elle est une propriété transversale des objets de la chaîne :

```text
DONNÉE          → data identity
CONTEXTE        → context identity
EXPÉRIENCE      → research/experiment identity
DÉCISION        → decision identity
ACTION          → action identity
RÉSULTAT        → result identity
TRACE           → reconstruction identity / links
MÉMOIRE         → experiment/knowledge identity
AUDIT           → audit identity
RÉVISION        → revision identity
```

Même règle pour provenance, version et preuve : ils sont des attributs/relations nécessaires, pas automatiquement des blocs supplémentaires.

---

## 5. Critère de complétude minimale

La cible est complète si, pour un cas donné, le système peut répondre de manière reconstructible à ces dix questions :

1. **Quelle donnée ?**
2. **Dans quel contexte ?**
3. **Quelle expérience/hypothèse ?**
4. **Quelle décision ?**
5. **Quelle action ?**
6. **Quel résultat ?**
7. **Quelle trace relie les éléments ?**
8. **Qu'a-t-on appris ou conservé ?**
9. **Comment cela a-t-il été audité/contesté ?**
10. **Quelle révision contrôlée en découle, ou pourquoi aucune ?**

Si une question critique reste impossible à répondre, la chaîne n'est pas complète.

---

## 6. Critère de minimalité

La cible est minimale si la suppression d'un bloc provoque la perte d'une capacité indispensable de la boucle.

### Suppression de DONNÉE
Impossible de savoir sur quoi repose le système.

### Suppression de CONTEXTE
Impossible de déterminer dans quelles conditions une information ou une connaissance est valable.

### Suppression de RECHERCHE / EXPÉRIENCE
Impossible de distinguer observation brute et apprentissage/test contrôlé.

### Suppression de DÉCISION
Impossible de relier connaissance et choix opérationnel.

### Suppression d'ACTION
Impossible de distinguer décision et comportement effectivement produit.

### Suppression de RÉSULTAT
Impossible d'évaluer ce qui est réellement arrivé.

### Suppression de TRACE
Impossible de reconstruire la chaîne complète.

### Suppression de MÉMOIRE
L'expérience disparaît comme connaissance exploitable au-delà de son occurrence.

### Suppression d'AUDIT
Une expérience peut être capitalisée sans contestation suffisante.

### Suppression de RÉVISION
Le système peut observer et apprendre sans mécanisme contrôlé de correction ou de nouvelle expérimentation.

Ainsi, les dix fonctions sont nécessaires à la **cible complète**, mais cela ne signifie pas dix composants techniques.

---

## 7. Ce qui est explicitement hors cible minimale

Les éléments suivants ne sont pas nécessaires pour définir la cible de l'ÉTAPE 2 :

- architecture d'agents ;
- orchestration distribuée ;
- modèle ML particulier ;
- moteur de décision particulier ;
- broker/exchange particulier ;
- système de stockage particulier ;
- nouvelle couche CONTEXT ;
- CI spécifique ;
- mécanisme de temporalité/look-ahead ;
- métrique universelle d'incertitude ;
- système d'adaptation autonome ;
- stratégie de trading particulière ;
- performance financière ;
- backtest complet ;
- monitoring de production ;
- infrastructure de déploiement.

Ces éléments peuvent devenir nécessaires dans les étapes prévues, mais ne définissent pas la cible minimale elle-même.

---

## 8. Propriété fondamentale : pas de raccourci causal

La cible interdit les raccourcis suivants :

```text
DONNÉE ─────────────→ DÉCISION
DÉCISION ───────────→ RÉSULTAT
RÉSULTAT ───────────→ CONNAISSANCE VALIDÉE
CONNAISSANCE ───────→ NOUVELLE ACTION
```

sans les relations intermédiaires pertinentes et sans preuve.

En particulier :

- une donnée ne constitue pas une décision ;
- un résultat favorable ne constitue pas à lui seul une connaissance validée ;
- une décision ne prouve pas qu'une action a eu lieu ;
- une action ne prouve pas son résultat ;
- un résultat ne prouve pas sa cause ;
- une trace ne crée pas les événements qu'elle prétend reconstruire ;
- une mémoire ne transforme pas automatiquement une hypothèse en connaissance validée ;
- un audit ne doit pas être confondu avec la correction qu'il pourrait recommander.

Cette règle est essentielle pour empêcher que la cible soit satisfaite uniquement par des objets documentaires ou des identifiants sans continuité réelle.

---

## 9. Propriété fondamentale : absence d'action valide

`DÉCISION` doit pouvoir représenter au minimum :

- agir ;
- ne pas agir ;
- réduire l'exposition ;
- suspendre ;
- arrêter ;
- demander une information/expérience supplémentaire lorsque cela est pertinent.

La cible n'est donc pas définie comme une machine qui transforme systématiquement une observation en trade.

Cela découle directement de la fondation du projet : ne pas agir est une décision valide.

---

## 10. Propriété fondamentale : promotion contrôlée

La boucle minimale ne permet pas :

```text
RÉSULTAT → modification silencieuse du comportement opérationnel
```

Le chemin autorisé est :

```text
RÉSULTAT
   ↓
MÉMOIRE
   ↓
AUDIT / CONTESTATION
   ↓
RÉVISION CONTRÔLÉE
   ↓
NOUVELLE EXPÉRIENCE
   ↓
PREUVE
   ↓
AUTORISATION
   ↓
NOUVEAU COMPORTEMENT
```

Ceci reprend la contrainte de mémoire expérimentale et d'adaptation contrôlée existante : les connaissances non validées ne doivent pas modifier silencieusement le comportement opérationnel.

---

## 11. Critère d'acceptation de l'ÉTAPE 2

L'ÉTAPE 2 pourra être considérée comme correctement définie lorsque les trois conditions suivantes seront satisfaites :

### A — Complétude fonctionnelle

La chaîne complète `DONNÉE → CONTEXTE → RECHERCHE/EXPÉRIENCE → DÉCISION → ACTION → RÉSULTAT → TRACE → MÉMOIRE → AUDIT → RÉVISION` est définie sans trou sémantique.

### B — Minimalité architecturale

Aucun composant technique nouveau n'est implicitement requis par la définition de la cible. Les blocs sont des fonctions à couvrir, pas des services à construire.

### C — Testabilité

Chaque liaison peut ultérieurement être testée par présence, identité, cohérence, provenance et résistance au bypass. La cible doit donc pouvoir être transformée en parcours synthétique adversarial à l'ÉTAPE 4 sans modifier son sens.

---

## 12. Verdict de ce document

Ce document est une **cible candidate**, pas encore une clôture automatique de l'ÉTAPE 2.

La prochaine opération de l'ÉTAPE 2 doit être uniquement :

> **Casser la cible minimale elle-même pour rechercher les ambiguïtés, raccourcis et blocs qui seraient en réalité inutiles ou insuffisamment définis.**

Aucune implémentation ne doit précéder ce contrôle.
