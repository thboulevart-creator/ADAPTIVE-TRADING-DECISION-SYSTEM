# AO-E0-M06-AMEND-01 — ROOT-CAUSE + ROUTE-SELECTION ANALYSIS V0.1

STATUS =
PROSPECTIVE_ANALYSIS_COMPLETE / CANDIDATE_FOR_TECHNICAL_QUALIFICATION

SCOPE =
MOMENTUM_V1 / USTECH / H1 / CC05_ECONOMIC_NET_PROFITABILITY

This analysis is pre-result and does not modify M06, DATA-01, DR-01 or B12.

## Frozen question

M06 currently binds:

ESTIMAND =
mean all-in net realized unit PnL per closed OOS/forward trade at F2_S4

H0 =
theta_AO_E0 <= 5.0

H1 =
theta_AO_E0 > 5.0

PLANNING_SIGMA =
336.4106561689863

PRECISION HALF-WIDTH =
5.0

CONFIDENCE =
0.99

POWER EFFECT =
5.0 above the H0 boundary

ALPHA =
0.01

TARGET POWER =
0.90

FINAL_REQUIRED_N =
58927 closed trades

## 1. Arithmetic audit

The frozen normal-mean planning mathematics recomputes exactly:

PRECISION_REQUIRED_N =
30036

POWER_REQUIRED_N =
58927

FINAL_REQUIRED_N =
58927

ARITHMETIC_ERROR =
FALSE

The 58,927 value is therefore not a coding or arithmetic defect under the frozen planning model.

The design effect-to-dispersion ratio is:

5.0 / 336.4106561689863 =
0.014862787216491717

The resulting information requirement is intrinsically large under the selected planning assumptions.

## 2. Sample-unit audit

The binding estimand is explicitly per CLOSED TRADE.

Therefore:

CLOSED_TRADE_SAMPLE_UNIT_MATCHES_CURRENT_ESTIMAND =
TRUE

Replacing closed trades by H1 decision bars would change the statistical observation unit without a demonstrated estimand-preserving mapping.

H1_SAMPLE_UNIT_SUBSTITUTION =
REJECT_FOR_CURRENT_ESTIMAND

This is not the primary defect.

## 3. Dependence audit

M06 already states:

NOMINAL_REQUIRED_N != EFFECTIVE_INDEPENDENT_N

and:

M04 dependence diagnostics remain required.

AO-E0-B8-SMF-01 also prospectively routes AO-E0 through:
- M04 dependence diagnostics;
- deterministic n-dependent lag rules;
- MOVING_BLOCK M05 inference;
- no implicit IID route.

Therefore:

DEPENDENCE_OMITTED =
FALSE

58927_IS_EFFECTIVE_INDEPENDENT_N_CLAIM =
FALSE

The dependence problem remains important for final validity, but it is not the newly discovered root cause.

## 4. Terminal-rule translation audit

M06 qualifies 58,927 as:

NOMINAL_MODEL_BASED_PLANNING_COUNT_ONLY

The DATA-01 formation rule later converts that number into:

FIRST_GOVERNED_DECISION_BOUNDARY_AT_OR_AFTER_58927_ADMISSIBLE_CLOSED_FORWARD_TRADES

This creates a stronger operational requirement than the epistemic wording of M06 itself.

M06's nominal planning target becomes a mandatory data-acquisition terminal count even though:
- it is not an effective-independent-N claim;
- dependence validity is separately evaluated;
- reaching it does not itself support or qualify the strategy;
- strategy semantics provide no finite guarantee of reaching it.

PRIMARY_ROOT_CAUSE =
NOMINAL_PLANNING_N_TRANSLATED_INTO_MANDATORY_TERMINAL_COUNT

## 5. Structural feasibility

The already-qualified M06-TR-01 lower bound remains:

ABSOLUTE 24x7 LOWER BOUND =
58927 hours

=
6.722222222222222 years

This assumes the impossible best case of one closed trade every hour continuously.

FINITE_COMPLETION_GUARANTEE =
FALSE

because a persistent signal can generate arbitrarily long HOLD sequences.

## 6. Exposed structural activity proxy

Only already-exposed structural activity information is used here.

E1-REAL-003 full sample:

CLOSED TRADES =
650

WINDOW =
2021-05-25T00:00:00.309Z
through
2026-05-24T23:59:59.963Z

WINDOW YEARS ON 365.25-DAY BASIS =
4.999315526339139

STRUCTURAL CLOSED-TRADE RATE =
130.01779875173776 per year

If, purely as a non-confirmatory feasibility illustration, that exposed structural activity rate persisted:

58927 / rate =
453.22256310859444 years

This is NOT:
- a forward forecast;
- a performance estimate;
- confirmatory evidence;
- a basis for strategy qualification.

It is an EXPOSED_STRUCTURAL_ACTIVITY_RATE_FEASIBILITY_PROXY_ONLY.

## 7. Would ordinary parameter relaxation solve the problem?

The previously documented 95% confidence / alpha 0.05 / power 0.80 sensitivity design requires:

POWER_REQUIRED_N =
27988

At the same exposed structural activity proxy:

27988 / rate =
215.26283530950738 years

Therefore:

RELAX_ALPHA_POWER_ONLY =
NOT_A_SUFFICIENT_OPERATIONAL_REMEDY

Changing inferential standards merely to make the experiment convenient would also contradict the original M06 qualification rationale.

## 8. Route adjudication candidate

### R0 — KEEP 58,927 AS MANDATORY TERMINAL COUNT

CLASSIFICATION =
NOT_RECOMMENDED

Reason:
internally deterministic but operationally extreme, no finite completion guarantee, and exposed structural activity proxy implies a multi-century order of magnitude.

### R1 — RELAX ALPHA / POWER / PRECISION FOR CONVENIENCE

CLASSIFICATION =
NOT_RECOMMENDED_AS_PRIMARY_REMEDY

Reason:
does not resolve the information-rate problem and weakens the predeclared evidentiary standard.

### R2 — REPLACE CLOSED-TRADE UNIT WITH H1 DECISION UNIT

CLASSIFICATION =
REJECT_FOR_CURRENT_ESTIMAND

Reason:
the estimand is per closed trade; the substitution changes the scientific observation unit.

### R3 — CHANGE ESTIMAND OR STRATEGY INFORMATION UNIT

CLASSIFICATION =
MAJOR_REDESIGN_ONLY

Reason:
scientifically possible, but this is no longer a minimal amendment to the current AO-E0 claim.

### R4 — DECOUPLE PLANNING N FROM A FIXED NON-PERFORMANCE CONFIRMATORY HORIZON

CLASSIFICATION =
RECOMMENDED_FOR_NEXT_DESIGN_PHASE

Core principle:

58927 may remain a REFERENCE_PLANNING_N while the confirmatory dataset is instead bounded by a separately preregistered calendar/information horizon that cannot depend on forward performance.

At that fixed horizon:
- analysis occurs once;
- M04/M05 and all validity gates remain binding;
- achieved n is reported;
- achieved/nominal precision-power shortfall is reported explicitly;
- a non-decisive result remains INCONCLUSIVE;
- no post-result extension is permitted merely because the result is unfavorable or imprecise.

This route does NOT yet define the horizon.

## 9. Required coherent amendment surface if R4 is later adopted

A later AO-E0-M06-AMEND-02 would have to amend coherently, before any real forward performance read:

1. M06:
   distinguish REFERENCE_PLANNING_N from mandatory stopping authority.

2. DATA-01:
   replace the 58,927-count terminal formation rule with the newly frozen non-performance horizon.

3. DR-01:
   remove the mechanical n<58927 => INCONCLUSIVE_INSUFFICIENT_SAMPLE rule and replace it with the newly preregistered fixed-horizon adequacy semantics.

4. TC-01:
   either retire its terminal-authority role or constrain it to descriptive count tracking only.

None of those changes are authorized by M06-AMEND-01.

## Verdict

M06_AMEND_01_ROOT_CAUSE =
PROVEN_DESIGN_ARTICULATION_DEFECT

ARITHMETIC_DEFECT =
NO

SAMPLE_UNIT_DEFECT =
NO

DEPENDENCE_OMISSION_DEFECT =
NO

PRIMARY_DEFECT =
NOMINAL_PLANNING_N_TRANSLATED_INTO_MANDATORY_TERMINAL_COUNT

DEEPER_INFORMATION_RATE_CONSTRAINT =
LOW_EFFECT_TO_DISPERSION_RATIO + LOW_CLOSED_TRADE_ARRIVAL_RATE

RECOMMENDED_ROUTE =
R4_DECOUPLE_PLANNING_N_FROM_FIXED_NONPERFORMANCE_CONFIRMATORY_HORIZON

NEXT =
AO-E0-M06-AMEND-02 DESIGN ONLY AFTER DISTINCT HUMAN ADOPTION

## Preserved firewall

M06 =
UNCHANGED / HUMAN_ADOPTED / BINDING / FROZEN

FINAL_REQUIRED_N =
58927

DATA01_TERMINAL_RULE =
UNCHANGED

DR01 =
UNCHANGED

REAL_TC01_FORWARD_READ =
FALSE

B12 =
CLOSED

OOS_PERFORMANCE_CONSUMPTION =
FALSE

REAL_FORWARD_PERFORMANCE_OBSERVATION =
FALSE

FORCE =
FALSE

STOP =
HUMAN_DECISION_REQUIRED
