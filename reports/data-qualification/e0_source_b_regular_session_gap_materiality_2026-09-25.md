# E0-SOURCE-B — registre de gaps de session régulière et matérialité

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `3a791cf2d8102b6c1dce3ca639033d51d07b2e11`

## 1. Entrées qualifiées

F1 exact :
- SHA-256 `2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067`;
- 376 003 618 timestamps ;
- 1 605 gaps >60 s ;
- registre des 1 605 gaps non tronqué.

Sémantique session :
- raw clock = GMT/UTC : `PASS_WITH_LIMITATION` pour session régulière ;
- USATECH summer break : 20:15→22:00 GMT ;
- USATECH winter break : 21:15→23:00 GMT ;
- Europe/Paris wall-clock : superseded pour cet usage.

Historique gap-forensics :
- 22 intervalles exacts ré-identifiés dans F1 ;
- 13 `DATASET_ACQUISITION_LOSS`;
- 9 `UNKNOWN_INSUFFICIENT_SOURCE_CONTEXT`.

## 2. Classification régulière des 1 605 gaps

Avec le calendrier régulier uniquement :
- `SESSION_BOUNDARY_GAP` : **1 290** ;
- `TRUE_OPEN_SESSION_GAP` : **315**.

Les 315 se répartissent actuellement en :
- `HISTORICAL_PROVEN_ACQUISITION_LOSS` : **13** ;
- `HISTORICAL_UNKNOWN` : **9** ;
- `HOLIDAY_CONTEXT_UNRESOLVED` : **4** ;
- `UNRESOLVED_CURRENT` hors holiday-context : **289**.

Important :
`HOLIDAY_CONTEXT_UNRESOLVED` signifie seulement qu'une notice officielle Dukascopy établit des horaires spéciaux le jour concerné. Cela ne signifie PAS que l'intervalle exact du gap est démontré comme fermeture planifiée.

## 3. Profil de durée des 315 gaps open-session

Nombre de gaps :
- >60 s : **315** ;
- >2 min : **154** ;
- >5 min : **86** ;
- >10 min : **17** ;
- >15 min : **12** ;
- >30 min : **10** ;
- >1 h : **8** ;
- >6 h : **1** ;
- >24 h : **0**.

Pour les gaps >15 min :
- 2 historiques `DATASET_ACQUISITION_LOSS` ;
- 3 avec contexte holiday officiel mais intervalle exact non encore expliqué ;
- 7 autres non résolus.

## 4. Douze gaps matériellement longs (>15 min)

| # | Début UTC | Fin UTC | Durée s | État |
|---|---|---|---:|---|
| 1 | 2022-01-24 03:18:18.863 | 2022-01-24 04:21:22.775 | 3783.912 | UNRESOLVED_CURRENT |
| 2 | 2022-10-18 12:08:25.479 | 2022-10-18 15:21:01.427 | 11555.948 | UNRESOLVED_CURRENT |
| 3 | 2023-06-02 15:10:45.266 | 2023-06-02 15:26:42.827 | 957.561 | UNRESOLVED_CURRENT |
| 4 | 2023-09-25 10:05:27.691 | 2023-09-25 11:00:00.163 | 3272.472 | UNRESOLVED_CURRENT |
| 5 | 2024-07-19 05:07:15.572 | 2024-07-19 08:03:07.060 | 10551.488 | UNRESOLVED_CURRENT |
| 6 | 2024-07-19 09:16:08.239 | 2024-07-19 10:48:54.634 | 5566.395 | UNRESOLVED_CURRENT |
| 7 | 2024-08-02 03:04:34.629 | 2024-08-02 03:33:57.794 | 1763.165 | HISTORICAL_PROVEN_ACQUISITION_LOSS |
| 8 | 2024-08-12 16:36:47.635 | 2024-08-12 17:06:48.558 | 1800.923 | HISTORICAL_PROVEN_ACQUISITION_LOSS |
| 9 | 2024-10-09 23:05:55.826 | 2024-10-10 00:11:49.780 | 3953.954 | UNRESOLVED_CURRENT |
| 10 | 2025-01-20 12:22:31.674 | 2025-01-20 13:32:28.486 | 4196.812 | HOLIDAY_CONTEXT_UNRESOLVED — MLK |
| 11 | 2025-11-28 02:44:16.413 | 2025-11-28 07:00:05.946 | 15349.533 | HOLIDAY_CONTEXT_UNRESOLVED — Thanksgiving |
| 12 | 2025-11-28 07:00:05.946 | 2025-11-28 13:31:28.348 | 23482.402 | HOLIDAY_CONTEXT_UNRESOLVED — Thanksgiving |

Un quatrième gap holiday-context, Thanksgiving 2025, dure seulement 63.402 s :
`2025-11-28 02:02:59.345 → 02:04:02.747 UTC`.

## 5. Preuves holiday disponibles

Dukascopy publie que le Trading Breaks Calendar indique les horaires spéciaux en GMT dus aux jours fériés.

2025 MLK :
notice officielle indiquant des special trading breaks pour CFD et bullion le 20 janvier 2025.

2025 Thanksgiving :
notice officielle indiquant des special market closures jeudi 27 et vendredi 28 novembre 2025.

Ces notices justifient un flag `HOLIDAY_CONTEXT`, mais les pages statiques récupérées ici ne donnent pas les horaires exacts USATECH 2025 de chaque intervalle.

Des notices historiques Dukascopy détaillées montrent pour USATECH que les jours MLK / Thanksgiving ont effectivement eu des fermetures anticipées et réouvertures spécifiques, mais elles ne doivent pas être extrapolées mécaniquement à 2025.

Conclusion :
les quatre gaps 2025 restent `UNRESOLVED` quant à leur intervalle exact jusqu'à preuve des horaires spéciaux correspondants.

## 6. Application du DATA CONTRACT

`docs/05-DATA-CONTRACT.md §1` impose :
- classification des écarts ;
- identification des écarts non explicables par le calendrier ;
- verdict `SÉRIE CONTINUE | SÉRIE DISCONTINUE`;
- interdiction de parcourir par index une série discontinue.

À l'état courant :

**VERDICT DE CONTINUITÉ : SÉRIE DISCONTINUE.**

Ce verdict ne rend pas le corpus inutilisable.

Usage possible ultérieur :
- parcours par horodatage ;
- rupture explicite de chaîne à chaque interruption suspecte ;
- aucune fenêtre, indicateur ou position ne doit traverser silencieusement une interruption non légitime ;
- les interruptions légitimes (daily break/week-end/holiday documenté) doivent être traitées comme telles ;
- toute transformation H1 devra produire son propre dataset identity + coverage report conformément au §3.

## 7. Décision de matérialité

Il n'est ni nécessaire ni justifié de prouver une cause externe pour chacun des 315 gaps avant de continuer la qualification structurelle du corpus.

La preuve nécessaire est :
1. calendrier régulier qualifié ;
2. holiday/special closures connues lorsqu'elles sont prouvables ;
3. registre des interruptions suspectes ;
4. moteur futur gap-aware empêchant toute traversée silencieuse ;
5. limites d'usage explicites.

Les 12 gaps >15 min constituent le sous-ensemble prioritaire pour forensic supplémentaire si la future transformation/recherche risque de les traverser.

## Verdict gouverné

**PASS — inventaire/classification de matérialité des interruptions pour permettre une utilisation future gap-aware.**

**FAIL — continuité parfaite du corpus : le corpus est DISCONTINU.**

**BLOCKED — tout moteur qui supposerait une continuité par index.**

Cette décision n'autorise pas E1/backtest/MT5.
