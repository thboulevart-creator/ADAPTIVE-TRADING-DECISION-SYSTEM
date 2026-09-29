# E1-TD-03 — PROSPECTIVE DATA ACQUISITION + DATASET IDENTITY / SEALING CONTRACT V0.1

## 0. STATUS

```text
SCHEMA =
ATDS_E1_TD_03_PROSPECTIVE_DATA_ACQUISITION_DATASET_IDENTITY_SEALING_CONTRACT_V0_1

CONTROL_ID = E1-TD-03

STATUS = CANDIDATE_AWAITING_HUMAN_ADOPTION

MODE =
DOCUMENTARY / READ-ONLY / PREREGISTRATION
```

Canonical repository state reviewed:

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

HEAD =
f4f47bbfe6a94b546b5ac7c7844673b53cc6e047

TREE =
020a24d6ce66edce167b0eb077c05a3b5219c6d6
```

---

# 1. PROTECTED RESEARCH BINDINGS

```text
E1_TD_01_CONTRACT_BLOB =
ba7671c24ce0cb8943169bd2be9701d48f41da76

E1_TD_01_HUMAN_ADOPTION_BLOB =
7051bc817696f7bc6fe0b74ae45c7f7436f45829

E1_TD_02_CONTRACT_BLOB =
9dac95f502a34c61c58d1a508fd7a21082422d1f

E1_TD_02_HUMAN_ADOPTION_BLOB =
60b404a6acd39703d30455638e87ee8ef064d809
```

These objects are protected dependencies.

E1-TD-03 cannot modify their research question, thresholds, evidence window, independence mode or admissibility rules.

---

# 2. LEGACY SOURCE-B LINEAGE ANCHORS

Historical Source-B identity:

```text
SOURCE_B_PARENT_DATASET_ID =
SOURCE_B_USTECH_PRICE_CORE_V0_1

SOURCE_B_PARENT_MANIFEST_SHA256 =
c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5

SOURCE_B_PARENT_INVENTORY_DIGEST =
5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf

SOURCE_B_PARENT_SCHEMA_SIGNATURE =
c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d
```

Historical qualification bindings:

```text
F0 =
5bbe977688ec65ba6196115b3c0a7cfcd3a70ed4b8ff5afe9b6a96d470fcfa9b

F1 =
2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067

F2 =
6484784faf7c77d1ba8b6d7f007ee8498ad085c4beef58a21be71898e767cb29
```

Historical Source-B facts:

```text
files = 212
ticks = 376003618
bytes = 3936721231

required price fields =
timestamp
bid_price
ask_price
```

These historical counts are lineage facts only.

They are not expected counts for the prospective corpus.

---

# 3. AUTHORITY OF THIS CONTRACT

This contract defines only the future acquisition and sealing protocol.

It may define:

```text
PROVENANCE_REQUIREMENTS
ACQUISITION_PROTOCOL
RAW_OBJECT_IDENTITY
COLLECTION_LEDGER
DATASET_IDENTITY
MANIFEST_SCHEMA
CANONICAL_DIGEST_RULES
SEALING_RULES
INTEGRITY_CHECKS
PERFORMANCE_BLINDNESS
BREAKER_FAMILIES
PASS_FAIL_BLOCKED_RULES
STOP_BOUNDARIES
```

It does not authorize execution.

Current authority remains:

```text
ACTUAL_DATA_ACQUISITION = FALSE
NEW_DATA_OBSERVATION = FALSE
DATASET_MATERIALIZATION = FALSE
DATASET_BUILD = FALSE
H1_BUILD = FALSE
MOMENTUM_EXECUTION = FALSE
PERFORMANCE_COMPUTATION = FALSE
BACKTEST = FALSE
```

---

# 4. FROZEN EVIDENCE TARGET

```text
INDEPENDENCE_MODE =
PROSPECTIVE_TEMPORAL_SAME_INSTRUMENT

ECONOMIC_INSTRUMENT =
USTECH

EVIDENCE_WINDOW =
[2026-10-01T00:00:00Z,
 2027-10-01T00:00:00Z)

WINDOW_DURATION =
12 CALENDAR MONTHS

SOURCE_POLICY =
SOURCE_B_CONTINUATION_OR_BLOCK
```

No part of E1-TD-03 may shift, shorten or extend this window.

---

# 5. RESERVED FUTURE DATASET IDENTITY

The future dataset identity is reserved as:

```text
DATASET_ID =
SOURCE_B_USTECH_TD01_PROSPECTIVE_20261001_20271001_V0_1
```

Current status:

```text
DATASET_ID_STATUS =
RESERVED_NOT_MATERIALIZED
```

Reservation of the identifier does not establish that the dataset exists, is available, is complete or is admissible.

---

# 6. SOURCE-B PROVENANCE GATE

Current governed repository evidence establishes Source-B cryptographic identity but does not, in the reviewed records, establish a literal external provider identifier sufficient for a new acquisition.

Therefore:

```text
SOURCE_B_EXTERNAL_PROVIDER_IDENTITY =
UNRESOLVED_FROM_REVIEWED_GOVERNED_RECORDS

SOURCE_B_PROVENANCE_GATE =
PENDING
```

Before any actual acquisition:

```text
SOURCE_B_PROVENANCE_GATE = PASS
```

must be established.

Acceptable evidence must identify, without ambiguity:

```text
provider / source lineage
data product or export mechanism
economic instrument mapping
provider-side symbol/instrument identifier
timestamp semantics
BID semantics
ASK semantics
data resolution
acquisition/export mechanism
relationship to historical SOURCE_B_USTECH_PRICE_CORE_V0_1
```

Secrets, passwords, API tokens and credentials must never be persisted in governance evidence.

If historical provenance cannot be established:

```text
STATUS =
BLOCKED_SOURCE_PROVENANCE
```

A dataset with merely similar columns or the label `USTECH` is insufficient.

---

# 7. NO AUTOMATIC SOURCE SUBSTITUTION

The following do not automatically qualify as Source-B continuation:

```text
another CFD provider
another NAS100 symbol
NASDAQ-100 cash index
NQ
MNQ
QQQ
reconstructed synthetic prices
mid-price-only data
single-price OHLC data
```

If Source-B continuation is unavailable:

```text
SOURCE_CONTINUITY_UNAVAILABLE = BLOCKED
```

A different source requires a separately governed source-equivalence qualification.

---

# 8. ACQUISITION ARCHITECTURE

Future collection must produce four logically separate evidence layers:

```text
LAYER_1 =
ORIGINAL RAW ACQUISITION OBJECTS

LAYER_2 =
APPEND-ONLY ACQUISITION LEDGER

LAYER_3 =
FINAL CANONICAL DATASET MANIFEST

LAYER_4 =
FINAL DATASET SEAL
```

No H1 or strategy output belongs to these layers.

---

# 9. ORIGINAL RAW OBJECT POLICY

Every acquired source object must be preserved byte-for-byte.

Immediately after acquisition, before transformation:

```text
SHA256(original_bytes)
size_bytes
acquired_at_utc
source_request_identity
```

must be recorded.

Forbidden:

```text
REENCODE
REWRITE
SORT
DEDUPLICATE
INTERPOLATE
FORWARD_FILL
NORMALIZE_PRICES
REPAIR_TIMESTAMPS
SILENT_SCHEMA_CONVERSION
```

The acquisition archive is immutable evidence.

---

# 10. PHYSICAL FILE LAYOUT MUST NOT DEFINE EVIDENCE SELECTION

The provider may deliver:

```text
daily files
weekly files
monthly files
arbitrary chunks
bulk exports
```

Physical provider chunking is not a research decision.

No performance-conditioned chunking is allowed.

If a provider object contains rows both inside and outside the evidence window, its original bytes remain unchanged in the acquisition archive.

Evaluation eligibility is later defined only by:

```text
2026-10-01T00:00:00Z
<= timestamp
<
2027-10-01T00:00:00Z
```

Out-of-window rows cannot become evaluation evidence.

---

# 11. REQUIRED RAW SEMANTICS

The prospective Source-B continuation must provide semantics compatible with:

```text
timestamp
bid_price
ask_price
```

The exact source schema must either:

```text
MATCH HISTORICAL SOURCE-B SEMANTICS
```

or be separately qualified as equivalent before acceptance.

A superficial rename is not sufficient evidence of equivalence.

---

# 12. SOURCE ORDER

Source order remains authoritative.

Forbidden:

```text
SORT_TO_REPAIR
```

The prospective corpus must permit a deterministic source ordering.

Within that governed ordering, timestamp defects must be surfaced rather than silently corrected.

---

# 13. GAP SEMANTICS

Existing continuity semantics remain protected:

```text
current_timestamp_ms - previous_timestamp_ms > 60000
→ FORBIDDEN_BOUNDARY

exactly 60000 ms
→ CONTINUITY_OK
```

Large gaps are not automatically acquisition failures.

They must be recorded.

A gap may represent:

```text
market inactivity
provider inactivity
missing source coverage
technical acquisition failure
```

The acquisition layer must not infer which explanation applies without evidence.

---

# 14. ACQUISITION REQUEST COVERAGE

Every intended collection interval must have a corresponding acquisition record.

For each interval:

```text
REQUESTED_INTERVAL
SOURCE_REQUEST_ID
REQUEST_TIMESTAMP
ACQUISITION_STATUS
RETURNED_OBJECT_IDENTITIES
```

must be known.

Unaccounted requested intervals are forbidden.

If an interval cannot be acquired:

```text
COVERAGE_STATUS =
UNRESOLVED
```

and final sealing is blocked until adjudicated.

---

# 15. NETWORK / DOWNLOAD RETRIES

A failed network request may be retried only as a data-acquisition operation.

Retries must not be silent.

Each attempt must receive a ledger event.

Before an object has been accepted:

```text
RETRY = PERMITTED_AND_LOGGED
```

After an object's exact bytes have been accepted and registered:

```text
SILENT_REPLACEMENT = FORBIDDEN
```

If the provider later supplies different bytes for the same logical source object:

```text
SOURCE_REVISION_DETECTED
→ BLOCKED_FOR_HUMAN_ADJUDICATION
```

No automatic overwrite is allowed.

---

# 16. APPEND-ONLY ACQUISITION LEDGER

Each acquisition event must contain at minimum:

```text
event_sequence
event_timestamp_utc
previous_event_digest
event_type
provider_lineage_id
instrument_id
source_request_id
requested_start_utc
requested_end_utc
object_relative_path
object_sha256
object_size_bytes
parse_status
row_count
first_timestamp_ms
last_timestamp_ms
schema_signature
event_status
```

No strategy or PnL field is allowed.

Each event receives a canonical SHA-256 digest.

The next event binds:

```text
previous_event_digest =
prior_event_digest
```

forming an append-only hash chain.

---

# 17. LEDGER EVENT TYPES

Allowed event types:

```text
ACQUISITION_REQUEST
ACQUISITION_FAILURE
OBJECT_RECEIVED
OBJECT_ACCEPTED
OBJECT_REJECTED
SOURCE_REVISION_DETECTED
FINAL_COVERAGE_CHECK
```

Forbidden event types include:

```text
PNL_CHECK
STRATEGY_CHECK
REGIME_CHECK
TRADE_COUNT_PEEK
PERFORMANCE_SCREEN
```

---

# 18. PERMITTED ACQUISITION-TIME INSPECTION

Only integrity/provenance inspection is permitted.

Allowed:

```text
file presence
byte size
SHA-256
schema
column presence
timestamp coverage
timestamp ordering
row counts
BID/ASK field validity
gap inventory
source provenance
request coverage
duplicate/raw-corruption diagnosis
```

Raw price fields may be parsed only where necessary for these integrity checks.

---

# 19. FORBIDDEN PRE-SEAL INSPECTION

Before final sealing, forbidden:

```text
MOMENTUM_V1 execution
signal generation
trade generation
PnL
expectancy
win rate
drawdown
largest strategy winner
FLIP_FRACTION
top-1%-winner concentration
top-5%-winner concentration
LONG/SHORT profitability
calendar profitability
regime profitability
H1 strategy preview
```

No acquisition decision may depend on such information.

---

# 20. H1 BUILD BOUNDARY

The acquisition phase may not construct the governed H1 strategy input.

```text
H1_BUILD_BEFORE_RAW_DATASET_SEAL =
FORBIDDEN
```

The raw dataset must first receive a final sealed identity.

Only a later governed frontier may authorize:

```text
SEALED_RAW
→ M1/AP0
→ H1
```

---

# 21. INCLUSION RULE

The final logical evidence corpus must contain:

```text
ALL ADMISSIBLE SOURCE-B RECORDS
whose timestamp satisfies:

2026-10-01T00:00:00Z
<= timestamp
<
2027-10-01T00:00:00Z
```

No other market-behaviour filter is permitted.

Forbidden:

```text
REMOVE_BAD_MARKET_PERIOD
REMOVE_HIGH_SPREAD_PERIOD
REMOVE_LOW_VOLATILITY_PERIOD
REMOVE_NEWS_PERIOD
REMOVE_LOSING_PERIOD
SELECT_TRENDING_PERIOD_ONLY
```

---

# 22. DATA QUALITY IS NOT PERFORMANCE QUALITY

Dataset acceptance may depend on:

```text
PROVENANCE
SCHEMA
BYTE_INTEGRITY
TIMESTAMP_INTEGRITY
COVERAGE
SOURCE_CONTINUITY
```

It may not depend on:

```text
WHETHER MOMENTUM WOULD WIN
WHETHER MARKET WAS TRENDING
WHETHER LARGE WINNERS OCCURRED
```

---

# 23. FINAL MANIFEST SCHEMA

The final dataset manifest must contain at minimum:

```text
schema
dataset_id
status

parent_source_dataset_id
parent_source_manifest_sha256
parent_source_inventory_digest
parent_source_schema_signature

provenance_record

economic_instrument
provider_instrument_identifier
source_semantics

logical_window_start_utc
logical_window_end_utc

required_fields
forbidden_repairs

file_count
total_rows
total_bytes

first_observed_timestamp_ms
last_observed_timestamp_ms

gap_gt_60000ms_count

files[]

canonical_inventory_digest

acquisition_ledger_final_digest

runtime_environment
created_at_utc
```

---

# 24. FILE RECORD SCHEMA

Each `files[]` record must contain exactly the governed equivalent of:

```text
relative_path
sha256
size_bytes
rows
first_timestamp_ms
last_timestamp_ms
schema_signature
source_request_id
```

`relative_path` is the canonical path field.

The historical E1-03 failure involving `path` versus `relative_path` must not be repeated.

---

# 25. CANONICAL SERIALIZATION

For E1-TD-03 governance objects containing only JSON-safe finite values:

```text
encoding = UTF-8
key ordering = lexical ascending
JSON separators = "," and ":"
insignificant whitespace = NONE
NaN / Infinity = FORBIDDEN
terminal newline = ONE LF
```

Equivalent Python reference semantics:

```text
json.dumps(
    payload,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
    allow_nan=False,
).encode("utf-8") + b"\n"
```

This definition is part of the contract.

---

# 26. CANONICAL INVENTORY DIGEST

The inventory payload contains:

```text
schema
dataset_id
logical_window
files[]
```

`files[]` must be sorted by:

```text
relative_path ascending
```

Duplicate `relative_path` values are forbidden.

Then:

```text
CANONICAL_INVENTORY_DIGEST =
SHA256(canonical_inventory_payload_bytes)
```

The ordering cannot be changed after data observation.

---

# 27. FINAL MANIFEST HASH

Once all manifest fields are complete:

```text
MANIFEST_SHA256 =
SHA256(exact canonical manifest bytes)
```

The manifest must not contain its own `MANIFEST_SHA256`, avoiding self-reference.

The manifest hash is stored in the separate seal record.

---

# 28. DATASET SEAL RECORD

A separate seal record must contain:

```text
schema =
ATDS_E1_TD_03_DATASET_SEAL_V0_1

dataset_id
manifest_sha256
canonical_inventory_digest
acquisition_ledger_final_digest

logical_window_start_utc
logical_window_end_utc

file_count
total_rows
total_bytes

provenance_status
coverage_status
integrity_status

performance_peek_before_seal = FALSE
h1_built_before_seal = FALSE
momentum_executed_before_seal = FALSE
pnl_observed_before_seal = FALSE

sealed_at_utc
human_authority_reference
```

---

# 29. CONDITIONS REQUIRED FOR SEALED

The final state:

```text
DATASET_STATUS = SEALED
```

is allowed only when all are true:

```text
WINDOW_HAS_ENDED = TRUE

SOURCE_B_PROVENANCE_GATE = PASS

INSTRUMENT_IDENTITY = PASS

REQUEST_COVERAGE = PASS

RAW_OBJECT_HASHES = PASS

SCHEMA = PASS

TIMESTAMP_INTEGRITY = PASS

CANONICAL_INVENTORY = PASS

MANIFEST_CANONICALIZATION = PASS

PERFORMANCE_BLINDNESS = PASS

H1_NOT_BUILT = PASS

STRATEGY_NOT_EXECUTED = PASS
```

Otherwise:

```text
DATASET_STATUS != SEALED
```

---

# 30. SEAL CANNOT OCCUR EARLY

For the adopted evidence window:

```text
FINAL_SEAL_BEFORE_2027-10-01T00:00:00Z =
FORBIDDEN
```

Interim raw objects may be individually hashed and frozen.

But the complete evidence dataset cannot be declared complete before the logical window ends.

---

# 31. POST-SEAL IMMUTABILITY

After final sealing, forbidden:

```text
ADD_FILE
REMOVE_FILE
REPLACE_FILE
EDIT_FILE
CHANGE_ROW
CHANGE_WINDOW
CHANGE_SOURCE
CHANGE_INSTRUMENT
CHANGE_SCHEMA
REWRITE_MANIFEST
```

Any byte-level change invalidates the seal.

The changed corpus becomes:

```text
NEW_DATASET_IDENTITY
```

and requires new human adjudication.

No in-place resealing is permitted.

---

# 32. SOURCE REVISION AFTER SEAL

If a provider later changes historical bytes:

```text
ORIGINAL_SEALED_DATASET =
PRESERVED
```

The replacement may be recorded separately as:

```text
SOURCE_REVISION_CANDIDATE
```

It must not silently replace the evidence already sealed.

---

# 33. PERFORMANCE BLIND COLLECTOR

Any future acquisition/identity runtime must be technically incapable of calculating strategy performance.

It must not import or delegate to:

```text
MOMENTUM_V1 runner
E1-05 runner
E1-08 executor
PnL evaluator
tail-dependence evaluator
strategy signal engine
```

Its authority surface is limited to:

```text
ACQUIRE
HASH
INVENTORY
VALIDATE
LEDGER
MANIFEST
SEAL
```

---

# 34. COLLECTOR OUTPUT PROHIBITIONS

The acquisition runtime must not output:

```text
signal
position
trade
PnL
expectancy
drawdown
win_rate
largest_winner
FLIP_FRACTION
tail-dependence verdict
```

Presence of such a field is a contract violation.

---

# 35. ADMISSIBILITY / FAILURE STATES

Allowed non-performance statuses:

```text
PASS_PROVENANCE
PASS_OBJECT_INTEGRITY
PASS_COLLECTION_EVENT
PASS_COVERAGE
SEALED

BLOCKED_SOURCE_PROVENANCE
BLOCKED_SOURCE_CONTINUITY
BLOCKED_INSTRUMENT_IDENTITY
BLOCKED_SCHEMA
BLOCKED_REQUEST_COVERAGE
BLOCKED_RAW_OBJECT_HASH
BLOCKED_TIMESTAMP_INTEGRITY
BLOCKED_SOURCE_REVISION
BLOCKED_MANIFEST
BLOCKED_INVENTORY_DIGEST
BLOCKED_PERFORMANCE_PEEK
BLOCKED_PREMATURE_H1_BUILD
BLOCKED_PREMATURE_STRATEGY_EXECUTION
BLOCKED_POST_SEAL_MUTATION
```

Forbidden status language:

```text
GOOD_PERIOD
PROMISING_DATA
FAVOURABLE_MARKET
PROFITABLE_WINDOW
```

---

# 36. PREREGISTERED BREAKER FAMILIES

The future qualification surface must at minimum attempt to break:

```text
B01  wrong TD-01 binding
B02  wrong TD-02 binding
B03  wrong evidence window
B04  unresolved Source-B provenance
B05  provider substitution
B06  instrument substitution
B07  missing required BID/ASK field
B08  raw byte mutation
B09  silent file replacement
B10  duplicate canonical relative_path
B11  source-order repair by sorting
B12  timestamp repair
B13  interpolation / forward-fill
B14  missing acquisition interval
B15  silent network retry
B16  unlogged source revision
B17  malformed ledger hash chain
B18  inventory order manipulation
B19  manifest canonicalization mismatch
B20  seal before window end
B21  H1 build before raw seal
B22  Momentum import or execution
B23  PnL/performance field emitted
B24  performance-conditioned file exclusion
B25  post-seal byte mutation
B26  post-seal manifest rewrite
B27  ungoverned reseal
B28  E1 data merged into prospective corpus
B29  rows outside logical window treated as evaluation rows
B30  unknown manifest field affecting identity
```

---

# 37. EXPECTED TEST-FIRST CASES

Before real acquisition is ever authorized, a synthetic qualification should cover at minimum:

```text
TD03-01  exact contract bindings
TD03-02  reserved dataset ID exact
TD03-03  evidence window exact
TD03-04  provenance unresolved → BLOCKED
TD03-05  valid synthetic provenance → PASS
TD03-06  provider substitution → BLOCKED
TD03-07  instrument substitution → BLOCKED
TD03-08  exact-byte SHA verification
TD03-09  mutated byte → BLOCKED
TD03-10  duplicate path → BLOCKED
TD03-11  missing required field → BLOCKED
TD03-12  non-monotone source ordering → BLOCKED
TD03-13  >60s gap recorded without repair
TD03-14  exactly 60s preserves continuity
TD03-15  missing acquisition interval → BLOCKED
TD03-16  retry is ledger-visible
TD03-17  accepted-object replacement → BLOCKED
TD03-18  acquisition-ledger hash chain exact
TD03-19  deterministic inventory digest
TD03-20  file-order permutation cannot change canonical inventory
TD03-21  one file hash mutation changes inventory
TD03-22  deterministic canonical manifest
TD03-23  premature seal → BLOCKED
TD03-24  strategy import → BLOCKED
TD03-25  PnL field → BLOCKED
TD03-26  H1 output before seal → BLOCKED
TD03-27  performance-based file filtering → BLOCKED
TD03-28  post-seal mutation invalidates dataset
TD03-29  seal binds manifest + inventory + ledger
TD03-30  collector exposes no backtest path
```

---

# 38. FROZEN NO-REPAIR POLICY

The prospective dataset retains the ATDS fail-closed principle:

```text
NO_SILENT_DATA_CORRECTION
```

A defect is:

```text
RECORDED
BOUNDED
OR BLOCKING
```

not silently repaired.

---

# 39. MINIMUM-TRADE RULE REMAINS OUTSIDE ACQUISITION

The acquisition layer may never inspect whether the final period produces:

```text
>= 100 CLOSED TRADES
```

That rule is evaluated only in the future performance experiment.

Therefore:

```text
TRADE_COUNT_DURING_ACQUISITION =
FORBIDDEN_TO_COMPUTE
```

The data window remains fixed regardless.

---

# 40. ACQUISITION TIMING AND PROSPECTIVENESS

Prospective independence is defined by:

```text
research question frozen before window
metrics frozen before window
evidence window frozen before window
no performance peek
no adaptive window change
```

It does not require every tick to be downloaded in real time.

Therefore acquisition may technically be:

```text
incremental during the window
OR
provider-archival retrieval after observations occurred
```

provided all Source-B continuity, provenance, completeness and blindness requirements are satisfied.

No later retrieval may be selected based on knowledge of MOMENTUM_V1 performance.

---

# 41. NO AUTOMATIC USE OF FUTURE DATA

Possession of the sealed dataset will not itself authorize:

```text
AP0/M1 BUILD
H1 BUILD
MOMENTUM_V1
TRADE GENERATION
PNL
TAIL-DEPENDENCE ANALYSIS
BACKTEST
```

Data authority and performance authority remain separate.

---

# 42. FORBIDDEN CLAIMS

E1-TD-03 cannot establish:

```text
TAIL_DEPENDENCE_SUPPORTED
TAIL_DEPENDENCE_REFUTED
EDGE_CONFIRMED
STRATEGY_QUALIFIED
ROBUST
PROFITABLE
BROKER_NET_PNL
LIVE_READY
```

It establishes only evidence provenance and identity.

---

# 43. STATE IF HUMANLY ADOPTED

```text
E1_TD_03_CONTRACT = ADOPTED

PROSPECTIVE_DATASET_ID =
SOURCE_B_USTECH_TD01_PROSPECTIVE_20261001_20271001_V0_1

PROSPECTIVE_DATASET_ID_STATUS =
RESERVED_NOT_MATERIALIZED

SOURCE_B_PROVENANCE_GATE =
PENDING

EVIDENCE_WINDOW =
[2026-10-01T00:00:00Z,
 2027-10-01T00:00:00Z)

RAW_ARCHIVE_POLICY = FROZEN
ACQUISITION_LEDGER_SCHEMA = FROZEN
MANIFEST_SCHEMA = FROZEN
CANONICALIZATION_RULE = FROZEN
INVENTORY_DIGEST_RULE = FROZEN
SEALING_RULE = FROZEN
POST_SEAL_IMMUTABILITY = FROZEN
PERFORMANCE_BLINDNESS = FROZEN
```

But:

```text
ACTUAL_DATA_ACQUISITION = NOT_AUTHORIZED
NEW_DATA_OBSERVATION = NOT_AUTHORIZED
DATASET_MATERIALIZATION = NOT_AUTHORIZED
H1_BUILD = NOT_AUTHORIZED
MOMENTUM_EXECUTION = NOT_AUTHORIZED
BACKTEST = NOT_AUTHORIZED
```

---

# 44. NEXT GOVERNED FRONTIER IF ADOPTED

The next boundary should be:

```text
E1-TD-03A
SOURCE-B PROVENANCE RECOVERY
+ ACQUISITION COLLECTOR TEST-FIRST QUALIFICATION
```

That frontier would be allowed to:

```text
recover/verify historical Source-B provenance
design the minimal collector runtime
persist synthetic breakers first
qualify hashing / ledger / manifest / sealing logic
```

using synthetic fixtures only unless separately authorized.

It still would not automatically authorize real acquisition.

If the provenance gate cannot be closed:

```text
E1-TD-03A = BLOCKED
```

and the system must stop rather than substitute a source.

---

# 45. CURRENT STOP

```text
E1_TD_03_CONTRACT = CANDIDATE
HUMAN_ADOPTION = REQUIRED

GITHUB_PERSISTENCE = NOT_AUTHORIZED

ACTUAL_DATA_ACQUISITION = NOT_AUTHORIZED
NEW_DATA_OBSERVATION = NOT_AUTHORIZED
DATASET_MATERIALIZATION = NOT_AUTHORIZED
DATASET_BUILD = NOT_AUTHORIZED
H1_BUILD = NOT_AUTHORIZED
MOMENTUM_EXECUTION = NOT_AUTHORIZED
PERFORMANCE_COMPUTATION = NOT_AUTHORIZED
BACKTEST = NOT_AUTHORIZED

STOP = TRUE
```
