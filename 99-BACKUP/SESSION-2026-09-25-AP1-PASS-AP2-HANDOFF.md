# Sauvegarde — AP1 exact PASS, AP2 handoff

Date : 2026-09-25

## AP1
SHA-256 :
`db8963bb1bd1fa5b76a9a435fcb9b2d24781f92df0c5e53b6664bafe6235076b`.

PASS :
- 1 709 180 minutes ;
- 376 003 618 ticks ;
- 1 606 segment starts ;
- spread reconcilé avec F2 ;
- aucune stratégie/return/signal/PnL.

## AP2
Helper :
`tools/ap2_volatility_map.py`

Blob :
`0dd8df0294f9ec459c74da571b80c27b7134c612`.

Purpose :
gap-aware descriptive volatility map.

Metrics :
- minute range bps ;
- abs log return 1/5/15/60m ;
- realized vol 5/15/60m.

Windows :
same segment + exact minute continuity only.

Next :
run AP2 locally and upload exact JSON.

Checkpoint active : §211.
