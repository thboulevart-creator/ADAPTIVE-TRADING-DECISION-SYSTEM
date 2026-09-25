# AP5 — observations comportementales price-core

Date : 2026-09-25  
Evidence : `reports/program/evidence/2026-09-25-AP5-MICROSTRUCTURE-PRICE-CORE.json`  
SHA-256 : `21dc09b082e32f20543c6206c276c24389b7b61fd930fbe2d1783adabaca4406`.

Ces observations sont descriptives et strategy-agnostic.

## Spread global

- spread tick-weighted moyen : 2.1395040593705206 ;
- médiane du spread moyen par minute : 3.342459677419323 ;
- spread minimum observé : 0.000999999996565748 ;
- spread maximum observé : 35.66699999999764.

## Densité de ticks

- moyenne : 219.99064931721645 ticks/minute observée ;
- médiane : 184 ;
- p90 : 443 ;
- p99 : 621 ;
- maximum : 830.

`tick_count` ne doit pas être interprété comme un volume négocié.

## Horloge New York

Proxy cash-clock weekday 09:30≤local<16:00 :
- 494243 minutes ;
- spread tick-weighted moyen 1.3266027854102884 ;
- tick density moyenne 382.0446278450074.

Weekday hors cash-clock :
- spread tick-weighted moyen 2.961567212934232 ;
- tick density moyenne 155.79167204561946.

Weekend :
- spread tick-weighted moyen 2.9304043635990986 ;
- tick density moyenne 132.9388871931278.

La différence d'horloge observée est descriptive ; elle ne constitue ni un edge ni une recommandation de trading.

## Relations descriptives

Pearson :
- spread moyen ↔ minute range : -0.3408104857682299 ;
- spread moyen ↔ |return 1m| : -0.23832275412888407 ;
- spread moyen ↔ tick density : -0.5910554340229595.

Aucune causalité n'est inférée.

## Quintiles de range

Spread tick-weighted moyen par quintile croissant de minute-range :
- Q1: 2.9679386586035297
- Q2: 2.6931923542133
- Q3: 2.3990828357516367
- Q4: 2.0847878539779305
- Q5: 1.7133299297862845

Tick density moyenne par quintile croissant de minute-range :
- Q1: 77.7910021179747
- Q2: 135.33390865795295
- Q3: 197.17641208064686
- Q4: 278.2318831252413
- Q5: 411.4200406042664

## Quintiles de tick density

Spread tick-weighted moyen par quintile croissant de tick density :
- Q1: 3.1795308514974803
- Q2: 3.0749636103311575
- Q3: 2.7173573495435024
- Q4: 2.1610166714784653
- Q5: 1.5260231178638717

Ces relations sont full-sample et descriptives. AP6 doit tester leur stabilité temporelle.

## Années

Années présentes : 2021 (partielle), 2022, 2023, 2024, 2025, 2026 (partielle).

Les écarts annuels présents dans AP5 sont des signaux à examiner en AP6, pas des conclusions de stabilité.
