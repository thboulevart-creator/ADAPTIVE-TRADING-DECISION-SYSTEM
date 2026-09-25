# AP0 — USTECH_PROFILE_MINUTE_CORE_V0_1 — adjudication du manifest exact

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `313afa6ac54b8a0bc37a3f9da88c7bbe06fb523d`

## 1. Preuve exacte ingérée

Manifest AP0 joint à la session :
- taille : **26 900 octets** ;
- SHA-256 exact : `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce` ;
- schema : `ATDS_AP0_USTECH_PROFILE_MINUTE_CORE_MANIFEST_V0_1` ;
- status : `AP0_COMPLETE` ;
- output identity : `USTECH_PROFILE_MINUTE_CORE_V0_1` ;
- source identity : `SOURCE_B_USTECH_PRICE_CORE_V0_1`.

Bindings confirmés :
- manifest source SHA-256 :
  `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5` ;
- F0 :
  `5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b` ;
- F1 :
  `2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067` ;
- F2 :
  `6484784faf7c77d1ba8b6d7f007ee8498ad085c4beef58a21be71898e767cb29` ;
- inventory digest :
  `5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf` ;
- schema signature :
  `c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d`.

## 2. Couverture

Le manifest déclare et l'adjudication confirme :
- source ticks lus : **376 003 618** ;
- minute rows écrites : **1 709 180** ;
- gaps >60 s : **1 605** ;
- segments : **1 606** ;
- segment-start rows : **1 606** ;
- fichiers mensuels : **61** ;
- output bytes : **91 734 766** ;
- premier tick source :
  `2021-05-25T00:00:00.309+00:00` ;
- dernier tick source :
  `2026-05-24T23:59:59.963+00:00`.

## 3. Recalcul des 61 entrées

Recalcul depuis `files[]` :
- nombre d'entrées : **61** ;
- chemins uniques : **61/61** ;
- SHA-256 déclarés uniques : **61/61** ;
- chaque SHA-256 = 64 hex lowercase valide ;
- somme rows = **1 709 180** ;
- somme source_ticks = **376 003 618** ;
- somme size_bytes = **91 734 766**.

Les trois sommes correspondent exactement au bloc `coverage`.

## 4. Couverture mensuelle exacte

Les chemins sont exactement la séquence :
`2021-05 → 2026-05`,
sans mois absent ni mois dupliqué.

Premier fichier :
`year=2021/month=05/USTECH-PROFILE-M1-2021-05.parquet`.

Dernier fichier :
`year=2026/month=05/USTECH-PROFILE-M1-2026-05.parquet`.

Segment IDs :
- premier : 0 ;
- dernier : 1605 ;
- frontières inter-fichiers non décroissantes et compatibles avec la continuité des segments.

## 5. Contrat de transformation

Le manifest exact confirme :
- `forward_fill=false` ;
- gap threshold strictement >60 000 ms ;
- `mid=(bid+ask)/2` ;
- `mid_is_execution_price=false` ;
- minute = `floor(timestamp_ms/60000)` ;
- spread = `ask-bid` ;
- spread mean = **tick-weighted** ;
- aucun volume utilisé ;
- aucun return ;
- aucune stratégie ;
- aucun PnL.

## 6. Budget et runtime

Budget :
- lecture logique planifiée :
  **9 024 086 832 octets** ;
- plafond :
  **12 884 901 888 octets (12 GiB)** ;
- output cap :
  **4 294 967 296 octets** ;
- max output files :
  100 ;
- physical OS read bytes non mesurés.

Runtime :
- NumPy 2.5.3 ;
- PyArrow 25.0.1.

## 7. Limite d'adjudication

Les 61 Parquet dérivés n'ont pas été transférés dans cette session.

L'adjudication indépendante porte donc sur :
- le manifest exact ;
- ses agrégats ;
- ses 61 hashes déclarés ;
- la cohérence interne ;
- le contrat du helper qui a self-vérifié chaque output avant `AP0_COMPLETE`.

Elle ne constitue pas un second re-hash externe des 91,7 MiB de Parquet dérivés.

## Verdict

**PASS — AP0 `USTECH_PROFILE_MINUTE_CORE_V0_1` admissible comme DatasetIdentity dérivée canonique.**

Ce PASS autorise :
- AP1 Intraday / Spread Census ;
- analyses descriptives strategy-agnostic ;
- lecture des champs AP0 uniquement.

Il n'autorise toujours pas :
- stratégie ;
- PnL ;
- E1 ;
- backtest ;
- MT5 ;
- volumes source.

## Prochaine action

Ouvrir AP1 :
**INTRADAY + SPREAD CENSUS**, strictement descriptif et gap-aware.
