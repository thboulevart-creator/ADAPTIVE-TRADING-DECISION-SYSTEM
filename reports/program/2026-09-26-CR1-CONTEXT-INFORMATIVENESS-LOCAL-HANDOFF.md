# CR1 — Context Informativeness — local execution handoff

Date : 2026-09-26  
Branch of authority : `integration/system-v1`

## Qualification status after incident

The prior local-run authorization is **revoked** pending persisted-head re-break of the corrected helper.

Corrected helper candidate:
- expected Git blob: `bb5cd4acd1b48141019c0ec3796ea61627dc0dbf`
- expected SHA-256: `423eed0f22b87a92210f53c6668c5b242c8ddb687da3292415c43879fb1f4eac`

Root cause:
the registry Git blob was correct, but its auxiliary SHA-256 had been miscomputed during orchestration. The raw Git blob SHA-256 is `24db0f82a602fa9e1abc04d2793898847c98dc27ed5fe4a16bcd12502fd787a4`.

Governance inputs:
- Context blob `4f927acb938f4d91b52fa07649b75b5f450d1d3f`, SHA-256 `3c507795c996e571152d4877a594abb889e4a8a017130332a166d5dda84af866`
- registry blob `490039cecf5a02ac7e553f8f7e47f6d4baedb584`, SHA-256 `24db0f82a602fa9e1abc04d2793898847c98dc27ed5fe4a16bcd12502fd787a4`
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
