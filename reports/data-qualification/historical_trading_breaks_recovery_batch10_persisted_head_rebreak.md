# HISTORICAL TRADING BREAKS RECOVERY — BATCH 10 PERSISTED-HEAD RE-BREAK

**PASS — `BATCH10_PERSISTED_HEAD_REBREAK_CONFIRMS_ATOMIC_INTEGRATION`**

- verifier trigger: `167c667db6279924aeb7e68101780814fdbf041e`
- workflow run/job: `35008589674` / `104514508763`
- permissions: `contents: read`
- full governed/adversarial regression: `458 passed in 1.47s`
- exact Batch 10 integration tests: `6 passed`
- atomic integration ancestor: `6d2f60525fed9a56fd4ebab587ce7ba699cedbda`
- global accounting: `111 / 60 / 51 / 0 FAIL`
- execution window: `68 / 37 / 31 / 0 FAIL`
- raw unresolved: `31`
- ledger: `50`
- same-capability BLOCKED/ineligible: `13`
- eligible unresolved: `18`
- capability changes: `0`
- attempts `46..50`: exact frozen order and provenance PASS
- `2025-01-01` and `2025-04-18`: unresolved, BLOCKED, ineligible under same capability
- progression regeneration: byte-stable
- final worktree: clean
- verifier mutation: NONE

Batch 11 was not frozen during this verifier.

No `.bi5`. No real backtest.
