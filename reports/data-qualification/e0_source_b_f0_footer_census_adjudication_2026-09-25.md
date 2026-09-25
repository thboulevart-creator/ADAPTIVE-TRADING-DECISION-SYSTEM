# E0-SOURCE-B-F0 — adjudication du JSON footer census exact

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `9ad2e6543fbb7009df054a58d2e5d82b4b3348d6`

## 1. Preuve exacte ingérée

Fichier F0 joint à la session :
- taille : **84 426 octets** ;
- SHA-256 : `5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b` ;
- schéma : `ATDS_E0_SOURCE_B_F0_FOOTER_CENSUS_V0_1` ;
- statut : `F0_COMPLETE`.

Binding :
- manifest SHA-256 : `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5` ;
- inventory digest corrigé : `5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf` ;
- expected files : 212 ;
- expected bytes : 3 936 721 231.

## 2. Cohérence structurelle intégrale

Le JSON exact a été parsé intégralement.

Recalculs :
- `files[]` : **212** ;
- chemins relatifs uniques : **212/212** ;
- somme `size_bytes` : **3 936 721 231** ;
- somme `num_rows` : **376 003 618** ;
- somme `num_row_groups` : **488** ;
- somme `footer_envelope_bytes` : **448 636** ;
- signatures de schéma distinctes : **1**.

La signature unique :
`c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d`
est portée par les **212/212 fichiers**.

## 3. Budget F0

- initial tail probe : **1 696 octets** ;
- footer envelopes : **448 636 octets** ;
- cumul logique planifié : **450 332 octets** ;
- plafond metadata : **134 217 728 octets** ;
- `within_128_mib_budget=true`.

Le helper déclare explicitement :
- `metadata_api_only=true` ;
- `column_data_scan=false` ;
- `corpus_writes=0` ;
- `strategy_calculation=false` ;
- `signal_calculation=false` ;
- `trade_or_pnl_calculation=false` ;
- `provider_network=false` ;
- `physical_os_read_bytes_measured=false`.

## 4. Schéma unique Source-B

PyArrow version : `25.0.1`.

Champs Arrow :
1. `timestamp` — `timestamp[ms]` — nullable ;
2. `bid_price` — `double` — nullable ;
3. `ask_price` — `double` — nullable ;
4. `bid_volume` — `double` — nullable ;
5. `ask_volume` — `double` — nullable.

Schéma Parquet du timestamp :
- physical type : `INT64` ;
- logical type :
  `Timestamp(isAdjustedToUTC=false, timeUnit=milliseconds, ...)`.

Aucune metadata Arrow de schéma n'est présente.

Conséquence :
- le corpus possède bien bid et ask au niveau schéma ;
- il n'existe pas de colonne `spread` explicite ;
- le spread pourra éventuellement être dérivé plus tard comme `ask_price - bid_price`, mais **aucun calcul prix n'est autorisé par F0/F1** ;
- `timestamp[ms]` est présent, mais `isAdjustedToUTC=false` ne permet pas de qualifier son fuseau réel. Le timezone reste **UNRESOLVED**.

## 5. Métadonnées temporelles

Candidat temporel unique : `timestamp`.

Sur les **488 row groups** :
- avec statistiques min/max : **488** ;
- sans statistiques min/max : **0**.

Bornes globales issues uniquement des metadata footer :
- min : `2021-05-25T00:00:00.309000` ;
- max : `2026-05-24T23:59:59.963000`.

Cela confirme une profondeur metadata-first d'environ cinq ans, cohérente avec les partitions nominales, mais ne prouve pas :
- l'ordre de tous les ticks ;
- l'absence de timestamps nuls ;
- l'absence de retours temporels ;
- l'absence de trous intrarow-group ;
- la nature normale/anormale des gaps ;
- le fuseau réel ;
- les sessions de marché.

## 6. Décision F1

Les footers suffisent pour :
- le schéma ;
- les row counts/groups ;
- les champs présents ;
- les bornes temporelles metadata ;
- la disponibilité complète de statistiques min/max par row group.

Ils ne suffisent **pas** pour la continuité tick-level.

**F1 EST NÉCESSAIRE.**

Portée F1 autorisable sous le préflight E0 existant :
- lire uniquement `timestamp` ;
- aucun `bid_price`, `ask_price`, volume ou autre colonne ;
- aucun calcul de stratégie, retour, trade ou PnL ;
- traiter un row group à la fois ;
- mesurer nulls, ordre, égalités adjacentes, retours temporels et gaps bruts ;
- ne pas qualifier un gap de défaut de marché avant contextualisation session/calendrier.

Budget logique minimal :
- 376 003 618 timestamps × 8 octets = **3 008 028 944 octets** décodés au maximum hors null bitmap/overhead ;
- ajouté au hashing initial 3 936 721 231 octets et au metadata F0, la route reste sous le plafond préenregistré de **16 GiB**.

## Verdict

**PASS — E0-SOURCE-B-F0 qualifié pour sa portée footer/metadata.**

**TO-PROVE : continuité tick-level et sémantique timezone/session.**

## Prochaine action gouvernée

Matérialiser, casser, corriger et re-breaker un helper **E0-SOURCE-B-F1** qui lit uniquement la colonne `timestamp`, puis l'exécuter localement.

Aucun prix, signal, stratégie, backtest, E1, MT5, paper/broker/live.
