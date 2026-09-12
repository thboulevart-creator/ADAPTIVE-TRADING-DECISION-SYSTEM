# MANIFESTE D'UN SYSTÈME INTELLIGENT DIGNE DE CONFIANCE — CANDIDAT GELÉ

**Statut :** CANDIDAT GELÉ — résultat de l'ÉTAPE 1
**Portée :** principe directeur transversal pour un système intelligent autonome et adaptatif
**Règle de gouvernance :** ce manifeste est un cadre de conception gelé pour la construction. Il ne devient pas automatiquement une règle normative universelle. Toute modification ultérieure passe par la gouvernance d'évolution, avec preuve et arbitrage.

## 1. Principes retenus

### 1.1 VALIDITÉ CONTEXTUELLE

Une connaissance, une hypothèse, une expérience ou une décision n'est exploitable qu'avec son contexte, son domaine de validité, ses hypothèses, ses limites et ses conditions d'invalidation pertinentes.

### 1.2 MÉMOIRE EXPÉRIMENTALE

Le système doit pouvoir conserver les hypothèses, expériences, paramètres, résultats, explications testées, échecs, réussites, résultats inconclusifs, connaissances validées, niveaux de preuve, provenance et liens avec les décisions ultérieures. Une hypothèse ne devient pas une connaissance validée par simple répétition ou succès isolé.

### 1.3 AUTO-CONTESTATION

Le système doit rechercher activement pourquoi ses hypothèses, connaissances, métriques, décisions, contrôles ou son architecture pourraient être faux, incomplets ou devenus invalides. L'absence d'anomalie n'est pas une preuve d'absence de problème.

### 1.4 TRAÇABILITÉ

Une décision critique doit être reconstructible à partir des informations disponibles, données utilisées, connaissances actives, hypothèses, contraintes, règles, incertitudes, alternatives, décision, action, résultat et contestation lorsque ces éléments sont applicables.

### 1.5 REPRODUCTIBILITÉ

Une conclusion importante doit pouvoir être reliée aux versions de code, configuration, données, provenance et conditions nécessaires à sa reproduction. Une performance isolée ne constitue pas une preuve suffisante.

### 1.6 AUDIT DE LA GOUVERNANCE

La gouvernance elle-même doit pouvoir être contestée. Son efficacité doit être évaluée périodiquement par recherche de problèmes non détectés, contournements, faux PASS et angles morts. Cette exigence ne justifie pas une récursion infinie de méta-gouvernance.

### 1.7 COMPLEXITÉ MAÎTRISÉE

Aucune capacité, couche, registre ou composant n'est justifié par son élégance ou sa sophistication. Toute extension doit démontrer une amélioration réelle de décision, action, résultat ou preuve supérieure à ses coûts, risques et nouvelles dépendances. La préférence va à la réutilisation et au plus petit mécanisme suffisant.

### 1.8 COÛT DE L'ERREUR

La conception doit considérer les conséquences de décisions erronées et les coûts d'une poursuite injustifiée. Réduction d'exposition, inaction, suspension et arrêt sont des décisions valides lorsque le niveau de preuve, l'incertitude ou le coût potentiel de l'erreur ne justifient plus l'action.

## 2. Propriétés intégrées, non autonomes

### 2.1 RÉSILIENCE

La résilience est une propriété transversale de continuité et de survivabilité. Elle n'est pas, à ce stade, une architecture autonome.

### 2.2 EXPLICABILITÉ OPÉRATIONNELLE

Elle est intégrée à la traçabilité et à la reconstruction décisionnelle. Aucun mécanisme d'explicabilité séparé n'est créé sans manque démontré.

### 2.3 ALIGNEMENT DYNAMIQUE

Il est interprété comme l'exigence de vérifier que le système, ses connaissances, objectifs, contraintes et décisions restent adaptés au contexte et à son évolution. Il est couvert par validité, changement et réévaluation.

### 2.4 RÉVERSIBILITÉ

Elle est intégrée aux mécanismes de résilience, d'autorisation contrôlée, de suspension, d'arrêt, de retour contrôlé et de reprise lorsque le risque le justifie.

### 2.5 HUMILITÉ ÉPISTÉMIQUE STRUCTURÉE

Elle est intégrée aux distinctions hypothèse/connaissance, preuve/absence de preuve, limites, domaine de validité, conditions d'invalidation, contestation et statuts `PASS / FAIL / BLOCKED` lorsqu'ils sont applicables.

## 3. Incertitude : principe réduit

La **quantification de l'incertitude** n'est pas une couche autonome ni une obligation de produire une métrique universelle. L'exigence retenue est de représenter correctement, lorsque pertinent, le niveau de preuve, la confiance, le domaine de validité, les limites, les conditions d'invalidation et l'état `BLOCKED` ou inconclusif.

Une précision numérique n'est exigée que si elle apporte une valeur démontrée à la décision ou au contrôle concerné.

## 4. Chaîne de valeur

Toute capacité retenue doit pouvoir être reliée à :

**CAPACITÉ → MEILLEURE DÉCISION → MEILLEURE ACTION → MEILLEUR RÉSULTAT → VALEUR MESURABLE**

Elle doit également être évaluée contre :

**COÛT DE COMPLEXITÉ + RISQUE INTRODUIT + NOUVELLES INCERTITUDES + POSSIBILITÉS DE BYPASS**.

Si cette chaîne ne peut pas être démontrée ou testée, la capacité reste hypothétique ou n'est pas promue.

## 5. Cycle de connaissance et d'action

**OBSERVATION → HYPOTHÈSE → EXPÉRIMENTATION → CONTESTATION → PREUVE → VALIDATION → AUTORISATION CONTRÔLÉE → DÉPLOIEMENT → SURVEILLANCE → RÉÉVALUATION**

Une découverte ou une connaissance validée ne modifie pas automatiquement le comportement opérationnel. La promotion vers l'opérationnel reste contrôlée.

## 6. Méthode de vérification

**CARTOGRAPHIER → LIRE → MAPPER LES PREUVES → TESTER LA COUVERTURE → CHERCHER LES BYPASS → CASSER → CORRIGER SI NÉCESSAIRE → RE-CASSER → ÉVALUER LE COÛT DE L'ERREUR RÉSIDUELLE → VERDICT → INTÉGRER SEULEMENT LE MINIMUM JUSTIFIÉ**

Un mécanisme n'obtient pas `PASS` parce qu'il existe ou paraît cohérent. Le verdict repose sur des preuves exécutables adaptées à la criticité. Une correction n'est suffisante qu'après re-test adversarial approprié.

## 7. Faillibilité maîtrisée

Le système n'est pas supposé être infaillible. Il doit pouvoir :

- se tromper ;
- détecter qu'il pourrait s'être trompé ;
- rechercher les conditions de l'erreur ;
- limiter les conséquences ;
- réviser ses hypothèses ;
- conserver ce qui a été appris ;
- vérifier la correction ;
- découvrir que son mécanisme de contrôle est lui-même insuffisant ;
- suspendre ou arrêter lorsque la preuve ou la confiance deviennent insuffisantes.

> **Le système doit être conçu pour pouvoir découvrir qu'il a mal pensé.**

## 8. Règle de non-prolifération

Le manifeste ne justifie aucune nouvelle architecture par lui-même. Une fonction déjà couverte par un mécanisme existant doit être portée par cet existant ou par son extension minimale. Une nouvelle couche n'est autorisée qu'après démonstration d'un manque, d'un risque ou d'une exigence importante non couverte.

## 9. Statut épistémique du manifeste

Ce document constitue le **MANIFESTE FINAL CANDIDAT GELÉ** de l'ÉTAPE 1 : suffisamment stable pour construire la suite sans le réécrire opportunément.

Ce gel n'est pas une prétention de vérité éternelle. Toute évolution ultérieure doit fournir la preuve du changement de contexte, de l'insuffisance du principe actuel ou d'une meilleure formulation, puis repasser par l'arbitrage de gouvernance.

**Aucun travail CONTEXT, CI, temporalité ou nouvelle architecture n'est autorisé par ce document.**
