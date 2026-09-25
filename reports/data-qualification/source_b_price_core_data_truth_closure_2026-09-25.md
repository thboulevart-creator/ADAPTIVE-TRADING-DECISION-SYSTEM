# SOURCE-B PRICE-CORE — DATA TRUTH closure

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `5395ff144983cf08a942a994b86e62be66d6b932`

## 1. DatasetIdentity autorisée

Nom de travail :
`SOURCE_B_USTECH_PRICE_CORE_V0_1`

Ancre :
- manifest SHA-256 :
  `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5`;
- inventory digest :
  `5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf`;
- 212 Parquet ;
- 3 936 721 231 octets ;
- 376 003 618 lignes ;
- période observée :
  `2021-05-25T00:00:00.309` →
  `2026-05-24T23:59:59.963`.

Champs AUTORISÉS :
- `timestamp`;
- `bid_price`;
- `ask_price`.

Champs NON QUALIFIÉS / NON AUTORISÉS :
- `bid_volume`;
- `ask_volume`.

## 2. Chaîne de preuve

### F0 — schema / metadata

PASS :
- schéma unique sur 212/212 ;
- 488 row groups ;
- timestamp[ms] ;
- bid/ask prix et volumes présents ;
- bornes temporelles metadata cohérentes.

### F1 — timestamp-only

PASS :
- 376 003 618 timestamps ;
- 0 null ;
- 0 backward transition ;
- 0 equal-adjacent ;
- 1 605 gaps >60 s inventoriés sans troncature.

### Session / gaps

PASS — portée session régulière uniquement, avec limites explicites :
- raw clock supportée GMT/UTC pour la session régulière ;
- publisher public déclare timestamp UTC ;
- 1 290 gaps = frontières de session régulière ;
- 315 gaps = en session régulière avant holiday overlay exhaustif ;
- 13 pertes d'acquisition historiques démontrées ;
- 9 gaps historiques inconnus ;
- série déclarée **DISCONTINUE**.

Le futur moteur ne doit jamais supposer la continuité par index.

### F2 — bid/ask

PASS :
- 376 003 618 paires ;
- 0 null bid/ask ;
- 0 non-finite non-null ;
- 0 prix <=0 ;
- 0 ask<bid ;
- 0 spread nul ;
- 0 spread négatif ;
- bid min/max = 10 431.569 / 29 805.338 ;
- ask min/max = 10 433.001 / 29 806.499 ;
- spread min/max/moyen =
  0.001 / 35.667 / 2.1395040593705223.

## 3. Provenance

Dataset public :
`CarlosSilva1/ustech-ticks`.

Documenté par le publisher :
- USTECH / Nasdaq 100 Index CFD ;
- timestamp UTC ;
- période 2021-05-25 → 2026-05-24 ;
- provenance : Dukascopy via Tickstory ;
- licence : CC-BY-4.0.

Convergence forte entre le public et le snapshot local.

Non certifié :
- équivalence tick-for-tick avec un feed Dukascopy natif ;
- équivalence avec un broker tiers ;
- transformations exactes Tickstory ;
- volumes.

## 4. Usages autorisés

Sous DATA TRUTH, SOURCE_B_USTECH_PRICE_CORE_V0_1 peut servir à :
- observation descriptive de l'actif ;
- statistiques prix/spread ;
- construction d'un Asset Behavioral Profile strategy-agnostic ;
- transformations dérivées gap-aware ;
- agrégation temporelle future ;
- exploration N0 uniquement après protocole spécifique applicable.

Toute transformation crée une nouvelle DatasetIdentity + coverage report.

## 5. Interdictions

Interdit sans mouvement séparé :
- utiliser bid_volume/ask_volume ;
- parcourir la série comme continue par simple index ;
- faire traverser silencieusement une fenêtre à un gap suspect ;
- déclarer le corpus "continu" ;
- déclarer l'équivalence feed Dukascopy native ;
- promouvoir un résultat en qualification de stratégie ;
- E1/backtest/MT5/paper/broker/live par cette clôture seule.

## 6. Verdict

**PASS — DATA TRUTH fermée pour le périmètre SOURCE-B PRICE-CORE uniquement.**

La fermeture signifie :
`timestamp + bid + ask` suffisamment qualifiés pour alimenter la fondation suivante avec les limites ci-dessus.

Elle ne signifie pas :
- toutes les colonnes qualifiées ;
- continuité parfaite ;
- dataset réparé ;
- stratégie validée ;
- moteur d'exécution prêt.

## 7. Fondation suivante

**ASSET BEHAVIORAL PROFILE CORE — strategy-agnostic.**

Première priorité :
créer une représentation dérivée gap-aware et auditable permettant de mesurer :
- volatilité ;
- comportement intraday ;
- expansion/compression ;
- structure temporelle ;
- spread ;
- saisonnalité ;
sans rechercher encore de performance de stratégie.
