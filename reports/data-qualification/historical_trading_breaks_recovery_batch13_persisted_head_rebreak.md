# HISTORICAL TRADING BREAKS RECOVERY — BATCH 13 PERSISTED-HEAD RE-BREAK

**PASS — `BATCH13_PERSISTED_HEAD_REBREAK_CONFIRMS_ATOMIC_INTEGRATION`**

## Functional state under test

- integration commit: `52b1978feb0018c1eafc80108e4b411edf0ec982`
- integration content: calendar + attempt ledger + deterministic progression + migrated state assertions
- frozen Batch 13 membership remained unchanged:
  1. `2026-01-01 — NEW_YEARS_OBSERVED`
  2. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
  3. `2026-02-16 — PRESIDENTS_DAY`
  4. `2026-04-03 — GOOD_FRIDAY`
  5. `2026-05-25 — MEMORIAL_DAY`

## Independent verifier

- verifier head: `bb8f6dbf7781accf7051c8e6bc9213757da1d6da`
- workflow run: `35023156320`
- job: `104563657205`
- permissions: `contents: read`
- delta from integration commit: only `.github/workflows/trading-breaks-recovery-batch13-persisted-head.yml`
- governed/adversarial regression: `447 passed in 2.39s`
- progression regeneration: byte-stable
- final worktree: clean
- verifier mutation: NONE

## Persisted Batch 13 evidence confirmed

Capture provenance retained for all five attempts:

- workflow run: `35020650564`
- job: `104555157264`
- probe commit: `a974275d06ff45b0a78ad6558a6480e25cfe0f73`
- artifact: `10416898441`
- artifact SHA-256: `59c93ab69bb1484fa0578bb8704aea76f15d67765e9a27ec0416c615d83faec8`

Independent adjudication persisted at:

- commit: `86a930200feca8abbf3ff68cbdd95439e8944f3e`
- workflow run: `35022492939`
- job: `104561408795`
- verdict: `PASS — 3 PASS / 2 BLOCKED / 0 FAIL`

Integrated PASS dates:

- `2026-01-19` — broker record `93608`
- `2026-02-16` — broker record `94467`
- `2026-05-25` — broker record `100253`

Persisted unresolved BLOCKED dates:

- `2026-01-01` — overlap record `92491` — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`
- `2026-04-03` — overlap record `98541` — `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

Neither BLOCKED date was inserted into executable calendar evidence.

## Deterministic post-Batch13 state

- global calendar: `111 candidates / 72 resolved / 39 unresolved / 0 FAIL`
- execution-window candidate: `68 candidates / 49 resolved / 19 unresolved / 0 FAIL`
- attempt ledger: `65`
- Batch 13 attempt sequences: `61..65`
- same-capability BLOCKED/ineligible: `16`
- current eligible unresolved: `3`
- material capability changes: `0`

Current eligible queue under `TRADING_BREAKS_PRIMARY_WIDGET_V1`:

1. `2026-06-19 — JUNETEENTH_OBSERVED`
2. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

## Boundary

Batch 13 is **FULLY CLOSED**.

No `.bi5` acquisition is authorized. No real backtest is authorized. The next recovery action must not manufacture a five-item batch by adding ineligible dates. The terminal eligible remainder must be governed and frozen before any new observation.
