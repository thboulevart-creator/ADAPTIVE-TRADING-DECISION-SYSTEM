# AO-E0-B8-DR-01 — FINAL QUALIFICATION DECISION RULE — QUALIFICATION V0.1

RESULT =
QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION

CONTROL =
AO-E0-B8-DR-01

BLOCKER TARGET =
BLOCKED_B8_FINAL_QUALIFICATION_DECISION_RULE_NOT_PREREGISTERED

## Exact candidate

CANDIDATE BLOB =
7b08d0af9cb733be186ddc2f4fa6ca22768284fd

DECISION TABLE BLOB =
1126cf429dc064104bdfe0615cea0a96b95b540e

RUNTIME BLOB =
bcf4b8541a7c223ee52f990e6dee621e1d83baa9

TESTS BLOB =
952f9f4b97e626495608517ccdde734694aa3a5e

## Final decision semantics

M05 CI interpretation:

lower > 5.0
→ SUPPORT signal

upper <= 5.0
→ REFUTE signal

otherwise
→ INCONCLUSIVE signal

POINT_ESTIMATE > 5
!=
AUTOMATIC SUPPORT

M06:

n < 58927
→ INCONCLUSIVE / INSUFFICIENT_SAMPLE

n >= 58927
→ SAMPLE ADEQUACY GATE PASS ONLY

N >= 58927
!=
SUPPORT

N >= 58927
!=
QUALIFIED

M07:

MATERIAL_INFLUENCE = TRUE
→ INCONCLUSIVE

SIGN_REVERSAL = TRUE
→ INCONCLUSIVE

M08:

MATERIAL_SELECTION_ASYMMETRY = TRUE
→ INCONCLUSIVE

NONSTATIONARITY:

stationarity_status != RESOLVED_FOR_RESAMPLING
→ INCONCLUSIVE / NONSTATIONARITY_UNRESOLVED

F2_S4:

COST_ROBUSTNESS_INCONCLUSIVE
→ INCONCLUSIVE

M05 SUPPORT + F2_S4 PASS
→ SUPPORT if every mandatory validity gate is clean

M05 SUPPORT + F2_S4 FAIL
→ INCONCLUSIVE / EVIDENCE CONFLICT

M05 REFUTE + F2_S4 FAIL
→ REFUTE if every mandatory validity gate is clean

M05 REFUTE + F2_S4 PASS
→ INCONCLUSIVE / EVIDENCE CONFLICT

The source COST_ROBUSTNESS_FAIL state is not alone sufficient to produce REFUTE because its existing semantics combine REFUTED_OR_NOT_SUPPORTED.

## Multiplicity / provenance decision

BOUND STATE =
CONTAMINATED / PARTIAL_SEARCH_UNIVERSE / n_trials=null

Under the already-frozen NEW_FORWARD_DATA_ONLY confirmation route:

PARTIAL_SEARCH_UNIVERSE =
MANDATORY QUALIFICATION LIMITATION
NOT A NUMERIC MULTIPLICITY CORRECTION
NOT A PRISTINE-HYPOTHESIS CLAIM

Mandatory limitations on SUPPORT:

- PRIOR_SEARCH_UNIVERSE_PARTIAL
- N_TRIALS_UNKNOWN
- ALPHA_NOT_MULTIPLICITY_CORRECTED
- HYPOTHESIS_ORIGIN_NOT_PRISTINE

Rationale:
the future confirmation slice is new and the decision rule is frozen before that slice is observed. The historical unknown search universe therefore remains visible provenance context but is not converted into an invented n_trials or post-hoc correction.

## Final qualification mapping

SUPPORT
→ QUALIFIED
→ reason = SUPPORTED_NEW_FORWARD_CC05_WITH_PARTIAL_PRIOR_SEARCH_UNIVERSE

REFUTE
→ NOT_QUALIFIED
→ reason = REFUTED_BY_VALID_FORWARD_CI_AND_COST_ROBUSTNESS_FAIL

INCONCLUSIVE
→ NOT_QUALIFIED
→ exact primary inconclusive reason
→ all simultaneous material reasons preserved

INCONCLUSIVE
!=
REFUTED

INCONCLUSIVE
!=
QUALIFIED

## Precedence / no-rescue rule

Any unresolved validity/information blocker prevents SUPPORT and REFUTE.

Fixed precedence begins with:
1. provenance route/binding mismatch;
2. insufficient sample;
3. unresolved nonstationarity;
4. blocked M05 inference;
5. M07 sign reversal;
6. M07 material influence;
7. M08 material selection asymmetry;
8. F2_S4 inconclusive;
9. M05 overlap;
10. M05/F2 conflict.

Only after those gates are clean can direct aligned evidence produce REFUTE or SUPPORT.

FAVORABLE_DIAGNOSTIC
!=
AUTHORITY_TO_OVERRIDE_GATE

All simultaneously triggered reasons remain recorded even though one fixed primary reason is selected.

## No new numeric thresholds

NEW_NUMERIC_THRESHOLDS_INTRODUCED =
NO

Only already-frozen values are used:

DELTA_MIN =
5.0

M06_FINAL_REQUIRED_N =
58927

No additional p-value, spread, influence, attrition, multiplicity or confidence threshold was created by DR-01.

## Synthetic / adversarial qualification

INDEPENDENT_LOCAL_REPLAY =
22 / 22 PASS

Covered:
- exact SUPPORT path;
- SUPPORT creates no authority;
- exact REFUTE path;
- CI overlap;
- boundary equality semantics;
- insufficient sample;
- required_n does not auto-support;
- unresolved nonstationarity;
- M07 material influence;
- M07 sign reversal;
- M08 asymmetry;
- F2_S4 inconclusive;
- M05-support/F2-fail conflict;
- M05-refute/F2-pass conflict;
- old OOS route rejection;
- invented n_trials rejection;
- search-universe relabel rejection;
- mandatory provenance limitations;
- multi-failure preservation;
- invalid interval fail-closed.

CANONICAL_EXECUTABLE_TESTS =
PERSISTED

CI_PASS_CLAIMED =
NO

## No-free-material-decision check

SUPPORT mapping =
FROZEN BY CANDIDATE

REFUTE mapping =
FROZEN BY CANDIDATE

INCONCLUSIVE mapping =
FROZEN BY CANDIDATE

M06 disposition =
FROZEN BY CANDIDATE

F2_S4 disposition =
FROZEN BY CANDIDATE

M07 disposition =
FROZEN BY CANDIDATE

M08 disposition =
FROZEN BY CANDIDATE

NONSTATIONARITY disposition =
FROZEN BY CANDIDATE

MULTIPLICITY disposition =
FROZEN BY CANDIDATE

PRECEDENCE =
FROZEN BY CANDIDATE

MULTI_FAILURE behavior =
FROZEN BY CANDIDATE

QUALIFICATION_STATUS mapping =
FROZEN BY CANDIDATE

QUALIFICATION_REASON mapping =
FROZEN BY CANDIDATE

POST_RESULT_MATERIAL_DISCRETION_ON_THIS_SURFACE =
NONE IDENTIFIED

## Authority

DR01_RULE =
NOT_HUMAN_ADOPTED

DECISION =
PENDING_HUMAN_PROMOTION

DECISION_AUTHORITY =
NONE

B8 =
BLOCKED

B12 =
CLOSED

AO-E0-B8-02 =
NOT_RERUN

AO_E0_EXECUTION =
NOT_AUTHORIZED

FORWARD_DATA_OBSERVATION =
NOT_AUTHORIZED

OOS_CONSUMPTION =
NOT_AUTHORIZED

REAL_PERFORMANCE_OBSERVATION =
NOT_AUTHORIZED

REAL_SMF_EXECUTION =
NOT_AUTHORIZED

## Recommendation

RECOMMENDATION =
ADOPT EXACT DR-01 CANDIDATE

Only a separate human decision may make this rule binding.

After such adoption, AO-E0-B8-02 may be separately authorized for a new rerun.

FORCE =
FALSE

STOP =
FINAL QUALIFICATION DECISION RULE CANDIDATE PERSISTED
