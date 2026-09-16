# PRE-BACKTEST CRITICAL-PATH REEVALUATION — 2026-09-16

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Verdict

**PASS — `CLASS_B_COMPLETENESS_IS_THE_ONLY_INFORMATIONAL_BLOCKER_WORTH_ATTACKING_NEXT`**

This is a decision record only. It does not mutate calendar evidence, attempt history, capability state, the execution window, `.bi5`, or backtest authorization.

Method:

**UNDERSTAND → COMPARE → BREAK → DECIDE**

## Evaluated state

Batch 15 V2 is fully closed.

Current deterministic execution-window state:

- candidate window: `2021-08-14 → 2026-08-14`
- candidates: `68`
- resolved: `56`
- unresolved: `12`
- FAIL: `0`
- attempt ledger: `73`
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- material capability changes: `1`
- execution-eligible unresolved Class A: `9`
- unresolved/ineligible Class B: `3`
- execution window frozen: NO
- `.bi5`: FORBIDDEN
- real backtest: NOT AUTHORIZED

The active branch HEAD used for this review is downstream of the fully closed Batch 15 V2 checkpoint; the only later user upload observed before this decision was `Carte Architecturale Snapshots Claude/ADTS-plan-systeme-autonome.pdf`, which does not mutate governed Trading Breaks state.

## What is already known about the 9 remaining Class A dates

The qualified V2 overlap contract has already independently readjudicated **all 14 Class-A dates** from immutable persisted broker evidence:

`14 PASS / 0 BLOCKED / 0 FAIL`

Five of those fourteen were integrated by Batch 15 V2. The remaining nine are therefore not an evidence-discovery problem. They already possess qualified offline PASS decisions:

1. `2023-12-25 — CHRISTMAS_OBSERVED`
2. `2024-01-01 — NEW_YEARS_OBSERVED`
3. `2024-03-29 — GOOD_FRIDAY`
4. `2024-12-25 — CHRISTMAS_OBSERVED`
5. `2025-01-01 — NEW_YEARS_OBSERVED`
6. `2025-04-18 — GOOD_FRIDAY`
7. `2025-12-25 — CHRISTMAS_OBSERVED`
8. `2026-01-01 — NEW_YEARS_OBSERVED`
9. `2026-04-03 — GOOD_FRIDAY`

Authoritative readjudication report:

`reports/data-qualification/trading_breaks_target_day_overlap_readjudication.md`

Integrating these nine is necessary eventually, but it is not the next informational bottleneck.

If all nine were integrated immediately, the execution window would move mechanically from:

`68 / 56 resolved / 12 unresolved`

to:

`68 / 65 resolved / 3 unresolved`

The execution-window freeze would still be BLOCKED because the governing boundary requires exactly zero unresolved and zero FAIL inside the proposed window.

Therefore splitting the already-proven nine into another Batch 16 / Batch 17 sequence would add operational work without answering the only remaining uncertain question.

## The actual unresolved uncertainty — Class B

The three Class-B dates are:

1. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
2. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Current blocking reason:

`NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

The existing historical runtimes already prove more than a generic failure for all three:

- exact requested historical date was honored;
- official page HTTP status was `200`;
- target navigation/document status was `200`;
- target instrument identity was `USATECH.IDX/USD` / `9016`;
- raw payload was present;
- runtime errors were empty;
- `matching_records` was empty;
- DOM witness lines were empty.

Additionally, `2021-12-31` was independently attempted twice under V1 and produced the same no-positive-record outcome twice with distinct run/artifact/probe provenance.

Persisted evidence sources include:

- `reports/data-qualification/historical_trading_breaks_recovery_batch01_runtime.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch02_runtime.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch03_runtime.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch14_runtime.json`

However, current route qualification explicitly proves only **positive historical break recovery**. It explicitly forbids interpreting an empty widget/API result as proof of normal trading and requires a separate negative-evidence/completeness contract before `NO_SPECIAL_CHANGE_EVIDENCE` may be populated.

So the remaining uncertainty is not “did the browser work?” It is:

> Does an exact-date, exact-instrument, successful broker-native Trading Breaks response with retained raw payload and no matching target record constitute a **complete enough broker statement** to prove that no special-session Trading Breaks interval existed for that target date?

## Paths compared

### Path A — integrate the 9 remaining Class A now

**DEFERRED, not rejected.**

The nine have already passed qualified semantic readjudication and can later be integrated without new observation. But doing so now does not unlock any downstream gate because the three Class-B dates remain unresolved.

No new information would be learned.

### Path B — freeze another V2 batch merely because 9 dates are eligible

**REJECTED.**

Batching was useful when execution/capture had to remain bounded before outcomes were known. These nine outcomes are already independently known and qualified offline. Recreating another batch boundary would be process repetition rather than risk reduction.

### Path C — immediately build an alternate broker route for the 3 Class B dates

**PREMATURE.**

The persisted captures already contain successful exact-date broker responses with empty target-record sets. Before paying the architectural cost of a new route, the system should first test whether the current broker-native response can be qualified as negative evidence under a much stricter completeness contract.

If completeness cannot be proven, then an alternate route becomes materially justified.

### Path D — treat empty payload result as regular-hours PASS immediately

**REJECTED.**

This would directly violate both `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1` and `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`.

HTTP `200`, empty `matching_records`, or absent DOM witness alone is not currently admissible negative evidence.

### Path E — move/freeze the execution window or start `.bi5`

**REJECTED.**

The execution-window boundary requires zero unresolved candidates in-window before freeze PASS. No window shift to avoid these dates is allowed, and `.bi5` acquisition requires a separately frozen PASS window and explicit acquisition authorization.

## Selected critical path

The highest-value next work is **not another integration batch**.

It is to qualify, offline and adversarially, a narrow Class-B negative-evidence/completeness contract using only the already persisted captures first.

The candidate contract must answer whether the broker-native response is complete enough to support exactly one of two outcomes:

1. **PASS negative evidence** — the response proves no target-instrument special Trading Breaks interval existed for the addressed target day, allowing governed `NO_SPECIAL_CHANGE_EVIDENCE`; or
2. **BLOCKED** — response completeness cannot be established, requiring a materially different broker-native route or archive/backfill capability.

It must never manufacture a PASS merely because `matching_records == []`.

## Minimum adversarial attacks required

Before any Class-B date can be upgraded, the contract must reject at minimum:

1. HTTP `200` with missing raw payload;
2. date not actually honored / current-date fallback;
3. wrong target instrument or missing instrument identity;
4. parser/filter bug that hides a record actually present in the raw payload;
5. raw payload containing an overlapping target-instrument record while normalized `matching_records` is empty;
6. incomplete/truncated/paginated response whose completeness cannot be proven;
7. response scope that does not guarantee the target date is fully represented;
8. adjacent-date or other-year absence borrowed as target-date evidence;
9. runtime/selector/network errors presented as empty evidence;
10. provenance mismatch between runtime, artifact, digest, job, and probe commit;
11. inconsistent repeated observations for the same target date;
12. `matching_records=[] → PASS` without an independently proven completeness property.

For `2021-12-31`, the two distinct historical attempts may be used as consistency evidence, but duplication alone must not substitute for route completeness.

## Consequence if the Class-B completeness contract passes

Only then may the three persisted Class-B cases be independently adjudicated offline.

If all three receive admissible negative-evidence PASS, the project can then perform one bounded **calendar-closure integration** using already-qualified evidence:

- integrate the nine remaining Class-A positive V2 PASS dates;
- integrate the three Class-B negative-evidence PASS dates;
- preserve every historical attempt unchanged;
- regenerate progression;
- adversarially re-break the resulting persisted HEAD.

The target post-state would then be `68 / 68 resolved / 0 unresolved / 0 FAIL` inside the execution window, enabling — but not automatically granting — the separate execution-window freeze gate.

## Consequence if the Class-B completeness contract is BLOCKED

Do not retry the same browser capability.

The next work must become a materially different capability that explicitly addresses `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`, such as the governed requirement already named by the progression contract:

- `ALTERNATE_BROKER_NATIVE_RECORD_ROUTE`, or
- `BROKER_ARCHIVE_BACKFILL_ACCESS`.

Only those three Class-B dates need that additional route. The nine Class-A dates do not.

## Exactly one next governed action

**Formalize and adversarially qualify an offline `TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1` candidate against the three already persisted Class-B captures, without browser access, without new capture, without calendar/ledger mutation, and without changing the current capability registry.**

The qualification must end in PASS / FAIL / BLOCKED.

Only after that verdict may the system decide whether existing Class-B evidence is sufficient or a materially different broker-native route is required.

No Batch 16 freeze.  
No new browser capture.  
No `.bi5`.  
No real backtest.
