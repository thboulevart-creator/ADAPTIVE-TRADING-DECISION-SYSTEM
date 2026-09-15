# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — BATCH 13 FULLY CLOSED / TERMINAL ELIGIBLE REMAINDER = 3

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Source-of-truth rule

GitHub code, executable tests, reports and qualified workflow evidence are authoritative. `Carte Architecturale Snapshots Claude/adts-carte-architecturale.md` remains a point-in-time diagnostic snapshot only.

The three immediate Claude priorities previously identified are closed at their executable loci:

1. recovery/checkpoint drift: **FIXED**;
2. `RESEARCH → DECISION` provenance/forgeability: **FIXED AND INDEPENDENTLY RE-BROKEN** on `feat/decision-producer-contract`;
3. durable boundary CI branch-name coupling: **FIXED AND INDEPENDENTLY RE-BROKEN** on `feat/decision-producer-contract`.

No DECISION code was copied artificially into this acquisition branch.

## Batch 12

Batch 12 remains **FULLY CLOSED**. Its persisted integration and independent read-only re-break remain historical proof and are not modified by this checkpoint.

## Batch 13 — FULLY CLOSED

Frozen membership remained immutable throughout freeze, capture, adjudication, integration and persisted-HEAD re-break:

1. `2026-01-01 — NEW_YEARS_OBSERVED`
2. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
3. `2026-02-16 — PRESIDENTS_DAY`
4. `2026-04-03 — GOOD_FRIDAY`
5. `2026-05-25 — MEMORIAL_DAY`

### Frozen-membership proof

- freeze baseline: `fa09da05bb80ba0a94cc4a58864f2ba52a6437ec`
- freeze qualification head: `882f89e0170fd1d039587c41cb598ea4e8f43ce0`
- freeze run/job: `35018781921` / `104548825643`
- persisted-membership verifier head: `b6fa2006938d47c0f4f9f91c9ab7bd152fe42052`
- persisted-membership run/job: `35018850696` / `104549069311`
- no target observation preceded membership freeze and re-break.

### Browser capture

- execution commit: `a974275d06ff45b0a78ad6558a6480e25cfe0f73`
- workflow run/job: `35020650564` / `104555157264`
- artifact: `10416898441`
- artifact SHA-256: `59c93ab69bb1484fa0578bb8704aea76f15d67765e9a27ec0416c615d83faec8`
- capture accounting: **5 CAPTURED / 0 BLOCKED / 0 FAIL**
- pre-browser governed/adversarial regression: `434 passed`
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- compact runtime persistence commit: `1c676343031e14b5b1867ff63ed313276484c7ef`

### Independent offline adjudication

- workflow run/job: `35022492939` / `104561408795`
- persisted adjudication commit: `86a930200feca8abbf3ff68cbdd95439e8944f3e`
- adversarial adjudication regression: `16 passed`
- verdict: **PASS — 3 PASS / 2 BLOCKED / 0 FAIL**

PASS:

- `2026-01-19` — broker record `93608`
- `2026-02-16` — broker record `94467`
- `2026-05-25` — broker record `100253`

BLOCKED and not promotable into exact target-date evidence:

- `2026-01-01` — overlap record `92491` — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`
- `2026-04-03` — overlap record `98541` (`Easter`) — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

No cross-date record was promoted.

### Atomic integration

- successful integration commit: `52b1978feb0018c1eafc80108e4b411edf0ec982`
- calendar: only the three PASS dates persisted
- ledger: all five Batch 13 attempts persisted
- attempt sequences: `61..65`
- outcomes: `BLOCKED, PASS, PASS, BLOCKED, PASS`
- all five attempts retain exact capture provenance
- both BLOCKED dates remain outside `SPECIAL_SESSION_EVIDENCE`.

### Independent persisted-HEAD re-break

- verifier head: `bb8f6dbf7781accf7051c8e6bc9213757da1d6da`
- workflow run/job: `35023156320` / `104563657205`
- permissions: `contents: read`
- integration ancestry + verifier-only delta: PASS
- governed/adversarial regression: **447 passed in 2.39s**
- frozen Batch 13 membership unchanged: PASS
- calendar / ledger / provenance exactness: PASS
- progression regeneration: byte-stable
- final worktree: clean
- verifier mutation: NONE

Persistent report:

`reports/data-qualification/historical_trading_breaks_recovery_batch13_persisted_head_rebreak.md`

Batch 13 closure verdict: **FULLY CLOSED**.

## Deterministic progression after Batch 13

- global calendar: `111 candidates / 72 resolved / 39 unresolved / 0 FAIL`
- execution-window candidate (`2021-08-14` → `2026-08-14`): `68 candidates / 49 resolved / 19 unresolved / 0 FAIL`
- recovery queue: `19`
- attempt ledger: `65`
- same-capability BLOCKED/ineligible: `16`
- eligible unresolved under current capability: `3`
- material capability changes: `0`
- execution window frozen: **NO**
- `.bi5`: **FORBIDDEN**
- real backtest: **NOT AUTHORIZED**

Current eligible queue, in deterministic chronological order:

1. `2026-06-19 — JUNETEENTH_OBSERVED`
2. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

## Terminal remainder boundary

The original first-batch policy fixed Batch 01 at five candidates. The recovery protocol requires every later batch size to be fixed and versioned before outcomes are observed, and forbids resizing to avoid difficult dates.

After Batch 13 there are only three execution-eligible candidates under the unchanged capability. Therefore:

- a synthetic five-item Batch 14 is forbidden;
- ineligible/BLOCKED dates must not be padded into the batch;
- the three current eligible dates must not be manually reduced, reordered or substituted;
- before any new browser observation, a separate terminal-remainder rule must define and adversarially qualify the only legitimate terminal batch: the complete current eligible queue of size three.

This is not a capability change. The 16 same-capability BLOCKED dates remain unresolved/ineligible and visible.

## Exactly one next governed action

**Formalize and adversarially qualify a Batch 14 terminal-remainder policy that freezes the complete current eligible queue of exactly three dates, proves that no eligible candidate is omitted and no ineligible candidate is inserted, and performs no browser observation. Only after that policy and persisted membership independently PASS may Batch 14 capture begin.**

No `.bi5`. No real backtest.
