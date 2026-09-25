# AP3 — adjudication du JSON exact
Date : 2026-09-25
Repository : thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM
Branch : integration/system-v1
Fresh HEAD : e8cedd4890d83623c4f835f57873d0989f178282

## Preuve et portée
JSON joint : 16 078 octets.
SHA-256 : caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef.
Schema ATDS_AP3_EXPANSION_COMPRESSION_V0_1 ; AP3_COMPLETE.
Preuve exacte conservée dans reports/program/evidence/2026-09-25-AP3-EXPANSION-COMPRESSION.json.
Helper distant relu : blob 8a7aa643eb6e4414dad378ca4ddb8b98adce7bd1.
Review relue : blob 5f77c8539c0076611e8e4630648612aafaffcf2f.
AP0 manifest binding : 62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce.
AP2 binding : 4e3c79a5b9c8131f62a8fb7f205712d8a5c4301ff01b7fd3ce7226d8799d9c9f.

Le hash du fichier reçu et les contrôles agrégés ci-dessous sont recalculés dans cette session.
Le rehash des 61 Parquet et le calcul sur corpus ont été exécutés localement par le propriétaire selon le rapport fourni ; ils ne sont pas réexécutés ici.
Le JSON ne contient pas de signature attestant le code exécuté : identité du helper exécuté non attestée indépendamment.
Les valeurs AP2 embarquées sont égales aux valeurs observées ; les agrégats disponibles sont confrontés à l'adjudication AP2 versionnée.
Pas de contre-expertise indépendante : relecture et tests par le même assistant.

## Contrôles exécutés
- Parsing strict : pas de clés dupliquées, NaN ou Infinity ; nombres finis.
- Coverage : 1 709 180 minutes, 1 606 segments, RV15 1 686 423, RV60 1 620 195.
- Réconciliation embarquée RV15 et RV60 : count, mean, p50, p90, p95, p99, p99.9, max identiques (écart 0).
- Pour chaque lentille : somme états = 1 686 423 ; shares recalculées.
- Durées : somme = minutes valides ; phase_count × mean = count par état à 1e-8.
- Matrices : somme = valid_transition_count ; probabilités recalculées à 1e-15.
- Identité croisée : count de l'état - transitions diagonales = nombre de phases de cet état.
- Phases absolues : 65 860 ; transitions éligibles : 1 684 923 ; blocs éligibles : 1 500.
- Phases normalisées : 111 765 ; transitions : 1 656 829 ; blocs éligibles : 29 594.
- Sommes 24 heures et 6 années = 1 686 423 ; sommes années par état = global.
- Somme minute_rows annuelle = 1 709 180 ; 2021/2026 partiels.
- Variance share par état : somme counts = 1 620 195 ; moyenne pondérée = globale (écart 0).
- Quantiles ordonnés, non négatifs ; max variance share 0.9952792267428946.
- Scope : causal_deployable=false, strategy_agnostic=true ; aucun signal/PnL/volume.

## Break / re-break
Fixture synthétique exécutée sur le helper exact : états [0,0,1,1,-1,2,2,2,0], minutes [0,1,2,3,4,5,7,8,9], segments [0,0,0,1,1,1,1,1,1], heures [0,0,0,0,0,0,0,1,1].
Résultat : 7 phases, 8 minutes valides, 3 transitions éligibles ; les frontières segment, minute manquante, invalidité et heure coupent correctement.
Fixture classification [1,2,3,NaN], seuils 1/3 : [COMPRESSION,NORMAL,EXPANSION,INVALID].
Aucune modification du helper AP3 nécessaire pour ces tests.

## Restrictions d'interprétation
- Les shares globales 20/60/20 sont construites par quantiles, pas une découverte empirique.
- Les fenêtres RV15 voisines partagent 14 retours sur 15 : auto-transitions élevées ne prouvent ni prévisibilité ni edge.
- Les phases normalisées sont tronquées à chaque changement d'heure ; le maximum observé de 60 minutes est lié à ce découpage. Ne pas comparer naïvement leur durée aux phases absolues.
- Normaliser par heure ne retire pas les différences entre années, ni toute saisonnalité.
- Variance share et état RV15 partagent un numérateur : leur association ne prouve aucune causalité.
- Pas de stabilité qualifiée avant AP6 ; pas de labels live (seuils full-sample).

## Verdict
PASS — adjudication descriptive AP3 du rapport local exact, sous les limites probatoires explicites ci-dessus.
Ce PASS permet AP4 Price Structure ; il n'autorise stratégie, backtest, MT5, signal, PnL ou optimisation.
