# ASSET BEHAVIORAL PROFILE CORE — revue adversariale du protocole V0.1

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD avant persistance : `fc5629ad5bbe152a5947fc0cc568929cab8196e5`

## Candidat

`docs/02.1-ASSET-BEHAVIORAL-PROFILE-CORE-PROTOCOL.md`

Blob :
`bfa0aa393224e54dd281735cedeb6e259089ee06`.

## Attaques

### AP-A1 — transformer l'Asset Profile en stratégie déguisée

Le protocole sépare explicitement :
- observation/description ;
- hypothèse ;
- test ;
- stratégie.

Il interdit signal, position, trade, PnL, optimisation et sélection d'expert.

**PASS.**

### AP-A2 — utiliser un prix d'exécution fictif

Le `mid` est défini comme variable descriptive :
`(bid+ask)/2`.

Le protocole interdit de le présenter comme prix d'exécution.

**PASS après correction.**

### AP-A3 — ambiguïté de `spread_mean`

Le candidat initial ne disait pas si la moyenne était pondérée par temps ou par ticks.

Correction :
`spread_mean` = moyenne **pondérée par tick** dans chaque minute.

**Re-break : PASS.**

### AP-A4 — masquer les gaps par l'agrégation minute

Aucun forward-fill.
Aucune minute synthétique.
Un nouveau segment commence après toute interruption strictement >60 000 ms.

Les retours continus ne peuvent pas traverser un segment.

**PASS.**

### AP-A5 — confusion entre pause de session et perte de données

Le CORE conserve les ruptures ; la qualification de session/gap provient de DATA TRUTH.
Il ne traite pas automatiquement toute rupture comme anomalie.

**PASS.**

### AP-A6 — contamination par volumes non qualifiés

Les champs bid_volume/ask_volume sont explicitement interdits dans V0.1.

**PASS.**

### AP-A7 — perte d'information microstructurelle

Une minute ne peut pas répondre à toutes les questions sub-minute.

Le protocole précise désormais que AP0 est une base canonique de profil, pas une compression universelle des ticks.

**PASS avec portée bornée.**

### AP-A8 — patterns choisis pour améliorer une stratégie

Expansion/compression doivent être décrites via distributions/quantiles, pas optimisées sur PnL.

**PASS.**

### AP-A9 — look-ahead caché

Le CORE est descriptif et ne produit aucun signal.
Toute future transformation/recherche décisionnelle devra avoir son propre contrat anti-look-ahead.

**PASS.**

### AP-A10 — instabilité temporelle ignorée

AP6 impose comparaison par année/sous-période et stabilité de tout pattern.

**PASS.**

## Verdict

**PASS — protocole ASSET BEHAVIORAL PROFILE CORE V0.1 suffisamment borné pour ouvrir AP0.**

Portée :
- strategy-agnostic ;
- price-core uniquement ;
- transformation 1 minute gap-aware ;
- mémoire empirique descriptive.

## Prochaine action

Pré-enregistrer et matérialiser AP0 :
`USTECH_PROFILE_MINUTE_CORE_V0_1`.
