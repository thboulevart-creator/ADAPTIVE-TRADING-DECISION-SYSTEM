# EXPLORATORY OFFLINE RESEARCH V0 — revue contradictoire et adjudication
Date : 2026-09-23
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant revue : `bbe3d60a59d6a79bec95e173409645c332f64b41`
Candidat examiné : `reports/program/2026-09-23-EXPLORATORY-OFFLINE-RESEARCH-V0-CANDIDAT.md` ; blob `63654614e74e71507a91de6412ddcba354a9be7a`.
Méthode : revue documentaire contradictoire interne ; **aucun auditeur externe indépendant, aucun test runtime, aucun test sur données réelles**.

## 1. État de départ et autorité

Le propriétaire a demandé **la revue/adjudication de V0 et la résolution textuelle minimale de §10**, pas l'exécution E0/E1. Le candidat reste intact dans l'historique et la présente revue apporte les précisions d'application qui lui manquent. L'abandon du contact Dukascopy (§191) et les preuves historiques demeurent intacts.

Références relues : `04-REFERENCE/AI-OPERATING-MEMORY.md` (§§4,5,8,10,14) ; `04-REFERENCE/RECOVERY-CHECKPOINT.md` (§§191–192) ; sauvegarde V0 du 23 septembre ; règles de sûreté GitHub ; `docs/04-VALIDATION-CRITERIA.md` (exploration/confirmation, OOS, N0) ; `docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md` ; `docs/05-DATA-CONTRACT.md` (proposition non adoptée) ; règle de couverture/borne d'exécution. La référence `docs/05` fournit des contre-exemples techniques, pas une qualification que cette revue aurait créée.

## 2. Contre-expertise interne : attaques contre V0 initial

| ID | Contre-exemple | Défaut ou risque observé | Correction déterministe exigée |
|---|---|---|---|
| A01 | « Je calcule déjà les signaux Momentum pour vérifier le CSV » sous E0 | Confusion inspection/expérience | E0 ne calcule aucun signal, position, trade ou PnL ; tout calcul stratégique est E1 |
| A02 | « Fiche acceptée » sans auteur nommé ; exécution par simple accès technique | Autorité insuffisamment explicite | Approbation **spécifique du propriétaire pour chaque run E1**, avec dataset, périmètre d'accès, borne ressources et absence de réseau ; l'adoption V0 ne donne aucune permission implicite |
| A03 | E0 scanne 376 millions de lignes sans plafond, ou écrit les fichiers temporaires dans le corpus | Exposition ressource/source | Préflight E0 proportionné, plafond ressources, accès en lecture seule, empreintes éventuellement par lot et état `INCOMPLET` si interruption |
| A04 | E1 traverse un trou ou exécute sur un timestamp reconstitué sans trace | Résultat trompeur | Tests préalables minimaux par usage (identité des octets, ordre et fuseau, trous pertinents, prix/timestamps d'exécution), rejet du segment invalide, aucun remplissage silencieux |
| A05 | Frais manquants remplacés par zéro puis résultat appelé « net réaliste » | Confusion scénario/preuve | Zéro uniquement scénario diagnostique brut ; frais non attestés : sensibilité étiquetée, pas de net réaliste ni baseline Momentum qualifiée |
| A06 | Prix regardés en E0, puis toute la période déclarée OOS vierge | Fuite par observation | Tracer **l'intensité de consultation** : métadonnées/qualité ≠ inspection des prix/résultats ; toute consultation de résultats dégrade le statut probatoire selon le cas, jamais remise à zéro |
| A07 | E1 sans amendement du §10 d'AI-OPERATING-MEMORY | Conflit normatif réel | Amender §10 explicitement ; conserver le gate confirmatoire et les exigences tick/5 ans là où applicables |
| A08 | Accord de deux parseurs synthétiques présenté comme validation BI5 universelle | Promotion illicite | Maintenir A=AMBIGUOUS, B=NOT_FOUND, C=INCOMPLETE_VERSION_COVERAGE ; global BI5 BLOCKED ; E1 limité au corpus et à la question |
| A09 | Bon résultat N0 réutilisé pour autoriser paper, test final vierge ou capital | Contournement promotion | N0 uniquement ; tout confirmatoire/OOS probatoire et tout paper/broker/live exigent des gates et autorisations séparés |
| A10 | Reconstituer des données corrigées sans nouvelle identité | Substitution | Toute transformation qui modifie les octets produit un dérivé identifié/hashé et un lien parent/version ; pas de correction silencieuse |
| A11 | Le statut « E0 adopté » permet d'ouvrir tout disque connecté | Accès non autorisé | Exiger emplacement/scope, droit/licence et autorisation effective ; accès technique ≠ autorité |
| A12 | Un run « Momentum V1 PASS » de 1 mois et sans prix à t+1 | Contradiction avec protocole déjà PASS | Préserver exigence cinq ans **pour sa qualification**, prix déterministe de t+1 et coûts documentés ; sinon seulement diagnostic distinct, ou BLOCKED selon la question |

### Qualification initiale du candidat

**FAIL DOCUMENTAIRE INITIAL**, pour A01/A02/A07 tant que les précisions opposables et la résolution §10 n'existent pas. A03–A12 sont des attaques couvertes partiellement par le candidat ; leur traitement détaillé reste nécessaire pour rendre le contrat non contournable. Il ne s'agit pas d'un FAIL d'une implémentation ni d'une invalidation des contrats historiques.

## 3. Corrections d'interprétation opposables à la version adoptée

La version V0 n'est adoptable qu'avec les précisions cumulatives suivantes (elles complètent le candidat ; aucune nouvelle couche runtime n'est créée) :

**E0** — Inventaire en lecture seule d'un corpus déjà existant *dans un emplacement et un environnement explicitement autorisés par le propriétaire*. Un préflight E0 identifie périmètre, accès licite, plafond de temps/espace/lectures, inventaire attendu et destination des seules métadonnées. Mesurer identité, qualité, couverture, anomalies et disponibilités de champs est permis ; **aucun indicateur de stratégie, signal, trade, fill, position ou PnL**. Si des valeurs de prix/résultats sont consultées plutôt que de simples métadonnées, enregistrer leur période et intensité. Une couverture non examinée est `UNVERIFIED/INCOMPLETE` ; jamais PASS par déduction de noms.

**E1** — Simulation historique offline *seulement après autorisation expresse du propriétaire pour le run précis*, distincte de son accord sur le contrat V0. L'autorisation désigne dataset exact et droits, corpus/horodatages, hypothèse ou diagnostic, conditions d'exécution, plafond ressources, isolement réseau, code et coûts/scénarios ; elle ne s'étend pas à d'autres runs. Préflight vérifiable : hashes, ordre/fuseau, trous compatibles avec horizon et signaux, prix d'exécution déterministe s'il existe un fill, interdiction de correction implicite, absence de fuite future. Si impossible, `BLOCKED` pour la question concernée. Transformations dans une copie dérivée explicitement identifiée, jamais dans le corpus brut. Une simulation avec coûts hypothétiques reçoit l'étiquette *scénario*, non *net réel observé*.

**Épistémologie** — Toute sortie E1 reste `N0 / EXPLORATOIRE`, y compris lorsqu'un résultat est reproduit ; historique de consultation de chaque période conservé. Aucun résultat E1 ne vaut validation confirmatoire, OOS vierge, qualification globale du fournisseur, décision d'allocation ou autorisation paper/broker/live. Le protocole Momentum V1 PASS est préservé : une sonde non conforme est un diagnostic distinct, sans usurper le nom de sa baseline qualifiée.

**Contrats conservés** — E0/E1 n'autorisent pas acquisition réseau/BI5 projet, FULL_INTERVAL, D materialization ni contact Dukascopy ; pas de nouveau statut sur les anciens gates ; pas de changement à `docs/04` ni à `docs/03.1.2`.

## 4. Résolution textuelle minimale du conflit §10 — condition d'adjudication

Modifier **uniquement §10** de `04-REFERENCE/AI-OPERATING-MEMORY.md` pour :
- distinguer E0 (non-backtest), E1 (exception à l'interdiction pour les simulations historiques exploratoires N0, seulement sous autorisation propre et préflight) et backtests confirmatoires (gate maintenu) ;
- préserver les exigences cinq ans, vrais ticks et coûts réalistes lorsqu'elles sont nécessaires à la *qualification visée*, notamment Momentum V1 selon son protocole ;
- n'accorder aucun droit d'exécution du seul fait du PASS documentaire de V0.

L'amendement ciblé du §10 a été persisté au commit `47bb3defb030878cbd7412bd010da1470185eb6a`, blob `70170b666c101777ff922b90c5091f2dc0976245`. La revue documentaire interne a ensuite été reprise sur ce HEAD. Ce changement est limité au §10 ; les autres sections de la mémoire opératoire sont conservées.

## 5. Conditions de relecture finale pré-enregistrées

- R01 : HEAD frais, dépôt et branche identiques, candidat original et §191 intacts.
- R02 : le texte §10 autorise explicitement E1 sans vider le gate confirmatoire ; E0 reste hors calcul stratégique.
- R03 : A01–A12 fermés par un texte opposable (candidat + cette revue + §10), sans élargissement E0/E1.
- R04 : l'adoption V0 ne suffit pas à lancer E0 hors accès autorisé ni E1 sans autorisation de run.
- R05 : aucun PASS attribué aux datasets ou anciens blocages BI5 ; aucun résultat de backtest ou qualification runtime revendiqué.
- R06 : un seul prochain mouvement : **E0 inventaire effectif borné, seulement après désignation et autorisation de l'emplacement**, pas E1 automatique.
- R07 : nouvelles mutations limitées au présent rapport, §10, checkpoint et sauvegarde ; aucune autre modification.

## 6. Relecture contradictoire du §10 persisté et décision documentaire

HEAD de la vérification ciblée : `47bb3defb030878cbd7412bd010da1470185eb6a`.

Contrôles R01–R07 : identité dépôt/branche/candidat, présence §191–§192, distinction E0 non backtest et E1 N0, gate confirmatoire inchangé dans sa fonction, dispositions A01–A12 examinées, autorisation **spécifique par run E1**, accès E0 expressément limité, conservation des statuts historiques et bornage des chemins modifiés. Les vérifications de texte/structure R01–R03 et R05–R07 ont réussi. R04 a d'abord donné un faux négatif **du contrôle lui-même** (prédicat de recherche sensible à la casse « approbation » avant vérification de l'expression correcte « Approbation ») ; un contrôle R04 corrigé, portant sur les trois phrases opposables réellement présentes, a réussi. Aucune modification du contrat n'a été justifiée par cette erreur du contrôle.

Analyse contradictoire interne : les trois défauts initiaux A01/A02/A07 sont fermés par §3 de ce rapport + §10 amendé. Les neuf autres attaques A03–A12 sont couvertes par les dispositions textuelles spécifiques, sans prétention de preuve logicielle ou de qualité d'un corpus encore inconnu. Le candidat d'origine reste historiquement immuable ; il est **adopté uniquement conjointement avec les corrections opposables §3 du présent rapport et le §10 amendé**. Une lecture isolée du candidat initial n'autorise rien.

**VERDICT : PASS DOCUMENTAIRE LIMITÉ — FRONTIÈRE EXPLORATORY OFFLINE RESEARCH V0.**

Sens exact de PASS : cohérence normative et non-contournement documentaire interne aux attaques A01–A12 et R01–R07, sous la seule portée E0/E1 précisée ici. Ne prouve ni couverture exhaustive de tous les contre-exemples, ni audit indépendant, ni gate runtime, ni accès à un dataset, ni exactitude de simulation, ni rentabilité. Une vérification finale après checkpoint et sauvegarde devra confirmer que les seules mutations sont §10, ce rapport, le checkpoint et la sauvegarde ; sinon le verdict de clôture doit être réexaminé.

**Capacité nouvellement ouverte sur le plan documentaire :** un inventaire E0 peut être autorisé par un mouvement distinct visant un emplacement et des ressources explicitement approuvés. **Aucune exécution E0 n'a lieu dans cette revue.** E1 demeure interdit tant qu'une expérience précise n'a pas reçu l'autorisation explicite du propriétaire et satisfait son préflight. Confirmation/paper/broker/live, nouvelle acquisition, FULL_INTERVAL, D materialization et contact Dukascopy restent fermés.

**Prochaine action gouvernée unique après clôture :** désigner et autoriser un périmètre E0 réel, puis effectuer un inventaire read-only borné des corpus historiques déjà disponibles ; ne pas ouvrir E1 automatiquement.

STOP.
