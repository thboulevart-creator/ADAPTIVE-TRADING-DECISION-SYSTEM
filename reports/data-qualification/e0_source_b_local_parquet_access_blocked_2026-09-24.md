# E0-SOURCE-B — accès local Parquet non établi

Date : 2026-09-24
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD après préflight : `057bf66f7af8a9ec80da2dd9ce6f0d4e086f1d99`
Préflight : `reports/data-qualification/e0_source_b_preflight_2026-09-24.md`

## Verdict

**BLOCKED — CORPUS LOCAL NON ACCESSIBLE DANS L'ENVIRONNEMENT D'EXÉCUTION COURANT**

Le périmètre autorisé était exclusivement :

`data/research_source_b_ustech/parquet/`

Aucun autre dataset n'a été substitué.

## Vérifications réellement effectuées

Après persistance du budget **avant toute lecture de Parquet**, l'environnement d'exécution a été inspecté uniquement pour établir la présence du chemin :

- répertoire courant de l'environnement : `/` ;
- `/mnt/data` accessible mais ne contient pas le corpus ;
- `data/research_source_b_ustech/parquet/` absent depuis le répertoire courant ;
- `/mnt/data/data/research_source_b_ustech/parquet/` absent ;
- recherche de métadonnées bornée sous `/home`, `/mnt`, `/workspace`, `/workspaces`, `/tmp` jusqu'à profondeur 8 :
  - aucun clone `ADAPTIVE-TRADING-DECISION-SYSTEM` trouvé ;
  - aucun dossier `research_source_b_ustech` trouvé ;
  - aucun chemin se terminant par `data/research_source_b_ustech/parquet` trouvé ;
- aucun fichier n'est attaché à la conversation courante ;
- deux recherches par titre dans la Library (`research_source_b_ustech parquet`, `.parquet`, puis `parquet`, `USTECH`) n'ont retourné aucune copie directement récupérable sous ces noms.

Le zéro résultat de recherche Library n'est pas utilisé comme preuve générale d'absence sur le compte ; le blocage repose sur l'absence du chemin dans **l'environnement local effectivement accessible à cette session** et l'absence de fichier/copie fourni à cette session.

## Budget préenregistré — non consommé sur le corpus

Le budget E0 avait été figé avant accès :

- maximum 1 000 entrées filesystem ;
- maximum 500 fichiers Parquet ;
- maximum 16 GiB de lecture cumulée des octets de fichiers ;
- maximum 128 MiB de footers/métadonnées ;
- aucun fichier individuel > 8 GiB lu intégralement ;
- aucun suivi de symlink hors périmètre ;
- aucune écriture dans le corpus ;
- aucune stratégie, trade, PnL ou backtest.

Aucun octet Parquet n'a été lu, donc aucune de ces bornes de contenu n'a été consommée.

## Ce qui n'est PAS établi

Ne pas réutiliser des chiffres provenant d'anciens échanges comme s'ils avaient été observés aujourd'hui. Dans ce mouvement, sont **NON VÉRIFIÉS** :

- existence actuelle du corpus local ;
- nombre de fichiers ;
- volume total ;
- nombre de lignes ;
- hashes ;
- schéma ;
- colonnes temporelles ;
- période réelle ;
- continuité ;
- trous ;
- fuseau/sessions ;
- champs bid/ask/spread ;
- provenance/licence ;
- admissibilité pour Momentum V1 ou portefeuille.

La présence passée alléguée d'un corpus local ne remplace pas l'observation actuelle.

## Environnement logiciel

L'absence du corpus intervient avant toute question de lecture Parquet. À titre de diagnostic secondaire seulement : `pandas` est présent dans l'environnement, tandis que `pyarrow`, `duckdb` et `fastparquet` n'y sont pas installés actuellement. Ce point n'est pas la cause du verdict ; le chemin est déjà absent/inaccessible.

## Limites de l'environnement

Cette session ne dispose pas d'un accès général au disque Windows/local de l'utilisateur. Le container d'exécution n'est pas le PC de l'utilisateur et aucun montage du clone local n'a été observé. Il serait faux de déclarer le corpus inexistant sur le PC ; seule son **inaccessibilité depuis cette session** est démontrée.

## Prochaine action gouvernée unique

**E0-SOURCE-B-ACCESS — rendre le chemin exact ou une copie/manifest fidèle du corpus existant accessible à la session, sans téléchargement fournisseur.**

Acceptable :
- attacher ou monter le dossier/corpus existant ;
- fournir une copie en lecture seule ;
- fournir un manifest exact des fichiers accompagné, idéalement, de leurs tailles/hashes et d'un moyen d'accéder ensuite aux octets nécessaires.

Une fois l'accès établi, refaire fresh HEAD, relire le préflight, conserver les mêmes plafonds sauf nouvelle décision explicite, puis exécuter l'inventaire E0.

Ne pas ouvrir E1, ne pas backtester, ne pas développer Momentum, ne pas utiliser paper/broker/live, ne pas réactiver le contact Dukascopy.

STOP.
