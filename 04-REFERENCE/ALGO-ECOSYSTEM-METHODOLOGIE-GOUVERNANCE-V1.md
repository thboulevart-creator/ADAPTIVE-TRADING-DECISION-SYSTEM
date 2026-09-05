# ALGO ECOSYSTEM — MÉTHODOLOGIE DE GOUVERNANCE & D'EXÉCUTION

**Version :** 1.0  
**Date :** 5 septembre 2026  
**Statut :** RÉFÉRENCE MÉTHODOLOGIQUE — consolidation des règles déjà établies dans les travaux ALGO ECOSYSTEM

## 0. Objet

Ce document consolide les règles méthodologiques transversales qui doivent être appliquées pendant le travail sur ALGO ECOSYSTEM.

Il ne crée pas de règle métier de trading ni de nouvelle architecture technique. Il rend durables les règles de travail, d'audit, de preuve, de décision et de gouvernance déjà établies dans les discussions et les artefacts du projet.

Les règles métier et décisions architecturales restent dans leurs documents propriétaires respectifs.

---

# 1. INVARIANT D'AUTONOMIE D'EXÉCUTION

Lorsqu'une action suivante est techniquement déterminée par le contexte, les décisions déjà prises et le pipeline en cours, elle doit être exécutée directement.

Il est interdit de remplacer l'exécution par une simple annonce de l'intention d'exécuter.

Séquence obligatoire :

```text
DÉTERMINER
   ↓
EXÉCUTER
   ↓
VÉRIFIER
   ↓
ENCHAÎNER
```

et non :

```text
ANNONCER
   ↓
ATTENDRE
   ↓
DEMANDER À L'UTILISATEUR DE DIRE « FAIS-LE »
```

Une action déjà déterminée ne nécessite pas de confirmation humaine supplémentaire.

L'assistant doit poursuivre automatiquement toutes les sous-actions nécessaires jusqu'à rencontrer un véritable verrou :

1. décision architecturale humaine réelle ;
2. information indispensable réellement absente ;
3. contre-expertise externe réellement nécessaire ;
4. contrainte technique empêchant objectivement de poursuivre.

**L'annonce d'une prochaine étape n'est jamais considérée comme son exécution.**

---

# 2. AUTONOMIE ≠ AUTORITÉ

L'autonomie d'exécution ne donne pas à l'assistant le pouvoir de prendre une décision réservée à l'humain.

L'assistant peut :

- rechercher les preuves ;
- auditer ;
- confronter les documents ;
- produire des tests ;
- identifier les contradictions ;
- proposer des options ;
- exécuter les actions déjà autorisées ;
- vérifier les résultats.

L'assistant ne doit pas transformer une décision humaine non prise en décision implicite.

```text
AUTONOMIE D'EXÉCUTION
        ≠
AUTORITÉ DE DÉCISION
```

---

# 3. PIPELINE DE TRAVAIL OBLIGATOIRE

Le pipeline méthodologique de référence est :

```text
QUESTION OUVERTE
      ↓
AUDIT / VÉRIFICATION DU CORPUS
      ↓
CONTRE-EXPERTISE SI NÉCESSAIRE
      ↓
ADJUDICATION
      ↓
DÉCISION EXPLICITE
      ↓
CORRECTION DU CONTRAT
      ↓
NOUVEL AUDIT ADVERSARIAL
      ↓
VALIDATION / GEL
```

Aucune correction ne doit précéder l'adjudication lorsqu'elle modifie une règle ou un contrat.

Aucune étape aval ne doit être engagée lorsque son prérequis normatif est encore bloqué.

Le plan maître existant utilise déjà le principe `Action → Résultat → Validation → GO/NO-GO → prochaine action` et exige qu'une phase ne passe pas à la suivante sans validation explicite de la précédente. Cette règle est conservée et renforcée ici par l'exigence d'autonomie d'exécution.

---

# 4. RÈGLE DE VÉRITÉ ET DE PREUVE

Objectif permanent : déterminer ce qui est vrai à partir des preuves disponibles, et non démontrer qu'une IA a raison ou tort.

Une conclusion doit être séparée de son niveau de preuve.

Catégories minimales :

```text
FAIT DÉMONTRÉ
INFÉRENCE
CONSÉQUENCE NÉCESSAIRE
ARCHITECTURE PROPOSÉE
QUESTION NON RÉSOLUE
ABSENCE DE PREUVE
EXPOSITION ARCHITECTURALE
VIOLATION ACTUELLE
```

Une absence de preuve n'est jamais transformée en fait.

Une préférence d'architecture n'est jamais transformée en exigence normative sans décision explicite.

---

# 5. BLOCKED NE DEVIENT JAMAIS PASS PAR DÉFAUT

Un contrôle non exécutable, une dépendance non résolue ou une preuve manquante ne peut pas être converti en `PASS` par approximation, substitution ou hypothèse implicite.

Règle :

```text
UNKNOWN / BLOCKED
      ≠
PASS
```

Si un invariant critique reste ambigu, non testable, non déterministe ou non vérifiable, le verdict reste bloqué ou négatif selon le protocole applicable.

Un finding ne disparaît pas parce qu'un document a été modifié ; son traitement et, lorsque requis, son re-test doivent être démontrés.

---

# 6. AUDIT ADVERSARIAL

L'audit ne cherche pas à valider par défaut.

Il cherche à casser la spécification, l'architecture ou l'implémentation avant que le défaut n'atteigne la production.

Toute proposition importante doit être attaquée par :

- contre-exemples ;
- cas limites ;
- contradictions ;
- changements de contexte ;
- dépendances cachées ;
- réordonnancement ;
- extension temporelle ;
- perte d'information ;
- comportement au redémarrage ;
- différences d'environnement ;
- chemins indirects de look-ahead/leakage.

Un test qui passe n'est pas une preuve suffisante si le test ne discrimine pas réellement le défaut recherché.

---

# 7. DISTINCTION OBLIGATOIRE DES ÉTATS D'UN FINDING

Pour chaque problème, distinguer explicitement :

### VIOLATION ACTUELLE
Une règle en vigueur est démontrablement violée.

### EXPOSITION ARCHITECTURALE
L'architecture permet encore un comportement dangereux, sans preuve qu'il se produit actuellement.

### ABSENCE DE PREUVE
Le corpus ou les tests ne permettent pas d'établir la conformité.

### QUESTION NON RÉSOLUE
Une décision nécessaire n'a pas encore été prise.

### CONSÉQUENCE NÉCESSAIRE
La conclusion découle logiquement d'une règle déjà établie, sans constituer une nouvelle décision.

### ARCHITECTURE PROPOSÉE
Une solution raisonnable est identifiée mais n'est pas encore normative.

Cette distinction doit apparaître dans les audits et adjudications.

---

# 8. CORPUS RÉEL AVANT MÉMOIRE

Le dépôt GitHub est la source de vérité documentaire du projet.

Le corpus réel doit être vérifié avant toute affirmation sur l'état du projet.

Les noms de fichiers historiques ou supposés ne doivent pas être utilisés comme s'ils existaient encore. `00-CORPUS-INDEX.md` fixe les noms réels du corpus et rappelle cette règle. fileciteturn170file0L2-L2

Une conversation, un résumé, une mémoire ou une hypothèse ne peut pas remplacer la vérification du dépôt lorsqu'une affirmation porte sur l'état matériel du projet.

---

# 9. GOUVERNANCE DES DOCUMENTS

Une idée importante doit être conservée dans un artefact durable dès qu'elle est suffisamment identifiée pour être réutilisée.

Une idée n'est pas automatiquement une vérité validée.

Les statuts doivent rester explicites :

```text
HYPOTHÈSE
PRINCIPE DE CONCEPTION
INVARIANT VALIDÉ
```

Le document de référence transversal existant applique déjà cette séparation et sert de mémoire architecturale/méthodologique. fileciteturn158file0L2-L2

---

# 10. DÉCISIONS HUMAINES

Les décisions architecturales importantes appartiennent au pilote humain.

Une IA peut confronter des options et démontrer leurs conséquences, mais elle ne doit pas créer silencieusement une décision normative.

Une contradiction entre deux analyses IA n'est pas résolue par moyenne, majorité ou consensus automatique.

Le propriétaire du concept et le processus d'arbitrage déterminent la décision.

Le protocole existant de `11 — CONTRADICTION & ARBITRATION REGISTRY` impose déjà la séparation entre détection, qualification, analyse, arbitrage, décision, raison et version. fileciteturn179file0L2-L2

---

# 11. CONTRE-EXPERTISE EXTERNE

La contre-expertise de Claude, Grok, Perplexity ou d'une autre source externe n'est pas obligatoire mécaniquement avant chaque décision.

Elle est utilisée lorsque l'indépendance supplémentaire est susceptible d'augmenter matériellement la robustesse de la décision.

Avant une décision importante, le système doit déterminer quelle méthode de vérification maximise la correction :

- corpus direct ;
- audit adversarial ;
- deuxième implémentation/référence ;
- contre-expertise externe ;
- combinaison de plusieurs méthodes.

Une contre-expertise reste une preuve/analyse externe et non l'autorité finale.

---

# 12. GEL ET CONTESTATION

`FROZEN` signifie : modification contrôlée.

`FROZEN` ne signifie pas : intouchable.

Une brique aval peut contester un contrat amont lorsqu'elle possède des preuves vérifiables, sans acquérir automatiquement le droit de le modifier.

```text
CONTESTER ≠ MODIFIER ≠ ARBITRER
```

Le protocole `12 — UPWARD CHALLENGE` formalise déjà cette séparation. fileciteturn181file0L2-L2

---

# 13. GOUVERNANCE DE CRITICITÉ

La profondeur d'audit doit être proportionnelle à l'impact potentiel, pas à la taille du changement documentaire.

Le protocole `13 — CRITICALITY & AUDIT PROTOCOL` définit notamment C0/C1/C2/C3 et impose une escalade lorsque la criticité est incertaine. Il exige également un audit adversarial complet pour les changements C3. fileciteturn190file0L2-L2

En cas de doute entre deux niveaux de criticité, le niveau supérieur est retenu provisoirement jusqu'à preuve permettant de réduire la criticité.

---

# 14. NON-DÉRIVE

Ne jamais étendre silencieusement le périmètre d'un contrat.

Une brique doit rester propriétaire de son concept et ne pas absorber progressivement :

- la logique d'une autre couche ;
- une décision non arbitrée ;
- une convention technique non décidée ;
- une responsabilité appartenant à une autre autorité.

Une bonne solution locale ne justifie pas l'extension silencieuse du périmètre.

---

# 15. HISTORIQUE ET TEMPORALITÉ

Une décision actuelle ne doit pas être présentée comme si elle avait toujours été connue.

Distinguer :

```text
ce qui était vrai à l'époque
ce qui était connu à l'époque
ce qui a été découvert ensuite
ce qui a été décidé ensuite
```

Le contrat temporel existant formalise cette distinction au niveau architectural, notamment entre vérité du monde, connaissance, utilisation et temps d'exécution, mais son statut doit être respecté lorsqu'il n'est pas encore normatif. fileciteturn169file0L2-L2

---

# 16. REPRODUCTIBILITÉ

Toute conclusion importante doit être reliée autant que possible à :

```text
DATASET
VERSION
CONFIGURATION
CODE / OUTIL
CALENDRIER
DATE
RÉSULTAT
PREUVES
```

Une modification importante doit être traçable.

Le résultat d'un backtest, d'un audit ou d'une validation n'est pas considéré comme reproductible uniquement parce qu'un fichier de résultat existe.

La provenance complète doit pouvoir être reconstruite à partir des artefacts disponibles.

---

# 17. DONNÉES ET BACKTESTS

Un backtest rentable ne constitue jamais à lui seul une preuve de robustesse.

Les contrôles doivent considérer, selon le contexte :

- données manquantes ;
- doublons ;
- ordre des observations ;
- timestamps ;
- fuseaux horaires ;
- gaps ;
- spread ;
- commissions ;
- slippage ;
- liquidité ;
- exécution partielle ;
- rejets ;
- redémarrages ;
- exposition ;
- levier ;
- limites de risque ;
- kill switch ;
- look-ahead ;
- repainting ;
- stabilité hors échantillon ;
- walk-forward ;
- sensibilité aux paramètres.

Pour les backtests MT5 visant la fidélité maximale aux données réelles, le paramètre de testeur à utiliser est `Every tick based on real ticks` lorsque ce mode est disponible et pertinent.

---

# 18. PAPER / LIVE

Pour les algorithmes destinés à l'exploitation :

```text
PAPER = mode par défaut
LIVE  = activation explicite
```

Le passage en LIVE ne doit pas être artificiellement interdit après validation du PAPER.

Il doit être :

- explicite ;
- visible dans la configuration ;
- enregistré dans les logs ;
- précédé des vérifications prévues par le protocole applicable.

Cette règle ne crée pas à elle seule une autorisation de trading : elle conserve la séparation entre sécurité technique et décision humaine d'activation.

---

# 19. RÈGLE DE CONSTRUCTION DES TESTS

Chaque exigence importante doit pouvoir être reliée à un test discriminant.

Un test doit indiquer au minimum :

```text
OBJECTIF
ENTRÉE
ÉTAT INITIAL
COMPORTEMENT ATTENDU
ATTAQUE / CONTRE-EXEMPLE
CRITÈRE PASS
CRITÈRE FAIL
PREUVE CONSERVÉE
```

Un contrôle impossible à exécuter ne doit pas être présenté comme réussi.

---

# 20. CHANGEMENTS ET CORRECTIONS

Avant correction d'une règle ou d'un contrat :

```text
FINDING
  ↓
CLASSIFICATION
  ↓
ADJUDICATION
  ↓
DÉCISION
  ↓
CORRECTION AUTORISÉE
  ↓
RETEST
  ↓
NOUVEL AUDIT SI NÉCESSAIRE
```

Une correction doit être minimale par rapport à la décision qui l'autorise.

Une correction ne doit pas profiter de l'occasion pour introduire d'autres règles non arbitrées.

---

# 21. RÈGLE DE PROTECTION CONTRE LA DÉRIVE DES CONVERSATIONS

Les discussions sont un espace de travail, pas une source durable suffisante.

Lorsqu'une règle est jugée importante et doit survivre à :

- un changement de conversation ;
- un changement de modèle ;
- une perte de contexte ;
- une limitation de mémoire ;
- une reprise du projet plusieurs jours plus tard ;

elle doit être matérialisée dans le dépôt ou dans le registre de référence approprié.

Aucune règle critique ne doit dépendre uniquement du fait qu'une IA « se souvient » de l'avoir vue.

---

# 22. RÈGLE DE RÉCUPÉRATION DES RÈGLES HISTORIQUES

Lorsqu'une règle antérieure est suspectée d'avoir existé uniquement dans une discussion :

1. rechercher les artefacts du projet et les documents importés disponibles ;
2. rechercher les décisions et audits qui l'ont déjà matérialisée ;
3. comparer avec l'état Git réel ;
4. distinguer règle confirmée, proposition, hypothèse et règle non retrouvée ;
5. ne jamais recréer comme fait une règle dont le contenu exact n'est pas suffisamment établi ;
6. si une règle importante est confirmée mais absente du dépôt, la consigner dans le document de référence approprié avec son statut réel ;
7. si sa nature est normative et que son propriétaire doit être identifié, ouvrir l'adjudication correspondante avant de la rendre normative.

Cette procédure transforme la mémoire historique en travail vérifiable au lieu de dépendre d'un souvenir implicite.

---

# 23. ÉTAT DE CONSOLIDATION AU 5 SEPTEMBRE 2026

Règles déjà matériellement présentes dans le dépôt :

- action → résultat → validation → GO/NO-GO ;
- distinction proposition / norme ;
- audit adversarial ;
- arbitrage avant correction ;
- conservation des contradictions ;
- distinction ownership / producteur / consommateur ;
- challenge ascendant ;
- criticité proportionnelle à l'impact ;
- point-in-time / look-ahead comme préoccupations méthodologiques ;
- reproductibilité ;
- principes transversaux et statuts HYPOTHÈSE / PRINCIPE / INVARIANT. fileciteturn196file0L2-L2

Règle ajoutée durablement par cette consolidation :

> **AUTONOMIE D'EXÉCUTION : lorsqu'une action est déterminée et exécutable, l'assistant l'exécute directement au lieu de seulement l'annoncer.**

Règle également consolidée :

> **Une règle importante ne doit pas rester dépendante de la mémoire d'une conversation ; elle doit être matérialisée dans un artefact durable avec son statut et son propriétaire appropriés.**

---

# 24. LIMITATION DE CETTE CONSOLIDATION

Cette V1 consolide les règles historiques que les artefacts accessibles, les discussions de projet actuellement récupérables et le corpus Git permettent d'établir avec suffisamment de confiance.

Elle ne prétend pas démontrer qu'elle contient littéralement chaque phrase jamais prononcée dans toutes les conversations du dossier ALGO ECOSYSTEM.

Une règle non retrouvée ne doit pas être inventée.

Toute nouvelle règle historique retrouvée ultérieurement doit être ajoutée avec :

```text
SOURCE
DATE / CONTEXTE
STATUT
PROPRIÉTAIRE
PREUVE
```

et, lorsqu'elle est normative, passer par la gouvernance appropriée avant adoption.

---

## FIN — ALGO ECOSYSTEM MÉTHODOLOGIE V1
