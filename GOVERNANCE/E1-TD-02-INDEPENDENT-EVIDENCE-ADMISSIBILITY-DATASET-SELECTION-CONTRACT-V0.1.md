# E1-TD-02 — INDEPENDENT EVIDENCE ADMISSIBILITY & DATASET SELECTION CONTRACT V0.1

## 0. STATUS

```text
SCHEMA =
ATDS_E1_TD_02_INDEPENDENT_EVIDENCE_ADMISSIBILITY_DATASET_SELECTION_CONTRACT_V0_1

CONTROL_ID = E1-TD-02

STATUS = CANDIDATE_AWAITING_HUMAN_ADOPTION
MODE = DOCUMENTARY / DATASET-ADMISSIBILITY PREREGISTRATION
```

Base :

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

HEAD =
23f93144e7c60acc02e3a7c0736aede020574ecc

TREE =
a26c4de1b830bb6ce13d10b9a165a2a330c47788
```

Protected research contract:

```text
E1_TD_01_CONTRACT_BLOB =
ba7671c24ce0cb8943169bd2be9701d48f41da76

E1_TD_01_HUMAN_ADOPTION_BLOB =
7051bc817696f7bc6fe0b74ae45c7f7436f45829
```

---

# 1. PURPOSE

This contract defines how the first independent evidence block for HYPOTHESIS-02 may be selected.

It must prevent:

```text
PERFORMANCE_BASED_DATASET_SELECTION
PERIOD_SHOPPING
INSTRUMENT_SHOPPING
POST_RESULT_WINDOW_EXTENSION
E1_OOS_REUSE
SOURCE_SUBSTITUTION
```

It does not authorize execution.

---

# 2. SELECTED INDEPENDENCE MODE

For the first independent evidence block:

```text
PRIMARY_INDEPENDENCE_MODE =
PROSPECTIVE_TEMPORAL_INDEPENDENCE

INSTRUMENT =
USTECH

STRATEGY =
FROZEN_MOMENTUM_V1

CROSS_INSTRUMENT_MODE =
NOT_SELECTED_FOR_FIRST_BLOCK
```

Rationale:

```text
change time
while holding strategy and instrument constant
```

This minimizes simultaneous changes.

---

# 3. PROSPECTIVE REQUIREMENT

The evaluation block must begin only after the admissibility contract has been humanly adopted.

Rule:

```text
EVIDENCE_WINDOW_START =
FIRST_FULL_UTC_MONTH_BOUNDARY_AFTER_HUMAN_ADOPTION
```

For adoption on 2026-09-29:

```text
EVIDENCE_WINDOW_START =
2026-10-01T00:00:00Z
```

Duration:

```text
EVIDENCE_WINDOW_DURATION =
12 CALENDAR MONTHS
```

Therefore, if adopted now:

```text
LOGICAL_WINDOW =
[2026-10-01T00:00:00Z,
 2027-10-01T00:00:00Z)
```

The window cannot be shortened, extended or shifted after any strategy-specific result has been observed.

---

# 4. WHY PRE-ADOPTION 2026 DATA IS EXCLUDED

The interval:

```text
2026-05-25
→
contract adoption
```

is not accepted as the primary prospective block.

Reason:

```text
IT ALREADY EXISTED BEFORE PREREGISTRATION
```

This does not imply that its market behaviour or strategy performance has actually been inspected.

It means only that it cannot receive the strongest prospective-independence status.

---

# 5. INSTRUMENT IDENTITY

The first block must preserve:

```text
ECONOMIC_INSTRUMENT = USTECH
```

An arbitrary substitute such as:

```text
NAS100 alternative provider
NQ futures
MNQ futures
NASDAQ-100 cash index
QQQ
synthetic CFD reconstruction
```

is not automatically equivalent.

A change in instrument semantics requires a separate equivalence/admissibility decision.

---

# 6. SOURCE CONTINUITY

Preferred source class:

```text
SOURCE_B_CONTINUATION
```

The future raw source should preserve, where available:

```text
same provider lineage
same USTECH instrument semantics
same timestamp semantics
same BID field semantics
same ASK field semantics
```

Required raw fields:

```text
timestamp
bid_price
ask_price
```

Volume remains unnecessary for this hypothesis.

If equivalent continuation of Source-B is unavailable:

```text
SOURCE_CONTINUITY_UNAVAILABLE = BLOCK
```

No automatic provider substitution is allowed.

A new source would require a separate source-equivalence qualification before performance use.

---

# 7. RAW DATA IMMUTABILITY

The admissible raw corpus must not be performance-conditioned.

Forbidden transformations:

```text
SORT_TO_REPAIR
DEDUPLICATE_TO_REPAIR
INTERPOLATE
FORWARD_FILL
SYNTHETIC_TICK_INSERTION
PRICE_RECONSTRUCTION
PERFORMANCE_BASED_ROW_FILTER
```

Source order is authoritative.

Data quality defects must be represented, bounded or cause blocking — not silently repaired.

---

# 8. CONTINUITY SEMANTICS

The future dataset must preserve the existing ATDS continuity rule:

```text
gap > 60000 ms
→ FORBIDDEN_BOUNDARY
```

Exactly:

```text
gap = 60000 ms
→ allowed
```

Continuity rules cannot be relaxed after observing results.

---

# 9. H1 DERIVATION

Future H1 derivation must preserve E1 semantics:

```text
timezone = UTC
bucket = exact 1 hour
60 exact M1 minutes required
same source segment required
no forward fill
no interpolation
no synthetic minutes
close = minute offset 59 mid_close
```

Continuity block and warmup semantics remain frozen.

---

# 10. WARMUP

The independent evidence block must not borrow pre-window strategy history.

Therefore:

```text
INITIAL_POSITION = 0
```

and:

```text
WARMUP =
FIRST 20 COMPLETED ADMISSIBLE H1 BARS
WITHIN THE INDEPENDENT WINDOW
```

No momentum signal may use H1 history before the independent evidence window.

This deliberately prioritizes independence over maximizing trade count.

---

# 11. EXECUTION SEMANTICS

If execution is later authorized, it must remain identical to frozen E1:

```text
same-bar execution = FORBIDDEN
earliest execution = t+1

BUY = ASK
SELL = BID

gap boundary crossing = FORBIDDEN
pyramiding = FORBIDDEN
```

No execution rule may be altered to improve sample size or performance.

---

# 12. COST SCOPE

Frozen:

```text
RAW BID/ASK SPREAD = INCLUDED

COMMISSION = EXCLUDED
ASSUMED_ZERO = FALSE

SLIPPAGE = EXCLUDED
ASSUMED_ZERO = FALSE

FINANCING = EXCLUDED
ASSUMED_ZERO = FALSE
```

The evidence block therefore cannot establish broker-net profitability.

---

# 13. MINIMUM EVIDENCE RULE

E1-TD-01 already freezes:

```text
MINIMUM_CLOSED_TRADES = 100
```

This contract does not change it.

Crucially:

```text
THE WINDOW IS NOT EXTENDED
IF CLOSED_TRADES < 100
```

If the preregistered 12-month block produces:

```text
CLOSED_TRADES < 100
```

then:

```text
VERDICT =
INSUFFICIENT_EVIDENCE
```

A second/longer window would require a new preregistration.

---

# 14. NO TRADE-COUNT PEEKING FOR WINDOW SELECTION

Before the window is frozen, the system may not run MOMENTUM_V1 merely to determine how many trades a candidate window would contain.

Therefore window length is selected by calendar rule:

```text
12 MONTHS
```

not by:

```text
RUN UNTIL 100 TRADES
```

This prevents adaptive stopping.

---

# 15. DATASET IDENTITY REQUIREMENTS

Before any performance execution, the complete raw corpus must receive a sealed identity containing at minimum:

```text
dataset_id
instrument_identity
source/provider identity
acquisition method
logical UTC window
first observed timestamp
last observed timestamp
required columns
file count
row count
total bytes
per-file SHA-256
canonical inventory digest
schema/version identity
```

The exact manifest bytes must be hashed.

---

# 16. DATASET SEAL

Required state before performance:

```text
DATASET_STATUS = SEALED
```

After sealing, forbidden:

```text
ADD_FILE
REMOVE_FILE
REPLACE_FILE
EDIT_FILE
CHANGE_WINDOW
CHANGE_SOURCE
FILTER_BY_MARKET_BEHAVIOUR
```

Any byte change creates a different dataset identity and invalidates the authorization binding.

---

# 17. PERFORMANCE BLINDNESS BEFORE SEAL

Before the dataset is sealed, prohibited observations include:

```text
strategy PnL
expectancy
win rate
largest winner
FLIP_FRACTION
top-1% concentration
top-5% concentration
LONG/SHORT profitability
calendar profitability
drawdown
```

These cannot influence dataset acceptance.

---

# 18. PERMITTED PRE-SEAL OBSERVATIONS

Only non-performance integrity information may be inspected:

```text
file presence
file hashes
schema
timestamp coverage
timestamp ordering
field availability
BID/ASK validity
gap inventory
file/row counts
source provenance
duplicate/raw corruption status
```

These observations determine technical admissibility, not strategy desirability.

---

# 19. ADMISSIBILITY VERDICTS

The dataset-selection stage may produce only:

```text
ADMISSIBLE
BLOCKED_SOURCE_IDENTITY
BLOCKED_INSTRUMENT_IDENTITY
BLOCKED_SCHEMA
BLOCKED_PROVENANCE
BLOCKED_WINDOW
BLOCKED_OVERLAP
BLOCKED_INTEGRITY
BLOCKED_UNSEALED
```

It may not produce:

```text
GOOD_DATASET
PROMISING_DATASET
PROFITABLE_PERIOD
FAVOURABLE_REGIME
```

---

# 20. E1 NON-OVERLAP

The independent evidence block must have zero evaluation overlap with E1.

E1 historical window:

```text
through 2026-05-24T23:59:59.963Z
```

Candidate first block, if adopted now:

```text
from 2026-10-01T00:00:00Z
```

Therefore:

```text
TEMPORAL_OVERLAP = 0
```

The unused interval between them does not become confirmatory evidence automatically.

---

# 21. E1 OOS CONTAMINATION

The exposed E1 OOS remains:

```text
HISTORICAL_MOTIVATION_ONLY
```

It cannot be merged into the new evidence block.

Forbidden:

```text
E1 + NEW BLOCK pooled primary verdict
threshold recalibration from E1
window selection based on E1-like market behaviour
```

---

# 22. NO MARKET-REGIME SELECTION

The first block is selected by time rule, not market behaviour.

Forbidden selection criteria:

```text
bull market
bear market
high volatility
low volatility
trend period
crisis period
AI boom
rate cycle
specific macro regime
```

These belong to HYPOTHESIS-01 and cannot control H2 evidence selection.

---

# 23. NO DIRECTIONAL SELECTION

The first block must include all admissible frozen strategy trades.

Forbidden primary filtering:

```text
LONG only
SHORT only
best direction
```

Directional asymmetry belongs to HYPOTHESIS-03.

---

# 24. CROSS-INSTRUMENT PATH

Cross-instrument evidence remains scientifically useful but is not the primary first block.

Status:

```text
CROSS_INSTRUMENT_EVIDENCE =
RETAINED_FOR_LATER_INDEPENDENT_BLOCK
```

It cannot be invoked automatically if the temporal block is:

```text
negative
insufficient
inconclusive
```

Doing so would create adaptive evidence shopping.

A cross-instrument block requires its own prior human authorization and frozen instrument-selection rule.

---

# 25. STRUCTURAL CLAIM

E1-TD-01 requires at least two independently preregistered blocks before any structural claim.

Therefore this first temporal block, even if:

```text
STRONG_TAIL_DEPENDENCE
```

can establish at most:

```text
TAIL_DEPENDENCE_SUPPORTED_ON_THIS_BLOCK
```

not:

```text
STRUCTURAL_TAIL_DEPENDENCE_CONFIRMED
```

---

# 26. DATA ACQUISITION STATUS

This contract does not itself authorize data acquisition or observation.

Current status:

```text
DATA_ACQUISITION = NOT_AUTHORIZED
DATASET_BUILD = NOT_AUTHORIZED
H1_BUILD = NOT_AUTHORIZED
PERFORMANCE_EXECUTION = NOT_AUTHORIZED
```

Those require later explicit authority.

---

# 27. PREREGISTERED BREAKER FAMILIES

Future qualification must detect at minimum:

```text
PRE_ADOPTION_DATA_AS_PROSPECTIVE
TEMPORAL_OVERLAP
WINDOW_SHIFT_AFTER_RESULT
WINDOW_EXTENSION_AFTER_RESULT
RUN_UNTIL_100_TRADES
SOURCE_SUBSTITUTION
INSTRUMENT_SUBSTITUTION
SCHEMA_MUTATION
UNSEALED_DATASET
POST_SEAL_FILE_MUTATION
PERFORMANCE_PEEK_BEFORE_SEAL
REGIME_BASED_WINDOW_SELECTION
DIRECTIONAL_SUBGROUP_SELECTION
CROSS_INSTRUMENT_FALLBACK_SHOPPING
PRE_WINDOW_WARMUP_LEAKAGE
E1_OOS_MERGE
```

---

# 28. EXPECTED TESTABILITY CASES

```text
IE-01  exact TD-01 binding
IE-02  prospective temporal mode frozen
IE-03  USTECH identity frozen
IE-04  adoption precedes evidence-window start
IE-05  12-calendar-month window frozen
IE-06  zero E1 temporal overlap
IE-07  pre-window warmup forbidden
IE-08  initial position zero
IE-09  Source-B continuation required or explicit block
IE-10  raw BID/ASK schema exact
IE-11  source-order/no-repair rules exact
IE-12  >60s continuity boundary exact
IE-13  H1 derivation semantics unchanged
IE-14  dataset manifest contains required provenance
IE-15  all files SHA-256 sealed
IE-16  post-seal byte mutation invalidates identity
IE-17  strategy-performance peek before seal blocked
IE-18  regime-based selection blocked
IE-19  LONG/SHORT selection blocked
IE-20  n<100 does not extend window
IE-21  cross-instrument automatic fallback blocked
IE-22  no execution authority exposed
```

---

# 29. STATE IF ADOPTED

If adopted on 2026-09-29:

```text
INDEPENDENCE_MODE =
PROSPECTIVE_TEMPORAL_SAME_INSTRUMENT

INSTRUMENT =
USTECH

EVIDENCE_WINDOW =
[2026-10-01T00:00:00Z,
 2027-10-01T00:00:00Z)

WINDOW_DURATION =
12 CALENDAR MONTHS

SOURCE_POLICY =
SOURCE_B_CONTINUATION_OR_BLOCK

MINIMUM_CLOSED_TRADES =
100

ADAPTIVE_WINDOW_EXTENSION =
FORBIDDEN

PERFORMANCE_PEEK_BEFORE_SEAL =
FORBIDDEN

DATASET =
NOT_YET_MATERIALIZED

DATA_ACQUISITION =
NOT_AUTHORIZED

BACKTEST =
NOT_AUTHORIZED
```

---

# 30. NEXT FRONTIER IF ADOPTED

The next possible frontier becomes:

```text
E1-TD-03
PROSPECTIVE DATA ACQUISITION
+ DATASET IDENTITY / SEALING CONTRACT
```

Its purpose would be to define how future USTECH data may be collected, verified and sealed without observing strategy performance.

It would still not authorize the H2 backtest itself.

---

# 31. STOP

```text
CONTRACT_STATUS = CANDIDATE
HUMAN_ADOPTION = PENDING

GITHUB_PERSISTENCE = NOT_AUTHORIZED
DATA_ACQUISITION = NOT_AUTHORIZED
NEW_DATA_OBSERVATION = NOT_AUTHORIZED
BACKTEST = NOT_AUTHORIZED

STOP = TRUE
```
