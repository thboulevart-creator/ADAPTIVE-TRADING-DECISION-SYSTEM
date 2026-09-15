# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — BATCH 12 CAPTURED AND INDEPENDENTLY ADJUDICATED

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branch: `feat/multi-year-dukascopy-acquisition`

## Recovery baseline

- State originally reconstructed against: `6462226b2dae13b20b2dc848b5bae8ce074fc297`.
- Last fully closed functional batch: Batch 11, integration commit `524a9a235e3af5dc59d455138427c68578b37942`.
- Batch 11 persisted-head closure: PASS.
- Claude snapshot: `Carte Architecturale Snapshots Claude/adts-carte-architecturale.md`.
- The Claude snapshot remains an unchanged point-in-time diagnostic artifact, not a normative source.
- Conservative repository cleanup removed only four proven-dead artifacts: the Claude-folder `.gitkeep` and three archived/no-op Batch 07 workflow stubs. Historical proof, reports, tests, policies, backups, and executable verification workflows were retained.

## Authoritative state

### Batch 11

- membership/capture/adjudication: **PASS**.
- atomic integration: **PASS — `524a9a235e3af5dc59d455138427c68578b37942`**.
- persisted-HEAD re-break: **PASS — `BATCH11_PERSISTED_HEAD_REBREAK_CONFIRMS_ATOMIC_INTEGRATION`**.
- closure verdict: **FULLY CLOSED**.

Persisted-head verifier:

- verifier head: `a39cbddd6eb4ab1920df4fd53481eda9e9f93827`
- workflow run/job: `35015337992` / `104537234034`
- governed/adversarial regression: `416 passed in 1.75s`
- progression regeneration: byte-stable
- final worktree: clean
- verifier mutation: NONE

Persisted re-break report:

`reports/data-qualification/historical_trading_breaks_recovery_batch11_persisted_head_rebreak.md`

### Batch 12 — frozen membership

- mechanical freeze baseline: `e6dfa007979975a626a464c8132893f71e5f7f4a`
- freeze qualification head: `e7a6d596921c8ac94cd4306e474a524d846e9abb`
- freeze qualification workflow run/job: `35015819061` / `104538840373`
- mechanical freeze qualification: **PASS**.
- persisted-membership verifier head: `58fe4d542250366dde4e9e085f1040c7602cc79e`
- persisted-membership workflow run/job: `35015879732` / `104539046887`
- persisted-membership re-break: **PASS — `BATCH12_PERSISTED_MEMBERSHIP_REBREAK_CONFIRMS_GOVERNED_FREEZE`**.
- governed/adversarial regression at membership re-break: `417 passed in 1.98s`
- progression regeneration: byte-stable
- final worktree: clean
- verifier permissions: `contents: read`
- verifier mutation: NONE

Frozen membership — immutable after observation:

1. `2025-11-27 — THANKSGIVING_DAY`
2. `2025-11-28 — THANKSGIVING_FRIDAY`
3. `2025-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2025-12-25 — CHRISTMAS_OBSERVED`
5. `2025-12-31 — NEW_YEARS_EVE_CANDIDATE`

Selection contract:

- exact selection rule: `eligible_recovery_queue()[:5]`
- fixed size: `5`
- order: immutable
- membership: immutable
- no target-specific observation preceded freeze
- shifted, permuted, substituted, shortened, extended, duplicated, and reversed variants were rejected

### Batch 12 — browser capture

- execution workflow commit: `2c2fd6e2db2e0ab75a6b978d6cddad679dbda5b8`
- workflow run/job: `35016454761` / `104540999314`
- pre-browser gates: **PASS before Chromium installation/execution**.
- all five frozen targets executed in immutable order.
- capture-stage results: **5 CAPTURED / 0 BLOCKED / 0 FAIL**.
- runtime errors: none.
- runtime report: `reports/data-qualification/historical_trading_breaks_recovery_batch12_runtime.json`
- artifact: `10416410006`
- artifact SHA-256: `6649d976bb9d586cce591cd9b9a9e0e71ed8e5496a1e47e2e52bbdaa2de0297d`
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- capture state mutation outside persisted runtime evidence: NONE.

Captured broker records:

1. `2025-11-27` — record `87363`
2. `2025-11-28` — record `87364`
3. `2025-12-24` — record `91078`
4. `2025-12-25` — overlapping record `91078`, whose break starts on `2025-12-24`
5. `2025-12-31` — record `92491`

### Batch 12 — independent offline adjudication

- adjudicator is offline and evidence-only: no Chromium, no Selenium, no `probe_candidate`, no live scheduler/queue selection.
- authoritative capture provenance is hard-checked before adjudication.
- adversarial adjudication tests: **PASS (`17 passed`)**.
- first adjudication workflow run `35016934580` proved the semantic verdict but failed only at persistence because `git diff --check` rejected an extra blank line at EOF in generated Markdown; no data/semantic gate failed.
- persistence-only formatting defect corrected without changing adjudication logic.
- successful replay workflow run/job: `35017238400` / `104543637831`.
- replay conclusion: **SUCCESS**.
- persisted adjudication commit: `ccff8090e87c74e770e190b9b26e69e3aecc0e23`.
- adjudication report: `reports/data-qualification/historical_trading_breaks_recovery_batch12_adjudication.json`.
- qualification report: `reports/data-qualification/historical_trading_breaks_recovery_batch12_qualification.md`.
- adjudication verdict: **PASS — `BATCH12_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION`**.
- accounting: **4 PASS / 1 BLOCKED / 0 FAIL**.

Exact adjudicated outcomes:

1. `2025-11-27 — THANKSGIVING_DAY` — **PASS** — exact record `87363`.
2. `2025-11-28 — THANKSGIVING_FRIDAY` — **PASS** — exact record `87364`.
3. `2025-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION` — **PASS** — exact record `91078`.
4. `2025-12-25 — CHRISTMAS_OBSERVED` — **BLOCKED — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`** — record `91078` starts on `2025-12-24`; cross-date overlap is deliberately not promoted into exact target-date evidence.
5. `2025-12-31 — NEW_YEARS_EVE_CANDIDATE` — **PASS** — exact record `92491`.

The `2025-12-25` BLOCKED outcome is an intentional fail-closed protection, not a semantic/data FAIL. It must remain unresolved unless a future admissible exact-target-date proof or materially changed capability justifies a retry.

## Deterministic state before Batch 12 atomic integration

The governed calendar/progression state has not yet integrated Batch 12 adjudicated outcomes, so the authoritative pre-integration accounting remains:

- global accounting: `111 candidates / 65 resolved / 46 unresolved / 0 FAIL`
- execution-window accounting: `68 candidates / 42 resolved / 26 unresolved / 0 FAIL`
- raw unresolved: `26`
- attempt ledger: `55`
- same-capability BLOCKED/ineligible: `13`
- eligible unresolved: `13`
- material capability changes: `0`
- execution window frozen: NO
- `.bi5`: FORBIDDEN
- real backtest: NOT AUTHORIZED

Batch 12 atomic integration: **NOT STARTED**.
Batch 12 persisted-HEAD re-break after integration: **NOT STARTED**.
Batch 12 closure verdict: **NOT YET CLOSED**.

## Claude architectural snapshot remediation status

The snapshot identified three immediate-priority concerns. Their current status is:

1. recovery/source-of-truth checkpoint drift: **FIXED**;
2. `RESEARCH → DECISION` provenance/forgeability weakness: **STILL PENDING**;
3. CI coverage too tightly coupled to specific branch names: **STILL PENDING**.

Those two remaining architecture remediations are not mixed into the Trading Breaks acquisition workstream unless they become a direct prerequisite. They remain mandatory before relying on the affected research/decision path as a final trusted system boundary.

## Autonomous continuation contract

Continue batches sequentially without requesting confirmation. Preserve, for each batch:

`persisted-head PASS → mechanical freeze from current eligible_recovery_queue()[:5] → adversarial membership qualification → browser capture with pre-browser gates → independent offline adjudication → atomic integration → independent persisted-head re-break`

Stop only on a true semantic/data FAIL, a required capability change, an unresolved contradiction needing human judgment, or exhaustion of the current execution-eligible queue.

A captured broker record is not automatically executable evidence. Cross-date overlaps must remain fail-closed unless the exact target-date contract is independently satisfied.

## Exactly one next governed action

**Atomically integrate Batch 12 exactly as independently adjudicated: persist calendar evidence only for the four PASS targets, record all five Batch 12 attempts including the `2025-12-25` BLOCKED outcome with exact capture provenance, leave `2025-12-25` unresolved, regenerate deterministic progression, run the governed/adversarial regression, and commit only after every integration gate PASS.**

After atomic integration, Batch 12 must still survive an independent read-only persisted-HEAD re-break before it can be declared fully closed or before Batch 13 membership is frozen.

No `.bi5`. No real backtest.
