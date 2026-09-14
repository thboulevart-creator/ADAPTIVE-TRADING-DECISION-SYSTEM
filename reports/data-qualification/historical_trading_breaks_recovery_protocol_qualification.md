# HISTORICAL TRADING BREAKS RECOVERY PROTOCOL — ADVERSARIAL QUALIFICATION

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

## Verdict

**PASS — `SYSTEMATIC_TRADING_BREAKS_RECOVERY_PROTOCOL_REJECTS_KNOWN_BYPASSES`**

This PASS certifies the recovery protocol and its executable validator. It does **not** promote any additional calendar date and does not authorize `.bi5` acquisition or a real backtest.

## Tested implementation

- protocol: `04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`
- validator: `tools/trading_breaks_recovery_protocol.py`
- adversarial suite: `tests/test_trading_breaks_recovery_protocol.py`
- workflow: `.github/workflows/trading-breaks-recovery-protocol.yml`
- workflow head: `f699de1c9aa7b5726276f07d40c5fc8543bc9392`
- workflow run: `34880921889`
- job: `104099717727`
- job conclusion: **success**
- Python: `3.12.14`
- pytest: **20 passed in 0.05s**

## Frozen recovery queue verified by runtime

The workflow independently asserted:

- queue count: **66**
- first unresolved: `2021-11-25 — THANKSGIVING_DAY`
- last unresolved in governed scope: `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

The two already-resolved in-window candidates are excluded mechanically:

- `2021-09-06 — LABOR_DAY`
- `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

No manual date exclusion is accepted by the validator.

## Adversarial attacks executed

The suite re-broke the protocol against the following failure/bypass classes:

1. frozen queue cardinality/order drift;
2. out-of-window target;
3. already-resolved date reintroduced into recovery queue;
4. requested-date mismatch;
5. wrong target instrument ID;
6. wrong target instrument name;
7. empty/no-record response promoted to evidence;
8. raw broker payload not retained;
9. network record for wrong instrument;
10. malformed epoch timestamp;
11. negative interval (`end < start`);
12. adjacent-date broker record;
13. DOM/network contradiction;
14. expected DOM cross-check missing;
15. workflow provenance missing;
16. artifact ID missing;
17. malformed artifact SHA-256;
18. malformed probe commit identity;
19. calibrated reopen semantics (`end + 60s`);
20. partial UTC hour incorrectly rounded to fully closed.

All 20 attacks were rejected or contained as specified.

## Positive-path control

A valid synthetic broker-native positive record for an unresolved governed candidate was accepted only when all required fields were present and consistent.

The validator produced:

- verdict: PASS;
- calibrated reopen = final closed minute + 60 seconds;
- only whole UTC hours fully contained in the closure interval.

This positive-path control does not constitute historical evidence for the synthetic date. It tests validator semantics only.

## Negative-evidence boundary preserved

An empty/no-record response returns:

`BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

It never produces PASS and never populates `NO_SPECIAL_CHANGE_EVIDENCE`.

Therefore the protocol preserves the already-locked limitation that the Trading Breaks route is qualified only for **positive historical break recovery**.

## Window immutability preserved

The validator hard-binds the governed recovery scope to:

`2021-08-14 → 2026-08-14`

Recovery outcomes are not inputs to the execution-window selection rule. The window cannot be shifted by the recovery protocol.

## Final qualification decision

The systematic protocol is now admissible for controlled application across the remaining 66 unresolved in-window candidates.

However:

- each date still requires exact broker-native positive evidence to pass;
- no-record remains BLOCKED;
- executable integration is date-level only;
- regression/coverage/boundary audit remains mandatory after any integration batch;
- execution-window freeze remains BLOCKED while unresolved dates remain;
- massive `.bi5` acquisition remains forbidden;
- real backtest remains forbidden.

## Exactly one next governed action

Apply the qualified protocol to the **first deterministic recovery batch** of unresolved candidates, preserving chronological order and independent date-level adjudication.

The batch size must be fixed before observing outcomes and must not be chosen to avoid difficult dates.
