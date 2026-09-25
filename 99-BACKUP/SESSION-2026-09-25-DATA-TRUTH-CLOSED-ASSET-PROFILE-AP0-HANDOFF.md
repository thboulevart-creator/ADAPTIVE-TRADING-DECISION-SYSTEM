# Sauvegarde — DATA TRUTH closed, Asset Behavioral Profile AP0 handoff

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## DATA TRUTH

`SOURCE_B_USTECH_PRICE_CORE_V0_1` :
**PASS** pour :
- timestamp ;
- bid_price ;
- ask_price.

Série :
**DISCONTINUE**.

Volumes :
NON QUALIFIÉS / NON AUTORISÉS.

F2 exact :
SHA-256 `6484784faf7c77d1ba8b6d7f007ee8498ad085c4beef58a21be71898e767cb29`.

## ASSET BEHAVIORAL PROFILE CORE

Protocole strategy-agnostic : PASS.

Objectif :
comprendre l'actif avant toute recherche d'edge.

## AP0

Output identity :
`USTECH_PROFILE_MINUTE_CORE_V0_1`.

Helper :
`tools/ap0_ustech_profile_minute_core.py`
blob `42fcb38809a1cc0365cd4027fae5154e1d6d3b4f`.

Expected:
- 376 003 618 source ticks ;
- 1 605 gaps >60s ;
- 1 606 segments ;
- 61 monthly Parquet files ;
- no fill ;
- no volume ;
- no return/strategy/PnL.

Recommended local output:
`%USERPROFILE%\Documents\ATDS-DERIVED\USTECH_PROFILE_MINUTE_CORE_V0_1`.

Next:
run AP0 and upload AP0-MANIFEST.json.

Checkpoint active: §209.
