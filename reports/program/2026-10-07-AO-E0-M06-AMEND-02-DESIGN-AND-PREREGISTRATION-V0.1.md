# AO-E0-M06-AMEND-02 — FIXED NON-PERFORMANCE CONFIRMATORY HORIZON DESIGN + PREREGISTRATION V0.1

STATUS =
CANDIDATE / NOT HUMAN ADOPTED / NOT APPLIED

## Selected horizon candidate

TYPE =
FIXED_365D_UTC_CALENDAR_HORIZON

EVIDENCE START =
2026-10-06T11:00:00Z

EVIDENCE END EXCLUSIVE =
2027-10-06T11:00:00Z

DURATION =
365 days / 8,760 hours

INCLUSION =
decision_time >= start AND decision_time < end

The horizon is selected before any real forward performance read.

## Why 365 days

The selected horizon is the minimum fixed calendar horizon that spans one complete annual cycle from the already-frozen forward evidence start.

It therefore crosses:
- both New York DST states;
- all four calendar quarters;
- year-end;
- a complete annual seasonal calendar.

90-day and 180-day candidates are rejected because they do not span a complete annual cycle.

730 days is not selected because it doubles latency while leaving the experiment overwhelmingly below the historical reference planning N under the already-exposed structural activity-rate proxy.

The exposed structural proxy is used only for feasibility illustration:
- 650 closed trades over about 4.9993 years;
- about 130.0178 closed trades/year;
- about 129.93 closed trades over 365 days at the same historical structural rate.

This proxy is not:
- forward performance;
- a performance forecast;
- confirmatory evidence;
- a stopping signal.

## M06 candidate semantics

The existing frozen calculation remains historically valid:

REFERENCE_PLANNING_N =
58927

PRECISION TARGET N =
30036

POWER TARGET N =
58927

Candidate amendment:

58927 ceases to be mandatory acquisition terminal authority.

It becomes:

REFERENCE_PLANNING_N

At the fixed horizon, report:
- actual closed-trade count;
- whether reference planning N was reached;
- planning-model precision half-width at actual n;
- planning-model power at actual n;
- existing M04/M05 validity status.

A planning shortfall cannot:
- automatically support;
- automatically refute;
- automatically extend the experiment.

## DATA-01 candidate semantics

Current rule:

FIRST DECISION BOUNDARY AT/AFTER 58927 ADMISSIBLE CLOSED FORWARD TRADES.

Candidate rule:

FIXED HALF-OPEN EVIDENCE WINDOW =
[2026-10-06T11:00:00Z, 2027-10-06T11:00:00Z)

Data after the fixed end cannot enter the same confirmatory instance.

A data gap or incomplete acquisition does not move the end date. It becomes a validity/data-completeness limitation.

## DR-01 candidate semantics

Remove:

n < 58927
→ automatic INCONCLUSIVE / INSUFFICIENT_SAMPLE

Replace with:

BEFORE FIXED HORIZON END
→ WAIT_NOT_READY

AT FIXED HORIZON END
→ run the existing validity and inference path.

n < 58927 becomes:

PLANNING_TARGET_NOT_REACHED

This is a limitation flag, not an automatic inference blocker.

n >= 58927 becomes:

PLANNING_TARGET_REACHED

This is not support and does not qualify the strategy by itself.

No new arbitrary minimum n is introduced.

Analyzability is delegated to the already-frozen M04/M05 runtime preconditions. If those cannot execute, the result is:

INCONCLUSIVE_INFERENCE_NOT_ANALYZABLE

Existing nonstationarity, influence, selection-asymmetry, cost robustness and M05 inference gates remain binding.

## TC-01 candidate role

TC-01 synthetic qualification is preserved.

Its future candidate role is:

DESCRIPTIVE_COUNT_TRACKER_ONLY

It no longer determines the experiment end.

A future TC-01 V0.2 should expose:
- cumulative_closed_trade_count;
- reference_planning_n_reached;
- bound_input_identity_digest;
- count_trace_digest.

The old terminal-authority fields should no longer have terminal authority.

REAL_TC01_FORWARD_READ remains unauthorized in M06-AMEND-02.

## No optional stopping

The following cannot authorize extension of the same experiment:
- unfavorable result;
- insufficient precision;
- achieved n below 58927;
- low planning-model power;
- near significance;
- support/refute direction;
- observed forward effect size;
- observed forward variance;
- observed profitability.

After the fixed end, any future additional experiment requires a new prospective governance decision.

## Exact scientific consequence

A fixed-horizon experiment may end as:

SUPPORT
REFUTE
INCONCLUSIVE

subject to the existing validity and inference gates.

INCONCLUSIVE is a valid terminal scientific result.

It does not authorize automatic continuation.

## Application status

M06 CHANGE =
NOT AUTHORIZED

DATA-01 CHANGE =
NOT AUTHORIZED

DR-01 CHANGE =
NOT AUTHORIZED

TC-01 REAL AUTHORITY CHANGE =
NOT AUTHORIZED

REAL FORWARD READ =
NOT AUTHORIZED

B12 =
CLOSED

This document is design/preregistration only.

STOP =
AFTER SYNTHETIC/DOCUMENTARY QUALIFICATION AND HUMAN DECISION PACKET
