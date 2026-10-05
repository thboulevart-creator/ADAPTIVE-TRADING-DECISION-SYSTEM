# BEPD-01D — HISTORICAL EXTENSION READINESS CONTRACT V0.1

**Date:** 2026-10-05  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Persistence parent HEAD:** `51332246a6101ade08b585f6d58bfce856f5ae00`  
**Persistence parent TREE:** `63015c16abeabc9095041cf8c4a8339e7a42b8db`  
**Status:** CANDIDATE_CANONICALLY_PERSISTED / HUMAN_ADOPTION_PENDING  
**Five-year scan authority:** NONE  
**Occurrence/Response map authority:** NONE  
**Strategy/PnL/trading authority:** NONE

## 1. Purpose

Define the historical extension semantics required before the BEPD-01C engine may be generalized beyond the adopted six-week calibration surface.

This contract answers only:

> Can the Weekly/H1 event semantics be extended to the AP0 historical corpus without silent calendar drift, invisible pre-corpus state invention, invalid H1 closes, denominator corruption or provenance loss?

It does not execute the historical study.

## 2. Bound upstream identities

```text
BEPD-01A CONTRACT =
341f6267f7f1add350759d6d95dfebfb5b9e46f7

BEPD-01A FIXTURE R1 =
d2e663eaef865507c1cb92f5baa0074dcfc11032

BEPD-01B BREAKER CONTRACT =
d602a0666ab92662f2355ce0f44893934a7943a1

BEPD-01B EXECUTABLE BREAKER =
8433b725bb47423eac5879074557202993a664c2

BEPD-01C ENGINE =
050c96049f720757231136386719a40dd5653bbe

BEPD-01D BOUNDED CHARACTERIZATION =
1ed879076c42c1c1697af0722cc99e6dbcb3a196

BEPD-01D LEDGER SCHEMA =
85f5cdda60397fce59efc1e5d36c1128cf9cc185
```

AP0 dataset:

```text
DATASET_ID =
USTECH_PROFILE_MINUTE_CORE_V0_1

AP0-MANIFEST.json SHA256 =
62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce

FIRST SOURCE TICK =
2021-05-25T00:00:00.309Z

LAST SOURCE TICK =
2026-05-24T23:59:59.963Z

MID_IS_EXECUTION_PRICE =
false
```

## 3. Historical Weekly boundary

The calibration-only `Monday 00:00 Europe/Paris` convention is not promoted as the general historical boundary.

Bounded AP0 characterization shows that during US/Europe DST mismatch weeks the source may already be trading before Monday 00:00 Europe/Paris.

Historical session-week identity is therefore:

```text
WEEK_BOUNDARY_TIMEZONE =
America/New_York

WEEK_START_LOCAL =
Sunday 18:00:00 inclusive

WEEK_END_LOCAL =
next Sunday 18:00:00 exclusive

WEEK_ID =
the Monday calendar date reached six hours after WEEK_START_LOCAL
```

The IANA timezone database must be used. No fixed UTC offset is permitted.

Store both:

```text
week_start_ny
week_start_utc
week_end_ny
week_end_utc
ny_utc_offset_at_start
```

`Europe/Paris` is allowed only as a derived display coordinate, never as the authoritative historical session boundary.

## 4. Compatibility with BEPD-01A

For all six adopted calibration weeks:

```text
2026-01-12
2026-01-19
2026-01-26
2026-02-02
2026-02-09
2026-02-16
```

the NY session-week interval and the BEPD-01A calibration window select exactly the same AP0 minute set.

Therefore this historical extension does not rewrite the adopted calibration observations.

## 5. Complete-corpus week semantics

A session week is eligible to create Weekly levels and to finalize target-week outcomes only when its full interval is contained inside the AP0 coverage envelope:

```text
week_start_utc >= first_source_tick_utc
AND
week_end_utc <= last_source_tick_utc
```

This is a coverage-envelope rule. It does not assert that every minute inside the interval is observed.

States:

```text
LEFT_TRUNCATED
COMPLETE_CORPUS_WEEK_OBSERVED_SURFACE
RIGHT_TRUNCATED
```

Only `COMPLETE_CORPUS_WEEK_OBSERVED_SURFACE` may:

- create a HIGH and LOW level;
- act as a finalized target week;
- contribute denominator opportunities.

The first partial corpus week is therefore excluded from level creation.

The final partial corpus week is excluded from finalized outcomes and denominators.

## 6. Initial active-liquidity state

The historical universe is intentionally claim-scoped:

```text
UNIVERSE =
CORPUS_BORN_WEEKLY_LEVELS
```

At the beginning of the first eligible complete week:

```text
ACTIVE_LEVEL_SET =
EMPTY_BY_CONSTRUCTION
```

This does not mean no older real market levels existed.

It means:

```text
PRE_CORPUS_ACTIVE_LEVELS =
UNKNOWN / OUTSIDE CLAIM UNIVERSE
```

Forbidden:

- inventing pre-corpus Weekly highs/lows;
- reconstructing them from unavailable data;
- treating unknown pre-corpus levels as known inactive;
- later claiming the ledger contains all real historical Weekly liquidity.

The permanent scope phrase is:

> active Weekly levels born and observable inside the qualified AP0 corpus.

## 7. Weekly observed-surface level construction

For each eligible complete session week:

```text
WEEKLY_HIGH =
max observed AP0 mid_high inside the session-week interval

WEEKLY_LOW =
min observed AP0 mid_low inside the session-week interval

WEEKLY_CLOSE =
last observed AP0 mid_close inside the session-week interval
```

These are observed-surface quantities.

Internal source gaps do not get forward-filled.

Each source week records:

```text
gap_count_gt60s
max_gap_ms
intersecting AP0 file identities
source_week_file_binding_digest
```

A gap does not silently erase the week, but the ledger must retain that the level was formed on the observed AP0 surface.

## 8. Gap and holiday semantics

AP0 establishes:

```text
adjacent timestamp gap > 60,000 ms
→ new segment
```

AP0 alone does not establish why a gap occurred.

Therefore:

```text
GAP OBSERVED != MARKET HOLIDAY
GAP OBSERVED != SCHEDULED CLOSURE
GAP OBSERVED != DATA OUTAGE
```

Core historical detection must use:

```text
gap_cause = UNKNOWN
```

unless a separately versioned and qualified calendar/source is later bound.

`holiday_tag` may exist only as diagnostic metadata. It may not change event inclusion, exclusion, thresholding or support claims under BEPD-01D.

No holiday-effect research is authorized here.

## 9. Historical H1 identity

Historical H1 buckets use UTC clock hours:

```text
H1_BUCKET =
[HH:00:00 UTC, next HH:00:00 UTC)
```

Reason:

- UTC is unambiguous through DST transitions;
- Europe/Paris fall-back can repeat a local wall-clock hour;
- all adopted BEPD-01A event H1 buckets contain the same minute sets under UTC bucketing.

Display conversions to New York or Paris may be stored separately.

## 10. Qualified H1 close

A clock-hour bucket has a qualified H1 close only if the AP0 minute whose `minute_start` is exactly:

```text
HH:59:00 UTC
```

is observed.

If the terminal minute is absent:

```text
H1_CLOSE_STATE =
INCOMPLETE_TERMINAL

TAKE_ELIGIBLE =
false

REINTEGRATION_ELIGIBLE =
false
```

The last earlier observed minute must not be laundered into an H1 close.

If the terminal minute is present but one or more internal gaps exist:

```text
H1_CLOSE_STATE =
QUALIFIED_WITH_INTERNAL_GAP
```

The close may be used because the event rule is close-based, but the internal gap count must be recorded.

If terminal minute is present and no internal gap exists:

```text
H1_CLOSE_STATE =
QUALIFIED_CONTIGUOUS
```

## 11. Level take and reintegration

BEPD-01A semantics remain unchanged:

```text
HIGH take:
qualified H1 close > active HIGH

LOW take:
qualified H1 close < active LOW
```

Equality is not a take.

Consumption is permanent at the first qualifying H1 close beyond the level.

Reintegration is the first strictly later qualified H1 close back on the inside:

```text
consumed HIGH → later close < level
consumed LOW  → later close > level
```

A missing-terminal H1 can never trigger take or reintegration.

## 12. Target-week finalization

An event may be detected intraweek, but `close_displacement` is finalized only after the complete target session week ends.

A right-truncated target week cannot produce a finalized EVENT_LEDGER row.

Levels still active at the final completed-corpus horizon become:

```text
ACTIVE_RIGHT_CENSORED
```

They are not converted into failures.

## 13. Ledger architecture

Machine-readable schema:

`GOVERNANCE/BEPD-01D-HISTORICAL-LEDGER-SCHEMA-V0.1.json`

### LEVEL_LEDGER

One row per corpus-born HIGH/LOW level from an eligible complete source week.

It is the authoritative universe for:

- level birth;
- active lifetime;
- permanent consumption;
- right censoring;
- source-week quality/provenance.

### EVENT_LEDGER

One row per consumed LEVEL_LEDGER level.

Multiple consumed levels in one target week remain multiple level events sharing one `sweep_cluster_id`.

They are not declared independent observations.

## 14. Opportunity denominator

Future occurrence rates may not use raw event counts alone.

Primary denominator:

```text
LEVEL_WEEK_OPPORTUNITY
=
one row for every corpus-born level
that is ACTIVE at the START of an eligible complete target week
```

Numerator:

```text
swept_this_week = true
```

Rules:

- a level born at the end of the current week is not a same-week opportunity;
- a consumed level contributes once in its consumption week and never later;
- an unswept level contributes again in the next eligible complete week;
- unknown pre-corpus levels contribute neither numerator nor denominator;
- right-truncated weeks contribute neither;
- rows sharing `target_week_id` have a common dependence key and may not be treated as IID.

A weekly cluster rate may be computed later as diagnostic only. It is not a substitute for the level-week denominator.

## 15. Provenance requirements

Every future historical build must persist a run manifest binding at minimum:

```text
repository
branch
HEAD
TREE
run_id
dataset_id
AP0 manifest SHA256
selected AP0 relative paths + per-file SHA256
timezone runtime identity
weekly boundary timezone/rule
H1 bucket timezone/rule
engine blob
BEPD-01D contract blob
ledger schema blob
breaker contract blob
breaker executable blob
entrypoint/command
output file paths + SHA256 + row counts
```

A source-file digest mismatch is fail-closed.

Filename alone is not provenance.

## 16. Mandatory scientific distinctions

```text
CORPUS_BORN_LEVEL != ALL_REAL_MARKET_LEVELS
COMPLETE_COVERAGE_ENVELOPE != GAP_FREE_WEEK
OBSERVED_GAP != HOLIDAY_CAUSE
PARTIAL_HOUR_LAST_OBSERVATION != H1_CLOSE
LEVEL_OPPORTUNITY != INDEPENDENT_OBSERVATION
RAW_EVENT_COUNT != OCCURRENCE_RATE
MULTI_LEVEL_CLUSTER != MULTIPLE_INDEPENDENT_WEEKS
HISTORICAL_LEDGER != EDGE
EDGE != STRATEGY
MID != EXECUTION_PRICE
READINESS_PASS != FIVE_YEAR_SUPPORT
```

## 17. Pre-scan gate

Before any exhaustive historical build may be authorized, a frozen breaker must cover at least:

- US spring DST transition;
- Europe spring transition after US;
- Europe fall transition before US;
- US fall transition;
- ambiguous/repeated local Paris hour avoidance;
- missing H1 terminal minute;
- terminal minute present with internal gap;
- gap-cause/holiday laundering;
- left-truncated first corpus week;
- first complete corpus week;
- unknown pre-corpus active level;
- right-truncated final week;
- old active level persistence;
- current-week self-opportunity;
- consumed-level no-repeat;
- multi-level same-week dependence;
- denominator reconstruction;
- required provenance identities;
- AP0 mid execution-price laundering;
- exhaustive-scan authority laundering.

## 18. Authority and stop boundary

```text
BOUNDED AP0 CHARACTERIZATION =
AUTHORIZED / EXECUTED

READINESS CONTRACT DESIGN =
AUTHORIZED / PERSISTED CANDIDATE

LEDGER SCHEMA DESIGN =
AUTHORIZED / PERSISTED CANDIDATE

PRE-SCAN BREAKER CONSTRUCTION =
AUTHORIZED

FIVE-YEAR EXHAUSTIVE SCAN =
NOT AUTHORIZED

OCCURRENCE MAP =
NOT AUTHORIZED

RESPONSE MAP =
NOT AUTHORIZED

RELATION SEARCH =
NOT AUTHORIZED

STRATEGY / BACKTEST / PNL =
NOT AUTHORIZED

PAPER / BROKER / LIVE / CAPITAL =
NOT AUTHORIZED
```

STOP before exhaustive historical execution.
