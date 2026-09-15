# HISTORICAL TRADING BREAKS RECOVERY — BATCH 13 POLICY

**FROZEN mechanically from `eligible_recovery_queue()[:5]` at baseline HEAD `fa09da05bb80ba0a94cc4a58864f2ba52a6437ec`.**

Frozen membership:

1. `2026-01-01 — NEW_YEARS_OBSERVED`
2. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
3. `2026-02-16 — PRESIDENTS_DAY`
4. `2026-04-03 — GOOD_FRIDAY`
5. `2026-05-25 — MEMORIAL_DAY`

Selection contract:

- fixed size: `5`
- selection rule: first five entries of the governed eligible recovery queue at freeze time
- order: immutable
- membership: immutable before observation
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- all five targets must be proven `INITIAL_ATTEMPT`, unattempted, unresolved, and execution-eligible at freeze

No observation, browser capture, live probing, or target-specific data inspection preceded this freeze.

Before any Batch 13 observation/capture, the persisted membership must independently survive adversarial qualification against the governed progression state.

No `.bi5`. No real backtest.
