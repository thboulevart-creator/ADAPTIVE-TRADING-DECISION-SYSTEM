# SESSION BACKUP — 2026-09-25 — AP5 PASS / AP6 PREFLIGHT

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Governance branch: `integration/system-v1`  
Fresh HEAD before close persistence: `6b396b52ebfa4f8ccd27a834ca1fd5ca1fedbfa7`.

## 1. Major result of the day

AP5 — MICROSTRUCTURE PRICE-CORE is **PASS**.

Qualified evidence:
- `reports/program/evidence/2026-09-25-AP5-MICROSTRUCTURE-PRICE-CORE.json`
- exact size: 39,460 bytes
- exact SHA-256: `21dc09b082e32f20543c6206c276c24389b7b61fd930fbe2d1783adabaca4406`
- schema: `ATDS_AP5_MICROSTRUCTURE_PRICE_CORE_V0_1`
- status: `AP5_COMPLETE`
- 61 AP0 files rehashed
- 1,709,180 minutes
- 376,003,618 source ticks
- 1,606 segments

Qualified R4 provenance:
- canonical AP5 helper SHA-256: `fdb929f54d5c816cd12fb03130545b3714a38cb2261d3b23433fb1cd4b0f7671`
- canonical AP4 evidence SHA-256: `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`
- both materialized as raw Git bytes
- helper py_compile PASS
- AP5_COMPLETE / exit code 0

Adjudication:
`reports/program/2026-09-25-AP5-MICROSTRUCTURE-PRICE-CORE-ADJUDICATION.md`

Behavioral observations:
`reports/program/2026-09-25-AP5-MICROSTRUCTURE-PRICE-CORE-BEHAVIORAL-OBSERVATIONS.md`

Previous failed attempts remain preserved as evidence:
- R1/R2 blocked on AP4 CRLF normalization;
- R3 produced AP5_COMPLETE but was rejected because helper provenance was not canonical;
- R4 was the first qualified run.

## 2. AP5 descriptive findings retained

Global:
- spread tick-weighted mean: `2.1395040593705206`
- minute-range mean: `4.033115022615127 bps`
- abs 1m return mean: `2.130371613870453 bps`
- tick density mean: `219.99064931721645`

Descriptive Pearson:
- spread mean vs minute range: `-0.3408104857682299`
- spread mean vs abs 1m return: `-0.23832275412888407`
- spread mean vs tick density: `-0.5910554340229595`

These are descriptive only. No causality, signal, edge, PnL or strategy claim.

## 3. Important execution lessons from AP5

Two Windows materialization hazards were discovered and closed:
1. AP4 evidence was converted LF→CRLF in an earlier staged snapshot, breaking exact SHA identity.
2. A staged helper used in R3 was not the frozen canonical helper; R3 was therefore correctly rejected.

The robust pattern retained for future local governed runs is:
- create a brand-new temporary stage;
- materialize exact files from raw Git blobs;
- hash in-process;
- hash again independently;
- compile helper;
- only then execute;
- use a unique output file;
- preserve all BLOCKED outputs instead of overwriting/deleting them.

The user's current local checkout is `feat/min-experiment-gaps-batch-v1`.
It is intentionally left untouched.
AP5/AP6 governance uses remote `integration/system-v1` plus exact Git object bindings.
Do not reset/rebase/merge/switch the user's local branch merely for governed corpus execution.

## 4. AP6 status

AP6 — SEASONALITY / STABILITY is **not executed**.

Its preflight is registered:
`reports/program/2026-09-25-AP6-SEASONALITY-STABILITY-PREFLIGHT.md`

Initial preflight commit:
`dff216afd0a6f93cc6a3a0a1d1175529cd549d22`

Clarification commit:
`6b396b52ebfa4f8ccd27a834ca1fd5ca1fedbfa7`

Clarification:
rolling/window metrics are attributed to the **endpoint minute**, consistent with AP2/AP4 semantics. Crossing an hour/day/month/quarter/year boundary does not invalidate an otherwise contiguous same-segment window.

AP6 registered dimensions:
- New York hour
- New York weekday
- New York month
- UTC year
- UTC calendar quarter

Primary complete-year reference:
- 2022
- 2023
- 2024
- 2025

2021 and 2026 remain partial context and are excluded from the primary stability coefficients.

Registered canonical metrics:
- minute range bps
- abs 1m log return bps
- RV15 bps
- RV60 bps
- efficiency15
- efficiency60
- spread_mean
- tick_count
- directional persistence/reversal

Registered stability measures:
- frozen-reference decile CDF distance
- CV of yearly means/medians/p90
- pairwise Spearman rank stability of seasonal category means
- category-level CV across complete years

No stable/unstable threshold is registered.
AP6 PASS will mean the stability measurements are valid, not that every pattern is stable.

## 5. AP6 candidate helper work performed in-session

A candidate AP6 helper and its synthetic/adversarial test harness were developed and reviewed in the assistant working session.

Latest in-session test state:
- 19/19 synthetic tests PASS
- 18/18 semantic mutants killed

Covered breaker classes include:
- return across missing minute
- RV15/RV60 across gap or segment
- efficiency across gap or segment
- UTC vs New York hour
- DST handling
- weekday coding
- New York month vs UTC month
- leakage of partial 2021/2026 into complete-year reference
- period-specific thresholds instead of frozen reference thresholds
- Pearson substituted for Spearman
- incorrect tie ranking
- temporal partition conservation
- AP3/AP4/AP5 binding mismatches
- AP0 member symlink/reparse alias
- forbidden source-volume use
- scope mutation toward strategy/PnL/optimization

Two weak fixtures were identified during mutation testing and strengthened before the final in-session 18/18 kill result:
- RV gap isolation
- persistence across bucket boundary

Static review also led to:
- removal of dead helper logic;
- reduced seasonal-stability masking cost;
- explicit final-segment invariant;
- endpoint temporal attribution clarification in preflight.

## 6. Critical limitation at session close

The AP6 helper/tests/mutation-runner **are not yet authoritative persisted artifacts on the governance branch**.

An attempted transfer was interrupted before a branch ref update.
Some Git blob objects may exist unreferenced, but they are not part of `integration/system-v1` and must not be treated as qualified artifacts.

Therefore:
- do not run AP6 corpus yet;
- do not claim AP6 helper PASS from the in-session local tests alone;
- first reconstruct/persist the exact candidate files;
- then fetch them back from the persisted HEAD;
- rerun py_compile, synthetic tests and mutation breakers on the persisted bytes;
- only after persisted-HEAD re-break PASS may a local corpus run be authorized.

## 7. Exact next governed action for tomorrow

1. fresh HEAD on `integration/system-v1`;
2. read this backup, AI operating memory and recovery checkpoint;
3. materialize/persist:
   - `tools/ap6_seasonality_stability.py`
   - AP6 synthetic tests
   - AP6 mutation breaker runner;
4. compute and record exact Git blob + SHA-256 identities;
5. persisted-HEAD re-break:
   - py_compile
   - synthetic suite
   - mutation suite
   - static scope/binding/path review;
6. if and only if all PASS:
   - persist AP6 helper adversarial review;
   - create AP6 local handoff;
   - execute the real AP0 corpus locally using a brand-new exact raw-Git stage;
7. adjudicate the exact AP6 JSON;
8. if AP6 PASS, build the final Asset Behavioral Profile CORE V0.1;
9. only after CORE V0.1 PASS may CONTEXT / REGIME RESEARCH be considered.

## 8. Scope still forbidden

Until CORE V0.1 is complete:
- no strategy design;
- no backtest;
- no PnL;
- no Sharpe/Profit Factor;
- no optimization;
- no MT5;
- no edge claim;
- no performance-oriented regime selection.

End-of-session status:
**AP5 PASS. AP6 PREFLIGHT PASS. AP6 helper candidate not yet persisted/qualified.**
