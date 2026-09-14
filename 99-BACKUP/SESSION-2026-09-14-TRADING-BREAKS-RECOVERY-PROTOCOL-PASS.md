# SESSION BACKUP — 2026-09-14 — TRADING BREAKS RECOVERY PROTOCOL PASS

## Purpose

Durable recovery snapshot after formalization and executable adversarial qualification of the systematic Dukascopy Trading Breaks historical recovery protocol.

No bulk recovery batch has been executed in this step.

## Authoritative branch

`feat/multi-year-dukascopy-acquisition`

## Upstream state preserved

- execution-window candidate: `2021-08-14` → `2026-08-14`
- in-window candidates: 68
- resolved: 2
- unresolved recovery queue: 66
- global candidates: 111
- global resolved: 25
- global unresolved: 86
- historical positive Trading Breaks route: PASS
- local runtime evidence archive: COMPLETE
- latest calendar/boundary regression before this protocol work: `63 PASS`
- `.bi5`: FORBIDDEN
- real backtest: NOT authorized

## Protocol

`04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROTOCOL.md`

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`

Final verdict:

**PASS — `SYSTEMATIC_TRADING_BREAKS_RECOVERY_PROTOCOL_REJECTS_KNOWN_BYPASSES`**

## Executable validator

`tools/trading_breaks_recovery_protocol.py`

The validator enforces:

- fixed execution-window scope;
- deterministic unresolved queue;
- exact target date;
- exact `USATECH.IDX/USD` / ID `9016` identity;
- positive broker-native record requirement;
- raw payload retention;
- DOM/network consistency where DOM is available;
- workflow/artifact/hash/commit provenance;
- calibrated `end + 60s` reopen semantics;
- whole-hour-only closure derivation;
- BLOCKED rather than PASS for empty/no-record responses.

## Adversarial suite

`tests/test_trading_breaks_recovery_protocol.py`

Workflow:

`.github/workflows/trading-breaks-recovery-protocol.yml`

Observed execution:

- head: `f699de1c9aa7b5726276f07d40c5fc8543bc9392`
- workflow run: `34880921889`
- job: `104099717727`
- conclusion: `success`
- pytest: **20 passed in 0.05s**

Runtime queue assertion:

- count: **66**
- first: `2021-11-25 — THANKSGIVING_DAY`
- last: `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

## Attack coverage

The executable suite rejects/contains:

1. frozen queue drift;
2. out-of-window target;
3. resolved-date reintroduction;
4. requested-date mismatch;
5. wrong instrument ID;
6. wrong instrument name;
7. empty/no-record promotion;
8. missing raw payload;
9. wrong network-record instrument;
10. malformed timestamp;
11. negative interval;
12. adjacent-date record;
13. DOM/network contradiction;
14. missing expected DOM cross-check;
15. missing workflow provenance;
16. missing artifact ID;
17. malformed artifact SHA-256;
18. malformed probe commit;
19. incorrect reopen semantics;
20. partial-hour rounding.

All passed as specified.

## Evidence boundary preserved

Protocol PASS does not promote any additional date.

Only an independently validated positive exact broker-native record may be submitted to the date-level evidence gate.

Empty/no-record remains:

`BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

No negative-evidence inference is authorized.

## Boundary matrix

- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL = PASS`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE = PASS`
- `FREEZE_EXECUTION_WINDOW = BLOCKED`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`
- `REAL_BACKTEST = BLOCKED`

## Exactly one next governed action

**Fix and version the first deterministic recovery-batch policy/size before observing any new date outcomes, then execute that first batch in chronological order under `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1`.**

The batch size must be selected for operational/reproducibility reasons only, not because particular dates look easier or harder.

Do not move the window. Do not infer from empty responses. Do not download `.bi5`. Do not start a real backtest.
