# AP2 — VOLATILITY MAP — preflight

Date : 2026-09-25

## 1. Entrées

DatasetIdentity :
`USTECH_PROFILE_MINUTE_CORE_V0_1`.

Bindings exacts :
- AP0 manifest SHA-256 :
  `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`;
- AP1 JSON SHA-256 :
  `db8963bb1bd1fa5b76a9a435fcb9b2d24781f92df0c5e53b6664bafe6235076b`.

Attendus :
- 61 Parquet AP0 ;
- 1 709 180 minutes ;
- 1 606 segments ;
- 376 003 618 source ticks.

Chaque Parquet AP0 sera re-hashé contre le manifest avant lecture.

## 2. Objet

Construire une cartographie descriptive de la volatilité, sans recherche d'edge.

Mesures :
- range minute normalisé en bps ;
- mouvement absolu close-to-close en bps sur 1, 5, 15, 60 minutes ;
- volatilité réalisée en bps sur fenêtres de 5, 15, 60 minutes.

Aucun rendement futur n'est utilisé comme label.
Toutes les mesures à l'instant t utilisent uniquement des observations <= t.

## 3. Colonnes AP0

Lecture :
- minute_start_ms_utc ;
- segment_id ;
- mid_open ;
- mid_high ;
- mid_low ;
- mid_close.

Aucun volume.
Aucun spread n'est nécessaire pour AP2.

## 4. Définitions

Minute range bps :
`(mid_high - mid_low) / mid_open * 10000`.

Pour horizon H minutes :
`r_H(t) = log(mid_close_t / mid_close_{t-H}) * 10000`.

AP2 décrit principalement :
`abs(r_H)`.

Une observation H est valide uniquement si :
- l'index t-H existe ;
- `segment_id_t == segment_id_{t-H}` ;
- `minute_start_t - minute_start_{t-H} == H*60000`.

Donc aucune minute absente ni rupture >60s n'est traversée.

Volatilité réalisée H :
`sqrt(sum(r_1m^2 over the last H valid 1m transitions)) * 10000`.

Elle est valide uniquement si les H transitions 1m sont toutes valides.

## 5. Dimensions

1. GLOBAL ;
2. NEW_YORK_HOUR — bucket selon l'heure locale de l'endpoint t ;
3. UTC_YEAR — 2021..2026.

2021 et 2026 doivent rester marquées comme années partielles.

AP6 fera la stabilité temporelle plus complète ; AP2 ne conclut pas à la stabilité.

## 6. Statistiques

Pour chaque métrique :
- count ;
- mean ;
- p50 ;
- p90 ;
- p95 ;
- p99 ;
- p99.9 ;
- max.

Méthode percentile NumPy :
`linear`.

## 7. Intégrité

Avant calcul :
- AP0 manifest exact ;
- AP1 exact ;
- 61 fichiers exacts, tailles + SHA-256 ;
- schéma AP0 exact ;
- ordre minute strict ;
- segment_id non décroissant ;
- mid OHLC finite et positif ;
- low <= open/close <= high.

Pendant calcul :
- aucun log sur prix <=0 ;
- aucune fenêtre cross-segment ;
- aucune fenêtre traversant une minute manquante ;
- counts valides par horizon conservés ;
- aucune interpolation.

## 8. Ressources

Input AP0 :
~91.7 MiB.

Lecture de 6 colonnes sur 1.7M lignes.
Mémoire cible :
<1 GiB.

Output :
JSON <=32 MiB.

## 9. Interdictions

AP2 ne produit pas :
- signal ;
- sens long/short ;
- règle d'entrée/sortie ;
- PnL ;
- Sharpe ;
- Profit Factor ;
- optimisation de seuil ;
- sélection d'horizon par performance ;
- MT5/backtest.

## 10. Verdict

**PASS — preflight AP2 autorise la matérialisation du helper candidat.**
