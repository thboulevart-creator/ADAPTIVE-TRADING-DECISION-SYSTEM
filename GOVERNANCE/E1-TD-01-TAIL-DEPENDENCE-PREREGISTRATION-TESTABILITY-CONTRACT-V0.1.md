# E1-TD-01 — TAIL-DEPENDENCE PREREGISTRATION & TESTABILITY CONTRACT V0.1

## 0. STATUS

```text
SCHEMA =
ATDS_E1_TD_01_TAIL_DEPENDENCE_PREREGISTRATION_TESTABILITY_CONTRACT_V0_1

CONTROL_ID = E1-TD-01

STATUS = CANDIDATE_AWAITING_HUMAN_ADOPTION

MODE = DOCUMENTARY / PREREGISTRATION
```

Base documentaire :

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

HEAD =
b2758218d22424555e482e1d6c35029df4333aaa

TREE =
93bd4ac4d2c43f387f03234bc4d1a9d7a85d53ad
```

Source de mémoire :

```text
E1_EXPERIMENTAL_MEMORY_BLOB =
46450fea882f453335fcca7851df9764fc1ddf5c

E1_RESEARCH_QUESTION_ADJUDICATION_BLOB =
5503f50924e64224f949115667e5feabc1098e54
```

---

# 1. AUTHORITY

Cette frontière autorise uniquement :

```text
TAIL_DEPENDENCE_DEFINITION = TRUE
METRIC_DEFINITION = TRUE
DECISION_RULE_DEFINITION = TRUE
FALSIFICATION_RULE_DEFINITION = TRUE
FUTURE_EVIDENCE_REQUIREMENT_DEFINITION = TRUE
```

Elle n’autorise pas :

```text
NEW_DATASET_SELECTION = FALSE
NEW_DATA_OBSERVATION = FALSE
NEW_BACKTEST = FALSE
NEXT_EXPERIMENT_EXECUTION = FALSE

STRATEGY_CHANGE = FALSE
PARAMETER_CHANGE = FALSE
LONG_ONLY = FALSE
SHORT_REMOVAL = FALSE
REGIME_FILTER = FALSE
OPTIMIZATION = FALSE

MT5 = FALSE
PAPER = FALSE
BROKER = FALSE
LIVE = FALSE
CAPITAL = FALSE
```

---

# 2. RESEARCH QUESTION

Question officielle :

> Sur une preuve réellement indépendante, la performance réalisée de MOMENTUM_V1 dépend-elle matériellement d’une très petite fraction de trades gagnants extrêmes, ou une éventuelle espérance positive demeure-t-elle suffisamment distribuée après retrait diagnostique de ces trades extrêmes ?

---

# 3. OPERATIONAL DEFINITION

Dans ce contrat, `TAIL_DEPENDENCE` signifie exclusivement :

> dépendance de la performance réalisée agrégée à une petite fraction des plus gros trades gagnants.

Cette définition ne signifie pas :

```text
COPULA_TAIL_DEPENDENCE
POWER_LAW_CONFIRMED
HEAVY_TAIL_DISTRIBUTION_CONFIRMED
EXTREME_VALUE_MODEL_CONFIRMED
```

Aucun de ces concepts statistiques n’est testé ici.

---

# 4. FROZEN STRATEGY OBJECT

L’objet étudié reste :

```text
STRATEGY = MOMENTUM_V1
TIMEFRAME = H1
LOOKBACK = 20 completed admissible H1 bars

momentum > 0 → LONG
momentum < 0 → SHORT
momentum = 0 → NEUTRAL

same-bar execution = FORBIDDEN
earliest execution = t+1

pyramiding = NONE
stop loss = NONE
take profit = NONE
trailing stop = NONE
break-even = NONE
regime filter = NONE
discretionary override = NONE
parameter optimization = NONE
```

La recherche sur la tail dependence ne peut pas modifier cet objet.

---

# 5. COST SCOPE

Pour isoler la question de recherche, le futur test devra conserver le périmètre E1 :

```text
RAW BID/ASK SPREAD = INCLUDED

COMMISSION = EXCLUDED
COMMISSION_ASSUMED_ZERO = FALSE

SLIPPAGE = EXCLUDED
SLIPPAGE_ASSUMED_ZERO = FALSE

FINANCING = EXCLUDED
FINANCING_ASSUMED_ZERO = FALSE
```

La future expérience ne pourra donc toujours pas produire de claim `BROKER_NET_PNL`.

---

# 6. UNIT OF ANALYSIS

Unité d’analyse :

```text
ONE CLOSED REALIZED TRADE
```

Notations :

```text
n = nombre total de trades clôturés

p_i = realized unit PnL du trade i

P = somme de tous les p_i

E = P / n
```

Les positions encore ouvertes sont exclues :

```text
OPEN_UNREALIZED = EXCLUDED_FROM_TAIL_METRICS
```

Les PnL non finis, manquants ou invalides bloquent l’analyse.

---

# 7. WINNER RANKING

On extrait uniquement les trades :

```text
p_i > 0
```

puis on les classe du plus grand au plus petit :

```text
W1 ≥ W2 ≥ ... ≥ Wm > 0
```

Aucun trade perdant n’est supprimé du diagnostic.

En cas d’égalité parfaite, l’ordre déterministe est :

```text
realized PnL descending
→ exit timestamp ascending
→ entry timestamp ascending
→ original ledger index ascending
```

---

# 8. PRIMARY METRIC — FLIP FRACTION

La métrique principale est :

```text
K_FLIP
```

Définition :

```text
K_FLIP =
plus petit nombre k de trades gagnants,
pris du plus grand au plus petit,
dont le retrait diagnostique rend :

P - SUM(W1...Wk) <= 0
```

Puis :

```text
FLIP_FRACTION = K_FLIP / n
```

Cette métrique répond directement à :

> Quelle fraction minimale des trades suffit à faire disparaître la performance agrégée positive ?

Le retrait est uniquement mathématique.

```text
STRATEGY_TRADE_REMOVAL = FORBIDDEN
```

---

# 9. FIXED CONCENTRATION LEVELS

Deux niveaux sont gelés avant toute nouvelle preuve :

```text
LEVEL_1 = 1 % des trades clôturés
LEVEL_2 = 5 % des trades clôturés
```

Pour chaque niveau :

```text
K_1 = max(1, ceil(0.01 × n))
K_5 = max(1, ceil(0.05 × n))
```

Seuls les plus gros gagnants disponibles sont concernés.

Les métriques suivantes seront calculées :

```text
PNL_AFTER_TOP_1_PERCENT_REMOVAL
EXPECTANCY_AFTER_TOP_1_PERCENT_REMOVAL

PNL_AFTER_TOP_5_PERCENT_REMOVAL
EXPECTANCY_AFTER_TOP_5_PERCENT_REMOVAL
```

---

# 10. SECONDARY DESCRIPTIVE METRICS

Les diagnostics secondaires autorisés sont :

```text
GROSS_PROFIT

TOP_1_PERCENT_SHARE_OF_GROSS_PROFIT
TOP_5_PERCENT_SHARE_OF_GROSS_PROFIT

LARGEST_WINNER
MEDIAN_TRADE_PNL

WIN_COUNT
LOSS_COUNT
WIN_RATE
```

Ils décrivent le mécanisme.

Ils ne peuvent pas remplacer la métrique principale `FLIP_FRACTION` après observation du résultat.

---

# 11. MINIMUM EVIDENCE

Un bloc indépendant ne peut produire une adjudication principale que si :

```text
CLOSED_TRADES >= 100
```

Si :

```text
CLOSED_TRADES < 100
```

alors :

```text
VERDICT = INSUFFICIENT_EVIDENCE
```

La fenêtre de données ne pourra pas être prolongée après observation des PnL dans le seul but d’atteindre 100 trades.

La fenêtre devra être fixée avant exécution.

---

# 12. BLOCK-LEVEL DECISION RULES

## Case A — no positive baseline

Si :

```text
P <= 0
```

alors :

```text
BLOCK_VERDICT =
NO_POSITIVE_EXPECTANCY_OBSERVED
```

La tail dependence d’une espérance positive ne peut pas être revendiquée sur ce bloc.

---

## Case B — strong tail dependence

Si :

```text
P > 0
AND
FLIP_FRACTION <= 0.01
```

alors :

```text
BLOCK_VERDICT =
STRONG_TAIL_DEPENDENCE
```

Interprétation :

1 % ou moins des trades suffit à éliminer la performance positive.

---

## Case C — material tail dependence

Si :

```text
P > 0
AND
0.01 < FLIP_FRACTION <= 0.05
```

alors :

```text
BLOCK_VERDICT =
MATERIAL_TAIL_DEPENDENCE
```

Interprétation :

la performance positive dépend d’au plus 5 % des trades.

---

## Case D — broadly distributed positive expectancy

Si :

```text
P > 0
AND
FLIP_FRACTION > 0.05
```

alors :

```text
BLOCK_VERDICT =
TAIL_DEPENDENCE_NOT_SUPPORTED_ON_THIS_BLOCK
```

Interprétation :

la performance positive ne disparaît pas après retrait diagnostique des 5 % plus gros trades gagnants.

---

# 13. STRUCTURAL CLAIM RULE

Un seul bloc indépendant ne peut jamais autoriser :

```text
STRUCTURAL_TAIL_DEPENDENCE_CONFIRMED
```

Après un seul bloc, le maximum autorisé est :

```text
TAIL_DEPENDENCE_SUPPORTED_ON_THIS_BLOCK
```

Une future revendication structurelle nécessiterait au minimum :

```text
>= 2 independently preregistered evidence blocks
```

avec :

```text
no overlap
no post-result threshold change
same frozen strategy semantics
same frozen metric definitions
```

et une adjudication séparée.

Cette condition ne constitue pas une autorisation de produire deux nouveaux backtests maintenant.

---

# 14. INDEPENDENCE REQUIREMENTS

La preuve future devra être choisie et gelée avant observation de sa performance.

Deux familles d’indépendance pourront ultérieurement être considérées :

```text
TEMPORAL_INDEPENDENCE
or
CROSS_INSTRUMENT_INDEPENDENCE
```

Aucune des deux n’est sélectionnée par ce contrat.

Si `TEMPORAL_INDEPENDENCE` est ultérieurement choisie :

```text
no timestamp overlap with E1 evidence
```

Si `CROSS_INSTRUMENT_INDEPENDENCE` est choisie :

```text
distinct instrument identity
no parameter adaptation from observed performance
```

Le mode d’indépendance devra être fixé avant tout accès aux performances.

---

# 15. E1 CONTAMINATION BOUNDARY

La fenêtre E1 :

```text
2025-05-25T00:00:00Z
→
2026-05-24T23:59:59.963Z
```

reste :

```text
EXPOSED
NON_CONFIRMATORY
```

Elle peut servir à :

```text
historical motivation
debugging
mechanistic explanation
hypothesis generation
```

Elle ne peut pas servir à :

```text
confirm the thresholds
confirm HYPOTHESIS-02
claim independent replication
claim structural tail dependence
```

---

# 16. NO SUBGROUP SHOPPING

La future adjudication primaire doit utiliser :

```text
ALL ADMISSIBLE CLOSED TRADES
```

Il est interdit de sélectionner après résultat :

```text
LONG only
SHORT only
specific year
specific month
specific volatility regime
specific session
specific market regime
specific winning subset
```

pour faire changer le verdict H2.

Ces analyses appartiennent à d’autres hypothèses et nécessitent leurs propres contrats.

---

# 17. NO STRATEGY MODIFICATION

Le diagnostic de retrait des plus gros gagnants ne signifie jamais :

```text
REMOVE_LARGE_WINNERS_FROM_STRATEGY
PROFIT_CAP
WINSORIZE_STRATEGY
CHANGE_EXIT
CHANGE_ENTRY
FILTER_TRADES
```

Ces actions restent interdites.

---

# 18. FALSIFICATION

HYPOTHESIS-02 est falsifiable au niveau d’un bloc indépendant.

Elle n’est pas supportée sur ce bloc lorsque :

```text
P > 0
AND
FLIP_FRACTION > 0.05
```

Elle est supportée sur ce bloc lorsque :

```text
P > 0
AND
FLIP_FRACTION <= 0.05
```

Le niveau de support est :

```text
<= 1 % → STRONG
> 1 % and <= 5 % → MATERIAL
```

Si :

```text
P <= 0
```

le résultat n’est pas transformé artificiellement en réfutation ou confirmation :

```text
NO_POSITIVE_EXPECTANCY_OBSERVED
```

---

# 19. FORBIDDEN CLAIMS

Cette recherche ne pourra à elle seule autoriser :

```text
STRATEGY_QUALIFIED
EDGE_CONFIRMED
ROBUST
CONFIRMATORY_STRATEGY_RESULT
PROFITABLE_STRATEGY
LONG_ONLY_IS_BETTER
SHORTS_SHOULD_BE_REMOVED
REGIME_FILTER_VALIDATED
BROKER_NET_PNL
ALL_IN_COST_PROFITABILITY
LIVE_PROFITABILITY
LIVE_READY
CAPITAL_AUTHORIZED
```

---

# 20. PREREGISTERED BREAKER FAMILIES

Le futur contrat/test devra au minimum pouvoir détecter :

```text
THRESHOLD_CHANGED_AFTER_DATA
TOP_WINNER_RANKING_CORRUPTION
LOSS_REMOVAL
CHERRY_PICKED_SUBGROUP
E1_OOS_REUSED_AS_CONFIRMATION
STRATEGY_MUTATION
COST_SCOPE_MUTATION
OPEN_POSITION_INCLUDED_AS_REALIZED
NONFINITE_PNL
SAMPLE_TOO_SMALL
WINDOW_EXTENDED_AFTER_RESULT
DATA_OVERLAP
METRIC_SUBSTITUTION
STRUCTURAL_CLAIM_FROM_SINGLE_BLOCK
```

---

# 21. EXPECTED TESTABILITY CASES

```text
TD-01  exact research-question identity
TD-02  exact E1 contamination status
TD-03  frozen MOMENTUM_V1 semantics
TD-04  no new dataset encoded in this contract
TD-05  closed-realized-trade unit only
TD-06  n < 100 → INSUFFICIENT_EVIDENCE
TD-07  deterministic winner ranking
TD-08  exact 1 % removal calculation
TD-09  exact 5 % removal calculation
TD-10  exact K_FLIP calculation
TD-11  P <= 0 → NO_POSITIVE_EXPECTANCY_OBSERVED
TD-12  FLIP_FRACTION <= 1 % → STRONG
TD-13  1 % < FLIP_FRACTION <= 5 % → MATERIAL
TD-14  FLIP_FRACTION > 5 % → NOT_SUPPORTED_ON_THIS_BLOCK
TD-15  subgroup cherry-picking blocked
TD-16  strategy mutation blocked
TD-17  overlapping evidence blocked
TD-18  post-observation threshold mutation blocked
TD-19  open unrealized PnL excluded
TD-20  single-block structural claim blocked
```

---

# 22. STOP BOUNDARIES

Stop immediately if the next step requires:

```text
NEW_DATASET_SELECTION
NEW_DATA_OBSERVATION
BACKTEST_EXECUTION
STRATEGY_CHANGE
PARAMETER_CHANGE
REGIME_FILTER
LONG_ONLY
SHORT_REMOVAL
THRESHOLD_CHANGE_AFTER_OBSERVATION
E1_OOS_CONFIRMATORY_REUSE
BROKER / MT5 / PAPER / LIVE / CAPITAL
```

without a new explicit human authorization.

---

# 23. STATE IF ADOPTED

If this contract is humanly adopted:

```text
TAIL_DEPENDENCE_RESEARCH_QUESTION = PREREGISTERED
OPERATIONAL_DEFINITION = FROZEN

PRIMARY_METRIC = FLIP_FRACTION
1_PERCENT_THRESHOLD = FROZEN
5_PERCENT_THRESHOLD = FROZEN
MINIMUM_CLOSED_TRADES = 100

DECISION_RULES = FROZEN
CONTAMINATION_RULES = FROZEN
FORBIDDEN_ANALYSES = FROZEN

NEW_DATASET = NOT_SELECTED
NEW_DATA = NOT_OBSERVED
NEW_BACKTEST = NOT_AUTHORIZED
STRATEGY_CHANGE = NOT_AUTHORIZED
```

Next possible frontier:

```text
INDEPENDENT EVIDENCE
→ ADMISSIBILITY / DATASET SELECTION CONTRACT
```

That frontier would require separate human authorization.

---

# 24. CURRENT STOP

```text
CONTRACT_STATUS = CANDIDATE
HUMAN_ADOPTION = PENDING

GITHUB_PERSISTENCE = NOT_AUTHORIZED
NEW_DATASET = NOT_SELECTED
NEW_EXPERIMENT = NOT_AUTHORIZED

STOP = TRUE
```
