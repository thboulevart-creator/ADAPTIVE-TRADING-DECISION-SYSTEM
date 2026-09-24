# E0-SOURCE-B — adjudication du manifest exact

Date : 2026-09-24
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `6215836c2d12c39d945cfb63d86f3ba8aeecf823`

## 1. Preuve ingérée

Le manifest exact généré localement par `tools/e0_source_b_access_manifest.py` a été joint à la session puis parsé intégralement.

Identité du fichier joint :
- taille JSON : **86 752 octets** ;
- SHA-256 du JSON exact : `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5` ;
- schéma déclaré : `ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1` ;
- statut déclaré : `MANIFEST_COMPLETE` ;
- génération UTC : `2026-09-24T10:58:11.531785+00:00`.

Le manifest n'est pas recopié dans GitHub afin d'éviter de republier inutilement les chemins absolus locaux. Son identité exacte est scellée par le SHA-256 ci-dessus.

Digest canonique de l'inventaire `relative_path<TAB>size_bytes<TAB>sha256`, trié dans l'ordre du manifest :
`c6baf5c42808317167b5dc60c88d86b4481b3d0004565bc3a7b33d54ef13ea54`.

## 2. Validation structurelle complète

Le parsing actuel vérifie **les 212 entrées**, pas un échantillon.

Résultats :
- `parquet_files = 212` et exactement 212 objets `files[]` ;
- `total_entries = 279`, inférieur au plafond 1 000 ;
- somme recalculée de `size_bytes` = **3 936 721 231 octets**, exactement égale à `total_parquet_bytes` ;
- `sha256_read_bytes = 3 936 721 231`, égal au volume total ;
- 212/212 `sha256_status = PASS` ;
- 212/212 empreintes au format hexadécimal SHA-256 de 64 caractères ;
- 212 chemins relatifs uniques ;
- 212 SHA-256 distincts ;
- 212/212 `parquet_magic_head = PAR1`, `parquet_magic_tail = PAR1`, `parquet_magic_status = PASS` ;
- `parquet_magic_checked = true` ;
- `sha256_complete = true` ;
- `snapshot_stable = true` ;
- `magic_read_bytes = 1696 = 212 × 8`.

Budget :
- 212 < 500 fichiers ;
- 279 < 1 000 entrées ;
- 3 936 721 231 < 17 179 869 184 octets (16 GiB) ;
- plus grand fichier : **33 177 264 octets**, très inférieur au plafond 8 GiB ;
- lecture magic 1 696 octets < 128 MiB.

Aucune contradiction interne n'a été trouvée entre les totaux déclarés et le détail des 212 entrées.

## 3. Structure nominale des partitions

Tous les chemins suivent :
`year=YYYY/month=MM/USTECH-YYYY-MM-partNNNN.parquet`.

Le nom de partition `year/month` correspond toujours au `YYYY-MM` du nom de fichier.

Couverture nominale de partitions :
- premier mois : **2021-05** ;
- dernier mois : **2026-05** ;
- **61 mois calendaires consécutifs** dans les noms ;
- aucun mois nominal manquant entre ces bornes ;
- indices `partNNNN` continus et démarrant à 0000 dans chaque mois ;
- 1 à 5 fichiers par mois.

Ceci est une propriété **de l'arborescence et des noms uniquement**. Elle ne démontre pas :
- que les timestamps contenus commencent réellement en mai 2021 ou finissent réellement en mai 2026 ;
- qu'un mois est complet ;
- qu'il n'existe aucun trou intrafichier ou inter-fichier ;
- que les lignes sont ordonnées ;
- que le fuseau ou les sessions sont corrects.

## 4. Verdict borné

**PASS — identité byte-level et stabilité du snapshot Source-B telles que décrites par le manifest exact, cohérent sur 212/212 fichiers.**

Ce PASS couvre :
- inventaire des fichiers ;
- tailles ;
- SHA-256 déclarés par le helper exécuté sur le corpus ;
- format container minimal `PAR1` ;
- cohérence des budgets ;
- stabilité metadata du snapshot pendant l'inventaire.

Il ne couvre PAS encore :
- schéma logique Parquet ;
- noms/types des colonnes ;
- row counts ;
- row groups ;
- timestamp field/type/timezone ;
- bornes temporelles réelles ;
- monotonicité ;
- trous ;
- bid/ask/spread ;
- provenance/licence ;
- adéquation Momentum V1 / portefeuille ;
- E1.

## 5. Minimum de lecture nécessaire pour la suite E0

La prochaine lecture doit rester **metadata-first**.

### Étape F0 — footer census de tous les 212 fichiers

Pour chaque fichier :
1. vérifier taille + mtime contre le manifest déjà scellé ;
2. lire uniquement les **8 derniers octets** ;
3. interpréter les 4 octets `footer_len` little-endian précédant `PAR1` ;
4. additionner `footer_len + 8` sur les 212 fichiers ;
5. si le total dépasse le plafond préenregistré de **128 MiB**, verdict BLOCKED ;
6. sinon lire exactement ces footers, sans colonnes de données.

Objectifs footer-only :
- schéma et cohérence inter-fichiers ;
- row count / row groups ;
- colonnes timestamp et types/logical types ;
- métadonnées timezone/Arrow si présentes ;
- présence des colonnes bid/ask/spread ;
- statistiques min/max de timestamp par row group si disponibles ;
- bornes temporelles réalisables sans lire les pages de données.

### Étape F1 — scan temporel minimal seulement si nécessaire

Les statistiques de footer ne peuvent pas, à elles seules, prouver l'absence de trous **à l'intérieur** d'un row group.

Si F0 ne suffit pas pour la continuité :
- lire uniquement la colonne temporelle identifiée ;
- aucune colonne prix/volume ;
- streaming par fichier/row group ;
- vérifier ordre, doublons temporels si applicable, min/max et gaps ;
- ne calculer aucun signal, retour, trade ou PnL.

La lecture prix/bid/ask n'est pas nécessaire pour mesurer les trous temporels ; leur existence/type peut être déterminé depuis le schéma footer.

## Prochaine action gouvernée unique

**E0-SOURCE-B-F0 — matérialiser puis exécuter un census read-only des footers Parquet des 212 fichiers, lié au manifest SHA-256 ci-dessus et limité au budget metadata de 128 MiB.**

STOP avant tout scan de colonne temporelle F1. F1 devra être décidé après examen de F0.

Aucun E1, backtest, paper/broker/live ou contact Dukascopy n'est ouvert.
