# AP1 — premières observations comportementales qualifiées

Date : 2026-09-25

Source :
`ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1`
SHA-256 :
`db8963bb1bd1fa5b76a9a435fcb9b2d24781f92df0c5e53b6664bafe6235076b`.

## Portée

Ces éléments sont des **OBSERVATIONS/DESCRIPTIONS**.

Ils ne sont pas :
- des signaux ;
- des règles de trading ;
- des causes ;
- des preuves d'edge.

## 1. Profil intraday New York

La période 09:00–15:00 New York concentre un régime descriptif plus actif que la nuit.

Exemples :
- 09:00 : range moyen 13.3538, ~370 ticks/min, spread tick-weighted 1.8964 ;
- 10:00 : range moyen 15.0050, ~439 ticks/min, spread 1.3211 ;
- 11:00 : range moyen 11.4715, ~389 ticks/min, spread 1.3262 ;
- 12:00–15:00 : range moyen ~9.73 à 10.71, ~343 à 367 ticks/min, spread ~1.329 à 1.332.

À l'inverse, plusieurs heures nocturnes présentent :
- range moyen ~3–5 points ;
- activité ~90–175 ticks/min ;
- spread tick-weighted ~2.9–3.05.

Observation candidate :
**activité/range élevés et spread plus étroit coexistent autour de la séance US active**.

Aucune causalité ni exploitabilité n'est revendiquée.

## 2. Fermeture / réouverture

17:00 New York :
- 0 minute ;
- 0 tick.

18:00 New York :
- 75 504 minutes observées ;
- 1 361 segment starts sur 1 606 au total ;
- activité moyenne ~91.8 ticks/min ;
- range moyen ~4.41 ;
- spread tick-weighted ~2.98.

Observation :
**la structure AP1 reproduit la fermeture quotidienne et la concentration des réouvertures à 18:00 New York.**

## 3. Weekday

Ranges moyens :
- MON : 6.418 ;
- TUE : 6.645 ;
- WED : 6.785 ;
- THU : 7.027 ;
- FRI : 8.178 ;
- SUN : 4.718 ;
- SAT : aucune observation.

Friday montre aussi une activité moyenne plus élevée (~260 ticks/min) et un spread moyen plus bas (~1.99) que Sunday (~133 ticks/min, spread ~2.93).

Observation :
**le profil intraday n'est pas homogène selon le weekday.**

## 4. Variation temporelle par année

Range moyen par UTC-year :
- 2021 partiel : 4.536 ;
- 2022 : 7.783 ;
- 2023 : 4.876 ;
- 2024 : 6.125 ;
- 2025 : 8.450 ;
- 2026 partiel : 10.574.

Spread tick-weighted :
- 2021 partiel : 2.262 ;
- 2022 : 2.346 ;
- 2023 : 2.252 ;
- 2024 : 2.341 ;
- 2025 : 1.964 ;
- 2026 partiel : 1.184.

Les années partielles 2021 et 2026 ne sont pas directement comparables à une année entière.

Observation :
**les distributions évoluent sensiblement dans le temps ; l'Asset Profile doit mesurer la stabilité au lieu d'utiliser une moyenne globale comme vérité permanente.**

## 5. Implication pour AP2

AP2 Volatility Map doit :
- rester gap-aware ;
- mesurer plusieurs horizons ;
- séparer au minimum New York hour et UTC-year ;
- ne pas traverser de minute manquante ou de segment ;
- conserver 2021/2026 comme périodes partielles explicites.

## Verdict

**PASS — observations AP1 admissibles comme mémoire descriptive candidate.**

Aucune promotion vers stratégie.
