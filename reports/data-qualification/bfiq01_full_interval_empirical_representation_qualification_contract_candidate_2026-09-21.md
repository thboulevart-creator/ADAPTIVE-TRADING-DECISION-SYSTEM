# B-FIQ-01 — FULL_INTERVAL_QUALIFIED EMPIRICAL REPRESENTATION-QUALIFICATION CONTRACT — CANDIDATE

Date: 2026-09-21  
Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
Branch: integration/system-v1  
Starting HEAD: 07545f5b00d8879ca2df935a21b9eb10fb96c67b  
Status: PERSISTED FORMALIZATION CANDIDATE — NOT YET QUALIFIED

## 0. Permission boundary

B-FIQ-01 formalizes the future exhaustive qualification only.

Still prohibited:

~~~text
new full-domain BI5 download
FULL_INTERVAL qualification execution
massive project acquisition
D materialization
real Q/F/Q-RM-12 full execution
backtest
paper/broker/live
positive P1.1 authorization
~~~

No provider request may occur in B-FIQ-01.

Historical documentary state remains unchanged:

~~~text
C08-D4-DOC = BLOCKED
C08-D5-DOC = BLOCKED
BPE-C08 V0.1 = BLOCKED
~~~

Prospective operational state remains:

~~~text
C08-D4-OP = NOT YET PASS
C08-D5-OP = NOT YET PASS
BPE-C08-OP-V0.2 = NOT YET PASS
~~~

## 1. Contract identity and purpose

~~~text
contract_id =
B_FIQ_01_USATECH_FULL_INTERVAL_EMPIRICAL_REPRESENTATION_QUALIFICATION

contract_version =
B_FIQ_01_USATECH_FULL_INTERVAL_EMPIRICAL_REPRESENTATION_QUALIFICATION_V0_1_CANDIDATE
~~~

Purpose:

qualify, for the operational historical-backtest pipeline, whether the exact provider archive material selected by the project is exhaustively classifiable across the complete governed USATECH representation domain under current-authority representation semantics.

This contract implements VERSIONED_EMPIRICAL_SUPERSESSION authorized by B-PE-01R.

It does not alter B-PE-01 V0.1 documentary truth.

## 2. Exact FULL_D_REPRESENTATION_DOMAIN construction

Frozen inputs:

~~~text
instrument = USATECHIDXUSD

execution_window_freeze =
04-REFERENCE/EXECUTION-WINDOW-FREEZE.json
blob bf7c43e9d90d952dfa3715c28575fdf6cf379a89

first_included_open_slot_utc =
2021-08-15T22:00:00Z

last_included_open_slot_utc =
2026-08-14T20:00:00Z

warmup_h1_bars =
20

session_calendar =
DUKASCOPY_USATECH_SESSION_CALENDAR_V3
tools/dukascopy_usatech_calendar.py
blob fab634aab7b8c299b0139c3c43bf5b89a2aa03d0
~~~

### 2.1 Evaluation-open set

~~~text
EVALUATION_OPEN_SET =
every UTC H1 slot S such that:

first_included_open_slot_utc <= S <= last_included_open_slot_utc

AND

classify_slot(date(S), hour(S)).status == EXPECTED_OPEN
~~~

### 2.2 Warmup-open set

Let P be the strictly ordered sequence of UTC H1 slots before first_included_open_slot_utc for which the same current-authority session calendar returns EXPECTED_OPEN.

~~~text
WARMUP_OPEN_SET =
the final exactly 20 members of P
~~~

The warmup start is derived, not guessed.

### 2.3 Wall-clock inventory envelope

~~~text
full_domain_first_h1 = min(WARMUP_OPEN_SET)
full_domain_last_h1  = last_included_open_slot_utc

FULL_D_REPRESENTATION_DOMAIN =
every UTC-aligned H1 slot
from full_domain_first_h1
through full_domain_last_h1 inclusive
~~~

Every wall-clock H1 in that envelope is represented in the inventory.

No hour may disappear because it is weekend, break, holiday, missing, unavailable, empty or inconvenient.

### 2.4 Required-provider-component predicate

For each interval:

~~~text
expected_market_status =
classify_slot(date(interval_start_utc), hour(interval_start_utc)).status
~~~

Then:

~~~text
EXPECTED_OPEN
→ provider_component_requirement = REQUIRED

EXPECTED_CLOSED
→ provider_component_requirement = NOT_REQUIRED_CALENDAR_CLOSED
~~~

A calendar-closed H1 is explicitly present in the inventory and never treated as a downloaded empty object.

Any other calendar status:

~~~text
→ INVENTORY_BUILD_BLOCKED
~~~

## 3. IntervalInventory — closed pre-request artifact

Future execution requires:

~~~text
schema =
B_FIQ_01_INTERVAL_INVENTORY_V0_1

inventory_id
contract_id
contract_version

provider_identity
instrument_identity

execution_window_freeze_identity
warmup_rule_identity
session_calendar_identity

full_domain_first_h1
full_domain_last_h1

wall_clock_interval_count
expected_open_interval_count
expected_closed_interval_count

intervals[]
  interval_ordinal
  interval_id
  interval_start_utc
  interval_end_utc
  expected_market_status
  calendar_reason
  calendar_schedule
  provider_component_requirement

created_at_utc
interval_inventory_root
inventory_seal
~~~

Rules:

- interval_ordinal is contiguous from zero;
- interval order is strictly ascending UTC start;
- interval width is exactly PT1H;
- adjacent inventory intervals differ by exactly one hour;
- first/last match derived domain bounds;
- counts exactly match the interval list;
- warmup-open cardinality is exactly 20;
- evaluation-open first/last match the freeze;
- duplicate/missing interval IDs are invalid.

### 3.1 Interval identity

~~~text
interval_id =
SHA256(
  canonical_json({
    instrument_identity,
    interval_start_utc,
    interval_end_utc,
    execution_window_freeze_identity,
    session_calendar_identity,
    expected_market_status
  })
)
~~~

### 3.2 Inventory root

~~~text
interval_inventory_root =
SHA256(
  canonical_json(
    ordered list of exact interval records
  )
)
~~~

The inventory must be persisted and sealed before any provider request.

## 4. ProviderDeliveryIdentityPolicy

Future execution must freeze provider-delivery identity independently of DNS/runtime details.

~~~text
schema =
B_FIQ_01_PROVIDER_DELIVERY_IDENTITY_POLICY_V0_1

policy_id
provider_identity = DUKASCOPY

allowed_delivery_endpoints[]
  scheme
  hostname
  port
  endpoint_role

allowed_redirect_edges[]
  source_endpoint
  target_endpoint
  semantic_relation

tls_policy
http_version_policy
provider_identity_evidence_refs

created_at_utc
policy_seal
~~~

Rules:

- response from an endpoint outside the allowed set is BLOCKED;
- redirect outside a predeclared allowed edge is BLOCKED;
- DNS/IP changes alone do not change provider identity;
- host substitution after observation is prohibited;
- provider identity evidence must be pinned before execution.

## 5. RepresentationRegimeManifest / LocatorManifest

Future execution requires a sealed representation-regime manifest before any request.

~~~text
schema =
B_FIQ_01_REPRESENTATION_REGIME_MANIFEST_V0_1

manifest_id
contract_id
contract_version
provider_delivery_identity_policy_id
provider_delivery_identity_policy_seal

regimes[]
  regime_id
  representation_identity
  applicability_rule
  interval_domain_rule
  locator_rendering_rule
  locator_source_evidence_refs
  representation_semantic_authority_refs
  transition_boundary_evidence_refs_if_any

open_world_rule
created_at_utc
manifest_seal
~~~

Initial candidate execution may contain K1 only if K1 remains the selected predeclared operational rule.

No K2 or unknown family may be inserted after results are visible.

### 5.1 Locator determinism

For every EXPECTED_OPEN interval, the manifest must render exactly one candidate locator for its assigned regime before execution.

For EXPECTED_CLOSED intervals:

~~~text
locator = NONE
request_allowed = false
~~~

Duplicate locator assignment to distinct open intervals is invalid unless the regime contract explicitly proves shared-object semantics and deterministic interval projection.

## 6. TransportPolicy and request-volume constraints

Future execution requires one sealed transport policy or one sealed composite policy-set identity if sharding is used.

Hard ceilings for the first executable version:

~~~text
method = GET
automatic_retry_count = 0
automatic_content_decoding = false
Accept-Encoding = identity

max_parallel_requests <= 4
aggregate_request_start_rate <= 2 requests / second

connect_timeout_seconds <= 15
per_request_total_timeout_seconds <= 60

max_response_body_bytes <= 50 MiB
automatic_redirect_follow = false
~~~

No execution may loosen these ceilings without a new B-FIQ contract version.

### 6.1 RequestBudget

Before execution:

~~~text
planned_request_count =
count(intervals where provider_component_requirement == REQUIRED)
~~~

A sealed RequestBudget must bind:

~~~text
request_budget_id
planned_request_count
maximum_actual_request_count
max_parallel_requests
aggregate_request_start_rate
transport_policy_id
interval_inventory_root
regime_manifest_seal
budget_seal
~~~

For the first exhaustive execution:

~~~text
maximum_actual_request_count = planned_request_count
~~~

Therefore no automatic retry and no exploratory extra request are permitted.

## 7. ExecutionShardPlan

Because exhaustive qualification may exceed one runtime/job, sharding is allowed only when predetermined.

~~~text
schema =
B_FIQ_01_EXECUTION_SHARD_PLAN_V0_1

shard_plan_id
interval_inventory_root
request_budget_id

shards[]
  shard_id
  first_interval_ordinal
  last_interval_ordinal
  required_request_count
  worker_identity_rule

shard_order_policy
cross_shard_overlap_policy = FORBIDDEN
created_at_utc
shard_plan_seal
~~~

Rules:

- every REQUIRED interval belongs to exactly one shard;
- no REQUIRED interval belongs to multiple shards;
- no shard may add intervals after execution starts;
- worker/runtime partitioning has no semantic effect;
- an infrastructure interruption before any request for an interval may leave it unattempted;
- an interval with uncertain request outcome is BLOCKED, not silently rescheduled inside the same qualification lineage.

A changed shard plan requires a new execution lineage.

## 8. Per-interval execution state machine

Every inventory interval must end with exactly one closed disposition.

### 8.1 Calendar-closed intervals

If:

~~~text
expected_market_status = EXPECTED_CLOSED
~~~

then only:

~~~text
CALENDAR_CLOSED_NO_COMPONENT
~~~

is valid.

Requirements:

- no provider request was sent;
- current-authority session-calendar identity matches inventory;
- no runtime mutation of expected-market status occurred.

This is not QUALIFIED_EMPTY.

### 8.2 Expected-open intervals

Allowed terminal dispositions:

~~~text
QUALIFIED_OBJECT
QUALIFIED_EMPTY
REFUTED_SELECTED_REGIME
BLOCKED_TRANSPORT
BLOCKED_LOCATOR
BLOCKED_UNKNOWN_REPRESENTATION
BLOCKED_DIAGNOSTIC_DISAGREEMENT
BLOCKED_INTEGRITY
BLOCKED_UNCLASSIFIED
~~~

No other terminal state is valid.

## 9. QUALIFIED_OBJECT

An EXPECTED_OPEN interval may become QUALIFIED_OBJECT only if all are true:

~~~text
one predeclared locator was requested
HTTP/provider transport succeeded
non-empty exact response bytes were captured
compressed raw SHA-256 persisted
capture seal valid
assigned regime decoder admitted the payload
both independent diagnostics succeeded
both diagnostics agree on decompressed SHA-256
both diagnostics agree on projection SHA-256
both diagnostics agree on record count
all prequalified decisive invariants pass
no positive competing-representation contradiction is unresolved
~~~

A successful HTTP status alone is insufficient.

## 10. QUALIFIED_EMPTY boundary

QUALIFIED_EMPTY is reserved but disabled by default in B-FIQ-01.

It may be used only if, before the exhaustive execution, a separate current-authority empty-object rule is referenced by the authority scope tuple.

That rule must distinguish at least:

~~~text
legitimate open interval with zero provider ticks
provider convention for empty BI5/object
object missing
HTTP 404
zero-byte transport body
malformed compressed body
truncated body
market actually closed
provider archive gap
~~~

Until such a rule exists:

~~~text
EXPECTED_OPEN + no non-empty QUALIFIED_OBJECT
→ cannot become QUALIFIED_EMPTY
→ BLOCKED
~~~

No 404, zero bytes or successful empty decompression can self-qualify as empty.

## 11. Exact TransportCapture

Every attempted provider request must produce:

~~~text
schema =
B_FIQ_01_TRANSPORT_CAPTURE_V0_1

capture_id
execution_lineage_id
shard_id
interval_id
regime_id

request_started_at_utc
request_completed_at_utc
request_method
request_locator
request_header_evidence
transport_policy_id
transport_policy_seal

provider_delivery_endpoint_observed
redirect_chain

http_status
response_headers
raw_response_byte_length
raw_response_sha256
content_addressed_body_ref

transport_disposition
capture_seal
~~~

Credential-bearing secrets are never persisted.

If request authentication is later required, the evidence rule must persist a secret-safe normalized request identity that is separately qualified before use.

## 12. Dual independent diagnostics at full scale

Every non-empty response proposed for QUALIFIED_OBJECT requires two diagnostic paths.

### Diagnostic A

~~~text
Python lzma FORMAT_ALONE
+
independent binary struct parser
~~~

### Diagnostic B

~~~text
xz/lzma external decompressor
+
independent manual byte parser
~~~

Exact executable identities/versions must be pinned before execution.

Hard independence:

- same raw input hash only;
- no shared decompressed intermediate;
- no shared parsed record stream;
- no copying output between paths;
- separate result seals;
- separate failure reporting.

For every object:

~~~text
A.decompressed_sha256 == B.decompressed_sha256
A.projection_sha256 == B.projection_sha256
A.record_count == B.record_count
~~~

Otherwise:

~~~text
BLOCKED_DIAGNOSTIC_DISAGREEMENT
~~~

Agreement proves compatibility with already-qualified semantics, not semantic truth of C01-C07.

## 13. Decisive representation invariants

Only invariants already justified by current-authority semantic adjudications may be decisive.

The future ExecutionContract must list each invariant with:

~~~text
invariant_id
semantic_claim_id
source_adjudication_id
source_adjudication_seal
failure_disposition
~~~

No profitability/chart-shape/expected-volatility heuristic is admissible.

No runtime value-based rule may be invented after observing failures.

## 14. Transition / multi-regime handling

The exhaustive execution is open-world but not adaptively repairable.

### 14.1 Predeclared multi-regime execution

Multiple regimes may coexist in one qualification only if the sealed RepresentationRegimeManifest already contains:

- every regime identity;
- deterministic complete applicability rules;
- exact transition/coexistence semantics;
- no interval ambiguity.

### 14.2 Newly discovered regime/transition

If execution positively demonstrates material inconsistent with the predeclared selected regime:

~~~text
REFUTED_SELECTED_REGIME
or
BLOCKED_UNKNOWN_REPRESENTATION
~~~

The current execution cannot add K2, move a boundary or change parser rules.

A new versioned regime manifest + new execution lineage is required.

No nearest-regime fallback.

## 15. Content-addressed durable evidence

A transient GitHub Actions artifact alone cannot satisfy B-FIQ.

Every material evidence object must have:

~~~text
evidence_object_id
media_type
byte_length
sha256
durable_storage_class
durable_content_address
repository_binding_record
created_at_utc
~~~

Allowed durable body storage classes must be declared before execution.

Minimum properties:

- content-addressed or immutable-versioned;
- exact-byte retrieval possible;
- integrity re-verifiable from SHA-256;
- retention at least through all dependent qualification/backtest audit lifetimes;
- access control does not prevent governed re-audit.

The repository must persist at least manifests, hashes, seals, adjudications and durable object references.

If any body referenced by a PASS cannot later be recovered and re-hashed:

~~~text
CAPTURE_INTEGRITY_FAILURE
→ OPEN reopen event
~~~

## 16. qualification_capture_set_root_sha256

Every wall-clock inventory interval produces one capture-set leaf.

For CALENDAR_CLOSED_NO_COMPONENT:

~~~text
{
  interval_ordinal,
  interval_id,
  disposition,
  calendar_identity,
  request_sent = false
}
~~~

For provider-request intervals:

~~~text
{
  interval_ordinal,
  interval_id,
  regime_id,
  provider_locator,
  retrieval_started_at_utc,
  retrieval_completed_at_utc,
  disposition,
  raw_sha256_or_null,
  capture_seal,
  diagnostic_A_seal_or_null,
  diagnostic_B_seal_or_null,
  qualified_empty_rule_identity_or_null
}
~~~

Then:

~~~text
qualification_capture_set_root_sha256 =
SHA256(canonical_json(ordered exact leaf list))
~~~

The root identifies the project's sequential capture set.

It does not claim provider-side atomicity.

## 17. CompletenessProof

A CompletenessProof must establish all:

~~~text
inventory wall-clock ordinals are contiguous
inventory root re-verifies
every inventory interval has exactly one terminal disposition
every REQUIRED interval has exactly one request attempt
no CLOSED interval has a request attempt
actual request count == planned request count
actual request count <= request budget
no duplicate required interval capture
no undeclared interval capture admitted
all required durable bodies recover and re-hash
capture-set root re-verifies
all diagnostic seals re-verify
~~~

Any mismatch:

~~~text
FULL_INTERVAL_QUALIFIED = NO
~~~

## 18. FULL_INTERVAL_QUALIFIED verdict

### PASS

Only if:

~~~text
every EXPECTED_CLOSED interval
= CALENDAR_CLOSED_NO_COMPONENT

AND

every EXPECTED_OPEN interval
= QUALIFIED_OBJECT
  OR QUALIFIED_EMPTY under a current-authority empty rule

AND CompletenessProof = PASS

AND no unresolved positive competing-provider-representation contradiction

AND all applicable C01-C07 adjudications are current authority

AND qualification_capture_set_root_sha256 valid

AND durable evidence integrity = PASS
~~~

Then:

~~~text
FULL_INTERVAL_QUALIFIED = PASS
~~~

### FAIL

FAIL is permitted only when valid non-transport evidence falsifies the predeclared operational representation rule, for example:

~~~text
selected regime directly retrieved
+
exact bytes intact
+
both independent diagnostics consistently establish
a predeclared decisive invariant violation
~~~

or another qualified positive contradiction makes the selected rule false.

FAIL never silently repairs the representation rule.

### BLOCKED

Any unresolved or indeterminate state, including:

~~~text
transport failure
timeout
429/5xx
auth/policy failure
unresolved redirect
404 without qualified-empty semantics
zero bytes without qualified-empty semantics
missing durable body
diagnostic disagreement
unknown representation
ambiguous transition
inventory mismatch
request-budget mismatch
calendar authority reopened
semantic authority reopened
capture integrity failure
positive contradiction unresolved
~~~

## 19. OperationalApplicabilityAdjudication

A FULL_INTERVAL execution does not self-promote C08.

A separate sealed adjudication must project the evidence:

~~~text
schema =
B_PE_01R_OPERATIONAL_APPLICABILITY_ADJUDICATION_V0_2

adjudication_id
successor_contract_id
successor_contract_version

authority_scope_tuple
authority_scope_tuple_digest

interval_inventory_root
qualification_capture_set_root_sha256

completeness_proof_id
completeness_proof_seal
FULL_INTERVAL_QUALIFIED_verdict

C08_D4_OP_verdict
C08_D5_OP_verdict
BPE_C08_OP_verdict

material_contradiction_status
limitations
created_at_utc
adjudication_seal
~~~

Projection rule:

~~~text
FULL_INTERVAL_QUALIFIED != PASS
→ BPE_C08_OP_verdict cannot PASS

FULL_INTERVAL_QUALIFIED = PASS
+
exact instrument binding PASS
+
full-domain regime classification PASS
+
current-authority scope tuple PASS
+
no material contradiction
→ C08-D4-OP PASS
→ C08-D5-OP PASS
→ BPE-C08-OP-V0.2 PASS
~~~

## 20. OperationalEvidenceReopenEvent

Inherited from B-PE-01R.

Mandatory triggers include:

~~~text
ARCHIVE_MUTATION_DETECTED
CAPTURE_INTEGRITY_FAILURE
INTERVAL_INVENTORY_CHANGE
EXECUTION_WINDOW_CHANGE
WARMUP_RULE_CHANGE
SESSION_CALENDAR_CHANGE
INSTRUMENT_SCOPE_CHANGE
REPRESENTATION_RULE_CHANGE
SEMANTIC_AUTHORITY_REOPENED
COMPETING_PROVIDER_REPRESENTATION_UNRESOLVED
PROVIDER_DELIVERY_IDENTITY_CHANGE
QUALIFIED_EMPTY_RULE_REOPENED
~~~

Any OPEN event makes historical operational PASS non-authoritative for new promotion.

## 21. OperationalAdjudicationSupersession

Inherited closed schema:

~~~text
prior adjudication
+
successor adjudication
+
reason
+
sealed supersession relation
~~~

Superseded PASS remains historical evidence only.

## 22. authority_scope_tuple

Future operational adjudication must bind:

~~~text
provider_identity
instrument_identity
representation_rule_identity

full_d_representation_domain_identity
execution_window_freeze_identity
warmup_rule_identity
session_calendar_identity
interval_inventory_root

provider_delivery_identity_policy_id
locator_regime_manifest_id
transport_policy_id
request_budget_id
execution_shard_plan_id

applicable_C01_C07_adjudications[]

qualified_empty_rule_id
qualified_empty_rule_seal

qualification_capture_set_root_sha256

successor_contract_id
successor_contract_version
~~~

Canonical digest:

~~~text
authority_scope_tuple_digest =
SHA256(canonical_json(authority_scope_tuple))
~~~

Downstream B/D use requires exact tuple-digest equality.

No subset/superset inheritance.

## 23. D binding

B-FIQ qualification is not D materialization.

A later D may use operational PASS only if it:

~~~text
consumes exact qualified captured bytes
OR
re-retrieves every required component and proves exact raw hash equality
~~~

Calendar-closed intervals remain explicit no-component intervals.

Any same-locator hash change before new downstream promotion:

~~~text
ARCHIVE_MUTATION_DETECTED
→ OPEN reopen event
~~~

## 24. Current-authority predicate

An operational PASS is current authority only if:

~~~text
BPE_C08_OP_verdict == PASS
FULL_INTERVAL_QUALIFIED == PASS

exact successor contract/version matches
exact authority_scope_tuple digest matches downstream requirement
exact interval inventory root matches
exact qualification capture-set root matches

no superseding adjudication
no OPEN reopen event

all referenced C01-C07 adjudications are current authority
qualified-empty rule remains current authority if used

durable evidence integrity re-verification = PASS
~~~

Otherwise it has zero authority for new downstream promotion.

## 25. Execution-lineage immutability

Once the first provider request in a future B-FIQ execution is sent, immutable:

- interval inventory;
- regime manifest;
- provider delivery policy;
- transport policy;
- request budget;
- shard plan;
- semantic invariant list;
- empty rule identity;
- durable storage policy.

Any change creates a new execution lineage.

No in-place repair.

## 26. Execution authorization boundary

A future B-FIQ execution is a separate real-data action and requires explicit user authorization.

Authorization must be scoped to:

~~~text
sealed IntervalInventory
sealed regime/locator manifest
sealed TransportPolicy
sealed RequestBudget
sealed ExecutionShardPlan
sealed semantic invariant list
sealed durable storage policy
STOP after qualification/adjudication artifacts
~~~

It does not authorize:

~~~text
D materialization
backtest
paper/broker/live
~~~

## 27. Candidate verdict

~~~text
B-FIQ-01 CONTRACT =
PERSISTED CANDIDATE / ADVERSARIAL BREAK REQUIRED
~~~

No provider request or exhaustive execution occurred.
