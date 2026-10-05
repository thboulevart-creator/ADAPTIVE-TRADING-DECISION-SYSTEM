# BEPD-03D — LEVEL AGE OCCURRENCE MAP — QUALIFICATION V0.1

**Date:** 2026-10-05  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Qualification persistence parent HEAD:** `04b637ccecfc9bc33f50fe2fde781190893a828d`  
**Qualification persistence parent TREE:** `e3fb8ab68dd27f9cc142b9ce2b7b21e3f6f5f23e`  
**Status:** QUALIFIED / COMPLETE / HISTORICAL_FIXED_CORPUS_DESCRIPTIVE_AGE_HETEROGENEITY_ONLY

## 1. Verdict

```text
BEPD-03D LEVEL AGE OCCURRENCE MAP =
PASS

RESULT =
PERSISTED

BEPD-03D INDEPENDENT BREAKER =
PASS

BEPD-03C REGRESSION =
PASS

BEPD-03B REGRESSION =
PASS

BEPD-03A REGRESSION =
PASS

M05 GENERALIZATION UNCERTAINTY =
BLOCKED
```

No ranking, significance test, bootstrap, cross-product, predictive interpretation or response analysis was executed.

## 2. Exact execution identity

The age map was calculated from the exact pre-result-frozen execution commit:

```text
EXECUTED HEAD =
4a9f7410cfa9407ce5c730ef6894ec4c31853176

EXECUTED TREE =
be9c3535103d01b6484ee3f2698dc65625ea7803

RUN_ID =
85391ee64b2565de90fe953680f5c386a6f979415ccae56019ef03d07ab9df45
```

Source BEPD-02 run:

```text
68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821
```

## 3. Bound implementation identities

```text
HUMAN AUTHORIZATION =
4bbcc78cf8e74bcb5fcd96bc51b60921ed82e2b0

IMPLEMENTATION CONTRACT =
ee9464c167954367591654514c7cb0596be7340b

CALCULATOR =
d3cbad6e744fd9a6029561824a9618c2751de4a7

FROZEN BREAKER CONTRACT =
b24f70dceec8fe51cc8ef2c46b2178dcd56b46cd

EXECUTABLE BREAKER =
72b5c4cb1262cf55e77e444ef870477792bb3f48
```

## 4. Persisted result identities

```text
RESULT.json
Git blob =
3f14d347ad34a68a1a8012bf387e00dd0f1501b4

SHA256 =
32240c4c9fc633ec60434c020673ad0a35d3ebeb0f5874aea00622c6600232d3

BYTES =
3727
```

```text
RUN_MANIFEST.json
Git blob =
853e28047e4e98464bb5f3cc1c8e1e0c725949ff

SHA256 =
b263207803362419ee9e83b9194f369035a6089c2a50f5417d35f879784866f7

BYTES =
1732
```

Initial local result commit:

```text
2dfdcd99d7f9862af0cb0274650a5639a7eb8c7c
```

A concurrent non-BEPD commit advanced the governed branch before push. The unchanged result commit was therefore reapplied on top of the fresh remote HEAD and persisted as:

```text
PERSISTENCE COMMIT =
d4eb2b6c05d64e72f5adfbe29ab13c366051fe53

PERSISTENCE TREE =
fd33e8ba15c2795144bbaa168dddbaa0be8d989c
```

No BEPD-03D result bytes were changed by that reapplication.

## 5. Global descriptive reference

BEPD-03B remains the reference:

```text
TARGET WEEKS =
259

UNIQUE LEVELS =
518

OPPORTUNITIES =
7213

EVENTS =
472

EXACT FRACTION =
472/7213

HISTORICAL PROPORTION =
0.065437404685983641
```

## 6. V05 — LEVEL_AGE_BAND

Canonical preregistered order only:

```text
AGE_1
target weeks = 259
unique levels = 518
opportunities = 518
events = 255
fraction = 255/518
proportion = 0.492277992277992278

AGE_2
target weeks = 233
unique levels = 261
opportunities = 261
events = 53
fraction = 53/261
proportion = 0.203065134099616858

AGE_3_4
target weeks = 228
unique levels = 207
opportunities = 381
events = 49
fraction = 49/381
proportion = 0.128608923884514436

AGE_5_8
target weeks = 233
unique levels = 156
opportunities = 546
events = 43
fraction = 43/546
proportion = 0.078754578754578755

AGE_9_16
target weeks = 218
unique levels = 110
opportunities = 754
events = 33
fraction = 33/754
proportion = 0.043766578249336870

AGE_17_32
target weeks = 209
unique levels = 77
opportunities = 1065
events = 20
fraction = 20/1065
proportion = 0.018779342723004695

AGE_33_64
target weeks = 176
unique levels = 57
opportunities = 1415
events = 12
fraction = 12/1415
proportion = 0.008480565371024735

AGE_65_PLUS
target weeks = 168
unique levels = 30
opportunities = 2273
events = 7
fraction = 7/2273
proportion = 0.003079630444346678
```

These cells are descriptive historical age heterogeneity only.

No bin is ranked, selected, called best/worst or interpreted as a future-probability estimate.

## 7. Boundary semantics verified

The breaker independently verified:

```text
AGE_1       = 1
AGE_2       = 2
AGE_3_4     = 3..4
AGE_5_8     = 5..8
AGE_9_16    = 9..16
AGE_17_32   = 17..32
AGE_33_64   = 33..64
AGE_65_PLUS = >=65

AGE <= 0 =
FAIL CLOSED

NON-INTEGER AGE =
FAIL CLOSED
```

No bin was modified after result exposure.

## 8. Reconciliation semantics

The age partition satisfies:

```text
sum(opportunity_count) =
7213

sum(event_count) =
472
```

Target-week counts are intentionally not summed across bins because one target week may contain active levels of different ages.

Unique-level counts are intentionally not summed across bins because one surviving level may move through several age bins over time.

Instead, the breaker verified:

```text
union(age-bin target_week_id sets)
=
global target-week set

union(age-bin level_id sets)
=
global unique-level set
```

## 9. Dependence and uncertainty

```text
OPPORTUNITY ROW != IID OBSERVATION

DEPENDENCE KEY =
target_week_id

MULTIPLE ACTIVE LEVELS IN SAME TARGET WEEK =
STRUCTURALLY DEPENDENT

SAME LEVEL ACROSS MULTIPLE TARGET WEEKS =
TEMPORAL REPEATED MEASURE

M05 GENERALIZATION UNCERTAINTY =
BLOCKED
```

No confidence interval, bootstrap, p-value or significance label was produced.

## 10. Qualification evidence

Pre-result upstream replay:

```text
BEPD_03A_OCCURRENCE_MEASUREMENT_BREAKER_PASS
BEPD_03B_GLOBAL_OCCURRENCE_BASELINE_BREAKER_PASS
BEPD_03C_CALENDAR_OCCURRENCE_MAP_BREAKER_PASS
```

Post-calculation:

```text
BEPD_03D_LEVEL_AGE_OCCURRENCE_MAP_BREAKER_PASS
BEPD03D_BREAKER_EXIT_CODE=0
```

### Persistence checkout note

The first persisted-head replay was attempted in a Windows worktree whose checkout had converted LF to CRLF through `core.autocrlf`.

That working-copy conversion changed the local byte SHA of `RESULT.json` to:

```text
9afd489d781fcf6daac7ece3edc9b2ec4def8b5c3417308b068ecfd2565f96ba
```

and the byte-level checker correctly failed closed.

A direct comparison of the original result commit and the persisted Git commit then established that the canonical Git content was unchanged in both commits:

```text
CANONICAL RESULT SHA256 =
32240c4c9fc633ec60434c020673ad0a35d3ebeb0f5874aea00622c6600232d3

MANIFEST-BOUND RESULT SHA256 =
32240c4c9fc633ec60434c020673ad0a35d3ebeb0f5874aea00622c6600232d3

CANONICAL MANIFEST SHA256 =
b263207803362419ee9e83b9194f369035a6089c2a50f5417d35f879784866f7
```

The persisted HEAD was then replayed from a new clean worktree with `core.autocrlf=false`.

Observed:

```text
BEPD_03D_LEVEL_AGE_OCCURRENCE_MAP_BREAKER_PASS
BEPD_03C_CALENDAR_OCCURRENCE_MAP_BREAKER_PASS
BEPD_03B_GLOBAL_OCCURRENCE_BASELINE_BREAKER_PASS
BEPD_03A_OCCURRENCE_MEASUREMENT_BREAKER_PASS
BEPD03A_PERSISTED_REGRESSION_EXIT=0
```

Therefore the intermediate failure was a checkout byte-representation issue, not a semantic or canonical-artifact mismatch.

## 11. Explicit non-claims

BEPD-03D does not establish:

```text
a best level age
an optimal age threshold
statistical significance
stationarity
future sweep probability
predictive information
causation
age-based edge
strategy validity
PnL
trading authority
```

Observed age-cell differences remain historical descriptive heterogeneity only.

## 12. Authority boundary

```text
BEPD-03D LEVEL AGE OCCURRENCE MAP =
QUALIFIED / COMPLETE

TAKE DAY ANALYSIS =
NOT AUTHORIZED

AGE CROSS-PRODUCTS =
NOT AUTHORIZED

M05 =
BLOCKED

RESPONSE MAP =
NOT AUTHORIZED

OCCURRENCE × RESPONSE =
NOT AUTHORIZED

EDGE / STRATEGY / BACKTEST / PNL =
NOT AUTHORIZED
```

STOP.
