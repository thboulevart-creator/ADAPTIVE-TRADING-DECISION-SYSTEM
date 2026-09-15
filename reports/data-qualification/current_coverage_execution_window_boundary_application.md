# CURRENT COVERAGE / EXECUTION-WINDOW BOUNDARY APPLICATION

Contract: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

## Current governed state after Batch 08 atomic integration + persisted-HEAD re-break PASS

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
- First current eligible unresolved entry: `2024-09-02 — LABOR_DAY`
- Current semantic capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- Capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- Batch 08: **FROZEN → EXECUTED → INDEPENDENTLY ADJUDICATED → ATOMICALLY INTEGRATED → PERSISTED-HEAD RE-BREAK PASS**
- Batch 09 membership: **NOT FROZEN**
- Massive native `.bi5` acquisition: **FORBIDDEN**
- Real backtest: **NOT AUTHORIZED**

The execution-window candidate remains exactly `2021-08-14 → 2026-08-14`. It MUST NOT be moved, shortened or lengthened to avoid unresolved dates.

## Batch 08 frozen membership

1. `2024-03-29 — GOOD_FRIDAY`
2. `2024-05-27 — MEMORIAL_DAY`
3. `2024-06-19 — JUNETEENTH_OBSERVED`
4. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
5. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`

Historical membership remains immutable. It MUST NOT be reconstructed from the current live queue.

## Batch 08 execution + independent adjudication — PASS

Execution provenance:

- run: `34984538763`
- job: `104433139005`
- probe commit: `5cc4834af2c75de99f6e3427f31ab07b38b42611`
- runtime persistence commit: `6136243c2fbe906a242546d3014a6ee78d30beeb`
- artifact: `10402433119`
- artifact SHA-256: `644e6d6776792dac03e7cb87a3bd63af0be603c6efe951f44c8911ecd9defadd`
- pre-Chromium governed regression: `307 passed in 1.47s`
- exact frozen identity gate: PASS
- no-live-membership-recalculation gate: PASS

Independent adjudication:

- successful run/job: `34985341285` / `104435886156`
- evidence commit: `c2c0ae35e61b5054c23ebbdba8f27d56c6c8380c`
- adversarial suite: `117 passed in 0.40s`
- final accounting: **4 PASS / 1 BLOCKED / 0 FAIL**

Date-level outcome:

- `2024-03-29 — GOOD_FRIDAY` — **BLOCKED** — no exact-target-date positive record admissible; overlap record `66555` starts `2024-03-28T20:14:59Z` and is never promoted.
- `2024-05-27 — MEMORIAL_DAY` — **PASS** — record `68242`; fully closed whole UTC hours `17..21`.
- `2024-06-19 — JUNETEENTH_OBSERVED` — **PASS** — record `69037`; fully closed whole UTC hours `17..21`.
- `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION` — **PASS** — record `69819`; start `17:14:59Z`, therefore only whole UTC hours `18..21` are projected closed.
- `2024-07-04 — INDEPENDENCE_DAY_OBSERVED` — **PASS** — record `69820`; fully closed whole UTC hours `17..21`.

The Good Friday cross-date interval remains blocker evidence only. It is absent from both `SPECIAL_SESSION_EVIDENCE` and `NO_SPECIAL_CHANGE_EVIDENCE`.

### Adjudication harness correction

The first adjudication run `34985087276` passed all substantive checks but failed only on Markdown EOF whitespace during persistence. No governed state was mutated. After a minimal persistence-only correction, the full adjudication chain was rerun and passed.

## Batch 08 atomic integration — PASS

Authoritative atomic integration commit:

`aa85a2ade1fe9d9b1ade78f77b9b56c5310a6e74`

Integration execution:

- run: `34987791998`
- job: `104444271495`
- trigger commit: `8aef1091193ae117d404f58573370ea9092b6c8c`
- pre-mutation integration contract: `79 passed in 0.33s`
- post-mutation governed regression: `335 passed in 1.62s`
- exact post-state assertion: PASS
- executable integration AST contains no browser/capture/live-membership selection path: PASS

Atomic mutations:

- only the four adjudicated PASS dates were added to executable calendar evidence;
- all five factual Batch 08 attempts were appended as sequences `36..40`;
- `2024-03-29` stayed unresolved and became `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`;
- no negative evidence was fabricated;
- progression was regenerated deterministically;
- no material semantic capability change was registered.

Post-integration persisted state:

- global: `111 / 53 resolved / 58 unresolved / 0 FAIL`
- execution window: `68 / 30 resolved / 38 unresolved / 0 FAIL`
- ledger: `40`
- material capability changes: `0`
- same-capability BLOCKED/ineligible: `10`
- eligible unresolved: `28`
- first current eligible unresolved: `2024-09-02 — LABOR_DAY`

Integration qualification:

`reports/data-qualification/historical_trading_breaks_recovery_batch08_integration_qualification.md`

### Integration pre-gate harness correction

Initial integration run `34987503866` / job `104443288047` stopped **before mutation** with `78 PASS / 1 FAIL`. The only failure was a self-referential source-text scanner detecting the word `playwright` inside a string literal for a test the integrator would later write. The guard was minimally changed to inspect executable AST imports/calls instead. No calendar, ledger or progression mutation occurred in the failed run. The complete integration chain was then rerun and passed.

## Batch 08 independent persisted-HEAD re-break — PASS

Independent verifier final trigger commit:

`d996d1e3573bfc36437710cc95510ca73b519650`

Verifier execution:

- run: `34988096558`
- job: `104445314023`
- permissions: `contents: read`
- exact detached persisted HEAD checkout: PASS
- integration commit ancestry: PASS
- governed-state immutability since `aa85a2a...`: PASS
- full regression: `335 passed in 1.47s`
- exact persisted accounting: PASS
- deterministic progression regeneration + tracked `git diff --exit-code`: PASS
- final read-only clean worktree assertion: PASS

The first verifier run `34987958976` / job `104444833841` passed every substantive proof but its final worktree-clean check rejected Python-created untracked `tests/__pycache__/` and `tools/__pycache__/`. Tracked `git diff --exit-code` had already passed. The verifier harness was minimally corrected with `PYTHONDONTWRITEBYTECODE=1`, then the complete verifier was rerun and passed. No governed state changed in either verifier run.

## Workflow closure

Completed Batch 08 workflows are archived to `workflow_dispatch` only. In particular:

- membership policy workflow: archived;
- browser execution workflow: archived;
- independent adjudication workflow: archived;
- atomic integration workflow: archived at commit `f4e86e45546e2fc32ff1dae8124115250bf59247`;
- persisted-HEAD verifier: archived at commit `550420e66a1d687a37ce645764ff0edb0c7c1b64`.

Normal pushes cannot silently repeat completed Batch 08 execution, adjudication, integration or persisted-HEAD verification.

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
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_EXECUTION_ADJUDICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_ATOMIC_INTEGRATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_PERSISTED_HEAD_REBREAK`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

Still BLOCKED downstream:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## Exactly one next governed action

**Freeze and version Batch 09 from the persisted post-Batch08 `eligible_recovery_queue()`, then adversarially break its membership before any browser/Chromium observation.**

Do not manually choose Batch 09 members. Recompute the governed eligible queue from the persisted current GitHub state, apply the governed fixed-size prefix rule, and freeze/version membership before observation. The currently proven first eligible entry is `2024-09-02 — LABOR_DAY`, but the remaining membership MUST be derived from GitHub rather than inferred from conversation.

No `.bi5`. No real backtest.
