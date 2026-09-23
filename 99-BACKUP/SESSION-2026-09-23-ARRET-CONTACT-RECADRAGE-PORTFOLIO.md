# Sauvegarde — arrêt du contact Dukascopy et reprise portefeuille

Date : 2026-09-23
Dépôt : thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM
Branche : integration/system-v1

## Instruction utilisateur

Le contact Dukascopy est explicitement abandonné. Ne plus proposer, préparer ou exécuter de courrier, formulaire, ticket, envoi ou relance Dukascopy. Ne plus demander d'identité utilisateur pour ces formulaires.

La décision primaire est :
reports/program/2026-09-23-ARRET-CONTACT-DUKASCOPY-REORIENTATION-PORTFOLIO.md
blob : b19537e2720a64945fa481e4ab526d87df6a3d6c

Le checkpoint section 191 supplante les sections 189/190 relatives à R-04 :
04-REFERENCE/RECOVERY-CHECKPOINT.md
blob avant cette sauvegarde : 3a1bc4ae6eda338352eec2d9be5a02b7c4a0ac30

Les workflows de contact R-02/R-03 ont été retirés de la branche active ; les rapports, contrats et qualifications historiques sont conservés en archives auditables.

## État technique conservé sans promotion abusive

B-PE-SEM-05R-03 CLOSED / PASS historique sur résolution du canal uniquement.

A = AMBIGUOUS
B = NOT_FOUND
C = INCOMPLETE_VERSION_COVERAGE

Qualification globale de la représentation BI5 native = BLOCKED pour son propre périmètre. Ne pas assimiler tests de compatibilité synthétique, accord de deux parseurs ou plausibilité de prix à une preuve externe exhaustive. Cela ne doit pas bloquer les expériences avec d'autres sources ou granularités si elles sont admissibles pour l'hypothèse testée.

Aucune réponse Dukascopy n'est requise avant de poursuivre la recherche de stratégies.

## Objectif principal

Construire, tester et sélectionner des stratégies de trading algorithmiques, puis évaluer un portefeuille diversifié de stratégies, avec résultats hors échantillon nets de frais, robustesse, contraintes d'exécution et gestion du risque agrégé. Rentabilité non présumée.

Conserver le dispositif de mémoire expérimentale : hypothèses, jeux de données et limites, protocoles, résultats, explications concurrentes, échecs, conclusions et statut de preuve.

## Prochaine action gouvernée unique

POST-ARRET-CONTACT-DUKASCOPY —
RECADRAGE EXPERIMENTAL PORTEFEUILLE V0 —
AUDIT / DECISION UNIQUEMENT.

Après fresh HEAD et relecture du checkpoint et de cette décision :
1. Inventorier les jeux de données réellement accessibles et distinguer présence, qualité et admissibilité selon l'expérience (CSV, Parquet, MT5, autres sources disponibles).
2. Inventorier ce qui existe déjà : Momentum V1, stratégie de base et témoins, moteur de recherche, test/rejeu, contrôles temporels, frais, mémoire expérimentale.
3. Proposer un premier test borné d'une hypothèse de stratégie avec dataset identifié, témoin, split chronologique train/validation/test, coûts, métriques de risque, seuils d'abandon et analyse des hypothèses.
4. Choisir le plus petit bloc expérimental utile à l'objectif portefeuille ; ne pas ajouter de nouvelles barrières documentaires non justifiées par ce test.
5. Arrêter après la décision ; n'activer ni paper/broker/live ni promotion implicite de données non qualifiées.

La première piste candidate existante est Momentum V1, sans imposer d'emblée le tick BI5 de Dukascopy si une autre granularité adaptée à l'hypothèse permet un test honnête.

## Interdictions actives

Ne pas ouvrir B-PE-SEM-05R-04/R-05/R-06.
Ne pas réintroduire le contact fournisseur sauf nouvelle instruction explicite.
Ne pas réécrire l'histoire ni effacer les preuves d'audit passées.
Ne pas transformer une expérience exploratoire en validation de trading réel sans gate spécifique.

## État GitHub lors de cette sauvegarde

HEAD vérifié avant sauvegarde : 8658cb68829f89dbb04d5c2c92b965b491d8d687
Message : checkpoint: supersede Dukascopy contact path with portfolio research objective

Revalider impérativement le fresh HEAD à la prochaine session.

STOP.
