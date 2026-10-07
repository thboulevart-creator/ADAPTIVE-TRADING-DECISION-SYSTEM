# AO-E0-M06-AMEND-02 — HUMAN DECISION PACKET V0.2 — 2026-10-07

## Qualified candidate

M06_AMEND_02 =
QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION

CI =
SUCCESS

SCOPED TESTS =
101 / 101 PASS

PROPOSED HORIZON =
FIXED_365D_UTC_CALENDAR_HORIZON

PROPOSED WINDOW =
[2026-10-06T11:00:00Z, 2027-10-06T11:00:00Z)

## Exact candidate amendment

M06:
- preserve 58,927 as REFERENCE_PLANNING_N;
- remove mandatory stopping authority from that number.

DATA-01:
- replace count-based terminal formation with the fixed 365-day evidence window;
- prohibit post-end data from entering the same confirmatory instance.

DR-01:
- remove automatic n<58,927 insufficient-sample blocking;
- report n<58,927 as a planning-target shortfall;
- retain all existing validity and inference gates;
- allow SUPPORT, REFUTE or INCONCLUSIVE at the fixed horizon according to those gates.

TC-01:
- preserve synthetic qualification;
- future role becomes DESCRIPTIVE_COUNT_TRACKER_ONLY;
- no terminal authority.

## Why this is the recommended candidate

The current 58,927 count is valid as a planning reference but operationally incoherent as mandatory stopping authority.

A one-year fixed horizon:
- is chosen before any performance read;
- covers a complete annual cycle;
- prevents optional stopping;
- produces a finite experiment;
- makes INCONCLUSIVE an acceptable terminal result;
- preserves dependence-aware M04/M05 inference.

Longer fixed horizons can be designed later as new experiments, but cannot be appended after observing this experiment's result.

## Human choices

### Recommended

ADOPT_EXACT_M06_AMEND_02_CANDIDATE

This should authorize a separate amendment-application implementation phase only.

It must NOT itself authorize:
- real forward performance read;
- B12 opening;
- AO-E0 real execution;
- trading.

### Alternatives

AMEND_CANDIDATE_BEFORE_ADOPTION

REJECT_M06_AMEND_02_CANDIDATE

ABANDON_CURRENT_CONFIRMATORY_ROUTE

OTHER_EXPLICITLY_GOVERNED_DECISION

## Required next phase if adopted

AO-E0-M06-AMEND-03 —
COHERENT PROSPECTIVE APPLICATION
+ M06 / DATA-01 / DR-01 / TC-01 V0.2 IMPLEMENTATION
+ FULL REGRESSION
+ PERSISTED-HEAD REBREAK

Scope of M06-AMEND-03 must be limited to applying the already-qualified semantic diffs.

It must still STOP before any first real TC-01 read or B12 opening unless separately authorized.

## Current state remains

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

ACTUAL_AMENDMENT_APPLICATION =
NOT AUTHORIZED

REAL_TC01_FORWARD_READ =
FALSE

PIPE01_FIRST_PERFORMANCE_READ =
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

STRATEGY_QUALIFIED =
NO CLAIM

TRADING =
NOT_AUTHORIZED

BROKER_EXECUTION =
NOT_AUTHORIZED

CAPITAL_DEPLOYMENT =
NOT_AUTHORIZED

FORCE =
FALSE

STOP =
HUMAN_DECISION_REQUIRED
