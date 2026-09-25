# AP1 — INTRADAY + SPREAD CENSUS — preflight

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `2781e334bc92d67aa381690e37435326cb0c8e0e`

## 1. Entrée

DatasetIdentity :
`USTECH_PROFILE_MINUTE_CORE_V0_1`.

Manifest AP0 exact :
- SHA-256 :
  `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`;
- 61 Parquet mensuels ;
- 1 709 180 minutes observées ;
- 376 003 618 ticks source ;
- 1 606 segments ;
- 91 734 766 octets output.

Chaque Parquet AP0 doit être re-hashé contre le manifest avant lecture AP1.

## 2. Objet

AP1 produit une cartographie descriptive de :
- activité tick ;
- range intraminute ;
- spread ;
- saisonnalité intraday de premier niveau.

Il ne mesure pas :
- rendement ;
- direction future ;
- autocorrélation ;
- edge ;
- stratégie ;
- PnL.

## 3. Colonnes AP0 lues

- `minute_start_ms_utc`;
- `tick_count`;
- `segment_id`;
- `segment_start`;
- `mid_high`;
- `mid_low`;
- `spread_mean`;
- `spread_min`;
- `spread_max`.

Aucun champ source volume.

## 4. Métriques

Par minute :
- `minute_range = mid_high - mid_low`.

Pour chaque bucket :
- minute_count ;
- source_tick_count ;
- tick_count mean / p50 / p90 / p99 ;
- minute_range mean / p50 / p90 / p95 / p99 ;
- spread tick-weighted mean :
  `sum(spread_mean * tick_count) / sum(tick_count)`;
- distribution de `spread_mean` :
  p50 / p90 / p95 / p99 ;
- spread_max_observed ;
- segment_start_count.

Les percentiles sont descriptifs, non optimisés.

## 5. Dimensions

Census exact :
1. GLOBAL ;
2. UTC_HOUR — 24 buckets ;
3. NEW_YORK_HOUR — 24 buckets ;
4. NEW_YORK_WEEKDAY — 7 buckets ;
5. NEW_YORK_WEEKDAY_HOUR — 168 buckets ;
6. YEAR — 2021..2026.

Timezone :
`America/New_York`,
dérivée depuis UTC avec gestion DST.

Aucune timezone Europe/Paris.

## 6. Stabilité minimale

AP1 n'est pas AP6, mais doit fournir assez de séparation temporelle pour éviter une moyenne unique trompeuse.

Le bloc YEAR est donc obligatoire.

Aucune conclusion de stabilité forte n'est autorisée par AP1 seul.

## 7. Contrôles d'intégrité

Avant calcul :
- manifest AP0 exact par SHA-256 ;
- 61 chemins exacts ;
- chaque Parquet existe ;
- chaque taille correspond ;
- chaque SHA-256 correspond ;
- somme rows = 1 709 180 ;
- somme source_ticks = 376 003 618.

Pendant lecture :
- row counts = manifest ;
- schema attendu AP0 ;
- minute_start strictement croissant globalement ;
- tick_count >0 ;
- mid_high >= mid_low ;
- spread_min >0 ;
- spread_min <= spread_mean <= spread_max ;
- segment_id non décroissant ;
- segment_start total = 1 606.

## 8. Ressources

Input :
~91,7 MiB Parquet AP0.

Lecture/re-hash intégral des 61 outputs :
autorisé.

Mémoire maximale cible :
**< 1 GiB**.

AP1 peut concaténer uniquement les colonnes requises des 1 709 180 minutes.

Output :
un JSON descriptif ;
cap **32 MiB**.

## 9. Interdictions

- aucun future label ;
- aucun return ;
- aucun signal ;
- aucun seuil choisi par performance ;
- aucun trade/PnL ;
- aucune recommandation de stratégie ;
- aucun volume source ;
- aucune interpolation.

## 10. Verdict

**PASS — preflight AP1 autorise la matérialisation du helper descriptif.**
