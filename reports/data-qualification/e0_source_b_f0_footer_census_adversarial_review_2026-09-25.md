# E0-SOURCE-B-F0 — revue adversariale du helper footer census

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `1411f1f0fd91104edc9f5a82a045eefcbcae3890`

## Objet

Revue adversariale interne de `tools/e0_source_b_footer_census.py` avant toute exécution sur les 212 Parquet Source-B.

Cette revue ne constitue pas une contre-expertise indépendante. Elle vise à empêcher l'exécution d'un candidat manifestement fragile avant le handoff local.

## Liaison imposée

Le helper refuse tout manifest autre que :
- SHA-256 JSON : `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5`;
- digest canonique path/size/hash : `c6baf5c42808317167b5dc60c88d86b4481b3d0004565bc3a7b33d54ef13ea54`;
- 212 fichiers ;
- 3 936 721 231 octets ;
- `MANIFEST_COMPLETE`;
- `sha256_complete=true`;
- `parquet_magic_checked=true`;
- `snapshot_stable=true`.

## Attaques

### A1 — écriture accidentelle dans le corpus

**Attaque :** fournir `--output` à l'intérieur du corpus puis provoquer un échec avant la vérification du chemin de sortie.

**Résultat candidat initial : FAIL.**
La première version ne vérifiait la destination qu'après plusieurs chemins d'échec capables d'écrire un rapport.

**Correction :**
la frontière `output outside corpus` est maintenant contrôlée immédiatement après résolution des chemins et avant toute fonction `blocked(...)` susceptible d'écrire.

**Re-break : PASS.**

### A2 — budget metadata sous-compté

**Attaque :** compter seulement `footer_len+8` alors que les 8 octets de probe initial avaient déjà été lus.

**Résultat candidat initial : FAIL.**

**Correction :**
`planned_cumulative_metadata_read_bytes = initial_tail_probe_bytes + sum(footer_len+8)`.

Le gate 128 MiB porte désormais sur cette somme cumulative logique.

**Re-break : PASS.**

### A3 — schéma signature non déterministe

**Attaque :** certains objets PyArrow peuvent avoir un `repr()` contenant une adresse mémoire, rendant un hash de schéma instable.

**Résultat candidat initial : À CORRIGER.**

**Correction :**
les valeurs non JSON natives sont converties par `item()` si disponible, sinon `str()`, et non `repr()`.

**Re-break : PASS pour la sérialisation prévue.**

### A4 — substitution de manifest

**Attaque :** fournir un autre manifest ayant le même nombre de fichiers.

**Résultat : PASS.**
Le SHA-256 exact du JSON et le digest canonique de l'inventaire doivent tous deux correspondre.

### A5 — path escape / symlink / reparse point

**Attaque :** chemin relatif sortant du corpus, autre volume, symlink/reparse.

**Résultat : PASS au niveau du helper.**
Le helper normalise les chemins, vérifie leur appartenance au corpus et bloque les reparse/symlink détectables.

### A6 — corpus modifié depuis le manifest

**Attaque :** modifier un fichier après génération du manifest.

**Résultat : PASS pour les modifications ordinaires visibles par taille/mtime.**
Avant F0, les 212 tailles et `mtime_ns` doivent rester identiques au manifest. Une nouvelle vérification taille/mtime est faite après lecture metadata.

**Limitation explicite :**
F0 ne re-hashe pas 3,9 GiB. Une modification hostile conservant volontairement taille **et** mtime n'est pas cryptographiquement exclue. Ce risque n'est pas promu en PASS cryptographique ; le manifest antérieur reste l'ancre SHA-256 du snapshot.

### A7 — dépassement du footer budget

**Attaque :** footer corrompu/très grand ou somme >128 MiB.

**Résultat : PASS.**
Chaque trailer est borné par la taille physique du fichier et la somme cumulative logique bloque avant le décodage PyArrow.

### A8 — lecture de colonnes par erreur

**Attaque :** charger une table, une colonne, un row group ou des pages de données.

**Résultat : PASS au niveau du code demandé.**
Le helper utilise `pyarrow.parquet.ParquetFile` pour metadata/schema et lit les statistiques déjà stockées dans les row-group metadata. Il n'appelle aucune API `read`, `read_table`, `read_row_group` ou scan de colonne.

**Limitation explicite :**
les octets physiques réellement lus par le système de fichiers / prefetch interne de PyArrow ne sont pas mesurés. Le budget est un budget logique footer/metadata établi à partir des longueurs exactes de footer. Le helper enregistre `physical_os_read_bytes_measured=false` afin de ne pas produire une fausse preuve byte-exacte.

### A9 — absence de PyArrow

**Attaque :** environnement local sans `pyarrow`.

**Résultat : PASS fail-closed.**
Le helper s'arrête avec `BLOCKED_PYARROW_NOT_AVAILABLE` après le probe footer/budget, sans scan de colonnes.

### A10 — heuristique timestamp erronée

**Attaque :** un nom de colonne ambigu fait identifier un mauvais champ temporel.

**Résultat : PASS par restriction de portée.**
F0 ne qualifie aucune sémantique temporelle à partir de l'heuristique. Il émet seulement des **candidats temporels** et leurs statistiques metadata. L'adjudication du champ exact reste une étape suivante.

### A11 — statistiques min/max absentes

**Attaque :** row groups sans statistiques temporelles.

**Résultat : PASS fail-closed pour F0.**
Le helper compte explicitement les row groups avec/sans min-max. Il ne lit pas les pages de données pour combler l'absence. F1 reste séparé.

## Verdict

**PASS — helper F0 suffisamment borné pour tentative locale read-only, avec deux limitations explicitement non sur-promues :**
1. identité courante contrôlée par taille/mtime + manifest SHA antérieur, sans re-hash complet pendant F0 ;
2. physical OS read bytes de PyArrow non mesurés, aucune API de lecture de colonne demandée.

Ce PASS autorise seulement la **tentative F0 locale**. Il ne qualifie aucun contenu du corpus.

## Frontière suivante

Exécuter le helper exact sur le clone local contenant Source-B et le manifest scellé.

Si `F0_COMPLETE` : joindre le JSON produit pour adjudication.
Si `BLOCKED_*` : joindre le JSON produit sans contourner le breaker.

Aucun F1, E1, backtest, MT5, paper/broker/live n'est ouvert.
