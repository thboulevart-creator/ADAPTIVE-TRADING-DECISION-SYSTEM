# E0-SOURCE-B — exécution du bridge observée, manifest complet à ingérer

Date : 2026-09-24
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `d1201d4be4a78acacb2a271899ab739ff9b704e0`

## Source du constat

Sortie terminale fournie par le propriétaire après exécution locale du helper versionné `tools/e0_source_b_access_manifest.py` sur le clone contenant le corpus Source-B :

```text
MANIFEST_COMPLETE
Parquet files: 212
Parquet bytes: 3936721231
Manifest: C:\Users\Boulevart\AppData\Local\Temp\ATDS-E0-SOURCE-B-MANIFEST.json
```

Cette sortie constitue une preuve utilisateur d'exécution réussie du bridge, mais **le contenu JSON du manifest n'est pas encore accessible à cette session**. Les SHA-256 individuels, magic checks par fichier, stabilité du snapshot et détails exacts ne sont donc pas encore réadjudiqués par la session.

## Confrontation au budget préenregistré

Budget actif :
- 500 fichiers Parquet maximum ;
- 16 GiB de lecture cumulée pour hashing ;
- 8 GiB maximum par fichier pour lecture intégrale ;
- 1 000 entrées filesystem ;
- 128 MiB de métadonnées.

Sortie observée :
- 212 fichiers Parquet : **dans la borne** ;
- 3 936 721 231 octets : **dans la borne de 16 GiB**.

Le statut `MANIFEST_COMPLETE` indique que le helper n'a déclenché aucun de ses breakers bloquants et qu'il a atteint sa terminaison complète. Cette portée reste celle du helper : inventaire/identité byte-level, pas schéma logique Parquet, pas période, pas trous temporels, pas licence et pas admissibilité stratégie.

## Verdict borné

**PASS — ACCESS LOCAL + EXÉCUTION COMPLÈTE DU BRIDGE, selon la sortie terminale fournie.**

**TO-PROVE — contenu exact du manifest JSON dans la session.**

Aucune promotion vers :
- admissibilité Momentum V1 ;
- continuité cinq ans ;
- OOS ;
- portefeuille ;
- E1 ;
- backtest ;
- paper/broker/live.

## Prochaine action gouvernée unique

Rendre le fichier exact suivant accessible à la session :

`C:\Users\Boulevart\AppData\Local\Temp\ATDS-E0-SOURCE-B-MANIFEST.json`

Puis :
1. fresh HEAD ;
2. ingérer le manifest exact ;
3. vérifier son schema/status/budget ;
4. vérifier les 212 entrées, tailles et SHA-256 déclarés ;
5. confirmer `snapshot_stable = true`, `parquet_magic_checked = true`, `sha256_complete = true` ;
6. seulement ensuite sélectionner le minimum de footers/octets requis pour schéma, bornes temporelles et trous.

STOP avant toute E1.
