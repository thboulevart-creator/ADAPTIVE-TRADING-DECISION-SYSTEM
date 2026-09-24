# Sauvegarde — E0-SOURCE-B manifest exact adjugé

Date : 2026-09-24
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`

## Preuve exacte ingérée

Manifest Source-B joint à la session :
- taille JSON : 86 752 octets ;
- SHA-256 exact : `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5` ;
- schéma : `ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1` ;
- statut : `MANIFEST_COMPLETE`.

Validation :
- 212 fichiers ;
- 3 936 721 231 octets ;
- 212/212 SHA-256 PASS ;
- 212/212 PAR1 head/tail PASS ;
- 212 chemins uniques ;
- 212 hashes distincts ;
- snapshot stable ;
- sha256 complete ;
- parquet magic checked ;
- budget préenregistré respecté.

Digest canonique de l'inventaire :
`c6baf5c42808317167b5dc60c88d86b4481b3d0004565bc3a7b33d54ef13ea54`.

Partitions nominales issues uniquement des noms :
2021-05 → 2026-05, 61 mois consécutifs, aucun mois nominal absent, indices partNNNN continus par mois.

Rapport :
`reports/data-qualification/e0_source_b_manifest_adjudication_2026-09-24.md`.

Checkpoint actif : §198.

## Verdict

**PASS borné — identité/inventaire byte-level du snapshot Source-B via helper + manifest exact.**

Non qualifiés :
- schéma logique ;
- row count / row groups ;
- timestamp/type/timezone ;
- bornes temporelles réelles ;
- ordre et trous ;
- bid/ask/spread ;
- provenance/licence ;
- Momentum/portefeuille ;
- E1.

## Prochaine action gouvernée unique

**E0-SOURCE-B-F0 — footer census read-only** :
- 8 derniers octets de chacun des 212 fichiers pour lire footer_len ;
- somme footer_len+8 ;
- BLOCKED si >128 MiB ;
- sinon lecture uniquement des footers ;
- extraire schéma, row counts/groups, timestamps/logical types/timezone, bid/ask/spread, min/max row-group si disponibles.

STOP avant tout scan de colonne temporelle.

Aucun E1, backtest, paper/broker/live ou contact Dukascopy.

STOP.
