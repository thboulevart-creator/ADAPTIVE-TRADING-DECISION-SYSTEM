# B-FIQ-01 — FULL_INTERVAL_QUALIFIED EMPIRICAL REPRESENTATION-QUALIFICATION CONTRACT — FINAL PERSISTED-HEAD RE-BREAK

Date: 2026-09-21  
Repository: thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
Branch: integration/system-v1  
Corrected composite HEAD: 36b28388896ca9270314b36340154174b6735cf5

Normative composite:

~~~text
candidate blob
171caf891e6943d27cd8b612cf01acc5ffb34d43

+
correction V0.2 blob
d4ba5eef1ce6f94a17af796b5a34bad244750df3
~~~

Composite identity:

~~~text
B_FIQ_01_USATECH_FULL_INTERVAL_EMPIRICAL_REPRESENTATION_QUALIFICATION_V0_2_CORRECTED
~~~

## 1. Scope

This contract qualifies the design of a future exhaustive empirical representation qualification.

No full-domain BI5 request was executed.

No D was materialized.

No backtest or trading execution was authorized or performed.

## 2. Exact full-domain semantics

The qualified domain is derived from frozen/current-authority inputs:

~~~text
instrument = USATECHIDXUSD

execution-window freeze blob =
bf7c43e9d90d952dfa3715c28575fdf6cf379a89

first included open H1 =
2021-08-15T22:00:00Z

last included open H1 =
2026-08-14T20:00:00Z

warmup =
exactly 20 preceding EXPECTED_OPEN H1 bars

session calendar =
DUKASCOPY_USATECH_SESSION_CALENDAR_V3

session calendar blob =
fab634aab7b8c299b0139c3c43bf5b89a2aa03d0
~~~

The IntervalInventory covers every UTC-aligned wall-clock H1 from the derived warmup start through the frozen last included open H1.

Thus weekends, daily breaks, special closures and other EXPECTED_CLOSED hours remain explicit inventory members rather than silently disappearing.

## 3. Calendar-open / calendar-closed split

For each inventory H1:

~~~text
EXPECTED_OPEN
→ REQUIRED provider component

EXPECTED_CLOSED
→ NOT_REQUIRED_CALENDAR_CLOSED
→ terminal disposition CALENDAR_CLOSED_NO_COMPONENT
→ request forbidden
~~~

Calendar-closed state is not QUALIFIED_EMPTY.

Any non-open/non-closed unresolved calendar state blocks inventory construction.

## 4. Exact pre-request artifacts required

Before any future provider request, all of the following must be persisted and sealed:

~~~text
IntervalInventory
ProviderDeliveryIdentityPolicy
RepresentationRegimeManifest
RequestManifest
TransportPolicy
RequestBudget
ExecutionShardPlan
DiagnosticIndependenceManifest
DurableEvidencePolicy
SemanticInvariantManifest
qualified-empty rule identity if used
~~~

Any mutation after first provider request creates a new execution lineage.

## 5. RequestManifest closure

The corrected contract requires a fully pre-rendered RequestManifest.

For every REQUIRED interval:

~~~text
exact interval ID
exact regime ID
exact request locator string
exact provider-delivery endpoint identity
request_expected = true
~~~

For every CLOSED interval:

~~~text
request_expected = false
locator = null
regime = null
~~~

Once sealed:

~~~text
runtime locator rendering has zero normative authority
~~~

Therefore zero-indexed month bugs, boundary rendering bugs, endpoint substitutions or other runtime locator drift cannot silently qualify.

## 6. Request-volume constraints

Hard first-execution ceilings:

~~~text
GET only
automatic retry = 0
HTTP automatic content decoding = false
Accept-Encoding = identity

max parallel requests <= 4
aggregate request-start rate <= 2 requests/second

connect timeout <= 15 s
per-request total timeout <= 60 s

per-response body cap <= 50 MiB
automatic redirect following = false
~~~

RequestBudget binds the exact planned request count to RequestManifest REQUIRED rows.

For the initial exhaustive execution:

~~~text
maximum actual request count
=
planned request count
~~~

No exploratory or adaptive extra request is allowed.

## 7. Deterministic sharding

Execution may be split across workers/jobs only under a presealed ExecutionShardPlan.

Every REQUIRED interval belongs to exactly one shard.

Cross-shard overlap is forbidden.

Worker partitioning does not change semantic domain membership.

An uncertain request outcome becomes BLOCKED and is not silently retried inside the same lineage.

## 8. QUALIFIED_EMPTY fail-closed rule

QUALIFIED_EMPTY exists structurally but is disabled by default.

It can be used only when a separate current-authority empty-object rule has already qualified how to distinguish:

~~~text
legitimate zero-tick open H1
provider empty-object convention
missing object
404
zero-byte body
malformed body
truncated body
calendar-closed market
archive gap
~~~

Without such rule:

~~~text
EXPECTED_OPEN + no non-empty qualified object
→ BLOCKED
~~~

No transport symptom self-qualifies as empty.

## 9. QUALIFIED_OBJECT rule

An EXPECTED_OPEN interval reaches QUALIFIED_OBJECT only when:

~~~text
sealed exact locator was requested
provider transport valid
non-empty exact bytes captured
raw SHA-256 valid
capture seal valid
assigned regime accepts payload

Diagnostic A PASS
Diagnostic B PASS

A/B decompressed SHA equal
A/B projection SHA equal
A/B record count equal

all current-authority decisive invariants pass
no unresolved positive material contradiction
~~~

HTTP 200 alone is insufficient.

## 10. Diagnostic independence

Initial candidate defect BFIQ01-F02 is closed.

A sealed DiagnosticIndependenceManifest must bind exact material implementation identities and hashes for:

~~~text
decompression
physical framing
primitive parsing
semantic projection
decisive invariant evaluation
~~~

Shared parser/projection/invariant implementation lineage yields:

~~~text
INDEPENDENCE = BLOCKED
~~~

Allowed shared material is limited to exact raw bytes and already-qualified immutable schemas/constants explicitly listed in the manifest.

Different tool names alone do not establish independence.

## 11. Open-world transition handling

Multi-regime qualification is permitted only when all regimes and their complete deterministic applicability rules are sealed before execution.

If a new transition/family is discovered after requests begin:

~~~text
REFUTED_SELECTED_REGIME
or
BLOCKED_UNKNOWN_REPRESENTATION
~~~

The current lineage cannot:

- add K2;
- move transition boundaries;
- replace locator rules;
- replace parsers;
- change scaling/semantics.

A new versioned lineage is required.

No nearest-format fallback exists.

## 12. Durable evidence

Initial candidate defect BFIQ01-F03 is closed.

A sealed DurableEvidencePolicy is mandatory.

Transient workflow artifacts are staging only and cannot support final authority.

Every body needed for candidate PASS must be durably persisted under the allowed policy before QualificationExecutionResult can close.

If required evidence later cannot be recovered and re-hashed:

~~~text
CAPTURE_INTEGRITY_FAILURE
→ OPEN OperationalEvidenceReopenEvent
~~~

## 13. Closed execution evidence membership

Initial candidate defect BFIQ01-F04 is closed.

For each REQUIRED interval, deterministic cardinality is exactly:

~~~text
1 TransportCapture
1 DiagnosticAResult
1 DiagnosticBResult
1 IntervalTerminalRecord
~~~

Even a diagnostic that cannot run must emit one sealed NOT_RUN record with the exact blocking reason.

For each CLOSED interval:

~~~text
1 IntervalTerminalRecord
0 TransportCapture
0 DiagnosticAResult
0 DiagnosticBResult
~~~

The QualificationExecutionResult contains exact registries of all produced evidence and an evidence_set_digest.

A record may not be omitted because it is unfavorable.

Any:

~~~text
missing required record
duplicate record ID
unexpected extra execution record
record seal mismatch
registry cardinality mismatch
~~~

forces:

~~~text
candidate FULL_INTERVAL verdict = BLOCKED
~~~

Operational adjudication cannot select a favorable subset.

## 14. qualification_capture_set_root

Every wall-clock inventory interval contributes exactly one leaf.

The root binds:

- interval identity/order;
- request-manifest row;
- regime/locator where requested;
- retrieval timestamps;
- terminal disposition;
- raw SHA or null;
- capture identity/seal;
- both diagnostic identities/seals;
- durable evidence identity;
- qualified-empty rule identity if any.

The resulting:

~~~text
qualification_capture_set_root_sha256
~~~

identifies the exact sequential capture set produced by the project.

It does not claim provider-side atomicity.

## 15. CompletenessProof

FULL_INTERVAL qualification requires a sealed CompletenessProof proving at least:

~~~text
contiguous wall-clock inventory
valid inventory root
exact one terminal disposition per interval

every REQUIRED row attempted exactly once
every CLOSED row attempted zero times

actual request count = planned request count
request budget respected

no duplicate required interval
no undeclared interval admitted

all required evidence registries complete
all record seals valid

all durable bodies recover and re-hash
all diagnostic seals re-verify

evidence_set_digest valid
capture-set root valid
~~~

Any mismatch means FULL_INTERVAL_QUALIFIED cannot PASS.

## 16. FULL_INTERVAL_QUALIFIED verdict

### PASS

Only when:

~~~text
all EXPECTED_CLOSED
= CALENDAR_CLOSED_NO_COMPONENT

all EXPECTED_OPEN
= QUALIFIED_OBJECT
  or current-authority QUALIFIED_EMPTY

CompletenessProof = PASS

DiagnosticIndependenceManifest = PASS

all applicable C01-C07 adjudications = current authority

no unresolved positive competing-representation contradiction

durable evidence integrity = PASS

evidence-set digest = valid
capture-set root = valid
~~~

### FAIL

Only adequate exact non-transport evidence may falsify the selected operational representation rule.

Example:

~~~text
exact provider bytes intact
+
both independent paths establish the same
predeclared decisive invariant violation
~~~

FAIL cannot repair the representation.

### BLOCKED

Any unresolved state, including:

~~~text
transport failure
timeout
429/5xx
auth/policy failure
unresolved redirect
404 without qualified-empty rule
zero bytes without qualified-empty rule
diagnostic disagreement
diagnostic independence blocked
unknown representation
ambiguous transition
inventory mismatch
request-manifest mismatch
request-budget mismatch
missing evidence registry member
durable body unavailable
calendar authority reopened
semantic authority reopened
capture integrity failure
material contradiction unresolved
~~~

## 17. Operational C08 projection

FULL_INTERVAL execution does not self-promote C08.

A sealed OperationalApplicabilityAdjudication must bind:

~~~text
QualificationExecutionResult
CompletenessProof
authority_scope_tuple
interval_inventory_root
request_manifest_root
evidence_set_digest
qualification_capture_set_root_sha256
~~~

Only if all operational prerequisites pass can it project:

~~~text
C08-D4-OP = PASS
C08-D5-OP = PASS
BPE-C08-OP-V0.2 = PASS
~~~

Documentary C08-D4-DOC/D5-DOC remain independent.

## 18. Current authority and downstream scope

authority_scope_tuple binds exact:

~~~text
provider
instrument
representation rule
full-D domain
execution-window freeze
warmup rule
session calendar
interval inventory root

provider delivery identity policy

regime/locator manifest
request manifest root
transport policy
request budget
shard plan

diagnostic independence manifest
semantic authority adjudications
qualified-empty rule if used
durable evidence policy

QualificationExecutionResult
evidence_set_digest
qualification_capture_set_root

successor contract/version
~~~

Downstream use requires exact tuple-digest equality.

Any scope change requires new adjudication.

## 19. D binding

B-FIQ PASS is not D materialization.

Later D may use operational C08 authority only by:

~~~text
consuming exact qualified captured bytes
OR
re-retrieving every required component
and proving exact raw-hash equality
~~~

Any later same-locator hash difference opens:

~~~text
ARCHIVE_MUTATION_DETECTED
~~~

and historical PASS loses authority for new promotion.

## 20. Initial defects closed

Adversarial break demonstrated:

~~~text
BFIQ01-F01 — exact request membership not sealed
BFIQ01-F02 — diagnostic independence self-asserted
BFIQ01-F03 — durable storage policy not scope-bound
BFIQ01-F04 — execution evidence-set membership not closed
~~~

All are closed by correction blob:

~~~text
d4ba5eef1ce6f94a17af796b5a34bad244750df3
~~~

No new material defect was demonstrated in the persisted corrected composite.

## 21. Final verdict

~~~text
B-FIQ-01 FULL_INTERVAL_QUALIFIED
EMPIRICAL REPRESENTATION-QUALIFICATION CONTRACT = PASS
~~~

This PASS qualifies the contract only.

It does not mean:

~~~text
IntervalInventory materialized
RequestManifest materialized
five-year provider requests sent
FULL_INTERVAL_QUALIFIED achieved
C08-D4-OP PASS
C08-D5-OP PASS
BPE-C08-OP-V0.2 PASS
D materialized
backtest authorized
~~~

## 22. Exactly one next governed action

Open only:

~~~text
B-FIQ-02 —
FULL_INTERVAL pre-execution package materialization and sealing
~~~

B-FIQ-02 remains non-network preparation only.

Required scope:

~~~text
fresh HEAD
→ read B-FIQ-01 PASS

→ materialize exact IntervalInventory
→ verify warmup/evaluation boundaries
→ compute interval_inventory_root

→ materialize ProviderDeliveryIdentityPolicy
→ materialize RepresentationRegimeManifest
→ render exact RequestManifest for every inventory H1
→ compute request_manifest_root

→ materialize TransportPolicy
→ materialize RequestBudget
→ materialize ExecutionShardPlan

→ materialize DiagnosticIndependenceManifest
→ materially prove A/B implementation independence
→ materialize SemanticInvariantManifest

→ materialize DurableEvidencePolicy

→ construct provisional authority_scope_tuple
   excluding future execution-dependent roots/results

→ adversarial break all pre-request artifacts
→ persisted-head re-break
→ PASS / FAIL / BLOCKED
→ audit + backup + checkpoint
→ STOP
~~~

Still prohibited inside B-FIQ-02:

~~~text
provider BI5 GET
full-interval execution
D materialization
backtest
paper/broker/live
~~~

Only after B-FIQ-02 PASS may an explicitly authorized B-FIQ execution be considered.

STOP.
