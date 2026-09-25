# AP5 — MICROSTRUCTURE PRICE-CORE — preflight V0.1

Date : 2026-09-25  
Fresh HEAD : `563adffe7f2452ff2897aea2c663b343c36068d2`.  
Parent : `docs/02.1-ASSET-BEHAVIORAL-PROFILE-CORE-PROTOCOL.md`, §7 AP5.  
AP4 exact PASS au checkpoint §216.

## 1. Objet

Qualifier descriptivement, sans stratégie :

- spread moyen / médian / percentiles ;
- spread par heure et fenêtre de session horloge ;
- spread extrême ;
- relation spread ↔ volatilité ;
- densité de ticks.

AP5 V0.1 opère sur la DatasetIdentity canonique minute :

`USTECH_PROFILE_MINUTE_CORE_V0_1`.

Il ne prétend pas qualifier toute microstructure sub-minute. Le protocole CORE indique explicitement que la transformation minute ne remplace pas les ticks pour les questions exigeant une résolution sub-minute.

## 2. Entrées et bindings

AP0 manifest exact :
`62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`.

AP4 evidence exacte :
`reports/program/evidence/2026-09-25-AP4-PRICE-STRUCTURE.json`
SHA-256 :
`c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`.

Couverture attendue :
- 61 Parquet ;
- 1 709 180 minutes ;
- 376 003 618 ticks source agrégés ;
- 1 606 segments ;
- 91 734 766 octets AP0.

Réconciliations obligatoires :
- spread min F2 : 0.000999999996565748 ;
- spread max F2 : 35.66699999999764 ;
- spread moyen tick-weighted F2/AP1 : 2.1395040593705223, tolérance 1e-9 ;
- minute_range_bps mean AP2 : 4.033115022615127, tolérance 1e-9 ;
- valid abs return 1m AP2 : 1 707 574 ;
- abs return 1m mean AP2 : 2.130371613870453 bps, tolérance 1e-9.

## 3. Colonnes autorisées

AP0 uniquement :
- minute_start_ms_utc ;
- tick_count ;
- segment_id ;
- segment_start ;
- mid_open ;
- mid_high ;
- mid_low ;
- mid_close ;
- spread_mean ;
- spread_min ;
- spread_max.

Aucun champ volume source.

`mid` reste descriptif uniquement et n'est jamais un prix d'exécution.

## 4. Mesures pré-enregistrées

### 4.1 Spread minute

Base :
`spread_mean` par minute.

Global :
- tick-weighted mean :
  `sum(spread_mean * tick_count) / sum(tick_count)` ;
- simple mean minute ;
- p10 / p25 / p50 / p75 / p90 / p95 / p99 / p99.9 ;
- min observé via `spread_min` ;
- max observé via `spread_max`.

Distribution de `spread_max` minute :
p50 / p90 / p95 / p99 / p99.9 / max.

Les percentiles sont `numpy.percentile(..., method="linear")`.

### 4.2 Tick density

Par minute :
`tick_count`.

Global :
- mean ;
- p10 / p25 / p50 / p75 / p90 / p95 / p99 / p99.9 ;
- max.

Aucun volume de transaction n'est inféré depuis `tick_count`.

### 4.3 Temps / session

Timezone intraday :
`America/New_York`, dérivée depuis UTC avec DST.

Buckets :
1. 24 heures New York ;
2. proxy de fenêtre cash horloge :
   - `NY_WEEKDAY_CASH_CLOCK_0930_1600` : lundi-vendredi, 09:30 <= heure locale < 16:00 ;
   - `NY_WEEKDAY_OUTSIDE_CASH_CLOCK` ;
   - `NY_WEEKEND`.

Ce proxy est une partition d'horloge descriptive. Il ne certifie ni calendrier officiel, ni holiday, ni ouverture réelle d'un marché sous-jacent.

Chaque bucket produit :
- minute_count ;
- source_tick_count ;
- tick_count distribution ;
- spread tick-weighted mean ;
- spread_mean p50/p90/p95/p99 ;
- spread_max_observed.

### 4.4 Relation spread ↔ volatilité

Volatilité minute descriptive :
`minute_range_bps = (mid_high-mid_low)/mid_open*10000`.

Retour 1m descriptif :
`abs(log(close_t/close_{t-1}))*10000`,
uniquement même segment et minute exactement contiguë.

Mesurer :
- Pearson(spread_mean, minute_range_bps) ;
- Pearson(spread_mean, abs_return_1m_bps) sur lignes valides ;
- Pearson(spread_mean, tick_count).

Aucune causalité n'est attribuée.

### 4.5 Quintiles descriptifs

Sur `minute_range_bps`, seuils full-sample :
p20 / p40 / p60 / p80.

Affectation déterministe :
`searchsorted(thresholds, value, side="right")`.

Pour chaque quintile :
- minute_count ;
- source_tick_count ;
- tick-weighted spread mean ;
- spread_mean p50/p90/p99 ;
- tick_count p50/p90/p99 ;
- minute_range_bps mean/p50/p90.

Les seuils full-sample impliquent :
`causal_deployable=false`.

Même logique descriptive séparée pour les quintiles de `tick_count`, afin d'observer spread ↔ densité.

### 4.6 Années

UTC years 2021..2026 :
- 2021 et 2026 marqués partial ;
- même résumé spread/tick density.

AP6 reste l'unique bloc de qualification complète de stabilité.

## 5. Intégrité

Avant calcul :
- manifest AP0 exact par SHA-256 ;
- 61 chemins exacts ;
- chaque fichier existe, taille + SHA exacts ;
- schéma AP0 exact ;
- metadata DatasetIdentity exacte ;
- `volumes_used=false` ;
- `mid_semantics=descriptive_only_not_execution_price`.

Pendant lecture :
- minute strictement croissante ;
- tick_count >0 ;
- segment_id non décroissant et incrément <=1 ;
- segment_start cohérent ;
- OHLC fini/positif/cohérent ;
- spread fini ;
- spread_min >0 ;
- spread_min <= spread_mean <= spread_max.

Après calcul :
- rows = 1 709 180 ;
- source ticks = 376 003 618 ;
- segment starts = 1 606 ;
- toutes partitions conservent les minutes ;
- quintiles conservent les minutes ;
- réconciliations F2/AP1/AP2 obligatoires avant `AP5_COMPLETE`.

## 6. Ressources

Input AP0 : ~91,7 MiB.

Mémoire cible :
**< 1 GiB**.

Le helper peut concaténer uniquement les colonnes requises des 1 709 180 minutes.

Output :
un JSON agrégé, cap 32 MiB.

Aucun rescan des 212 Parquet Source-B n'est requis par AP5 V0.1.

## 7. Interdictions

- aucun volume source ;
- aucune profondeur carnet ;
- aucune reconstruction order flow ;
- aucune microstructure sub-minute déclarée qualifiée ;
- aucun signal ;
- aucun trade ;
- aucun PnL ;
- aucune stratégie ;
- aucun sweep orienté performance ;
- aucun MT5 ;
- aucune causalité déduite d'une corrélation.

## 8. Tests adversariaux pré-enregistrés

- weighted spread mean distinct du simple mean ;
- gap/segment coupe le retour 1m ;
- formule range en bps réconcilie AP2 ;
- DST New York dérivé depuis UTC ;
- frontières 09:30 incluses / 16:00 exclues ;
- weekend séparé ;
- quintile `side="right"` testé sur égalités ;
- conservation des quintiles ;
- Pearson testé sur oracle simple et cas variance nulle ;
- faux manifest/hash/identity rejetés ;
- spread invariant cassé rejeté ;
- tick_count <=0 rejeté ;
- output existant ou situé dans l'input refusé ;
- aucune colonne volume demandée ;
- mutants : moyenne non pondérée, gap traversé, denominator range incorrect, frontière session 16:00 incluse, quintile side="left".

Audit par le même assistant ; aucune indépendance revendiquée. Tout FAIL doit être corrigé puis re-break.

## 9. Verdict preflight

**PASS — AP5 V0.1 est suffisamment borné pour matérialiser un helper candidat.**

AP5 corpus reste **BLOCKED** jusqu'au helper testé, re-break PASS, puis exécution locale et ingestion du JSON exact.
