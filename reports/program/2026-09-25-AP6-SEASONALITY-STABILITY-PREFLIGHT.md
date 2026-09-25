# AP6 — SEASONALITY / STABILITY — PREFLIGHT V0.1

Date : 2026-09-25  
Repository : `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch : `integration/system-v1`  
Fresh HEAD before persistence : `7904177b6ddd121aaba6fd00ea7ede01cc1db87e`.

## 1. Purpose

AP6 closes the Asset Behavioral Profile CORE measurement sequence by quantifying temporal seasonality and distribution stability.

Protocol requirements:
- hour;
- weekday;
- month;
- year;
- sub-periods;
- distribution stability.

AP6 is descriptive and strategy-agnostic.
AP6 PASS will mean **the stability measurements are valid under this contract**, not that the asset itself is stable.

No binary stable/unstable threshold is preregistered.

## 2. Exact upstream bindings

AP0:
- identity `USTECH_PROFILE_MINUTE_CORE_V0_1`;
- manifest SHA-256 `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`;
- 61 files;
- 1,709,180 minutes;
- 376,003,618 source ticks;
- 1,606 segments.

Upstream evidence chain:
- AP2 SHA-256 `4e3c79a5b9c8131f62a8fb7f205712d8a5c4301ff01b7fd3ce7226d8799d9c9f`;
- AP3 SHA-256 `caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef`;
- AP4 SHA-256 `c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad`;
- AP5 SHA-256 `21dc09b082e32f20543c6206c276c24389b7b61fd930fbe2d1783adabaca4406`.

AP6 helper must verify:
- exact AP3/AP4/AP5 evidence bytes from repo-root;
- AP3→AP2 binding;
- AP4→AP3 binding;
- AP5→AP4 binding;
- AP0 manifest binding.

## 3. AP0 columns allowed

Read only:
- `minute_start_ms_utc`;
- `tick_count`;
- `segment_id`;
- `mid_open`;
- `mid_high`;
- `mid_low`;
- `mid_close`;
- `spread_mean`.

Source volume fields remain forbidden.

The same exact-path / no-symlink-or-reparse / size+SHA controls qualified in AP5 apply to every AP0 member.

## 4. Canonical metric arrays

AP6 reconstructs only the following strategy-agnostic metrics.

1. `minute_range_bps`  
   `(mid_high-mid_low)/mid_open*10000`.

2. `abs_log_return_1m_bps`  
   `abs(log(close_t/close_t-1))*10000`, only same segment and exact +60,000 ms.

3. `realized_vol_15m_bps`  
   AP2 exact semantics: sqrt(sum of squared valid signed 1m log returns over 15 contiguous minutes) × 10000.

4. `realized_vol_60m_bps`  
   Same semantics at 60 minutes.

5. `efficiency_15m`  
   AP4 exact semantics: abs(sum signed 1m bps) / sum(abs(signed 1m bps)) over a valid contiguous 15-minute window; exact flat windows excluded.

6. `efficiency_60m`  
   Same semantics at 60 minutes.

7. `spread_mean`  
   AP0 per-minute arithmetic mean spread.

8. `tick_count`  
   AP0 ticks per observed minute; **not traded volume**.

Structural rate:
- non-zero 1m directional persistence/reversal, with AP4 exact adjacency semantics.

## 5. Required global reconciliations

Tolerance for floating aggregate reconciliation: `1e-9`.

Must reproduce:
- minute_range mean = `4.033115022615127`;
- abs return 1m count = `1,707,574`;
- abs return 1m mean = `2.130371613870453`;
- RV15 count = `1,686,423`;
- RV15 mean = `10.478525943077567`;
- RV60 count = `1,620,195`;
- RV60 mean = `21.63083566473441`;
- efficiency15 count = `1,686,423`;
- efficiency15 mean = `0.25740927472902353`;
- efficiency60 count = `1,620,195`;
- efficiency60 mean = `0.13080767215518072`;
- persistence rate = `0.4933796682202942`;
- spread tick-weighted mean = `2.1395040593705223` within tolerance;
- tick density mean = `219.99064931721645`.

## 6. Temporal dimensions

### 6.1 New York hour

`America/New_York`, DST-aware, codes 0..23.

### 6.2 New York weekday

`America/New_York`, Monday=0 ... Sunday=6.

Empty categories remain explicit count=0/null.

### 6.3 New York month

`America/New_York`, month 1..12.

### 6.4 UTC year

2021..2026.

- 2021 = partial dataset year;
- 2026 = partial dataset year;
- 2022..2025 = primary complete-year reference set.

"Complete year" here means not truncated by the dataset start/end boundary. It does not claim gap-free market coverage.

### 6.5 UTC calendar quarter

From 2021Q2 through 2026Q2.

- first and last quarter are boundary-partial;
- other quarters are calendar windows, not claims of gap-free coverage.

This dimension satisfies the protocol's sub-period requirement without data-driven boundary selection.

## 7. Bucket summaries

For each metric and each non-empty temporal bucket:
- count;
- mean;
- p10;
- p50;
- p90;
- p99.

For spread, also:
- tick-weighted spread mean using `tick_count`.

For every temporal dimension:
- minute counts must conserve 1,709,180;
- source tick counts must conserve 376,003,618;
- each metric's valid count must conserve its global valid count.

## 8. Distribution stability measure

Primary reference population:
**UTC years 2022, 2023, 2024, 2025 only.**

For each canonical metric:

1. compute reference decile thresholds p10..p90 on pooled reference observations;
2. compute the reference empirical CDF at those frozen thresholds;
3. for every UTC year and UTC quarter, compute its empirical CDF at the same frozen thresholds;
4. define:

`decile_cdf_distance = max_i abs(F_period(threshold_i) - F_reference(threshold_i))`.

This is a deterministic, bounded [0,1] distribution-drift measure.

Period-specific thresholds are forbidden.

No threshold converts this distance into stable/unstable.

Also report across complete years 2022..2025:
- CV of yearly means: population std / mean;
- CV of yearly medians;
- CV of yearly p90 values.

## 9. Seasonal-pattern stability

For each canonical metric and each seasonal dimension:
- NY hour;
- NY weekday;
- NY month;

build category **mean** vectors separately for 2022, 2023, 2024, 2025.

For every pair of complete years:
- use only categories non-empty in both years;
- require at least 3 common categories;
- compute Spearman rank correlation using deterministic average ranks for ties.

Report:
- pair count;
- minimum Spearman;
- mean Spearman;
- median Spearman.

Level drift:
for each category with values in all four complete years:
- population CV across its four yearly means.

Report:
- eligible category count;
- median category CV;
- maximum category CV.

No stability label is emitted.

## 10. Structural stability

Directional persistence/reversal must be computed with AP4 exact semantics:
- global;
- UTC year;
- UTC quarter.

Efficiency 15m and 60m are already canonical metric arrays and therefore receive the same yearly/quarter distribution stability analysis as the other metrics.

AP4 breakout/reentry findings are **not promoted as temporally stable by AP6 V0.1** because future-reentry labels are deliberately excluded from this stability helper. They may remain descriptive historical observations but cannot be called stable in the final CORE without a separate governed test.

## 11. Epistemic scope

Required output flags:
- `strategy_agnostic=true`;
- `signals_calculated=false`;
- `pnl_calculated=false`;
- `optimization=false`;
- `source_volume_used=false`;
- `future_labels_used=false`;
- `causal_deployable=false`;
- `stability_measured=true`;
- `stability_threshold_applied=false`.

Reference deciles and full historical comparisons are retrospective descriptive statistics, not live thresholds.

## 12. Adversarial plan

Synthetic breakers must cover at minimum:

1. return crossing a missing minute;
2. RV15/RV60 crossing a gap or segment;
3. efficiency crossing a gap or segment;
4. UTC-vs-New-York hour error;
5. DST transition behavior;
6. weekday code shift;
7. New-York month vs UTC-month confusion;
8. partial 2021/2026 leakage into the 2022..2025 reference population;
9. period-specific decile thresholds substituted for frozen reference thresholds;
10. Spearman replaced by Pearson;
11. incorrect tie ranking;
12. temporal partition conservation failure;
13. AP3/AP4/AP5 binding mismatch;
14. AP0 member symlink/reparse alias;
15. forbidden source-volume use;
16. output scope mutation toward strategy/PnL/optimization.

Mutation breakers must kill the corresponding semantic mutants.

## 13. Resource/output bounds

Target peak memory: < 1 GiB.

Output JSON:
- target < 64 MiB;
- no minute-level rows exported;
- aggregates only.

## 14. Promotion semantics

AP6 may PASS if:
- exact bindings pass;
- corpus invariants pass;
- all preregistered metrics reconcile;
- all temporal partitions conserve;
- stability metrics are computed exactly as registered;
- adversarial tests/re-break pass;
- scope remains strategy-agnostic.

AP6 PASS **does not mean all patterns are stable**.

After AP6 PASS:
- construct the final Asset Behavioral Profile CORE V0.1;
- each promoted behavioral statement must carry its temporal stability evidence or an explicit instability/unresolved limitation;
- only then may the next CONTEXT / REGIME RESEARCH gate be considered.
