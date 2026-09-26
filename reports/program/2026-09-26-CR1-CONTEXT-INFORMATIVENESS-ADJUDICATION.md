# CR1 — Context Informativeness — adjudication

Date: 2026-09-26  
Branch: `integration/system-v1`  
Fresh HEAD before persistence: `56bf58171f0556bcaf92bbecfc16c8ef067da167`.

## Exact evidence

- path: `reports/program/evidence/2026-09-26-CR1-CONTEXT-INFORMATIVENESS.json`
- bytes: **49,694**
- SHA-256: `c7aacf73c175c6af49a4866ad62f1d65c0b46b05fa6cd0dd0def4eb5ce87ba3f`
- Git blob: `cd40bf975613d1fa0e6d7277c2850ec87104727e`
- schema: `ATDS_CR1_CONTEXT_INFORMATIVENESS_V0_1`
- status: `CR1_COMPLETE`
- research class: `N0_EXPLORATORY_PREVIOUSLY_EXPOSED_CORPUS`

The uploaded JSON was independently rehashed and its exact bytes were materialized into GitHub.

## Binding / coverage

PASS:
- AP0 files rehashed: 61
- AP0 manifest SHA-256 exact
- Context SHA-256 exact
- registry SHA-256 exact
- CORE Git blob exact
- context_id exact
- minutes: 1,709,180
- source ticks: 376,003,618
- segments: 1,606
- primary folds: F1/F2/F3
- D2026 diagnostic only
- pristine OOS claim = false

## Frozen decision rule

SUPPORTED_N0 requires:
- delta_log_loss > 0 in F1, F2 and F3;
- pooled delta_brier > 0;
- no critical/sparse control failure.

REFUTED_N0 if:
- pooled delta_log_loss <= 0; or
- delta_log_loss <= 0 in at least two primary folds.

All remaining mixed/control-failure cases:
NOT_INTERPRETABLE.

## Adjudication by hypothesis

### CR-H01-NY-HOUR — SUPPORTED_N0

Primary RV15:
- F1 dLL = 0.2775294024199957
- F2 dLL = 0.26826699947310173
- F3 dLL = 0.17423986090619237
- pooled dLL = 0.24005176401092465
- pooled dBrier = 0.08969084678865082
- sparse guard: false

Secondary RV60 is also positive in F1/F2/F3.

Interpretation:
NY hour contains reproducible N0 information about near-future volatility versus the unconditional B0 baseline.

### CR-H02-WEEKDAY — SUPPORTED_N0, SMALL PRIMARY EFFECT

Primary RV15 beyond NY-hour B1:
- F1 dLL = 0.0005726040073839034
- F2 dLL = 0.0023885350518644266
- F3 dLL = 0.0033508232205008426
- pooled dLL = 0.002104441807445786
- pooled dBrier = 0.0011387045233012686

The frozen rule is satisfied.

Important robustness limit:
RV60 dLL is negative in F1 and F2 and positive only in F3. Therefore H02 is admitted by the registered primary rule but should not be treated as a strong multi-horizon result.

### CR-H03-ABS-VOL — SUPPORTED_N0

Primary RV15 beyond B2:
- F1 dLL = 0.2502269722722088
- F2 dLL = 0.26216865516454546
- F3 dLL = 0.2916594218165949
- pooled dLL = 0.2680154633647407
- pooled dBrier = 0.10187720283359873

Secondary RV60 is positive in all primary folds.

Interpretation:
current absolute RV15 state contains reproducible N0 information about future volatility beyond hour+weekday.

### CR-H04-REL-VOL — SUPPORTED_N0

Primary RV15 beyond B2:
- F1 dLL = 0.2789231377160968
- F2 dLL = 0.2869935651306814
- F3 dLL = 0.2954911633488768
- pooled dLL = 0.28713816384475954
- pooled dBrier = 0.1226916188155511

Secondary RV60 is positive in all primary folds.

Interpretation:
hour-relative current RV15 state contains reproducible N0 information beyond hour+weekday.

No ranking between H03 and H04 is authorized by CR1.

### CR-H05-SPREAD — NOT_INTERPRETABLE

Primary SPREAD15 scores are positive:
- F1 dLL = 0.5234476930516094
- F2 dLL = 0.8434531316376631
- F3 dLL = 0.9967953073196434
- pooled dLL = 0.7880069039386851
- pooled dBrier = 0.42184722733643515

However F2 test-state 1 contains only **21** observations, below the preregistered floor of 100.

The sparse guard therefore triggers.

This hypothesis is **not promoted**, despite large positive scores.

Secondary SPREAD60 has the same sparse F2 state.

### CR-H06-TICK-DENSITY — SUPPORTED_N0

Primary TICK15 beyond B2:
- F1 dLL = 0.42268992133531036
- F2 dLL = 0.8243448805352295
- F3 dLL = 0.4019594068361636
- pooled dLL = 0.5500694985468306
- pooled dBrier = 0.2423917969252228
- sparse guard: false

Secondary TICK60 is positive in F1/F2/F3.

Interpretation:
recent relative tick-density state contains reproducible N0 information about future activity beyond hour+weekday.

tick_count remains activity density, not traded volume.

### CR-H07-GAP-REOPEN — REFUTED_N0

Primary RV15 beyond B2:
- F1 dLL = -0.0025978590081998654
- F2 dLL = -0.0014121290223163552
- F3 dLL = -0.002520932667611664
- pooled dLL = -0.002175858309524977
- pooled dBrier = -0.0008832696091270033

Secondary RV60 is also negative in all primary folds.

The preregistered SPREAD15 diagnostic is not a rescue:
F1/F2 dLL are negative, F3 positive only.

Verdict remains REFUTED_N0.

### CR-H08-EFFICIENCY — REFUTED_N0

Primary EFF15 beyond B2:
- F1 dLL = -0.0011970807520653715
- F2 dLL = -0.0009122010760627131
- F3 dLL = -0.0006607682561488026
- pooled dLL = -0.0009232544186902744
- pooled dBrier = -0.00036476117769722007

Secondary EFF60 is also negative in all primary folds.

Verdict: REFUTED_N0.

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
- regime_labels_instantiated = false
- mt5_used = false
- pristine_oos_claim = false

## CR2 admission set

Under the frozen CR2 admission rule, only SUPPORTED_N0 axes may enter a future synthesis preflight:

- CR-H01-NY-HOUR
- CR-H02-WEEKDAY
- CR-H03-ABS-VOL
- CR-H04-REL-VOL
- CR-H06-TICK-DENSITY

Excluded:
- CR-H05-SPREAD — unresolved / NOT_INTERPRETABLE
- CR-H07-GAP-REOPEN — REFUTED_N0
- CR-H08-EFFICIENCY — REFUTED_N0

Admission does not mean mandatory inclusion and does not authorize combinatorial search.

## Epistemic limit

CR1 used a previously exposed corpus.

Therefore:
**no VALIDATED/CONFIRMED/OOS regime claim is authorized.**

SUPPORTED_N0 means reproducible exploratory information under this preregistered chronological protocol only.

## Verdict

**PASS — CR1 CONTEXT INFORMATIVENESS COMPLETE.**

Five hypotheses are SUPPORTED_N0.
Two are REFUTED_N0.
One is NOT_INTERPRETABLE.

The next permissible frontier is a bounded **CR2 REGIME-CANDIDATE SYNTHESIS PREFLIGHT** using only the admitted axes and no outcome-driven combination search.
