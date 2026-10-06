# AO-E0-B8-M06-02 — M06 PRE-RESULT SAMPLE-ADEQUACY PARAMETER PREREGISTRATION — QUALIFICATION

RESULT =
QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION

CONTROL =
AO-E0-B8-M06-02

SCOPE =
MOMENTUM_V1 / USTECH / H1 / CC05_ECONOMIC_NET_PROFITABILITY

## Canonical bindings

PLANNING_STDDEV =
336.4106561689863

PLANNING_STDDEV_EPISTEMIC_CLASS =
EXPOSED_E1_PLANNING_PROXY_ONLY

M06_RUNTIME_BLOB =
fce7998167745659cb0fd5d03a8de14946b0394d

M06_CONTRACT_BLOB =
618171fd013f7f9cfe39f233048e650fc276b729

B4_DELTA_MIN =
5.0 price units per closed trade

B4_DELTA_MIN_BLOB =
8cf494fcfffe0575d3e2a0fe887e2f524a3eb304

## Candidate rule

SAMPLE_ADEQUACY_MODE =
PRECISION_AND_POWER

COMBINATION_RULE =
FINAL_REQUIRED_N = MAX(PRECISION_REQUIRED_N, POWER_REQUIRED_N)

POST_RESULT_RULE_CHANGE =
FORBIDDEN

## Precision candidate

MODEL_REF =
NORMAL_MEAN_KNOWN_SIGMA

STDDEV =
336.4106561689863

HALF_WIDTH =
5.0

HALF_WIDTH_BASIS =
FROZEN B4 DELTA_MIN USED AS POLICY RESOLUTION UNIT

CONFIDENCE_LEVEL =
0.99

PRECISION_REQUIRED_N =
30036

The 0.99 confidence level is a conservative policy candidate, not a universal SMF rule.
SMF-00 explicitly forbids a universal 99% rule.

## Power candidate

The AO-E0 claim remains:

H0: theta_AO_E0 <= 5.0
H1: theta_AO_E0 > 5.0

For planning power only, the estimand is centered at the frozen null boundary:

CENTERED_EFFECT =
theta_AO_E0 - 5.0

EFFECT_SIZE =
5.0

EFFECT_SEMANTICS =
minimum design excess of one frozen DELTA_MIN policy margin above the H0 boundary

DESIGN_ALTERNATIVE_THETA =
10.0

EFFECT_SOURCE =
PREDECLARED

ALPHA =
0.01

TARGET_POWER =
0.90

ALTERNATIVE =
GREATER

MAX_N =
58927

POWER_REQUIRED_N =
58927

ACHIEVED_POWER_AT_REQUIRED_N =
0.9000043763601825

POWER_AT_N_MINUS_1 =
0.8999990037841005

The design alternative theta=10.0 is NOT a new qualification threshold.
The binding economic threshold remains theta>5.0.

## Final nominal sample adequacy

FINAL_REQUIRED_N =
58927 CLOSED TRADES

This is a nominal model-based planning count only.

NOMINAL_REQUIRED_N != EFFECTIVE_INDEPENDENT_N

M04 dependence diagnostics remain required.
No implicit IID validity is granted.
Failure of future dependence assumptions must propagate to the control state.

NORMAL_MEAN_KNOWN_SIGMA is the only currently supported M06 planning model.
Use of the adopted planning sigma as a fixed input does NOT claim the population sigma is truly known.

## Design-only sensitivity

BASELINE_95_80:
precision_n = 17390
power_n = 27988
final_n = 27988

RECOMMENDED_99_90:
precision_n = 30036
power_n = 58927
final_n = 58927

STRICT_99_95:
precision_n = 30036
power_n = 71391
final_n = 71391

No future result or exposed E1 performance value was used to select among these policy candidates.
The exposed E1 package contributes only the already-human-adopted planning sigma.

## Qualification evidence

CANDIDATE_CONTRACT_BLOB =
95a2e41c1e004e3b4461631060d8b12380983caa

QUALIFICATION_TOOL_BLOB =
766ee7fd27f6bf2f2af2699ef240c5fb44d8d0b0

EXECUTABLE_TESTS_BLOB =
c50a5a388e3acb9e91ca9f7b8849395d4a0da3d5

WORKFLOW_BLOB =
87c05d28fbc53686694a7165d0480d017194c645

INDEPENDENT_DETERMINISTIC_REPLAY =
PASS

INDEPENDENT_DYNAMIC_CHECKS =
13 / 13 PASS

CONTRACT_STATIC_AND_AUTHORITY_CHECKS =
12 / 12 PASS

TOTAL_QUALIFICATION_CHECKS =
25 / 25 PASS

GITHUB_ACTIONS_RUN_OBSERVED_AT_QUALIFICATION_TIME =
NO

The absence of an observable GitHub Actions run is NOT recorded as CI PASS.
The executable qualification surface is persisted for later rebreak.

## Epistemic firewalls

STATISTICAL_SIGNIFICANCE != ECONOMIC_RELEVANCE
MINIMUM_EFFECT_OF_INTEREST != OBSERVED_EFFECT
PLANNING_SIGMA != CONFIRMATORY_SIGMA
REQUIRED_N != STRATEGY_QUALIFICATION
POWER_TARGET_MET != EDGE_GENERALIZABLE
PRECISION_TARGET_MET != LIVE_PROFITABILITY
KNOWN_SIGMA_MODEL != POPULATION_SIGMA_KNOWN
ALPHA_0_01 != MULTIPLICITY_CORRECTION

B9 multiplicity/search-provenance controls remain separate.

## Recommendation

RECOMMENDATION =
ADOPT_CANDIDATE_IF_THE_PROJECT_ACCEPTS_THE_RESULTING_NOMINAL_SAMPLE_REQUIREMENT

Rationale:
- it introduces no performance-fitted threshold;
- it reuses the already-frozen DELTA_MIN as the only grounded policy scale;
- it preserves the one-sided direction of the exact AO-E0 claim;
- it combines precision and power by a predeclared max rule;
- relaxing the parameters merely to obtain a convenient sample size would violate the purpose of preregistration.

If 58927 closed trades is operationally unacceptable, the remedy is NOT post-hoc relaxation.
A separate pre-result decision must revisit the claim scale, supported statistical model, or evidence design.

## Preserved state

M06_PARAMETER_PREREGISTRATION =
QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION

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

STOP =
M06 PARAMETER PREREGISTRATION CANDIDATE PERSISTED
