# Sauvegarde — F0 exact adjugé, F1 timestamp-only handoff

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## F0 exact

JSON F0 :
- SHA-256 : `5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b` ;
- taille : 84 426 octets ;
- status : `F0_COMPLETE`.

Résultats qualifiés :
- 212 fichiers ;
- 3 936 721 231 octets ;
- 376 003 618 lignes ;
- 488 row groups ;
- 1 schéma unique ;
- timestamp + bid/ask prix/volumes ;
- timestamp physique INT64, logique timestamp[ms], `isAdjustedToUTC=false` ;
- 488/488 row groups avec stats temporelles ;
- min metadata : 2021-05-25T00:00:00.309000 ;
- max metadata : 2026-05-24T23:59:59.963000.

Verdict :
**PASS F0 — footer/metadata uniquement.**

Timezone/session/continuité tick-level restent non qualifiés.

## F1

F1 est nécessaire car les footers ne prouvent pas l'ordre et les gaps internes.

Helper :
`tools/e0_source_b_timestamp_continuity_scan.py`
blob :
`dbcf05f8701bd434e75a08beeddce8fde08a8266`.

Revue :
`reports/data-qualification/e0_source_b_f1_timestamp_scan_adversarial_review_2026-09-25.md`
blob :
`a52c1982941205279e7c834fd44a45cffb0ad90d`.

Portée stricte :
- timestamp uniquement ;
- aucun prix/volume ;
- streaming row group ;
- aucun signal, retour, trade, PnL ;
- raw null/equal/backward/gap inventory ;
- aucune interprétation timezone/session/gap anormal.

Budget logique cumulé planifié :
6 945 200 507 octets < 16 GiB.

## Prochaine action unique

Exécuter F1 localement avec :
- manifest exact ;
- F0 exact ;
- corpus Source-B.

Si `F1_COMPLETE`, joindre :
`%TEMP%\ATDS-E0-SOURCE-B-F1-TIMESTAMP-SCAN.json`.

Si `BLOCKED_*`, joindre le même JSON sans contourner.

Checkpoint actif : §202.

Aucun E1/backtest/MT5/paper/broker/live.
