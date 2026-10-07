# AO-E0-M06-AMEND-01 — HUMAN AUTHORIZATION — 2026-10-07

HUMAN_DECISION =
AUTHORIZE_PROSPECTIVE_M06_AMENDMENT_ANALYSIS_ONLY

SOURCE_HUMAN_MESSAGE =
"Ok fais exactement comme tu as dis"

AUTHORIZED_SCOPE =
- determine whether the M06 operational defect originates in sample unit, terminal-rule translation, estimand, independence/effective-sample treatment, or their articulation;
- recompute existing frozen M06 planning mathematics;
- use already-exposed structural activity information only as a planning/feasibility proxy;
- compare amendment routes prospectively;
- produce a recommendation and a human decision packet.

NOT_AUTHORIZED =
- change FINAL_REQUIRED_N = 58927;
- change alpha, target power, confidence level, planning sigma, DELTA_MIN, effect size, H0, H1 or estimand;
- change DATA-01 terminal rule;
- change DR-01 decision rule;
- authorize or execute a real TC-01 forward read;
- open B12;
- consume OOS performance;
- observe real forward performance;
- execute AO-E0 or real SMF;
- strategy optimization;
- trading, broker execution or capital deployment.

M06 =
HUMAN_ADOPTED / BINDING / FROZEN

FINAL_REQUIRED_N =
58927

B8 =
CLOSED

B12 =
CLOSED

FORCE =
FALSE

STOP =
AFTER_PROSPECTIVE_ROOT_CAUSE_AND_ROUTE_RECOMMENDATION
