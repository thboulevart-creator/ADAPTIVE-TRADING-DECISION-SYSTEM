# CR2 — REGIME-CANDIDATE SYNTHESIS — PREFLIGHT V0.1

Date: 2026-09-26  
Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`  
Fresh HEAD before persistence: `8ba1f75d40e021d469481de3e061c07bed88fcd9`.

## 1. Purpose

CR1 is complete.

CR1 established five SUPPORTED_N0 axes:
- NY hour;
- NY weekday;
- absolute RV15 state;
- hour-relative RV15 state;
- relative tick-density state.

CR2 asks a narrower question:

> **Does a fixed joint dynamic state built from volatility + activity carry reproducible information about the next market-environment distribution beyond either constituent axis alone, after conditioning on hour+weekday?**

CR2 is still N0 exploratory.

It does not create a validated regime and does not test trading performance.

## 2. Why only two candidate families

H03 absolute volatility and H04 hour-relative volatility are two alternative representations of the same broad volatility dimension.

They must not be blindly multiplied together.

Therefore exactly two candidate families are preregistered:

### C01 — ABS_VOL × TICK
3 absolute-volatility states × 3 relative tick-density states = 9 joint states.

### C02 — REL_VOL × TICK
3 hour-relative-volatility states × 3 relative tick-density states = 9 joint states.

No third family is authorized.

No outcome-driven choice between C01 and C02 is authorized.

## 3. Calendar backbone

NY hour + NY weekday remain the B2 conditioning backbone.

They are **not** multiplied into the regime-state identity.

This avoids a 24×7×3×3 Cartesian explosion and keeps the candidate dynamic-state space fixed at nine cells.

## 4. Excluded CR1 axes

CR-H05 SPREAD:
NOT_INTERPRETABLE because of sparse F2 state count = 21.

CR-H07 GAP/REOPEN:
REFUTED_N0.

CR-H08 EFFICIENCY:
REFUTED_N0.

These axes cannot enter CR2 V0.1.

## 5. Candidate state identity

Each candidate family has exactly nine neutral state IDs:

`V0T0, V0T1, V0T2, V1T0, V1T1, V1T2, V2T0, V2T1, V2T2`.

No semantic label such as:
- trend;
- range;
- breakout;
- stress;
- calm;
- risk-on;
- risk-off

may be assigned during CR2.

The states are purely categorical joint context bins.

## 6. Causal construction

At observation time `t`:
- all context information must be timestamped <= t;
- dynamic-state thresholds are learned on the training fold only;
- the target begins at t+1;
- no target may cross a missing minute or segment boundary;
- no test-fold threshold refit is allowed.

CR1 definitions are reused:
- absolute RV15 state;
- hour-relative RV15 state;
- hour-relative trailing tick5 state.

No lookback/threshold alteration is permitted.

## 7. Joint future-environment target

Primary horizon:
15 minutes.

Two future variables:
- RV15;
- TICK15.

For each fold:
1. learn RV15 quintile thresholds from train only;
2. learn TICK15 quintile thresholds from train only;
3. freeze both into test;
4. combine them into a 5×5 = **25-class joint target**.

This tests a market-environment distribution rather than direction/PnL.

Secondary robustness:
same construction at 60 minutes.

The secondary horizon cannot rescue a failed primary result.

## 8. Fixed comparisons

Each candidate must beat **both** of its registered constituent baselines.

### C01 comparisons
1. C01 joint state vs B2 + ABS_VOL_STATE
2. C01 joint state vs B2 + TICK_STATE

### C02 comparisons
1. C02 joint state vs B2 + REL_VOL_STATE
2. C02 joint state vs B2 + TICK_STATE

This asks whether the joint state contains information not already explained by either constituent alone.

No "best baseline" selection is performed after results.

## 9. Folds

Primary:
- F1 → 2023 test
- F2 → 2024 test
- F3 → 2025 test

Diagnostic only:
- D2026 → partial 2026

All remain previously exposed N0 data.

No pristine OOS claim.

## 10. Scoring

Empirical categorical probability models with fixed Laplace alpha = 1.

Primary:

`delta_log_loss = constituent_baseline_log_loss - joint_candidate_log_loss`

Secondary:

`delta_brier = constituent_baseline_brier - joint_candidate_brier`

Positive means the fixed joint state improves descriptive probability relative to that constituent baseline.

## 11. Sparse guard

Each of the nine joint candidate states must have at least **500 valid test observations in every primary fold**.

If any state falls below 500:
candidate status = NOT_INTERPRETABLE.

500 is preregistered before CR2 calculation and is not tunable after results.

## 12. Scientific decision rule

### SUPPORTED_N0_SYNTHESIS

Only if, for **both required comparisons**:
- dLL > 0 in F1;
- dLL > 0 in F2;
- dLL > 0 in F3;
- pooled dBrier > 0;
- sparse/control guards PASS.

### REFUTED_N0_SYNTHESIS

If, for **either required comparison**:
- pooled dLL <= 0; or
- dLL <= 0 in at least two primary folds.

### NOT_INTERPRETABLE

All remaining mixed/control/sparse cases.

No candidate can be promoted because it merely has a large pooled score.

## 13. No winner selection

C01 and C02 are parallel preregistered hypotheses.

CR2 V0.1 explicitly forbids:
- ranking them;
- choosing whichever scores higher;
- deleting one after seeing results;
- averaging them into a new candidate;
- adding H05/H07/H08;
- changing bins;
- searching additional interactions.

Possible outcomes include:
- both supported;
- one supported and one refuted;
- both refuted;
- one/both not interpretable.

All are valid scientific outcomes.

## 14. Relationship to future regime labels

Even a SUPPORTED_N0_SYNTHESIS result only means:

> a fixed joint dynamic state carries reproducible exploratory information about a future environment distribution beyond each constituent axis alone.

It does **not** mean:
- a market regime has been validated;
- the state is tradable;
- the state predicts direction;
- the state has economic value.

Semantic regime naming and expert specialization remain forbidden.

## 15. Confirmatory boundary

Any later non-N0 regime claim requires:
- a frozen confirmatory Charter;
- new/pristine data;
- exact causal reconstruction;
- preregistered falsification;
- negative-result retention.

The current corpus cannot supply that confirmation.

## 16. Required implementation breakers

At minimum:
1. target starts at t rather than t+1;
2. gap/segment crossing;
3. test thresholds leak into train state construction;
4. RV/TICK target quintiles refit on test;
5. C01 accidentally uses REL_VOL;
6. C02 accidentally uses ABS_VOL;
7. H03 and H04 combined into one family;
8. hour/weekday multiplied into dynamic state ID;
9. one constituent comparison omitted;
10. weaker constituent baseline substituted after results;
11. sparse joint state allowed to SUPPORT;
12. D2026 changes primary status;
13. C01/C02 winner selected;
14. forbidden H05/H07/H08 axis injected;
15. semantic regime label injected;
16. PnL/direction/signal target introduced;
17. candidate omitted from output;
18. 60m secondary result rescues failed 15m primary.

## 17. Machine-readable registry

Frozen registry:
`reports/program/evidence/2026-09-26-CR2-CANDIDATE-REGISTRY-V0.1.json`

A candidate family not present in that registry is outside CR2 V0.1.

## Verdict

**PASS — CR2 REGIME-CANDIDATE SYNTHESIS PREFLIGHT V0.1.**

Meaning:
- exactly two bounded candidate families are defined;
- no synthesis calculation has occurred;
- no candidate regime exists yet;
- no strategy research is authorized.

### Next governed action

Materialize CR2 synthesis helper + synthetic/adversarial tests only.

Do not execute the corpus until persisted-head re-break passes.
