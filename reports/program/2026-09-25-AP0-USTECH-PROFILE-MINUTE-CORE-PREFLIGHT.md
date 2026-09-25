# AP0 — USTECH_PROFILE_MINUTE_CORE_V0_1 — preflight

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `9b9b7a56bc8a73dab8e8e5ae231cc31738c1afdc`

## 1. Entrée

DatasetIdentity :
`SOURCE_B_USTECH_PRICE_CORE_V0_1`.

Bindings :
- manifest :
  `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5`;
- F0 :
  `5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b`;
- F1 :
  `2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067`;
- F2 :
  `6484784faf7c77d1ba8b6d7f007ee8498ad085c4beef58a21be71898e767cb29`.

Attendus :
- 212 fichiers ;
- 376 003 618 ticks ;
- 1 605 interruptions >60 s ;
- 0 timestamp null/backward/equal-adjacent ;
- 0 bid/ask invalides selon F2.

## 2. Output identity

`USTECH_PROFILE_MINUTE_CORE_V0_1`.

Sortie :
- Parquet mensuel ;
- 1 fichier par mois UTC réellement observé ;
- manifest JSON final ;
- aucune écriture dans le corpus source.

Le répertoire output doit être neuf/non existant.

## 3. Schéma dérivé

Pour chaque minute UTC contenant au moins un tick :

- `minute_start_ms_utc : int64` ;
- `first_tick_ms : int64` ;
- `last_tick_ms : int64` ;
- `tick_count : int64` ;
- `segment_id : int64` ;
- `segment_start : bool` ;
- `gap_before_ms : int64 nullable` ;
- `mid_open : float64` ;
- `mid_high : float64` ;
- `mid_low : float64` ;
- `mid_close : float64` ;
- `spread_mean : float64` ;
- `spread_min : float64` ;
- `spread_max : float64`.

Aucun volume.

## 4. Définitions

`mid = (bid + ask) / 2`.

`spread = ask - bid`.

`spread_mean` :
moyenne pondérée par tick.

Minute :
`floor(timestamp_ms / 60_000)`.

Segment :
- premier segment = 0 ;
- incrément après chaque transition strictement >60 000 ms ;
- aucun retour continu ne pourra traverser un changement de segment.

## 5. Couverture

Aucune minute manquante n'est synthétisée.

Le manifest AP0 doit produire :
- source ticks lus ;
- minute bars écrites ;
- segments ;
- gaps détectés ;
- période min/max ;
- mois présents ;
- lignes et hash de chaque fichier mensuel ;
- taille totale output ;
- runtime versions.

Attendus structurels :
- source ticks = 376 003 618 ;
- gaps >60 s = 1 605 ;
- segments = 1 606 ;
- premier tick = 1621900800309 ;
- dernier tick = 1779667199963.

## 6. Ressources

Lecture logique planifiée :
`376 003 618 × 3 × 8 = 9 024 086 832 octets`
pour timestamp + bid + ask décodés.

Budget AP0 dédié :
**12 GiB logical source decode**.

Output cap :
**4 GiB**.

Files output cap :
**100**.

Source files cap :
**212 exacts**.

Traitement :
- un row group à la fois ;
- agrégation vectorisée par minute ;
- flush mensuel ;
- aucun corpus complet en mémoire.

## 7. Interdictions

AP0 ne calcule pas :
- return ;
- volatilité ;
- stratégie ;
- signal ;
- PnL ;
- expert ;
- régime.

AP0 est uniquement une transformation canonique.

## 8. Failure policy

BLOCKED si :
- binding différent ;
- source file taille/mtime différente ;
- timestamp non strictement croissant ;
- bid/ask invalides ;
- nombre de gaps !=1 605 ;
- source ticks !=376 003 618 ;
- segment count !=1 606 ;
- output cap dépassé ;
- output root déjà existant ;
- tentative d'écriture dans source corpus.

Aucune correction silencieuse des données.

## Verdict

**PASS — AP0 preflight autorise la matérialisation d'un helper candidat.**
