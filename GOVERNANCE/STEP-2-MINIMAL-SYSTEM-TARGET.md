# ÉTAPE 2 — Cible minimale opérationnelle du système

**Statut :** CIBLE CANDIDATE CORRIGÉE — à geler après contrôle final de l'ÉTAPE 2
**Branche :** `feat/step2-minimal-system-target`
**Périmètre :** définition de la cible uniquement. Aucun composant nouveau, aucune implémentation CONTEXT, CI ou temporalité n'est autorisé ici.

## 1. Finalité

Définir le plus petit système capable de démontrer une chaîne complète de décision, d'action, de résultat, d'apprentissage et de gouvernance, sans transformer les fonctions en architecture technique.

La fondation du projet définit la finalité comme l'amélioration durable des décisions sous incertitude, avec valeur mesurable et maîtrise du risque/coût. Elle rappelle également que la capacité ne vaut que par son effet démontré sur décision, action, résultat et valeur. La gouvernance impose en parallèle de réutiliser l'existant avant toute nouvelle couche.

## 2. Cible minimale

La cible comporte une **colonne vertébrale de provenance** et une **boucle de connaissance/gouvernance**.

### 2.1 Colonne vertébrale

**DONNÉE → CONTEXTE → RECHERCHE / EXPÉRIENCE → DÉCISION → ACTION → RÉSULTAT → TRACE**

Cette chaîne est un **parcours de référence complet**. Elle ne signifie pas que chaque décision crée une nouvelle expérience, ni que chaque bloc doit être exécuté de manière synchrone.

`RECHERCHE / EXPÉRIENCE` désigne la base expérimentale ou de connaissance pertinente sur laquelle une décision peut s'appuyer. Une décision peut réutiliser une expérience antérieure ou une connaissance déjà validée.

### 2.2 Boucle de connaissance/gouvernance

**TRACE → MÉMOIRE → AUDIT → RÉVISION → nouvelle RECHERCHE / EXPÉRIENCE**

Cette boucle assure la conservation, la contestation et la révision contrôlée. Elle n'impose pas une exécution après chaque résultat : son déclenchement dépendra ultérieurement des règles de criticité, de réévaluation et de promotion.

### 2.3 Vue globale

```text
DONNÉE
   ↓
CONTEXTE
   ↓
BASE DE RECHERCHE / EXPÉRIENCE
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
AUDIT / CONTESTATION
   ↓
RÉVISION CONTRÔLÉE
   └──────────────→ nouvelle RECHERCHE / EXPÉRIENCE
```

Les dix éléments sont des **fonctions à couvrir**, pas dix services, agents, bases ou modules.

## 3. Contrat minimal des fonctions

| Fonction | Question minimale | Entrée minimale | Sortie minimale |
|---|---|---|---|
| DONNÉE | Qu'avons-nous réellement observé/utilisé ? | donnée identifiable + provenance pertinente | donnée identifiable/admissible |
| CONTEXTE | Dans quelles conditions cette donnée/connaissance est-elle pertinente ? | donnée + contexte pertinent | contexte identifiable |
| RECHERCHE / EXPÉRIENCE | Qu'avons-nous testé/appris et quelle connaissance est disponible ? | contexte + hypothèse/objectif/expérience pertinente | expérience/connaissance identifiable + preuves |
| DÉCISION | Quelle décision a été prise et sur quelle base ? | informations/connaissances disponibles + contraintes | décision identifiable |
| ACTION | Quel comportement a effectivement suivi la décision ? | décision | action identifiable, y compris absence d'action contrôlée |
| RÉSULTAT | Qu'est-il effectivement arrivé ? | action + observations du résultat | résultat identifiable |
| TRACE | Peut-on reconstruire les relations entre les éléments ? | identités + relations + preuves disponibles | projection reconstructible |
| MÉMOIRE | Que doit-on conserver pour apprendre/reproduire ? | expérience + résultat + trace + preuves | mémoire d'expérience/connaissance |
| AUDIT | Le chemin et ses conclusions résistent-ils à la contestation ? | trace + mémoire + règles + preuves | constat/verdict/anomalies |
| RÉVISION | Que doit-on modifier, conserver ou retester ? | audit + preuves + décision de révision | nouvelle hypothèse/expérience, maintien ou aucune modification |

## 4. Identité, provenance et preuve : propriétés transversales

`IDENTITÉ`, `PROVENANCE`, `VERSION`, `PREUVE` et `VALIDITÉ` ne sont pas ajoutées comme blocs supplémentaires.

Elles traversent les fonctions et permettent de les relier correctement :

```text
DONNÉE          → identité/provenance
CONTEXTE        → identité + lien vers donnée
EXPÉRIENCE      → identité + contexte + hypothèse + conditions
DÉCISION        → identité + base/connaissances pertinentes
ACTION          → identité + décision
RÉSULTAT        → identité + action + observation
TRACE           → relations de reconstruction
MÉMOIRE         → expérience/connaissance + preuves
AUDIT           → identité + objet audité + verdict/preuves
RÉVISION        → identité + justification + résultat attendu
```

Une trace ne crée jamais les événements qu'elle prétend reconstruire.

## 5. Critère de complétude

Pour un cas donné, la cible doit permettre de répondre à :

1. Quelle donnée ?
2. Dans quel contexte ?
3. Quelle expérience/connaissance pertinente ?
4. Quelle décision ?
5. Quelle action réelle ?
6. Quel résultat réel ?
7. Quelle trace relie ces éléments ?
8. Qu'a-t-on conservé/appris ?
9. Comment cela a-t-il été contesté/audité ?
10. Quelle révision contrôlée en découle, ou pourquoi aucune ?

Si une question critique reste impossible à résoudre, la cible n'est pas complète.

## 6. Critère de minimalité

La cible est minimale si chaque fonction remplit une nécessité distincte :

- sans **DONNÉE**, aucune base observable ;
- sans **CONTEXTE**, aucune délimitation de validité ;
- sans **RECHERCHE / EXPÉRIENCE**, aucune distinction entre observation et connaissance/test ;
- sans **DÉCISION**, aucune liaison vers un choix ;
- sans **ACTION**, aucun comportement réel à évaluer ;
- sans **RÉSULTAT**, aucune observation de conséquence ;
- sans **TRACE**, aucune reconstruction fiable ;
- sans **MÉMOIRE**, perte de l'apprentissage au-delà de l'occurrence ;
- sans **AUDIT**, promotion possible sans contestation suffisante ;
- sans **RÉVISION**, pas de boucle contrôlée de correction/réévaluation.

Cela ne signifie pas que dix composants techniques seront nécessaires.

## 7. Anti-raccourcis

La cible interdit notamment :

```text
DONNÉE ─────────→ DÉCISION
DÉCISION ───────→ RÉSULTAT
RÉSULTAT ───────→ CONNAISSANCE VALIDÉE
CONNAISSANCE ───→ NOUVELLE ACTION
```

sans les relations pertinentes et sans preuve.

Un résultat favorable ne valide pas automatiquement une connaissance. Un résultat n'établit pas automatiquement sa cause. Une mémoire n'autorise pas automatiquement un changement opérationnel. Un audit ne constitue pas une correction automatique.

## 8. Décision sans action et absence de résultat commercial

`DÉCISION` doit pouvoir représenter notamment :

- agir ;
- ne pas agir ;
- réduire l'exposition ;
- suspendre ;
- arrêter ;
- demander une information ou une expérience supplémentaire.

`ACTION` n'est donc pas synonyme d'ordre broker.

La cible n'impose pas qu'une décision produise un résultat financier. Le résultat doit représenter ce qui s'est effectivement produit dans le domaine concerné.

## 9. Promotion contrôlée

Le raccourci suivant est interdit :

```text
RÉSULTAT → modification silencieuse du comportement
```

Le parcours de promotion est conceptuellement :

```text
RÉSULTAT
   ↓
MÉMOIRE
   ↓
AUDIT / CONTESTATION
   ↓
RÉVISION
   ↓
NOUVELLE EXPÉRIENCE / PREUVE
   ↓
AUTORISATION CONTRÔLÉE
   ↓
NOUVEAU COMPORTEMENT
```

Une révision peut conclure **aucun changement**.

## 10. Hors cible minimale

Ne font pas partie de la définition de la cible :

- architecture d'agents ;
- orchestration distribuée ;
- modèle ML particulier ;
- moteur de décision particulier ;
- broker/exchange particulier ;
- stockage particulier ;
- nouvelle couche CONTEXT ;
- CI spécifique ;
- mécanisme de temporalité/look-ahead ;
- métrique universelle d'incertitude ;
- adaptation autonome ;
- stratégie de trading particulière ;
- performance financière ;
- backtest complet ;
- monitoring de production ;
- infrastructure de déploiement.

## 11. Critère de gel de l'ÉTAPE 2

La cible pourra être gelée uniquement lorsque le contrôle adversarial aura confirmé simultanément :

### A — Complétude

Les dix fonctions forment une chaîne de provenance et une boucle de connaissance sans trou sémantique.

### B — Minimalité

Aucune fonction redondante ni nouveau composant technique n'est imposé par la cible.

### C — Non-confusion

Le contrôle distingue explicitement :

- expérience nouvelle vs connaissance expérimentale existante ;
- trace vs producteur d'événements ;
- fonction vs composant technique ;
- audit vs correction ;
- résultat vs causalité ;
- boucle de gouvernance vs pipeline synchrone.

### D — Testabilité

Chaque liaison pourra ultérieurement être attaquée par identité absente, identité étrangère, incohérence, provenance manquante, résultat absent ou raccourci de causalité.

## 12. Statut

**CIBLE MINIMALE CANDIDATE CORRIGÉE.**

Le cassage adversarial initial a révélé quatre ambiguïtés importantes et elles ont été corrigées avant tout gel :

1. une décision n'exige pas une nouvelle expérience ;
2. une trace est une projection de reconstruction, pas un producteur ;
3. mémoire/audit/révision sont une boucle fonctionnelle, pas un pipeline synchrone obligatoire ;
4. les dix éléments sont des fonctions, pas dix composants.

**Aucune implémentation ne doit commencer avant le verdict formel de l'ÉTAPE 2.**
