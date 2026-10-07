# AO-E0-M06-AMEND-02 — HUMAN DECISION PACKET — 2026-10-07

## Candidate verdict

M06_AMEND_02_DESIGN =
QUALIFIED_CANDIDATE_PENDING_CI

PROPOSED_ROUTE =
FIXED_365D_UTC_CALENDAR_HORIZON

PROPOSED_WINDOW =
[2026-10-06T11:00:00Z, 2027-10-06T11:00:00Z)

REFERENCE_PLANNING_N =
58927

REFERENCE_PLANNING_N_TERMINAL_AUTHORITY =
REMOVE_IN_CANDIDATE_AMENDMENT

## Proposed coherent amendment

M06:
58927 becomes REFERENCE_PLANNING_N rather than mandatory stopping authority.

DATA-01:
replace closed-trade-count terminal formation rule with fixed 365-day half-open calendar window.

DR-01:
remove automatic n<58927 insufficient-sample blocker; at the fixed horizon, retain existing validity/inference gates and report planning-target shortfall as limitation only.

TC-01:
retain only a descriptive structural count role; remove terminal authority.

## Why this candidate

365 days is the shortest fixed horizon spanning one complete annual cycle from the frozen forward evidence start.

It is independent of:
- PnL;
- returns;
- expectancy;
- win rate;
- drawdown;
- forward effect size;
- forward variance;
- CI favorability;
- support/refute direction.

The already-exposed structural activity proxy implies only about 130 closed trades per year. Therefore adding a second year still does not approach the 58,927 reference planning target, while doubling latency.

## Mandatory no-extension rule

After 2027-10-06T11:00:00Z:

THE SAME CONFIRMATORY INSTANCE ENDS.

The following do not authorize extension:
- n < 58927;
- low planning-model power;
- insufficient precision;
- near significance;
- unfavorable result;
- favorable result;
- data gap;
- observed performance.

If the fixed-window evidence is non-decisive:

RESULT =
INCONCLUSIVE

Any later experiment requires new prospective governance.

## Candidate next human choices

ADOPT_EXACT_M06_AMEND_02_CANDIDATE

REJECT_M06_AMEND_02_CANDIDATE

AMEND_BEFORE_ADOPTION

ABANDON_CURRENT_CONFIRMATORY_ROUTE

## If exact candidate is later adopted

A separate implementation/application phase would still be required.

That later phase must:
- mutate M06 prospectively;
- mutate DATA-01 terminal semantics;
- mutate DR-01 decision semantics;
- replace/restrict TC-01 authority;
- regression-test all affected surfaces;
- persist exact adoption receipts;
- STOP before any real forward performance read unless separately authorized.

## Current firewall

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

TRADING =
NOT_AUTHORIZED

BROKER_EXECUTION =
NOT_AUTHORIZED

CAPITAL_DEPLOYMENT =
NOT_AUTHORIZED

FORCE =
FALSE

STOP =
HUMAN_DECISION_REQUIRED_AFTER_QUALIFICATION
