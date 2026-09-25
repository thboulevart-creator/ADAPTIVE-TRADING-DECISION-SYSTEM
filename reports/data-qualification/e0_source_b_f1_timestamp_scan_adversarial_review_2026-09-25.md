# E0-SOURCE-B-F1 — revue adversariale du scan timestamp-only

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `e75f776cb02ad22b52e885bcf9c26dafa176e271`

## Objet

Qualifier le helper :
`tools/e0_source_b_timestamp_continuity_scan.py`

avant toute lecture de colonne sur Source-B.

Blob candidat revu :
`dbcf05f8701bd434e75a08beeddce8fde08a8266`.

F1 ne cherche pas de stratégie et ne lit aucune donnée de prix/volume. Son unique objet est d'inventorier la structure temporelle brute de `timestamp`.

## Binding obligatoire

Le helper est lié simultanément à :
- manifest exact SHA-256 :
  `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5`;
- F0 exact SHA-256 :
  `5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b`;
- inventory digest :
  `5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf`;
- schema signature :
  `c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d`;
- 212 fichiers ;
- 376 003 618 lignes ;
- 488 row groups ;
- champ `timestamp`;
- type attendu `timestamp[ms]`.

## Budget

Historique logique comptabilisé :
- hashing manifest Source-B : 3 936 721 231 octets ;
- F0 metadata logique : 450 332 octets ;
- F1 timestamp décodé maximal : 376 003 618 × 8 = 3 008 028 944 octets.

Total logique planifié :
**6 945 200 507 octets**, sous le plafond de **17 179 869 184 octets (16 GiB)**.

Limitation conservée :
les octets physiques réellement lus par le filesystem/PyArrow ne sont pas mesurés. Le rapport doit conserver `physical_os_read_bytes_measured=false`.

## Attaques

### F1-A1 — lecture accidentelle des prix/volumes

**Attaque :** une API lit toute la table ou plusieurs colonnes.

**Contrôle :**
chaque row group est lu via :
`read_row_group(..., columns=["timestamp"], use_threads=False)`.

Après lecture, le helper exige exactement :
- 1 colonne ;
- nom = `timestamp`.

Aucune API de prix, bid, ask ou volume n'est appelée.

**Verdict : PASS statique.**

### F1-A2 — substitution du manifest ou de F0

SHA-256 exact des deux JSON requis avant lecture colonne.

**Verdict : PASS statique.**

### F1-A3 — dérive du corpus depuis le manifest

Chaque fichier doit conserver taille + `mtime_ns` du manifest avant lecture et après scan.

**Verdict : PASS pour dérive metadata ordinaire.**

Limitation :
pas de re-hash des 3,9 GiB pendant F1 ; une modification hostile conservant taille et mtime n'est pas cryptographiquement ré-exclue. L'ancre cryptographique reste le manifest scellé.

### F1-A4 — dérive schéma/row count/row groups

Pour chaque fichier :
- signature F0 attendue ;
- row count Parquet = row count F0 ;
- num row groups = F0.

**Verdict : PASS statique.**

### F1-A5 — F1 produit des timestamps incompatibles avec F0

Le scan doit retrouver exactement :
- min = `1621900800309` ms ;
- max = `1779667199963` ms.

Sinon :
`BLOCKED_F1_F0_TEMPORAL_BOUND_MISMATCH`.

**Verdict : PASS fail-closed.**

### F1-A6 — timestamps nuls

Les nulls sont comptés explicitement.
Le helper ne relie jamais deux timestamps séparés par un null pour inventer une continuité.

Les segments sont cassés autour des nulls.

**Verdict : PASS.**

### F1-A7 — timestamp égal interprété comme ligne dupliquée

Interdit.

Le helper compte uniquement :
`equal_adjacent_timestamps`.

Il ne conclut pas à un duplicate row puisque bid/ask/volume ne sont pas lus.

**Verdict : PASS par restriction sémantique.**

### F1-A8 — retour temporel

Tout `current_timestamp < previous_timestamp` est compté comme `backward_transition` et des exemples sont conservés.

Le registre est borné à 10 000 objets ; le compteur total reste distinct du registre.

Une erreur de bookkeeping de troncature détectée pendant la revue a été corrigée avant handoff.

**Verdict : PASS.**

### F1-A9 — très grand nombre de gaps

Tous les gaps sont comptés selon les seuils :
- >1 s ;
- >10 s ;
- >60 s ;
- >5 min ;
- >1 h ;
- >6 h ;
- >24 h.

Les événements >60 s sont enregistrés jusqu'à 100 000 objets.
Les 2 000 plus grands sont conservés séparément.

La troncature éventuelle est explicitement signalée.

**Verdict : PASS.**

### F1-A10 — perte des transitions entre row groups/fichiers

Le dernier timestamp valide d'un row group est comparé au premier du suivant uniquement si la frontière physique n'est pas cassée par un null.

Le même mécanisme traverse naturellement les frontières de fichiers puisque l'ordre est celui du manifest.

**Verdict : PASS statique.**

### F1-A11 — classification abusive d'un gap

Le helper n'applique aucun calendrier de marché ni timezone.

Il enregistre :
- `timezone_claim=null`;
- `session_claim=null`;
- `gap_abnormality_claim=null`;
- `session_calendar_applied=false`.

Donc :
```text
gap observé ≠ donnée manquante prouvée
```.

**Verdict : PASS.**

### F1-A12 — fuseau fabriqué

Les ISO produits sont nommés explicitement `naive_iso` et dérivent de l'encodage epoch millisecond uniquement pour rendre les valeurs lisibles.

Aucun suffixe `Z` et aucune qualification UTC ne sont produits.

**Verdict : PASS.**

### F1-A13 — dépassement de mémoire

Le corpus n'est jamais chargé entièrement.
Traitement : un row group, une colonne.

Un row group typique est donc borné par sa colonne timestamp, ses arrays NumPy temporaires et overhead.

**Verdict : PASS architectural.**

### F1-A14 — dépendance absente

Absence PyArrow/NumPy :
`BLOCKED_RUNTIME_DEPENDENCY`.

**Verdict : PASS fail-closed.**

## Limitation de la revue

L'environnement assistant courant ne possède pas PyArrow ; aucun test synthétique runtime Parquet n'est donc revendiqué ici.

La revue est statique + contractuelle. La première exécution réelle locale reste une tentative qualifiante et tout `BLOCKED_*` doit être conservé, non contourné.

## Verdict

**PASS — helper F1 suffisamment borné pour tentative locale timestamp-only.**

Ce PASS n'est pas :
- un PASS de continuité ;
- un PASS de timezone ;
- un PASS de sessions ;
- un PASS de qualité des prix ;
- une autorisation E1/backtest.

## Frontière suivante

Exécuter F1 localement avec :
- le manifest scellé ;
- le JSON F0 exact ;
- le corpus existant.

Si `F1_COMPLETE` : joindre le JSON F1.
Si `BLOCKED_*` : joindre le JSON sans contourner.

STOP avant toute lecture bid/ask/volume.
