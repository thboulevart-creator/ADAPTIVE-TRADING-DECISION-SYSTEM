# PRE-BACKTEST CRITICAL-PATH REEVALUATION — 2026-09-15

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Purpose

Re-evaluate the real blocking path to the first accepted backtest after the current Trading Breaks recovery capability reached exhaustion. This document is a decision record, not a new data source and not a calendar mutation.

Method: **UNDERSTAND → COMPARE → BREAK → DECIDE**.

## Current factual state

The terminal Batch 14 has already been integrated at:

`075b33b79c8de3b2f4f6201a7541c6555585a5e4`

Batch 14 adjudication:

- `2026-06-19 — JUNETEENTH_OBSERVED` → PASS
- `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION` → BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`
- `2026-07-03 — INDEPENDENCE_DAY_OBSERVED` → PASS

Post-integration progression:

- execution-window candidates: `68`
- resolved: `51`
- unresolved: `17`
- attempt ledger: `68`
- same-capability BLOCKED/ineligible: `17`
- eligible under `TRADING_BREAKS_PRIMARY_WIDGET_V1`: `0`
- material capability changes: `0`

Therefore a Batch 15 under the same capability is impossible and forbidden by the progression contract. Repeating the batch mechanism would not reduce the blocking state.

Batch 14 integration has not yet received its independent persisted-HEAD read-only re-break. Until that proof exists, Batch 14 is integrated but not fully closed.

## The 17 unresolved dates are two different problems

Inspection of the persisted attempt ledger shows two distinct blocking classes.

### Class A — positive broker record exists, but exact-start-date rule rejects it: 14 dates

Blocking reason:

`NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

These dates have a broker-native record overlapping the addressed target day, but the existing adjudication refuses promotion when the record starts on the preceding calendar date.

The 14 affected current unresolved dates are:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`
- `2022-12-26 — CHRISTMAS_OBSERVED`
- `2023-01-02 — NEW_YEARS_OBSERVED`
- `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
- `2023-12-25 — CHRISTMAS_OBSERVED`
- `2024-01-01 — NEW_YEARS_OBSERVED`
- `2024-03-29 — GOOD_FRIDAY`
- `2024-12-25 — CHRISTMAS_OBSERVED`
- `2025-01-01 — NEW_YEARS_OBSERVED`
- `2025-04-18 — GOOD_FRIDAY`
- `2025-12-25 — CHRISTMAS_OBSERVED`
- `2026-01-01 — NEW_YEARS_OBSERVED`
- `2026-04-03 — GOOD_FRIDAY`

### Class B — no positive broker record recovered: 3 dates

Blocking reason:

`NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

The three dates are:

- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

These three are genuine negative-evidence/completeness problems and must not be conflated with Class A.

## Semantic inconsistency discovered

The capture layer already treats a Trading Breaks record as relevant when its interval overlaps the target day:

`start < target_day_end && end >= target_day_start`

It also derives `fully_closed_hours_utc` specifically for the addressed target calendar date.

The core recovery protocol likewise exposes:

`derive_fully_closed_hours_utc(target_date, start, reopen)`

which computes only whole target-day UTC hours fully covered by the broker-native closed interval.

However the positive adjudication contract additionally rejects any record whose `start.date()` is not exactly the addressed target date. Later batch adjudicators convert an overlapping cross-date record into:

`BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

This creates an architectural mismatch:

- capture semantics: interval overlap with the target day is meaningful;
- calendar representation: target-day whole-hour closure is what is ultimately stored;
- historical hand-authored evidence already represents multi-day holiday windows across consecutive calendar dates;
- adjudication semantics: requires broker record start date == target date.

The exact-start-date requirement is therefore a stronger condition than the downstream calendar fact being proved. It must be independently justified or removed; it must not be preserved merely because previous batches used it.

## Decision

### Rejected path 1 — continue batching

**REJECTED.** Eligible queue under the current capability is empty. A Batch 15 would violate the progression state rather than advance it.

### Rejected path 2 — search for a new source for all 17 dates

**REJECTED.** Fourteen of the seventeen dates already possess positive broker-native evidence. Treating them as missing-data cases solves the wrong problem.

### Rejected path 3 — bypass calendar qualification and acquire `.bi5`

**REJECTED.** The current acquisition boundary remains fail-closed: execution-window freeze is blocked while in-window unresolved dates remain. This reevaluation does not authorize `.bi5` or a real backtest.

### Selected path — split semantic admissibility from negative completeness

The critical path is now:

1. **Integrity closure of already-integrated Batch 14**  
   Perform one independent, read-only persisted-HEAD re-break of integration commit `075b33b79c8de3b2f4f6201a7541c6555585a5e4`. This is not another recovery batch; it closes already-mutated governed state.

2. **Qualify target-day overlap semantics using existing evidence only**  
   Build the smallest offline contract that asks whether a broker-native interval can prove target-day closed hours when:
   - the exact target date request was honored;
   - instrument is exactly USATECH `9016`;
   - a primary broker Trading Breaks record exists;
   - the record interval actually overlaps the target day;
   - raw payload is retained;
   - DOM/network evidence is consistent where required;
   - full provenance is retained;
   - target-day closed hours are derived by interval intersection;
   - no closed hour outside the broker interval is invented.

   The contract must adversarially reject at minimum:
   - adjacent non-overlapping records;
   - wrong requested date;
   - wrong instrument;
   - malformed/negative interval;
   - missing payload/provenance;
   - DOM/network contradiction;
   - interval that does not cover any whole target-day hour;
   - borrowing evidence from an unrelated record or year.

   This qualification must initially be **offline/read-only** and reuse the already captured Class-A evidence. No new browser observation is justified merely to change adjudication semantics.

3. **Re-adjudicate Class A only if the new semantic contract passes**  
   Re-evaluate the 14 preserved overlap-blocked dates from their existing artifacts/provenance. Integrate only independently proven target-day closures. Historical attempt records remain immutable; the new decision must be attributable to a new qualified capability/contract rather than rewriting old verdict history.

4. **Treat Class B as a separate negative-evidence problem**  
   For the remaining three true no-record dates, determine whether the official Trading Breaks route can be qualified as a complete negative-evidence source for an exact honored date/instrument. Empty response must remain BLOCKED unless completeness is proven. If completeness cannot be proven, use a materially different primary evidence source for those three dates only.

5. **Only after execution-window unresolved = 0 and FAIL = 0**  
   Freeze the fixed execution window `2021-08-14 → 2026-08-14`, then freeze the OOS split, pass the separate native-tick acquisition authorization, acquire and qualify the five-year tick dataset/cost model, and only then execute Momentum V1 baseline.

## Exactly one next governed action

**Independently re-break the persisted Batch 14 integration HEAD in read-only mode. If and only if that passes, the following workstream is not Batch 15 but an offline adversarial qualification of target-day overlap semantics against the already captured Class-A evidence.**

No new browser capture is authorized by this decision record.  
No `.bi5`.  
No real backtest.
