# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 09 independent adjudication PASS

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
- Batch 09 execution/capture: **PASS — exact frozen membership executed**
- Batch 09 independent adjudication: **PASS — `4 PASS / 1 BLOCKED / 0 FAIL`**
- Batch 09 atomic integration: **NOT STARTED**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 08 final closed state

Authoritative atomic integration commit: `aa85a2ade1fe9d9b1ade78f77b9b56c5310a6e74`.

Independent persisted-HEAD verifier trigger: `d996d1e3573bfc36437710cc95510ca73b519650`.

Final Batch 08 state:

- execution/adjudication: `4 PASS / 1 BLOCKED / 0 FAIL`;
- integration run/job: `34987791998` / `104444271495`;
- persisted-HEAD re-break run/job: `34988096558` / `104445314023`;
- `2024-03-29 — GOOD_FRIDAY` remains unresolved as `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`;
- post-Batch08 global state: `111 / 53 / 58 / 0 FAIL`;
- post-Batch08 execution window: `68 / 30 / 38 / 0 FAIL`;
- ledger: `40`;
- same-capability BLOCKED/ineligible: `10`;
- eligible unresolved: `28`.

## Batch 09 frozen membership — PASS

Selection rule at freeze time: `eligible_recovery_queue()[:5]`, fixed batch size `5`.

Mechanically frozen snapshot commit: `20a2c1722a2bc4798c0e5079ba51aa1f7bb5edb5`.

Frozen membership, exact order:

1. `2024-09-02 — LABOR_DAY`
2. `2024-11-28 — THANKSGIVING_DAY`
3. `2024-11-29 — THANKSGIVING_FRIDAY`
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2024-12-25 — CHRISTMAS_OBSERVED`

Freeze qualification:

- run/job: `34992224672` / `104459485505`;
- trigger: `e325a6d918daf3022be92a2ead9725e04030f0cc`;
- snapshot commit: `20a2c1722a2bc4798c0e5079ba51aa1f7bb5edb5`;
- pre-snapshot adversarial suite: `81 passed in 0.30s`;
- post-snapshot governed regression: `351 passed in 1.52s`.

Independent persisted-membership re-break:

- run/job: `34992441792` / `104460203391`;
- trigger: `1a8953d0d589e904bb465f0206bfa97ea05f73b4`;
- regression: `351 passed in 1.55s`;
- immutable snapshot and deterministic regeneration: PASS.

Membership workflows are archived manual-only.

## Batch 09 exact frozen execution — PASS

Authoritative execution provenance:

- workflow run: `34993614373`;
- job: `104464228483`;
- probe commit: `0b5dedf6028add27040af112d0bceef76be25827`;
- runtime persistence commit: `e1dce6a85aed3785c151c0b3e51138219cc50f87`;
- artifact: `10406357435`;
- artifact SHA-256: `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`;
- artifact files: `31`;
- artifact size: `3599127` bytes.

All pre-browser identity/immutability/protocol gates passed before Chromium. Governed regression: `359 passed in 1.31s`. Execution consumed only immutable `batch09_targets()`; no skip, substitution, reorder, duplicate, expansion or shortening occurred.

Authoritative runtime:

`reports/data-qualification/historical_trading_breaks_recovery_batch09_runtime.json`

The execution workflow is archived manual-only at commit `785b29fa0e54848d21f02ce88b9e56a51adf8cd3`.

## Batch 09 independent adjudication — PASS

Adjudication was performed offline against the persisted runtime and immutable `batch09_targets()` only. There was no Playwright, Chromium, browser, `probe_candidate`, live recovery queue, progression selection, or membership recalculation path.

Authoritative adjudication run:

- corrected authoritative run: `34995973784`;
- job: `104472165374`;
- trigger commit: `a23836aa296dbfb6080b0b710aacc493a42edc20`;
- full governed + adversarial regression: `387 passed in 1.39s`;
- persisted adjudication evidence commit: `394753a95259356a205dd98a7675bddfb6b53b2e`;
- verdict: **PASS — `BATCH09_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**;
- accounting: **4 PASS / 1 BLOCKED / 0 FAIL**.

The adjudicator independently verified the locked execution provenance against GitHub Actions before adjudication:

- run `34993614373` conclusion/head SHA;
- job `104464228483` identity/conclusion;
- artifact `10406357435` non-expired;
- SHA-256 `dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc`;
- probe commit `0b5dedf6028add27040af112d0bceef76be25827`.

Date-level adjudication:

1. `2024-09-02 — LABOR_DAY` → **PASS**, record `70878`, fully closed UTC hours `[17,18,19,20,21]`.
2. `2024-11-28 — THANKSGIVING_DAY` → **PASS**, record `72887`, fully closed UTC hours `[18,19,20,21,22]`.
3. `2024-11-29 — THANKSGIVING_FRIDAY` → **PASS**, record `72888`, start `18:14:59Z`; hour `18` is not rounded closed; fully closed hours `[19,20,21,22,23]`.
4. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION` → **PASS**, record `74339`, start `18:14:59Z`; hour `18` is not rounded closed; fully closed hours `[19,20,21,22,23]`.
5. `2024-12-25 — CHRISTMAS_OBSERVED` → **BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`**. Capture was `CAPTURED`, but record `74339` starts on `2024-12-24`, so the cross-date overlap is not promoted.

Adversarial coverage included frozen-membership tampering, result reordering, run/job/artifact/hash/probe/artifact-URL provenance tampering, wrong requested date/epoch/instrument, DOM/network contradiction, duplicate network records, duplicate DOM witnesses, missing network with DOM, capture-layer `PASS` injection, `CAPTURED → PASS` bypass, stored reopen tampering and partial-hour rounding tampering.

The first adjudication run `34995813928` reached and passed all semantic gates, `387 tests`, adjudication, exact result assertion and executable-state non-mutation, but the final persistence step failed solely because `git diff --cached --check` rejected an extra blank line at EOF in the generated Markdown. No governed state was mutated. The persistence harness was minimally corrected to normalize the report EOF; the complete workflow was rerun as `34995973784` and passed end to end.

Persisted reports:

- `reports/data-qualification/historical_trading_breaks_recovery_batch09_adjudication.json`
- `reports/data-qualification/historical_trading_breaks_recovery_batch09_qualification.md`

The completed adjudication workflow is archived to `workflow_dispatch` only at commit `4a5b3e048c2c8f1aef460706d91ec632e8d2036c`.

## State mutation boundary after adjudication

Independent adjudication is evidence-only. It does not itself integrate executable calendar evidence or factual attempt outcomes.

Therefore the persisted executable state is still unchanged from post-Batch08 integration:

- global executable calendar: `111 / 53 resolved / 58 unresolved / 0 FAIL`;
- execution window: `68 / 30 resolved / 38 unresolved / 0 FAIL`;
- raw recovery queue: `38`;
- historical attempt ledger: `40`;
- material capability changes: `0`;
- same-capability attempted BLOCKED/ineligible: `10`;
- eligible unresolved: `28`.

The next atomic integration, if it passes, must apply exactly four PASS dates to executable calendar evidence and append all five factual Batch 09 attempts to the ledger. The expected post-integration state to prove, not assume, is:

- global: `111 / 57 resolved / 54 unresolved / 0 FAIL`;
- execution window: `68 / 34 resolved / 34 unresolved / 0 FAIL`;
- ledger: `45`;
- same-capability BLOCKED/ineligible: `11`;
- eligible unresolved: `23`;
- `2024-12-25` remains unresolved and becomes same-capability attempted BLOCKED/ineligible.

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_INDEPENDENT_ADJUDICATION`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

Still BLOCKED downstream:

- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_ATOMIC_INTEGRATION — NOT YET EXECUTED`
- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Atomically integrate the independently adjudicated Batch 09 outcomes into executable calendar evidence, the historical attempt ledger and deterministic progression state, consuming only the persisted Batch 09 adjudication and immutable `batch09_targets()`.**

The integration must:

- add executable special-session evidence for exactly the four adjudicated PASS dates and no other date;
- append exactly five factual Batch 09 attempts to the historical ledger in frozen order;
- preserve `2024-12-25` unresolved with adjudicated BLOCKED reason `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`;
- regenerate progression deterministically;
- reject duplicate/reordered/substituted outcomes, provenance drift, cross-date promotion and any attempt to integrate the BLOCKED date;
- prove the expected post-state `111/57/54`, window `68/34/34`, ledger `45`, BLOCKED/ineligible `11`, eligible `23`, capability changes `0`;
- rerun the complete governed regression after mutation;
- remain on the same branch, with no `.bi5` and no real backtest.

A persisted-HEAD re-break remains a separate governed action after atomic integration PASS.