# Sauvegarde — AP0 exact PASS, AP1 handoff

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## AP0

Manifest SHA-256 :
`62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`.

PASS :
- 61 monthly Parquet ;
- 1 709 180 minutes ;
- 376 003 618 source ticks ;
- 1 605 gaps ;
- 1 606 segments ;
- 91 734 766 output bytes.

DatasetIdentity :
`USTECH_PROFILE_MINUTE_CORE_V0_1`.

## AP1

Helper :
`tools/ap1_intraday_spread_census.py`

Blob :
`9f613063fb8a190a1ff6f2f8b12c97c4ed97712a`.

Purpose :
strategy-agnostic intraday activity/range/spread census.

Mandatory:
- re-hash 61 AP0 files ;
- conserve 1 709 180 minutes / 376 003 618 ticks ;
- reconcile F2 spread min/max/mean ;
- no returns/signals/PnL/volume source.

Next:
run AP1 locally and upload exact AP1 JSON.

Checkpoint active: §210.
