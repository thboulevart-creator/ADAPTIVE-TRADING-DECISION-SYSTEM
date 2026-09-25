# Sauvegarde — AP2 exact PASS, AP3 handoff

Date : 2026-09-25

## AP2
SHA-256 :
`4e3c79a5b9c8131f62a8fb7f205712d8a5c4301ff01b7fd3ce7226d8799d9c9f`.

PASS :
- 1 709 180 minutes ;
- 1 606 segments ;
- abs returns 1/5/15/60m gap-aware ;
- RV5/RV15/RV60 gap-aware ;
- no strategy/signal/PnL.

## AP3
Helper :
`tools/ap3_expansion_compression.py`

Blob :
`8a7aa643eb6e4414dad378ca4ddb8b98adce7bd1`.

Purpose :
descriptive expansion/compression census with:
- absolute RV15 p20/p80 ;
- intraday-normalized RV15 p20/p80 ;
- phase durations ;
- adjacent transitions ;
- variance share RV15^2/RV60^2.

Full-sample thresholds:
`causal_deployable=false`.

Next :
run AP3 locally and upload exact JSON.

Checkpoint active : §212.
