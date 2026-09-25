# AP2 — VOLATILITY MAP — revue adversariale du helper

Date : 2026-09-25

Candidat :
`tools/ap2_volatility_map.py`

Blob :
`0dd8df0294f9ec459c74da571b80c27b7134c612`.

## Attaques

### V1 — substitution des entrées
Le helper exige :
- AP0 manifest exact ;
- AP1 JSON exact ;
- 61 fichiers AP0 ;
- 1 709 180 minutes ;
- 376 003 618 ticks source ;
- 1 606 segments.

Chaque Parquet AP0 est re-hashé avant lecture.

**PASS.**

### V2 — colonnes non autorisées
Lecture uniquement :
- minute_start_ms_utc ;
- segment_id ;
- mid_open/high/low/close.

Aucun volume, aucun spread source, aucun tick brut.

**PASS.**

### V3 — mid utilisé comme prix d'exécution
Metadata AP0 obligatoire :
`mid_semantics=descriptive_only_not_execution_price`.

AP2 ne simule aucune exécution.

**PASS.**

### V4 — retour traversant un gap
Pour horizon H :
- même segment ;
- différence de timestamp exactement H minutes ;
- index t-H présent.

Donc une minute absente invalide la mesure.

**PASS.**

### V5 — realized volatility traversant une rupture
La RV H exige H transitions 1m toutes valides.
Le helper vérifie également même segment et différence exacte H minutes entre début/fin.

**PASS.**

### V6 — look-ahead
Toutes les métriques endpoint t utilisent uniquement :
t et observations antérieures.

Aucun label futur.

**PASS.**

### V7 — confusion direction/volatilité
AP2 conserve seulement :
- range normalisé ;
- valeur absolue des log returns ;
- realized volatility.

Aucune direction long/short.

**PASS.**

### V8 — OHLC invalide
Chaque Parquet :
- OHLC finite ;
- prix >0 ;
- low <= open/close <= high.

**PASS fail-closed.**

### V9 — ordre/segments
Minute timestamps strictement croissants.
Segment IDs non décroissants, saut max +1, frontière fichier contrôlée.

**PASS.**

### V10 — normalisation par niveau de prix
Minute range :
`(high-low)/open*10000`.

Log return :
`abs(log(close_t/close_t-H))*10000`.

**PASS.**

### V11 — fenêtres RV
RV H :
`sqrt(sum(r_1m^2))*10000`
sur exactement H transitions valides.

**PASS.**

### V12 — timezone
Bucket intraday endpoint :
UTC → America/New_York via zoneinfo.

Pas d'offset hardcodé.

**PASS.**

### V13 — années partielles
2021 et 2026 sont marquées `partial_period=true`.

**PASS.**

### V14 — percentiles
NumPy method = `linear`.
p50/p90/p95/p99/p99.9 + mean/max.

**PASS.**

### V15 — stratégie déguisée
Aucun signal, future label, PnL, Sharpe, Profit Factor, optimisation ou sélection d'horizon par performance.

**PASS.**

## Verdict

**PASS — helper AP2 suffisamment borné pour tentative locale.**

AP2 qualifie une carte descriptive de volatilité ; il ne valide aucun edge.

Prochaine frontière :
exécution locale AP2 et ingestion du JSON exact.
