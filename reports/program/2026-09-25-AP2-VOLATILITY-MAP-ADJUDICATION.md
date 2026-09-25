# AP2 — VOLATILITY MAP — adjudication du JSON exact

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `48357e048073b2499c25fba5013342cd3d9faa6c`

## 1. Preuve exacte ingérée

JSON AP2 joint à la session :
- taille : **85 770 octets** ;
- SHA-256 exact :
  `4e3c79a5b9c8131f62a8fb7f205712d8a5c4301ff01b7fd3ce7226d8799d9c9f` ;
- schema :
  `ATDS_AP2_VOLATILITY_MAP_V0_1` ;
- status :
  `AP2_COMPLETE` ;
- input :
  `USTECH_PROFILE_MINUTE_CORE_V0_1`.

Bindings :
- AP0 manifest SHA-256 :
  `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce` ;
- AP1 SHA-256 :
  `db8963bb1bd1fa5b76a9a435fcb9b2d24781f92df0c5e53b6664bafe6235076b` ;
- AP0 files rehashed : **61**.

## 2. Couverture

- minute rows : **1 709 180** ;
- segments : **1 606** ;
- first minute : `1621900800000` ;
- last minute : `1779667140000`.

Fenêtres valides :
- abs log return 1m : **1 707 574** ;
- 5m : **1 701 503** ;
- 15m : **1 686 423** ;
- 60m : **1 620 195** ;
- realized vol 5m : **1 701 503** ;
- 15m : **1 686 423** ;
- 60m : **1 620 195**.

Les counts RV H correspondent exactement aux counts abs-return H, conformément au contrat de continuité.

## 3. Conservation par dimensions

Dimensions :
- 24 New York hours ;
- 6 UTC years 2021..2026.

Recalcul :
- somme minute_count NY = **1 709 180** ;
- somme minute_count YEAR = **1 709 180** ;
- pour chacune des 8 métriques, la somme des counts des 24 heures NY = count GLOBAL ;
- pour chacune des 8 métriques, la somme des counts des 6 années = count GLOBAL.

Aucune observation valide n'est perdue entre GLOBAL et les dimensions.

## 4. Global

### Minute range normalisé

`minute_range_bps` :
- count = **1 709 180** ;
- mean = **4.033115022615127 bps** ;
- p50 = **2.767335232937379** ;
- p90 = **8.452819127290656** ;
- p95 = **11.454296534689933** ;
- p99 = **20.04541787089356** ;
- p99.9 = **37.78860508083989** ;
- max = **345.41732189903695**.

### Mouvement absolu close-to-close

1m :
- mean = **2.130371613870453 bps** ;
- p50 = **1.2042650753782058** ;
- p90 = **4.993458113429487** ;
- p99 = **13.830059560311309** ;
- p99.9 = **28.035463016686172** ;
- max = **350.0086720231564**.

5m :
- mean = **4.810221232143677 bps** ;
- p50 = **2.7099993833286558** ;
- p90 = **11.28655312864453** ;
- p99 = **31.328943055515843** ;
- max = **530.1642009448602**.

15m :
- mean = **8.4091464945747 bps** ;
- p50 = **4.782867989753365** ;
- p90 = **19.782370974830375** ;
- p99 = **54.08429520234808** ;
- max = **657.4668344763312**.

60m :
- mean = **17.14892473333806 bps** ;
- p50 = **9.91324631525939** ;
- p90 = **40.55240684473858** ;
- p99 = **107.38374287876555** ;
- max = **815.21874305732**.

### Realized volatility

5m :
- mean = **5.759246480746593 bps** ;
- p50 = **4.017018692233439** ;
- p90 = **11.973324399846604** ;
- p99 = **27.817552764782196** ;
- max = **352.08418375574**.

15m :
- mean = **10.478525943077567 bps** ;
- p50 = **7.617655651183205** ;
- p90 = **21.152386132760906** ;
- p99 = **46.061288822136234** ;
- max = **423.7015867665045**.

60m :
- mean = **21.63083566473441 bps** ;
- p50 = **16.196822486770692** ;
- p90 = **42.70878114042718** ;
- p95 = **55.075242344886554** ;
- p99 = **89.010616408331** ;
- p99.9 = **163.6268960212105** ;
- max = **479.92029054395715**.

## 5. Intégrité statistique

Recalcul interne :
- pour GLOBAL et tous les buckets non vides :
  `mean >=0` ;
- `p50 <= p90 <= p95 <= p99 <= p99.9 <= max` ;
- aucune métrique négative ;
- les buckets vides restent null/count=0.

## 6. Portée épistémique

Le JSON exact déclare :
- strategy_agnostic = true ;
- backward_looking_only = true ;
- future_labels = false ;
- signals_calculated = false ;
- pnl_calculated = false ;
- source_volume_used = false.

Contrat :
- fenêtre même segment ;
- continuité minute exacte ;
- aucune interpolation ;
- aucune optimisation.

## Verdict

**PASS — AP2 VOLATILITY MAP qualifié.**

Ce PASS autorise :
- observations descriptives de volatilité ;
- ouverture AP3 Expansion / Compression.

Il n'autorise pas :
- stratégie ;
- causalité ;
- edge ;
- PnL ;
- backtest ;
- MT5.
