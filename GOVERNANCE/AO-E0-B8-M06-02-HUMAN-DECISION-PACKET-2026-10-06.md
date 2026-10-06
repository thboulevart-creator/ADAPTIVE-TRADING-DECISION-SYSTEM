# AO-E0-B8-M06-02 — HUMAN DECISION PACKET

STATUS =
QUALIFIED_CANDIDATE / HUMAN_DECISION_PENDING

CONTROL =
AO-E0-B8-M06-02 — M06 PRE-RESULT SAMPLE-ADEQUACY PARAMETER PREREGISTRATION V0.1

## Candidate proposed for adoption

SAMPLE_ADEQUACY_MODE =
PRECISION_AND_POWER

MODEL_REF =
NORMAL_MEAN_KNOWN_SIGMA

PLANNING_STDDEV =
336.4106561689863

PLANNING_STDDEV_EPISTEMIC_CLASS =
EXPOSED_E1_PLANNING_PROXY_ONLY

PRECISION_HALF_WIDTH =
5.0

CONFIDENCE_LEVEL =
0.99

PRECISION_REQUIRED_N =
30036

POWER_EFFECT_SIZE =
5.0

POWER_EFFECT_SOURCE =
PREDECLARED

POWER_EFFECT_SEMANTICS =
minimum design excess above the frozen H0 boundary theta=5.0

DESIGN_ALTERNATIVE_THETA =
10.0

ALPHA =
0.01

TARGET_POWER =
0.90

ALTERNATIVE =
GREATER

POWER_MAX_N =
58927

POWER_REQUIRED_N =
58927

COMBINATION_RULE =
FINAL_REQUIRED_N = MAX(PRECISION_REQUIRED_N, POWER_REQUIRED_N)

FINAL_REQUIRED_N =
58927

## Required interpretation

The frozen AO-E0 economic threshold remains:

H0: theta_AO_E0 <= 5.0
H1: theta_AO_E0 > 5.0

theta=10.0 is a POWER DESIGN ALTERNATIVE only.
It is NOT a new economic qualification threshold.

FINAL_REQUIRED_N is a NOMINAL MODEL-BASED PLANNING COUNT.
It is NOT a claim of effective independent sample size.
M04 remains required and future dependence findings must propagate.

0.99 confidence is a candidate policy choice, not a universal SMF rule.
alpha=0.01 is not a multiplicity correction.

## Qualification

M06_PARAMETER_PREREGISTRATION =
QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION

QUALIFICATION_CHECKS =
25 / 25 PASS

GITHUB_ACTIONS_RUN_OBSERVED =
NO

CI_PASS_CLAIMED =
NO

CANONICAL_EXECUTABLE_TESTS =
PERSISTED

## Recommendation

RECOMMENDED_HUMAN_DECISION =
ADOPT

Reason:
this is the strongest currently grounded configuration that does not fit parameters to observed performance and does not weaken the already-frozen economic materiality scale merely to make required_n convenient.

The resulting 58927 nominal closed trades is a material operational warning.
If that requirement is unacceptable, reject this candidate and open a separate pre-result redesign decision.
Do NOT lower the statistical parameters after observing results.

## Human choices

OPTION_A =
ADOPT EXACT CANDIDATE

OPTION_B =
REJECT WITHOUT SUBSTITUTING PARAMETERS

No automatic adoption is authorized.

B8 =
BLOCKED_PENDING_DISTINCT_HUMAN_ADOPTION

B12 =
CLOSED

AO_E0_EXECUTION =
NOT_AUTHORIZED

FORWARD_DATA_OBSERVATION =
NOT_AUTHORIZED

REAL_PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

FORCE =
FALSE
