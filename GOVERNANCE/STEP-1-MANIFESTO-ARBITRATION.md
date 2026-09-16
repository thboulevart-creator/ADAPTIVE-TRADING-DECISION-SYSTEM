# ÉTAPE 1 — Arbitrage contradictoire du manifeste

**Statut :** ARBITRAGE EFFECTUÉ — candidat gelé pour la suite de la trajectoire
**Base vérifiée :** `main` @ `b24f297538893c0ca56d35345f60e1d1a9d6b0bc`
**Branche d'arbitrage :** `feat/step1-manifest-arbitration-freeze`
**Périmètre :** uniquement l'arbitrage des 14 principes. Aucun travail CONTEXT, CI, temporalité ou nouvelle architecture n'est inclus.

## 1. Sources et discipline de preuve

Le manifeste candidat source est `GOVERNANCE/TRUSTWORTHY-INTELLIGENT-SYSTEM-MANIFESTO-CANDIDATE.md`.

La gouvernance de référence impose notamment : capacité ≠ valeur ; rechercher d'abord la couverture existante ; ne créer une nouvelle couche qu'en cas de manque démontré ; distinguer couverture démontrée, partielle, exposition, absence de preuve et violation ; formalisation → candidat → cassage adversarial → correction → re-cassage → verdict ; `BLOCKED` n'est jamais `PASS` ; les règles proposées restent non normatives jusqu'à validation/adjudication.

La contradiction externe exploitable retrouvée est celle de **Grok** : elle confirme notamment le risque de surinterpréter `DecisionTrace` comme pivot central, recommande de prouver l'existence d'un producteur réel avant de créer plusieurs composants, et conclut `BLOCKED` lorsque la preuve d'intégration manque.

**Claude : aucune sortie substantielle exploitable n'a été retrouvée dans le dépôt ou les artefacts accessibles au moment de l'arbitrage. La réponse Claude disponible précédemment indiquait une indisponibilité de crédits et ne contient pas de position principe-par-principe. Elle n'est donc pas inventée ni utilisée comme preuve.** Cette absence est conservée comme limite de provenance ; elle ne vaut pas approbation implicite.

## 2. Arbitrage principe par principe

| # | Principe candidat | Décision | Arbitrage contre la gouvernance | Effet attendu sur design / opération / tests |
|---|---|---|---|---|
| 1 | VALIDITÉ CONTEXTUELLE | **GARDER** | Cohérent avec domaine de validité, hypothèses, conditions d'invalidation et évolution du contexte. | Contraint connaissances, expériences, décisions et réévaluations ; testable par contexte/domaine/validité. |
| 2 | MÉMOIRE | **GARDER** | Exigence explicite de mémoire expérimentale : hypothèses, expériences, résultats, explications testées, échecs, connaissances validées, preuves. | Change la persistance et les tests de reconstruction/capitalisation. |
| 3 | AUTO-CONTESTATION | **GARDER** | Fondation normative de méta-gouvernance ; protège contre faux PASS et angles morts. | Change contrôles, audits, tests adversariaux et conditions de suspension/révision. |
| 4 | TRAÇABILITÉ | **GARDER** | Nécessaire pour reconstruire pourquoi une décision a été prise ; distingue audit du résultat et du raisonnement. | Change contrats de preuve et tests de reconstruction. |
| 5 | REPRODUCTIBILITÉ | **GARDER** | Déjà transversale dans provenance, recherche, validation et continuité. | Change versionnage, provenance, données, configuration et tests de répétabilité. |
| 6 | RÉSILIENCE | **FUSIONNER** | La gouvernance la définit comme propriété transversale de continuité/survivabilité, pas comme architecture autonome. | Conserve l'exigence sans créer une couche dédiée prématurée. |
| 7 | AUDIT DE LA GOUVERNANCE | **GARDER** | La méta-gouvernance exige que la gouvernance elle-même soit contestable et son efficacité évaluée. | Change audits de gouvernance et tests de faux PASS/bypass. |
| 8 | COMPLEXITÉ MAÎTRISÉE | **GARDER** | Garde-fou direct contre la prolifération ; aucune capacité ne justifie une couche sans valeur démontrée. | Change sélection des composants et seuil de création de mécanismes. |
| 9 | QUANTIFICATION DE L'INCERTITUDE | **RÉDUIRE** | L'incertitude est déjà couverte par preuves, confiance, domaine de validité, limites, invalidation et `BLOCKED`. | Représenter l'incertitude ; ne pas imposer une métrique universelle ni une couche autonome. |
| 10 | EXPLICABILITÉ OPÉRATIONNELLE | **FUSIONNER** | Sa substance est déjà portée par la traçabilité/reconstruction décisionnelle. | Reste testable via informations, règles, incertitudes, alternatives, décision, action et résultat. |
| 11 | COÛT DE L'ERREUR | **GARDER** | Directement compatible avec la finalité : valeur attendue sous contraintes de risque, coût et incertitude. | Change seuils de décision et tests de conséquences ; interdit de raisonner uniquement en exactitude. |
| 12 | ALIGNEMENT DYNAMIQUE | **FUSIONNER** | Trop large seul ; sa substance est couverte par changement/validité, évolution, objectifs et réévaluation. | Conserve la réévaluation d'adéquation sans mécanisme d'alignement générique. |
| 13 | RÉVERSIBILITÉ | **FUSIONNER** | Propriété opérationnelle utile, principalement portée par résilience, autorisation, suspension/arrêt et reprise. | Conserve suspension, arrêt, retour contrôlé et reprise lorsque justifiés ; pas de couche autonome. |
| 14 | HUMILITÉ ÉPISTÉMIQUE STRUCTURÉE | **FUSIONNER** | Son contenu est déjà porté par hypothèses, preuves, limites, invalidation, contestation et statuts de connaissance. | Renforce les statuts épistémiques sans ajouter de composant. |

## 3. Décisions finales

### GARDER — 8
1. Validité contextuelle
2. Mémoire
3. Auto-contestation
4. Traçabilité
5. Reproductibilité
6. Audit de la gouvernance
7. Complexité maîtrisée
8. Coût de l'erreur

### FUSIONNER — 5
9. Résilience → propriété transversale de continuité/survivabilité
10. Explicabilité opérationnelle → traçabilité/reconstruction décisionnelle
11. Alignement dynamique → changement/validité + évolution contrôlée
12. Réversibilité → résilience + autorisation/suspension/arrêt/reprise
13. Humilité épistémique structurée → incertitude + preuves + contestation + statuts de connaissance

### RÉDUIRE — 1
14. Quantification de l'incertitude → représentation structurée de l'incertitude sans couche quantitative autonome

### LAISSER COMME HYPOTHÈSE — 0
Aucun des 14 thèmes n'est conservé comme capacité autonome sans mécanisme et preuve. Les formulations génériques non opérationnelles sont absorbées dans les principes retenus ou restent non normatives.

### REJETER — 0 comme thème, mais rejet des couches redondantes
Aucun thème n'est rejeté comme idée sans valeur. En revanche, toute transformation en couche autonome qui ne change ni décision, ni action, ni résultat, ni preuve est rejetée.

## 4. Test critique « est-ce réellement architectural ? »

Filtre : **si le principe ne change pas le design, l'opération ou les tests, il ne devient pas une contrainte architecturale autonome.**

Les principes conservés ont un effet direct sur décisions, preuves, contrôles, risques ou tests. Les principes fusionnés restent obligatoires comme propriétés de fonctions déjà existantes. La quantification de l'incertitude n'est pas promue comme couche autonome. Aucune nouvelle architecture n'est justifiée par le manifeste.

## 5. Limite de l'arbitrage externe

L'arbitrage est contradictoire au sens où le manifeste a été confronté à la gouvernance existante et à la contestation Grok disponible. Il n'est **pas** permis d'affirmer qu'une double sortie Claude + Grok complète est disponible : la sortie Claude substantielle manque.

Cette limite est une absence de preuve, pas un PASS implicite.

Le manifeste est donc **gelé comme candidat de construction** : son contenu ne doit plus être réécrit pendant la construction de la trajectoire sans passer par le mécanisme de gouvernance d'évolution. Ce gel ne constitue pas à lui seul le verdict final de l'ÉTAPE 1.
