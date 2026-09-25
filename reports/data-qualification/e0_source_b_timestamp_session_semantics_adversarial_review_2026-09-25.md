# E0-SOURCE-B — revue adversariale de la réconciliation timestamp/session

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `f8d914c23623abd811e991d301ec263ede709bc6`

## Candidat revu

`reports/data-qualification/e0_source_b_timestamp_session_semantics_reconciliation_2026-09-25.md`

Blob :
`0f257567f00bb3970ece80d37b5f6d7ee3789187`.

## Attaques

### T1 — horaires officiels actuels ≠ preuve historique complète 2021–2026

La page officielle actuelle pourrait avoir changé.

Contre-évidence :
- le F1 observe les mêmes deux régimes sur toute la période ;
- les bascules annuelles tombent sur les premiers jours de trading suivant le changement DST US ;
- une notice officielle Dukascopy 2024 confirme explicitement que le passage au Summer Trading time suit le DST US et inclut USATECH.

Verdict :
**PASS_WITH_LIMITATION** pour la session régulière ; pas de prétention à certifier chaque special holiday schedule historique.

### T2 — simple coïncidence des heures

Hypothèse alternative : les timestamps seraient Europe/Paris mais les pauses coïncideraient fortuitement.

Test :
- summer brut 20:15→22:00.
Si Europe/Paris CEST, conversion GMT ≈18:15→20:00, contradictoire avec l'officiel 20:15→22:00.
- winter brut 21:15→23:00.
Si Europe/Paris CET, conversion GMT ≈20:15→22:00, contradictoire avec l'officiel 21:15→23:00.

Verdict :
**H-EUROPE/PARIS cassée pour la session régulière.**

### T3 — metadata Parquet `isAdjustedToUTC=false`

Ce flag signifie que le fichier ne transporte pas lui-même une timezone ajustée. Il ne prouve pas que la valeur d'horloge ne peut pas être GMT/UTC par convention d'écriture.

Le verdict reste une sémantique dataset-level, pas une propriété encodée par Parquet.

**PASS_WITH_LIMITATION.**

### T4 — ancien rapport timezone_normalized_provenance

Il imposait Europe/Paris et trouvait une proximité temporelle avec une source.

Contre-analyse :
- source et Parquet sont des flux denses : nearest timestamp à quelques dizaines de ms n'est pas une preuve suffisante d'offset absolu ;
- seulement 33 exact timestamps communs sur 7 156/8 184 ;
- 0 exact bid/ask match ;
- prix divergents d'environ 786 points en moyenne ;
- le rapport lui-même est `PASS_WITH_LIMITATION` et classe uniquement `TEMPORALLY_ALIGNED_BUT_PRICE_DIVERGENCE`.

Il ne surclasse pas l'empreinte session officielle.

**PASS — ancien verdict conservé mais superseded pour la timezone.**

### T5 — conversion implicite dans les anciens scripts

Le script historique C1 utilise `datetime.timestamp()` sur datetime naïf. Cette fonction dépend de la timezone locale de l'OS.

C'est une source réelle de décalage implicite et explique pourquoi certains anciens rapports affichent un shift par rapport aux millisecondes physiques.

**PASS — défaut historique identifié.**

### T6 — classification de tous les gaps sans jours fériés

Le candidat ne prétend pas cela.
Les 315 TRUE_OPEN_SESSION_GAP sont calculés uniquement sous session régulière ; holidays/special breaks restent séparés.

**PASS par restriction de portée.**

## Verdict

**PASS_WITH_LIMITATION — raw timestamp clock = GMT/UTC supporté pour la classification des sessions régulières Source-B.**

**SUPERSEDED — Europe/Paris wall-clock comme politique de session.**

Reste à traiter :
- horaires spéciaux/jours fériés ;
- interruptions de cotation ouvertes ;
- origine/acquisition pour les gaps résiduels non déjà cross-checkés.

Aucun E1/backtest/MT5 n'est ouvert.
