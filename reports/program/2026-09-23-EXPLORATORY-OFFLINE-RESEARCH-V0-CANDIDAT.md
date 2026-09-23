# EXPLORATORY OFFLINE RESEARCH V0 — frontière expérimentale candidate

Date : 2026-09-23
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD de référence vérifié avant formalisation : `fc2e634bdbb89f57b67c2dabd45cd96c60d76f9f`
Statut : **CANDIDAT DOCUMENTAIRE — NON QUALIFIÉ — AUCUNE EXÉCUTION AUTORISÉE PAR CE SEUL DOCUMENT**
Nature de l'instruction : décision explicite du propriétaire de *formaliser* une frontière unique, puis STOP avant toute implémentation.

## 1. Objet et résultat attendu

Réduire l'écart entre le dispositif de provenance/qualification existant et les expériences produisant des résultats économiques sur des stratégies, en commençant par Momentum V1 et des témoins simples. La rentabilité, l'admissibilité d'un corpus concret et la fidélité d'une exécution historique restent des questions à démontrer, jamais des prémisses.

La frontière proposée distingue strictement :
- **E0 — Inventaire/lecture hors ligne de corpus historiques existants**, sans mutation des sources ;
- **E1 — Simulation historique exploratoire hors ligne, bornée par une fiche d'expérience préalablement acceptée**, avec résultats limités au niveau N0 ;
- **C — Recherche confirmatoire / validation OOS à statut probatoire déclaré**, soumise aux contrats de validation propres ;
- **P — Paper, broker et live**, soumis à leurs autorisations distinctes et actuellement fermés.

E0 et E1 sont les seules capacités visées. C et P ne sont pas ouverts par cette formalisation.

## 2. Autorité, hiérarchie et conflit à résoudre

Références déjà présentes et conservées :
- `04-REFERENCE/AI-OPERATING-MEMORY.md`, notamment §4, §8, **§10** et §14 ;
- `04-REFERENCE/RECOVERY-CHECKPOINT.md`, §191 ;
- `reports/program/2026-09-23-ARRET-CONTACT-DUKASCOPY-REORIENTATION-PORTFOLIO.md` ;
- `docs/04-VALIDATION-CRITERIA.md`, §0 (exploration ≠ confirmation), §3 et §7 ;
- `docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md`.

**Conflit explicite :** le §10 d'AI-OPERATING-MEMORY interdit actuellement tout « real backtest » tant que tous les blocs obligatoires ne sont pas PASS. La décision du propriétaire de formaliser E0/E1 n'efface pas cette règle, ne prononce aucun PASS et ne vaut pas autorisation d'exécution réelle.

**Disposition candidate proportionnée :** lors de l'adjudication de V0, modifier *explicitement et seulement pour E1* la portée opérationnelle du §10 : maintenir l'interdiction des backtests confirmatoires et des usages opérationnels jusqu'à satisfaction de leurs gates ; permettre une simulation historique **strictement exploratoire N0**, hors ligne et sur corpus existant, uniquement après préflight d'expérience E1 accepté. L'amendement exact devra être validé et inscrit au checkpoint avant la première simulation E1 sur données réelles. Un résultat E1 n'hérite d'aucun PASS BI5 global, Q/F/FULL_INTERVAL, N1-N4 ou P1.1 positif.

**Effet présent de V0 candidat :** droit de formaliser cette frontière et de la soumettre à une revue bornée, pas droit d'exécuter E1. Une fois E0 adopté et le périmètre d'accès établi, l'inventaire/lecture E0 n'est pas une acquisition externe ni un backtest. Toute donnée protégée, tout environnement non désigné et toute dépense demandent une autorisation spécifique.

## 3. E0 — Périmètre proposé pour l'inventaire en lecture seule

Entrées : corpus historiques **déjà détenus et accessibles légalement** dans un emplacement expressément désigné ; CSV, Parquet, export MT5 ou autre représentation décrite. L'existence locale, les droits d'accès, la licence d'usage et les hashes ne sont **pas présumés**.

Opérations E0 prévues : inventaire des fichiers ; inspection en lecture seule du schéma, des métadonnées et d'échantillons tracés ; hashing exact des octets accessibles ; bornes temporelles, comptages, doublons, ordre, trous, fuseau, construction H1, sessions et champs de prix ; provenance, version et restrictions d'usage. Ne jamais corriger silencieusement, interpoler ou considérer un nom de fichier comme une preuve de couverture.

Sortie minimale E0 :
`dataset_id / source / instrument / representation / granularity / timezone / période observée / hashes / schema / coverage / gaps / anomalies / bid-ask-spread disponibles / licence / emplacements et limites d'accès / usages envisageables et interdits`.

L'absence de corpus accessible produit `BLOCKED — CORPUS NON IDENTIFIÉ`, non un dataset fictif. Une faille de qualité peut être acceptable pour une question exploratoire limitée mais bloquante pour une autre ; la décision doit être explicite **par usage**.

Hors E0 : nouveau téléchargement fournisseur, scraping réseau de données de marché, BI5 GET de projet, FULL_INTERVAL, D materialization, écriture/réparation du corpus d'origine, publication de corpus sous licence restrictive, accès aux identifiants/broker, tout formulaire ou contact Dukascopy.

## 4. E1 — Périmètre proposé d'une simulation exploratoire bornée

Aucune simulation E1 sur données réelles avant : (a) adoption de la frontière et harmonisation expresse avec le §10, (b) autorisation de l'expérience précise, (c) préflight documenté et accepté.

La fiche minimale **avant chaque exécution E1** doit identifier :
1. hypothèse ou simple diagnostic de plomberie, actif, horizon, résultat recherché, stratégie exacte et témoins ;
2. `dataset_id`, version/hash et origine, période exacte, schéma, fuseau, granularité, qualité/continuité et limites compatibles avec le test ;
3. commit de code, paramètres figés pour ce run, calendrier/sessions, warmup, horodatage d'information disponible, signal à clôture de t et exécution au plus tôt t+1 ;
4. méthode de formation des barres, prix d'exécution déterministe disponible, conversion des unités/PnL, spread, commission et slippage applicables : valeurs attestées ou scénarios de sensibilité **explicitement non présentés comme réalistes** ;
5. bornes de lecture, plafond de ressources et de fichiers, absence de réseau et de tout ordre, traitements reproductibles, témoins, métriques, invalidations et conditions d'abandon ;
6. journal de consultation des périodes, et statut explicitement N0 de tout résultat ; si une période a été explorée, ne plus la présenter ensuite comme juge final vierge.

**Momentum V1 particulier :** reprendre intégralement le protocole PASS du document 3.1.2, sans optimiser horizon, sorties, prix ou règles après résultat. Son protocole exige au moins cinq ans pour un **résultat de qualification**, un prix déterministe au premier point admissible de t+1 et des coûts requis documentés. Si ceux-ci manquent, l'exécution prétendant satisfaire cette baseline est `BLOCKED`. Une sonde plus courte, brute ou utilisant des scénarios de coût non attestés est seulement un diagnostic exploratoire séparé et étiqueté, jamais « Momentum V1 baseline PASS ».

Résultats E1 attendus, si ultérieurement exécuté : journal des trades/fills, PnL brut/net ou sensibilité non assimilable au net réaliste, turnover, exposition, drawdown, métriques par période, témoins, anomalies, limites, hashes, explications concurrentes, piste de falsification ou abandon. Jamais de rendement garanti ni de recommandation d'engagement de capital.

## 5. Frontières de non-promotion

| Situation | Usage E0/E1 proposé | Qualification / production |
|---|---|---|
| CSV/Parquet avec provenance partielle | E0 possible ; E1 seulement pour question compatible et limites visibles | Pas de promotion de provenance |
| Représentation BI5 native avec A/B/C ouverts | Incertitudes conservées ; choisir autre source si besoin | A=AMBIGUOUS, B=NOT_FOUND, C=INCOMPLETE_VERSION_COVERAGE ; gate natif global toujours BLOCKED |
| Données H1 sans ticks | Diagnostics de signal H1 possibles ; simulation de fills seulement si ses hypothèses sont honnêtes et explicites | Aucune preuve d'exécution tick |
| Données consultées en exploration | Étudier/formuler une hypothèse | Période non réutilisable en prétendant qu'elle est vierge OOS |
| Coûts obligatoires inconnus | Diagnostic brut ou stress séparé, non qualifiant | Baseline exigeant coûts réalistes = BLOCKED |
| Résultat exploratoire favorable | Hypothèse candidate à tester plus tard | N0 seulement ; aucun N1–N4, paper/broker/live |

Interdictions inchangées : contact Dukascopy, R-04/R-05/R-06, acquisition BI5 de projet, FULL_INTERVAL, D materialization, backtest confirmatoire, promotion de données non qualifiées, capital réel, paper/broker/live, ordre de marché, activation P1.1 positive. Aucun effacement des closeouts, archives, preuves ou anciens verdicts.

## 6. Revue adversariale nécessaire avant activation

Soumettre le candidat, sans test d'exécution à ce stade, aux contre-exemples suivants :
- E1 déguisé en « diagnostic E0 » ;
- données détenues mais non accessibles/licenciées ;
- manque de prix à t+1, trous traversés silencieusement, changement de fuseau, fuite temporelle ;
- coût inconnu remplacé par zéro puis appelé « PnL net réel » ;
- réemploi d'une période consultée comme OOS vierge ;
- PASS synthétique ou double parseur assimilé à une vérité fournisseur ;
- publication d'un bon résultat N0 comme qualification, ou accès paper/broker par glissement sémantique ;
- tentative d'exécuter E1 sans amendement explicite du §10.

La formalisation ne constitue pas ce cassage. Aucun statut PASS n'est attribué à V0.

## 7. Disposition et arrêt

**Livrable actuel : un seul candidat de frontière, sans code, sans nouveau dataset, sans backtest, sans réseau fournisseur.**

Prochaine action gouvernée unique *après cette formalisation* : **revue contradictoire/adjudication de cette frontière V0 et résolution textuelle minimale du conflit avec le §10**, puis décision PASS / FAIL / BLOCKED sur le périmètre documentaire seulement. Si ce mouvement est accepté, l'action utile suivante sera l'inventaire E0 des corpus existants, sans ajout de nouvelle couche générale.

STOP — NE PAS IMPLÉMENTER OU EXÉCUTER E0/E1 DANS LE MOUVEMENT DE FORMALISATION.
