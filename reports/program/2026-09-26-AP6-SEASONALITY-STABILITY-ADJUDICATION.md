# AP6 — Seasonality / Stability — adjudication

Date : 2026-09-26  
Branch : `integration/system-v1`  
Fresh HEAD avant persistance : `7d7678780ff2f3818010ff7d77b6e08dce776797`.

## Evidence exacte reçue

Fichier local/handoff :
`ATDS-AP6-SEASONALITY-STABILITY.json`

- taille : **273 269 octets**
- SHA-256 : `f2cfa2c8c43f70519904c375452027f79415890be20a61c4c0452c06127e17fd`
- schema : `ATDS_AP6_SEASONALITY_STABILITY_V0_1`
- status : `AP6_COMPLETE`

Le fichier joint a été lu directement depuis son sandbox path, rehashé et parsé. Le hash et la taille correspondent exactement au terminal local.

Le pont Files de cette session n'a pas exposé la pièce jointe pour une ingestion brute vers GitHub. Un seal durable des métriques et de l'identité exacte est donc persisté à :
`reports/program/evidence/2026-09-26-AP6-SEASONALITY-STABILITY-SEAL.json`.

Cette limitation est d'archivage ; elle ne change pas les contrôles numériques exécutés sur les octets exacts reçus.

## Provenance R4-like AP6

Avant exécution :
- governed remote HEAD = `7d7678780ff2f3818010ff7d77b6e08dce776797`
- helper exact SHA-256 `e5463af97783e193f54e1ef25d96626c6a9a511e7236469054b69a788f6dfc6c`
- AP3/AP4/AP5 exacts matérialisés depuis raw Git blobs
- CRLF = 0
- helper py_compile PASS
- AP6 helper persisted-HEAD : 19/19 synthetic PASS, 18/18 mutants killed
- AP6_COMPLETE / exit code 0

## Coverage / bindings

PASS :
- 61 AP0 files rehashed
- 1 709 180 minutes
- 376 003 618 source ticks
- 1 606 segments
- AP0/AP2/AP3/AP4/AP5 bindings exacts

## Réconciliations globales

Toutes exactes :
- minute range mean = 4.033115022615127
- abs 1m log-return mean = 2.130371613870453
- RV15 mean = 10.478525943077567
- RV60 mean = 21.63083566473441
- efficiency15 mean = 0.25740927472902353
- efficiency60 mean = 0.13080767215518072
- directional persistence = 0.4933796682202942
- spread tick-weighted mean = 2.1395040593705206
- tick density mean = 219.99064931721645

## Conservation temporelle

Pour NY hour, NY weekday, NY month, UTC year et UTC quarter :
- minute counts reconservent 1 709 180
- source ticks reconservent 376 003 618
- chaque count valide de métrique est reconservé

## Résultats de stabilité qualifiés

### 1. Volatilité / activité : forme stable, amplitude variable

Sur les années complètes 2022–2025 :
- range mean CV = 0.27341767729335076
- RV15 mean CV = 0.27134198978031876
- RV60 mean CV = 0.2724738996000803
- tick-count mean CV = 0.27879057812587826

Les distributions absolues changent donc matériellement entre années.

Mais le classement horaire NY est fortement conservé :
- range min pairwise Spearman = 0.967391304347826
- RV15 = 0.9634387351778656
- RV60 = 0.9649915302089215
- tick density = 0.9812252964426877

La forme intraday est donc beaucoup plus persistante que son amplitude absolue.

### 2. Weekday vs month

Weekday volatility/range/tick :
- minimum pairwise Spearman = 0.9428571428571428

Month :
- range min Spearman = -0.6503496503496503
- RV15 = -0.6643356643356644
- RV60 = -0.6713286713286714
- tick density = -0.6293706293706294

Aucune saisonnalité mensuelle stable n'est promue.

### 3. Efficiency

Les distributions efficiency sont comparativement stables :
- efficiency15 mean CV = 0.008681687430761328
- max complete-year CDF distance = 0.007968981430839406
- efficiency60 mean CV = 0.011057265350893943
- max complete-year CDF distance = 0.010976486139100905

Les profils hour/month/weekday d'efficiency sont en revanche moins persistants en rang ; seul le niveau de distribution est qualifié comme relativement stable.

### 4. Direction minute

Persistence globale = 0.4933796682202942.

Années complètes :
- 2022 = 0.49452891898935064
- 2023 = 0.4910111896105733
- 2024 = 0.4940297763986439
- 2025 = 0.49496903113371954

La métrique reste proche de 0.5 ; aucune persistance directionnelle dominante ni edge n'est inféré.

### 5. Spread

Le profil horaire du spread conserve un rang notable :
- NY-hour min Spearman = 0.775691699604743

Mais la distribution de spread dérive fortement :
- complete-year CDF distance 2022 = 0.2822877149123234
- 2023 = 0.2133650106971534
- 2024 = 0.3537806014928728
- 2025 = 0.2312275743840782

Les très fortes distances observées fin 2025 / 2026 restent un constat de dataset/provider. Aucune cause n'est inférée.

## Non-promotions

AP6 V0.1 ne qualifie pas comme stable :
- AP4 breakout/reentry future-label findings
- month seasonality
- source volume / depth / order flow
- microstructure sub-minute
- causalité
- edge
- signal
- stratégie

## Verdict

**PASS — AP6 SEASONALITY / STABILITY.**

Le PASS qualifie la mesure de stabilité ; il ne signifie pas que toutes les propriétés sont stables.

La construction du **ASSET BEHAVIORAL PROFILE CORE V0.1** est autorisée.
