# SFE-01 V0.2 — HUMAN ADJUDICATION — ADOPT WITH AMENDMENTS

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`

## 0. Human decision

The human authority explicitly decided:

```text
SFE-01 V0.2 =
ADOPT_WITH_AMENDMENTS
```

This adjudication adopts the documentary strategy-family definition contained in:

```text
GOVERNANCE/SFE-01-DUAL-STRATEGY-FAMILY-DEFINITION-CANDIDATE-V0.2.md

BLOB =
027c42b38bf9c74415b21e98bcce19124f744995
```

subject to the binding amendments in this adjudication.

The V0.2 source blob remains immutable.  
This adjudication file is the normative amendment layer.

Therefore the adopted object is:

```text
SFE_01_ADOPTED_DEFINITION =
V0.2_BLOB
+
THIS_HUMAN_ADJUDICATION
```

## 1. Fresh-verified persistence base

Immediately before persistence:

```text
HEAD =
ac9edbbe5638c903faa88f579f8f854061be935e

TREE =
5e76da01d7091f5dae218ecbfd56c20f5e03ab8c

V0_2_BLOB =
027c42b38bf9c74415b21e98bcce19124f744995

V0_2_REVIEW_PACKAGE_BLOB =
30b912bb4eec08aead03847f7f5b39aade046c80

ARCHITECTURE_V2_ADJUDICATION_BLOB =
1817969d1b2431be3476a7ab4b52b61e8f5da172

REPOSITORY_SAFETY_RULES_BLOB =
b69f3cfab5318b950d70d4310bb763f08ef9d374
```

External V0.2 re-review supplied by the human:

```text
MODEL =
Claude Opus 5.5

SOURCE_BLOB_REVIEWED =
027c42b38bf9c74415b21e98bcce19124f744995

OVERALL_VERDICT =
PASS_WITH_NON_BLOCKING_FINDINGS

RAW_REVIEW_SHA256 =
26901a9596c7f00fc6e6137f41c2450ccb3878bd7e5b6fc26b9ef859458b8f06
```

The reviewer also reported weak independence because the V0.1 and V0.2 reviews came from the same model lineage. This review is therefore advisory evidence, not independent scientific validation.

## 2. Adoption scope

This adoption establishes only that:

1. BREAKOUT_V1 and MEAN_REVERSION_V1 are sufficiently specified as documentary candidate family definitions;
2. their frozen signal rules and parameters may serve as the basis for separately authorized downstream contracts;
3. the residual findings listed below become binding downstream obligations;
4. no performance, profitability, robustness, implementation, execution or production claim is created.

It does not establish that either family works.

## 3. Frozen strategy rules and parameters

### 3.1 BREAKOUT_V1

```text
BAR_INTERVAL = H1
LOOKBACK = 20

U_t = max(C_(t-20), ..., C_(t-1))
L_t = min(C_(t-20), ..., C_(t-1))

C_t > U_t → LONG
C_t < L_t → SHORT
otherwise → NEUTRAL
```

Ties remain NEUTRAL.

### 3.2 MEAN_REVERSION_V1

```text
BAR_INTERVAL = H1
LOOKBACK = 20
Z_THRESHOLD = 1.0
SIGMA_DENOMINATOR = 20

MU_t =
mean(C_(t-20) ... C_(t-1))

SIGMA_t =
population_std(C_(t-20) ... C_(t-1))

Z_t =
(C_t - MU_t) / SIGMA_t

Z_t <= -1.0 → LONG
Z_t >= +1.0 → SHORT
otherwise → NEUTRAL
```

No signal rule or numerical parameter is changed by this adjudication.

## 4. Resolution of the V0.2 external re-review

The human accepts the review conclusion:

```text
BREAKOUT_V1_DEFINITION =
READY_FOR_HUMAN_ADJUDICATION

MEAN_REVERSION_V1_DEFINITION =
READY_FOR_HUMAN_ADJUDICATION

SFE_01_V0_2_AS_A_WHOLE =
READY_FOR_HUMAN_ADJUDICATION
```

and adopts V0.2 with the amendments below.

### 4.1 Closed prior findings

The following are accepted as closed within the SFE-01 documentary surface:

```text
F01 = CLOSED
F02 = CLOSED
F03 = CLOSED
F06 = CLOSED
F07 = CLOSED
F09 = CLOSED
F10 = CLOSED
F13 = CLOSED
F15 = CLOSED
F16 = CLOSED
```

### 4.2 Residual findings converted to binding downstream obligations

The following are not treated as reasons to reopen the frozen strategy definitions.  
They are binding requirements for any future experiment/data/implementation contract that touches their surface:

```text
F04-R
F05-R
F08-R
F11-R
F12-R
F14-R
N01
N02
N03
N04
N05
N07
N08
N09
```

### 4.3 N06 resolved by canonical repository evidence

The external reviewer marked N06 because it could not verify whether Architecture V2 had been adopted.

Canonical repository evidence establishes:

```text
GOVERNANCE/ATDS-ARCHITECTURE-V2-HUMAN-ADJUDICATION-2026-10-01.md

BLOB =
1817969d1b2431be3476a7ab4b52b61e8f5da172

STATUS =
HUMAN_ADOPTED_WITH_AMENDMENTS
```

Therefore:

```text
N06 =
CLOSED / NOT_APPLICABLE
```

No Architecture V2 authority ambiguity remains on this point.

## 5. Binding amendment A — exposure is semantic, not merely identical-data overlap

A future experiment must not define exposure only by exact equality of source, instrument or date window.

If the design of a later experiment is materially informed by an earlier result, including through:

- a correlated instrument;
- an adjacent window;
- a closely related source;
- a structurally linked family;
- any inspected evidence capable of informing parameter, source, window or statistical choices;

then the later experiment must declare that exposure.

```text
WHEN EXPOSURE STATUS IS REASONABLY UNCERTAIN
→ DEFAULT = EXPOSED
```

No evidence may be called pristine merely because its instrument name or exact timestamps differ.

## 6. Binding amendment B — E1 overlap default for both SFE families

Any future SFE evaluation window that overlaps observations already inspected under E1 is:

```text
E1_EXPOSED
BY DEFAULT
```

for both BREAKOUT_V1 and MEAN_REVERSION_V1.

A claim that such evidence remains pristine requires separate explicit human adjudication before performance observation.

This rule is stricter than the minimum V0.2 wording for MEAN_REVERSION_V1 and closes the residual discretion identified in F05-R.

## 7. Binding amendment C — symmetry of post-result integrity audits

Any post-result search for provenance, data-integrity or admissibility defects must be governed symmetrically.

Before such an audit can affect evidentiary authority, persist:

- the audit trigger;
- audit scope;
- date/time or commit identity;
- checks to be performed;
- the rule for applying the same class of audit regardless of whether the observed result was favorable or unfavorable.

```text
SUPPORTED_RESULT
AND
REFUTED_RESULT

MUST NOT RECEIVE
ASYMMETRIC INTEGRITY SCRUTINY
```

A real later-discovered defect may still invalidate evidence, but the audit trail must show that it was not a post-hoc rescue mechanism.

## 8. Binding amendment D — primary proposition uses raw zero reference

The adopted primary behavioral proposition for each V1 family remains:

```text
PRIMARY_EFFECT_REFERENCE =
RAW_ZERO
```

Thus the primary directional target remains:

```text
mean(Y) > 0
```

subject to the future preregistered statistical decision rule.

Any adjustment for unconditional market drift is:

```text
SECONDARY_ANALYSIS
```

unless a separately versioned future strategy/experiment definition explicitly changes the proposition under separate human authority.

For the required unconditional drift diagnostic:

```text
UNCONDITIONAL_R_SURFACE =
all valid consecutive admissible H1 transitions
inside the declared evaluation block
after predeclared dataset-validity filters,
regardless of SFE signal state
```

No signal-conditioned subset may be relabeled "unconditional".

## 9. Binding amendment E — mandatory data-construction fields

Before any SFE performance observation, the future dataset/experiment contract must freeze at minimum:

- instrument identity;
- source/provider identity;
- price field;
- tick/observation cleaning policy;
- outlier policy;
- exact tick/observation-to-close construction rule;
- H1 boundary alignment;
- timezone convention;
- daylight-saving handling if relevant;
- missing-interval policy;
- forward-fill policy;
- futures roll/adjustment policy if relevant;
- continuity segmentation;
- duplicate-timestamp handling.

A field that is not applicable must be explicitly marked `NOT_APPLICABLE`; it may not be silently omitted.

## 10. Binding amendment F — no synthetic close from an empty interval

For SFE evidence:

```text
NO PRIMARY OBSERVATION
INSIDE A BAR INTERVAL
→ NO ADMISSIBLE OBSERVED CLOSE
```

A carried-forward price is not an observed close unless a future separately authorized contract explicitly defines and justifies a synthetic representation.

Default:

```text
FORWARD_FILL =
FORBIDDEN
```

A continuity block begins with:

```text
continuity_ordinal = 0
```

The future dataset-validity contract must explicitly define the scope and consequence of duplicate timestamps.

## 11. Binding amendment G — protected evidence from other experiments

A dataset/window reserved for another preregistered confirmatory experiment, including E1-TD or C01 where applicable, may not be consumed by SFE merely because SFE has a separate experiment identity.

Before use of any reserved evidence:

```text
SEPARATE HUMAN AUTHORIZATION REQUIRED
```

and the act must explicitly state whether it:

- consumes the reserved evidence;
- changes its pristine/confirmatory status;
- creates cross-program exposure.

Default:

```text
RESERVED_CONFIRMATORY_EVIDENCE
IS NOT AVAILABLE TO SFE
```

## 12. Binding amendment H — primary decision surface

For each V1 family, the primary experiment verdict must concern:

```text
ALL_DIRECTIONAL_EVENTS
```

as frozen by SFE-01.

Co-firing, exclusive, LONG-only, SHORT-only and other subsets are descriptive by default.

They may become decision-bearing only when:

1. explicitly preregistered before performance observation;
2. their role in the decision rule is stated;
3. multiplicity is handled where more than one inferential claim is made.

The phrase:

```text
multiple-testing treatment if applicable
```

must not be used to decide applicability after seeing results.

## 13. Binding amendment I — statistical unit and clustered dependence

A future evidence-sufficiency contract must specify:

- statistical unit;
- dependence structure assumed;
- treatment of serial dependence;
- treatment of clustered/persistent directional events;
- effective-sample-size method or other justified dependence-aware sufficiency rule.

```text
RAW_EVENT_COUNT
ALONE
IS NOT SUFFICIENT
```

when events are materially clustered.

## 14. Binding amendment J — diagnostics for inadmissible t+1 exclusions

If directional events are excluded because `t+1` is inadmissible, the future experiment must preregister diagnostics sufficient to detect systematic missingness, including at least:

- number and fraction excluded;
- temporal distribution;
- relation to continuity breaks;
- relation to observable volatility/context available without using forbidden future information.

The exclusion mechanism must not be assumed missing-at-random without evidence.

## 15. Binding amendment K — no performance observation before persisted preregistration

Effective immediately:

```text
PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED
```

For SFE this includes, without limitation:

- calculating `Y` on real evaluation data;
- computing mean `Y`;
- examining strategy-conditioned returns;
- exploratory notebooks that reveal SFE performance;
- informal/manual inspection that exposes the same result surface.

A future preregistration is valid only when:

```text
CONTRACT =
PERSISTED CANONICAL ARTIFACT

AND

CONTRACT COMMIT
PRECEDES
ANY AUTHORIZED PERFORMANCE CALCULATION
```

The ordering must be externally auditable.

## 16. Binding amendment L — numerical semantics for both implementations

Before implementation:

### BREAKOUT_V1 / SFE-02A must freeze

- input price representation;
- numeric precision/type;
- exact comparison semantics;
- equality/tie handling after data construction.

### MEAN_REVERSION_V1 / SFE-02B must freeze

the V0.2 numerical obligations for mean, population variance, square root, threshold comparison and zero-dispersion handling.

Neither implementation may select numerical semantics after performance observation.

## 17. Binding amendment M — reporting category refinement

If future reporting uses "exclusive" events, it must distinguish at minimum:

```text
OTHER_FAMILY = NEUTRAL
```

from:

```text
OTHER_FAMILY = UNDEFINED
```

so undefinedness is not silently merged with genuine non-signal behavior.

## 18. Binding amendment N — parameter-freeze provenance

The earliest persisted evidence currently identified for the unchanged V1 parameters is:

```text
SFE-01 V0.1 BLOB =
99d1698d303797b25ed7c140c5ad43f276cefe2c
```

The current adopted documentary definition is anchored by:

```text
SFE-01 V0.2 BLOB =
027c42b38bf9c74415b21e98bcce19124f744995
```

Therefore:

```text
EARLIEST_PARAMETER_FREEZE_EVIDENCE =
V0.1

CURRENT_ADOPTED_DEFINITION_SOURCE =
V0.2 + THIS ADJUDICATION
```

## 19. Preserved scientific limits

Adoption does not mean:

```text
BREAKOUT_V1_SUPPORTED
MEAN_REVERSION_V1_SUPPORTED
BREAKOUT_V1_PROFITABLE
MEAN_REVERSION_V1_PROFITABLE
BREAKOUT_BEATS_MEAN_REVERSION
MEAN_REVERSION_BEATS_BREAKOUT
ROBUST
SOURCE_INDEPENDENT
REGIME_VALIDATED
PRODUCTION_READY
```

Both remain:

```text
UNTESTED
```

with respect to future authorized SFE experiments.

## 20. Authority firewall after adoption

This adoption does **not** authorize:

```text
SFE-02A
SFE-02B
IMPLEMENTATION
BACKTEST
PERFORMANCE_OBSERVATION
OPTIMIZATION
RANKING
ROUTER
REGIME_FILTER
MOMENTUM_V1_MODIFICATION
E1_OR_E1_TD_MODIFICATION
TD03B_CONSUMPTION
A0
C01_REAL
UU-P1
UU-P2
UU-P3
P22-04
MT5
PAPER
BROKER
LIVE
CAPITAL
```

Every future authority remains separate.

## 21. Adopted state

```text
SFE_01_V0_2 =
HUMAN_ADOPTED_WITH_AMENDMENTS

BREAKOUT_V1_DEFINITION =
HUMAN_ADOPTED
UNTESTED

MEAN_REVERSION_V1_DEFINITION =
HUMAN_ADOPTED
UNTESTED

SIGNAL_RULE_CHANGE =
NONE

PARAMETER_CHANGE =
NONE

V0_2_EXTERNAL_REVIEW =
PASS_WITH_NON_BLOCKING_FINDINGS

RESIDUAL_FINDINGS =
BOUND_AS_DOWNSTREAM_OBLIGATIONS

ARCHITECTURE_V2_STATUS =
HUMAN_ADOPTED_WITH_AMENDMENTS

PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

SFE_02A =
NOT_AUTHORIZED

SFE_02B =
NOT_AUTHORIZED

NEXT_ACTION =
HUMAN CHOICE OF WHICH SEPARATE DOWNSTREAM CONTRACT TO AUTHORIZE

STOP =
TRUE
```
