# HISTORICAL TRADING BREAKS RECOVERY — BATCH 12 POLICY

**FROZEN mechanically from `eligible_recovery_queue()[:5]` at baseline HEAD `e6dfa007979975a626a464c8132893f71e5f7f4a`.**

Frozen membership:

1. `2025-11-27 — THANKSGIVING_DAY`
2. `2025-11-28 — THANKSGIVING_FRIDAY`
3. `2025-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
4. `2025-12-25 — CHRISTMAS_OBSERVED`
5. `2025-12-31 — NEW_YEARS_EVE_CANDIDATE`

Selection contract:

- fixed size: `5`
- selection rule: first five entries of the governed eligible recovery queue at freeze time
- order: immutable
- membership: immutable before observation
- capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`
- all five targets were `INITIAL_ATTEMPT`, unattempted, unresolved, and execution-eligible at freeze

No observation, browser capture, live probing, or target-specific data inspection preceded this freeze.

Before any Batch 12 observation/capture, the persisted membership must independently survive adversarial qualification against the governed progression state.

No `.bi5`. No real backtest.
