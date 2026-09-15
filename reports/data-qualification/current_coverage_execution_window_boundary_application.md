# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 09 atomic integration PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 57 resolved / 54 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 34 resolved / 34 unresolved / 0 FAIL**
- Historical Trading Breaks broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Attempt-aware recovery progression: **PASS**
- Historical attempt ledger entries: **45**
- Registered material capability changes: **0**
- Attempted BLOCKED / same-capability execution-ineligible: **11**
- Execution-eligible unresolved: **23**
- Current semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- Capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- Batch 08: **FROZEN → EXECUTED → ADJUDICATED → ATOMICALLY INTEGRATED → PERSISTED-HEAD RE-BREAK PASS**
- Batch 09 membership: **FROZEN + ADVERSARIALLY QUALIFIED + INDEPENDENT PERSISTED-MEMBERSHIP RE-BREAK PASS**
- Batch 09 execution/capture: **PASS**
- Batch 09 independent adjudication: **PASS — `4 PASS / 1 BLOCKED / 0 FAIL`**
- Batch 09 atomic integration: **PASS — `BATCH09_ATOMIC_CALENDAR_ATTEMPT_PROGRESSION_INTEGRATION_COHERENT`**
- Batch 09 persisted-HEAD re-break: **PENDING — separate governed action**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 09 immutable frozen membership

Frozen snapshot commit: `20a2c1722a2bc4798c0e5079ba51aa1f7bb5edb5`.

Exact frozen order:

1. `2024-09-02 — LABOR_DAY`
2. `2024-11-28 — THANKSGIVING_DAY`
3. `2024-11-29 — THANKSGIVING_FRIDAY`
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2024-12-25 — CHRISTMAS_OBSERVED`

All execution, adjudication and integration work consumed immutable `batch09_targets()`; the membership was not reconstructed from a live queue.

## Batch 09 execution and independent adjudication

Authoritative execution provenance:

- execution run/job: `34993614373` / `104464228483`
- probe commit: `0b5dedf6028add27040af112d0bceef76be25827`
- runtime persistence commit: `e1dce6a85aed3785c151c0b3e51138219cc50f87`
- artifact: `10406357435`
- artifact SHA-256: `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`

Independent adjudication:

- run/job: `34995973784` / `104472165374`
- trigger commit: `a23836aa296dbfb6080b0b710aacc493a42edc20`
- regression: `387 passed in 1.39s`
- persisted evidence commit: `394753a95259356a205dd98a7675bddfb6b53b2e`
- verdict: **PASS — `BATCH09_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**
- accounting: **4 PASS / 1 BLOCKED / 0 FAIL**

Date-level outcomes:

- `2024-09-02 — LABOR_DAY` → PASS, record `70878`, whole closed UTC hours `[17,18,19,20,21]`.
- `2024-11-28 — THANKSGIVING_DAY` → PASS, record `72887`, hours `[18,19,20,21,22]`.
- `2024-11-29 — THANKSGIVING_FRIDAY` → PASS, record `72888`, start `18:14:59Z`; hour `18` remains open; hours `[19,20,21,22,23]`.
- `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION` → PASS, record `74339`, start `18:14:59Z`; hour `18` remains open; hours `[19,20,21,22,23]`.
- `2024-12-25 — CHRISTMAS_OBSERVED` → **BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**. Record `74339` starts on `2024-12-24`; the cross-date overlap is not promoted.

## Batch 09 atomic integration — PASS

Integration workflow:

- trigger commit: `f80db7bde42cf6cdcec3d43e62b862d9cdd97c0b`
- run/job: `34997562157` / `104477530292`
- pre-mutation adversarial contract suite: `98 passed in 0.28s`
- exact pre-state/anti-partial guard: PASS
- deterministic progression regeneration: PASS
- full post-mutation governed regression: **`399 passed in 1.24s`**
- exact post-state assertion: PASS
- no-browser/no-capture/no-live-membership AST guard: PASS
- atomic integration commit: `126ff25129728dc9f5c26cfeff701c1e04270843`
- qualification report: `reports/data-qualification/historical_trading_breaks_recovery_batch09_integration_qualification.md`

The integration committed one coherent state transition only after all worktree checks passed.

Exact calendar mutation:

- added `2024-09-02` only from adjudicated PASS record `70878`;
- added `2024-11-28` only from adjudicated PASS record `72887`;
- added `2024-11-29` only from adjudicated PASS record `72888`;
- added `2024-12-24` only from adjudicated PASS record `74339`;
- **did not add `2024-12-25`** to `SPECIAL_SESSION_EVIDENCE`;
- **did not add `2024-12-25`** to `NO_SPECIAL_CHANGE_EVIDENCE`.

Exact ledger mutation:

- `41 — batch09:2024-09-02 — PASS`
- `42 — batch09:2024-11-28 — PASS`
- `43 — batch09:2024-11-29 — PASS`
- `44 — batch09:2024-12-24 — PASS`
- `45 — batch09:2024-12-25 — BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

After deterministic progression regeneration:

- raw unresolved queue: `34`;
- attempt ledger: `45`;
- same-capability attempted BLOCKED/ineligible: `11`;
- execution-eligible unresolved: `23`;
- capability changes: `0`;
- `2024-12-25` remains unresolved, latest attempt `batch09:2024-12-25`, outcome `BLOCKED`, eligibility reason `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`;
- first execution-eligible unresolved candidate is `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`.

The completed Batch 09 integration workflow is archived to `workflow_dispatch` only with read permissions at commit `937accbcf00647c1c234ee96ae6bc3339db8d4c0`. A normal push cannot silently repeat the integration.

## Current boundary decisions

PASS now includes:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_CONTRACT`
- all completed Batch 01–08 recovery/integration gates, including Batch 08 persisted-HEAD re-break
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_PERSISTED_MEMBERSHIP_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_EXECUTION_CAPTURE`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_INDEPENDENT_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_ATOMIC_INTEGRATION`

Still BLOCKED / pending downstream:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_PERSISTED_HEAD_REBREAK — NOT YET EXECUTED`
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

No `.bi5` acquisition occurred. No real backtest occurred.

## Exactly one next governed action

**Independently re-break the persisted HEAD after Batch 09 atomic integration, read-only and from the persisted integrated state, proving that calendar evidence, ledger `41..45`, deterministic progression, exact `111/57/54` + `68/34/34` accounting, unresolved/ineligible `2024-12-25`, and all adversarial regressions survive independently of the mutation workflow.**

Do not freeze Batch 10 before that persisted-HEAD re-break passes. Do not rerun Batch 09 execution or adjudication. No `.bi5`. No real backtest.
