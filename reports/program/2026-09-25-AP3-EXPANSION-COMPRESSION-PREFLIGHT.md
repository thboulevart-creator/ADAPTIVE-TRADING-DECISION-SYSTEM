# AP3 — EXPANSION / COMPRESSION — preflight

Date : 2026-09-25

## 1. Entrées

DatasetIdentity :
`USTECH_PROFILE_MINUTE_CORE_V0_1`.

Bindings :
- AP0 manifest SHA-256 :
  `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`;
- AP2 JSON SHA-256 :
  `4e3c79a5b9c8131f62a8fb7f205712d8a5c4301ff01b7fd3ce7226d8799d9c9f`.

AP2 est PASS et lie déjà AP1 exact.

Chaque Parquet AP0 sera re-hashé contre le manifest.

## 2. Objet

Décrire les phases de volatilité sans transformer une observation en stratégie.

AP3 doit distinguer :
1. **ABSOLUTE VOLATILITY STATE** ;
2. **INTRADAY-NORMALIZED VOLATILITY STATE**.

La seconde lentille évite de confondre la saisonnalité normale de l'heure avec une expansion/compression inhabituelle.

## 3. Mesure de base

Mesure primaire :
`RV15_BPS`

exactement définie comme AP2 :
`sqrt(sum(valid 1m log returns^2 over last 15 transitions))*10000`.

Validité :
- même segment ;
- 15 transitions 1m toutes valides ;
- continuité exacte minute par minute.

AP3 doit reconstruire les agrégats RV15 AP2 à tolérance 1e-9 avant toute classification.

Mesure secondaire :
`VARIANCE_SHARE_15_OF_60 = RV15^2 / RV60^2`.

Interprétation descriptive :
fraction de la variance réalisée 60m concentrée dans les 15 dernières minutes.

Valeur attendue dans [0,1] lorsque RV60 >0.

## 4. Lentille absolue

Sur toutes les RV15 valides :
- threshold compression = percentile 20 ;
- threshold expansion = percentile 80.

États :
- COMPRESSION : RV15 <= p20 ;
- NORMAL : p20 < RV15 < p80 ;
- EXPANSION : RV15 >= p80.

Les seuils p20/p80 sont fixés avant calcul et ne dépendent d'aucun PnL.

## 5. Lentille intraday-normalisée

Pour chaque heure America/New_York :
- calculer la médiane descriptive de RV15.

Pour chaque observation valide :
`NORMALIZED_RV15 = RV15 / median_RV15_of_same_NY_hour`.

Puis sur toutes les valeurs normalisées valides :
- compression <= p20 ;
- normal entre p20 et p80 ;
- expansion >= p80.

Cela retire une partie de la saisonnalité intraday attendue sans prétendre supprimer tous les effets temporels.

## 6. Limitation causale explicite

Les médianes horaires et quantiles p20/p80 sont calculés sur le **corpus complet**.

Donc :
- AP3 est une description ex post du comportement ;
- les labels AP3 NE SONT PAS autorisés comme feature temps-réel ou signal ;
- `causal_deployable=false`.

Une éventuelle version causale devra utiliser uniquement une distribution disponible avant t sous contrat séparé.

## 7. Phases

Pour chaque lentille :
- une phase = suite de minutes consécutives, même segment, même état ;
- invalid RV15 coupe une phase ;
- gap/segment change coupe une phase.

Mesurer par état :
- share des observations ;
- nombre de phases ;
- durée moyenne ;
- p50/p90/p99 ;
- durée max.

## 8. Transitions

Transitions directes uniquement entre minutes :
- consécutives exactement 60s ;
- même segment ;
- état valide aux deux endpoints.

Matrice 3x3 :
COMPRESSION / NORMAL / EXPANSION.

Conserver :
- counts ;
- probabilités conditionnelles par état source.

Aucune transition future n'est utilisée comme label prédictif.

## 9. Dimensions de stabilité minimale

Pour la lentille intraday-normalisée :
- shares par UTC year 2021..2026 ;
- 2021 et 2026 marquées partielles.

AP6 reste responsable de la stabilité complète.

## 10. Variance concentration

Pour `VARIANCE_SHARE_15_OF_60` :
- global count/mean/p50/p90/p99 ;
- mêmes statistiques par état intraday-normalisé.

Aucune interprétation de direction du prix.

## 11. Colonnes AP0

Lecture :
- minute_start_ms_utc ;
- segment_id ;
- mid_close.

Aucun volume.
Aucun spread.
Aucun prix d'exécution.

## 12. Intégrité

BLOCKED si :
- AP0/AP2 bindings différents ;
- hash d'un Parquet AP0 différent ;
- ordre minute non strict ;
- segment jump >1 ;
- mid_close non finite/<=0 ;
- reconstruction RV15/RV60 AP2 échoue ;
- variance share >1 au-delà de tolérance numérique ;
- conservation des counts impossible.

## 13. Ressources

Input AP0 :
~91,7 MiB.

Lecture de 3 colonnes sur 1,709M lignes.
Mémoire cible <1 GiB.

Output JSON <=32 MiB.

## 14. Interdictions

- aucun signal ;
- aucun PnL ;
- aucun Sharpe/Profit Factor ;
- aucune optimisation ;
- aucune sélection de seuil par résultat futur ;
- aucune direction long/short ;
- aucun backtest/MT5.

## Verdict

**PASS — preflight AP3 autorise la matérialisation du helper candidat.**
