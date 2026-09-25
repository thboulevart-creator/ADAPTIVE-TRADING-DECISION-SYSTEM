# AP5 — MICROSTRUCTURE PRICE-CORE — revue adversariale et re-break du candidat persisté

Date : 2026-09-25  
Branche : `integration/system-v1`  
Fresh HEAD avant persistance de cette revue : `715c3e4affa44778785d6c222782eda257ed19e7`.

## 1. Artefacts exacts re-breakés

Helper :
- path : `tools/ap5_microstructure_price_core.py` ;
- blob Git : `21de65a7fbf8277dd2eb0afc99f4c2b80912af06` ;
- SHA-256 : `fdb929f54d5c816cd12fb03130545b3714a38cb2261d3b23433fb1cd4b0f7671`.

Tests :
- path : `tests/test_ap5_microstructure_price_core.py` ;
- blob Git : `f0b732b66e258fff416cdf643c1de6fa4c373baa` ;
- SHA-256 : `ca6d836b7eafccd765a3716186dd05c08b036db69a44deac6476300399473375`.

Mutation runner :
- path : `tests/run_ap5_mutation_breakers.py` ;
- blob Git : `3bf31bfd14d5fdd3a3663fef2bc1e26468aab243` ;
- SHA-256 : `4b9ab0f46a508a7f41258dd01385048ae718b037443352d820b27a642b0c2c91`.

Le commit correctif portant exactement ces blobs est :
`715c3e4affa44778785d6c222782eda257ed19e7`.

Les blobs GitHub ont été comparés aux Git-object SHA des fichiers locaux exécutés : identité exacte.

## 2. Exécutions de re-break

Sur les octets locaux identiques aux blobs persistés :

- `python tests/test_ap5_microstructure_price_core.py` : **12/12 PASS** ;
- `python tests/run_ap5_mutation_breakers.py` : **7/7 mutants détectés** ;
- `python -m py_compile tools/ap5_microstructure_price_core.py` : **PASS**.

Mutants tués :
1. moyenne spread non pondérée ;
2. retour traversant un gap ;
3. mauvais dénominateur du range ;
4. inclusion erronée de 16:00 NY ;
5. affectation quintile `side=left` ;
6. bypass de la détection de symlink/reparse dans la chaîne des arguments ;
7. bypass de la détection de symlink/reparse pour un membre AP0 déclaré par le manifest.

Evidence :
`reports/program/evidence/2026-09-25-AP5-MUTATION-RESULTS.json`.

## 3. Défauts trouvés pendant l'audit

### Défaut A — résolution trop précoce des chemins d'arguments

Le premier candidat résolvait certains chemins avec `Path.resolve()` avant le contrôle symlink/reparse. Un alias pouvait donc être déréférencé avant inspection.

Correction :
- ajout de `path_chain_has_reparse_or_symlink()` ;
- contrôle avant résolution pour repo-root, AP0 root, AP0 manifest et parent output ;
- contrôle du chemin AP4 ;
- test dédié ;
- mutant `PATH_CHAIN_BYPASS`.

### Défaut B — même exposition sur les 61 membres AP0 du manifest

Le candidat persisté au commit :
`1acf9667f562b19edbe439d8a7d4a86fca430cff`
contrôlait la cible résolue, mais pas la chaîne lexicale du chemin de chaque fichier AP0 avant résolution.

Cela protégeait les octets via taille + SHA mais ne satisfaisait pas pleinement l'exigence de chemin exact sans alias reparse/symlink.

Correction :
- ajout de `resolve_manifest_member(root, rel)` ;
- rejet de toute chaîne contenant un symlink/reparse avant `resolve()` ;
- conservation du contrôle d'appartenance au root, existence et type fichier ;
- test dédié ;
- mutant `MANIFEST_MEMBER_CHAIN_BYPASS`.

Correction persistée au commit :
`715c3e4affa44778785d6c222782eda257ed19e7`.

## 4. Revue statique de portée

Le helper :
- lit uniquement les colonnes AP0 pré-enregistrées ;
- ne lit aucun champ volume source ;
- re-hashe les 61 fichiers avant et après lecture ;
- exige le manifest AP0 exact ;
- exige l'evidence AP4 exacte par SHA-256 ;
- vérifie schéma, metadata DatasetIdentity, `volumes_used=false` et sémantique mid ;
- exige minute strictement croissante, tick_count positif, segments cohérents, OHLC/spread valides ;
- reconstruit les retours 1m uniquement sur minute exactement contiguë et même segment ;
- réconcilie spread F2/AP1 et range/retour 1m AP2 avant `AP5_COMPLETE` ;
- utilise `America/New_York` avec DST ;
- traite 09:30 inclus et 16:00 exclu pour le proxy cash-clock ;
- conserve les minutes dans les partitions heure/session/année et quintiles ;
- n'exporte aucun signal, PnL, stratégie ou volume source ;
- déclare explicitement la microstructure sub-minute non qualifiée ;
- déclare `causal_deployable=false` en raison des seuils full-sample descriptifs.

## 5. Limites

- Même assistant pour production et audit : aucune indépendance revendiquée.
- Le corpus AP0 n'est pas disponible dans cet environnement ; aucune exécution réelle des 61 Parquet n'est revendiquée ici.
- Les tests portent sur les contrats synthétiques et les breakers ; PyArrow + corpus réel restent à éprouver localement.
- Le proxy 09:30–16:00 est une partition d'horloge NY, pas une vérité de calendrier de marché/holiday.
- `tick_count` est une densité de ticks, jamais un volume traité.
- Les corrélations sont descriptives ; aucune causalité.
- Les quantiles sont full-sample ; aucune utilisation live autorisée.
- Le helper ne prétend pas protéger contre un processus hostile concurrent capable de modifier puis restaurer les fichiers entre contrôles ; les hashes pré/post couvrent la dérive ordinaire, pas une attestation du poste.

## 6. Verdict

**PASS — helper AP5 suffisamment borné et re-breaké pour une tentative locale sur le corpus AP0.**

**BLOCKED — qualification AP5 corpus jusqu'à l'exécution locale et ingestion du JSON exact.**

Aucun AP6, backtest, MT5, PnL ou stratégie n'est ouvert avant adjudication AP5.
