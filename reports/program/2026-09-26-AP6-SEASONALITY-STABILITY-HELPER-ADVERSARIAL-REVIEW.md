# AP6 — Seasonality / Stability — helper adversarial review

Date : 2026-09-26  
Branch : `integration/system-v1`  
Persisted HEAD reviewed : `27eeefa038d1a06390c90582d900847159c18688`.

## 1. Candidate identity

Production helper:
- path: `tools/ap6_seasonality_stability.py`
- Git blob: `28b5a298156616b9385dc0d8e4b0cfbaa3705497`
- SHA-256: `e5463af97783e193f54e1ef25d96626c6a9a511e7236469054b69a788f6dfc6c`
- bytes: 28,784

Synthetic harness:
- path: `tests/test_ap6_seasonality_stability.py`
- Git blob: `0fa5a4b7a5bd7da117ab0f26077c74b7d58336c2`
- SHA-256: `fcb5859fbf325c0b525a89a1d7f9fe5289bbea72aaf9e0d30b401b5fb2af356b`
- bytes: 5,503

Mutation runner:
- path: `tests/run_ap6_mutation_breakers.py`
- Git blob: `5dc0b786cabb649b18752d099fef6a9b01fe34a5`
- SHA-256: `75fc8904a8c37490e1e42a18a2bbf52c53d4e57a5e0e209513bf73746eb1d2b9`
- bytes: 3,123

The Git blob identities of the persisted files were matched against the locally executed files with `git hash-object`, establishing byte equality.

## 2. Re-break of persisted bytes

- `python -m py_compile`: PASS
- synthetic suite: **19/19 PASS**
- mutation suite: **18/18 KILLED**

Mutation evidence:
`reports/program/evidence/2026-09-26-AP6-MUTATION-RESULTS.json`

## 3. Synthetic coverage

The suite covers:
- 1m return crossing a missing minute;
- RV15/RV60 gap/segment boundaries;
- efficiency gap continuity;
- direct RV endpoint-boundary gap;
- New York DST conversion;
- New York month vs UTC month;
- weekday coding;
- UTC quarter coding;
- exclusion of 2021/2026 from the complete-year reference;
- frozen-reference CDF drift;
- Spearman vs Pearson;
- deterministic average tie ranks;
- persistence bucket-boundary adjacency;
- AP3/AP4/AP5 upstream binding chain;
- symlink/reparse path-chain defense;
- forbidden scope mutations;
- temporal partition conservation;
- population CV.

## 4. Mutants killed

All preregistered semantic mutants were killed:
RETURN_CROSS_GAP, RV_CROSS_GAP, EFFICIENCY_BAD_WINDOW, NY_TIMEZONE_UTC,
WEEKDAY_SHIFT, NY_MONTH_REPLACED_UTC, QUARTER_OFF_BY_ONE,
PARTIAL_YEARS_LEAK_REFERENCE, PERIOD_SPECIFIC_CDF_THRESHOLDS,
SPEARMAN_TO_PEARSON, TIE_RANK_FIRST, PERSISTENCE_CROSS_BUCKET,
AP5_BINDING_BYPASS, SYMLINK_CHAIN_BYPASS, SOURCE_VOLUME_SCOPE_TRUE,
STABILITY_THRESHOLD_TRUE, PNL_SCOPE_TRUE, PARTITION_MINUTE_CHECK_BYPASS.

## 5. Static review

PASS:
- AP0 manifest exact binding;
- AP3/AP4/AP5 exact evidence SHA bindings;
- AP3→AP2, AP4→AP3, AP5→AP4 chain validation;
- only preregistered AP0 columns are read;
- no bid/ask/source volume field is read;
- AP0 manifest members and bound evidence paths reject symlink/reparse chains;
- each AP0 file is checked by size/SHA/schema/metadata and rehashed after read;
- reconstructed coverage checks 1,709,180 minutes / 376,003,618 ticks;
- first and final segment identity checked;
- AP2/AP4/AP5 global reconciliation constants are preregistered;
- temporal dimensions are NY hour/weekday/month + UTC year/quarter;
- rolling observations use endpoint-minute temporal attribution;
- primary stability reference is exactly 2022–2025;
- frozen-reference decile CDF distance is used;
- Spearman uses average ranks for ties;
- temporal partitions conserve minutes/ticks/valid metric counts;
- output is aggregate-only and bounded to 64 MiB;
- strategy/PnL/optimization/future labels/stability-threshold scope remains false.

## 6. Important limits

- This is a synthetic/adversarial qualification of the helper, not a corpus result.
- Same assistant produced and reviewed the candidate; **no independent review is claimed**.
- The 2022–2025 reference is retrospective descriptive context, not a live threshold.
- AP6 PASS, if later obtained, will qualify the stability measurements, not assert that every observed behavior is stable.
- AP4 breakout/reentry future-label findings remain outside AP6 V0.1 stability promotion.
- No strategy, edge, PnL, backtest or MT5 statement is authorized.

## Verdict

**PASS — AP6 helper is qualified for one governed local corpus attempt.**

AP6 corpus itself remains **BLOCKED/PENDING EXECUTION** until exact local evidence is returned and adjudicated.
