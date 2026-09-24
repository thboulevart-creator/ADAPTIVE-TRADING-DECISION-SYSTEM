# Sauvegarde — E0-SOURCE-B accès corpus Parquet local BLOCKED

Date : 2026-09-24
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## État initial

Fresh HEAD :
`652ef8bdfe4f99d5ac336ff509d8bfef5b47ebaf`.

Checkpoint actif §194 : prochaine action = E0 sur le corpus local
`data/research_source_b_ustech/parquet/`, budget à fixer avant lecture.

## Préflight préenregistré

Fichier :
`reports/data-qualification/e0_source_b_preflight_2026-09-24.md`
commit :
`057bf66f7af8a9ec80da2dd9ce6f0d4e086f1d99`.

Budget inchangé :
- 1 000 entrées maximum ;
- 500 fichiers Parquet maximum ;
- 16 GiB de lecture cumulée des octets ;
- 128 MiB de footers/métadonnées ;
- fichier > 8 GiB non lu intégralement ;
- aucun symlink hors périmètre ;
- zéro écriture corpus ;
- zéro stratégie/trade/PNL/backtest.

Le budget a été persisté **avant** la première tentative d'accès au chemin.

## Résultat d'accès

L'environnement d'exécution de cette session n'est pas le disque Windows de l'utilisateur. Aucun clone ATDS ni corpus Source-B n'était monté.

Vérifications de présence uniquement :
- chemin relatif depuis `/` : absent ;
- chemin sous `/mnt/data` : absent ;
- recherche bornée de dossiers sous `/home`, `/mnt`, `/workspace`, `/workspaces`, `/tmp` : aucun `research_source_b_ustech`, aucun chemin exact, aucun clone `ADAPTIVE-TRADING-DECISION-SYSTEM` ;
- conversation : aucun fichier attaché ;
- Library : recherches ciblées par titres `research_source_b_ustech/parquet/USTECH` sans résultat récupérable.

Ces constats n'établissent pas l'inexistence du corpus sur le PC ; ils établissent uniquement son **inaccessibilité dans la session**.

Aucun octet `.parquet` n'a été lu. Aucun hash, schéma, période, nombre de lignes ou trou n'a été inventé à partir des anciens échanges.

Rapport BLOCKED :
`reports/data-qualification/e0_source_b_local_parquet_access_blocked_2026-09-24.md`
blob :
`1833b723036276adac86167863a4f3b44250d29f`
commit :
`968a545cc0a08b332c461d933c53fd0228ab1d61`.

Checkpoint §195 :
commit `253b3b65ea5a0c606cc28e9a91b4760847bf043b`
blob `1002ee42a29df1c8559721c6806a8db0e3045db0`.

## Verdict

**E0-SOURCE-B = BLOCKED — CORPUS LOCAL NON ACCESSIBLE DANS L'ENVIRONNEMENT D'EXÉCUTION COURANT.**

Le blocage est d'accès, non de données. Les chiffres antérieurement évoqués pour ce corpus restent NON VÉRIFIÉS aujourd'hui.

E1, backtest confirmatoire, développement Momentum, paper/broker/live, capital réel et contact Dukascopy restent fermés.

## Prochaine action gouvernée unique

**E0-SOURCE-B-ACCESS** — rendre le chemin exact ou une copie read-only fidèle du corpus déjà existant accessible à la session ; à défaut fournir un manifest exact permettant ensuite l'accès aux octets. Puis fresh HEAD et reprise du même préflight/budget, sans l'élargir silencieusement.

STOP.
