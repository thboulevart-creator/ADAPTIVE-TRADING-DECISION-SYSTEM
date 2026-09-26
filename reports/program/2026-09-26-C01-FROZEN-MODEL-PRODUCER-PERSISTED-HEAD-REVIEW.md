# C01 — Frozen Confirmatory Model Producer — persisted-HEAD review

Date: 2026-09-26  
Branch: `integration/system-v1`  
Persisted candidate HEAD reviewed: `aa2c3311d1d838ada7f99dba69d94b463f089b3c`

## Exact persisted identities

Producer:
- path: `tools/c01_frozen_model_artifact.py`
- bytes: 21,431
- Git blob: `ee0989f29399bf9f904ca314fdb5f01cc45ddec8`
- SHA-256: `682c1ce6f06f753cf3f0508396394bf6acd51249dfe61dc1c89815755137133c`

Tests:
- path: `tests/test_c01_frozen_model_artifact.py`
- bytes: 7,316
- Git blob: `1386ab0da905817f496c11197afd63b35620ccee`
- SHA-256: `2d0d447816a48b8b4ee9a694778356313a407c84ccdb0cb56746252ab4732217`

Mutation runner:
- path: `tests/run_c01_frozen_model_mutation_breakers.py`
- bytes: 3,079
- Git blob: `4d42ba615444601f115e65c8379d6d303fa5487b`
- SHA-256: `222ca69aa57491a12b3df6f03866de3e1ce6807049dc855eb79a23950c7acdb1`

## Persisted-head re-break

- `py_compile`: PASS
- synthetic suite: **25/25 PASS**
- mutation suite: **15/15 KILLED**

Same assistant performed production/review; no independent-review claim.

## Bound governance inputs

- CR1 helper blob: `bb5cd4acd1b48141019c0ec3796ea61627dc0dbf`
- CR2 helper blob: `34c702e926b3baec90c57b8366177c2db1eca074`
- CR2 exact evidence blob: `d6543d12fc01405fedb006ddb5d714a772f32678`
- C01 Charter V0.2 blob: `ada0ebf41ecd7ab406d2656ac745ed7003d5b5c1`
- AP0 manifest SHA-256: `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`

## Static review

PASS:
- AP0 is read-only and fully rehashed.
- only `minute_start_ms_utc`, `tick_count`, `segment_id`, `mid_close` are read.
- confirmation model producer binds exact CR1/CR2 helpers, CR2 evidence and Charter V0.2.
- development anchor is `utc_year(t)<=2025`.
- future targets begin strictly after t using qualified CR1 helpers.
- exact minute/same-segment continuity remains required.
- 24 training-only NY-hour medians are produced for tick5 normalization.
- registered ABS-RV15, relative-tick, RV15-target and TICK15-target thresholds are reproduced exactly.
- three frozen categorical models are produced:
  - B2 + ABS_VOL;
  - B2 + TICK;
  - B2 + ABS_VOL + TICK.
- fixed Laplace alpha = 1.
- model digest binds the medians, thresholds, target quintiles and all three count matrices.
- D2026 is used only as an already-exposed reproduction control and must reproduce exact CR2 C01 scores/sample counts/joint-state counts.
- output is exclusive/no overwrite.
- output schema is `ATDS_C01_FROZEN_CONFIRMATORY_MODEL_V0_1`.
- `confirmation_data_accessed=false`.
- direction/PnL/trades/signals/optimization/threshold search/feature search/interaction search/winner selection/semantic labels/MT5 all remain false.

## Confirmatory boundary

This qualification authorizes only one run over the already-existing AP0 development corpus.

It does **not** authorize reading, scoring, fitting or evaluating confirmation observations in the fixed window:
`2026-05-25T00:00:00Z → 2027-05-24T23:59:59Z`.

## Verdict

**PASS — C01 frozen-model producer qualified for one development-only local run.**

The resulting model artifact must itself be authenticated, reviewed and sealed before any confirmatory-data plumbing can be considered.
