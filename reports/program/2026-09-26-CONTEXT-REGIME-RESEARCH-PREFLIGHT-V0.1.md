# CONTEXT / REGIME RESEARCH — PREFLIGHT V0.1

Date : 2026-09-26  
Repository : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch : `integration/system-v1`  
Fresh HEAD before persistence : `23ff3c93356ce93c2a1dbe74ec192d948a78050e`.

## 1. Purpose

The Asset Behavioral Profile CORE V0.1 is closed/PASS.

This preflight opens the next frontier without jumping to strategy research.

The immediate question is:

> **Which context variables contain reproducible information about the subsequent market environment, beyond already-known calendar structure, without selecting variables because they later produce attractive trading performance?**

The first research layer is therefore **context informativeness**, not regime naming and not expert performance.

No research calculation is executed by this preflight.

## 2. Existing contracts preserved

This preflight does not replace:
- `docs/03-REGIME-EXPERT-RESEARCH-FOUNDATION.md`;
- `GOVERNANCE/STEP-3-CONTEXT-RESEARCH-CONTRACT-GATE.md`;
- `docs/D1.3-RESEARCH-CHARTER.md`;
- `docs/RESEARCH-FINDINGS-CONTRACT.md`;
- the adopted EXPLORATORY OFFLINE RESEARCH V0 boundary.

The older foundation's conceptual labels:
- TENDANCE
- RANGE
- BREAKOUT
- STRESS

remain **hypotheses/categories for later research**, not facts inherited by this preflight.

No label is allowed to become a regime merely because its name sounds economically plausible.

## 3. Epistemic status — N0 only

The 2021–2026 corpus has already been inspected extensively during AP0→AP6.

Therefore:

**no period inside this corpus may now be described as pristine or independent OOS evidence.**

Chronological train→test separation is still useful for anti-overfit diagnostics, but it remains:

`N0 / EXPLORATORY / PREVIOUSLY EXPOSED CORPUS`.

A future confirmatory claim requires:
- a frozen research Charter before calculation; and
- genuinely new or otherwise pristine data not previously used to modify the research design.

This distinction is mandatory.

## 4. Why context axes are allowed into CR1

Only axes supported by the CORE are admitted.

### C1 — New York hour
CORE basis:
the relative intraday ordering of range/RV/activity is highly persistent.

### C2 — New York weekday
CORE basis:
weekday ordering is temporally persistent for volatility/activity.

### C3 — absolute volatility state
CORE basis:
absolute volatility level is materially nonstationary; current state may therefore matter.

### C4 — hour-relative volatility state
CORE basis:
hour explains a large structural component, but hour normalization alone did not remove inter-year variation.

### C5 — spread state
CORE basis:
spread has intraday structure and material temporal drift.

### C6 — tick-density state
CORE basis:
activity has strong intraday structure and temporal level drift.

### C7 — gap/reopen state
CORE basis:
1,605 discontinuity/reopen boundaries are material and downstream research must not bridge them silently.

### C8 — efficiency state
CORE basis:
efficiency15/60 distribution levels are comparatively stable and may describe path geometry.

Calendar month is excluded from CR1 because AP6 did not support stable month ordering.

## 5. Causal information cutoff

For an observation time `t`:

`CONTEXT(t)` may use only information timestamped `<= t`.

The target begins strictly after the context cutoff:

`FORWARD TARGET = t+1 ... t+H`.

A context variable cannot use:
- the target window;
- future extrema;
- future reentry labels;
- full-fold statistics;
- thresholds learned on the test fold.

All rolling context metrics end at `t`.

All forward targets require exact one-minute continuity and same-segment continuity.

Any gap or segment boundary invalidates the affected target; it is never filled.

## 6. Forward environment targets

The first layer deliberately excludes signed directional return and all economic performance.

### Primary horizon
15 minutes.

Primary descriptive targets:
1. forward RV15 bps;
2. forward efficiency15;
3. forward mean spread over next 15 minutes;
4. forward mean tick density over next 15 minutes.

### Secondary robustness horizon
60 minutes:
- forward RV60;
- forward efficiency60;
- forward spread mean60;
- forward tick density60.

The 60-minute results cannot rescue a failed primary 15-minute hypothesis.

No target is:
- PnL;
- expectancy;
- trade return;
- drawdown;
- Sharpe;
- hit rate of a strategy.

## 7. Fixed chronological folds

### F1
Train: 2021-05-25 → 2022-12-31  
Test: 2023 calendar year.

### F2
Train: through 2023-12-31  
Test: 2024 calendar year.

### F3
Train: through 2024-12-31  
Test: 2025 calendar year.

### D2026
Train: through 2025-12-31  
Test: 2026-01-01 → 2026-05-24.

D2026 is **partial diagnostic only** and cannot change the F1–F3 status rule.

Because all periods have already been viewed during asset profiling, none is labelled pristine OOS.

## 8. Baselines

### B0 — unconditional
Training-fold unconditional target distribution.

### B1 — time baseline
Training-fold target distribution conditioned on NY hour.

### B2 — calendar baseline
Training-fold target distribution conditioned on NY hour + NY weekday.

This hierarchy prevents a variable such as volatility, spread or activity from receiving credit merely for rediscovering the already-qualified intraday/weekday structure.

## 9. Context definitions frozen before results

### CR-H01 — NY_HOUR
Known `America/New_York` hour at t.

Baseline: B0.  
Primary target: forward RV15.

### CR-H02 — NY_WEEKDAY
Known New York weekday at t.

Baseline: B1.  
Primary target: forward RV15.

### CR-H03 — BACKWARD_RV15_ABSOLUTE_STATE
RV15 ending at t.

LOW / MID / HIGH thresholds:
training-fold tertiles only.

Baseline: B2.  
Primary target: forward RV15.

### CR-H04 — BACKWARD_RV15_HOUR_RELATIVE_STATE
RV15 ending at t divided by the **training-only median RV15 for the same NY hour**.

LOW / MID / HIGH:
training-fold tertiles.

Baseline: B2.  
Primary target: forward RV15.

### CR-H05 — BACKWARD_SPREAD5_HOUR_RELATIVE_STATE
Mean spread over `t-4..t`, divided by training-only same-hour median.

LOW / MID / HIGH:
training tertiles.

Baseline: B2.  
Primary target: forward spread mean15.

### CR-H06 — BACKWARD_TICK5_HOUR_RELATIVE_STATE
Mean tick_count over `t-4..t`, divided by training-only same-hour median.

LOW / MID / HIGH:
training tertiles.

Baseline: B2.  
Primary target: forward tick density15.

`tick_count` remains activity density, not traded volume.

### CR-H07 — MINUTES_SINCE_SEGMENT_START_STATE

Fixed categories:
- REOPEN = 0;
- EARLY = 1..15;
- POST = 16..60;
- MATURE >60.

No threshold learning.

Baseline: B2.  
Primary target: forward RV15.  
Co-primary descriptive diagnostic: forward spread mean15.

### CR-H08 — BACKWARD_EFFICIENCY15_STATE
Efficiency15 ending at t.

LOW / MID / HIGH:
training-fold tertiles.

Baseline: B2.  
Primary target: forward efficiency15.

## 10. No bin optimisation

For every continuous candidate:
- exactly three context states: LOW/MID/HIGH;
- thresholds = training-only tertiles;
- no quartile/quintile/decile comparison;
- no search for "best threshold";
- no target-aware threshold adjustment.

The tertile choice is an interpretability/budget rule, not a claim that three states are naturally correct.

## 11. Target discretisation for information scoring

For each fold and each target:

1. use training data only;
2. compute target quintile thresholds on training data;
3. freeze those thresholds;
4. map train and test outcomes to the same five target classes.

No test-fold quantile recalibration is allowed.

This produces a fixed categorical environment outcome without introducing trade direction or PnL.

## 12. Information scoring

A candidate context is compared against its registered baseline using simple empirical categorical probabilities learned on the train fold.

Fixed smoothing:
Laplace/add-one smoothing.

Primary score:

`delta_log_loss = baseline_log_loss - candidate_log_loss`

Positive means the candidate gives a better out-of-fold probabilistic description of the target than its baseline.

Secondary score:

`delta_brier = baseline_brier - candidate_brier`

Positive is better.

All scores are reported for every fold and every preregistered hypothesis.

No "best candidate" ranking is authorized in CR1.

## 13. Scientific status rule — frozen before computation

For each primary hypothesis:

### SUPPORTED_N0
Only if:
- `delta_log_loss > 0` in F1;
- `delta_log_loss > 0` in F2;
- `delta_log_loss > 0` in F3;
- pooled chronological `delta_brier > 0`;
- all critical controls PASS.

### REFUTED_N0
If:
- pooled chronological `delta_log_loss <= 0`; or
- `delta_log_loss <= 0` in at least 2 of F1/F2/F3.

### NOT_INTERPRETABLE
If:
- neither rule above applies;
- required context cells are too sparse;
- continuity/provenance/control fails;
- a fold cannot be validly evaluated.

A tiny positive effect can satisfy SUPPORTED_N0, but it must be reported with its exact magnitude.

Therefore `SUPPORTED_N0` means **reproducible information under this exploratory protocol**, not material economic value.

## 14. Sample-size guard

Every reported conditional cell must expose:
- train count;
- test count.

A context category with fewer than 100 valid test targets in a fold is marked sparse for that fold.

A primary hypothesis cannot be SUPPORTED_N0 if the state responsible for the apparent information is sparse in any required fold.

This count is a quality floor, not an optimisation parameter.

## 15. Anti-selection controls

CR1 forbids:

1. testing extra indicators after seeing results;
2. changing tertiles to quartiles/quintiles;
3. changing lookbacks after results;
4. creating feature interactions after results;
5. retaining only successful context axes;
6. deleting failed folds;
7. using D2026 to rewrite F1–F3 hypotheses;
8. changing the primary target after results;
9. reporting only pooled results;
10. ranking candidates and selecting a winner;
11. measuring any PnL;
12. naming a context state TENDANCE/RANGE/BREAKOUT/STRESS because its outcome "looks like" such a regime.

All eight preregistered hypotheses must be persisted, including REFUTED and NOT_INTERPRETABLE outcomes.

## 16. Why this does not manufacture an edge

The CR1 question is not:

> "Which segmentation makes money?"

It is:

> **"Does information available at t improve the description of a strictly future, non-economic market-environment distribution compared with a simpler preregistered baseline?"**

The context definition is frozen before target evaluation.

The target is descriptive.

The baseline is explicit.

The folds are chronological.

The result can fail.

No strategy is selected from the result.

This separates **market-state information** from **trading-value claims**.

## 17. Context identity and RESEARCH boundary

This preflight does not claim that the runtime CONTEXT→RESEARCH integration is now complete.

Any future executable research run must bind to a valid `Context` at RESEARCH entry and verify:
- context_id;
- dataset_id;
- dataset_version;
- content_hash;
- instrument;
- granularity;
- timezone_storage;
- configuration_version.

A late trace/audit check cannot replace this boundary validation.

Research artefacts must additionally bind:
- CORE V0.1 identity;
- this preflight/registry identity;
- exact code/config;
- exact train/test fold;
- exact hypothesis_id.

## 18. Relationship to the legacy four regimes

The foundation's:
- TENDANCE;
- RANGE;
- BREAKOUT;
- STRESS

are **not instantiated in CR1**.

CR1 first determines which context axes carry reproducible N0 information.

Only after CR1 adjudication may a separate CR2 preflight ask whether a bounded combination of supported axes can form useful regime candidates.

CR2 may not reopen failed axes merely to obtain prettier labels.

## 19. CR2 admission rule

An axis may enter a future regime-synthesis candidate only if its registered primary hypothesis is:
`SUPPORTED_N0`.

REFUTED_N0 axes are excluded.

NOT_INTERPRETABLE axes remain unresolved and cannot be silently treated as supported.

No CR2 combination is pre-authorized by this document.

## 20. Confirmatory promotion

Because the current corpus is already exposed, CR1 cannot prove a validated regime.

A future confirmatory stage must:
1. choose a bounded hypothesis from CR1;
2. freeze a D1-style Charter;
3. use genuinely new/pristine data;
4. reproduce context construction causally;
5. preregister falsification and decision criteria;
6. retain all negative results.

Only that later stage may use a non-N0 status.

## 21. Resource / execution scope

CR1 implementation target:
- AP0 canonical minute data only;
- no raw 376M tick rescan unless separately justified;
- read-only corpus;
- aggregate outputs only;
- target peak memory <1 GiB;
- no network;
- no MT5;
- no broker action;
- no PnL.

Any execution helper must first receive its own synthetic/adversarial qualification.

## 22. Required breakers before CR1 corpus execution

At minimum:

1. future value leaks into context lookback;
2. target starts at t instead of t+1;
3. target crosses a gap;
4. target crosses a segment;
5. test-fold thresholds leak into train/fitting;
6. test-fold tertiles are refit;
7. 2026 diagnostic changes primary status;
8. baseline B2 omitted for state variables;
9. NY timezone replaced with UTC;
10. Laplace smoothing omitted only in one model;
11. sparse state falsely allowed to SUPPORT;
12. failed fold dropped;
13. primary target silently changed;
14. extra context feature injected;
15. PnL/return-direction target introduced;
16. regime label injected before CR2;
17. foreign Context identity accepted;
18. output omits REFUTED/NOT_INTERPRETABLE hypotheses.

## 23. Machine-readable hypothesis registry

The frozen CR1 family is persisted at:

`reports/program/evidence/2026-09-26-CONTEXT-REGIME-HYPOTHESIS-REGISTRY-V0.1.json`

This registry is the anti-snooping inventory.

A hypothesis not present in that registry is not part of CR1 V0.1.

## Verdict

**PASS — CONTEXT / REGIME RESEARCH PREFLIGHT V0.1.**

Meaning:
- research questions and anti-selection rules are defined;
- no context axis has yet passed;
- no regime has yet been identified;
- no strategy research has begun.

### Next governed action

Materialize a **CR1 context-informativeness helper + synthetic/adversarial tests only**.

Do not execute the real corpus until the persisted helper passes its own re-break.
