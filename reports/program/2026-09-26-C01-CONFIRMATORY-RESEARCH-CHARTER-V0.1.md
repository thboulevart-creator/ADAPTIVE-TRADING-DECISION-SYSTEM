# C01 — CONFIRMATORY RESEARCH CHARTER V0.1

Date: 2026-09-26  
Status: **FROZEN BEFORE CONFIRMATION-DATA ACCESS**

This is an experiment-specific frozen Charter for C01. It does not freeze or amend the repository-wide draft `docs/D1.3-RESEARCH-CHARTER.md`.

## 1. Origin

CR2 exact evidence:
- Git blob `d6543d12fc01405fedb006ddb5d714a772f32678`
- SHA-256 `5c05e9e8d965314f4a6852aa71f442f89a0962133edc79873cf610682f34c501`

C01:
`CR2-C01-ABS_VOL_X_TICK`

CR2 status:
`SUPPORTED_N0_SYNTHESIS`.

C01 is eligible for confirmation because it independently satisfied its preregistered CR2 rule.

This is **not** a ranking against C02.

## 2. Confirmatory hypothesis

> On genuinely new/pristine USTECH price-core data, the frozen C01 ABS_VOL × TICK joint state improves the probabilistic description of the next-15m joint RV15 × TICK15 environment beyond both frozen constituent baselines.

The hypothesis is falsifiable.

The confirmatory test remains descriptive and non-economic.

## 3. Frozen candidate structure

Calendar backbone:
- NY hour;
- NY weekday.

Dynamic state:
- absolute backward RV15 tertile state;
- backward tick5 hour-relative tertile state.

Joint dynamic state:
3 × 3 = 9 neutral categories.

No semantic regime names are allowed.

## 4. Development fit cutoff

All fitted parameters must come only from development observations up to:

`2025-12-31T23:59:59Z`

This reproduces the training side of the already-registered D2026 CR2 diagnostic.

No 2026 confirmation-period information may enter fitting.

## 5. Already frozen numeric thresholds

From the CR2 D2026 fold:

### ABS RV15 state
- low/mid = 5.371776146488064
- mid/high = 10.71209216288787

### tick5 NY-hour-relative state
- low/mid = 0.8005586592178772
- mid/high = 1.2183908045977012

### future RV15 target quintiles
- 3.973523081929233
- 6.185588239477184
- 9.29219887827349
- 15.11786314181646

### future TICK15 target quintiles
- 91.53333333333333
- 144.26666666666668
- 220.66666666666666
- 338.8

These values cannot be refit on confirmation data.

## 6. Frozen-model artifact required before confirmation access

Before any confirmation-data calculation, a separate immutable model artifact must serialize:

1. 24 training-only New-York-hour medians used to normalize tick5;
2. B2 + ABS_VOL baseline probability tables for the 25-class target;
3. B2 + TICK baseline probability tables;
4. B2 + ABS_VOL + TICK candidate probability tables;
5. Laplace alpha = 1;
6. exact code/data/config identities.

This artifact must be generated solely from development data <= 2025-12-31.

Its production is the next governed implementation step.

## 7. Confirmation data window

Fixed before confirmation outcome inspection:

Start:
`2026-05-25T00:00:00Z`

End:
`2027-05-24T23:59:59Z`

The window is exactly 12 months and begins strictly after the AP0 behavioral-profile period.

The confirmation data must:
- be USTECH;
- preserve the same price-core semantics;
- preserve the same source lineage;
- not have been used to alter C01;
- have demonstrable provenance.

If prior exposure to these observations has influenced the candidate, the result cannot be called confirmatory.

## 8. No early evaluation

The primary confirmation score must not be computed before the fixed confirmation window closes.

Context/state-count plumbing may be validated without target-outcome scoring, but it may not modify the candidate.

This prevents optional stopping based on favorable scores.

## 9. Primary target

25-class joint future environment:

`RV15 quintile × TICK15 quintile`

Target begins strictly at `t+1`.

No gap or segment crossing.

## 10. Frozen baselines

C01 must be compared against both:

1. B2 + ABS_VOL
2. B2 + TICK

No weaker baseline may replace either one.

No baseline may be refit on confirmation data.

## 11. Sparse guard

Every one of the nine joint states must have at least:

**500 valid primary targets**

in the fixed confirmation window.

If any state has fewer than 500:
`NOT_INTERPRETABLE`.

The sparse floor cannot be lowered after observing data.

## 12. Confirmation decision

### CONFIRMED

Only if:
- every joint state has >=500 valid observations;
- vs ABS_VOL: dLL > 0 and dBrier > 0;
- vs TICK: dLL > 0 and dBrier > 0;
- all provenance, identity, causality and continuity controls PASS.

### REFUTED

If:
- either required comparison has dLL <= 0; or
- either required comparison has dBrier <= 0.

### NOT_INTERPRETABLE

If:
- sparse guard fails;
- new/pristine eligibility cannot be established;
- identity/provenance/continuity fails;
- another critical control invalidates the test.

The 60m horizon remains secondary only and cannot rescue a failed 15m confirmation.

## 13. Forbidden modifications

After this Charter is frozen, the same confirmatory test cannot:
- change bins;
- change thresholds;
- refit hour medians;
- refit probability tables;
- add/remove features;
- add C02;
- change the target;
- change the baseline;
- lower sparse requirements;
- select a favorable subperiod;
- introduce semantic regime names;
- introduce PnL/direction/strategy/MT5.

Any such change requires a new Charter and the current confirmation claim is abandoned.

## 14. Epistemic meaning

A future `CONFIRMED` result would confirm only:

> the frozen C01 context state contains incremental descriptive information about the future volatility/activity environment on the preregistered new-data window.

It would still not establish:
- directional predictability;
- profitability;
- a trading strategy;
- causal mechanism;
- execution realism.

## Verdict

**CHARTER FROZEN — C01 CONFIRMATORY TEST DEFINED BEFORE CONFIRMATION-DATA ACCESS.**

### Next governed action

Materialize and qualify the **C01 frozen-model artifact producer** using development data only.

No confirmation-data access is authorized before that artifact is sealed.
