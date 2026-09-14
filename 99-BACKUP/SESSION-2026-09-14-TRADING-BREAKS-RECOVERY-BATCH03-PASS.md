# SESSION BACKUP — 14 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY BATCH 03 PASS

## Final verdict

**PASS — Batch 03 independently adjudicated, atomically integrated, and independently re-broken on persisted HEAD.**

Batch accounting:

- attempted: `5`
- PASS: `4`
- BLOCKED: `1`
- FAIL: `0`

No absence of evidence was promoted to PASS or to `NO_SPECIAL_CHANGE_EVIDENCE`.

## Frozen Batch 03 membership

1. `2022-05-30 — MEMORIAL_DAY`
2. `2022-06-20 — JUNETEENTH_OBSERVED`
3. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
4. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
5. `2022-09-05 — LABOR_DAY`

Membership was frozen and adversarially qualified before observation. It was never recalculated during execution or adjudication.

## Authoritative browser execution

- workflow run: `34892253133`
- job: `104137558818`
- probe commit: `9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4`
- artifact ID: `10367930592`
- artifact SHA-256: `994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41`
- instrument: `USATECH.IDX/USD` / `9016`
- pre-browser gates: PASS

Observed and independently adjudicated:

- `2022-05-30` → PASS — broker record `37019`, `Memorial Day`, fully closed UTC hours `17–21`
- `2022-06-20` → PASS — broker record `38945`, `Juneteenth Holiday`, fully closed UTC hours `17–21`
- `2022-07-01` → BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`
- `2022-07-04` → PASS — broker record `41225`, `Independence Day`, fully closed UTC hours `17–21`
- `2022-09-05` → PASS — broker record `42569`, `Labor Day`, fully closed UTC hours `17–21`

Only the four PASS dates were integrated into executable calendar evidence.

## First adversarial adjudication FAIL and correction

First adjudication run:

- run: `34892773715`
- job: `104139273746`
- result: FAIL before accepting a final adjudication

Root cause: the DOM exposes the human instrument name `USATECH.IDX/USD`, while the network record uses Dukascopy instrument ID `9016`. The initial adapter compared those representations directly and generated a false `DOM_NETWORK_CONTRADICTION`.

Minimal correction:

- validate the exact DOM human name first;
- normalize it to governed ID `9016` only after that validation;
- attack a wrong DOM instrument name explicitly so it cannot be silently normalized.

Corrected adjudication re-break:

- run: `34893116066`
- job: `104140394051`
- conclusion: SUCCESS
- suite: `62 passed`
- final adjudication: `4 PASS / 1 BLOCKED / 0 FAIL`
- persisted adjudication commit: `a46e48ee4e4b1828e28418bfca1a0f84fd795b19`

## First atomic integration FAIL and correction

First integration run:

- run: `34893471211`
- job: `104141565466`
- result: FAIL
- integration commit pushed: **NO**

The branch therefore remained clean.

The run found:

1. a stale Batch 02 regression asserting the old current unresolved count `61` instead of post-Batch03 `57`;
2. historical adjudication replay was incorrectly tied to live `recovery_queue()`. Once PASS dates were integrated and left the unresolved queue, a historical replay would falsely reject them.

Correction:

- live recovery validation remains tied to current `recovery_queue()` so resolved dates cannot re-enter execution eligibility;
- historical replay is validated against an immutable frozen batch scope only;
- frozen replay scope rejects empty/malformed scope, duplicates, non-chronological order, absent target and candidate-reason substitution;
- this correction does not mutate the live queue and does not register a material broker-evidence capability change.

No new broker observation was required.

## Final atomic integration PASS

- run: `34893854678`
- job: `104142824703`
- regression: `104 passed`
- atomic integration commit: `d85d6102f8b9d9204521dacfbdcc3a0212f8de5e`

The same atomic commit integrated:

- the four PASS dates into calendar evidence;
- all five Batch 03 factual attempts into the attempt ledger;
- the regenerated progression runtime and regression boundaries.

`2022-07-01` remained unresolved/BLOCKED.

## Independent persisted-HEAD proof

After the integration commit had already been persisted, the branch was independently checked again:

- run: `34893976903`
- job: `104143235284`
- conclusion: SUCCESS
- suite: `104 passed in 0.60s`

Confirmed persisted state:

- global calendar: `111 / 34 resolved / 77 unresolved / 0 FAIL`
- execution-window candidate: `68 / 11 resolved / 57 unresolved / 0 FAIL`
- attempt ledger entries: `15`
- registered material capability changes: `0`
- attempted BLOCKED / currently ineligible: `4`
- currently execution-eligible unresolved: `53`
- first currently eligible unresolved candidate: `2022-11-24 — THANKSGIVING_DAY`

The four attempted BLOCKED/ineligible dates are:

- `2021-12-24`
- `2021-12-31`
- `2022-04-15`
- `2022-07-01`

They remain unresolved in calendar accounting and are excluded only from current execution eligibility under the unchanged capability.

## Workflow closure

The following Batch 03 workflows are archived to `workflow_dispatch` only:

- Batch 03 membership policy qualification
- Batch 03 browser execution
- Batch 03 independent adjudication
- Batch 03 atomic integration
- Batch 03 persisted-HEAD regression

No normal push can silently replay the completed Batch 03 chain.

## Local ZIP evidence

The previously governed three local ZIP archives remain **PASS** and require no corrective action.

Versioned references:

- `LOCAL-EVIDENCE/README.md`
- `LOCAL-EVIDENCE/dukascopy-trading-breaks-widget/2026-09-14/manifest-sha256.csv`

The ZIP binaries themselves remain intentionally ignored by Git. Their names, sizes, roles, workflow/artifact identities and independently checked SHA-256 hashes remain versioned in the manifest.

## Current boundary state

PASS:

- historical Trading Breaks route
- recovery protocol
- Batch 01
- Batch 02
- attempt-aware progression
- Batch 03 membership freeze
- Batch 03 execution/adjudication/integration
- persisted-HEAD Batch 03 regression
- local runtime evidence archive

Still BLOCKED:

- global coverage PASS
- execution-window freeze
- massive `.bi5` acquisition
- real backtest

## Exactly one next governed action

**Freeze and version Batch 04 with `BATCH_SIZE = 5` as exactly the first five entries of the current governed `eligible_recovery_queue()`, BEFORE any Batch 04 historical observation.**

The complete Batch 04 membership is deliberately **not defined in this backup**. It must be mechanically derived and versioned during the freeze itself. The only current execution-progression fact recorded here is that the first eligible unresolved candidate is `2022-11-24 — THANKSGIVING_DAY`.

No `.bi5`. No real backtest.
