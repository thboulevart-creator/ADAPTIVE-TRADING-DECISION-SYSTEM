# E0-SOURCE-B-F1 — adjudication du JSON timestamp-only exact

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `820e1191eb8078d93b39209d4f218ca8e5c969bd`

## 1. Preuve exacte ingérée

JSON F1 joint à la session :
- taille : **1 954 830 octets** ;
- SHA-256 exact : `2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067` ;
- schema : `ATDS_E0_SOURCE_B_F1_TIMESTAMP_SCAN_V0_1` ;
- status : `F1_COMPLETE`.

Bindings confirmés :
- F0 SHA-256 : `5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b` ;
- manifest SHA-256 : `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5` ;
- inventory digest : `5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf` ;
- schema signature : `c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d` ;
- champ : `timestamp` ;
- type : `timestamp[ms]`.

## 2. Recalcul intégral du JSON F1

Le JSON complet a été parsé.

Contrôles :
- `files[]` = **212** ;
- somme `rows_read` = **376 003 618** ;
- somme nulls = **0** ;
- somme backward transitions = **0** ;
- somme equal-adjacent timestamps = **0** ;
- somme positive transitions = **376 003 617**, soit exactement `rows - 1` ;
- `recorded_backwards[]` = **0** ;
- `recorded_gaps_gt_60s[]` = **1 605** ;
- `largest_gaps[]` = **1 605**, donc aucun gap >60 s n'est omis par la limite de registre ;
- `gap_records_truncated=false` ;
- `backward_records_truncated=false`.

Compte global des transitions positives dépassant les seuils :
- >1 s : **18 066 589** ;
- >10 s : **140 853** ;
- >60 s : **1 605** ;
- >5 min : **1 376** ;
- >1 h : **1 298** ;
- >6 h : **270** ;
- >24 h : **266**.

Bornes :
- min exact scan : `2021-05-25T00:00:00.309` ;
- max exact scan : `2026-05-24T23:59:59.963` ;
- ces bornes correspondent aux bornes F0 metadata.

Plus grand gap positif brut :
- **265 872 098 ms** ;
- soit **265 872,098 s** ;
- entre `2025-04-17T20:13:59.627` et `2025-04-20T22:05:11.725`.

## 3. Contrat d'interprétation respecté

Le JSON F1 déclare :
- `session_calendar_applied=false` ;
- `timezone_qualified=false` ;
- `gap_abnormality_claim=null` ;
- `session_claim=null` ;
- `timezone_claim=null`.

Donc F1 ne transforme pas les 1 605 gaps bruts en 1 605 pertes de données.

Il prouve seulement la structure temporelle brute du snapshot :
- ordre strictement croissant ;
- aucune valeur timestamp nulle ;
- aucune égalité adjacente ;
- inventaire complet des transitions >60 s.

## 4. Budget / portée de lecture

Le JSON confirme :
- colonnes demandées : `timestamp` uniquement ;
- aucune colonne prix ;
- aucune colonne volume ;
- aucun calcul signal/stratégie/retour/trade/PnL ;
- corpus writes = 0 ;
- row-group streaming = true ;
- planned cumulative logical bytes = **6 945 200 507**, sous 16 GiB ;
- physical OS read bytes non mesurés.

## 5. Convergence avec les preuves historiques

Les métriques F1 reproduisent exactement les chiffres centraux du travail antérieur Source-B :
- 376 003 618 lignes ;
- 1 605 gaps >60 s ;
- max ~265 872,098 s.

Il existe donc une forte raison de considérer le corpus courant comme le même corpus logique que celui ayant servi au gap-forensics historique, sous réserve de vérifier les anciens bindings/hashes et rapports locaux.

## Verdict

**PASS — E0-SOURCE-B-F1 qualifié pour l'inventaire temporel brut timestamp-only.**

Ce PASS couvre :
- intégrité structurelle temporelle brute ;
- ordre strict des timestamps ;
- absence de nulls ;
- absence d'égalités adjacentes ;
- inventaire complet des gaps bruts >60 s.

Il ne couvre PAS encore :
- fuseau réel ;
- calendrier/session ;
- classification normal vs anomalie ;
- origine des 22 open-session gaps historiques ;
- qualité bid/ask ;
- admissibilité E1/backtest.

## Prochaine action gouvernée

Récupérer les artefacts locaux gap-forensics historiques avant toute nouvelle classification externe, puis vérifier leur binding au corpus courant.

Aucun calendrier/événement ne doit être refait avant cette récupération.
