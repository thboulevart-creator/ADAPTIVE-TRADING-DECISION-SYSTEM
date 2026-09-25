# E0-SOURCE-B — revue adversariale du classifieur de gaps de session régulière

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `ae11a11d6f5dd8f0c7faee682f4112f17d1625e6`

## Candidat

`tools/e0_source_b_regular_session_gap_classifier.py`

Blob :
`1dde9a83cbaa6cf12e446d05a854354669d0f39d`.

## Contrat

Entrée :
F1 exact SHA-256
`2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067`.

Portée :
- classifier les 1 605 gaps >60 s ;
- raw clock traité GMT/UTC uniquement sous le verdict timestamp/session qualifié ;
- session régulière America/New_York ;
- aucun holiday override ;
- aucun accès prix/volume.

## Attaques

### R1 — glissement DST

Le helper construit les frontières en timezone `America/New_York` puis convertit en UTC.
Il n'encode pas manuellement UTC-4/UTC-5.

**PASS.**

### R2 — break quotidien

Mon–Thu :
16:15→18:00 NY.

**PASS.**

### R3 — week-end

Vendredi 16:15 NY → dimanche 18:00 NY en un seul intervalle fermé.

**PASS.**

### R4 — gap touchant exactement une frontière

L'intersection exige une durée strictement positive :
`max(start,closed_start) < min(end,closed_end)`.

Un endpoint exactement à la réouverture ne crée donc pas artificiellement une durée fermée si le reste du gap est ouvert.

**PASS.**

### R5 — F1 partiel/tronqué

Le helper bloque si :
- SHA F1 différent ;
- schema/status différents ;
- rows != 376 003 618 ;
- gap count != 1 605 ;
- liste != 1 605 ;
- `gap_records_truncated != false`.

**PASS fail-closed.**

### R6 — holiday implicitement traité comme régulier

Le helper marque explicitement :
`holiday_overrides_applied=false`.

Il ne présente jamais `TRUE_OPEN_SESSION_GAP` comme preuve de perte d'acquisition.

**PASS par restriction de portée.**

### R7 — reproduction indépendante

Une implémentation indépendante basée sur détection de périodes fermées, appliquée au F1 exact, donne :
- `SESSION_BOUNDARY_GAP = 1 290`;
- `TRUE_OPEN_SESSION_GAP = 315`.

Le helper candidat produit la même logique exacte par intersections d'intervalles.

**PASS.**

## Verdict

**PASS — classifieur reproductible de session régulière.**

Ce PASS qualifie seulement la séparation :
`1 290 regular-session boundary / 315 regular-session-open`.

Il ne qualifie pas :
- holidays/special breaks ;
- origine des 315 ;
- acquisition loss hors 13 cas historiques ;
- qualité des prix.

Aucun E1/backtest/MT5 n'est ouvert.
