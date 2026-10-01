# SFE-01 — DUAL STRATEGY FAMILY DEFINITION — CANDIDATE V0.2

**Date:** 2026-10-01  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 0. Authority status

```text
SFE-01 = DOCUMENTARY_CANDIDATE_V0_2
BREAKOUT_V1 = DEFINITION_CANDIDATE
MEAN_REVERSION_V1 = DEFINITION_CANDIDATE

V0_1_EXTERNAL_REVIEW = FAIL
V0_2_TARGETED_CLOSURE = ADDRESSED_PENDING_RE_REVIEW

HUMAN_ADOPTION = PENDING
IMPLEMENTATION = NOT_AUTHORIZED
BACKTEST = NOT_AUTHORIZED
EXECUTION = NOT_AUTHORIZED
RANKING = NOT_AUTHORIZED
ROUTER = NOT_AUTHORIZED
REGIME_FILTER = NOT_AUTHORIZED
```

This document is non-normative until separate human adoption.

It supersedes V0.1 only as the current **candidate under review**.  
V0.1 remains immutable historical evidence of the first candidate and its adversarial break.

No signal rule or strategy parameter has been changed from V0.1.

## 1. Fresh-verified amendment base

Immediately before V0.2 creation:

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

HEAD =
11e6e6f637f62799144a122c2e3e11510e06c935

TREE =
90b30582449419384c59cda1cf9a809d4720620c

V0_1_PATH =
GOVERNANCE/SFE-01-DUAL-STRATEGY-FAMILY-DEFINITION-CANDIDATE-V0.1.md

V0_1_BLOB =
99d1698d303797b25ed7c140c5ad43f276cefe2c

V0_1_EXTERNAL_REVIEW_PACKAGE_BLOB =
e89050df1be93bb5ff636d34d602bb43abbde9fc

CLAUDE_REVIEW_UPLOAD_SHA256 =
7a17613f62234f3aae190ad13c323b4f7629f9516ce1bee61155927ac0235763
```

The external review verdict was `FAIL`, with findings `SFE01-F01` through `SFE01-F16`.

The V0.2 amendment treats F01-F05 as adoption-blocking and F06-F16 as targeted hardening findings.

## 2. Governing provenance and declared candidate inheritances

### 2.1 Repository safety

`GOVERNANCE/REPOSITORY-SAFETY-RULES.md` remains mandatory.

```text
IDENTIFY REPOSITORY
→ VERIFY BRANCH
→ VERIFY BASE / REFERENCE COMMIT
→ VERIFY TARGET PATH
→ CHECK APPLICABILITY / PROVENANCE
→ ACTION
```

```text
BLOCKED / UNKNOWN / TO-PROVE
MUST NOT BE RELABELED PASS
```

### 2.2 Foundational research direction

The project V1 research foundation identifies three simple expert families:

```text
MOMENTUM
BREAKOUT
MEAN REVERSION
```

The baseline must precede adaptive routing. Results must be calculated rather than assumed. Look-ahead, leakage, overfitting, data snooping, selection bias and OOS optimization are prohibited methodological failure modes.

### 2.3 Declared candidate inheritances from the Momentum/E1 precedent

SFE-01 explicitly reuses the following **concepts only**:

```text
DECLARED_CANDIDATE_INHERITANCE_01 =
COMPLETED_BAR_SIGNAL_SEMANTICS

DECLARED_CANDIDATE_INHERITANCE_02 =
CONTINUITY_AWARE_LOOKBACK

DECLARED_CANDIDATE_INHERITANCE_03 =
20_COMPLETED_H1_BAR_TIMESCALE

DECLARED_CANDIDATE_INHERITANCE_04 =
NO_PARAMETER_OPTIMIZATION

DECLARED_CANDIDATE_INHERITANCE_05 =
SIGNAL_IS_NOT_EXECUTION
```

These are independently restated in SFE-01.

They do **not** import E1 authority, E1 execution authority, E1 dataset authority, E1 performance evidence, or E1 confirmation status.

```text
E1_CONCEPT_REUSE
≠
E1_AUTHORITY_INHERITANCE
```

### 2.4 Architecture V2 applicability

```text
PASS =
NO FAILURE FOUND
WITHIN THE DEFINED
AND ACTUALLY TESTED SURFACE
```

SFE-01 distinguishes:

```text
IMPLEMENTATION INDEPENDENCE
DATA / SOURCE INDEPENDENCE
SPECIFICATION / ASSUMPTION DIVERSITY
AUTHORITY INDEPENDENCE
```

and preserves:

```text
DISCOVERY MUST NOT SILENTLY CONSUME
CONFIRMATORY EVIDENCE
```

## 3. Purpose

SFE-01 defines two separate deterministic V1 family baselines:

```text
TRACK A = BREAKOUT_V1
TRACK B = MEAN_REVERSION_V1
```

The purpose is not to rank them.

The purpose is to define two different behavioral propositions before any performance-driven tuning.

## 4. Separation and dependency invariant

### 4.1 Distinct strategy identities

```text
BREAKOUT_V1
≠
MEAN_REVERSION_V1
≠
MOMENTUM_V1
```

Identity distinction does **not** mean statistical or logical independence.

### 4.2 No silent cross-family tuning

No result from one family may alter the frozen definition or experiment design of the other without explicit exposure handling and a new governed decision.

```text
BREAKOUT_RESULT
→ NO SILENT MEAN_REVERSION_TUNING

MEAN_REVERSION_RESULT
→ NO SILENT BREAKOUT_TUNING
```

### 4.3 Experiment-design contamination firewall

If BREAKOUT_V1 and MEAN_REVERSION_V1 will use any shared source, instrument, price field, window, segmentation or evaluation evidence:

```text
BOTH EXPERIMENT CONTRACTS
MUST BE PREREGISTERED
BEFORE ANY PERFORMANCE RESULT
FROM EITHER FAMILY IS OBSERVED
```

If the second contract is designed after observing the first family's result on materially shared evidence:

```text
SECOND_EXPERIMENT =
EXPOSED / NON_BLIND / EXPLORATORY
```

It may not be represented as pristine independent confirmation on that shared evidence.

## 5. Common candidate observation surface

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

The exact source, dataset, instrument, price field and evaluation window are not selected here.

```text
DATA_SOURCE = UNSELECTED
DATASET_IDENTITY = UNSELECTED
INSTRUMENT_IDENTITY = UNSELECTED
PRICE_FIELD = UNSELECTED
EXPERIMENT_WINDOW = UNSELECTED
```

All of those must be preregistered before any SFE performance observation.

### 5.3 Causal close semantics

For bar `t`:

```text
C_t =
strictly positive,
finite,
completed H1 close at t
```

No incomplete bar may be used.

A signal at `t` may depend only on observations available no later than the close of `t`.

Timestamps must be strictly increasing. Duplicate timestamps are invalid.

### 5.4 Shared lookback

```text
LOOKBACK =
20 completed admissible H1 bars
```

The value 20 remains unchanged from V0.1.

It is a preregistered baseline specification choice, not an empirical optimum.

It is also a shared dependency with MOMENTUM_V1 and between the two SFE families.

### 5.5 Continuity

A 20-bar lookback is admissible only when all required observations belong to one coherent continuity block with consecutive ordinals.

Cross-block lookback is forbidden.

The future dataset-identity contract must freeze:

- the exact segmentation rule;
- gap handling;
- expected H1 timestamp spacing;
- when a new block begins;
- whether a block identifier can reappear;
- how missing bars are represented;
- the causal rule by which block membership is knowable at signal time.

A future response observation `t+1` is admissible only when:

- it is the immediately following completed H1 bar;
- it remains in the same admissible continuity block;
- its close is finite and strictly positive.

The future experiment must publish the number of directional events excluded because `t+1` was not admissible.

## 6. Shared state and event semantics

Both families use:

```text
LONG
SHORT
NEUTRAL
UNDEFINED
```

These are signal states only.

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

### 6.1 Frozen directional-event definition

For both V1 families:

```text
DIRECTIONAL_EVENT_AT_t
=
EVERY ELIGIBLE H1 BAR
WHOSE SIGNAL STATE AT t
IS LONG OR SHORT
```

A directional event is **not** restricted to a transition into LONG or SHORT.

Therefore a sequence:

```text
LONG, LONG, LONG
```

contains three directional event-bars if all three bars are eligible.

This event definition is frozen before performance observation.

## 7. TRACK A — BREAKOUT_V1

### 7.1 Identity

```text
STRATEGY_ID = BREAKOUT_V1
FAMILY = BREAKOUT
VERSION = V1
```

### 7.2 One-bar behavioral hypothesis

> When a completed H1 close exits beyond the range defined by the preceding 20 admissible H1 closes, the immediately following admissible H1 close-to-close response has positive directional continuation on average in the breakout direction.

This is a **one-response-bar behavioral hypothesis**.

It is not a profitability claim and does not claim continuation beyond the next H1 response bar.

### 7.3 Reference channel

For eligible `t`:

```text
U_t = max(C_{t-20}, ..., C_{t-1})
L_t = min(C_{t-20}, ..., C_{t-1})
```

`C_t` is excluded from `U_t` and `L_t`.

### 7.4 Signal rule — UNCHANGED FROM V0.1

```text
if C_t > U_t:
    BREAKOUT_V1_t = LONG

else if C_t < L_t:
    BREAKOUT_V1_t = SHORT

else:
    BREAKOUT_V1_t = NEUTRAL
```

Ties remain neutral.

### 7.5 UNDEFINED conditions

`BREAKOUT_V1_t = UNDEFINED` when:

- fewer than 20 admissible preceding H1 closes exist in the same continuity block;
- any required close is missing, non-finite or non-positive;
- timestamps are not strictly increasing;
- continuity ordinals are incoherent;
- the lookback crosses a continuity boundary;
- the current completed close is unavailable.

### 7.6 Earliest eligibility

```text
ordinal 0..19 → UNDEFINED
ordinal 20    → first eligible signal
```

### 7.7 Behavioral response

For every directional event-bar:

```text
d_t = +1 for LONG
d_t = -1 for SHORT

R_(t,t+1) =
C_(t+1) / C_t - 1

Y_BREAKOUT_t =
d_t × R_(t,t+1)
```

This is defined only if `t+1` satisfies the admissibility conditions in Section 5.5.

```text
Y_BREAKOUT_t > 0
→ one-bar response aligned with breakout direction

Y_BREAKOUT_t < 0
→ one-bar response opposed breakout direction
```

It is observational close-to-close response, not executable return.

### 7.8 Direction of effect versus future statistical verdict

SFE-01 freezes only the predicted effect direction:

```text
PREDICTED_EFFECT_DIRECTION =
mean(Y_BREAKOUT) > 0
```

SFE-01 does **not** allow the sign of the sample mean alone to create a final `SUPPORTED` verdict.

Before any performance observation, the future experiment contract must freeze:

- evidence-sufficiency criteria;
- statistical procedure;
- null treatment;
- uncertainty/confidence rule;
- exact mapping from statistical result to finding status.

The mapping must include a non-decisive outcome such as:

```text
NOT_INTERPRETABLE /
NON_DECISIVE_STATISTICAL_EVIDENCE
```

A future `REFUTED` status must therefore be produced by the preregistered experiment-level decision rule, not by post hoc interpretation.

### 7.9 Construct-validity limit

BREAKOUT_V1 tests:

```text
20-BAR PRIOR-CLOSE RANGE-EXTREME BREACH
+
ONE-BAR DIRECTIONAL CONTINUATION
```

It does **not** require prior volatility compression.

Therefore:

```text
BREAKOUT_V1
≠
COMPRESSION_CONDITIONED_BREAKOUT
```

A negative result does not refute every possible breakout definition.

### 7.10 Explicit non-claims

BREAKOUT_V1 does not claim:

- profitability;
- positive expectancy after costs;
- robustness across sources/assets;
- robustness at other bar intervals;
- persistence beyond one response H1 bar;
- compression-conditioned breakout;
- regime-specific superiority;
- optimal lookback;
- optimal entry/exit;
- production readiness.

## 8. TRACK B — MEAN_REVERSION_V1

### 8.1 Identity

```text
STRATEGY_ID = MEAN_REVERSION_V1
FAMILY = MEAN_REVERSION
VERSION = V1
```

### 8.2 One-bar behavioral hypothesis

> When a completed H1 close is at least one historical 20-bar population standard deviation away from the mean of the preceding 20 admissible H1 closes, the immediately following admissible H1 close-to-close response has positive directional movement toward that recent mean on average.

This is a **one-response-bar behavioral hypothesis**.

It is not a profitability claim and does not claim multi-bar completion of a reversion.

### 8.3 Reference mean

```text
MU_t =
(1 / 20) ×
sum(C_i for i = t-20 ... t-1)
```

### 8.4 Reference dispersion

```text
SIGMA_t =
sqrt(
  (1 / 20) ×
  sum((C_i - MU_t)^2 for i = t-20 ... t-1)
)
```

`C_t` remains excluded.

### 8.5 Standardized displacement

```text
Z_t =
(C_t - MU_t) / SIGMA_t
```

### 8.6 Frozen threshold — UNCHANGED FROM V0.1

```text
Z_THRESHOLD = 1.0
SIGMA_DENOMINATOR = 20
```

No optimization claim is made.

### 8.7 Signal rule — UNCHANGED FROM V0.1

```text
if Z_t <= -1.0:
    MEAN_REVERSION_V1_t = LONG

else if Z_t >= +1.0:
    MEAN_REVERSION_V1_t = SHORT

else:
    MEAN_REVERSION_V1_t = NEUTRAL
```

Exact-threshold states remain directional.

### 8.8 UNDEFINED conditions

`MEAN_REVERSION_V1_t = UNDEFINED` when:

- fewer than 20 admissible preceding H1 closes exist in the same continuity block;
- any required close is missing, non-finite or non-positive;
- timestamps are not strictly increasing;
- continuity ordinals are incoherent;
- the lookback crosses a continuity boundary;
- the current completed close is unavailable;
- `SIGMA_t` is zero or non-finite under the future frozen numerical semantics.

### 8.9 Earliest eligibility

```text
ordinal 0..19 → UNDEFINED
ordinal 20    → first eligible signal
```

### 8.10 Behavioral response

For every directional event-bar:

```text
d_t = +1 for LONG
d_t = -1 for SHORT

R_(t,t+1) =
C_(t+1) / C_t - 1

Y_MEAN_REVERSION_t =
d_t × R_(t,t+1)
```

This is defined only when `t+1` satisfies Section 5.5.

Positive `Y_MEAN_REVERSION_t` means one-bar movement in the hypothesized reversion direction.

This is observational close-to-close response, not executable return.

### 8.11 Direction of effect versus future statistical verdict

SFE-01 freezes only:

```text
PREDICTED_EFFECT_DIRECTION =
mean(Y_MEAN_REVERSION) > 0
```

The sample-mean sign alone cannot create `SUPPORTED`.

The future experiment contract must preregister the complete evidence-sufficiency and statistical decision rule, including a non-decisive outcome.

### 8.12 Construct-validity limit

MEAN_REVERSION_V1 uses price **levels** relative to the recent mean and dispersion of those levels.

A steady trend can therefore produce `|Z_t| >= 1` without a discrete shock.

Therefore:

```text
MEAN_REVERSION_V1
DOES NOT DISTINGUISH
STEADY TREND DISPLACEMENT
FROM SHOCK-LIKE DISPLACEMENT
```

A negative result does not refute mean reversion at other response horizons or under other displacement definitions.

### 8.13 Numerical-semantics obligation

Before any implementation of SFE-02B, its contract must freeze at minimum:

- numeric type/precision;
- summation algorithm or equivalent deterministic reduction semantics;
- population-variance computation method;
- square-root semantics;
- threshold comparison form;
- deterministic treatment of mathematically zero dispersion;
- edge-case concordance tests between independent/reference implementations.

No implementation may choose these semantics after inspecting strategy performance.

### 8.14 Explicit non-claims

MEAN_REVERSION_V1 does not claim:

- profitability;
- positive expectancy after costs;
- robustness across sources/assets;
- robustness at other bar intervals;
- reversion beyond one response H1 bar;
- shock-specific mean reversion;
- regime-specific superiority;
- optimal lookback;
- optimal z threshold;
- optimal entry/exit;
- production readiness.

## 9. Parameter freeze and anti-optimization rule

Parameters remain exactly:

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

The canonical Git blob assigned to this V0.2 document at persistence becomes the documentary freeze anchor for these candidate parameters.

Any later numerical parameter change requires a new strategy version.

No result may be used to rescue V1 under the same identity by changing its parameters.

## 10. Cross-family mechanical coupling

### 10.1 Co-signal direction

When both families produce directional signals on the same eligible bar, they cannot signal the same direction.

For a BREAKOUT_V1 LONG:

```text
C_t > U_t
and
U_t >= MU_t

therefore
C_t > MU_t

so MEAN_REVERSION_V1
cannot be LONG
```

The symmetric statement holds for BREAKOUT_V1 SHORT.

Thus, on directional co-firing bars:

```text
d_BREAKOUT_t =
-d_MEAN_REVERSION_t
```

### 10.2 Shared-response identity on co-firing bars

Both definitions use the same:

```text
R_(t,t+1)
```

Therefore on every bar where both are directional:

```text
Y_BREAKOUT_t =
-Y_MEAN_REVERSION_t
```

This is a declared mechanical dependency, not independent evidence.

### 10.3 Required future reporting

Any future experiment on materially shared evidence must publish separately:

```text
N_BREAKOUT_DIRECTIONAL
N_MEAN_REVERSION_DIRECTIONAL
N_CO_FIRING
N_BREAKOUT_EXCLUSIVE
N_MEAN_REVERSION_EXCLUSIVE
```

and the family response summaries at least for:

```text
CO_FIRING_EVENTS
FAMILY_EXCLUSIVE_EVENTS
ALL_DIRECTIONAL_EVENTS
```

No aggregate result may hide the co-firing structure.

## 11. Dependency relationship to MOMENTUM_V1

The canonical MOMENTUM_V1 rule is:

```text
M_t =
C_t / C_(t-20) - 1

M_t > 0 → LONG
M_t < 0 → SHORT
M_t = 0 → NEUTRAL
```

On the same H1 close representation and 20-bar lookback:

### 11.1 BREAKOUT LONG implication

```text
C_t > max(C_(t-20), ..., C_(t-1))
⇒ C_t > C_(t-20)
⇒ MOMENTUM_V1 = LONG
```

### 11.2 BREAKOUT SHORT implication

```text
C_t < min(C_(t-20), ..., C_(t-1))
⇒ C_t < C_(t-20)
⇒ MOMENTUM_V1 = SHORT
```

Therefore:

```text
BREAKOUT_V1_DIRECTIONAL_EVENTS
⊂
MOMENTUM_V1_DIRECTIONAL_STATES
```

under the same admissible H1 close stream and lookback semantics.

This is a structural dependence.

BREAKOUT_V1 remains a distinct rule, but it is not evidence-independent of MOMENTUM_V1 with respect to 20-bar directional change.

### 11.3 E1 overlap rule

Any future SFE evaluation window that overlaps market observations already inspected under E1 must be explicitly labeled:

```text
E1_EXPOSED
NOT_PRISTINE_CONFIRMATORY_EVIDENCE
```

for propositions materially linked to the prior E1 exposure.

For BREAKOUT_V1 this is mandatory because of the structural implication above.

For MEAN_REVERSION_V1, exposure status must also account for:

- shared H1/20-bar/source representation;
- co-firing coupling with BREAKOUT_V1;
- any direct inspection of MR-computable outcomes on the same evidence.

No shared historical evidence may be relabeled pristine merely because the strategy name differs.

## 12. Shared dependencies and assumption-diversity status

Both families share:

- H1 completed bars;
- close-only candidate representation;
- 20-bar causal lookback;
- continuity semantics;
- one-response-bar horizon;
- the same response return formula;
- no regime filter;
- future source/instrument/price-field choices if selected jointly.

Therefore:

```text
DATA_SOURCE_DIVERSITY =
NOT_YET_DEFINED

IMPLEMENTATION_INDEPENDENCE =
FUTURE_REQUIREMENT

SPECIFICATION_DIVERSITY =
PARTIAL

AUTHORITY_INDEPENDENCE =
DEPENDS_ON_ADJUDICATOR_IDENTITY
```

Human adjudication preserves the authority boundary, but it does not by itself prove sociological or methodological independence of the adjudicator.

No absolute independence claim is permitted.

## 13. Regime firewall

Neither V1 signal inspects regime.

```text
BREAKOUT_V1_SIGNAL
does not inspect REGIME

MEAN_REVERSION_V1_SIGNAL
does not inspect REGIME
```

No ADX, ATR regime classifier, trend filter, stress filter, session filter or router may modify the V1 signal.

A regime-conditioned variant requires a separately versioned object and separate authority.

## 14. Execution and PnL firewall

SFE-01 defines signal states and one-bar behavioral responses only.

It does not define or authorize:

- entry price;
- exit price;
- order timing;
- position persistence;
- stop;
- take profit;
- pyramiding;
- scaling;
- leverage;
- size;
- spread treatment;
- commission;
- slippage;
- financing;
- broker execution.

```text
BEHAVIORAL_SUPPORTED
≠
ECONOMIC_EDGE
≠
EXECUTABLE_PROFITABILITY
```

Even a positive behavioral response smaller than realistic costs has no established economic significance here.

A future PnL claim requires a separately qualified execution/cost contract.

## 15. Future experiment contract — mandatory preregistration surface

Before **any performance observation**, each family experiment contract must freeze at minimum:

- experiment identity;
- instrument identity;
- source/provider identity;
- dataset identity;
- price field (`bid`, `ask`, `mid`, `last`, or explicitly defined alternative);
- H1 construction method;
- continuity segmentation;
- exact evaluation window;
- exposure status relative to E1 and the other SFE family;
- directional-event definition (must match Section 6.1);
- handling of inadmissible `t+1`;
- minimum event count;
- evidence-sufficiency gates;
- statistical procedure;
- null hypothesis treatment;
- uncertainty/confidence rule;
- multiple-testing treatment if applicable;
- exact mapping to `SUPPORTED / REFUTED / NOT_INTERPRETABLE`;
- treatment of non-decisive statistical evidence;
- treatment of unconditional market drift;
- reporting of `n_LONG` and `n_SHORT`;
- unconditional mean of `R_(t,t+1)` over the relevant admissible bar surface;
- co-firing/exclusive-event reporting when both families share evidence.

No item in this list may be selected after seeing the relevant family performance and still be represented as preregistered.

## 16. Drift and directional-imbalance disclosure

For every future experiment, publish:

```text
n_LONG
n_SHORT
mean_unconditional_R
mean_Y_LONG
mean_Y_SHORT
mean_Y_combined
```

The experiment contract must state before results how unconditional drift and directional imbalance are interpreted.

The combined `mean(Y)` may not be treated as a pure family effect without this disclosure.

SFE-01 does not prescribe a performance-enhancing correction.

It requires transparent decomposition.

## 17. Validity gates and NOT_INTERPRETABLE

### 17.1 Predeclared block-level validity gates

Before outcome interpretation, the experiment contract must freeze block-level validity criteria for:

- provenance;
- dataset identity;
- continuity;
- admissibility;
- minimum evidence;
- required fields.

These gates must be evaluated and persisted before computing the final finding status from outcome evidence.

Warmup or an individual invalid bar does not automatically make an entire block `NOT_INTERPRETABLE`; block-level treatment must be preregistered.

### 17.2 Later-discovered provenance defect

If a material provenance or integrity defect is discovered after an earlier finding:

```text
DO NOT SILENTLY REWRITE HISTORY
```

Instead:

1. preserve the original finding and evidence trail;
2. record the newly discovered defect;
3. explicitly invalidate the affected evidentiary authority where justified;
4. issue a superseding status such as:

```text
NOT_INTERPRETABLE /
POST_HOC_PROVENANCE_INVALIDATION
```

A later defect may invalidate evidence; it may not be used opportunistically to rescue an unfavorable result without documented objective basis.

## 18. Candidate finding-status semantics

Before experiment:

```text
BREAKOUT_V1 = UNTESTED
MEAN_REVERSION_V1 = UNTESTED
```

A future experiment may produce:

```text
SUPPORTED
REFUTED
NOT_INTERPRETABLE
```

with reason codes, including where applicable:

```text
NON_DECISIVE_STATISTICAL_EVIDENCE
INSUFFICIENT_EVIDENCE
PROVENANCE_FAILURE
ADMISSIBILITY_FAILURE
POST_HOC_PROVENANCE_INVALIDATION
```

The complete mapping must be frozen in the experiment contract before any performance observation.

No single result generalizes silently to other assets, sources, bar intervals, response horizons, regimes, or history.

## 19. V1 one-bar falsification target

SFE-01 freezes the **direction of the proposition**, not the full future statistical decision function.

### 19.1 BREAKOUT_V1

Target proposition:

```text
EXPECTED ONE-BAR
DIRECTIONAL RESPONSE
IN BREAKOUT DIRECTION
IS POSITIVE
```

### 19.2 MEAN_REVERSION_V1

Target proposition:

```text
EXPECTED ONE-BAR
DIRECTIONAL RESPONSE
IN REVERSION DIRECTION
IS POSITIVE
```

A future valid preregistered experiment must specify how evidence supports, refutes or fails to decide these propositions.

A refuted one-bar V1 proposition does not refute the broader family at other response horizons.

## 20. Parameter and design contamination rules

### 20.1 No post-result rescue

No post-result change to:

- lookback;
- threshold;
- bar interval;
- event definition;
- source;
- instrument;
- price field;
- window;
- segmentation;
- statistical procedure;
- validity gate;

may be used to rescue V1 under the same pristine-evidence claim.

### 20.2 New version rule

A motivated change requires:

```text
NEW VERSION
+
EXPLICIT EXPOSURE STATUS
+
NEW PREREGISTRATION
+
SEPARATE HUMAN AUTHORIZATION
```

## 21. Explicit forbidden claims

SFE-01 does not permit:

```text
BREAKOUT_V1_IS_PROFITABLE
MEAN_REVERSION_V1_IS_PROFITABLE
BREAKOUT_BEATS_MEAN_REVERSION
MEAN_REVERSION_BEATS_BREAKOUT
BEST_STRATEGY
REGIME_ROUTER_VALIDATED
SOURCE_INDEPENDENT_VALIDATION
ASSUMPTION_INDEPENDENT_VALIDATION
ROBUST_ACROSS_MARKETS
MULTI_HORIZON_VALIDATION
PRODUCTION_READY
PAPER_READY
BROKER_READY
LIVE_READY
CAPITAL_READY
```

## 22. Future qualification topology and authority firewall

If SFE-01 is later human-adopted, the candidate topology remains:

```text
SFE-02A — BREAKOUT_V1
CONTRACT
→ TEST-FIRST RED
→ MINIMAL IMPLEMENTATION
→ ADVERSARIAL BREAK
→ QUALIFICATION
→ STOP

SFE-02B — MEAN_REVERSION_V1
CONTRACT
→ TEST-FIRST RED
→ MINIMAL IMPLEMENTATION
→ ADVERSARIAL BREAK
→ QUALIFICATION
→ STOP
```

But:

```text
ADOPTION_OF_SFE_01
DOES_NOT_AUTHORIZE
SFE_02A
OR
SFE_02B
```

Each requires its own separate human authorization.

All `NOT_AUTHORIZED` statuses in Section 0 survive adoption unless separately and explicitly lifted.

No implementation, backtest or experiment follows automatically.

## 23. Comparative-study firewall

Only after separately authorized and qualified standalone work may a comparative study be proposed.

```text
SFE-03_COMPARATIVE_STUDY =
NOT_AUTHORIZED
```

No ranking is created by SFE-01.

## 24. V0.1 adversarial finding resolution matrix

The following means **addressed in this candidate**, not independently verified closed.

### SFE01-F01 — mechanical co-firing coupling

```text
RESOLUTION =
Sections 10.1–10.3 explicitly define opposite co-signal direction,
Y_BREAKOUT = -Y_MEAN_REVERSION on co-firing bars,
and mandatory co-firing/exclusive reporting.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F02 — ambiguous directional event

```text
RESOLUTION =
Section 6.1 fixes every eligible LONG/SHORT H1 bar as a directional event.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F03 — sign-only falsification ambiguity

```text
RESOLUTION =
Sections 7.8, 8.11, 18 and 19 separate predicted effect direction
from the future preregistered statistical verdict
and require a non-decisive outcome.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F04 — sequential cross-family experiment contamination

```text
RESOLUTION =
Section 4.3 requires both experiment contracts to be preregistered
before either result is observed when evidence is materially shared;
otherwise the later experiment is exposed/non-blind/exploratory.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F05 — MOMENTUM dependency and E1 overlap

```text
RESOLUTION =
Section 11 cites the exact MOMENTUM_V1 rule,
proves BREAKOUT directional events imply same-direction MOMENTUM states,
and defines E1 overlap as exposed/non-pristine.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F06 — MR arithmetic semantics

```text
RESOLUTION =
Section 8.13 requires numerical semantics and edge-case concordance
to be frozen before SFE-02B implementation.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F07 — continuity segmentation

```text
RESOLUTION =
Section 5.5 delegates an explicit causal segmentation rule
to the future dataset-identity contract
and requires reporting t+1 exclusions.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F08 — NOT_INTERPRETABLE timing / post-hoc invalidation

```text
RESOLUTION =
Section 17 freezes block-level validity gates before outcome interpretation
while preserving explicit later provenance invalidation with audit history.

STATUS =
ADDRESSED_WITH_CORRECTED_REMEDY_PENDING_RE_REVIEW
```

### SFE01-F09 — family-level overclaim / one-bar scope

```text
RESOLUTION =
Sections 7.2, 8.2 and 19 explicitly restrict the tested proposition
to one response H1 bar and deny family-wide refutation.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F10 — construct validity

```text
RESOLUTION =
Sections 7.9 and 8.12 declare:
BREAKOUT_V1 is not compression-conditioned;
MEAN_REVERSION_V1 can trigger under steady trends.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F11 — drift × directional imbalance

```text
RESOLUTION =
Sections 15 and 16 require preregistered treatment and disclosure
of n_LONG, n_SHORT and unconditional mean R.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F12 — instrument and price-field selection

```text
RESOLUTION =
Sections 5.2 and 15 make instrument identity and price field
mandatory preregistered experiment fields.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F13 — adoption authority leak

```text
RESOLUTION =
Section 22 states that SFE-01 adoption does not authorize SFE-02A/B
and all NOT_AUTHORIZED states persist.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F14 — edge cases / wording

```text
RESOLUTION =
Sections 5.3 and 5.5 require strictly positive finite closes,
strictly increasing timestamps and explicit admissible t+1.
The controlling phrase is now "before any performance observation."

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F15 — provenance / authority-independence overclaim

```text
RESOLUTION =
Section 12 changes authority-independence status to depend on adjudicator identity.
Section 9 anchors the parameter freeze to the persisted V0.2 blob.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

### SFE01-F16 — undeclared E1 concept inheritance

```text
RESOLUTION =
Section 2.3 explicitly lists candidate conceptual inheritances
and denies any E1 authority inheritance.

STATUS =
ADDRESSED_PENDING_RE_REVIEW
```

## 25. Required re-review targets

The next external reviewer must:

1. re-test all F01-F16 resolutions;
2. search for regressions introduced by V0.2;
3. verify that signal rules and parameters are unchanged;
4. independently check the algebraic coupling claims;
5. independently check the MOMENTUM subset implication;
6. challenge event semantics and contamination handling;
7. challenge future statistical-decision delegation for hidden flexibility;
8. challenge continuity and numerical-semantics delegation;
9. challenge authority boundaries after human adoption;
10. return `FAIL` if any adoption-blocking ambiguity remains.

## 26. V0.2 candidate conclusion

```text
SFE_01_V0_2 =
PRODUCED_CANDIDATE

V0_1_FINDINGS_F01_TO_F16 =
ADDRESSED_IN_TEXT
PENDING_EXTERNAL_RE_REVIEW

BREAKOUT_V1_SIGNAL_RULE =
UNCHANGED

BREAKOUT_V1_PARAMETERS =
UNCHANGED

MEAN_REVERSION_V1_SIGNAL_RULE =
UNCHANGED

MEAN_REVERSION_V1_PARAMETERS =
UNCHANGED

IMPLEMENTATION =
NOT_AUTHORIZED

BACKTEST =
NOT_AUTHORIZED

OPTIMIZATION =
NOT_AUTHORIZED

RANKING =
NOT_AUTHORIZED

ROUTER =
NOT_AUTHORIZED

REGIME_FILTER =
NOT_AUTHORIZED

NEXT_ACTION =
EXTERNAL_ADVERSARIAL_RE_REVIEW

HUMAN_ADOPTION =
NOT_YET_AUTHORIZED

STOP =
TRUE
```
