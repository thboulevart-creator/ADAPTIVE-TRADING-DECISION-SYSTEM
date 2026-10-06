# AO-E0-B8-SMF-01 — PRE-RESULT M04/M05/M07/M08 MATERIAL CONFIGURATION PREREGISTRATION — QUALIFICATION

RESULT =
QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION

CONTROL =
AO-E0-B8-SMF-01

SCOPE =
MOMENTUM_V1 / USTECH / H1 / CC05_ECONOMIC_NET_PROFITABILITY

## Binding blocker being remediated

B8-02 EXACT BLOCKER =
BLOCKED_B8_PRE_RESULT_SMF_NUMERIC_CONFIGURATION_INCOMPLETE

B8-02 BLOCKER BLOB =
821d0b033e6bb993e64832d2fa0c2e84de24872e

B8-02 QUALIFICATION RECEIPT =
2867b3753d53ddc26732850f41e77e9cb3ab310c

## Candidate configuration

### M04

ACF_ESTIMATOR =
ADJUSTED

LAGS_POLICY =
L = min(n - 1, ceil(n^(1/3)))
LAGS = [1,2,...,L]

AT M06 NOMINAL N = 58927:
MAX_LAG = 39
LAG_COUNT = 39

ABSOLUTE_THRESHOLD =
0.05

Rationale:
- ADJUSTED corrects the pair-count attenuation across positive lags inside the already-qualified runtime surface.
- The lag horizon grows sublinearly with n and is fixed by a deterministic rule, eliminating post-result lag selection.
- 0.05 is a pre-result material-dependence threshold, not a significance cutoff.
- As a scale heuristic only, rho=0.05 corresponds to about 1.105 variance inflation under a simple AR(1) approximation.
- AR(1) is not assumed and independence is never claimed from low ACF.

STRUCTURAL_FLAGS =
INDEPENDENT EVIDENCE

LOW_ACF_WITHIN_TESTED_LAGS
!=
INDEPENDENCE_PROVEN

### M05

SCHEME_POLICY =
MOVING_BLOCK_ONLY_FOR_AO_E0_WHEN_M05_EXECUTES

IID ROUTE =
NOT USED BY THIS AO-E0 CANDIDATE

INTERVAL_METHOD =
PERCENTILE

CONFIDENCE_LEVEL =
0.99

REPLICATIONS =
50000

SEED =
21449402

SEED DERIVATION =
sha256('AO-E0-B8-SMF-01/M05/V0.1')[0:8] modulo (2^31-1)

BLOCK_LENGTH_POLICY =
block_length = min(n, 1 + max(M04_LAGS(n)))

AT M06 NOMINAL N = 58927:
BLOCK_LENGTH = 40

UNRESOLVED_NONSTATIONARITY =
BLOCK_GLOBAL_RESAMPLING

Rationale:
- fixed MOVING_BLOCK routing removes any post-result IID-versus-block choice;
- PERCENTILE is selected prospectively and is not chosen after observing interval favorability;
- 0.99 is an autonomous AO-E0 uncertainty policy for the qualification claim; it is numerically equal to M06 confidence but is not inherited from M06;
- 50000 replications give an expected 250 replicate means in each 0.5% tail of a 99% interval while limiting the cost of the current pure-Python runtime;
- seed is reproducibility-only;
- block length is generated from n and the already-frozen M04 lag rule only, never from observed performance or CI favorability.

MORE_REPLICATIONS
!=
MODEL_VALIDITY

SEED
!=
STATISTICAL_ASSUMPTION

### M07

MATERIALITY_ABS_DELTA =
5.0

Rationale:
M07 measures leave-one-dependence-unit-out change in the same mean-PnL units as the AO-E0 economic claim. A shift equal to the already-frozen 5.0-unit economic materiality scale is treated as materially concentrated evidence.

This is a separate M07 policy decision.

DELTA_MIN
!=
AUTOMATIC_M07_THRESHOLD

SIGN_REVERSAL =
SEPARATE SIGNAL

AUTOMATIC_OUTLIER_DELETION =
FORBIDDEN

### M08

MAX_INCLUSION_RATE_GAP =
0.05

Rationale:
An absolute five-percentage-point inclusion-rate gap across declared strata is treated prospectively as material sample-selection asymmetry for this qualification-critical claim.

This is:
- not a p-value threshold;
- not calibrated from the future observed gap;
- not proof of causal selection bias.

OBSERVED_GAP
!=
THRESHOLD_SOURCE

## No-silent-inheritance review

M06_CONFIDENCE_LEVEL =
0.99

M05_CONFIDENCE_LEVEL =
0.99

The equality is intentional but semantic inheritance is FALSE.

M05 0.99 is separately justified as the uncertainty level for the AO-E0 confirmatory qualification CI.

DELTA_MIN =
5.0

M07_MATERIALITY_ABS_DELTA =
5.0

The equality is intentional but automatic inheritance is FALSE.

M07 5.0 is separately justified because the influence statistic and the AO-E0 estimand are expressed in the same mean-PnL units and the purpose of M07 is to detect economically material concentration.

## Synthetic/adversarial qualification

INDEPENDENT_LOCAL_SYNTHETIC_REPLAY =
PASS

INDEPENDENT_LOCAL_CHECKS =
20 / 20 PASS

Covered:
- n-dependent lag and block rules;
- material dependence detection;
- structural-flag precedence;
- no independence claim from low tested ACF;
- unsupported/empty/duplicate/invalid M04 inputs;
- deterministic MOVING_BLOCK bootstrap;
- unresolved nonstationarity fail-closed;
- IID without explicit justification fail-closed;
- invalid M05 method/confidence/replications/seed/block;
- exact M07 materiality behavior;
- invalid M07 threshold;
- exact M08 inclusion-gap behavior;
- invalid/missing M08 inputs.

CANONICAL_EXECUTABLE_TESTS =
PERSISTED

CANONICAL_TEST_BLOB =
210d0cb4044dc0c943e572d0b837ba543534d2ab

QUALIFICATION_TOOL_BLOB =
cb1c75e2d3311e113f18b2d304ed41fc7cafc9c6

WORKFLOW_BLOB =
d9ced6ee829b7fc4d89460bb61c9fb7a669eb739

GITHUB_ACTIONS_RUN_OBSERVED_AT_QUALIFICATION_TIME =
NO

CI_PASS_CLAIMED =
NO

The absence of an observable Actions run is not converted into CI evidence.

## No-free-material-parameter check

M04 estimator =
BOUND BY CANDIDATE

M04 lags =
BOUND BY DETERMINISTIC RULE

M04 absolute threshold =
BOUND BY CANDIDATE

M05 scheme routing =
BOUND TO MOVING_BLOCK FOR AO-E0

M05 interval method =
BOUND BY CANDIDATE

M05 confidence level =
BOUND BY CANDIDATE

M05 replications =
BOUND BY CANDIDATE

M05 seed =
BOUND BY CANDIDATE

M05 block length =
BOUND BY DETERMINISTIC RULE

M07 materiality_abs_delta =
BOUND BY CANDIDATE

M08 max_inclusion_rate_gap =
BOUND BY CANDIDATE

POST_RESULT_DISCRETION_ON_LISTED_PARAMETERS =
NONE

## Preserved state

M06 =
HUMAN_ADOPTED / BINDING / FROZEN / UNMODIFIED

FINAL_REQUIRED_N =
58927

M04/M05/M07/M08 CONFIGURATION =
NOT_HUMAN_ADOPTED

B8 =
BLOCKED

B12 =
CLOSED

AO_E0_EXECUTION =
NOT_AUTHORIZED

FORWARD_DATA_OBSERVATION =
NOT_AUTHORIZED

REAL_PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

AO-E0-B8-02 =
NOT_RERUN

## Recommendation

RECOMMENDATION =
ADOPT_EXACT_CANDIDATE

The candidate removes the post-result discretion identified by B8-02 without using any real AO-E0 result and without changing M06, DELTA_MIN, F2_S4, strategy identity, or cost scope.

A separate human decision is required before these values become binding.

STOP =
SMF MATERIAL CONFIGURATION CANDIDATE PERSISTED
