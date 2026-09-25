# Sauvegarde — F1 exact PASS, bundle gap-forensics historique à récupérer

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## F1 exact

SHA-256 :
`2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067`.

PASS timestamp-only :
- 376 003 618 lignes ;
- 0 null ;
- 0 backward ;
- 0 equal-adjacent ;
- 1 605 gaps >60 s ;
- plus grand gap brut 265 872 098 ms ;
- aucune classification session/timezone appliquée.

## Gap-forensics historique local

Inventaire :
- 53 artefacts ;
- 28 reports ;
- 25 tools ;
- 5 774 487 octets ;
- CSV SHA-256 `a9a3fa3719c87a64526b1ef8f33e10611a11f1f752a4b06c562afd26a8ee8871`.

La chaîne de rapports historiques gap/session/timezone/provenance existe localement et doit être récupérée avant toute nouvelle recherche calendrier/événement.

## Bundler

`tools/e0_source_b_recover_gap_forensics_bundle.py`
blob :
`bcdd55c512257afa4e94feab869f7a986f8dc68c`.

Revue :
`reports/data-qualification/e0_source_b_gap_forensics_bundle_adversarial_review_2026-09-25.md`.

Le bundler :
- sélectionne exactement les 53 chemins ;
- n'accède pas à `data/` ;
- ne modifie pas les sources ;
- produit hors repo ;
- hash chaque source ;
- re-hash chaque entrée ZIP après création.

## Prochaine action unique

Exécuter le bundler localement et joindre :
`%TEMP%\ATDS-SOURCE-B-GAP-FORENSICS-HISTORICAL.zip`.

Puis adjudication/réutilisation des preuves historiques.

Checkpoint actif : §204.

Aucun E1/backtest/MT5/paper/broker/live.
