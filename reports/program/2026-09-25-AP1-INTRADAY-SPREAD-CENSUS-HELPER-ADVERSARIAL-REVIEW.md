# AP1 — INTRADAY + SPREAD CENSUS — revue adversariale du helper

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `77a28fdfc315374eed740cb6f4cef351a99d740a`

## Candidat

`tools/ap1_intraday_spread_census.py`

Blob :
`9f613063fb8a190a1ff6f2f8b12c97c4ed97712a`.

## Attaques

### A1 — substitution de l'entrée AP0

Le helper exige le manifest AP0 exact :
`62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`.

Il exige aussi :
- identité `USTECH_PROFILE_MINUTE_CORE_V0_1` ;
- 61 fichiers ;
- 1 709 180 minutes ;
- 376 003 618 ticks ;
- 1 606 segments.

**PASS.**

### A2 — fichier AP0 modifié après création du manifest

Avant lecture, chacun des 61 Parquet est :
- trouvé sous le root AP0 ;
- vérifié par taille ;
- re-hashé SHA-256 contre le manifest exact.

**PASS cryptographique.**

### A3 — colonnes hors scope

AP1 lit uniquement :
- minute_start_ms_utc ;
- tick_count ;
- segment_id ;
- segment_start ;
- mid_high ;
- mid_low ;
- spread_mean ;
- spread_min ;
- spread_max.

Aucun volume source, aucun bid/ask tick brut.

**PASS.**

### A4 — schéma ou metadata dérivés falsifiés

Chaque Parquet AP0 doit avoir :
- le schéma exact attendu ;
- `dataset_identity=USTECH_PROFILE_MINUTE_CORE_V0_1` ;
- `volumes_used=false` ;
- `mid_semantics=descriptive_only_not_execution_price`.

**PASS.**

### A5 — ordre temporel cassé

Minute timestamps :
- strictement croissants dans chaque fichier ;
- strictement croissants entre fichiers.

**PASS fail-closed.**

### A6 — segments cassés

Le helper vérifie :
- segment_id non décroissant ;
- saut maximal +1 ;
- segment_start exactement lorsque segment_id augmente ;
- premier segment = 0 ;
- total segment_start = 1 606 ;
- dernier segment = 1605.

**PASS.**

### A7 — range invalide

`minute_range = mid_high - mid_low`.

Toute ligne `mid_high < mid_low` bloque.

Aucun return ou direction n'est calculé.

**PASS.**

### A8 — spread invalide

Pour chaque minute :
- spread_min >0 ;
- spread_min <= spread_mean <= spread_max ;
- valeurs finite.

**PASS.**

### A9 — agrégation AP0 ayant déformé le spread global

AP1 reconstruit :
`sum(spread_mean * tick_count)/sum(tick_count)`.

Il doit retrouver F2 à tolérance 1e-9 :
- min = 0.000999999996565748 ;
- max = 35.66699999999764 ;
- mean = 2.1395040593705223.

Sinon AP1 bloque.

**PASS design.**

### A10 — DST New York incorrect

Les dimensions NY sont dérivées par :
UTC hour → `America/New_York` via `zoneinfo`.

L'offset n'est pas hardcodé.
Les heures répétées/manquantes DST sont naturellement agrégées selon l'heure locale observée.

**PASS.**

### A11 — percentiles non reproductibles

Méthode explicitement :
NumPy `percentile(..., method="linear")`.

Runtime NumPy/PyArrow est enregistré.

**PASS.**

### A12 — bucket vide

Les 24/7/168 buckets sont matérialisés même sans minute.
Les métriques vides deviennent null et les counts restent 0.

**PASS.**

### A13 — perte de conservation

Chaque dimension doit sommer exactement :
**1 709 180 minutes**.

Le total ticks relu doit être :
**376 003 618**.

**PASS fail-closed.**

### A14 — stratégie déguisée

AP1 ne calcule :
- aucun return ;
- aucun label futur ;
- aucun signal ;
- aucun PnL ;
- aucune optimisation.

Les percentiles décrivent les distributions observées.

**PASS.**

### A15 — mémoire

Le corpus dérivé fait 1 709 180 lignes.
Les colonnes requises sont concaténées en NumPy ; ordre de grandeur très inférieur à 1 GiB.
Les ticks bruts ne sont jamais chargés.

**PASS architectural.**

## Verdict

**PASS — helper AP1 suffisamment borné pour tentative locale.**

AP1 pourra produire une première carte descriptive :
- activité intraday ;
- range minute ;
- spread ;
- différences UTC / New York / weekday / year.

Il ne produit aucune hypothèse de trading validée.

## Frontière suivante

Exécuter AP1 localement sur le répertoire AP0 qualifié puis joindre le JSON exact.

Aucun AP2 avant adjudication AP1.
