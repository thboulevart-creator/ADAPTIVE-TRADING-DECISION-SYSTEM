# CR2 — Regime-Candidate Synthesis — local execution handoff

Date: 2026-09-26  
Branch of authority: `integration/system-v1`

## Qualified identities

CR2 helper:
- Git blob `34c702e926b3baec90c57b8366177c2db1eca074`
- SHA-256 `cdea6b317400fbbd32208e05343a6a2c1c78c3cfbd04bcf0271fc7e60dfcf757`

CR1 helper dependency:
- Git blob `bb5cd4acd1b48141019c0ec3796ea61627dc0dbf`

Context:
- Git blob `4f927acb938f4d91b52fa07649b75b5f450d1d3f`
- SHA-256 `3c507795c996e571152d4877a594abb889e4a8a017130332a166d5dda84af866`

CR1 exact evidence:
- Git blob `cd40bf975613d1fa0e6d7277c2850ec87104727e`
- SHA-256 `c7aacf73c175c6af49a4866ad62f1d65c0b46b05fa6cd0dd0def4eb5ce87ba3f`

CR2 registry:
- Git blob `c6e19dc67c521d8f79814473ffa19ae427398e4f`

AP0 manifest:
- SHA-256 `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`

## Execution pattern

Preserve the user's local branch unchanged.

For one authorized corpus attempt:
1. fetch `origin/integration/system-v1`;
2. require exact authorized remote HEAD;
3. verify AP0 manifest SHA;
4. create a brand-new temp stage;
5. materialize CR2 helper + CR1 helper + Context + CR1 evidence + CR2 registry from raw Git blobs;
6. verify all Git blob identities and registered SHA-256 values;
7. py_compile CR2 helper;
8. execute once to a unique output;
9. preserve any BLOCKED output;
10. if CR2_COMPLETE, copy exact JSON to handoff directory and return terminal + JSON.

No strategy, PnL, direction target, semantic regime naming, winner selection, optimization or MT5.
