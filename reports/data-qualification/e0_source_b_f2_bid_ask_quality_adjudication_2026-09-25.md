# E0-SOURCE-B-F2 — adjudication du JSON bid/ask exact

Date : 2026-09-25
Dépôt : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branche : `integration/system-v1`
HEAD vérifié avant écriture : `1dfe39eeb3415756807556f8ec49db34ad3391a1`

## 1. Preuve exacte ingérée

JSON F2 joint à la session :
- taille : **76 768 octets** ;
- SHA-256 : `6484784faf7c77d1ba8b6d7f007ee8498ad085c4beef58a21be71898e767cb29` ;
- schema : `ATDS_E0_SOURCE_B_F2_BID_ASK_QUALITY_V0_1` ;
- status : `F2_COMPLETE`.

Bindings :
- manifest SHA-256 : `c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5` ;
- F0 SHA-256 : `5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b` ;
- F1 SHA-256 : `2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067` ;
- inventory digest : `5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf` ;
- schema signature : `c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d`.

## 2. Recalcul intégral

Le JSON complet a été parsé.

Contrôles :
- `files[]` = **212** ;
- chemins uniques = **212/212** ;
- somme `rows` = **376 003 618** ;
- somme bid null = **0** ;
- somme ask null = **0** ;
- somme bid nonfinite non-null = **0** ;
- somme ask nonfinite non-null = **0** ;
- somme bid <=0 = **0** ;
- somme ask <=0 = **0** ;
- somme `ask < bid` = **0** ;
- somme spread <=0 = **0** ;
- somme spread ==0 = **0**.

Le summary correspond aux agrégats fichier par fichier.

## 3. Extrema et spread

Sur **376 003 618** paires valides :
- bid min = **10 431.569** ;
- bid max = **29 805.338** ;
- ask min = **10 433.001** ;
- ask max = **29 806.499** ;
- spread min = **0.000999999996565748** ;
- spread max = **35.66699999999764** ;
- spread moyen = **2.1395040593705223** ;
- valid spread count = **376 003 618**.

Aucun spread nul ou négatif.

## 4. Budget et portée

Le JSON déclare :
- max cumul logique = **17 179 869 184** octets ;
- avant F2 = **6 945 200 507** ;
- bid/ask F2 planifié = **6 016 057 888** ;
- cumul planifié = **12 961 258 395** ;
- physical OS read bytes measured = false.

Lecture :
- `bid_price` ;
- `ask_price`.

Non lus :
- timestamp ;
- bid_volume ;
- ask_volume.

Aucun signal, stratégie, retour, trade ou PnL.

## 5. Volumes

Le JSON exact déclare :
`volume_fields_qualified=false`.

Les champs volume sont donc présents par schéma mais **NON QUALIFIÉS**.

Ils ne doivent être utilisés dans aucun Asset Profile, feature, signal, filtre, régime ou recherche tant qu'un mouvement séparé ne les qualifie.

## Verdict

**PASS — E0-SOURCE-B-F2 qualifié pour bid_price/ask_price.**

Ce PASS couvre :
- présence et validité numérique de bid/ask ;
- positivité ;
- relation ask > bid ;
- spread strictement positif ;
- extrema et spread global agrégé.

Ce PASS ne couvre pas :
- distribution détaillée du spread ;
- spread par session/news ;
- slippage ;
- volumes ;
- équivalence feed native Dukascopy ;
- continuité parfaite.

## Conséquence

Le sous-ensemble de champs :
`timestamp + bid_price + ask_price`
possède désormais une chaîne de qualification actuelle suffisante pour former un **Source-B PRICE-CORE** avec limites explicites.

La clôture DATA TRUTH globale doit donc être formulée comme une clôture de périmètre autorisé, et non comme une qualification de toutes les colonnes du Parquet.
