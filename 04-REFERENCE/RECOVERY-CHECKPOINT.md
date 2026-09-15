# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — BATCH 12 CLOSED / BATCH 13 MEMBERSHIP SECURED

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

## Claude architectural snapshot remediation status

Three immediate-priority concerns were identified:

1. recovery/source-of-truth checkpoint drift: **FIXED**;
2. `RESEARCH → DECISION` provenance/forgeability weakness: **NEXT — PENDING**;
3. durable CI coverage too tightly coupled to specific branch names: **PENDING AFTER ITEM 2**.

The Trading Breaks workstream is now at a safe deterministic boundary: Batch 12 is fully closed and Batch 13 membership is frozen and independently re-broken before observation. Browser capture is deliberately paused while the two remaining Claude priority defects are addressed.

## Governing continuation rule

Do not start Batch 13 browser observation while the architecture-remediation block is active. Batch 13 membership is already immutable and may be resumed later from this checkpoint without reselection.

## Exactly one next governed action

**Audit and remediate the current executable `RESEARCH → DECISION` boundary against the actual repository state. Identify the smallest forgeability/provenance weakness still executable now, fix only that boundary, then adversarially break fallback, silent reconstruction, `context_id`-only acceptance, mismatched/stale research identity and any equivalent bypass. Do not build new RESEARCH architecture.**

Only after this boundary reaches a defensible PASS should the second Claude priority — durable CI branch-coupling coverage — be remediated.

No `.bi5`. No real backtest.
