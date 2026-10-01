# SFE-01 — DUAL STRATEGY FAMILY DEFINITION — CANDIDATE V0.1

**Date:** 2026-10-01  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 0. Authority status

```text
SFE-01 = DOCUMENTARY_CANDIDATE
BREAKOUT_V1 = DEFINITION_CANDIDATE
MEAN_REVERSION_V1 = DEFINITION_CANDIDATE

HUMAN_ADOPTION = PENDING
IMPLEMENTATION = NOT_AUTHORIZED
BACKTEST = NOT_AUTHORIZED
EXECUTION = NOT_AUTHORIZED
RANKING = NOT_AUTHORIZED
ROUTER = NOT_AUTHORIZED
REGIME_FILTER = NOT_AUTHORIZED
```

This document is non-normative until separate human adoption.

It defines two candidate strategy families before any implementation or performance inspection of those families.

## 1. Fresh-verified persistence base

Immediately before creation:

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

HEAD =
fcca78571a26955ae3fe462746ef49557e4e84e5

TREE =
5ae2814c1d4a00bb5551ecb8adef9e8fb72684f1

REPOSITORY_SAFETY_RULES_BLOB =
b69f3cfab5318b950d70d4310bb763f08ef9d374
```

## 2. Governing provenance and applicability

### 2.1 Normative repository safety

`GOVERNANCE/REPOSITORY-SAFETY-RULES.md` is mandatory.

Relevant invariants:

```text
VERIFY REPOSITORY
→ VERIFY BRANCH
→ VERIFY BASE / REFERENCE COMMIT
→ VERIFY TARGET PATH
→ CHECK APPLICABILITY / PROVENANCE
→ ACTION
```

and:

```text
BLOCKED / UNKNOWN / TO-PROVE
MUST NOT BE RELABELED PASS
```

### 2.2 Foundational research direction

`docs/01-SYSTEM-VISION.md` identifies the intended V1 expert families:

```text
MOMENTUM
MEAN REVERSION
BREAKOUT
```

`docs/03-REGIME-EXPERT-RESEARCH-FOUNDATION.md` states:

- Breakout seeks to exploit a departure from a compression zone or defined structure;
- Mean Reversion seeks to exploit return toward a reference after significant displacement;
- the first experts should remain simple and measurable;
- results must be calculated rather than assumed;
- the baseline is mandatory before adaptive routing;
- look-ahead, leakage, overfitting, data snooping, selection bias, and OOS optimization must be avoided;
- complexity is earned by evidence rather than used as a starting point.

### 2.3 Momentum precedent — methodological only

`docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md` and E1 contracts demonstrate useful methodological precedents:

- closed-bar signal semantics;
- no same-bar use of a signal;
- explicit warmup;
- continuity-aware lookback;
- fixed rules before execution;
- no parameter optimization;
- signal ≠ order;
- execution/cost claims require their own qualified surface.

Those E1 contracts are scoped to E1 / MOMENTUM_V1.

Therefore:

```text
E1_CONTRACT_EXISTS
≠
E1_CONTRACT_AUTOMATICALLY_GOVERNS_SFE
```

SFE-01 may reuse a concept only as an explicitly declared candidate inheritance.

### 2.4 Architecture V2 applicability

Architecture V2 requires:

```text
PASS =
NO FAILURE FOUND
WITHIN THE DEFINED
AND ACTUALLY TESTED SURFACE
```

and distinguishes:

```text
IMPLEMENTATION INDEPENDENCE
DATA / SOURCE INDEPENDENCE
SPECIFICATION / ASSUMPTION DIVERSITY
AUTHORITY INDEPENDENCE
```

SFE-01 therefore records shared and non-shared assumptions explicitly.

It also preserves:

```text
DISCOVERY MUST NOT SILENTLY CONSUME
CONFIRMATORY EVIDENCE
```

## 3. Purpose of SFE-01

SFE-01 creates two separate deterministic family definitions:

```text
TRACK A = BREAKOUT_V1
TRACK B = MEAN_REVERSION_V1
```

The objective is not to determine which is better.

The objective is to make each hypothesis independently testable before any performance-driven tuning.

## 4. Separation invariant

```text
BREAKOUT_V1
≠
MEAN_REVERSION_V1
≠
MOMENTUM_V1
```

No result from one family may alter the frozen definition of the other without:

1. closing the current experiment;
2. explicitly exposing that evidence;
3. creating a new version identity;
4. preregistering the change;
5. obtaining separate human authorization.

Therefore:

```text
BREAKOUT_RESULT
→ NO SILENT MEAN_REVERSION_TUNING

MEAN_REVERSION_RESULT
→ NO SILENT BREAKOUT_TUNING
```

## 5. Common candidate observation surface

The first family definitions use the same minimal abstract observation surface solely to reduce unnecessary degrees of freedom.

### 5.1 Bar granularity

```text
BAR_INTERVAL = H1
```

This is a candidate research granularity, not a multi-horizon claim.

### 5.2 Required fields

A future admissible bar stream must provide at least:

```text
bar_start_timestamp
continuity_block_id
continuity_ordinal
close
```

The exact future dataset/source is intentionally not selected here.

```text
DATA_SOURCE = UNSELECTED
DATASET_IDENTITY = UNSELECTED
EXPERIMENT_WINDOW = UNSELECTED
```

SFE-01 does not consume, mutate, or reserve E1-TD evidence.

### 5.3 Causal close semantics

For a bar indexed by `t`:

```text
C_t = finite completed H1 close at t
```

No incomplete bar may be used.

A signal at `t` may depend only on observations available no later than the close of `t`.

### 5.4 Shared lookback

```text
LOOKBACK = 20 completed admissible H1 bars
```

The value 20 is selected before any Breakout or Mean Reversion performance is observed.

Rationale:

- preserves a minimal single-horizon baseline;
- limits free parameters;
- aligns the initial family-comparison horizon with the existing MOMENTUM_V1 research horizon;
- is not claimed to be optimal for either new family.

This creates an explicit shared specification dependency:

```text
SHARED_ASSUMPTION =
20_BAR_H1_LOOKBACK
```

Therefore results from the two families are not specification-independent evidence regarding the lookback choice.

### 5.5 Continuity

A 20-bar lookback is admissible only when all required observations belong to one coherent continuity block with consecutive ordinals.

Cross-block lookback is forbidden.

A future response observation at `t+1` is admissible only if it remains in the same continuity block and is the immediately following completed H1 bar.

## 6. Shared state vocabulary

Both candidate families use:

```text
LONG
SHORT
NEUTRAL
UNDEFINED
```

These are **signal states only**.

They are not orders, positions, fills, or execution authority.

```text
SIGNAL_STATE
≠
ORDER
≠
POSITION
≠
EXECUTION
≠
PNL
```

A future mapping from signal to target exposure and execution requires a separate contract.

## 7. TRACK A — BREAKOUT_V1

### 7.1 Strategy identity

```text
STRATEGY_ID = BREAKOUT_V1
FAMILY = BREAKOUT
VERSION = V1
```

### 7.2 Research hypothesis

Candidate behavioral hypothesis:

> When a completed H1 close exits beyond the range defined by the preceding 20 admissible H1 closes, the immediately following admissible H1 price response has positive directional continuation on average in the breakout direction.

This is a behavioral hypothesis.

It is not a profitability claim.

### 7.3 Reference channel

For eligible `t`:

```text
U_t = max(C_{t-20}, ..., C_{t-1})
L_t = min(C_{t-20}, ..., C_{t-1})
```

The current close `C_t` is excluded from construction of `U_t` and `L_t`.

This prevents the breakout threshold from being defined using the event it is attempting to classify.

### 7.4 Signal rule

```text
if C_t > U_t:
    BREAKOUT_V1_t = LONG

else if C_t < L_t:
    BREAKOUT_V1_t = SHORT

else:
    BREAKOUT_V1_t = NEUTRAL
```

Ties are neutral:

```text
C_t = U_t → NEUTRAL
C_t = L_t → NEUTRAL
```

### 7.5 UNDEFINED conditions

`BREAKOUT_V1_t = UNDEFINED` if any of the following holds:

- fewer than 20 admissible preceding H1 closes exist in the same continuity block;
- any required close is absent or non-finite;
- H1 ordering is non-monotonic;
- continuity ordinals are incoherent;
- the lookback would cross a continuity boundary;
- the current completed close is unavailable.

### 7.6 Earliest eligibility

If a continuity block begins at ordinal 0:

```text
ordinal 0..19 → UNDEFINED
ordinal 20    → first eligible signal
```

### 7.7 Candidate behavioral response metric

For a directional event at `t` with:

```text
d_t = +1 for LONG
d_t = -1 for SHORT
```

define, only when `t+1` is admissible:

```text
R_(t,t+1) = C_(t+1) / C_t - 1

Y_BREAKOUT_t =
d_t × R_(t,t+1)
```

Interpretation:

```text
Y_BREAKOUT_t > 0
→ next-bar movement aligned with breakout direction

Y_BREAKOUT_t < 0
→ next-bar movement opposed breakout direction
```

This metric is observational and close-to-close.

It is **not executable return** because a signal formed at close `t` cannot assume execution at `C_t`.

### 7.8 Candidate falsification predicate

On a future preregistered evaluation block that independently satisfies its future evidence-sufficiency contract:

```text
mean(Y_BREAKOUT) > 0
→ behavioral prediction SUPPORTED on that block

mean(Y_BREAKOUT) <= 0
→ behavioral prediction REFUTED on that block
```

If evidence sufficiency, provenance, continuity, or admissibility fails:

```text
NOT_INTERPRETABLE
```

SFE-01 does not define the future minimum number of events, confidence procedure, statistical test, source, or evaluation window.

Those must be frozen before any execution.

### 7.9 Explicit non-claims

BREAKOUT_V1 does not currently claim:

- economic profitability;
- positive expectancy after costs;
- robustness across sources;
- robustness across assets;
- robustness across horizons;
- regime-specific superiority;
- optimal lookback;
- optimal entry or exit logic;
- production readiness.

## 8. TRACK B — MEAN_REVERSION_V1

### 8.1 Strategy identity

```text
STRATEGY_ID = MEAN_REVERSION_V1
FAMILY = MEAN_REVERSION
VERSION = V1
```

### 8.2 Research hypothesis

Candidate behavioral hypothesis:

> When a completed H1 close is at least one historical 20-bar population standard deviation away from the mean of the preceding 20 admissible H1 closes, the immediately following admissible H1 price response has positive directional movement toward that recent mean on average.

This is a behavioral hypothesis.

It is not a profitability claim.

### 8.3 Reference mean

For eligible `t`:

```text
MU_t =
(1 / 20) ×
sum(C_i for i = t-20 ... t-1)
```

### 8.4 Reference dispersion

Population standard deviation is used deliberately to remove degrees of freedom:

```text
SIGMA_t =
sqrt(
  (1 / 20) ×
  sum((C_i - MU_t)^2 for i = t-20 ... t-1)
)
```

The current close `C_t` is excluded from `MU_t` and `SIGMA_t`.

If:

```text
SIGMA_t = 0
```

the signal is `UNDEFINED`.

### 8.5 Standardized displacement

```text
Z_t =
(C_t - MU_t) / SIGMA_t
```

### 8.6 Frozen candidate displacement threshold

```text
Z_THRESHOLD = 1.0
```

This value is selected before any MEAN_REVERSION_V1 performance is observed.

It is a minimal symmetric candidate threshold, not an empirical optimum.

### 8.7 Signal rule

```text
if Z_t <= -1.0:
    MEAN_REVERSION_V1_t = LONG

else if Z_t >= +1.0:
    MEAN_REVERSION_V1_t = SHORT

else:
    MEAN_REVERSION_V1_t = NEUTRAL
```

At exact thresholds the directional state applies.

### 8.8 UNDEFINED conditions

`MEAN_REVERSION_V1_t = UNDEFINED` if any of the following holds:

- fewer than 20 admissible preceding H1 closes exist in the same continuity block;
- any required close is absent or non-finite;
- H1 ordering is non-monotonic;
- continuity ordinals are incoherent;
- the lookback would cross a continuity boundary;
- the current completed close is unavailable;
- `SIGMA_t` is zero or non-finite.

### 8.9 Earliest eligibility

If a continuity block begins at ordinal 0:

```text
ordinal 0..19 → UNDEFINED
ordinal 20    → first eligible signal
```

### 8.10 Candidate behavioral response metric

For a directional event at `t` with:

```text
d_t = +1 for LONG
d_t = -1 for SHORT
```

define:

```text
R_(t,t+1) = C_(t+1) / C_t - 1

Y_MEAN_REVERSION_t =
d_t × R_(t,t+1)
```

Because the signal direction is opposite the displacement, positive `Y_MEAN_REVERSION_t` means the next-bar move was in the hypothesized reversion direction.

This metric is observational and close-to-close.

It is not executable return.

### 8.11 Candidate falsification predicate

On a future preregistered evaluation block that independently satisfies its future evidence-sufficiency contract:

```text
mean(Y_MEAN_REVERSION) > 0
→ behavioral prediction SUPPORTED on that block

mean(Y_MEAN_REVERSION) <= 0
→ behavioral prediction REFUTED on that block
```

If evidence sufficiency, provenance, continuity, or admissibility fails:

```text
NOT_INTERPRETABLE
```

SFE-01 does not define the future minimum number of events, confidence procedure, statistical test, source, or evaluation window.

Those must be frozen before any execution.

### 8.12 Explicit non-claims

MEAN_REVERSION_V1 does not currently claim:

- economic profitability;
- positive expectancy after costs;
- robustness across sources;
- robustness across assets;
- robustness across horizons;
- regime-specific superiority;
- optimal lookback;
- optimal z threshold;
- optimal entry or exit logic;
- production readiness.

## 9. Parameter freeze and anti-optimization rule

Candidate parameters are:

```text
BREAKOUT_V1:
BAR_INTERVAL = H1
LOOKBACK = 20

MEAN_REVERSION_V1:
BAR_INTERVAL = H1
LOOKBACK = 20
Z_THRESHOLD = 1.0
SIGMA_DENOMINATOR = 20
```

After human adoption, any change to these values requires a new strategy version.

Examples:

```text
BREAKOUT_V1
→ cannot silently become lookback 55

MEAN_REVERSION_V1
→ cannot silently become threshold 1.5
```

If a future result motivates such a change, the current evidence becomes hypothesis-generating for the new version, not untouched confirmation.

## 10. Cross-family contamination boundary

### 10.1 Forbidden tuning flow

```text
observe BREAKOUT_V1 results
→ alter MEAN_REVERSION_V1
→ call same evidence independent
= FORBIDDEN
```

and:

```text
observe MEAN_REVERSION_V1 results
→ alter BREAKOUT_V1
→ call same evidence independent
= FORBIDDEN
```

### 10.2 Separate experiment identities

Any future execution must create separate experiment identities:

```text
BREAKOUT_V1_EXPERIMENT_ID
≠
MEAN_REVERSION_V1_EXPERIMENT_ID
```

### 10.3 Separate result interpretation

A result for one family cannot close the other.

```text
BREAKOUT_SUPPORTED
≠
MEAN_REVERSION_REFUTED

MEAN_REVERSION_SUPPORTED
≠
BREAKOUT_REFUTED
```

unless a future preregistered experiment explicitly tests a logically shared proposition that warrants that interpretation.

SFE-01 does not create such a shared proposition.

## 11. Dependency and assumption comparison

### 11.1 Shared dependencies

Both definitions share:

- completed H1 bars;
- finite close observations;
- 20-bar causal lookback;
- continuity-safe history;
- one-bar behavioral response horizon;
- no regime filter;
- no source selected yet;
- no execution or cost model yet.

Therefore they are **not independent validations** of:

- H1 as a useful horizon;
- a 20-bar timescale;
- close-only market representation;
- the future selected data source.

### 11.2 Breakout-specific dependencies

BREAKOUT_V1 uniquely depends on:

```text
RECENT_RANGE_EXTREME
+
CHANNEL_BREACH
+
CONTINUATION_DIRECTION
```

It does not require an estimated mean or variance.

### 11.3 Mean-Reversion-specific dependencies

MEAN_REVERSION_V1 uniquely depends on:

```text
RECENT_MEAN
+
RECENT_DISPERSION
+
STANDARDIZED_DISPLACEMENT
+
REVERSION_DIRECTION
```

It does not require a channel breach.

### 11.4 Assumption diversity status

```text
DATA_SOURCE_DIVERSITY =
NOT_YET_DEFINED

IMPLEMENTATION_INDEPENDENCE =
FUTURE_REQUIREMENT

SPECIFICATION_DIVERSITY =
PARTIAL

AUTHORITY_INDEPENDENCE =
PRESERVED_BY_HUMAN_ADOPTION_BOUNDARY
```

The two families are meaningfully different hypotheses, but they still share important observational and timescale assumptions.

No claim of absolute assumption independence is permitted.

## 12. Regime firewall

SFE-01 deliberately excludes regime conditioning.

Therefore:

```text
BREAKOUT_V1_SIGNAL
does not inspect REGIME

MEAN_REVERSION_V1_SIGNAL
does not inspect REGIME
```

No ADX, ATR regime classifier, session classifier, stress filter, trend filter, or router may modify the signal under V1.

Reason:

the repository research foundation requires baseline expert behavior to be known before adaptive routing is credited with value.

A regime-conditioned version would be a later, separately versioned object.

## 13. Execution firewall

SFE-01 defines signals and behavioral predictions only.

It does not adopt:

- E1-04 as the SFE execution contract;
- any entry price;
- any exit price;
- any stop;
- any take profit;
- pyramiding;
- scaling;
- leverage;
- position sizing;
- commission assumption;
- slippage assumption;
- financing assumption;
- broker model.

A future strategy backtest must separately define and qualify its execution/cost surface before making economic claims.

## 14. Data and evidence firewall

### 14.1 No dataset selected

```text
SOURCE = UNSELECTED
DATASET = UNSELECTED
WINDOW = UNSELECTED
```

### 14.2 E1 evidence remains separate

No E1 historical result is used here as evidence that BREAKOUT_V1 or MEAN_REVERSION_V1 works.

The shared 20-bar horizon is a pre-experiment specification choice, not a result-derived validation.

### 14.3 E1-TD untouched

```text
TD01 = UNCHANGED
TD02 = UNCHANGED
TD03 = UNCHANGED
TD03A = UNCHANGED
TD03B = UNCHANGED
TD03B_EVENT_BUDGET = UNTOUCHED
```

No Source-B prospective object is consumed by SFE-01.

## 15. Future evidence-sufficiency requirements — deliberately open

SFE-01 intentionally does **not** invent the following:

- minimum directional-event count;
- statistical confidence procedure;
- bootstrap or asymptotic method;
- multiple-testing correction;
- source identity;
- evaluation dates;
- development/evaluation split;
- economic PnL metric;
- cost model;
- acceptance threshold for production.

Those are experiment-level choices.

They must be preregistered before any performance observation.

Until then:

```text
BEHAVIORAL_PREDICTION =
DEFINED

EXPERIMENTAL_SUFFICIENCY =
NOT_YET_DEFINED

REAL_EXECUTION =
NOT_AUTHORIZED
```

## 16. Candidate status semantics

Before any future experiment:

```text
BREAKOUT_V1 = UNTESTED
MEAN_REVERSION_V1 = UNTESTED
```

A future experiment may classify its own scoped finding as:

```text
SUPPORTED
REFUTED
NOT_INTERPRETABLE
```

but only within its actual preregistered evidence surface.

No single result may be silently generalized to all assets, sources, horizons, regimes, or market history.

## 17. What would falsify the family-level behavioral prediction

### BREAKOUT_V1

A valid future experiment capable of adjudicating the candidate prediction refutes the prediction on its declared evidence block if:

```text
mean(Y_BREAKOUT) <= 0
```

### MEAN_REVERSION_V1

A valid future experiment capable of adjudicating the candidate prediction refutes the prediction on its declared evidence block if:

```text
mean(Y_MEAN_REVERSION) <= 0
```

These rules deliberately allow refutation.

No post-result parameter search may be used to rescue V1 under the same identity.

## 18. Explicit forbidden claims

SFE-01 does not permit:

```text
BREAKOUT_V1_IS_PROFITABLE
MEAN_REVERSION_V1_IS_PROFITABLE
BREAKOUT_BEATS_MEAN_REVERSION
MEAN_REVERSION_BEATS_BREAKOUT
BEST_STRATEGY
REGIME_ROUTER_VALIDATED
SOURCE_INDEPENDENT_VALIDATION
ROBUST_ACROSS_MARKETS
PRODUCTION_READY
PAPER_READY
BROKER_READY
LIVE_READY
CAPITAL_READY
```

## 19. Future qualification topology

If SFE-01 is later human-adopted, the next candidate engineering topology is:

```text
SFE-02A
BREAKOUT_V1
CONTRACT
→ TEST-FIRST RED
→ MINIMAL IMPLEMENTATION
→ ADVERSARIAL BREAK
→ QUALIFICATION
→ STOP

SFE-02B
MEAN_REVERSION_V1
CONTRACT
→ TEST-FIRST RED
→ MINIMAL IMPLEMENTATION
→ ADVERSARIAL BREAK
→ QUALIFICATION
→ STOP
```

SFE-02A and SFE-02B must remain separately closable.

Failure in one does not grant authority to mutate or skip the other.

No backtest follows automatically from implementation qualification.

## 20. Comparative study firewall

Only after both standalone families possess independently qualified definitions/implementations and separately authorized experiments may a future comparison be proposed.

That future surface would require its own contract.

It must not be inferred from SFE-01.

```text
SFE-03_COMPARATIVE_STUDY =
NOT_AUTHORIZED
```

## 21. Review targets before human adoption

External review should attempt to falsify at least:

1. causal computability of both definitions;
2. ambiguity in bar/window indexing;
3. hidden look-ahead;
4. hidden parameter tuning;
5. false execution/PnL implications;
6. cross-family contamination;
7. dependence laundering;
8. inappropriate reuse of E1 authority;
9. ambiguity in `UNDEFINED`;
10. insufficiency of falsification logic;
11. whether BREAKOUT_V1 is truly a breakout family baseline;
12. whether MEAN_REVERSION_V1 is truly a mean-reversion family baseline;
13. whether the two definitions are distinct enough to justify separate experiments;
14. whether the shared 20-bar/H1 assumptions are represented honestly;
15. whether any statement overclaims independence or validation.

## 22. SFE-01 candidate conclusion

```text
SFE_01_DOCUMENTARY_DEFINITION =
PRODUCED_CANDIDATE

BREAKOUT_V1 =
DEFINED_CANDIDATE
UNTESTED
NOT_ADOPTED

MEAN_REVERSION_V1 =
DEFINED_CANDIDATE
UNTESTED
NOT_ADOPTED

IMPLEMENTATION =
NOT_AUTHORIZED

BACKTEST =
NOT_AUTHORIZED

RANKING =
NOT_AUTHORIZED

ROUTER =
NOT_AUTHORIZED

REGIME_FILTER =
NOT_AUTHORIZED

NEXT_ACTION =
EXTERNAL_ADVERSARIAL_REVIEW
THEN HUMAN_ADJUDICATION

STOP =
TRUE
```
