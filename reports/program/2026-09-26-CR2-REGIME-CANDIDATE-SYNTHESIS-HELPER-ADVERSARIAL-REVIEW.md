# CR2 — Regime-Candidate Synthesis — helper adversarial review

Date: 2026-09-26  
Branch: `integration/system-v1`  
Persisted candidate HEAD reviewed: `6f6fd02ba65a597fd04a1bb3e78edded7b19594d`

## Exact identities

Production helper:
- path: `tools/cr2_regime_candidate_synthesis.py`
- Git blob: `34c702e926b3baec90c57b8366177c2db1eca074`
- SHA-256: `cdea6b317400fbbd32208e05343a6a2c1c78c3cfbd04bcf0271fc7e60dfcf757`
- bytes: 25,383

Synthetic harness:
- Git blob: `dec91d42c70f5b38dbd23ba170222b5803aeb316`
- SHA-256: `7d72970ef38fab67a29fc33b6f7bdb5d3220557080f35144bb6b2dceb02b6582`
- bytes: 9,078

Mutation runner:
- Git blob: `0dc3875d51131095adb6a81772df825eaca26306`
- SHA-256: `89d91f5a171402363f236084f2787334892baca6598736af359c538db7725bce`
- bytes: 4,062

Persisted Git blob identities exactly match the locally executed bytes.

## Persisted-head re-break

Using system Python isolated from notebook warmup:
- py_compile: PASS
- synthetic suite: **26/26 PASS**
- mutation suite: **20/20 KILLED**

## Governed dependencies

The helper requires, inside the fresh stage:
- qualified CR1 helper blob `bb5cd4acd1b48141019c0ec3796ea61627dc0dbf`;
- Context exact SHA-256 `3c507795c996e571152d4877a594abb889e4a8a017130332a166d5dda84af866`;
- exact CR1 evidence blob `cd40bf975613d1fa0e6d7277c2850ec87104727e`;
- exact CR2 registry blob `c6e19dc67c521d8f79814473ffa19ae427398e4f`;
- AP0 manifest SHA-256 `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`.

No silent fallback/reconstruction is accepted for these identities.

## Static review

PASS:
- CR1 exact hypothesis statuses are required;
- forbidden CR1 scope must remain false;
- CR2 registry admits exactly C01/C02 and the five CR1-supported axes;
- no H05 spread, H07 gap or H08 efficiency enters the synthesis;
- C01 uses absolute RV15 only;
- C02 uses hour-relative RV15 only;
- both use hour-relative trailing tick5;
- H03 and H04 are never multiplied together;
- B2 hour+weekday remains conditioning backbone;
- dynamic identity remains exactly 3x3 = nine states;
- joint target remains 5x5 = 25 classes;
- RV/TICK target quintiles are learned on training fold only;
- dynamic tertiles are learned on training fold only;
- candidate is compared against both constituent baselines on the same test sample;
- all nine joint states, including zero-count states, are subject to sparse floor 500;
- D2026 cannot alter primary status;
- secondary 60m results cannot rescue primary 15m status;
- only AP0 minute/tick_count/segment_id/mid_close are read;
- no spread/source volume/depth/order-flow;
- no direction target, PnL, trades, signals, optimization, MT5, winner selection or semantic regime label.

## Limits

- CR2 remains `N0_EXPLORATORY` on a previously exposed corpus.
- Even `SUPPORTED_N0_SYNTHESIS` would mean incremental descriptive information only.
- C01 and C02 are parallel preregistered candidates; CR2 V0.1 does not rank or select between them.
- Same assistant produced and reviewed the helper; **no independent review is claimed**.

## Verdict

**PASS — CR2 helper qualified for one governed local corpus attempt.**

No CR2 candidate has yet been supported or refuted by corpus evidence.
