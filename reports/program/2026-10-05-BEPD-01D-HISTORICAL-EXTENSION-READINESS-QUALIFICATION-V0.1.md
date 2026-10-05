# BEPD-01D — HISTORICAL EXTENSION READINESS — QUALIFICATION V0.1

**Date:** 2026-10-05  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Qualification persistence parent HEAD:** `ae69973806637ffd77cd3d112894f4599619c62f`  
**Qualification persistence parent TREE:** `f0e2aaea936ffa587c3c5715c6c5e8579cd8ecad`  
**Status:** QUALIFIED_CANDIDATE / PASS_WITH_NON_BLOCKING_NOTES / HUMAN_ADOPTION_PENDING

## 1. Qualification verdict

```text
BEPD-01D PRE-SCAN BREAKER =
PASS

EXACT OUTPUT =
BEPD_01D_PRE_SCAN_BREAKER_PASS

PROCESS EXIT CODE =
0

BEPD-01B / BEPD-01C BOUNDED REGRESSION =
PASS

EXACT OUTPUT =
BEPD_01B_BREAKER_PASS

REGRESSION EXIT CODE =
0
```

This is a readiness qualification only.

It is not a five-year historical result and does not establish market support, edge, strategy validity or trading authority.

## 2. Exact qualified identities

```text
BEPD-01D HUMAN AUTHORIZATION =
c7b7b54366eb15748f539f30b4520081d9c94756

BOUNDED HISTORICAL CHARACTERIZATION =
1ed879076c42c1c1697af0722cc99e6dbcb3a196

HISTORICAL LEDGER SCHEMA =
85f5cdda60397fce59efc1e5d36c1128cf9cc185

HISTORICAL EXTENSION READINESS CONTRACT =
a508fbaaa7468d3fd7a17991e48b9b207e274245

FROZEN PRE-SCAN BREAKER CONTRACT =
c2bf489b4991931d940d273d45856c308d0c99c9

EXECUTABLE PRE-SCAN BREAKER =
e8e0375604511765ce796f93354a2eaf55822b45

UPSTREAM BEPD-01B BREAKER =
8433b725bb47423eac5879074557202993a664c2

UPSTREAM BEPD-01C ENGINE =
050c96049f720757231136386719a40dd5653bbe
```

## 3. Calendar finding

Bounded AP0 characterization established that:

```text
Monday 00:00 Europe/Paris
!=
safe universal historical session-week boundary
```

During the US/Europe DST mismatch, source observations occur before Paris Monday midnight.

The qualified candidate historical boundary is:

```text
TIMEZONE =
America/New_York

SESSION WEEK =
[Sunday 18:00 local, next Sunday 18:00 local)

WEEK_ID =
following Monday date
```

IANA timezone conversion is required; fixed UTC offsets are forbidden.

On all six adopted BEPD-01A calibration weeks, this interval selected exactly the same AP0 minute set as the previously qualified calibration window.

## 4. Corpus edge semantics

AP0 coverage:

```text
FIRST SOURCE TICK =
2021-05-25T00:00:00.309Z

LAST SOURCE TICK =
2026-05-24T23:59:59.963Z
```

Derived candidate corpus boundaries:

```text
LEFT-TRUNCATED SESSION WEEK START =
2021-05-23T18:00:00-04:00
→ INELIGIBLE FOR LEVEL CREATION

FIRST COMPLETE ELIGIBLE SESSION WEEK START =
2021-05-30T18:00:00-04:00
WEEK_ID = 2021-05-31

LAST COMPLETE ELIGIBLE SESSION WEEK START =
2026-05-17T18:00:00-04:00
WEEK_ID = 2026-05-18

RIGHT-TRUNCATED NEXT SESSION WEEK START =
2026-05-24T18:00:00-04:00
→ INELIGIBLE FOR FINALIZED OUTCOMES / DENOMINATOR
```

## 5. Initial-state qualification

The candidate claim universe is:

```text
CORPUS_BORN_WEEKLY_LEVELS
```

Initial active state:

```text
EMPTY_BY_CONSTRUCTION
```

Interpretation:

```text
PRE-CORPUS REAL LEVELS =
UNKNOWN / OUTSIDE CLAIM UNIVERSE
```

No pre-corpus Weekly liquidity may be synthesized, guessed, backfilled or treated as known inactive.

This is a claim-scope boundary, not a statement that no older real levels existed.

## 6. H1 and gap qualification

Historical H1 identity:

```text
UTC clock-hour buckets
```

Qualified H1 close requires:

```text
observed AP0 minute_start = HH:59:00 UTC
```

If that terminal minute is missing, an earlier last observation may not be promoted to H1 close.

If terminal minute exists with internal gaps, the close remains observable but internal gap count is retained.

Gap causation remains:

```text
UNKNOWN
```

under AP0 alone.

Observed gap does not prove holiday, scheduled closure or data outage.

Holiday tags are diagnostic-only unless a separate calendar authority is later qualified and bound.

## 7. Ledger qualification

Two primary ledgers are frozen as candidate schema:

```text
LEVEL_LEDGER
grain = one row per corpus-born Weekly HIGH/LOW level

EVENT_LEDGER
grain = one row per consumed level
```

A reconstructible derived view is defined:

```text
LEVEL_WEEK_OPPORTUNITY
grain =
one row per ACTIVE corpus-born level
at the START of each eligible complete target week
```

Primary future occurrence denominator:

```text
COUNT(eligible LEVEL_WEEK_OPPORTUNITY rows)
```

Primary numerator:

```text
COUNT(rows where swept_this_week = true)
```

Raw event count alone is not an occurrence rate.

Rows sharing the same target week are dependent by construction and may not be treated as IID without a separate method decision.

## 8. Provenance qualification

Future historical output must bind exact:

```text
repo / branch / HEAD / TREE
run_id
AP0 manifest SHA256
selected monthly Parquet relative paths + SHA256
timezone runtime identity
week/H1 rules
engine blob
contract blob
ledger schema blob
breaker identities
entrypoint
output paths + SHA256 + row counts
```

Filename alone is insufficient provenance.

Source-file hash mismatch is fail-closed.

## 9. Breaker surface

26 frozen pre-scan cases cover:

```text
DST boundary drift
US/EU mismatch minute loss
ambiguous local-hour identity
partial H1 close laundering
internal-gap recording
holiday/gap cause laundering
left/right corpus truncation
pre-corpus state invention
old-level persistence
self-opportunity
post-consumption opportunity
same-week dependence
denominator omission
ledger schema drift
source hash mismatch
filename-as-provenance
mid-as-execution-price
readiness-to-support laundering
authority expansion
```

All 26 materialized cases passed the executable readiness breaker.

## 10. Non-blocking notes

```text
NB-01:
AP0 alone does not classify the cause of observed gaps.
This remains UNKNOWN by design and is not a blocker for observed-surface ledger construction.

NB-02:
holiday_tag remains diagnostic-only under this candidate.
A causal or exclusion role for holiday calendars would require a separate bound authority.

NB-03:
COMPLETE_CORPUS_WEEK_OBSERVED_SURFACE means coverage-envelope complete,
not gap-free.

NB-04:
The candidate universe intentionally excludes all unknown pre-corpus Weekly levels.
Claims must remain scoped to corpus-born levels.
```

These notes narrow claims; they do not authorize post-result filtering.

## 11. Human decision state

```text
BEPD-01D CONTRACT =
QUALIFIED CANDIDATE

BEPD-01D LEDGER SCHEMA =
QUALIFIED CANDIDATE

BEPD-01D PRE-SCAN BREAKER =
GREEN

HUMAN ADOPTION =
NOT YET SUPPLIED
```

No future exhaustive historical build should bind this candidate as policy until a separate human adjudication adopts the exact qualified identities.

## 12. Authority and stop boundary

```text
BOUNDED CHARACTERIZATION =
COMPLETE

PRE-SCAN READINESS QUALIFICATION =
PASS_WITH_NON_BLOCKING_NOTES

FIVE-YEAR EXHAUSTIVE SCAN =
NOT AUTHORIZED

OCCURRENCE MAP =
NOT AUTHORIZED

RESPONSE MAP =
NOT AUTHORIZED

RELATION / CONTEXT SEARCH =
NOT AUTHORIZED

STRATEGY / BACKTEST / PNL =
NOT AUTHORIZED

PAPER / BROKER / LIVE / CAPITAL =
NOT AUTHORIZED
```

STOP before exhaustive historical execution.
