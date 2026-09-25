# E0-SOURCE-B-F2 — revue adversariale du scan bid/ask courant

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `921b74628f8e24a399d3a253b5b72147d71cdfcc`

## Candidat

`tools/e0_source_b_bid_ask_quality_scan.py`

Blob :
`c3fbcda9b82dcf96bfc4ccc94b37e1e622369fd5`.

## Objet

Rejouer sur le snapshot exact courant les contrôles minimaux de qualité nécessaires au prix :
- nulls bid/ask ;
- non-finite ;
- prix <=0 ;
- ask < bid ;
- spread <=0 / spread ==0 ;
- extrema bid/ask ;
- spread min/max/moyenne.

Aucun timestamp, volume, signal, retour, trade ou PnL n'est demandé par F2.

## Binding

Le helper exige simultanément :
- manifest SHA-256 `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5` ;
- F0 SHA-256 `5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b` ;
- F1 SHA-256 `2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067` ;
- inventory digest `5cf0fe2c...` ;
- schema signature `c770f02e...` ;
- 212 fichiers ;
- 376 003 618 lignes.

## Budget

Avant F2 :
**6 945 200 507 logical bytes** comptabilisés.

F2 maximal bid+ask :
`376 003 618 × 2 × 8 = 6 016 057 888` octets.

Cumul planifié :
**12 961 258 395 octets (~12,07 GiB)**.

Plafond :
**17 179 869 184 octets (16 GiB)**.

**PASS — dans le budget gelé.**

Comme F0/F1, les physical OS read bytes de PyArrow ne sont pas mesurés ; le budget est une comptabilité logique conservatrice explicite.

## Attaques

### Q1 — lecture accidentelle timestamp/volume

Chaque row group :
`columns=["bid_price","ask_price"]`.

Le helper exige exactement ces deux colonnes après lecture.

**PASS.**

### Q2 — dataset remplacé

Manifest/F0/F1 exacts sont liés par SHA-256.
Les 212 fichiers courants doivent conserver taille + mtime du manifest avant et après lecture.

**PASS pour dérive ordinaire.**

Limitation historique conservée :
pas de re-hash 3,9 GiB pendant F2 ; une modification hostile conservant taille/mtime n'est pas ré-exclue cryptographiquement.

### Q3 — row count / row group drift

Chaque fichier est confronté au F0 :
- `num_rows`;
- `num_row_groups`;
- schema signature portée par le F0 exact.

**PASS.**

### Q4 — nulls masqués par fill

Les null counts Arrow sont enregistrés avant conversion NumPy.
Les NaN introduits par `fill_null(..., nan)` sont soustraits pour calculer les non-null nonfinite.

**PASS.**

### Q5 — bid/ask inversés

Sur chaque paire finie :
`spread = ask - bid`.

Comptes distincts :
- `ask_lt_bid` ;
- `zero_spread` ;
- `nonpositive_spread`.

**PASS.**

### Q6 — prix non positifs / inf / nan

Comptés séparément sur bid et ask.

**PASS.**

### Q7 — overflow/mémoire

Traitement un row group à la fois.
Somme spread en float64.
Aucun corpus complet n'est chargé simultanément.

**PASS architectural.**

### Q8 — volumes implicitement qualifiés

Le rapport doit conserver :
`volume_fields_qualified=false`.

Aucune conclusion sur bid_volume/ask_volume n'est autorisée par F2.

**PASS par restriction de portée.**

### Q9 — extrema non initialisés

Le candidat initial utilisait une comparaison d'identité avec `math.inf`.

Correction avant handoff :
`math.isinf(...)`.

**Re-break : PASS.**

## Verdict

**PASS — helper F2 suffisamment borné pour tentative locale read-only.**

Ce PASS autorise seulement le scan bid/ask actuel.
Il ne qualifie pas encore les résultats.

## Frontière suivante

Exécuter F2 localement avec manifest + F0 + F1 exacts.

Si `F2_COMPLETE` : joindre le JSON.
Si `BLOCKED_*` : joindre le JSON sans contourner.

Aucun volume scan, E1, backtest ou MT5.
