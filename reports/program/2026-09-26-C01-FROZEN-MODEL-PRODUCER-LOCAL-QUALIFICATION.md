# C01 — frozen-model artifact producer — local qualification

Date: 2026-09-26

## Status

**LOCAL CANDIDATE QUALIFIED — NOT YET PERSISTED / NOT YET AUTHORIZED FOR CORPUS**

No confirmation data was accessed.

## Candidate identities

Helper candidate:
- intended path: `tools/c01_frozen_model_artifact.py`
- bytes: 21,431
- SHA-256: `682c1ce6f06f753cf3f0508396394bf6acd51249dfe61dc1c89815755137133c`
- expected Git blob: `ee0989f29399bf9f904ca314fdb5f01cc45ddec8`

Synthetic tests:
- intended path: `tests/test_c01_frozen_model_artifact.py`
- bytes: 7,316
- SHA-256: `2d0d447816a48b8b4ee9a694778356313a407c84ccdb0cb56746252ab4732217`
- expected Git blob: `1386ab0da905817f496c11197afd63b35620ccee`

Mutation runner:
- intended path: `tests/run_c01_frozen_model_mutation_breakers.py`
- bytes: 3,079
- SHA-256: `222ca69aa57491a12b3df6f03866de3e1ce6807049dc855eb79a23950c7acdb1`
- expected Git blob: `4d42ba615444601f115e65c8379d6d303fa5487b`

## Local qualification

- py_compile: PASS
- synthetic: **25/25 PASS**
- mutation: **15/15 KILLED**

## Producer purpose

The producer is restricted to development AP0 data and must serialize:
- 24 tick5 NY-hour medians;
- frozen ABS RV15 thresholds;
- frozen relative tick thresholds;
- frozen RV15/TICK15 target quintiles;
- B2+ABS_VOL count/probability table;
- B2+TICK count/probability table;
- B2+ABS_VOL+TICK count/probability table;
- canonical model digest.

It must also reproduce the already-observed CR2 D2026 C01 scores/state counts before emitting a frozen model artifact.

## Scope guards

The local candidate keeps:
- confirmation_data_accessed = false
- pnl_calculated = false
- direction_target_used = false
- winner_selection = false
- semantic_regime_labels_instantiated = false
- optimization/feature search/interaction search = false
- MT5 = false

## Mutation breakers killed

15/15:
- old Charter accepted
- confirmation-window drift
- threshold drift
- C02 promotion accepted
- forbidden scope opening
- count-matrix oversize
- Laplace removal
- digest blind to candidate counts
- weak numeric comparison
- D2026 score reproduction bypass
- D2026 state-count reproduction bypass
- confirmation-data access enabled
- PnL enabled
- winner selection enabled
- symlink/reparse bypass

## Required next action

Persist the **exact three candidate byte streams** to GitHub and require the expected Git blob IDs above.

Then:
1. fetch persisted HEAD;
2. recover exact persisted bytes;
3. py_compile;
4. 25/25 synthetic;
5. 15/15 mutation;
6. static review;
7. only then authorize one development-corpus model-freeze run.

No confirmation-data access before the resulting model artifact is sealed.
