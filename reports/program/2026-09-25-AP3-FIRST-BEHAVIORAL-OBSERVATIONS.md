# AP3 — premières observations comportementales
Date : 2026-09-25
Type : DESCRIPTION / OBSERVATION ex post.
DatasetIdentity : USTECH_PROFILE_MINUTE_CORE_V0_1, dérivé de SOURCE_B_USTECH_PRICE_CORE_V0_1.
Preuve : reports/program/evidence/2026-09-25-AP3-EXPANSION-COMPRESSION.json.
SHA-256 : caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef.
Période : 2021-05-25 → 2026-05-24, discontinue ; prix mid descriptifs.
Méthode : preflight AP3 et helper blob 8a7aa643eb6e4414dad378ca4ddb8b98adce7bd1.

1. Seuils absolus RV15 : compression <=4.038130426072135 bps ; expansion >=15.018274772834737 bps.
2. Après division par la médiane RV15 de la même heure NY : compression <=0.6304316352021648 ; expansion >=1.6569597384304056. Les parts 20/60/20 résultent de cette définition.
3. Les différences annuelles restent importantes après normalisation horaire. Part d'expansion : 2021 partiel 9.43 %, 2022 48.48 %, 2023 9.62 %, 2024 8.64 %, 2025 18.18 %, 2026 partiel 23.76 %. AP6 doit qualifier leur stabilité ; aucune explication causale testée.
4. Phases absolues : médianes compression 5 min, normal 11 min, expansion 11 min ; moyennes 18.54, 30.54, 23.20 min. Les queues longues influencent les moyennes.
5. Phases normalisées : médianes 5/11/9 min ; durées limitées par les frontières horaires. Ce ne sont pas des durées de régimes naturels.
6. Part des 15 dernières minutes dans la variance 60m : moyenne 25.8766 %, médiane 23.0155 %, p99 73.9552 %. Moyennes par état normalisé : compression 18.5543 %, normal 25.6195 %, expansion 33.9841 %. Association partiellement mécanique (RV15 partagé), pas une prédiction.

Limites : seuils et baselines full-sample, causal_deployable=false ; fenêtres chevauchantes ; pas d'échantillons indépendants revendiqués ; pas de mesure directionnelle ; aucun edge ni PnL ; aucune conclusion de stabilité avant AP6.
Hypothèse candidate : la normalisation horaire seule ne suffit pas à rendre la distribution invariante entre années. Cette observation appelle AP6, pas une optimisation AP3.
