# C01 — CONFIRMATORY RESEARCH CHARTER V0.2

Date: 2026-09-26  
Status: **FROZEN BEFORE CONFIRMATION-DATA ACCESS**  
Supersedes: V0.1, preserved unchanged.

## 1. Amendment scope

V0.2 changes only the wording of the development-fit temporal boundary.

CR2 D2026 uses a training mask on the anchor timestamp `t`:

`utc_year(t) <= 2025`

The target is strictly future:

`t+1 ... t+H`

Therefore an anchor in the final minutes of 2025 may have a valid target window extending into the first minutes of 2026 if exact-minute and same-segment continuity holds.

V0.1 described this too broadly as all fitted information ending at 2025-12-31.

V0.2 corrects that semantic imprecision before any confirmation-data access.

No candidate, threshold, target, baseline, sparse rule, confirmation window or decision rule changes.

## 2. Candidate

`CR2-C01-ABS_VOL_X_TICK`

Origin CR2 evidence:
- blob `d6543d12fc01405fedb006ddb5d714a772f32678`
- SHA-256 `5c05e9e8d965314f4a6852aa71f442f89a0962133edc79873cf610682f34c501`

CR2 status:
`SUPPORTED_N0_SYNTHESIS`.

## 3. Exact development semantics

### Anchor rule

Every fitted training anchor must satisfy:

`utc_year(t) <= 2025`.

### Context parameters

The following are learned only from context observations anchored at `t <= 2025`:
- 24 NY-hour medians for tick5 normalization;
- ABS RV15 tertile thresholds;
- relative tick5 tertile thresholds.

### Target parameters and probability tables

For target quintiles and categorical probability tables:
- the anchor `t` must satisfy `utc_year(t) <= 2025`;
- the target starts strictly at `t+1`;
- the target may cross the 2025/2026 UTC-year boundary only if exact-minute continuity and same-segment continuity hold.

This exactly reproduces the registered CR2 D2026 fold semantics.

No anchor inside the confirmation window may enter fitting.

## 4. Already frozen thresholds

ABS RV15:
- 5.371776146488064
- 10.71209216288787

tick5 hour-relative:
- 0.8005586592178772
- 1.2183908045977012

future RV15 quintiles:
- 3.973523081929233
- 6.185588239477184
- 9.29219887827349
- 15.11786314181646

future TICK15 quintiles:
- 91.53333333333333
- 144.26666666666668
- 220.66666666666666
- 338.8

## 5. Frozen-model artifact

Before confirmation-data access, serialize:
1. 24 NY-hour tick5 medians;
2. B2+ABS_VOL 25-class counts/probability model;
3. B2+TICK 25-class counts/probability model;
4. B2+ABS_VOL+TICK 25-class candidate counts/probability model;
5. Laplace alpha = 1;
6. exact identities and registered thresholds.

The artifact must reproduce the thresholds above.

## 6. Confirmation data window

Unchanged:

`2026-05-25T00:00:00Z → 2027-05-24T23:59:59Z`

Same source lineage / USTECH price-core semantics required.

No primary confirmation score before the fixed window closes.

## 7. Primary decision rule

CONFIRMED only if:
- each of 9 joint states has >=500 valid primary targets;
- vs ABS_VOL: dLL > 0 and dBrier > 0;
- vs TICK: dLL > 0 and dBrier > 0;
- all identity/provenance/causality/continuity controls PASS.

REFUTED if either comparison has dLL <=0 or dBrier <=0.

NOT_INTERPRETABLE on sparse/provenance/control failure.

60m remains diagnostic only.

## 8. Forbidden

Unchanged:
- refit on confirmation data;
- threshold/bin search;
- feature/interaction modification;
- semantic regime naming;
- strategy/PnL/direction;
- winner selection;
- C02 redesign;
- MT5.

## Verdict

**V0.2 FROZEN BEFORE CONFIRMATION-DATA ACCESS.**

Next:
materialize and qualify the C01 frozen-model artifact producer using the exact D2026 development semantics above.
