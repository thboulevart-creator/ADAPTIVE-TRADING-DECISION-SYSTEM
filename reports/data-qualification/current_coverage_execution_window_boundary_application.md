# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state

- Global research envelope: `2018-05-01` → `2026-08-14`
- Independently selected execution-window candidate: `2021-08-14` → `2026-08-14`
- Window frozen: **NO**
- Global calendar: **111 candidates / 30 resolved / 81 unresolved / 0 FAIL**
- Execution-window candidate: **68 candidates / 7 resolved / 61 unresolved / 0 FAIL**
- Historical broker-evidence route: **PASS**
- Systematic Trading Breaks recovery protocol: **PASS**
- Recovery Batch 01: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**
- Recovery Batch 02: **PASS — 2 PASS / 3 BLOCKED / 0 FAIL**
- Attempt-aware recovery progression: **PASS**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened, or lengthened to avoid unresolved dates.

## Calendar evidence state after Batch 02

Resolved in-window dates remain:

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
6. `2022-02-21 — PRESIDENTS_DAY`
7. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

Global coverage remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

The positive-record boundary remains unchanged: empty/no-record responses and neighboring-date overlaps do not prove regular trading and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.

## Batch 02 authoritative provenance

Frozen membership:

1. `2021-12-24 — CHRISTMAS_OBSERVED`
2. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
3. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
4. `2022-02-21 — PRESIDENTS_DAY`
5. `2022-04-15 — GOOD_FRIDAY`

Runtime:

- workflow run: `34888022168`
- job: `104123381873`
- probe commit: `619a0200a9718827346d3c5458d1c1a290f3e5ce`
- artifact ID: `10364984459`
- artifact SHA-256: `ecd110649b1049d308171357ff0574aee4a8670c0d4f35c018854d7d3771ceab`
- conclusion: **SUCCESS**

Independent adjudication:

- `2021-12-24` → **BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE**
- `2021-12-31` → **BLOCKED — NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED**
- `2022-01-17` → **PASS**
- `2022-02-21` → **PASS**
- `2022-04-15` → **BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE**

Only the two PASS dates were integrated.

Persisted executable-evidence commit:

`95c7275e1bb7b4abea611a674568441b2a4c52f7`

Post-integration validation:

- integration run `34888531830`, job `104125107659`: **98 passed**
- independent calendar regression `34888592937`, job `104125313335`: **70 passed**
- global accounting: `111 / 30 / 81`
- window accounting: `68 / 7 / 61`
- orphan evidence: `0`
- contradictory evidence: `0`
- evidence-shape errors: `0`

## Attempt-aware recovery progression — qualified

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_progression_qualification.md`

Final verdict:

**PASS — `ATTEMPT_AWARE_RECOVERY_PROGRESSION_REJECTS_RETRY_BYPASSES_AND_PREVENTS_STARVATION`**

The progression boundary now separates three distinct states:

1. **calendar evidence state** — resolved versus unresolved/BLOCKED;
2. **attempt history** — immutable factual executions under semantic capabilities;
3. **execution eligibility** — whether another execution is currently justified.

Authoritative attempt ledger:

`reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`

Authoritative material-capability-change registry:

`reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`

Current capability:

`TRADING_BREAKS_PRIMARY_WIDGET_V1`

Current semantic fingerprint:

`82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

The ledger contains **10** historical attempts. The material capability-change registry contains **0** qualified changes.

### Current deterministic progression state

- calendar unresolved dates: **61**
- historical attempts: **10**
- registered material capability changes: **0**
- already-attempted BLOCKED / currently execution-ineligible: **3**
- unresolved currently execution-eligible: **58**

The following dates remain unresolved but cannot be replayed under the unchanged current capability:

- `2021-12-24` → `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`
- `2021-12-31` → `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`
- `2022-04-15` → `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

They remain in `recovery_queue()` and in the `61` unresolved count. They are excluded only from the execution projection `eligible_recovery_queue()`.

Later never-attempted unresolved dates remain execution-eligible, so the attempted-BLOCKED prefix no longer causes starvation.

## Adversarial progression qualification history

First nominal adversarial run:

- run: `34890138036`
- job: `104130467209`
- trigger commit: `fe09849451c868a9abb624d9d1525539e0b49d25`
- suite: **67 passed**

That nominal PASS was deliberately not accepted as final. A second design review found two genuine bypasses:

1. a relevant `proof_capability` token alone could masquerade as a material capability change;
2. caller-supplied progression inputs could inject an unversioned retry authorization.

Minimal corrections now require an actual route/protocol/capture change, newly qualified blocker-relevant proof capability, no proof-capability regression, exact fingerprints/dimensions, and a versioned qualification contract/commit. Production scheduling accepts no caller-provided attempts/current capability/change authorization.

Final corrected re-break:

- run: `34890560172`
- job: `104131879994`
- trigger commit: `c020a5132d053011f517007b9562b5257bbf9aaf`
- suite: **72 passed in 0.51s**
- corrected runtime commit: `b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`
- runtime verdict: **PASS — `ATTEMPT_AWARE_PROGRESSION_STATE_IS_DETERMINISTIC_AND_NON_STARVING`**

The progression qualification workflow is archived to `workflow_dispatch` only after PASS.

## Retry semantics now frozen

A BLOCKED date may become execution-eligible again only after a versioned, qualified material evidence-capability change that:

- changes the exact semantic fingerprint;
- changes a real executable semantic dimension (`route_contract`, `protocol_contract`, or `capture_implementation`);
- adds a blocker-relevant proof capability;
- removes no previously qualified proof capability;
- binds exact old/new fingerprints and actual changed dimensions;
- has its own qualification contract and qualification commit.

A new run/job/artifact/probe commit under the same capability is not a material change.

A proof-capability token alone is not a material change.

## Current boundary decisions

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT = PASS`
- `WINDOW_SELECTION_RULE = PASS`
- `WINDOW_CANDIDATE_DEFINED = PASS`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01 = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02 = PASS`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION = PASS`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE = PASS`
- `DECLARE_GLOBAL_COVERAGE_PASS = BLOCKED`
- `FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST = BLOCKED — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Freeze and version Batch 03 with `BATCH_SIZE = 5` as exactly the first five entries of the governed `eligible_recovery_queue()`, before any Batch 03 historical observation.**

The Batch 03 policy MUST derive membership mechanically from `eligible_recovery_queue()` and MUST NOT use raw `recovery_queue()[:5]`, expected outcome, holiday type, apparent ease, manual substitution, or convenience.

This document does not itself freeze Batch 03.

No `.bi5` acquisition. No real backtest.
