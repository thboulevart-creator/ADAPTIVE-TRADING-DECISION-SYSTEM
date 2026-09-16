# HISTORICAL TRADING BREAKS RECOVERY — BATCH 14 PERSISTED-HEAD RE-BREAK

**PASS — `BATCH14_PERSISTED_HEAD_REBREAK_CONFIRMS_TERMINAL_INTEGRATION`**

- atomic integration commit: `075b33b79c8de3b2f4f6201a7541c6555585a5e4`
- pre-verifier checkpoint: `fb79f8bbe2478a640030cd8fce98a9a1b073b396`
- verifier trigger: `ceec67b5951c52564c3ce610c8347d0f46a721e4`
- workflow run/job: `35063579495` / `104688908778`
- verifier permissions: `contents: read`
- governed/adversarial regression: `461 passed in 2.01s`
- progression regeneration: byte-stable
- final worktree: clean
- verifier state mutation: NONE

## Persisted terminal Batch 14 truth

Frozen terminal membership remains exactly:

1. `2026-06-19 — JUNETEENTH_OBSERVED`
2. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

Calendar evidence remains exactly:

- `2026-06-19` — PASS — broker record `101094` — fully closed UTC hours `[17,18,19,20,21,22,23]`.
- `2026-07-02` — unresolved/BLOCKED — absent from both resolving evidence surfaces.
- `2026-07-03` — PASS — broker record `101959` — fully closed UTC hours `[17,18,19,20,21,22,23]`.

Batch 14 attempt ledger remains sequences `66..68` in frozen order with outcomes `PASS / BLOCKED / PASS` and exact execution provenance from run/job `35023845609 / 104565948108`, artifact `10418961548`, artifact SHA-256 `00dd2044a76d926417779d22c7ce08b67318a9d00933b9cac1bc980f2a7c9910`, probe commit `4194108c6c9e2c0308209b31cfa64ba8fb3b9f2b`.

## Persisted post-state

- global calendar: `111 / 74 resolved / 37 unresolved / 0 FAIL`
- execution-window candidate: `68 / 51 resolved / 17 unresolved / 0 FAIL`
- raw unresolved queue: `17`
- attempt ledger: `68`
- same-capability BLOCKED/ineligible: `17`
- execution-eligible unresolved under `TRADING_BREAKS_PRIMARY_WIDGET_V1`: `0`
- material capability changes: `0`

`2026-07-02` remains `UNRESOLVED`, latest outcome `BLOCKED`, eligibility `false`, reason `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`.

The current capability is exhausted. A Batch 15 under the same capability is forbidden.

No `.bi5`. No real backtest.
