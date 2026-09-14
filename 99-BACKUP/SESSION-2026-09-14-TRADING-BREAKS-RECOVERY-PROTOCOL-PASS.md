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

## Local workstation archive verification — 2026-09-14

Canonical local root:

`C:\Users\Boulevart\Documents\ADAPTIVE-TRADING-DECISION-SYSTEM\LOCAL-EVIDENCE\dukascopy-trading-breaks-widget\2026-09-14\raw-zips\`

The three retained ZIP artifacts were independently re-hashed on the workstation with PowerShell `Get-FileHash -Algorithm SHA256` after being placed under the canonical local evidence root.

Observed hashes:

- `dukascopy-trading-breaks-widget-2020-02-17-authoritative.zip`
  - `F49FB3AA5B66C22127EDA3AC4593A387F6F83D3AB1D1D31EB742D44C49FB6A91`
- `dukascopy-trading-breaks-widget-2020-02-17-headed-browser.zip`
  - `AAF5341F3D7E10B60CC24622D6F16C2FFA3E3F31D6B108F69F53C6F3A2D48849`
- `dukascopy-trading-breaks-widget-pilot-2021-09-06-authoritative.zip`
  - `8D8B568E17FD0E8D5D8C448742290313F78614CCD95C915AEF5B978ED7F90DDC`

These values match `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv` exactly (case-insensitive hexadecimal representation).

The local helper script had been removed after use, then was restored explicitly from:

`origin/feat/multi-year-dukascopy-acquisition`

Verified local state:

- `Test-Path .\tools\archive_local_trading_breaks_evidence.ps1` → `True`
- local SHA-256: `F8B5593EBB754A77A80728880B3FEDFD1F3FB750A2FEFAC00B3F4E48C5AF56B7`

This local script hash is recorded as a workstation-file integrity observation; the repository remains authoritative for the versioned script content.

The raw ZIPs remain local and Git-ignored. GitHub stores the governed manifest, documentation, probes, workflows and recovery state — not duplicate binary ZIP payloads.

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
