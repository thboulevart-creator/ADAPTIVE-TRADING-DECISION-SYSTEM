# E1 — POST-EXPERIMENT RESEARCH QUESTION ADJUDICATION

## Decision

```text
DECISION = ADOPT
DATE = 2026-09-29

E1_POST_EXPERIMENT_RESEARCH_QUESTION_ADJUDICATION = COMPLETE
SELECTED_RESEARCH_QUESTION = HYPOTHESIS-02 — TAIL DEPENDENCE
```

This decision is documentary only. It does not authorize a new dataset, backtest, strategy mutation, parameter change, optimization or execution.

## Source state

E1 is closed as an exploratory experiment.

The following hypotheses remain part of the E1 experimental memory:

```text
HYPOTHESIS-01 = REGIME DEPENDENCE
HYPOTHESIS-02 = TAIL DEPENDENCE
HYPOTHESIS-03 = DIRECTIONAL ASYMMETRY
HYPOTHESIS-04 = STRUCTURAL USTECH DIRECTIONAL BIAS
HYPOTHESIS-05 = PERIOD-SPECIFIC 2026 EFFECT
```

None is demonstrated by E1.

## Adjudication criteria

The hypotheses were compared according to:

```text
EXPECTED_INFORMATION
CONTAMINATION_RISK
EXPERIMENTAL_COST
FALSIFIABILITY
```

## Selected question

```text
HYPOTHESIS-02 = SELECTED_FOR_FUTURE_PROTOCOL_DESIGN
```

Official research question:

> On genuinely independent evidence, is the realised performance distribution of frozen MOMENTUM_V1 structurally dependent on a small number of extreme winning trades, or is positive expectancy distributed sufficiently broadly that it does not depend on rare outsized winners?

## Rationale

E1 observed on the already exposed/reproduced OOS:

```text
closed trades = 114
realised PnL = +2856.668
largest OOS winner = +3617.517
remaining 113 trades = -760.849
OOS median closed trade < 0
```

Therefore the immediate unresolved question is the mechanism of realised expectancy: whether MOMENTUM_V1 depends structurally on rare large winners.

This question was selected because it is highly informative, can be framed with relatively low contamination risk, is comparatively inexpensive to test, and can be made strongly falsifiable through preregistered concentration diagnostics on genuinely independent evidence.

Selection does not establish that tail dependence exists.

## Other hypotheses

```text
HYPOTHESIS-01 REGIME DEPENDENCE = RETAIN OPEN
HYPOTHESIS-03 DIRECTIONAL ASYMMETRY = RETAIN OPEN
HYPOTHESIS-04 STRUCTURAL USTECH DIRECTIONAL BIAS = RETAIN OPEN
```

HYPOTHESIS-05 PERIOD-SPECIFIC 2026 EFFECT is retained as an observation-driven clue that may overlap with regime dependence. It is not selected as the next standalone question.

## Frozen boundaries

The following remain NOT AUTHORIZED:

```text
LONG_ONLY
SHORT_REMOVAL
PARAMETER_CHANGE
REGIME_FILTER
OPTIMIZATION
PROFIT_CAP
WINSORISATION_AS_STRATEGY_RULE
LARGE-WINNER_REMOVAL
NEW_DATASET_SELECTION
NEW_BACKTEST
NEXT_EXPERIMENT
E2_EXECUTION
E1_RERUN
```

The E1 OOS remains exposed and may be used only as historical motivation, descriptive analysis, debugging or hypothesis generation. It cannot serve as independent confirmation.

## Next frontier

```text
NEXT_FRONTIER =
TAIL-DEPENDENCE RESEARCH QUESTION
→ PREREGISTRATION / TESTABILITY CONTRACT DESIGN
```

That future frontier may define, before observing any independent evidence:

- what counts as tail dependence;
- what diagnostics will be computed;
- what would support or refute the hypothesis;
- what concentration thresholds or invariants are fixed in advance;
- what evidence is admissible;
- what contamination controls apply.

It still does not authorize selection or observation of a new dataset and does not authorize a backtest.

## Final state

```text
E1 = CLOSED
E1_MEMORY = PERSISTED
E1_POST_EXPERIMENT_RESEARCH_QUESTION_ADJUDICATION = COMPLETE

H2_TAIL_DEPENDENCE = SELECTED_FOR_FUTURE_PROTOCOL_DESIGN
H1_REGIME = OPEN
H3_DIRECTIONAL = OPEN
H4_STRUCTURAL_BIAS = OPEN
H5_2026_EFFECT = RETAINED_AS_SUBORDINATE_CLUE

NEXT_DATASET = NOT_SELECTED
NEXT_EXPERIMENT = NOT_AUTHORIZED
NEW_BACKTEST = NOT_AUTHORIZED
STRATEGY_CHANGE = NOT_AUTHORIZED

STOP = TRUE
```
