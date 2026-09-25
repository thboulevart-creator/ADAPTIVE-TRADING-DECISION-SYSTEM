# E0-SOURCE-B — sidecar SHA-256 du bundle historique reçu

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `cc809f0063a8ac7a60886aa509f014b6425d93c9`

## Preuve reçue

Le fichier sidecar joint contient exactement :

```text
072f26bfacd51ba1501d3c9009d79c78436f360fc6eccd7143275db759f9d028  ATDS-SOURCE-B-GAP-FORENSICS-HISTORICAL.zip
```

Le SHA-256 du fichier sidecar lui-même dans la session est :

`e37f242814ff6aada0b09861910b0f5fa4f1afa591d2a1627fe0acd4e3fe6c6b`.

## Portée

Ce sidecar établit uniquement la valeur attendue du SHA-256 du ZIP :

`072f26bfacd51ba1501d3c9009d79c78436f360fc6eccd7143275db759f9d028`.

Le ZIP lui-même n'est pas encore joint à la session ; son contenu, son manifest interne et les 53 artefacts ne sont donc pas encore ingérés ni adjudicables.

## Prochaine action gouvernée unique

Joindre le fichier exact :

`ATDS-SOURCE-B-GAP-FORENSICS-HISTORICAL.zip`

Puis :
1. recalculer son SHA-256 et comparer au sidecar ;
2. vérifier le manifest interne ;
3. re-hasher les 53 entrées ;
4. parser les rapports historiques ;
5. reconstruire la chaîne de preuve gap/session/origin/source/loss/repairability.

Aucune nouvelle recherche calendrier/événement avant cette ingestion.
