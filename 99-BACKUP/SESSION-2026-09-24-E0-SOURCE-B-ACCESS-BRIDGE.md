# Sauvegarde — E0-SOURCE-B-ACCESS bridge local

Date : 2026-09-24
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## État initial

Fresh HEAD :
`a0f2dfe250f17a7cc89497363c74aa8e06ba665a`.

Le §195 indiquait :
- préflight E0 chiffré déjà persisté ;
- corpus local `data/research_source_b_ustech/parquet/` inaccessible à la session ;
- aucun octet Parquet lu ;
- E1 fermé.

## Action effectuée

Un helper local read-only a été préparé afin de transformer l'accès local du propriétaire en un manifest exact attachable à la session :

`tools/e0_source_b_access_manifest.py`
blob `892ceca1d7f64572f16de9a8a874fe8c3cacec44`.

Rapport :
`reports/data-qualification/e0_source_b_access_bridge_2026-09-24.md`
blob `72b5fd167663d7cf38bf74242244736c4e61b7c0`.

Checkpoint §196 :
commit `6ed11820adaf9a7434984d51027b7ac192d51d7c`
blob `ca515f62a42c297e6b63b594879285f8790912b3`.

Un premier helper PowerShell a été créé mais supprimé avant activation après revue statique, car son approche de chemin relatif dépendait d'une API .NET variable et son énumération pouvait matérialiser tout l'arbre avant contrôle du budget. Il ne doit pas être utilisé.

## Budget conservé sans élargissement

Le helper Python reprend strictement le préflight déjà persisté :
- 1 000 entrées max ;
- 500 fichiers Parquet max ;
- 16 GiB total de lecture pour hashing ;
- 128 MiB de métadonnées ;
- aucun fichier > 8 GiB lu intégralement ;
- aucun symlink suivi ;
- aucune écriture corpus ;
- aucune stratégie/trade/PNL/backtest.

Il produit un JSON hors corpus, par défaut :
`%TEMP%\ATDS-E0-SOURCE-B-MANIFEST.json`.

## Test du bridge

Avant versionnement, une copie identique du helper Python a été :
- compilée par `python -m py_compile` ;
- exécutée sur deux fichiers synthétiques temporaires encadrés par `PAR1` ;
- résultat : `MANIFEST_COMPLETE`, 2 fichiers, SHA-256 complets, magic PASS, snapshot stable.

Ce test ne porte pas sur Source-B.

## État actuel

**ACCESS BRIDGE = READY.**
**CORPUS SOURCE-B = TOUJOURS INACCESSIBLE DANS CETTE SESSION.**

Aucun octet du corpus réel n'a été lu. Aucun chiffre historique sur ses fichiers/lignes/couverture n'est considéré comme observation actuelle.

E1, confirmatoire, paper/broker/live, capital réel, acquisition fournisseur et contact Dukascopy restent fermés.

## Prochaine action gouvernée unique

Sur le PC/clone local contenant réellement Source-B, exécuter depuis la racine ATDS :

`python tools/e0_source_b_access_manifest.py`

Puis rendre le fichier `%TEMP%\ATDS-E0-SOURCE-B-MANIFEST.json` accessible à cette conversation/session. Même si le statut est `BLOCKED_*`, conserver et joindre le JSON. Ne pas contourner le budget.

Après réception : fresh HEAD, adjudication du manifest, puis seulement sélection bornée des octets/footers nécessaires.

STOP.
