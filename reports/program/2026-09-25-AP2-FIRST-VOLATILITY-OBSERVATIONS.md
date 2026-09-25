# AP2 — premières observations qualifiées de volatilité

Date : 2026-09-25

Source :
`ATDS_AP2_VOLATILITY_MAP_V0_1`
SHA-256 :
`4e3c79a5b9c8131f62a8fb7f205712d8a5c4301ff01b7fd3ce7226d8799d9c9f`.

## Portée

OBSERVATIONS/DESCRIPTIONS uniquement.

Aucun signal, causalité, edge ou stratégie.

## 1. Distribution globale

Minute range normalisé :
- mean 4.0331 bps ;
- p50 2.7673 ;
- p90 8.4528 ;
- p99 20.0454 ;
- p99.9 37.7886 ;
- max 345.4173.

Mouvement absolu 1m :
- mean 2.1304 bps ;
- p50 1.2043 ;
- p90 4.9935 ;
- p99 13.8301 ;
- p99.9 28.0355 ;
- max 350.0087.

Realized vol 60m :
- mean 21.6308 bps ;
- p50 16.1968 ;
- p90 42.7088 ;
- p99 89.0106 ;
- p99.9 163.6269 ;
- max 479.9203.

Observation :
les queues sont lourdes par rapport aux médianes ; une moyenne unique ne décrit pas suffisamment le comportement.

## 2. Structure intraday New York

RV60 moyenne :
- 00:00 NY : ~9.74 bps ;
- 08:00 : ~21.64 ;
- 09:00 : ~32.42 ;
- 10:00 : ~49.79 ;
- 11:00 : ~39.05 ;
- 12:00 : ~31.83 ;
- 13:00–15:00 : ~29.73–30.98.

Range minute moyen :
- 00:00 : ~1.72 bps ;
- 08:00 : ~4.45 ;
- 09:00 : ~7.91 ;
- 10:00 : ~8.88 ;
- 11:00 : ~6.79.

Observation :
**la volatilité possède une saisonnalité intraday structurelle très forte.**

Conséquence :
une définition naïve de compression/expansion sur seuil global confondrait en partie régime et heure de la journée.

## 3. Variation annuelle

RV60 moyenne :
- 2021 partiel : ~16.21 bps ;
- 2022 : ~32.82 ;
- 2023 : ~18.92 ;
- 2024 : ~17.24 ;
- 2025 : ~20.82 ;
- 2026 partiel : ~21.59.

Range minute moyen bps :
- 2021 partiel : ~2.97 ;
- 2022 : ~6.12 ;
- 2023 : ~3.51 ;
- 2024 : ~3.22 ;
- 2025 : ~3.88 ;
- 2026 partiel : ~4.13.

Observation :
**le niveau absolu de volatilité change fortement selon les sous-périodes.**

2021 et 2026 restent partielles et ne doivent pas être comparées comme années pleines.

## 4. Implication AP3

AP3 doit séparer :
1. **ABSOLUTE VOLATILITY STATE** — position absolue de RV15 dans sa distribution ;
2. **INTRADAY-NORMALIZED STATE** — RV15 rapportée à son niveau typique pour l'heure New York.

Cela permet de ne pas appeler automatiquement la nuit "compression" et l'ouverture US "expansion" simplement à cause de la saisonnalité attendue.

Les seuils AP3 seront descriptifs/quantiles et jamais choisis selon un PnL.

## Verdict

**PASS — observations AP2 admissibles comme mémoire descriptive.**
