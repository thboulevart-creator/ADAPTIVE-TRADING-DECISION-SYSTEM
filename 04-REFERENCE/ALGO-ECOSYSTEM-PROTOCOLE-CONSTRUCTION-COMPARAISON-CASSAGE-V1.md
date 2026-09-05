# ALGO ECOSYSTEM — PROTOCOLE DE CONSTRUCTION, COMPARAISON & CASSAGE DES RÉPONSES

**Version :** 1.1  
**Date :** 5 septembre 2026  
**Statut :** RÉFÉRENCE MÉTHODOLOGIQUE — OBLIGATOIRE POUR LES QUESTIONS IMPORTANTES  
**Dépendance :** `04-REFERENCE/ALGO-ECOSYSTEM-METHODOLOGIE-GOUVERNANCE-V1.md`

---

# 0. OBJET

Ce protocole définit le fonctionnement de référence à appliquer lorsqu'une question importante peut conduire à une décision architecturale, normative, méthodologique ou de gouvernance.

Le système ne doit pas fonctionner selon le modèle :

```text
QUESTION → RÉPONSE → DÉCISION
```

Il doit fonctionner selon le modèle :

```text
QUESTION
   ↓
FORMALISATION
   ↓
RÉPONSE 1
   ↓
AUDIT DU RAISONNEMENT DE RÉPONSE 1
   ↓
RÉPONSE 2 INDÉPENDANTE
   ↓
COMPARAISON
   ↓
SÉLECTION D'UNE CANDIDATE
   ↓
CASSAGE ADVERSARIAL
   ↓
CORRECTION / RESTRICTION / REJET
   ↓
RE-CASSAGE SI NÉCESSAIRE
   ↓
RÉPONSE ROBUSTE
   ↓
DÉCISION HUMAINE UNIQUEMENT SI RÉELLEMENT NÉCESSAIRE
```

Le but est d'augmenter progressivement l'autonomie du processus sans transférer silencieusement aux IA une autorité normative qui ne leur appartient pas.

---

# 1. PRINCIPE CENTRAL

Une réponse n'est pas une vérité simplement parce qu'elle est convaincante, détaillée, cohérente ou produite par une IA réputée compétente.

Une réponse est d'abord une **candidate**.

Principe fondamental :

```text
RÉPONSE
   ≠
RÉPONSE VALIDÉE
```

La validation nécessite l'examen de :

```text
RAISONNEMENT
PREUVES
HYPOTHÈSES
ALTERNATIVES
LIMITES
DÉTERMINISME
REPRODUCTIBILITÉ
RÉSISTANCE ADVERSARIALE
```

Le processus doit chercher activement à découvrir pourquoi la réponse pourrait être fausse, incomplète, non conforme ou dangereuse.

---

# 2. RÈGLE DE FONCTIONNEMENT OBLIGATOIRE

Pour toute question entrant dans le périmètre de ce protocole, les étapes doivent être exécutées dans l'ordre défini ci-dessous.

Il est interdit de sauter directement de la question à une décision lorsque les étapes intermédiaires sont nécessaires pour établir la robustesse de la réponse.

Le système doit appliquer :

```text
DÉTERMINER
   ↓
CONSTRUIRE
   ↓
AUDITER
   ↓
RECONSTRUIRE INDÉPENDAMMENT
   ↓
COMPARER
   ↓
SÉLECTIONNER
   ↓
CASSER
   ↓
CORRIGER OU REJETER
   ↓
RE-CASSER SI NÉCESSAIRE
   ↓
DÉCIDER UNIQUEMENT SI NÉCESSAIRE
```

Une étape terminée ne signifie pas que sa conclusion est vraie. Elle signifie uniquement que le contrôle correspondant a été exécuté.

---

# 3. PHASE 1 — DÉFINITION EXACTE DU PROBLÈME

Avant toute construction de réponse, le système doit déterminer :

1. la question exacte ;
2. le résultat recherché ;
3. le périmètre ;
4. les documents et sources applicables ;
5. les contraintes déjà gelées ;
6. les éléments explicitement hors périmètre ;
7. les inconnues ;
8. le critère permettant de considérer une réponse comme suffisante ;
9. l'autorité compétente si une décision finale est nécessaire.

Une question ambiguë ne doit jamais être silencieusement simplifiée.

Si plusieurs interprétations peuvent modifier le résultat, elles doivent être distinguées avant la construction.

Une question peut être techniquement analysable même si sa formulation humaine initiale est imprécise. Le système doit alors formaliser le problème plutôt que demander immédiatement à l'humain de résoudre lui-même l'ambiguïté technique.

---

# 4. PHASE 2 — RÉPONSE 1 : CONSTRUCTION EXPLICITE

La première réponse doit être construite comme une démonstration contrôlée.

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
CONCLUSION CANDIDATE
```

La réponse 1 doit répondre simultanément à deux questions :

> « Quelle est la réponse ? »

et :

> « Pourquoi cette réponse plutôt qu'une autre ? »

---

# 5. FICHE OBLIGATOIRE DE CONSTRUCTION DE LA RÉPONSE 1

Lorsque la nature de la question le permet, la réponse 1 doit expliciter :

### 5.1 Réponse

La conclusion candidate.

### 5.2 Preuves

Les faits documentaires, techniques, expérimentaux ou logiques utilisés.

### 5.3 Raisonnement

La chaîne logique reliant les preuves à la conclusion.

### 5.4 Hypothèses

Les hypothèses nécessaires mais non démontrées.

### 5.5 Alternatives

Les solutions sérieusement envisageables.

### 5.6 Pourquoi cette réponse

Les raisons pour lesquelles la candidate paraît supérieure aux alternatives connues.

### 5.7 Conditions de validité

Les conditions sous lesquelles la conclusion reste valable.

### 5.8 Limites et faiblesses connues

Ce que la réponse ne démontre pas encore.

Une réponse qui donne uniquement une conclusion sans rendre son raisonnement reconstructible est insuffisamment construite.

---

# 6. PHASE 3 — AUDIT DU RAISONNEMENT DE RÉPONSE 1

Avant de produire la deuxième réponse, la construction de la réponse 1 doit être auditée.

Cet audit ne cherche pas encore à décider si la conclusion est vraie.

Il cherche à déterminer si le raisonnement présenté est complet, explicite et falsifiable.

Rechercher notamment :

- prémisse non démontrée ;
- saut logique ;
- hypothèse cachée ;
- définition ambiguë ;
- alternative ignorée ;
- dépendance documentaire non vérifiée ;
- confusion fait / inférence ;
- confusion inférence / décision normative ;
- architecture proposée présentée comme exigence ;
- conclusion plus forte que les preuves ;
- circularité ;
- raisonnement dépendant de la conclusion ;
- cas limite absent ;
- domaine de validité non déclaré ;
- contre-exemple déjà connu non traité.

Cette étape ne transforme jamais une réponse en PASS.

Elle prépare une base falsifiable pour la seconde analyse.

---

# 7. PHASE 4 — RÉPONSE 2 : RECONSTRUCTION INDÉPENDANTE

La deuxième réponse doit répondre à la même question à partir du même corpus et des mêmes contraintes, mais en reconstruisant son propre raisonnement.

Elle ne doit pas traiter la réponse 1 comme une vérité de référence.

L'objectif n'est pas d'obtenir une reformulation.

L'objectif est d'obtenir une **seconde trajectoire de raisonnement**.

La réponse 2 doit donc, lorsque possible, fournir :

- sa conclusion ;
- ses preuves ;
- son raisonnement ;
- ses hypothèses ;
- ses alternatives ;
- ses critères de choix ;
- les raisons de sa conclusion ;
- ses limites ;
- ses conditions de validité.

Une réponse 2 qui reprend simplement la conclusion ou l'architecture de la réponse 1 sans reconstruction indépendante réduit fortement la valeur de la contre-expertise et doit être identifiée comme telle.

---

# 8. MESURE DE L'INDÉPENDANCE

Deux réponses différentes ne sont pas nécessairement deux raisonnements indépendants.

Le système doit rechercher les prémisses communes cachées.

Comparer notamment :

```text
SOURCES UTILISÉES
DÉFINITIONS
PRÉMISSES
HYPOTHÈSES
CHAÎNES D'INFÉRENCE
OPTIONS CONSIDÉRÉES
CRITÈRES DE CHOIX
```

Deux réponses qui convergent parce qu'elles partagent une même prémisse non vérifiée ne constituent pas une preuve renforcée.

Principe :

```text
DIVERSITÉ DE SORTIE
   ≠
INDÉPENDANCE DE RAISONNEMENT
```

La qualité de l'indépendance doit donc être examinée avant de tirer une conclusion de la convergence.

---

# 9. PHASE 5 — RÉPONSE 3 CONDITIONNELLE

Une troisième analyse peut être sollicitée si :

- les deux premières divergent sur un point critique ;
- une décision est difficilement réversible ;
- les conséquences d'une erreur sont élevées ;
- une dépendance documentaire reste contradictoire ;
- les deux analyses semblent partager une hypothèse critique ;
- une troisième perspective peut réellement discriminer les options.

La troisième réponse n'est pas obligatoire par principe.

Elle doit fournir une capacité supplémentaire de discrimination ou de falsification.

Il est interdit d'utiliser mécaniquement une majorité d'IA comme substitut à une preuve.

---

# 10. PHASE 6 — COMPARAISON

Les réponses doivent être comparées avant toute sélection.

La comparaison porte au minimum sur :

```text
CONCLUSION
PREUVES
RAISONNEMENT
HYPOTHÈSES
ALTERNATIVES
LIMITES
RISQUES
CONDITIONS DE VALIDITÉ
INDÉPENDANCE
```

La comparaison doit identifier :

```text
CONVERGENCES
DIVERGENCES
PRÉMISSES COMMUNES
HYPOTHÈSES DIFFÉRENTES
POINTS NON DÉMONTRÉS
RISQUES DÉTECTÉS PAR UNE SEULE RÉPONSE
OPTIONS ÉLIMINÉES
QUESTIONS RESTANTES
```

Une convergence est un signal, pas une preuve.

Une divergence n'est pas automatiquement une erreur : elle peut révéler une hypothèse différente, une ambiguïté du corpus ou une vraie décision non résolue.

---

# 11. PHASE 7 — ÉLIMINATION DES CANDIDATES

Avant de sélectionner une réponse, chaque candidate doit être testée contre les critères de conformité et de robustesse.

Une réponse peut être éliminée si elle :

- contredit le corpus ;
- dépend d'une hypothèse non autorisée ;
- transforme une hypothèse en fait ;
- crée une décision normative sans autorité ;
- ne couvre pas un cas critique ;
- détruit une information nécessaire ;
- introduit une ambiguïté ;
- n'est pas déterministe ;
- n'est pas reproductible ;
- ne permet pas de vérifier son résultat ;
- échoue sur un contre-exemple connu ;
- repose sur une prémisse que l'analyse ne peut pas établir.

Le système doit préférer la réponse la mieux justifiée, et non la réponse la plus élégante ou la plus détaillée.

---

# 12. PHASE 8 — SÉLECTION D'UNE RÉPONSE CANDIDATE

Lorsque la comparaison permet de réduire l'espace des solutions, une seule candidate doit être retenue pour le cassage approfondi.

Le dossier de sélection doit indiquer :

```text
RÉPONSE RETENUE
RAISONS DE LA SÉLECTION
RÉPONSES ÉLIMINÉES
RAISONS DE L'ÉLIMINATION
RISQUES RESTANTS
POINTS NON PROUVÉS
```

La sélection ne constitue pas une validation finale.

Elle signifie :

> « C'est actuellement la meilleure candidate connue. Nous allons maintenant essayer de la détruire. »

Si aucune candidate ne domine suffisamment les autres, le système ne doit pas fabriquer une préférence artificielle. Il doit conserver la divergence ou déclencher une analyse supplémentaire si elle est justifiée.

---

# 13. PHASE 9 — CASSAGE ADVERSARIAL

La candidate retenue doit être attaquée comme si l'objectif était de démontrer qu'elle est fausse, incomplète ou dangereuse.

Le cassage doit rechercher activement :

### 13.1 Contre-exemples

Construire des cas où la candidate échoue.

### 13.2 Cas limites

Tester les frontières du domaine.

### 13.3 Cas adverses

Construire volontairement les conditions les plus défavorables.

### 13.4 Alternatives oubliées

Chercher une solution sérieuse qui n'a pas été considérée.

### 13.5 Hypothèses cachées

Retirer ou inverser une hypothèse et observer si la conclusion tient.

### 13.6 Extension du domaine

Tester ce qui se produit lorsque le contexte ou les entrées changent dans les limites plausibles du domaine.

### 13.7 Contradictions

Comparer la candidate aux règles, décisions et invariants déjà gelés.

### 13.8 Reproductibilité

Tester la stabilité sous les conditions déclarées.

### 13.9 Perte d'information

Vérifier qu'une simplification n'a pas détruit une information nécessaire.

### 13.10 Cas non couverts

Identifier explicitement ce que la candidate ne sait pas déterminer.

### 13.11 Dépendances cachées

Rechercher les dépendances à l'environnement, à une version, à une convention implicite ou à un choix non déclaré.

---

# 14. RÈGLE DE CASSAGE

L'absence de défaut trouvé ne constitue pas une preuve absolue de correction.

Le cassage doit être orienté vers la falsification.

Le résultat doit être classé :

```text
RÉFUTÉE
INCOMPLÈTE
ROBUSTE SOUS CONDITIONS
ROBUSTE
```

### RÉFUTÉE

Un contre-exemple ou une contradiction démontre que la candidate ne peut pas être retenue dans le domaine considéré.

### INCOMPLÈTE

La candidate peut être correcte sur son domaine mais ne couvre pas un cas nécessaire à la question.

### ROBUSTE SOUS CONDITIONS

La candidate résiste aux attaques exécutées à condition que des conditions explicites soient respectées.

### ROBUSTE

Dans le domaine explicitement défini et après les attaques pertinentes exécutées, aucune faiblesse déterminante n'a été démontrée.

`ROBUSTE` ne signifie pas « impossible à réfuter ».

---

# 15. PHASE 10 — CORRECTION APRÈS CASSAGE

Lorsqu'une faiblesse critique ou majeure est trouvée :

```text
CANDIDATE
   ↓
FAILLE
   ↓
CORRECTION / RESTRICTION / REJET
   ↓
NOUVELLE CANDIDATE
   ↓
NOUVEAU CASSAGE
```

Une correction n'est pas validée simplement parce qu'elle résout le défaut initial.

Elle doit être réattaquée afin de vérifier qu'elle n'introduit pas une nouvelle faiblesse.

Si plusieurs corrections successives sont nécessaires, le processus continue jusqu'à obtenir une candidate robuste sous le domaine défini ou jusqu'à démontrer qu'aucune solution ne peut être établie avec les informations disponibles.

---

# 16. DISTINCTION ENTRE VÉRITÉ, COMPLÉTUDE ET CONFORMITÉ

Le protocole doit évaluer séparément :

```text
VÉRITÉ
COMPLÉTUDE
CONFORMITÉ
DÉTERMINISME
REPRODUCTIBILITÉ
RÉSISTANCE ADVERSARIALE
```

Une réponse peut être vraie mais incomplète.

Une réponse peut être complète mais reposer sur une prémisse fausse.

Une réponse peut être techniquement élégante mais non normative.

Une réponse peut être conforme au corpus mais insuffisamment déterministe.

Une réponse peut être robuste dans un domaine mais invalide hors de ce domaine.

Le système doit donc déclarer explicitement les conditions et le domaine de validité.

---

# 17. DISTINCTION DES STATUTS ÉPISTÉMIQUES

Le protocole doit préserver les distinctions suivantes :

```text
FAIT ÉTABLI
INFÉRENCE
CONSÉQUENCE NÉCESSAIRE
HYPOTHÈSE
ARCHITECTURE PROPOSÉE
OPTION
QUESTION NON RÉSOLUE
ABSENCE DE PREUVE
UNKNOWN
BLOCKED
```

Il est interdit de transformer :

```text
UNKNOWN → PASS
BLOCKED → PASS
ABSENCE DE PREUVE → FAIT
ARCHITECTURE PROPOSÉE → EXIGENCE NORMATIVE
CONVERGENCE IA → PREUVE
```

---

# 18. PLACE DE LA DÉCISION HUMAINE

Le but du protocole n'est pas de supprimer l'autorité humaine.

Le but est de supprimer autant que possible le besoin pour l'humain de résoudre lui-même des problèmes techniques que le processus peut analyser rigoureusement.

Le processus cible est :

```text
QUESTION HUMAINE IMPRÉCISE
        ↓
PROBLÈME FORMALISÉ
        ↓
RÉPONSE 1
        ↓
AUDIT DU RAISONNEMENT
        ↓
RÉPONSE 2 INDÉPENDANTE
        ↓
COMPARAISON
        ↓
CANDIDATE
        ↓
CASSAGE
        ↓
RÉPONSE ROBUSTE
        ↓
DÉCISION HUMAINE CIBLÉE SI NÉCESSAIRE
```

L'humain doit recevoir, autant que possible :

1. la question exacte ;
2. les faits établis ;
3. les règles applicables ;
4. les options réellement restantes ;
5. la candidate retenue ;
6. les raisons de cette sélection ;
7. les attaques exécutées ;
8. les faiblesses restantes ;
9. les conséquences des choix possibles ;
10. la formulation précise de la décision à prendre.

L'humain ne doit pas être sollicité pour choisir entre des options techniques qui peuvent encore être discriminées par analyse.

---

# 19. CONDITIONS D'ARRÊT

Le processus ne doit pas s'arrêter prématurément simplement parce qu'une réponse paraît convaincante.

Il peut s'arrêter pour les raisons suivantes :

### 19.1 Robustesse suffisante

Une candidate résiste aux attaques pertinentes dans le domaine défini et aucune faiblesse déterminante ne subsiste.

### 19.2 Information indispensable manquante

Une donnée sans laquelle aucune conclusion fiable n'est possible manque réellement.

Dans ce cas :

```text
BLOCKED / QUESTION NON RÉSOLUE
```

et aucune hypothèse de remplacement ne doit être transformée en fait.

### 19.3 Autorité externe indispensable

Une autorité documentaire, réglementaire, métier ou autre est nécessaire pour trancher une question qui ne peut pas être résolue par le corpus et l'analyse disponibles.

### 19.4 Décision humaine réellement normative

Après réduction maximale de l'espace des solutions par l'analyse, plusieurs options restent normativement valides et le corpus ne permet pas de choisir.

Dans ce cas seulement, la décision humaine est requise.

---

# 20. AUTOMATISATION PROGRESSIVE

Le protocole doit être conçu pour augmenter progressivement son autonomie.

Peuvent progressivement être automatisés :

- formalisation de la question ;
- récupération du corpus ;
- extraction des contraintes ;
- identification des dépendances ;
- construction des réponses ;
- audit des raisonnements ;
- comparaison ;
- détection des prémisses communes ;
- génération de contre-exemples ;
- détection de contradictions ;
- tests adversariaux ;
- vérification de reproductibilité ;
- génération du dossier de décision ;
- suivi des questions restantes ;
- déclenchement conditionnel d'une analyse supplémentaire.

Ne peut pas être automatisé silencieusement :

- une décision normative explicitement réservée à l'humain ;
- un arbitrage de gouvernance non délégué ;
- l'acceptation d'une hypothèse comme vérité sans autorité ;
- le passage de `UNKNOWN` ou `BLOCKED` à un statut validé sans preuve.

---

# 21. DOSSIER DE TRAÇABILITÉ

Pour une question importante, le système doit pouvoir conserver au minimum :

```text
question_id
question
scope
corpus_version
constraints
unknowns
response_1
response_1_reasoning
response_1_evidence
response_1_assumptions
response_1_alternatives
response_1_self_audit
response_2
response_2_reasoning
response_2_evidence
response_2_assumptions
response_2_alternatives
independence_analysis
comparison
selected_candidate
eliminated_candidates
selection_reasoning
adversarial_attacks
identified_failures
corrections
retest_results
remaining_uncertainties
human_decision_if_required
decision_owner
decision_version
```

Le format concret de stockage est une question d'architecture documentaire.

Le contenu informationnel ci-dessus est le minimum recommandé pour conserver la traçabilité du raisonnement.

---

# 22. RÈGLE DE NON-DÉRIVE

Ce protocole définit une méthode de raisonnement et de sélection.

Il ne crée aucune règle métier de trading et ne décide aucune architecture technique particulière.

Il ne doit pas absorber silencieusement :

- la logique de stratégie ;
- la logique d'exécution ;
- la gestion du risque ;
- une décision normative non adjudicée ;
- une convention technique non déclarée.

Toute extension de périmètre doit être explicitement identifiée.

---

# 23. RELATION AVEC LA GOUVERNANCE

Le présent protocole complète le protocole de décision humaine assistée défini dans :

```text
04-REFERENCE/ALGO-ECOSYSTEM-METHODOLOGIE-GOUVERNANCE-V1.md
```

Il précise la préparation analytique de la décision :

```text
CONTRE-EXPERTISE
      ↓
COMPARAISON
      ↓
SÉLECTION
      ↓
CASSAGE
      ↓
RÉPONSE ROBUSTE
      ↓
DÉCISION HUMAINE SI NÉCESSAIRE
```

Le présent document ne transfère aucune autorité normative aux IA.

---

# 24. PROTOCOLE OPÉRATIONNEL À APPLIQUER DÉSORMAIS

Lorsqu'une question importante arrive, le système doit suivre cette séquence sans attendre une instruction humaine supplémentaire lorsque l'étape suivante est techniquement déterminée :

```text
1. FORMALISER LA QUESTION
2. IDENTIFIER LE CORPUS ET LES CONTRAINTES
3. CONSTRUIRE RÉPONSE 1
4. EXAMINER LE RAISONNEMENT DE RÉPONSE 1
5. CONSTRUIRE RÉPONSE 2 INDÉPENDANTE
6. COMPARER LES DEUX RÉPONSES
7. ÉVALUER LEUR INDÉPENDANCE
8. ÉLIMINER LES CANDIDATES INSUFFISANTES
9. RETENIR UNE CANDIDATE SI POSSIBLE
10. CASSER LA CANDIDATE
11. CORRIGER, RESTREINDRE OU REJETER SI NÉCESSAIRE
12. RE-CASSER APRÈS CORRECTION
13. DÉTERMINER LE STATUT FINAL DE LA RÉPONSE
14. NE SOLLICITER L'HUMAIN QUE SI UNE VRAIE DÉCISION RESTE OUVERTE
```

### Règle d'autonomie

Si l'étape suivante est techniquement déterminée par le contexte, elle doit être exécutée directement.

Ne pas remplacer l'exécution par une annonce du type :

```text
« Je pourrais maintenant... »
```

Le comportement attendu est :

```text
DÉTERMINER → EXÉCUTER → VÉRIFIER → ENCHAÎNER
```

L'arrêt n'est justifié que par :

1. une véritable décision humaine ;
2. une information indispensable réellement manquante ;
3. une contre-expertise externe réellement nécessaire ;
4. un blocage technique objectif.

---

# 25. CRITÈRE DE QUALITÉ FINAL

Une réponse importante est considérée comme méthodologiquement forte lorsque :

```text
PROBLÈME CLAIREMENT FORMALISÉ
+
PREUVES VÉRIFIÉES
+
RAISONNEMENT RECONSTRUCTIBLE
+
HYPOTHÈSES EXPLICITES
+
ALTERNATIVES EXAMINÉES
+
SECONDE ANALYSE RÉELLEMENT INDÉPENDANTE
+
COMPARAISON EXPLICITE
+
CANDIDATE JUSTIFIÉE
+
CASSAGE ADVERSARIAL EXÉCUTÉ
+
CORRECTIONS RE-CASSÉES SI NÉCESSAIRE
+
STATUT ET LIMITES EXPLICITES
```

Cette formule est méthodologique et ne constitue pas un score numérique.

---

# 26. RÈGLE DE VÉRITÉ FINALE

Le protocole n'a pas pour objectif de trouver une réponse qui semble vraie.

Il a pour objectif de trouver la réponse **la mieux établie et la plus résistante aux tentatives de réfutation disponibles**, puis de laisser à l'humain uniquement ce qui reste réellement normatif ou indécidable.

Principe final :

```text
UNE RÉPONSE EST UNE CANDIDATE
JUSQU'À CE QU'ELLE AIT ÉTÉ :

CONSTRUITE
AUDITÉE
RECONSTRUITE INDÉPENDAMMENT
COMPARÉE
SÉLECTIONNÉE
CASSÉE
ET, SI NÉCESSAIRE, CORRIGÉE PUIS RE-CASSÉE.
```

---

## FIN — PROTOCOLE V1.1
