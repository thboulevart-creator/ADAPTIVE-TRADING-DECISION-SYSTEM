# Apprentissage par l’expérience et adaptation gouvernée — V0.1

Date : 19 septembre 2026.
Statut : **CANDIDAT D’ARCHITECTURE — NON QUALIFIÉ — NON IMPLÉMENTÉ PAR CET AJOUT**.

## Intention du propriétaire

Le système doit pouvoir construire progressivement une partie de ses connaissances, modèles, heuristiques et stratégies à partir de ses expériences, plutôt que dépendre exclusivement de règles anticipées par son concepteur. Il doit proposer et tester ses propres améliorations, conserver réussites et échecs et adapter son comportement lorsque les preuves le justifient.

Cette intention est enregistrée dès maintenant. Elle ne prouve ni une intelligence générale, ni une amélioration automatique. Le mécanisme proposé ci-dessous reste à qualifier. Ce document complète les exigences existantes sans remplacer les contrats qualifiés ni autoriser leur contournement.

## Boucle minimale à construire

1. Observer un contexte et retrouver les expériences pertinentes, avec leur provenance et leurs limites.
2. Formuler une hypothèse réfutable et une modification candidate identifiée.
3. Fixer avant le test la référence de comparaison, la métrique utile, les contraintes, le budget d’exploration, la durée, les critères de succès, d’arrêt et d’invalidation.
4. Tester dans un environnement isolé ou dans un périmètre explicitement autorisé.
5. Mesurer l’effet observé, les coûts, les effets indésirables et l’incertitude ; distinguer corrélation, soutien causal et résultat non interprétable.
6. Conserver une expérience et une conclusion contextualisée, y compris en cas d’échec ou d’absence de conclusion.
7. Évaluer la proposition sur des données réservées, avec un évaluateur et des critères que le proposant ne peut pas modifier pour réussir.
8. Adopter uniquement dans le périmètre autorisé, surveiller la dérive et restaurer la version précédente si les conditions de validité disparaissent.

Une mémoire consultable ne suffit pas : il faudra démontrer qu’une expérience modifie une décision ultérieure de façon traçable et améliore un résultat sur des observations nouvelles.

## Objets logiques proposés, à mapper sur l’existant

- **Expérience** : identifiant, contexte, hypothèse, version du système, sources et empreintes des données, action, prédiction, protocole, résultat, qualité de mesure, coûts, facteurs de confusion, contradictions, limites.
- **Connaissance candidate** : conclusion, expériences sources, explications réellement testées, domaine de validité, incertitude, conditions de réutilisation, expiration et invalidation.
- **Proposition d’adaptation** : version de départ, changement exact, justification, périmètre, protocole d’évaluation, budget, risques, retour arrière.
- **Décision de promotion** : identité de l’évaluateur autorisé, preuves, critères figés, verdict motivé, version activée et autorisation distincte.

Ce sont des responsabilités logiques ; ne pas créer quatre nouveaux sous-systèmes si les modèles existants les couvrent.

## Frontière d’autorité

L’adaptation peut proposer des changements de paramètres, de modèles, de stratégies, de recherche ou de code. Au premier incrément, ces changements restent en simulation ou observation parallèle, sans effets externes.

Une autonomie ultérieure d’activation peut être déléguée dans une enveloppe préalablement qualifiée : changements autorisés, budget, seuils, durée et retour arrière. Aucune délégation illimitée n’est implicite.

L’apprenant ne peut pas augmenter ses permissions ou budgets, changer seul l’objectif ou la métrique de jugement, modifier ses propres tests de qualification, écraser les preuves contradictoires ni s’attribuer une autorisation. Une proposition de modification de ces éléments suit une requalification séparée.

Conserver les faits et leurs révisions sans écrasement silencieux. Prévoir rétention, minimisation et suppression autorisée des données sensibles ; la traçabilité ne justifie pas une conservation illimitée.

## Critères de démonstration et attaques nécessaires

- Une expérience réutilisée cite ses preuves et vérifie l’adéquation du nouveau contexte.
- Un gain sur les seules données d’apprentissage ne permet pas une promotion ; contrôler fuite de données, essais multiples et sélection opportuniste des résultats.
- Un résultat favorable avec mesure invalide, coûts excessifs ou contrainte violée ne permet pas une promotion.
- Une preuve absente, falsifiée, périmée ou provenant d’un autre candidat est rejetée.
- Un proposant ne peut pas remplacer l’évaluateur, les critères ou les données réservées.
- Un changement de régime peut provoquer abstention, retest ou rétrogradation ; une seule observation ne crée pas une règle universelle.
- Un redémarrage conserve expériences, versions et décisions ; une régression permet un retour arrière vérifiable.
- Une amélioration locale ne se transfère pas automatiquement aux autres dépôts : tout transfert reste une hypothèse à tester.
- Une expérience synthétique prouve au mieux le mécanisme logiciel ; elle ne prouve pas une valeur réelle dans le domaine.

Aucun seuil statistique universel n’est fixé ici. Leur choix et la taille d’échantillon doivent dépendre du domaine, du coût d’erreur et du protocole arrêté avant l’évaluation.

## Ordre de réalisation

Cartographier l’existant → spécifier le plus petit parcours expérience/connaissance/proposition/évaluation → casser ses frontières → implémenter → vérifier sur des cas contrôlés → mesurer sur données nouvelles → autoriser un périmètre borné → surveiller.

Commencer par l’apprentissage de connaissances et le choix entre stratégies autorisées. La génération de code et la révision des méthodes d’apprentissage viennent seulement après démonstration de valeur et qualification des protections correspondantes.

## Ancrage dans ce dépôt

Réutiliser `GOVERNANCE/EXPERIMENTAL-MEMORY-CHARTER.md`. Le manifeste `GOVERNANCE/TRUSTWORTHY-INTELLIGENT-SYSTEM-MANIFESTO-CANDIDATE.md` reste candidat ; cet ajout ne le promeut pas.

L’index de reprise de main mentionne B09 BLOCKED, mais renvoie explicitement au checkpoint de `feat/v4-3-instrument-contracts`. Celui lu le 19 septembre décrit B09 PASS historique, le protocole 3.1.2 PASS et son exécution BLOCKED faute de données multi-années et d’environnement vérifiés. Conserver ces distinctions ; aucun backtest n’a été exécuté dans ce chantier.

Application envisagée : apprendre les conditions de validité des stratégies et leur dégradation après coûts. Comparaison hors échantillon, découpage temporel, nombre total d’essais, spread, commissions, slippage, risque et drawdown doivent participer à l’évaluation. Le profit brut seul ne qualifie rien.

Les exigences existantes de données, ticks réels, durée minimale applicable et qualification préalable restent en vigueur. Aucune transaction réelle, hausse de risque ou modification du protocole momentum n’est autorisée par ce document.

Prochaine action unique pour CE chantier : mapper une expérience de recherche à la charte existante et définir son contrat de consommation par une décision future, sans lancer le baseline bloqué ni rouvrir les blocs historiques.

## Point de reprise de ce chantier

Dépôt : ADAPTIVE-TRADING-DECISION-SYSTEM.
Base main inspectée : `43ec28f3e09856fe508874af3aaf32079761d2d5`.
Branche : `docs/apprentissage-experience-2026-09-19`.
Périmètre : formalisation documentaire de l’intention et des critères ; aucun code, test ou contrat qualifié modifié.
Qualification technique : **BLOCKED — mécanisme non implémenté ni exécuté par ce chantier**.
La prochaine action est celle précisée dans l’ancrage ci-dessus ; elle ne remplace pas le checkpoint des autres chantiers.
