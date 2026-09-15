# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — BATCH 12 CLOSED / BATCH 13 MEMBERSHIP SECURED / CLAUDE PRIORITIES CLOSED

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branch: `feat/multi-year-dukascopy-acquisition`

## Recovery baseline

- State originally reconstructed against: `6462226b2dae13b20b2dc848b5bae8ce074fc297`.
- Previous fully closed batch: Batch 11, integration commit `524a9a235e3af5dc59d455138427c68578b37942`.
- Claude snapshot: `Carte Architecturale Snapshots Claude/adts-carte-architecturale.md`.
- The Claude snapshot remains a point-in-time diagnostic artifact, not a normative source.
- Conservative cleanup removed only four proven-dead artifacts; historical proof, reports, tests, policies, backups and executable verification workflows were retained.

## Batch 12 — FULLY CLOSED

Frozen membership remained immutable throughout capture, adjudication and integration:

1. `2025-11-27 — THANKSGIVING_DAY`
2. `2025-11-28 — THANKSGIVING_FRIDAY`
3. `2025-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2025-12-25 — CHRISTMAS_OBSERVED`
5. `2025-12-31 — NEW_YEARS_EVE_CANDIDATE`

Capture provenance:

- execution commit: `2c2fd6e2db2e0ab75a6b978d6cddad679dbda5b8`
- run/job: `35016454761` / `104540999314`
- artifact: `10416410006`
- artifact SHA-256: `6649d976bb9d586cce591cd9b9a9e0e71ed8e5496a1e47e2e52bbdaa2de0297d`
- capture accounting: `5 CAPTURED / 0 BLOCKED / 0 FAIL`
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

Independent offline adjudication:

- persisted commit: `ccff8090e87c74e770e190b9b26e69e3aecc0e23`
- run/job: `35017238400` / `104543637831`
- verdict: **PASS — 4 PASS / 1 BLOCKED / 0 FAIL**
- `2025-12-25` remained `BLOCKED — NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`; cross-date record `91078` was not promoted into exact target-date evidence.

Atomic integration:

- successful run/job: `35018379789` / `104547480092`
- governed/adversarial regression: `432 passed in 1.84s`
- integration commit: `f16c952ce0695421808b19afbcb6acee38991437`
- calendar: only four PASS targets persisted
- ledger: all five attempts persisted, sequences `56..60`, outcomes `PASS, PASS, PASS, BLOCKED, PASS`
- all five attempts preserve exact capture provenance
- `2025-12-25` is not present in `SPECIAL_SESSION_EVIDENCE` and remains unresolved/ineligible under unchanged capability.

Independent persisted-HEAD re-break:

- verifier head: `9dcfda6941438186d0735a0561029ea3858bdac7`
- run/job: `35018452145` / `104547721021`
- permissions: `contents: read`
- regression: `432 passed in 2.10s`
- calendar/ledger/provenance: PASS
- frozen membership: unchanged
- progression regeneration: byte-stable
- worktree: clean
- verifier mutation: NONE

Batch 12 closure verdict: **FULLY CLOSED**.

## Deterministic progression after Batch 12

- global accounting: `111 candidates / 69 resolved / 42 unresolved / 0 FAIL`
- execution-window accounting: `68 candidates / 46 resolved / 22 unresolved / 0 FAIL`
- recovery queue: `22`
- attempt ledger: `60`
- same-capability BLOCKED/ineligible: `14`
- eligible unresolved: `8`
- material capability changes: `0`
- execution window frozen: NO
- `.bi5`: FORBIDDEN
- real backtest: NOT AUTHORIZED

## Batch 13 — membership mechanically frozen and independently secured

Freeze baseline was the post-Batch12 closure checkpoint commit:

- baseline: `fa09da05bb80ba0a94cc4a58864f2ba52a6437ec`
- selection contract: exact `eligible_recovery_queue()[:5]`
- fixed size: `5`
- membership/order: immutable before observation

Mechanically frozen membership:

1. `2026-01-01 — NEW_YEARS_OBSERVED`
2. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
3. `2026-02-16 — PRESIDENTS_DAY`
4. `2026-04-03 — GOOD_FRIDAY`
5. `2026-05-25 — MEMORIAL_DAY`

Freeze qualification:

- qualification head: `882f89e0170fd1d039587c41cb598ea4e8f43ce0`
- workflow run/job: `35018781921` / `104548825643`
- permissions: `contents: read`
- regression: **433 passed in 2.25s**
- frozen set proved exactly equal to `derive()` and `eligible_recovery_queue()[:5]`
- all five proved unresolved, unattempted, `INITIAL_ATTEMPT`, execution-eligible
- adversarial shifted/permuted/substituted/shortened/extended/duplicated/reversed variants rejected
- progression regeneration: byte-stable
- worktree: clean
- browser observation: NONE

Independent persisted-membership re-break:

- verifier head: `b6fa2006938d47c0f4f9f91c9ab7bd152fe42052`
- workflow run/job: `35018850696` / `104549069311`
- permissions: `contents: read`
- verifier-only delta from qualification head: PASS
- regression: **433 passed in 2.03s**
- exact persisted membership equals governed prefix: PASS
- adversarial variants rejected again: PASS
- progression regeneration: byte-stable
- worktree: clean
- verifier mutation: NONE

Batch 13 browser capture: **NOT STARTED**.
No target-specific observation occurred before or during the freeze/qualification/re-break sequence.

## Claude architectural snapshot — immediate-priority remediation status

All three immediate priorities identified from the Claude snapshot are now closed at their actual executable loci.

### 1. Recovery/source-of-truth checkpoint drift — FIXED

- recovery state is explicitly checkpointed on the active acquisition branch;
- Batch 12 closure, Batch 13 frozen membership and continuation boundaries are persisted here;
- Claude snapshot remains diagnostic only and cannot override repository evidence.

### 2. `RESEARCH → DECISION` provenance / forgeability — FIXED ON EXECUTABLE BRANCH

The acquisition branch does not contain an executable DECISION component, so this defect was correctly remediated on the existing branch where the boundary actually exists:

`feat/decision-producer-contract`

Pre-remediation state:

- previous HEAD: `6eb2a45c2ca66ea75af0f87abe9248e985341448`
- workflow run/job: `34745928161` / `103693748664`
- status: **FAIL**
- root weakness: trust was carried by `_factory_validated` on `ResearchRunEvidence` itself; reconstruction/mutation semantics were not bound to an external attestation of the original object identity/content.

Remediation:

- self-declared `_factory_validated` trust removed from the evidence contract;
- factory attestation is now process-local and external to the evidence object;
- attestation binds the exact object identity plus a fingerprint of all seven upstream identity fields: `provenance_id`, `research_run_id`, `code_version`, `configuration_version`, `dataset_id`, `dataset_version`, `context_id`;
- exact reconstruction, `copy.copy`, `copy.deepcopy`, legacy marker injection, `object.__setattr__`, direct `__dict__` mutation and altered/stale identity all invalidate admissibility;
- both `produce_decision()` and `ResearchFindings.from_research_run_evidence()` require the bound attestation;
- no new RESEARCH architecture or persistent registry was introduced.

Primary post-remediation boundary run:

- remediated functional head: `3406f1a32c5c9609e7deda6bf6be21350d64f116`
- workflow run: `35019496050`
- complete executable boundary chain: **PASS**.

Independent persisted-HEAD adversarial re-break:

- first verifier run/job: `35019564948` / `104551584450`
- verdict: **PASS**
- reconstruction, legacy self-marker, shallow/deep copy, every identity-field mutation, direct dictionary mutation and forged-evidence Findings seeding rejected;
- verifier permissions: `contents: read`;
- worktree: clean;
- verifier mutation: NONE.

Final cross-remediation verifier:

- final verifier head: `c0116d195063c464d602fb699654ac61adc7290c`
- workflow run/job: `35019876682` / `104552615501`
- conclusion: **SUCCESS**.

This remediation intentionally remains on `feat/decision-producer-contract`; it is not copied into the Dukascopy acquisition branch, because that branch has no executable DECISION component to patch.

### 3. Durable CI branch-name coupling — FIXED ON EXECUTABLE BOUNDARY BRANCH

The four durable boundary workflows on `feat/decision-producer-contract` were previously tied to historical feature-branch names. They are now branch-neutral and path-scoped:

- `.github/workflows/data-to-context.yml`
- `.github/workflows/context-to-research-boundary.yml`
- `.github/workflows/research-findings-contract.yml`
- `.github/workflows/research-to-decision-boundary.yml`

Current durable CI contract:

- no `branches:` restriction;
- no `feat/...` branch identity embedded in these four workflows;
- `push` coverage on any branch when relevant paths change;
- `pull_request` coverage when relevant paths change;
- `workflow_dispatch` retained;
- `permissions: contents: read`;
- path-scoped to avoid unrelated/document-only executions;
- pytest pinned to `8.4.2` in the remediated workflows.

Individual workflow proof after conversion:

- DATA → CONTEXT: run `35019658706` — **SUCCESS**;
- CONTEXT → RESEARCH: run `35019671227` — **SUCCESS**;
- Research Findings Contract: run `35019685715` — **SUCCESS**;
- RESEARCH → DECISION plus durable CI anti-regression gate: run/job `35019747006` / `104552186983` — **SUCCESS**.

A durable anti-regression test now fails if any of these four workflows reintroduces a branch-name restriction or `feat/...` coupling.

Independent final read-only re-break:

- verifier head: `c0116d195063c464d602fb699654ac61adc7290c`
- run/job: `35019876682` / `104552615501`
- exact final-remediation ancestry and verifier-only delta: PASS;
- complete executable boundary + CI contracts: PASS;
- provenance/forgeability attack matrix: PASS;
- branch-neutral/path-scoped/PR-covered/read-only workflow assertions: PASS;
- final worktree: clean;
- verifier mutation: NONE.

Claude immediate-priority status is therefore:

1. source-of-truth checkpoint drift: **FIXED**;
2. RESEARCH → DECISION provenance/forgeability: **FIXED AND INDEPENDENTLY RE-BROKEN**;
3. durable CI branch-name coupling: **FIXED AND INDEPENDENTLY RE-BROKEN**.

## Governing continuation rule

The architecture-remediation pause is lifted. Resume Trading Breaks from the already frozen Batch 13 membership. Do not recompute, reselect, reorder, substitute or otherwise mutate its five targets after the now-completed architecture work.

## Exactly one next governed action

**Execute Batch 13 browser capture using only the five already frozen targets, under the existing pre-browser gates and unchanged capability fingerprint, with no reselection or membership mutation. Stop before independent adjudication unless the capture stage itself is fully PASS and its artifact/provenance are available.**

No `.bi5`. No real backtest.
