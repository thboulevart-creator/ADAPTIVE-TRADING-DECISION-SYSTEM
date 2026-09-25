# AP4 — PRICE STRUCTURE — preflight V0.1
Date : 2026-09-25
Fresh HEAD : d1e9691ed96332a822165b7b0ba002d371e36bfb.
Parent : docs/02.1-ASSET-BEHAVIORAL-PROFILE-CORE-PROTOCOL.md, §7 AP4.
AP3 PASS ; aucune stratégie, optimisation, exécution de marché ou PnL.

## Entrées et ressources
AP0 DatasetIdentity USTECH_PROFILE_MINUTE_CORE_V0_1.
Manifest exact SHA-256 62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce.
AP3 exact SHA-256 caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef.
61 Parquet, 91 734 766 octets, 1 709 180 minutes, 1 606 segments ; rehash intégral.
Colonnes : minute_start_ms_utc, first_tick_ms, last_tick_ms, segment_id, segment_start, gap_before_ms, mid_open, mid_high, mid_low, mid_close.
Pas de volume ni spread. mid descriptif uniquement.
Mémoire cible <1 GiB, plafond logique entrées Parquet 128 MiB, JSON 32 MiB, un fichier output hors corpus. Temps cible <10 min sur poste utilisateur ; non mesuré avant run.
Aucun nouvel accès source. Les 61 fichiers exacts sont scellés par le manifest ; rejet symlinks/reparse, échappements de chemins, nulls, OHLC invalides, ordre/segments incohérents.
Output existant refusé, création exclusive ; aucun écrasement du corpus ou des preuves.

## Métriques préenregistrées
### 1. Direction minute
r_t = log(close_t/close_{t-1}) × 10000 en bps.
Valide seulement si même segment et minute exactement adjacente.
Signe -1/0/+1 sans seuil arbitraire ; les variations exactement nulles restent une catégorie séparée.
Matrice des signes de r_t et r_{t+1}, endpoints contigus et même segment.
Taux de retournement = couples (+,-) ou (-,+) / couples dont les deux signes sont non nuls.
Taux de persistance = couples (+,+) ou (-,-) / même dénominateur.
Les zéros et frontières sont recensés séparément, jamais sautés.
### 2. Mouvements directionnels
Run = suite de retours non nuls de même signe sur minutes consécutives et même segment.
Un zéro ou une frontière coupe le run.
Durée = nombre de transitions minute ; amplitude = somme des |r| en bps.
Ce sont des swings élémentaires close-to-close à résolution 1m, pas des pivots structurels/ZigZag ni des swings tick-level.
Leur distribution dépend de la granularité ; aucun seuil choisi par performance.
### 3. Efficacité directionnelle
Horizons fixes 15 et 60 transitions minute.
E_H = |somme r| / somme |r|, mêmes H retours contigus, même segment.
Dénominateur nul : exclu et compté ; valeur dans [0,1] à tolérance 1e-9.
Mesurer aussi le déplacement signé et absolu ; réconcilier les counts valides AP2 déjà persistés 1 686 423 / 1 620 195.
### 4. Franchissements descriptifs
Horizons fixes H=15 et H=60 minutes précédentes, excluant la minute courante.
Upper_t = max(mid_high[t-H:t]), Lower_t = min(mid_low[t-H:t]).
Evénement UP si close_t > Upper_t, DOWN si close_t < Lower_t ; égalité exclue.
Toutes les H transitions reliant les H+1 minutes doivent être contiguës dans le même segment.
Chaque minute admissible est une observation ; franchissements successifs autorisés, pas des événements indépendants.
Aucune entrée/sortie/trade.
### 5. Réintégration rétrospective
Pour chaque franchissement, geler [Lower_t,Upper_t] de l'événement.
Chercher la première clôture future dans cet intervalle inclusif sur les 15 prochaines minutes, même segment et continuité exacte.
Trois issues : REENTERED (observé avant la frontière, délai 1..15), NOT_REENTERED_FULL_15M (15 minutes observées), CENSORED (frontière/fin avant 15 minutes sans réintégration).
Une clôture sautant entièrement le range n'est pas une réintégration.
Counts doivent se conserver ; pas de taux « succès » ni probabilité prédictive. Aucune généralisation aux censurés.
future_observations_used=true, causal_deployable=false ; aucune sortie label minute/live.
### 6. Réouvertures
Uniquement chaque changement de segment (>60s tick-level).
Durée interruption = first_tick_ms courant - last_tick_ms précédent.
Déplacement discontinu = log(mid_open courant/mid_close précédent) × 10000.
1 605 frontières attendues ; vérifier gap_before_ms exact.
Ce contraste est explicitement discontinu, jamais inclus dans les retours continus.
Ne pas assimiler fermeture normale, jour férié ou perte d'acquisition ; aucune causalité attribuée.

## Sorties et stabilité
Résumé global et distributions count/mean/p50/p90/p99/max, signes et counts.
Persistance et efficacité également par UTC-year, 2021/2026 partiels. AP6 conserve la qualification complète de stabilité.
Sorties agrégées uniquement. Aucun signal, aucun PnL, aucune optimisation.
L'absence de stabilité détaillée par heure ici est une limite, pas un PASS AP6.

## Tests préenregistrés
Oracle simple boucles indépendantes des routines vectorisées :
- gap et segment coupent tous retours/fenêtres/runs ;
- zéros coupent runs et sont exclus du dénominateur nonzero-pair ;
- H prix passés uniquement, pas de fuite de la minute courante ;
- égalité aux bornes, UP/DOWN et range figé ;
- réintégration à +1 et +15, hors horizon, saut complet du range, censure et fin ;
- conservation des 3 issues et des runs ;
- contrefaçon hash/identité, output dans corpus ou existant refusés ;
- réouverture à part et durée exacte ;
- fixtures aléatoires seed fixé pour les limites de fenêtre.
Audit par le même assistant, non indépendant ; tout FAIL corrigé puis re-break.

## Verdict
PASS — preflight autorise un helper candidat AP4 et ses tests synthétiques.
AP4 corpus reste BLOCKED jusqu'à l'exécution locale et l'adjudication du JSON.
