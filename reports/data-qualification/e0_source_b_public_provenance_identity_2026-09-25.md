# E0-SOURCE-B — provenance publique, identité instrument et limites de preuve

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `e4240d9b2239419ff3cdb902613d2be6217c4bc0`

## 1. Source publique observée

Dataset public :
`CarlosSilva1/ustech-ticks`

URL :
`https://huggingface.co/datasets/CarlosSilva1/ustech-ticks`

Arbre public observé le 2026-09-25 :
- branche `main` ;
- taille affichée : **3.94 GB** ;
- années présentes : 2021, 2022, 2023, 2024, 2025, 2026 ;
- commit court affiché : `30996ad`, marqué `verified` ;
- licence affichée : **CC-BY-4.0**.

## 2. Déclarations du dataset card

Le README public déclare :
- instrument : **USTECH (Nasdaq 100 Index CFD)** ;
- alias : USTECH / US Tech 100 ;
- période : **2021-05-25 → 2026-05-24** ;
- granularité : tick milliseconde ;
- ~376 millions de lignes ;
- Apache Parquet Snappy ;
- partitionnement Hive `year/month` ;
- `timestamp` = UTC tick time, millisecond precision ;
- `bid_price` = best bid, index points ;
- `ask_price` = best ask, index points ;
- volumes bid/ask ;
- provenance déclarée : **“Sourced from Dukascopy via Tickstory”** ;
- usage research/educational sous CC-BY-4.0.

Le Dataset Viewer affiche :
- split `train` ~376M rows ;
- timestamp[ms] ;
- bid/ask/volumes ;
- premiers ticks commençant à `2021-05-25T00:00:00.309000` ;
- derniers ticks affichés jusqu'à `2026-05-24T23:59:59.963000`.

## 3. Convergence avec le snapshot local qualifié

Snapshot local :
- 212 Parquet ;
- **3 936 721 231 octets** ;
- **376 003 618 lignes** ;
- min timestamp exact : `2021-05-25T00:00:00.309` ;
- max timestamp exact : `2026-05-24T23:59:59.963` ;
- schéma : timestamp/bid_price/ask_price/bid_volume/ask_volume.

Ces éléments convergent exactement avec les caractéristiques principales du dataset public.

Le dataset card public dit explicitement que `timestamp` est UTC. Cette déclaration indépendante du calcul de session renforce le verdict courant :
`raw timestamp clock = GMT/UTC`.

## 4. Ce qui est prouvé vs déclaré

### Prouvé pour le snapshot local

- identité byte-level locale via manifest SHA-256 ;
- 212 fichiers ;
- taille locale exacte ;
- 376 003 618 lignes ;
- schéma ;
- période réelle par lecture ;
- horodatage strictement croissant ;
- structure des gaps bruts.

### Documenté par le publisher public

- nom USTECH / Nasdaq 100 Index CFD ;
- timestamp UTC ;
- provenance `Dukascopy via Tickstory` ;
- licence CC-BY-4.0 ;
- période/format/partitionnement.

### Non prouvé

La déclaration `Sourced from Dukascopy via Tickstory` est une **provenance documentaire de publisher**.

Elle ne prouve pas :
- l'équivalence tick-for-tick avec un flux Dukascopy natif ;
- l'absence de transformation Tickstory ;
- l'identité exacte d'un symbole broker tiers ;
- l'équivalence de prix avec VT Markets NAS100 ;
- qu'un prix source extérieur peut réparer automatiquement le corpus.

Les anciens cross-checks source ont d'ailleurs trouvé des divergences de prix, donc feed equivalence reste non certifiée.

## 5. Verdict

**PASS — identité documentaire du dataset public : USTECH / Nasdaq 100 Index CFD, timestamp UTC, période 2021-05-25→2026-05-24, licence CC-BY-4.0.**

**PASS — convergence structurelle forte entre le dataset public et le snapshot local courant.**

**BLOCKED — équivalence cryptographique du snapshot local avec les 212 objets distants actuels : les hashes distants n'ont pas été réacquis dans ce mouvement.**

**BLOCKED — équivalence feed-value native Dukascopy : non démontrée et non requise pour reconnaître la provenance documentaire.**

## 6. Conséquence

Source-B peut porter l'identité de recherche :
`USTECH / Nasdaq 100 Index CFD — CarlosSilva1/ustech-ticks — publisher provenance: Dukascopy via Tickstory`

avec limites explicites :
- corpus discontinu ;
- feed equivalence non certifiée ;
- traitements gap-aware obligatoires ;
- toute transformation produit une nouvelle DatasetIdentity.

Aucun E1/backtest/MT5 n'est ouvert.
