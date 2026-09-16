# COVERAGE ENVELOPE / EXECUTION WINDOW BOUNDARY — GOVERNANCE RULE V1

## 1. Purpose

This rule separates four different claims that MUST NOT be conflated:

1. continuing historical qualification inside the broad research coverage envelope;
2. declaring the broad coverage envelope complete;
3. freezing a future contiguous execution/backtest window of at least five years;
4. authorizing massive native `.bi5` acquisition for that frozen window.

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`.

Allowed verdicts: **PASS / FAIL / BLOCKED**.

The rule exists specifically to prevent both false global PASS and cherry-picked execution windows that are chosen only to avoid known evidence gaps.

## 2. Scope distinction

### Global coverage envelope

The current research envelope (`2018-05-01` → `2026-08-14`) is a discovery/qualification superset. A BLOCKED historical date remains part of its truth state until resolved. A later qualification step MUST NOT silently remove or reclassify it.

### Future execution window

A future execution window is a contiguous subset selected for actual data acquisition/backtest. It may be narrower than the global envelope, but its boundaries must be justified independently of known evidence gaps and versioned before acquisition.

A gap outside a future execution window does not become resolved. It remains BLOCKED in the global envelope.

## 3. Action A — CONTINUE_LATER_QUALIFICATION

Continuing qualification into later dates (for example 2020+) is **PASS** when:

- every prior unresolved/FAIL date remains durably recorded with its existing verdict;
- later qualification does not claim global coverage PASS;
- no prior gap is silently deleted, reclassified, or excluded from reports;
- the work remains evidence gathering / qualification only;
- no acquisition/backtest authorization is inferred from this PASS.

A prior BLOCKED date does **not** force research to stop chronologically forever. It blocks the unresolved claim, not independent evidence gathering for later dates.

This PASS means only: `QUALIFICATION_MAY_CONTINUE`.

## 4. Action B — DECLARE_GLOBAL_COVERAGE_PASS

Global coverage may receive PASS only when:

- every candidate special-session date inside the global envelope is resolved;
- unresolved count is exactly zero;
- no FAIL date remains;
- there are no contradictory/malformed/orphan evidence records.

Any unresolved date, including an `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`, keeps global coverage **BLOCKED**.

## 5. Action C — FREEZE_EXECUTION_WINDOW

A future execution window may receive PASS only when ALL conditions hold:

1. exact start and end dates are versioned;
2. the window is contiguous — no manual deletion of individual dates inside it;
3. the window spans at least five calendar years;
4. the selection rationale is explicit, versioned, and independent of known unresolved/FAIL dates;
5. the window was not moved, shortened, or shifted merely to avoid a known evidence gap;
6. every calendar candidate inside the proposed window has been enumerated;
7. unresolved candidate count inside the proposed window is zero;
8. FAIL candidate count inside the proposed window is zero;
9. any global gaps outside the window remain visible and unchanged in global reports;
10. the window is not described as proving the entire global envelope.

A window that excludes `2019-07-03` can therefore be admissible only if its independent research rationale stands without reference to that gap. “Start in 2020 because 2019-07-03 is BLOCKED” is explicitly invalid.

If evidence inside the proposed window is still incomplete, verdict is BLOCKED. If the window is cherry-picked, non-contiguous, or below five years, verdict is FAIL.

## 6. Action D — AUTHORIZE_MASSIVE_ACQUISITION

This boundary rule does NOT itself authorize acquisition.

Massive native `.bi5` acquisition remains BLOCKED unless a separate acquisition decision proves at least:

- an execution window already frozen with PASS under Action C;
- every mandatory calendar/data qualification gate required for that frozen window is PASS;
- exact symbol/source/window are frozen;
- native tick acquisition/manifest/hash/reconciliation protocol is ready;
- no OHLC M1, interpolation, synthetic or substituted ticks are allowed;
- explicit acquisition authorization is recorded.

Therefore `CONTINUE_LATER_QUALIFICATION = PASS` MUST NOT be reused as acquisition permission.

## 7. Anti-cherry-pick invariants

The following are forbidden:

- moving the start date to the day/year after a known BLOCKED date without an independent research reason;
- choosing the shortest possible five-year window solely because its calendar happens to be complete;
- removing a troublesome date from an otherwise contiguous window;
- redefining the global envelope after discovering evidence gaps merely to obtain PASS;
- reporting `0 unresolved` by counting only a preferred subset while calling it global coverage;
- using an outside-window gap as if it were resolved;
- using future-window admissibility to rewrite historical global verdicts;
- starting massive acquisition merely because later qualification is allowed.

## 8. PASS / FAIL / BLOCKED semantics

- **PASS**: the requested action is allowed under this contract; it does not imply PASS for other actions.
- **FAIL**: the requested boundary/action violates a hard invariant (for example cherry-picking, non-contiguous exclusion, <5 years, hidden gap).
- **BLOCKED**: the action could be valid in principle but required evidence/state is incomplete.

## 9. Required adversarial qualification

Before first use, attack at minimum:

1. continue 2020+ while preserving a 2019 BLOCKED gap;
2. false global PASS with one unresolved date;
3. proposed 2020+ window chosen explicitly because 2019 is blocked;
4. independent >=5-year window with zero in-window unresolved but outside global gaps preserved;
5. >=5-year window with one unresolved date inside;
6. manual exclusion of a single bad date from a window;
7. <5-year window with perfect evidence;
8. acquisition attempt before window freeze;
9. acquisition attempt after `CONTINUE_LATER_QUALIFICATION` PASS but without acquisition gate;
10. hidden/reclassified historical gap.

The rule must pass adversarial qualification before it is applied to the current `2019-07-03` / `2020+` frontier.
