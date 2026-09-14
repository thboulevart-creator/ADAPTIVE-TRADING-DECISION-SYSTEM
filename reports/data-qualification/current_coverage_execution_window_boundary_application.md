# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state

- Global research envelope: `2018-05-01` → `2026-08-14`
- Independently selected execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

## Calendar accounting after Trading Breaks Batch 02

### Global

- candidate dates: **111**
- resolved candidate dates: **30**
- unresolved candidate dates: **81**
- FAIL dates: **0**
- orphan special evidence: **0**
- contradictory evidence: **0**
- evidence-shape errors: **0**

Global coverage remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

### Fixed execution-window candidate

The selected window remains exactly:

`2021-08-14` → `2026-08-14`

Current in-window accounting:

- candidates: **68**
- resolved: **7**
- unresolved/BLOCKED: **61**
- FAIL: **0**

Resolved in-window candidates:

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
6. `2022-02-21 — PRESIDENTS_DAY`
7. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

The window MUST NOT be shifted, shortened, or lengthened to avoid unresolved dates.

## Evidence route and parent protocol

Historical broker route:

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

Systematic recovery protocol:

**PASS — `SYSTEMATIC_TRADING_BREAKS_RECOVERY_PROTOCOL_REJECTS_KNOWN_BYPASSES`**

The route remains qualified only for **positive exact historical break records**. Empty/no-record responses and neighboring-date overlaps do not prove regular trading and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Batch 02 — frozen before observation

Policy:

`04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-BATCH02-POLICY.md`

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02_POLICY_V1`

Frozen size:

`BATCH_SIZE = 5`

Immutable Batch 02 membership:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
3. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
4. `2022-02-21 — PRESIDENTS_DAY`
5. `2022-04-15 — GOOD_FRIDAY`

The membership and size were versioned before any Batch 02 browser observation.

### Authoritative runtime provenance

- workflow run: `34888022168`
- job: `104123381873`
- probe commit: `619a0200a9718827346d3c5458d1c1a290f3e5ce`
- artifact ID: `10364984459`
- artifact SHA-256: `ecd110649b1049d308171357ff0574aee4a8670c0d4f35c018854d7d3771ceab`
- workflow conclusion: **SUCCESS**
- instrument: `USATECH.IDX/USD` / Dukascopy ID `9016`

Runtime report:

`reports/data-qualification/historical_trading_breaks_recovery_batch02_runtime.json`

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_batch02_qualification.md`

### Independent Batch 02 adjudication

- `2021-12-24` → **BLOCKED — no exact target-date positive record admissible**
- `2021-12-31` → **BLOCKED — no positive exact broker record recovered**
- `2022-01-17` → **PASS — exact primary broker positive break record validated**
- `2022-02-21` → **PASS — exact primary broker positive break record validated**
- `2022-04-15` → **BLOCKED — no exact target-date positive record admissible**

Batch accounting:

- PASS: **2**
- BLOCKED: **3**
- FAIL: **0**

Only the two PASS records were integrated into executable calendar evidence.

## Executable evidence added by Batch 02

### 2022-01-17 — Martin Luther King Day

- broker record: `32811`
- break start: `17:59Z`
- final closed minute: `22:59Z`
- calibrated reopen: `23:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- exact DOM/network witness: concordant

### 2022-02-21 — Presidents Day

- broker record: `33515`
- break start: `17:59Z`
- final closed minute: `22:59Z`
- calibrated reopen: `23:00Z`
- fully closed UTC hours: `18,19,20,21,22`
- exact DOM/network witness: concordant

Persisted executable-evidence integration commit:

`95c7275e1bb7b4abea611a674568441b2a4c52f7`

## Regression after Batch 02 integration

Integration validation:

- run: `34888531830`
- job: `104125107659`
- conclusion: **SUCCESS**
- pytest: **98 passed**
- asserted global accounting: `111 / 30 resolved / 81 unresolved`
- asserted execution-window accounting: `68 / 7 resolved / 61 unresolved`

Independent regression against persisted repository state:

- run: `34888592937`
- job: `104125313335`
- conclusion: **SUCCESS**
- pytest: **70 passed**
- global accounting assertions: **PASS**
- orphan special evidence: `0`
- contradictory evidence: `0`
- evidence-shape errors: `0`

## Current recovery-queue boundary

The unresolved in-window queue contains **61** dates.

First unresolved candidate remains:

`2021-12-24 — CHRISTMAS_OBSERVED`

Last unresolved candidate remains:

`2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

This is intentional: a BLOCKED outcome does **not** resolve a calendar candidate.

### Newly exposed progression boundary

Batch 02 demonstrates that raw `recovery_queue()` and future execution eligibility are not the same concept once a date has already been attempted under the current positive-record route and remains BLOCKED.

A naive future scheduler using only:

`recovery_queue()[:5]`

would repeatedly select `2021-12-24`, `2021-12-31`, and `2022-04-15`, starving later unresolved candidates even though those three dates have already been attempted under the unchanged route.

This MUST NOT be solved by:

- marking BLOCKED dates resolved;
- creating negative evidence from absence;
- removing them from global/window unresolved accounting;
- shifting the execution window;
- manually skipping dates without a governed rule.

The required separation is:

1. **calendar evidence state** — PASS/resolved versus unresolved/BLOCKED;
2. **recovery attempt state** — whether a date has already been attempted under a specific route/protocol capability;
3. **batch execution eligibility** — whether a new attempt is justified under the current capability or requires an explicit retry predicate.

## Current boundary decisions

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01 = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02 = PASS`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST = BLOCKED — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Formalize and adversarially qualify an attempt-aware recovery progression contract before defining Batch 03.**

The contract must preserve all BLOCKED dates as unresolved calendar candidates while preventing dates already attempted under the unchanged Trading Breaks route/protocol capability from indefinitely starving later unresolved candidates. A blocked date may become execution-eligible again only through an explicit deterministic retry predicate tied to a material evidence-route/capability change, not convenience or expected outcome.

Only after that progression contract is PASS may Batch 03 membership be frozen and observed.

No `.bi5` acquisition. No real backtest.
