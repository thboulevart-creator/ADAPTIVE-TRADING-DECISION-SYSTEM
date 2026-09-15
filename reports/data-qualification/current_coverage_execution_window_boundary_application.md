# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 09 exact frozen execution capture PASS

- Global research envelope: `2018-05-01` → `2026-08-14`
- Execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Persisted executable global calendar: **111 candidates / 53 resolved / 58 unresolved / 0 FAIL**
- Persisted execution-window candidate: **68 candidates / 30 resolved / 38 unresolved / 0 FAIL**
- Historical Trading Breaks broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Attempt-aware recovery progression: **PASS**
- Historical attempt ledger entries: **40**
- Registered material capability changes: **0**
- Attempted BLOCKED / same-capability execution-ineligible: **10**
- Execution-eligible unresolved: **28**
- Current semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- Capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- Batch 08: **FROZEN → EXECUTED → INDEPENDENTLY ADJUDICATED → ATOMICALLY INTEGRATED → PERSISTED-HEAD RE-BREAK PASS**
- Batch 09 membership: **FROZEN + ADVERSARIALLY QUALIFIED + INDEPENDENT PERSISTED-MEMBERSHIP RE-BREAK PASS**
- Batch 09 execution/capture: **PASS — EXACT FROZEN MEMBERSHIP EXECUTED; INDEPENDENT ADJUDICATION PENDING**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 08 final closed state

Authoritative atomic integration commit: `aa85a2ade1fe9d9b1ade78f77b9b56c5310a6e74`.

Independent persisted-HEAD verifier trigger: `d996d1e3573bfc36437710cc95510ca73b519650`.

Final Batch 08 state:

- execution/adjudication: `4 PASS / 1 BLOCKED / 0 FAIL`;
- integration run/job: `34987791998` / `104444271495`;
- post-mutation regression: `335 passed in 1.62s`;
- persisted-HEAD re-break run/job: `34988096558` / `104445314023`;
- persisted regression: `335 passed in 1.47s`;
- `2024-03-29 — GOOD_FRIDAY` remains unresolved as `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`;
- global state: `111 / 53 / 58 / 0 FAIL`;
- execution window: `68 / 30 / 38 / 0 FAIL`;
- ledger: `40`;
- same-capability BLOCKED/ineligible: `10`;
- eligible unresolved: `28`.

Historical Batch 08 harness corrections remain preserved in the Batch 08 backup/checkpoint: the initial integration source-text false positive and first persisted verifier `__pycache__` cleanliness issue were both corrected and completely rerun without governed-state mutation.

## Batch 09 mechanical membership freeze — PASS

Freeze baseline checkpoint: `2e94b8bfa1459d300ee315d0754f84973be2dd1e`.

Selection rule: `eligible_recovery_queue()[:5]` with fixed batch size `5`.

Authoritative freeze:

- run/job: `34992224672` / `104459485505`;
- trigger commit: `e325a6d918daf3022be92a2ead9725e04030f0cc`;
- frozen snapshot commit: `20a2c1722a2bc4798c0e5079ba51aa1f7bb5edb5`;
- pre-snapshot adversarial suite: `81 passed in 0.30s`;
- post-snapshot full governed regression: `351 passed in 1.52s`;
- persisted pre-freeze state: raw unresolved `38`, eligible `28`, attempts `40`, BLOCKED/ineligible `10`, capability changes `0`;
- all five members were `INITIAL_ATTEMPT` with no prior factual attempt.

Frozen membership:

1. `2024-09-02 — LABOR_DAY`
2. `2024-11-28 — THANKSGIVING_DAY`
3. `2024-11-29 — THANKSGIVING_FRIDAY`
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2024-12-25 — CHRISTMAS_OBSERVED`

Independent persisted-membership re-break:

- trigger commit: `1a8953d0d589e904bb465f0206bfa97ea05f73b4`;
- run/job: `34992441792` / `104460203391`;
- permissions: `contents: read`;
- full regression: `351 passed in 1.55s`;
- `batch09_targets() == eligible_recovery_queue()[:5]` at persisted freeze state: PASS;
- deterministic progression regeneration and clean read-only worktree: PASS.

Freeze/qualification workflows are archived manual-only at commits `884f03d32d8b08ea10bbfa32ca689deaacef9955` and `65ce1af2ea52a3c40fa7597effef2e45b45703c2`.

## Batch 09 exact frozen execution — CAPTURE PASS, ADJUDICATION PENDING

Execution was built by reusing exactly the registered semantic capture implementation `tools.trading_breaks_recovery_batch01.probe_candidate`. The execution wrapper accepts no caller-provided membership and obtains targets only from `batch09_targets()`.

Execution provenance:

- workflow trigger/probe commit: `0b5dedf6028add27040af112d0bceef76be25827`;
- run: `34993614373`;
- job: `104464228483`;
- runtime persistence commit: `e1dce6a85aed3785c151c0b3e51138219cc50f87`;
- artifact: `10406357435`;
- artifact SHA-256: `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`;
- artifact files: `31`;
- artifact size: `3599127` bytes.

All pre-browser gates passed before Chromium installation/opening:

- checkpoint ancestry and frozen-state immutability: PASS;
- full governed + Batch 09 execution regression: `359 passed in 1.31s`;
- exact immutable frozen identity: PASS;
- execution path has no live `eligible_recovery_queue`, `recovery_queue`, progression, freeze-derivation, skip/priority selection call: PASS;
- qualified `probe_candidate` itself has no membership-selection call: PASS.

The browser then executed exactly the five frozen members in order. No member was skipped, substituted, reordered, duplicated, added or removed.

Raw capture-layer results, deliberately **not yet date-level adjudication verdicts**:

- `2024-09-02`: `CAPTURED`, record `70878`, broker-native start `2024-09-02T16:59:59Z`, broker reason `Labor Day`.
- `2024-11-28`: `CAPTURED`, record `72887`, start `2024-11-28T17:59:59Z`, broker reason `Thanksgiving Day`.
- `2024-11-29`: `CAPTURED`, record `72888`, start `2024-11-29T18:14:59Z`, multi-day interval through `2024-12-01T22:59:59Z`, broker reason `Thanksgiving Day`.
- `2024-12-24`: `CAPTURED`, record `74339`, start `2024-12-24T18:14:59Z`, interval through `2024-12-25T22:59:59Z`, broker reason `Christmas`.
- `2024-12-25`: capture returned the same overlapping record `74339`, whose native start is `2024-12-24T18:14:59Z`; this is **not** promoted here and must be attacked by independent cross-date adjudication.

All five raw results retained instrument `USATECH.IDX/USD`, observed instrument ID `9016`, requested-date metadata, broker payload, DOM witness and no runtime error. Capture-layer `CAPTURED` means only `POSITIVE_RECORD_CAPTURED_PENDING_ARTIFACT_PROVENANCE_ADJUDICATION`.

Authoritative persisted runtime:

`reports/data-qualification/historical_trading_breaks_recovery_batch09_runtime.json`

Execution qualification:

`reports/data-qualification/historical_trading_breaks_recovery_batch09_execution_qualification.md`

The completed execution workflow is archived to `workflow_dispatch` only at commit `785b29fa0e54848d21f02ce88b9e56a51adf8cd3`. Normal pushes cannot silently execute Batch 09 again.

## State mutation boundary after execution

Execution/capture alone does not resolve dates and does not create factual ledger adjudication outcomes. Therefore until independent adjudication and later atomic integration:

- global executable calendar remains `111 / 53 resolved / 58 unresolved / 0 FAIL`;
- execution window remains `68 / 30 resolved / 38 unresolved / 0 FAIL`;
- raw recovery queue remains `38`;
- historical attempt ledger remains `40`;
- capability changes remain `0`;
- same-capability attempted BLOCKED/ineligible remains `10`;
- eligible unresolved remains `28`.

No `.bi5` acquisition occurred. No real backtest occurred.

## Current boundary decisions

PASS now includes:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_CONTRACT`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_PERSISTED_HEAD_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_PERSISTED_MEMBERSHIP_REBREAK`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_EXECUTION_CAPTURE`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

Still BLOCKED downstream:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_INDEPENDENT_ADJUDICATION`
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Independently adjudicate the persisted Batch 09 runtime against the immutable `batch09_targets()` membership and exact locked execution provenance, with no browser and no live membership recalculation.**

The adjudicator must independently attack at least frozen-membership tampering/reordering, provenance tampering, wrong instrument/date, DOM/network contradiction, duplicate records, cross-date promotion (especially `2024-12-25` record `74339`), partial-hour rounding, and any attempt to equate capture-layer `CAPTURED` with automatic date-level PASS.

Do not integrate calendar evidence or append Batch 09 ledger outcomes before adjudication PASS. No `.bi5`. No real backtest.
