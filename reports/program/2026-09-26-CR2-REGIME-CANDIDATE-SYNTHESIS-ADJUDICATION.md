# CR2 — Regime-Candidate Synthesis — adjudication

Date: 2026-09-26  
Branch: `integration/system-v1`  
Fresh HEAD before persistence: `637fabd57e1fd15199c8eee37c13ed46a9eed9ef`.

## Exact evidence

- path: `reports/program/evidence/2026-09-26-CR2-REGIME-CANDIDATE-SYNTHESIS.json`
- bytes: **32,243**
- SHA-256: `5c05e9e8d965314f4a6852aa71f442f89a0962133edc79873cf610682f34c501`
- Git blob: `d6543d12fc01405fedb006ddb5d714a772f32678`
- schema: `ATDS_CR2_REGIME_CANDIDATE_SYNTHESIS_V0_1`
- status: `CR2_COMPLETE`
- research class: `N0_EXPLORATORY_PREVIOUSLY_EXPOSED_CORPUS`

The uploaded JSON was independently rehashed and its exact bytes were materialized into GitHub.

## Coverage / bindings

PASS:
- AP0 files rehashed: 61
- AP0 manifest SHA-256 exact
- CR1 helper blob exact
- CR1 evidence blob exact
- CR2 registry blob exact
- context_id exact
- minutes: 1,709,180
- source ticks: 376,003,618
- segments: 1,606
- primary folds: F1/F2/F3
- D2026 diagnostic only
- pristine OOS = false

## Frozen CR2 decision rule

A candidate is `SUPPORTED_N0_SYNTHESIS` only if:
- for both constituent comparisons, dLL > 0 in F1, F2 and F3;
- for both comparisons, pooled dBrier > 0;
- no primary-fold joint state has fewer than 500 observations.

A candidate is `REFUTED_N0_SYNTHESIS` if, for either required comparison:
- pooled dLL <= 0; or
- dLL <= 0 in at least two primary folds.

All remaining mixed/sparse/control cases are `NOT_INTERPRETABLE`.

## CR2-C01-ABS_VOL_X_TICK

Status: **SUPPORTED_N0_SYNTHESIS**

Sparse guard:
- F1: PASS
- F2: PASS
- F3: PASS
- overall primary sparse guard: false

Primary 15m, vs TICK constituent:
- F1 dLL = 0.0753495114418481
- F2 dLL = 0.14083046325367876
- F3 dLL = 0.11535510281365902
- pooled dLL = 0.11056396074976749
- pooled dBrier = 0.02194639801497622
- pooled n = 996,920

Primary 15m, vs ABS_VOL constituent:
- F1 dLL = 0.2168747512832856
- F2 dLL = 0.6821687321422925
- F3 dLL = 0.19730198549328315
- pooled dLL = 0.36593043148676285
- pooled dBrier = 0.08215720862168718
- pooled n = 996,920

All registered primary comparisons are positive in all three primary folds.

The smallest F2 joint-state count is 623, still above the preregistered 500 floor.

Secondary 60m remains positive on both constituent comparisons:
- pooled vs TICK dLL = 0.11728622405587763
- pooled vs TICK dBrier = 0.02096990795418452
- pooled vs ABS_VOL dLL = 0.33366715189967766
- pooled vs ABS_VOL dBrier = 0.07104367999346206

D2026 is diagnostic only and contains a sparse state (state 6, n=229); by contract this does not alter the primary F1–F3 status.

Interpretation:
the fixed 3×3 joint state `ABS_VOL × TICK`, conditioned on the B2 hour+weekday backbone, contains reproducible N0 information about the 25-class future RV15×TICK15 environment beyond either constituent state alone.

This is not a trading-value, causal, directional, or validated-regime claim.

## CR2-C02-REL_VOL_X_TICK

Status: **NOT_INTERPRETABLE**

The score direction is positive:

Primary 15m, vs TICK:
- F1 dLL = 0.06345039131290298
- F2 dLL = 0.12553951625960824
- F3 dLL = 0.1204649577621284
- pooled dLL = 0.1031942410994029
- pooled dBrier = 0.02833746080502464

Primary 15m, vs REL_VOL:
- F1 dLL = 0.17143046955985564
- F2 dLL = 0.6293241983996927
- F3 dLL = 0.1909694134552542
- pooled dLL = 0.3310348555328766
- pooled dBrier = 0.06746003016442648

However F2 joint state 2 contains only **53** test observations.

The preregistered sparse minimum is 500.

Therefore:
**C02 remains NOT_INTERPRETABLE.**

Its positive scores cannot override the sparse guard.

D2026 also has a sparse state (state 6, n=78), but D2026 is diagnostic only.

Secondary 60m is positive on both comparisons, but secondary results cannot rescue a sparse/failed primary status.

## No winner selection

CR2 V0.1 forbids ranking C01 against C02.

Therefore this adjudication does not call C01 "better".

It records:
- C01 independently satisfies its preregistered support rule;
- C02 independently fails interpretability because of sparse primary support.

## Scope verification

PASS:
- strategy_agnostic = true
- direction_target_used = false
- pnl_calculated = false
- trades_calculated = false
- signals_calculated = false
- optimization = false
- threshold_search = false
- feature_search = false
- interaction_search = false
- winner_selection = false
- semantic_regime_labels_instantiated = false
- mt5_used = false
- pristine_oos_claim = false

## Epistemic limit

CR2 used a previously exposed corpus.

Therefore:
- C01 is an **N0 regime-candidate synthesis**, not a validated regime;
- no semantic regime label is authorized;
- no expert specialization is authorized;
- no strategy/PnL research is authorized from this evidence alone.

## Verdict

**PASS — CR2 REGIME-CANDIDATE SYNTHESIS COMPLETE.**

Results:
- C01 ABS_VOL × TICK: `SUPPORTED_N0_SYNTHESIS`
- C02 REL_VOL × TICK: `NOT_INTERPRETABLE`

The next permissible frontier is a **confirmatory Charter for C01 on genuinely new/pristine data**.
