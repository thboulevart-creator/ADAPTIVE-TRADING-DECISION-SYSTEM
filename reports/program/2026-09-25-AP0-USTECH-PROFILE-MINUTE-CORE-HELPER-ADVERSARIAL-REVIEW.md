# AP0 — USTECH_PROFILE_MINUTE_CORE_V0_1 — revue adversariale du helper

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `e2e702d27d378ac7cf58f9447157737030acb824`

## Candidat

`tools/ap0_ustech_profile_minute_core.py`

Blob :
`42fcb38809a1cc0365cd4027fae5154e1d6d3b4f`.

## Binding

Le helper exige :
- manifest exact ;
- F0 exact ;
- F1 exact ;
- F2 exact ;
- inventory digest ;
- schema signature ;
- 212 fichiers ;
- 376 003 618 lignes ;
- 1 605 gaps >60 s ;
- bornes temporelles F1 exactes.

**PASS statique.**

## Attaques

### H1 — lire une colonne non autorisée

Lecture exacte :
- timestamp ;
- bid_price ;
- ask_price.

Aucun volume.

**PASS.**

### H2 — masquer une interruption

Chaque transition adjacente >60 000 ms :
- incrémente `segment_id`;
- incrémente `gap_count`;
- marque `segment_start`;
- enregistre `gap_before_ms`.

Le run doit finir avec :
- 1 605 gaps ;
- 1 606 segments ;
- 1 606 lignes segment_start.

**PASS.**

### H3 — forward-fill / minute artificielle

Le helper n'écrit une minute que si au moins un tick y existe.
Aucune boucle de calendrier ou reindex minute complet n'est utilisée.

**PASS.**

### H4 — minute dupliquée à une frontière row-group/fichier

Une minute partagée entre deux row groups/fichiers est fusionnée dans un objet `pending`.

Le helper exige ensuite que chaque minute finalisée soit strictement supérieure à la précédente.

**PASS.**

### H5 — gap >60 s fusionné dans la même minute

Le helper bloque explicitement si une rupture >60 s prétend appartenir à la même minute UTC que le pending.

**PASS fail-closed.**

### H6 — spread moyen mal pondéré

Le helper conserve `spread_sum` + `spread_count` puis calcule :
`sum(spread_tick)/tick_count`.

Fusion de fragments d'une même minute :
les sommes et comptes sont additionnés avant division.

**PASS.**

### H7 — mid utilisé comme prix d'exécution

Metadata output :
`mid_semantics=descriptive_only_not_execution_price`.

Aucun trade/return/PnL n'est calculé.

**PASS.**

### H8 — OHLC minute incohérent

Avant émission :
- tick_count >0 ;
- first/last tick dans la minute ;
- low <= open/close <= high ;
- 0 < spread_min <= spread_mean <= spread_max.

**PASS.**

### H9 — couverture mensuelle incomplète

Le candidat initial ne bornait que le nombre de fichiers.

Correction :
- exactement 61 fichiers mensuels ;
- séquence exacte 2021-05 → 2026-05 ;
- aucun mois dupliqué.

**Re-break : PASS.**

### H10 — perte de ticks lors de l'agrégation

Le manifest final exige :
`sum(output.source_ticks) = 376 003 618`.

Le source read count doit aussi égaler 376 003 618.

**PASS.**

### H11 — output corrompu

Chaque Parquet mensuel est :
- réouvert après écriture ;
- contrôlé row count + schema ;
- hashé SHA-256.

Avant succès final, chaque fichier déclaré est re-hashé une seconde fois et comparé au manifest.

**PASS.**

### H12 — overwrite d'une sortie précédente

Le répertoire output doit ne pas exister.

**PASS.**

### H13 — écriture dans le corpus source

Tout output situé dans le corpus source est refusé.

**PASS.**

### H14 — dérive source pendant AP0

Chaque fichier source :
- taille + mtime vérifiées avant lecture ;
- taille + mtime revérifiées après lecture ;
- row count + row groups confrontés à F0.

Limitation :
les 3,9 GiB ne sont pas re-hashés pendant AP0.
L'ancre cryptographique reste le manifest scellé.

**PASS avec limitation explicitement conservée.**

### H15 — budget

Lecture logique :
9 024 086 832 octets.

Plafond :
12 GiB.

Output :
max 4 GiB, max 100 fichiers.

**PASS.**

### H16 — transformation devenant analyse

Le manifest AP0 déclare :
- returns_calculated=false ;
- strategy_calculated=false ;
- pnl_calculated=false.

AP0 ne mesure pas encore volatilité/patterns.

**PASS.**

## Limitation runtime

Le helper sera réellement exécuté dans l'environnement local PyArrow qui a déjà exécuté F0/F1/F2.
Le premier run AP0 reste une tentative qualifiante :
tout `BLOCKED_AP0_*` doit être conservé et non contourné.

## Verdict

**PASS — helper AP0 suffisamment borné pour tentative locale.**

Ce PASS autorise uniquement la transformation :
`SOURCE_B_USTECH_PRICE_CORE_V0_1 → USTECH_PROFILE_MINUTE_CORE_V0_1`.

Il n'autorise aucune analyse comportementale avant adjudication du manifest AP0.
