# TRADING BREAKS TARGET-DAY OVERLAP SEMANTICS — QUALIFICATION

**PASS — `TARGET_DAY_OVERLAP_ATTRIBUTION_ADVERSARIALLY_QUALIFIED`**

Contract: `TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1`

Qualified proof capability: `QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION`

Addresses blocker: `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

## Authoritative qualification

- trigger/qualification commit: `061e97d90eed2c4c3f1d5f2a261e457fd796413f`
- workflow run/job: `35064060544` / `104690359352`
- permissions: `contents: read`
- focused adversarial suite: `76 passed in 0.23s`
- persisted Class-A cases qualified offline: `14 / 14 PASS`
- full governed regression: `472 passed in 1.81s`
- browser/Chromium/Playwright/probe/live-selection path: NONE
- governed calendar/ledger/progression/capability registry mutation: NONE
- final worktree: clean

## Qualified semantic rule

A broker-native positive Trading Breaks interval may support a target day even when the interval starts on an earlier calendar day, provided the independent validator proves all of the following:

- exact target/requested date identity;
- exact USATECH instrument identity;
- retained raw primary broker payload;
- exactly one unambiguous broker record;
- well-formed broker-native interval;
- actual temporal overlap with the target UTC day;
- at least one complete target-day UTC hour proven closed;
- start/end/reopen derivatives recompute exactly from raw broker timestamps;
- target-day whole closed hours recompute exactly, with no partial-hour rounding;
- workflow/job/artifact/hash/probe provenance is complete and valid;
- if DOM evidence exists, it must agree exactly with the primary network record; contradiction is FAIL.

DOM absence alone is not promoted into evidence. It is tolerated only when the primary broker-network record and retained provenance independently satisfy the full contract.

## Adversarial rejection proven

The qualification rejects at minimum:

- adjacent but non-overlapping records;
- wrong requested/target date;
- wrong instrument;
- reversed/malformed intervals;
- fabricated reopen timestamps;
- missing raw payload or provenance;
- multiple/ambiguous records;
- DOM/network contradictions;
- tampered or rounded target-day hours;
- unrelated-year record borrowing;
- `CAPTURED → PASS` bypass;
- overlap that proves no complete UTC target-day hour.

## Class-A result

All fourteen historical dates blocked solely by `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE` passed this offline semantic contract against their already persisted broker-native evidence. Historical attempts remain immutable and no current capability has been changed by this qualification itself.

No new browser capture. No `.bi5`. No real backtest.
