# SESSION BACKUP — 2026-09-26 — CR1 CANDIDATE QUALIFIED LOCALLY / EXACT TRANSFER PENDING

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branch: `integration/system-v1`
Fresh HEAD before persistence: `98a58f676cab1a436b762c8e5bbb3190f078b538`.

## Upstream closed state

- AP0→AP6 PASS.
- ASSET BEHAVIORAL PROFILE CORE V0.1 PASS.
- CONTEXT / REGIME RESEARCH PREFLIGHT V0.1 PASS.
- CR1 Context identity materialized.

CR1 remains:
**N0 / EXPLORATORY / PREVIOUSLY EXPOSED CORPUS.**

No regime has been identified.
No strategy/PnL/MT5/optimization is authorized.

## CR1 local candidate

Exact local production helper:
- working path: `/mnt/data/cr1_context_informativeness.py`
- bytes: **36,971**
- SHA-256: `2ec7ae1b2db5f0afe7b9ff4405c26d2f85cb2141b527aec203bd0e1c37ee0cf0`
- expected Git blob: `484f74d0c05eabd3ecc0d9b35fbbafdf120f408a`

Exact synthetic harness:
- path: `/mnt/data/test_cr1_context_informativeness.py`
- bytes: **8,354**
- SHA-256: `758d5f68b38ea704bdb5256375f8f03cebf51dc07eae470f698104aabf4106b8`
- expected Git blob: `d326ddafa1d348decb4ae67ac480bc01060ac340`

Exact mutation runner:
- path: `/mnt/data/run_cr1_mutation_breakers.py`
- bytes: **3,289**
- SHA-256: `7b9a8ef462378a64779f9ecfb4e55464ef5f84264814b212ee37338d225c7146`
- expected Git blob: `69455bdbbde6e9f693e8f29c0fb2969fa8490d15`

## Local qualification

- `python -m py_compile`: PASS
- synthetic tests: **26/26 PASS**
- mutation breakers: **20/20 KILLED**

Coverage includes:
- full Context identity / forged context rejection;
- t→t+1 causal target alignment;
- return/forward target gap and segment breakers;
- trailing metrics causal at t;
- train-only folds and frozen thresholds;
- train-only target quintiles;
- B0/B1/B2 baseline hierarchy;
- H07 fixed gap/reopen categories;
- H07 spread15 registered diagnostic;
- sparse-state support guard;
- D2026 excluded from primary adjudication;
- no direction/PnL/regime labels;
- NY DST;
- symlink/reparse path protection;
- exact eight-hypothesis registry retention.

Static review before persistence also confirmed:
- supplied Context/registry/CORE required from repo-root;
- no silent Context reconstruction/fallback;
- CORE upstream binding checked;
- AP0 read scope limited to minute/tick_count/segment_id/mid_close/spread_mean;
- vectorized integer key scoring;
- output retains all hypotheses including negative/uninterpretable outcomes.

## Transfer status

Two exact Git objects have already been created in GitHub object storage but are **unreferenced and non-authoritative**:
- synthetic harness blob `d326ddafa1d348decb4ae67ac480bc01060ac340`;
- mutation runner blob `69455bdbbde6e9f693e8f29c0fb2969fa8490d15`.

The production helper has **not** been successfully created as its expected complete blob.

Manual base64/chunk transfer attempts detected byte differences before any branch ref update. Those incomplete/unreferenced objects must not be used.

No CR1 tool file currently exists in the governance tree.
No corpus run is authorized.

## Next exact action

Obtain the exact 36,971-byte helper as a visible conversation attachment, then:

1. read its exact bytes through Files;
2. require SHA-256 `2ec7ae1b2db5f0afe7b9ff4405c26d2f85cb2141b527aec203bd0e1c37ee0cf0`;
3. create Git blob and require `484f74d0c05eabd3ecc0d9b35fbbafdf120f408a`;
4. fresh HEAD;
5. create one tree containing helper + exact harness + exact mutation runner;
6. commit candidate and fast-forward `integration/system-v1`;
7. fetch persisted bytes;
8. re-run py_compile + 26/26 synthetic + 20/20 mutation suite on persisted identity;
9. only after PASS, persist helper adversarial review/local handoff;
10. only then authorize one real CR1 corpus run.

Do not bypass exact byte identity.
