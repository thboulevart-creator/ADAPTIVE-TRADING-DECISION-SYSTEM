# CR1 — Context Informativeness — local execution handoff

Date : 2026-09-26  
Branch of authority : `integration/system-v1`

## Qualified production helper

- Git blob: `484f74d0c05eabd3ecc0d9b35fbbafdf120f408a`
- SHA-256: `2ec7ae1b2db5f0afe7b9ff4405c26d2f85cb2141b527aec203bd0e1c37ee0cf0`

Governance inputs:
- Context blob `4f927acb938f4d91b52fa07649b75b5f450d1d3f`, SHA-256 `3c507795c996e571152d4877a594abb889e4a8a017130332a166d5dda84af866`
- registry blob `490039cecf5a02ac7e553f8f7e47f6d4baedb584`, SHA-256 `0320e51fb4f53fbed2c2e6a51d41c83e2b8ddd7afe59c6fca91a0a34eaf7f8f5`
- CORE blob `eee2c1b4c27029f05d6ea246ae95cf30c17f0d5e`
- AP0 manifest SHA-256 `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`
- Context ID `CTX-d0501ec820062bfe373f1f4b94de4e191ca2c7e05bbe788b3d5d963750158cbf`

## Execution rules

Preserve the user's local branch unchanged.

One corpus attempt only:
1. fetch governed remote branch;
2. require exact authorized HEAD;
3. verify AP0 manifest;
4. create a brand-new temp stage;
5. materialize helper + Context + registry + CORE from raw Git blobs;
6. verify exact identities before execution;
7. py_compile helper;
8. execute once to a unique output;
9. preserve BLOCKED output if any;
10. if CR1_COMPLETE, copy exact JSON to handoff directory and return terminal + JSON.

No strategy, PnL, signed direction target, MT5, optimisation or regime naming.
