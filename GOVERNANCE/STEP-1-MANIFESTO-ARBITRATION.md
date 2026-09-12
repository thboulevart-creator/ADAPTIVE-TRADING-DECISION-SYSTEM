# ÉTAPE 1 — Arbitrage contradictoire du manifeste

**Statut :** ARBITRAGE EFFECTUÉ — candidat gelé pour la suite de la trajectoire
**Base vérifiée :** `main` @ `b24f297538893c0ca56d35345f60e1d1a9d6b0bc`
**Branche d'arbitrage :** `feat/step1-manifest-arbitration-freeze`
**Périmètre :** uniquement l'arbitrage des 14 principes. Aucun travail CONTEXT, CI, temporalité ou nouvelle architecture n'est inclus.

## 1. Sources et discipline de preuve

Le manifeste candidat source est `GOVERNANCE/TRUSTWORTHY-INTELLIGENT-SYSTEM-MANIFESTO-CANDIDATE.md`.

La gouvernance de référence impose notamment :
- capacité ≠ valeur ;
- rechercher d'abord la couverture existante ;
- ne créer une nouvelle couche qu'en cas de manque démontré ;
- distinguer couverture démontrée, partielle, exposition, absence de preuve et violation ;
- soumettre les intégrations au cycle formalisation → candidat → cassage adversarial → correction → re-cassage → verdict ;
- `BLOCKED` n'est jamais `PASS` ;
- les règles proposées restent non normatives jusqu'à validation/adjudication.

La contradiction externe exploitable retrouvée est celle de **Grok** : elle confirme notamment le risque de surinterpréter `DecisionTrace` comme pivot central, recommande de prouver l'existence d'un producteur réel avant de créer plusieurs composants, et conclut `BLOCKED` lorsque la preuve d'intégration manque.

**Claude : aucune sortie substantielle exploitable n'a été retrouvée dans le dépôt ou les artefacts accessibles au moment de l'arbitrage. La réponse Claude disponible précédemment indiquait une indisponibilité de crédits et ne contient pas de position principe-par-principe. Elle n'est donc pas inventée ni utilisée comme preuve.**

Cette absence est explicitement conservée comme limite de provenance ; elle ne vaut pas approbation implicite.

## 2. Arbitrage principe par principe

| # | Principe candidat | Décision | Arbitrage contre la gouvernance | Effet attendu sur design / opération / tests |
|---|---|---|---|---|
| 1 | VALIDITÉ CONTEXTUELLE | **GARDER** | Déjà cohérent avec le domaine de validité, les hypothèses, les conditions d'invalidation et l'évolution de contexte. Ce principe change réellement ce qui peut être considéré comme connaissance exploitable. | Contraint les connaissances, expériences, décisions et réévaluations ; doit être testable par contexte/domaine/validité. |
| 2 | MÉMOIRE | **GARDER** | La mémoire expérimentale est déjà une exigence explicite de gouvernance : hypothèses, expériences, résultats, explications testées, échecs, connaissances validées et preuves. | Change la persistance du système et les tests de reconstruction/capitalisation. |
| 3 | AUTO-CONTESTATION | **GARDER** | C'est une fondation normative existante de méta-gouvernance. Elle protège contre les faux PASS et les angles morts du système. | Change les contrôles, audits, tests adversariaux et conditions de suspension/révision. |
| 4 | TRAÇABILITÉ | **GARDER** | Nécessaire pour répondre à « pourquoi cette décision ? ». La gouvernance distingue explicitement audit du résultat et audit du raisonnement opérationnel. | Change les contrats de preuve et les tests de reconstruction. |
| 5 | REPRODUCTIBILITÉ | **GARDER** | Déjà transversale dans provenance, recherche, validation et continuité. Elle conditionne la crédibilité des expériences et conclusions. | Change les exigences de version, provenance, données, configuration et tests de répétabilité. |
| 6 | RÉSILIENCE | **FUSIONNER** | La gouvernance l'identifie comme propriété transversale de continuité/survivabilité, pas comme justification d'une architecture autonome. | Conserve l'exigence ; supprime le risque d'une couche dédiée prématurée. |
| 7 | AUDIT DE LA GOUVERNANCE | **GARDER** | La méta-gouvernance exige déjà que la gouvernance elle-même soit contestable et que son efficacité soit évaluée. | Change les audits de gouvernance et les tests de faux PASS/bypass. |
| 8 | COMPLEXITÉ MAÎTRISÉE | **GARDER** | C'est un garde-fou direct contre la prolifération : aucune capacité ne justifie une couche sans valeur démontrée. | Change la sélection des composants et le seuil de création de nouveaux mécanismes. |
| 9 | QUANTIFICATION DE L'INCERTITUDE | **RÉDUIRE** | La gouvernance couvre déjà l'incertitude par preuves, confiance, domaine de validité, limites, invalidation et `BLOCKED`. Une couche de quantification autonome n'est pas justifiée. | Conserver la représentation de l'incertitude ; ne pas imposer une métrique universelle sans besoin démontré. |
| 10 | EXPLICABILITÉ OPÉRATIONNELLE | **FUSIONNER** | Sa valeur réelle est déjà portée par la traçabilité/reconstruction décisionnelle. Comme principe autonome, elle crée une redondance conceptuelle. | L'exigence reste testable via la reconstruction des informations, règles, incertitudes, alternatives, décision, action et résultat. |
| 11 | COÛT DE L'ERREUR | **GARDER** | Directement compatible avec la finalité du système : valeur attendue sous contraintes de risque, coût et incertitude. Il influence les décisions d'action, réduction d'exposition, suspension et arrêt. | Change les seuils de décision et les tests de conséquences ; interdit de raisonner uniquement en exactitude. |
| 12 | ALIGNEMENT DYNAMIQUE | **FUSIONNER** | Terme trop large pris seul. Sa substance utile est déjà couverte par changement/validité, évolution de gouvernance, objectifs et réévaluation. | Conserver l'exigence de réévaluer l'adéquation ; ne pas créer un mécanisme d'« alignement » générique. |
| 13 | RÉVERSIBILITÉ | **FUSIONNER** | La réversibilité est une propriété opérationnelle utile, mais principalement une conséquence de résilience, autorisation contrôlée, suspension/arrêt et reprise. | Conserver les capacités de suspension, arrêt, retour contrôlé et reprise là où le risque le justifie ; pas de couche autonome. |
| 14 | HUMILITÉ ÉPISTÉMIQUE STRUCTURÉE | **FUSIONNER** | Le contenu opérationnel est déjà porté par hypothèses, niveaux de preuve, limites, invalidation, contestation et distinction connaissance/hypothèse. Comme principe autonome, il est trop redondant. | Renforce les statuts épistémiques et les tests de surinterprétation sans ajouter de composant. |

## 3. Résultat de l'arbitrage

### GARDER
1. Validité contextuelle
2. Mémoire
3. Auto-contestation
4. Traçabilité
5. Reproductibilité
6. Audit de la gouvernance
7. Complexité maîtrisée
8. Coût de l'erreur

### FUSIONNER
9. Résilience → propriété transversale de continuité/survivabilité
10. Explicabilité opérationnelle → traçabilité/reconstruction décisionnelle
11. Alignement dynamique → changement/validité + évolution contrôlée
12. Réversibilité → résilience + autorisation/suspension/arrêt/reprise
13. Humilité épistémique structurée → incertitude + preuves + contestation + statuts de connaissance

### RÉDUIRE
14. Quantification de l'incertitude → représentation structurée de l'incertitude sans couche quantitative autonome

### LAISSER COMME HYPOTHÈSE
Aucun principe n'est promu comme capacité autonome supplémentaire sans mécanisme et preuve. Les formulations génériques non opérationnelles sont absorbées dans les principes retenus ou restent non normatives.

### REJETER
Aucun des 14 thèmes n'est rejeté comme idée sans valeur. En revanche, leurs formulations redondantes ou leur transformation en couches autonomes sont rejetées lorsqu'elles ne changent ni décision, ni action, ni résultat, ni preuve.

## 4. Test critique : « est-ce réellement architectural ? »

Le filtre appliqué est : **si le principe ne change pas le design, l'opération ou les tests, il ne devient pas une contrainte architecturale autonome.**

Résultat :
- les principes conservés ont un effet direct sur les décisions, preuves, contrôles, risques ou tests ;
- les principes fusionnés restent obligatoires, mais comme propriétés de fonctions déjà existantes ;
- la quantification de l'incertitude n'est pas promue comme couche autonome ;
- aucune nouvelle architecture n'est justifiée par le manifeste.

## 5. Limite de l'arbitrage externe

L'arbitrage est contradictoire au sens où le manifeste a été confronté à la gouvernance existante et à la contestation Grok disponible. Il n'est **pas** permis d'affirmer qu'une double sortie Claude + Grok complète est disponible : la sortie Claude substantielle manque.

Cette limite est une absence de preuve, pas un PASS implicite.

Le manifeste ci-dessous est donc **gelé comme candidat de construction** : son contenu ne doit plus être réécrit pendant la construction de la trajectoire sans passer par le mécanisme de gouvernance d'évolution. Ce gel ne constitue pas à lui seul le verdict final de l'ÉTAPE 1.
