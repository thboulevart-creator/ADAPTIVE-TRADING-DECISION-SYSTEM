# ALGO ECOSYSTEM — PROTOCOLE DE CONSTRUCTION, COMPARAISON & CASSAGE DES RÉPONSES

**Version :** 1.0  
**Date :** 5 septembre 2026  
**Statut :** RÉFÉRENCE MÉTHODOLOGIQUE  
**Dépendance :** `ALGO-ECOSYSTEM-METHODOLOGIE-GOUVERNANCE-V1.md`

---

## 0. OBJET

Ce protocole définit la méthode de référence à appliquer aux questions importantes susceptibles de produire une décision architecturale, normative, méthodologique ou de gouvernance.

L'objectif n'est pas seulement d'obtenir une réponse.

L'objectif est de produire une réponse :

- construite à partir d'un raisonnement explicite ;
- justifiée par des preuves ;
- comparée à une ou plusieurs réponses indépendantes ;
- sélectionnée selon des critères explicites ;
- puis attaquée adversarialement afin de rechercher ses faiblesses, ses hypothèses cachées et ses incomplétudes.

Le protocole vise à déplacer progressivement le travail humain de :

```text
CHERCHER LA RÉPONSE
```

vers :

```text
COMPRENDRE
ARBITRER
VALIDER
```

lorsqu'une décision humaine réelle reste nécessaire.

---

# 1. PRINCIPE CENTRAL

Une réponse ne doit jamais être considérée comme fiable uniquement parce qu'elle est convaincante, détaillée ou produite par une IA réputée compétente.

Une réponse doit être traitée comme une **candidature à la vérité ou à la décision** jusqu'à ce que son raisonnement, ses preuves, ses alternatives et sa résistance aux attaques aient été examinés.

Principe :

```text
RÉPONSE
   ≠
RÉPONSE VALIDÉE
```

Le protocole distingue donc obligatoirement :

```text
CONSTRUCTION
COMPARAISON
SÉLECTION
CASSAGE
VALIDATION
DÉCISION
```

---

# 2. PIPELINE DE RÉFÉRENCE

Pour une question importante :

```text
QUESTION
   ↓
DÉFINITION EXACTE DU PROBLÈME
   ↓
RÉPONSE 1 — CONSTRUCTION EXPLICITE
   ↓
AUDIT DU RAISONNEMENT DE RÉPONSE 1
   ↓
RÉPONSE 2 — CONSTRUCTION INDÉPENDANTE
   ↓
[ RÉPONSE 3 SI NÉCESSAIRE ]
   ↓
COMPARAISON
   ↓
CONVERGENCES / DIVERGENCES / HYPOTHÈSES
   ↓
ÉLIMINATION DES RÉPONSES INSUFFISANTES
   ↓
RÉPONSE CANDIDATE RETENUE
   ↓
CASSAGE ADVERSARIAL
   ↓
RECHERCHE DE FAILLES / INCOMPLÉTUDES
   ↓
CORRECTION OU REJET
   ↓
RE-CASSAGE SI CORRECTION
   ↓
RÉPONSE ROBUSTE
   ↓
DÉCISION HUMAINE UNIQUEMENT SI NÉCESSAIRE
```

La décision humaine ne doit donc pas intervenir au début pour demander à l'humain de trouver lui-même la solution technique.

Elle intervient après réduction de l'espace des solutions par l'analyse.

---

# 3. PHASE 1 — DÉFINIR LA QUESTION

Avant de chercher une réponse, le système doit déterminer :

1. la question exacte ;
2. le périmètre ;
3. les documents applicables ;
4. les contraintes déjà gelées ;
5. les décisions qui ne peuvent pas être modifiées ;
6. les éléments encore inconnus ;
7. le critère permettant de considérer une réponse comme suffisante.

Une question ambiguë ne doit pas être transformée silencieusement en une question plus facile.

Si plusieurs interprétations sont possibles et qu'elles peuvent modifier le résultat, elles doivent être explicitées avant la construction de la réponse.

---

# 4. PHASE 2 — RÉPONSE 1 : CONSTRUCTION DU RAISONNEMENT

La première réponse doit être produite comme une démonstration contrôlée, et non comme une conclusion isolée.

Elle doit permettre de reconstruire :

```text
QUESTION
   ↓
FAITS UTILISÉS
   ↓
RÈGLES APPLICABLES
   ↓
HYPOTHÈSES
   ↓
INFÉRENCES
   ↓
OPTIONS ENVISAGÉES
   ↓
CRITÈRES DE CHOIX
   ↓
CONCLUSION
```

La question obligatoire n'est pas seulement :

> « Quelle est la réponse ? »

mais également :

> « Quel raisonnement produit cette réponse, quelles prémisses la rendent possible et pourquoi cette réponse plutôt qu'une autre ? »

---

# 5. FICHE DE CONSTRUCTION DE LA RÉPONSE 1

Pour toute décision importante, la première réponse doit autant que possible fournir :

### 5.1 Réponse

La conclusion candidate.

### 5.2 Preuves

Les faits documentaires ou techniques utilisés.

### 5.3 Raisonnement

La chaîne logique reliant les preuves à la conclusion.

### 5.4 Hypothèses

Les hypothèses nécessaires mais non démontrées.

### 5.5 Alternatives

Les solutions sérieusement envisageables mais non retenues.

### 5.6 Pourquoi cette réponse

Les raisons précises pour lesquelles la réponse candidate domine les alternatives connues.

### 5.7 Conditions de validité

Les conditions sous lesquelles la réponse resterait correcte.

### 5.8 Faiblesses connues

Les points que la première analyse ne parvient pas à démontrer complètement.

Une réponse qui ne peut pas expliquer pourquoi elle est vraie ou préférable est une réponse incomplètement construite.

---

# 6. PHASE 3 — AUDIT DE LA CONSTRUCTION

Avant de demander une deuxième réponse, la première doit être auditée sur sa propre construction.

Rechercher notamment :

- prémisse non démontrée ;
- saut logique ;
- hypothèse cachée ;
- alternative ignorée ;
- définition ambiguë ;
- dépendance documentaire non vérifiée ;
- confusion entre fait et conséquence ;
- confusion entre architecture proposée et exigence normative ;
- conclusion plus forte que les preuves ;
- circularité ;
- raisonnement dépendant de la conclusion elle-même.

Cette étape ne valide pas la réponse.

Elle vérifie seulement que le raisonnement présenté est intelligible et falsifiable.

---

# 7. PHASE 4 — RÉPONSE 2 INDÉPENDANTE

La deuxième réponse doit être construite indépendamment de la première autant que possible.

Elle ne doit pas recevoir la première réponse comme vérité de référence lorsque l'objectif est de mesurer l'indépendance du raisonnement.

Elle doit répondre à la même question à partir du même corpus et des mêmes contraintes, mais en reconstruisant son propre chemin logique.

Elle doit également fournir :

- sa conclusion ;
- ses preuves ;
- son raisonnement ;
- ses hypothèses ;
- ses alternatives ;
- les raisons de son choix ;
- ses limites.

Une deuxième réponse qui se contente de paraphraser la première ne constitue pas une véritable contre-expertise indépendante.

---

# 8. RÉPONSE 3 — UTILISATION CONDITIONNELLE

Une troisième réponse indépendante peut être sollicitée lorsque :

- les deux premières réponses divergent sur un point critique ;
- une décision est difficilement réversible ;
- le risque de mauvaise interprétation est élevé ;
- une troisième perspective peut réellement discriminer les options.

La troisième réponse n'est pas obligatoire mécaniquement.

Elle doit apporter une information nouvelle ou une capacité de falsification supplémentaire.

---

# 9. PHASE 5 — COMPARAISON DES RÉPONSES

Les réponses ne doivent pas être comparées uniquement sur leur conclusion.

La comparaison doit porter sur :

```text
CONCLUSION
PREUVES
RAISONNEMENT
HYPOTHÈSES
ALTERNATIVES
LIMITES
RISQUES
CONDITIONS DE VALIDITÉ
```

La synthèse doit produire au minimum :

```text
CONVERGENCES
DIVERGENCES
HYPOTHÈSES DIFFÉRENTES
POINTS NON DÉMONTRÉS
RISQUES UNIQUEMENT IDENTIFIÉS PAR UNE RÉPONSE
OPTIONS ÉLIMINÉES
QUESTIONS RESTANTES
```

Une majorité de réponses ne constitue pas une preuve.

Une convergence peut être un signal de robustesse, mais elle ne remplace pas une preuve.

---

# 10. PHASE 6 — ÉLIMINATION

Avant de sélectionner une réponse, rechercher activement pourquoi chaque réponse pourrait être insuffisante.

Une réponse peut être éliminée si elle :

- contredit le corpus ;
- dépend d'une hypothèse non autorisée ;
- crée une nouvelle décision sans autorité ;
- ne couvre pas un cas critique ;
- détruit une information nécessaire ;
- introduit une ambiguïté ;
- n'est pas déterministe ;
- ne permet pas de vérifier son propre résultat ;
- ne résiste pas à un contre-exemple déjà connu.

Le but n'est pas de conserver la réponse qui semble la plus élégante.

Le but est de conserver la réponse qui résiste le mieux aux critères de validité.

---

# 11. PHASE 7 — SÉLECTION D'UNE RÉPONSE CANDIDATE

Une seule réponse candidate doit être retenue pour le cassage approfondi lorsque la comparaison permet de réduire l'espace des solutions.

La sélection doit indiquer :

```text
RÉPONSE RETENUE
POURQUOI
RÉPONSES ÉLIMINÉES
POURQUOI
RISQUES RESTANTS
```

Cette sélection n'est pas encore une validation définitive.

Elle signifie seulement :

> « C'est actuellement la meilleure candidate connue ; maintenant nous allons essayer de la détruire. »

---

# 12. PHASE 8 — CASSAGE ADVERSARIAL

La réponse candidate doit ensuite être attaquée comme si l'objectif était de démontrer qu'elle est fausse, incomplète ou dangereuse.

Chercher notamment :

### 12.1 Contre-exemples

Construire des cas où la réponse échoue.

### 12.2 Cas limites

Tester les frontières du domaine.

### 12.3 Cas adverses

Construire volontairement les situations les plus défavorables à la réponse.

### 12.4 Alternatives oubliées

Chercher une solution non considérée pendant la construction.

### 12.5 Hypothèses cachées

Retirer une hypothèse et vérifier si la conclusion tient encore.

### 12.6 Extension du domaine

Tester ce qui se produit lorsque le contexte évolue.

### 12.7 Reproductibilité

Vérifier que la réponse reste déterministe sous les conditions déclarées.

### 12.8 Information loss

Vérifier qu'aucune information critique n'est perdue pour simplifier la réponse.

### 12.9 Contradiction

Comparer la réponse avec les autres règles ou décisions déjà gelées.

### 12.10 Cas non couverts

Chercher explicitement ce que la réponse ne sait pas décider.

---

# 13. RÈGLE DE CASSAGE

Une réponse candidate ne doit pas être déclarée robuste parce qu'aucun défaut n'a immédiatement été trouvé.

Le test doit chercher activement des conditions de réfutation.

Le résultat du cassage doit être classé :

```text
RÉFUTÉE
INCOMPLÈTE
ROBUSTE SOUS CONDITIONS
ROBUSTE
```

`ROBUSTE` ne signifie pas mathématiquement impossible à réfuter.

Cela signifie que, dans le domaine explicitement défini et après les attaques exécutées, aucune faiblesse déterminante n'a été démontrée.

---

# 14. RÉPARATION APRÈS CASSAGE

Si une faiblesse critique ou majeure est trouvée :

```text
RÉPONSE CANDIDATE
      ↓
FAILLE IDENTIFIÉE
      ↓
CORRECTION / RESTRICTION / REJET
      ↓
NOUVELLE CANDIDATE
      ↓
NOUVEAU CASSAGE
```

Une correction importante ne doit pas être considérée comme validée simplement parce qu'elle semble résoudre le défaut initial.

Elle doit être réattaquée.

---

# 15. DISTINCTION ENTRE COMPLETUDE ET VÉRITÉ

Une réponse peut être vraie mais incomplète.

Une réponse peut être complète mais reposer sur une prémisse fausse.

Une réponse peut être techniquement élégante mais non normative.

Une réponse peut être conforme au corpus mais insuffisamment déterministe.

Le protocole doit donc évaluer séparément :

```text
VÉRITÉ
COMPLÉTUDE
CONFORMITÉ
DÉTERMINISME
REPRODUCTIBILITÉ
RÉSISTANCE ADVERSARIALE
```

---

# 16. PLACE DE LA DÉCISION HUMAINE

Le but du protocole n'est pas de supprimer artificiellement l'autorité humaine.

Le but est de supprimer autant que possible le besoin pour l'humain de résoudre lui-même des problèmes techniques que le processus d'analyse peut résoudre de manière plus rigoureuse.

Le système doit donc chercher à transformer :

```text
QUESTION HUMAINE IMPRÉCISE
        ↓
PROBLÈME FORMALISÉ
        ↓
ANALYSES INDÉPENDANTES
        ↓
COMPARAISON
        ↓
RÉPONSE CANDIDATE
        ↓
CASSAGE
        ↓
RÉPONSE ROBUSTE
        ↓
DÉCISION HUMAINE CIBLÉE
```

La décision humaine doit porter autant que possible sur un arbitrage compréhensible et explicite, et non sur la découverte technique initiale.

Exemple :

```text
MAUVAIS PROCESSUS
« Quelle architecture dois-je choisir ? »
→ l'humain doit inventer la solution.

PROCESSUS CIBLE
« Voici les options, les preuves, les raisons,
les risques et les résultats du cassage.
L'option A est la meilleure candidate sous telles conditions.
L'option B échoue pour telles raisons.
Voici ce qui reste réellement indécidable. »
→ l'humain arbitre uniquement ce qui reste normativement ouvert.
```

---

# 17. AUTOMATISATION PROGRESSIVE

Le protocole doit être conçu pour être de plus en plus automatisable.

Peuvent progressivement être automatisés :

- formalisation de la question ;
- récupération du corpus ;
- extraction des contraintes ;
- construction des réponses ;
- vérification des preuves ;
- comparaison ;
- génération de contre-exemples ;
- détection de contradictions ;
- tests adversariaux ;
- vérification de reproductibilité ;
- génération du dossier de décision.

Ne peut pas être automatisé silencieusement :

- une décision normative explicitement réservée à l'humain ;
- un arbitrage de gouvernance non délégué ;
- l'acceptation d'une hypothèse comme vérité sans autorité pour le faire.

L'automatisation doit réduire le nombre de décisions humaines, mais jamais en transformant une absence de décision en décision implicite.

---

# 18. QUAND LE PROCESSUS DOIT S'ARRÊTER

Le processus s'arrête avant décision humaine uniquement lorsqu'une information indispensable manque ou qu'une autorité externe est réellement nécessaire.

Le processus s'arrête pour décision humaine lorsqu'après analyse et cassage il reste une véritable alternative normative ou architecturale que le corpus ne permet pas de trancher.

Dans ce cas, le dossier transmis à l'humain doit contenir :

1. question exacte ;
2. réponse candidate ;
3. raisonnement ;
4. preuves ;
5. alternatives ;
6. comparaison ;
7. cassage ;
8. faiblesses restantes ;
9. conséquence de chaque choix ;
10. formulation précise de la décision à prendre.

L'humain ne doit pas recevoir une question vague lorsque le système est capable de la réduire à un arbitrage précis.

---

# 19. INTERDICTIONS

Il est interdit de :

- choisir une réponse par intuition avant comparaison ;
- choisir une réponse par majorité d'IA ;
- considérer une réponse détaillée comme automatiquement meilleure ;
- cacher les hypothèses ;
- confondre convergence et preuve ;
- présenter une architecture proposée comme normative ;
- utiliser une deuxième IA comme simple chambre d'écho ;
- arrêter l'audit parce qu'une réponse paraît convaincante ;
- considérer l'absence de contre-exemple trouvé comme preuve absolue ;
- transformer `UNKNOWN` ou `BLOCKED` en décision implicite ;
- demander à l'humain de choisir avant de lui avoir expliqué les conséquences lorsque la question est techniquement analysable.

---

# 20. CRITÈRE DE QUALITÉ FINAL

Pour une question importante, la qualité d'une réponse est évaluée par :

```text
QUALITÉ
=
CLARTÉ DU PROBLÈME
+
QUALITÉ DES PREUVES
+
SOLIDITÉ DU RAISONNEMENT
+
COUVERTURE DES ALTERNATIVES
+
INDÉPENDANCE DES CONTRE-EXPERTISES
+
QUALITÉ DE LA COMPARAISON
+
RÉSISTANCE AU CASSAGE
+
TRAÇABILITÉ
```

Cette formule est méthodologique et non numérique : elle ne définit pas un calcul de score obligatoire.

---

# 21. ARTÉFACT DE DÉCISION

Pour les décisions importantes, le dossier durable devrait conserver au minimum :

```text
question_id
question
corpus_version
constraints
response_1
response_1_reasoning
response_2
response_2_reasoning
response_3_if_needed
comparison
selected_candidate
eliminated_candidates
adversarial_attacks
identified_failures
corrections
retest_results
remaining_uncertainties
human_decision_if_required
decision_owner
decision_version
```

Le format concret de stockage peut être défini par l'architecture documentaire du projet.

La structure ci-dessus définit le contenu informationnel attendu, pas une implémentation particulière.

---

# 22. RELATION AVEC LE PROTOCOLE DE DÉCISION HUMAINE ASSISTÉE

Le présent protocole complète `§10.1` de la méthodologie de gouvernance.

`§10.1` établit la nécessité de contre-expertise et de compréhension humaine pour les décisions importantes.

Le présent protocole précise **comment préparer cette décision** :

```text
CONSTRUIRE UNE PREMIÈRE RÉPONSE
        ↓
EXPLIQUER SON RAISONNEMENT
        ↓
CONSTRUIRE UNE DEUXIÈME RÉPONSE INDÉPENDANTE
        ↓
COMPARER
        ↓
RETENIR LA MEILLEURE CANDIDATE
        ↓
ESSAYER DE LA CASSER
        ↓
RÉPARER OU REJETER
        ↓
RÉPÉTER SI NÉCESSAIRE
        ↓
PRÉSENTER À L'HUMAIN UNIQUEMENT L'ARBITRAGE RESTANT
```

Le présent protocole ne transfère aucune autorité normative aux IA.

---

# 23. STATUT MÉTHODOLOGIQUE

Ce document est une règle de méthode.

Il ne crée aucune décision métier de trading ni aucune architecture technique particulière.

Il doit être appliqué avec les principes suivants déjà en vigueur :

- `AUTONOMIE ≠ AUTORITÉ` ;
- `UNKNOWN / BLOCKED ≠ PASS` ;
- corpus réel avant mémoire ;
- audit adversarial ;
- distinction fait / inférence / conséquence / proposition ;
- décision humaine explicite lorsque réellement nécessaire ;
- traçabilité et reproductibilité.

---

## FIN — PROTOCOLE V1.0
