# TRADING BREAKS TARGET-DAY OVERLAP V2 — CAPABILITY ACTIVATION QUALIFICATION

**PASS — `TARGET_DAY_OVERLAP_V2_CAPABILITY_ATOMICALLY_ACTIVATED`**

## Semantic qualification parent

- contract: `TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1`
- qualification run/job: `35064060544` / `104690359352`
- focused suite: `76 passed`
- full governed suite: `472 passed`
- persisted Class-A cases: `14/14 PASS`

## Capability activation

- activation trigger: `ad19da6d071a18162084c16d42ebebc5f6674bb1`
- activation run/job: `35064668675` / `104692209493`
- atomic activation commit: `31b285a30f5648e1f3979ed8847c5a2c8c7a022c`
- pre-mutation suite: `62 passed`
- post-activation current-state suites: `131 passed`, `16 passed / 5 deselected`, `223 passed`
- historical attempts `1..68`: unchanged
- capabilities: V1 + `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- current V2 fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`
- material capability changes: `1`
- executable changed dimension: `protocol_contract`
- added proof capability: `QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION`
- blocker explicitly addressed: `NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

## Persisted-HEAD independent re-break

- verifier trigger: `22c3841efe54e256ed89b75969aba26d4e990bb4`
- verifier run/job: `35064836069` / `104692720276`
- permissions: `contents: read`
- semantic/current-state suite: `131 passed`
- progression suite: `16 passed / 5 historical-state assertions deselected`
- exact persisted state: PASS
- progression regeneration: byte-stable
- final worktree: clean

Persisted progression after V2 activation:

- unresolved: `17`
- attempt ledger: `68`
- material capability changes: `1`
- current capability: V2
- Class-A retry eligible: `14`
- Class-B still ineligible: `3`

No calendar evidence was changed by capability activation. No historical attempt was rewritten. No browser capture occurred. No `.bi5`. No real backtest.
