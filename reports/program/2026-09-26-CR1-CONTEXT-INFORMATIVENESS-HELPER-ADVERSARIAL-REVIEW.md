# CR1 — Context Informativeness — helper adversarial review

Date : 2026-09-26  
Branch : `integration/system-v1`  
Persisted candidate HEAD reviewed : `6e9f1b4c44e0e76346061677dfe2e4fbf7f69001`

## Exact identities

Helper:
- path: `tools/cr1_context_informativeness.py`
- Git blob: `484f74d0c05eabd3ecc0d9b35fbbafdf120f408a`
- SHA-256: `2ec7ae1b2db5f0afe7b9ff4405c26d2f85cb2141b527aec203bd0e1c37ee0cf0`
- bytes: 36,971

Synthetic harness:
- blob: `d326ddafa1d348decb4ae67ac480bc01060ac340`
- SHA-256: `758d5f68b38ea704bdb5256375f8f03cebf51dc07eae470f698104aabf4106b8`
- bytes: 8,354

Mutation runner:
- blob: `69455bdbbde6e9f693e8f29c0fb2969fa8490d15`
- SHA-256: `7b9a8ef462378a64779f9ecfb4e55464ef5f84264814b212ee37338d225c7146`
- bytes: 3,289

The persisted Git blobs exactly match the locally executed candidate bytes.

## Persisted-byte re-break

- py_compile: PASS
- synthetic: **26/26 PASS**
- mutation: **20/20 KILLED**

## Critical boundaries covered

- deterministic Context identity and forged-context rejection;
- exact hypothesis-family preservation;
- Context/registry/CORE bound inputs;
- t-only trailing context;
- target starts strictly at t+1;
- future target rejects same-segment time gaps and segment crossings;
- NY timezone / DST;
- UTC chronological fold boundaries;
- D2026 excluded from primary adjudication;
- fixed reopen state boundaries;
- continuous context tertiles learned on train only;
- target quintiles learned on train only and frozen into test;
- unseen categorical keys receive fixed Laplace/uniform fallback;
- baseline B0/B1/B2 hierarchy;
- state hypotheses use B2;
- H07 spread15 diagnostic retained;
- sparse state blocks support;
- all hypotheses remain in output;
- no direction target, PnL, regime labels, feature search, threshold search, interaction search or winner selection.

## Static review

PASS:
- AP0 manifest identity is hard-bound;
- only minute_start/tick_count/segment_id/mid_close/spread_mean are read;
- no source volume/depth/order-flow field;
- AP0 files are size/hash/schema/metadata checked and rehashed after read;
- Context is supplied and exact, not reconstructed;
- registry family must be exactly the eight preregistered hypotheses;
- CORE exact Git blob and full upstream binding are verified;
- relative hour normalization is learned on training fold only;
- primary target classes are training-only quintiles;
- candidate and baseline are scored on the same test sample;
- scientific status uses F1/F2/F3 only;
- D2026 is diagnostic;
- fail-closed on sparse states;
- output family omission is rejected;
- scope remains N0 exploratory and non-economic.

## Limitations

- The corpus was already exposed during AP0→AP6; CR1 remains **N0 exploratory**, not pristine OOS.
- A positive CR1 result means descriptive out-of-fold information relative to a baseline, not economic value.
- Exact learned state thresholds are reproducible from frozen code/data/fold but are not serialized as a separate top-level audit object in V0.1; target thresholds and state counts are serialized per fold.
- Same assistant produced and reviewed the candidate; no independent review is claimed.
- No regime is instantiated by CR1.

## Verdict

**PASS — CR1 helper qualified for one governed local corpus attempt.**

CR1 corpus remains pending until exact local evidence is returned and adjudicated.
