# AO-E0-M06-AMEND-02 — TECHNICAL QUALIFICATION V0.1

RESULT =
QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION

SCOPE =
FIXED-HORIZON DESIGN + PREREGISTRATION + SYNTHETIC/DOCUMENTARY QUALIFICATION ONLY

CANONICAL CANDIDATE HEAD =
29c70163114c42bd5a52b2ec83a497e50522bcf2

TREE =
10b646f43a352cc46c619552525ae792e7bd463a

## Canonical CI

WORKFLOW =
AO-E0 M06-AMEND-02 Fixed Horizon Qualification

RUN =
37620817257

JOB =
112790339419

CONCLUSION =
SUCCESS

M06-AMEND-02 TESTS =
40 / 40 PASS

FROZEN M06 REGRESSION =
17 / 17 PASS

FROZEN TC-01 REGRESSION =
44 / 44 PASS

TOTAL =
101 / 101 PASS

GOVERNED SOURCE BLOBS UNCHANGED =
PASS

AUTHORITY FIREWALL =
PASS

## Qualified horizon candidate

TYPE =
FIXED_365D_UTC_CALENDAR_HORIZON

WINDOW =
[2026-10-06T11:00:00Z, 2027-10-06T11:00:00Z)

DURATION =
365 days

The horizon is fixed before any real forward performance read and cannot depend on PnL, returns, expectancy, drawdown, observed effect size, observed variance, CI favorability, significance or support/refute direction.

## Qualified rationale

365 days is the shortest candidate spanning one complete annual calendar cycle from the frozen evidence start.

The window contains both New York DST states and spans all four quarters plus year-end.

90/180-day candidates fail the full-annual-cycle criterion.

730 days is not selected because it doubles latency while the already-exposed structural activity proxy remains orders of magnitude below REFERENCE_PLANNING_N.

The proxy is structural feasibility information only, not performance and not a forecast.

## Qualified M06 candidate diff

CURRENT =
FINAL_REQUIRED_N 58927 acts downstream as mandatory sample/terminal authority.

CANDIDATE =
58927 becomes REFERENCE_PLANNING_N only.

At the fixed horizon, report:
- actual closed-trade count;
- whether 58927 was reached;
- planning-model precision half-width at actual n;
- planning-model power at actual n;
- existing M04/M05 validity status.

Planning shortfall cannot itself support, refute or extend the experiment.

## Qualified DATA-01 candidate diff

CURRENT =
first governed decision boundary at/after 58927 admissible closed forward trades.

CANDIDATE =
fixed half-open evidence window ending 2027-10-06T11:00:00Z.

Data after the fixed end cannot enter the same confirmatory instance.

A data gap cannot automatically extend the horizon.

## Qualified DR-01 candidate diff

CURRENT =
n < 58927 => INCONCLUSIVE_INSUFFICIENT_SAMPLE.

CANDIDATE =
n < 58927 => PLANNING_TARGET_NOT_REACHED limitation only.

Before the fixed end:
WAIT_NOT_READY.

At the fixed end:
run existing validity and inference gates.

No new arbitrary numeric minimum n is introduced.

Existing M04/M05 analyzability conditions remain controlling.

If inference cannot execute:
INCONCLUSIVE_INFERENCE_NOT_ANALYZABLE.

If existing validity gates block:
INCONCLUSIVE with the existing reason.

Valid existing SUPPORT / REFUTE inference paths remain preserved.

## Qualified TC-01 candidate diff

TC-01 synthetic qualification remains preserved.

Candidate future role =
DESCRIPTIVE_COUNT_TRACKER_ONLY.

TC-01 no longer has terminal authority.

REAL_TC01_FORWARD_READ remains unauthorized.

## No optional stopping

The same confirmatory instance cannot be extended because of:
- unfavorable result;
- favorable result;
- n below 58927;
- insufficient precision;
- low planning-model power;
- near significance;
- observed forward effect;
- observed forward variance;
- data gap.

A later experiment requires new prospective governance.

## Repository-wide CI caveat

REPOSITORY_GLOBAL_CI =
NOT_ALL_GREEN

P0.4 RUN 37620816964 =
FAILURE

P0.6 RUN 37620817242 =
FAILURE

Both failures remain the same broad historical BERD02 .bi5 guard condition.

They are not relabeled as PASS.

M06_AMEND_02_CLAIM_SCOPED_CI =
SUCCESS

## Preserved current state

M06 =
UNCHANGED / HUMAN_ADOPTED / BINDING / FROZEN

FINAL_REQUIRED_N =
58927

DATA01_TERMINAL_RULE =
UNCHANGED

DR01 =
UNCHANGED

TC01_REAL_AUTHORITY =
FALSE

M06_AMEND_02_CANDIDATE =
NOT_YET_HUMAN_ADOPTED

ACTUAL_AMENDMENT_APPLICATION =
NOT AUTHORIZED

REAL_TC01_FORWARD_READ =
FALSE

B12 =
CLOSED

OOS_PERFORMANCE_CONSUMPTION =
FALSE

REAL_FORWARD_PERFORMANCE_OBSERVATION =
FALSE

REAL_AO_E0_EXECUTION =
FALSE

REAL_SMF_EXECUTION =
FALSE

TRADING / BROKER / CAPITAL =
NOT AUTHORIZED

FORCE =
FALSE

STOP =
HUMAN_DECISION_REQUIRED
