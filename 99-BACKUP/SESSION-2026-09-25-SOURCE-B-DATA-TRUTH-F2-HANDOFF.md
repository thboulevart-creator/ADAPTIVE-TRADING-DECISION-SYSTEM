# Sauvegarde — Source-B Data Truth, F2 bid/ask handoff

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## État atteint

### Byte/schema/time
- 212 Parquet ;
- 3 936 721 231 octets ;
- 376 003 618 lignes ;
- 488 row groups ;
- schéma unique ;
- timestamp[ms], bid/ask prix et volumes ;
- F1 : 0 null timestamp, 0 backward, 0 equal-adjacent.

### Gaps
- 1 605 >60s ;
- session régulière réconciliée en raw GMT/UTC ;
- 1 290 frontières de session ;
- 315 gaps en session ouverte avant holiday overlay exhaustif ;
- 13 pertes d'acquisition historiques exactes ;
- 9 historiques inconnues ;
- série = DISCONTINUE ;
- usage futur obligatoirement gap-aware/par horodatage.

### Provenance
Public dataset :
`CarlosSilva1/ustech-ticks`.

Documented identity:
- USTECH / Nasdaq100 Index CFD ;
- timestamp UTC ;
- CC-BY-4.0 ;
- publisher provenance Dukascopy via Tickstory ;
- période et row count convergent avec le local.

Feed-value equivalence native Dukascopy : non certifiée.

### F2

Helper :
`tools/e0_source_b_bid_ask_quality_scan.py`.

Portée :
bid_price + ask_price uniquement.

Budget cumulé planifié :
12 961 258 395 octets <16 GiB.

Revue adversariale F2 : PASS pour tentative locale.

## Prochaine action

Exécuter F2 localement.
Joindre `%TEMP%\ATDS-E0-SOURCE-B-F2-BID-ASK-QUALITY.json`.

Puis adjudication F2 et synthèse de fermeture Data Truth.

Checkpoint actif : §207.

Aucun E1/backtest/MT5/paper/broker/live.
