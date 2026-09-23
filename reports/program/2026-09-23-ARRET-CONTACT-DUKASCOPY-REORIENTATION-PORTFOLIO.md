# Décision de réorientation — Arrêt définitif de la voie « contact Dukascopy »

Date : 2026-09-23
Dépôt : thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM
Branche : integration/system-v1
Décision : DEMANDE EXPLICITE DE L’UTILISATEUR / EFFET IMMÉDIAT

## 1. Instruction impérative

La voie de contact direct avec Dukascopy est retirée du plan actif du projet.

Sont abandonnés, sans création de leurs successeurs :
- B-PE-SEM-05R-04 : constitution et scellement d’un message sortant ;
- B-PE-SEM-05R-05 : envoi du message et capture de l’envoi ;
- B-PE-SEM-05R-06 : capture et exploitation de la réponse ;
- toute préparation, relance ou nouvelle tentative de contact Dukascopy justifiée par ces blocs.

Aucun message, formulaire ni ticket ne doit être envoyé ou préparé dans ce cadre. Les anciens contrats d’enquête et de résolution de canal deviennent des **archives historiques sans effet opérationnel**. Leurs verdicts PASS concernent uniquement la qualité de leurs propres artefacts passés et **n’autorisent aucune action présente**.

L’arrêt de cette voie est une décision de pilotage et non la prétention que les incertitudes sémantiques natives BI5 auraient été résolues.

## 2. Objectif à nouveau prioritaire

Construire et évaluer un portefeuille de stratégies de trading algorithmiques dont la performance et les risques sont mesurés hors échantillon, nets de frais, avec reproductibilité et contrôle des faux positifs.

L’objectif n’est pas de rendre parfaite la documentation d’un fournisseur. Les mécanismes de preuve et de gouvernance doivent répondre à une nécessité expérimentale démontrée, et non être une fin en soi.

Aucune rentabilité n’est présumée, garantie ou déclarée acquise.

## 3. Traitement des acquis

Conserver en archives auditables :
- recherche documentaire et logicielle Dukascopy ;
- qualification historique B-PE-SEM-05/R01/R02/R03 ;
- limites A = AMBIGUOUS, B = NOT_FOUND, C = INCOMPLETE_VERSION_COVERAGE ;
- implémentations et contrôles génériques déjà qualifiés ;
- inventaire de données et fenêtre de recherche existante.

Ne pas convertir les anciennes hypothèses du format natif BI5 en vérités prouvées. Ne pas transférer un PASS documentaire ou de compatibilité synthétique vers un PASS global réel. La voie native BI5 demeure une option de données **sous limites documentées**, pas un préalable exclusif à toute recherche.

## 4. Cadre du prochain mouvement

Prochaine action gouvernée unique :

POST-ARRET-CONTACT-DUKASCOPY —
RECADRAGE EXPERIMENTAL PORTEFEUILLE V0
— AUDIT / DECISION UNIQUEMENT.

Séquence :
1. fresh HEAD ; relire la présente décision et le checkpoint ;
2. inventorier les données réellement accessibles et leur qualité (existantes, autres sources autorisées, Parquet/CSV/MT5 selon disponibilités) ;
3. distinguer les défauts bloquant une expérience précise des incertitudes non bloquantes pour d’autres expériences ;
4. inventorier les composants stratégiques et expérimentaux déjà implémentés et qualifiés ;
5. définir un premier test économique minimal : Momentum V1 et témoins simples, puis tester des approches suffisamment distinctes si les résultats le justifient ;
6. choisir une seule première expérience bornée avec identité des données, coûts, séparation temporelle, comparaison témoin, critères d’arrêt et résultats auditables ;
7. définir une progression vers un portefeuille : validation individuelle hors échantillon, corrélations des pertes, exposition agrégée, capacité d’exécution, drawdown et robustesse ;
8. inscrire ce nouveau chemin sans affaiblir rétroactivement les qualifications historiques ni autoriser trading réel par simple décision documentaire ;
9. STOP après la sélection.

La recherche et le développement de stratégies peuvent avancer sur des données qualifiées **pour l’usage expérimental considéré** sans attendre une déclaration externe exhaustive sur tous les octets du format natif historique. Toute simulation doit afficher explicitement la classe de fiabilité des données et les limites sur les conclusions qu’elle autorise. Les expériences exploratoires ne sont pas des validations d’exploitation réelle.

## 5. Données et critères indispensables, à fixer lors du recadrage

Au minimum : instrument, période, granularité pertinente, fuseau et sessions, spread/commissions/slippage, trous de données, règles anti-fuite temporelle, train/validation/test chronologiques, comparaison témoin, métriques de risque et rendement, stabilité entre régimes, reproductibilité.

Éviter d’imposer une profondeur tick universelle si la première hypothèse se teste honnêtement avec des barres ; si la décision ou l’exécution dépendent du tick, exiger une preuve de qualité tick adaptée à ce test.

## 6. Frontière

Interdits à partir de cette décision :
- préparation ou envoi de contact Dukascopy ;
- ouverture B-PE-SEM-05R-04/R05/R06 ;
- réactivation automatique de la voie contact ;
- promotion silencieuse des anciennes incertitudes BI5 au rang de preuves ;
- passage automatique de tests exploratoires à paper/broker/live.

Les travaux futurs sur données, stratégies, backtests et portefeuille doivent recevoir leurs propres autorisations proportionnées et explicites. Ils ne dépendent plus d’une réponse Dukascopy.

STOP.
