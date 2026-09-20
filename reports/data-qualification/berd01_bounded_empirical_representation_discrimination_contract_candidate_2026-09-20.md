# B-ERD-01 — BOUNDED EMPIRICAL REPRESENTATION-DISCRIMINATION CONTRACT — CANDIDATE

**Date:** 2026-09-20
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM
**Branch:** integration/system-v1
**Starting HEAD:** 4e969db19f852e00dc219b084163fbf4b5397c87
**Status:** PERSISTED FORMALIZATION CANDIDATE — NOT YET QUALIFIED

## 0. Permission boundary

This block formalizes an experiment only.

Still prohibited:

~~~text
provider contact
real BI5 download
real BI5 processing
real project acquisition
D materialization
real Q/F/Q-RM-12 execution
real backtest
paper/broker/live
positive P1.1 authorization
~~~

No HTTP request to a BI5 object may be executed in B-ERD-01.

Preserved state:

~~~text
B-PE-05 = NOT EXECUTED
C08-D4 = BLOCKED
C08-D5 = BLOCKED
BPE-C08 = BLOCKED
B global executable gate = BLOCKED
~~~

B-PE-01 remains unchanged.

## 1. Decision problem

Define a bounded future experiment answering:

> For USATECHIDXUSD and predeclared target-date probes, which known Dukascopy historical-tick representation hypotheses are consistent with the material actually served, without assuming hourly or daily authority in advance?

The experiment is a discriminator, not a backtest and not a full acquisition.

It must support a candidate representation for observed probes, refute a candidate for observed probes, detect coexistence or aliasing, detect unresolved competition, and detect unknown representation.

It must never promote a sample to five-year continuity.

## 2. Contract identity

~~~text
contract_id =
B_ERD_01_DUKASCOPY_USATECHIDXUSD_BOUNDED_REPRESENTATION_DISCRIMINATOR

contract_version =
B_ERD_01_DUKASCOPY_USATECHIDXUSD_BOUNDED_REPRESENTATION_DISCRIMINATOR_V0_1_CANDIDATE
~~~

Target:

~~~text
provider = Dukascopy
instrument = USATECHIDXUSD / USATECH.IDX/USD
research market-time interval = 2021-08-14 through 2026-08-14
purpose = representation discrimination before full D materialization
~~~

## 3. Hypothesis register

### H_HOURLY

For an observed probe interval, a provider-served legacy hour-addressed historical-tick object family is sufficient to account for the observed target material.

Probe-local only.

### H_DAILY

For an observed probe market date, a provider-served daily historical-tick object family is sufficient to account for the observed target material.

Probe-local only.

### H_COEXISTENCE

For an observed probe, more than one representation family is simultaneously available and materially describes the same target history.

This does not imply semantic equivalence.

### H_TRANSITION_PATTERN

Across predeclared probe anchors, supported representation states differ in a temporally ordered pattern.

This yields only:

~~~text
PROBE_OBSERVED_TRANSITION_PATTERN
~~~

not a complete transition boundary.

### H_UNKNOWN

Unknown-family handling is split into two states:

~~~text
UNKNOWN_REPRESENTATION_EVIDENCED
KNOWN_CANDIDATES_INSUFFICIENT
~~~

UNKNOWN_REPRESENTATION_EVIDENCED requires positive captured evidence of an unregistered family, such as:

- redirect to an unregistered object family;
- provider metadata explicitly identifying another historical-tick representation;
- provider bytes/content structure positively incompatible with all registered candidate signatures while still constituting provider material.

If K1/K2 are merely absent, unusable or transport-blocked:

~~~text
KNOWN_CANDIDATES_INSUFFICIENT
→ BLOCKED
~~~

Do not claim an unknown representation was observed without positive evidence.

No closest-known-format fallback exists.

## 4. Known candidate representation families

Known candidates are not exhaustive.

### K1 — LEGACY_HOURLY_TICK_BI5

Evidence basis:

- B-PE-03 provider evidence establishes historical hour-addressed h_ticks.bi5 family existence.
- B-PE-02 independent implementations provide pinned locator corroboration.

~~~text
representation_candidate_id = K1_LEGACY_HOURLY_TICK_BI5
bucket_semantics = hour-addressed tick object
locator_family = h_ticks.bi5
authority_status = CANDIDATE_FOR_EMPIRICAL_DISCRIMINATION
~~~

Exact URL rendering rules must be persisted in a future LocatorManifest before any request.

No path rendering detail may be guessed from memory.

### K2 — CURRENT_DAILY_TICK_BI5

Evidence basis:

B-PE-02 provider-current Historical Price Data documentation observed a current daily historical-tick BI5 representation and warned about older hourly semantics.

~~~text
representation_candidate_id = K2_CURRENT_DAILY_TICK_BI5
bucket_semantics = daily historical-tick object
authority_status = CANDIDATE_FOR_EMPIRICAL_DISCRIMINATION
~~~

The exact daily locator template is not fabricated in this formalization.

Before future execution, LocatorManifest must bind an exact provider documentation anchor and exact rendered locator template.

If K2 cannot be rendered from captured provider evidence without inference:

~~~text
B-ERD execution = BLOCKED
~~~

### K_UNKNOWN

Not a locator template.

It is the fail-closed state reached when known candidates fail to explain observed provider behavior or competing material cannot be classified.

## 5. LocatorManifest — future closed input

Future execution requires an immutable LocatorManifest:

~~~text
schema = B_ERD_01_LOCATOR_MANIFEST_V0_1

locator_manifest_id
contract_id
contract_version
provider_host
instrument_id
candidate_families
for each candidate family:
  candidate_id
  source_evidence_ids
  source_anchor_ids
  rendering_rule
  month/date encoding rule
  hour rule if applicable
  exact example locator
  authority_limitations
manifest_created_at_utc
manifest_seal
~~~

Rules:

- no runtime locator guessing;
- no search-discovered locator added after probe results are visible;
- any change requires a new manifest identity and seal;
- K1/K2 are not treated as exhaustive.

## 6. Deterministic bounded probe anchors

Probe selection is fixed before any real response exists.

Every anchor resolves to exactly one governed market-open H1 comparison window:

~~~text
W_probe = [market_h1_start_utc, market_h1_start_utc + 1 hour)
~~~

All candidate families are compared only after projection to the same W_probe.

Daily-object observations outside W_probe remain captured evidence but do not contribute to cross-family cardinality/coverage comparison for that probe.

Probe anchors:

~~~text
PW = final governed market-open H1 interval of the mandatory 20-H1 warmup prefix
P0 = H1 interval containing or immediately following frozen first included open slot
P1 = first governed market-open H1 interval on/after 2022-08-14
P2 = first governed market-open H1 interval on/after 2023-08-14
P3 = first governed market-open H1 interval on/after 2024-08-14
P4 = first governed market-open H1 interval on/after 2025-08-14
P5 = last governed market-open H1 interval strictly before 2026-03-03T00:00:00Z
P6 = first governed market-open H1 interval strictly after 2026-03-03T23:59:59Z
P7 = H1 interval containing or immediately preceding frozen last included open slot
~~~

Rules:

- exact timestamps are persisted before any provider request;
- no probe is moved because a locator fails;
- duplicate resolved intervals retain all anchor identities but execute once;
- P5/P6 do not imply JETTA caused a BI5 transition;
- PW tests bounded warmup applicability only;
- probes stratify the domain but do not qualify unsampled intervals.

## 7. ProbePlan — future closed input

~~~text
schema = B_ERD_01_PROBE_PLAN_V0_1

probe_plan_id
contract_id
contract_version
target_instrument
target_research_interval
session_calendar_identity
execution_window_freeze_identity
resolved_probes[]
  probe_id
  anchor_rule_id
  market_interval_start_utc
  market_interval_end_utc
  comparison_window_duration = PT1H
  expected_market_open_basis
candidate_locator_manifest_id
created_at_utc
probe_plan_seal
~~~

No mutation after the first provider object request.

## 8. Exact raw transport capture

Every future attempted candidate locator must produce one immutable TransportCapture.

For BI5 object probes the transport protocol is fixed:

~~~text
request_method = GET
automatic_retry_count = 0
~~~

Any timeout, client transport exception, 429, 5xx, auth/policy failure, truncated/incomplete transfer or other transport ambiguity is fail-closed for that candidate/probe.

A later rerun is a new execution_id and new capture set; it never overwrites or replaces the earlier failed capture.

~~~text
schema = B_ERD_01_TRANSPORT_CAPTURE_V0_1

capture_id
probe_plan_id
probe_id
candidate_id
request_method
requested_locator
request_started_at_utc
response_received_at_utc
redirect_chain
final_locator
http_status
selected_response_headers
raw_response_byte_length
raw_response_sha256
content_signature
transport_disposition
capture_created_at_utc
capture_seal
~~~

Selected headers include when present:

~~~text
Content-Type
Content-Length
Content-Encoding
ETag
Last-Modified
Accept-Ranges
Cache-Control
Via
Server
Location
Retry-After
~~~

Raw response bytes are preserved exactly.

HTTP metadata is evidence, not semantic truth.

## 9. Transport and family dispositions

Transport dispositions:

~~~text
OBJECT_BYTES_OBTAINED
OBJECT_ABSENT_SIGNAL
REDIRECTED_TO_REGISTERED_FAMILY
REDIRECTED_TO_UNKNOWN
RATE_LIMITED
TRANSIENT_SERVER_FAILURE
AUTH_OR_POLICY_BLOCK
NON_BI5_CONTENT
TRANSPORT_AMBIGUOUS
~~~

Family dispositions are distinct:

~~~text
FAMILY_OBSERVED
FAMILY_NOT_OBSERVED
FAMILY_REFUTED
FAMILY_TRANSPORT_BLOCKED
FAMILY_LOCATOR_BLOCKED
~~~

Rules:

- HTTP 200 alone does not mean valid object;
- HTTP 404 is at most OBJECT_ABSENT_SIGNAL and cannot alone create FAMILY_REFUTED;
- FAMILY_NOT_OBSERVED has zero refutation weight;
- FAMILY_REFUTED requires a predeclared falsifiable candidate prediction plus valid captured evidence that directly contradicts that prediction;
- 429, 5xx, auth/policy failure, timeout and transport exception become FAMILY_TRANSPORT_BLOCKED;
- locator rendering ambiguity becomes FAMILY_LOCATOR_BLOCKED;
- HTML/error bodies never become empty tick files;
- unexpected redirect/content may support UNKNOWN_REPRESENTATION_EVIDENCED only when positive evidence identifies an unregistered family;
- all known families merely absent/unusable becomes KNOWN_CANDIDATES_INSUFFICIENT → BLOCKED;
- HEAD-only observations are insufficient for object-byte claims.

## 10. Object identity and cardinality

For each candidate family/probe, record:

~~~text
candidate locator count attempted
object bytes obtained count
raw hashes
raw byte lengths
redirect outcomes
transport failures
~~~

Object cardinality is family-specific.

Hourly family may require multiple hour locators for one probe interval.

Daily family may use one day object covering that interval.

Object-count equality is not required for semantic equivalence.

## 11. Semantic discrimination layers

### L0 — transport/object evidence

Can establish exact bytes returned, redirects/content identity, and known/unknown object-family behavior.

Cannot establish tick semantic correctness.

### L1 — representation-specific structural interpretation candidate

May attempt decompression under the candidate representation, framing candidate, physical accounting, and raw structural fingerprints.

Successful structural decode is not provider-truth PASS.

A structural failure can refute that exact candidate interpretation for captured bytes only when transport capture is valid.

### L2 — semantic projection diagnostics

Where candidate interpretation permits, derive diagnostic logical projections:

~~~text
timestamps
ask
bid
volumes
source provenance
~~~

These remain diagnostics until B evidence rules are explicitly satisfied or versioned.

No plausibility check may silently redefine B-PE-01 truth.

## 12. Independent diagnostic paths

For captured bytes, future execution must use at least two independently implemented diagnostic paths where semantic comparison is attempted.

Requirements:

~~~text
no shared decoded intermediate
no copied per-record interpretation output
separate decompression/parse path where feasible
separate result sealing
exact raw input hash cross-binding
~~~

Agreement supports only:

~~~text
CANDIDATE_SEMANTIC_CONSISTENCY
~~~

It does not establish external provider authority.

Disagreement:

~~~text
BLOCKED
~~~

Existing I_A/I_B may not automatically be reused unless the execution contract proves they satisfy this discriminator's independence/input requirements.

## 13. Plausibility checks

Plausibility is diagnostic, never silent repair.

Candidate checks may include:

~~~text
decoded timestamps finite and within candidate bucket semantics
price fields finite after candidate scaling
bid/ask values finite
no impossible timestamp domain under candidate rule
coverage interval consistent with requested market interval
~~~

Forbidden:

- strategy profitability;
- expected chart shape;
- preferred volatility;
- looks-like-NASDAQ judgement;
- outcome-driven thresholds.

A plausibility failure is decisive only when the invariant was prequalified for that candidate.

## 14. Cross-family coverage comparison

Where K1 and K2 both yield classifiable material, compare candidate semantic projections.

At minimum:

~~~text
candidate occurrence counts
timestamp-domain coverage
first/last candidate timestamps
exact timestamp multiplicity
strict duplicate multiplicity
overlap count
K1-only candidate observations
K2-only candidate observations
payload-value disagreements at matched candidate timestamps
~~~

No content-based deduplication.

Observed states:

~~~text
SEMANTICALLY_EQUIVALENT_ON_PROBE
STRICT_SUBSET
STRICT_SUPERSET
OVERLAP_WITH_DIVERGENCE
DISJOINT
COMPARISON_BLOCKED
~~~

Semantic equivalence on one probe proves nothing outside that probe.

## 15. Candidate, probe and overall dispositions

Per candidate / per probe:

~~~text
SUPPORTED
REFUTED
NOT_OBSERVED
BLOCKED
~~~

Per probe:

~~~text
DISCRIMINATED
NON_DISCRIMINATING
BLOCKED
~~~

Predeclared top-level proposition:

~~~text
T0 =
"the bounded probe set can discriminate the observed representation state
without unresolved transport, locator, unknown-family or semantic competition"
~~~

Overall verdict remains exactly:

~~~text
PROBE_SUPPORTED
PROBE_REFUTED
BLOCKED
~~~

Rules:

- PROBE_SUPPORTED iff every required probe is DISCRIMINATED and T0 holds;
- PROBE_REFUTED iff valid non-transport evidence demonstrates T0 is false for at least one required probe;
- BLOCKED iff evidence is insufficient to decide T0 because of transport, locator, unknown-family, integrity or semantic ambiguity;
- refuting K1 while supporting K2 does not make the execution overall PROBE_REFUTED if the probe is successfully discriminated;
- transport ambiguity never refutes;
- no majority vote.

## 16. Cross-probe synthesis

Allowed synthesis:

~~~text
all observed probes support K1
some observed probes support K1 and later probes support K2
observed probes show coexistence
one or more probes blocked
one or more probes indicate unknown representation
~~~

Only PROBE_OBSERVED_TRANSITION_PATTERN may be used when ordered probes differ.

Never infer an unsampled transition instant.

## 17. Anti-extrapolation hard boundary

~~~text
PROBE_SUPPORTED
≠
FULL_INTERVAL_QUALIFIED
~~~

and:

~~~text
all P0-P7 support K1
≠
K1 proven for every manifest-relevant interval
~~~

B-ERD execution cannot authorize full D.

## 18. FULL_INTERVAL_QUALIFIED — separate future evidence class

The representation domain relevant to future D is explicitly:

~~~text
FULL_D_REPRESENTATION_DOMAIN =
mandatory deterministic 20-H1 warmup prefix
+
frozen evaluation interval
~~~

A future rule may become FULL_INTERVAL_QUALIFIED only through a separately governed action establishing every manifest-relevant interval across FULL_D_REPRESENTATION_DOMAIN by one or more of:

### FI-1 — exhaustive locator/membership enumeration

Every manifest-relevant interval receives explicit representation evidence with no unresolved gaps.

### FI-2 — qualified deterministic transition boundaries

Exact non-overlapping representation regimes and boundaries cover every manifest-relevant interval.

### FI-3 — another explicitly qualified complete-coverage method

Must be adversarially qualified before use.

A bounded sample alone is never FI evidence.

## 19. Integrity and sealing rules

All structured artifacts in B-ERD-01 inherit exactly the B-PE-01 canonical JSON rule:

~~~text
UTF-8
sorted object keys
compact separators
ensure_ascii = false
allow_nan = false
duplicate object keys rejected
~~~

All structured seals use lowercase SHA-256 hex:

~~~text
LocatorManifest.manifest_seal =
SHA256(canonical_json(locator_manifest_without_manifest_seal))

ProbePlan.probe_plan_seal =
SHA256(canonical_json(probe_plan_without_probe_plan_seal))

TransportCapture.capture_seal =
SHA256(canonical_json(transport_capture_without_capture_seal))

ExecutionResult.result_seal =
SHA256(canonical_json(execution_result_without_result_seal))
~~~

Raw response hashes remain:

~~~text
SHA256(exact response bytes)
~~~

Seal mismatch invalidates the artifact and blocks its evidentiary use.

## 20. Future execution result

~~~text
schema = B_ERD_01_EXECUTION_RESULT_V0_1

execution_id
contract_id/version
locator_manifest_id/seal
probe_plan_id/seal
transport_capture_ids/seals
diagnostic_path_ids/versions
per_probe_candidate_results
per_probe_hypothesis_dispositions
cross_probe_summary
unknown_representation_events
limitations
overall_probe_verdict
created_at_utc
result_seal
~~~

overall_probe_verdict exactly:

~~~text
PROBE_SUPPORTED
PROBE_REFUTED
BLOCKED
~~~

Overall PROBE_SUPPORTED means only that bounded discrimination succeeded within the declared probe set and no blocking condition remains there.

It does not mean B/C08/global gate PASS.

## 21. Decision-use boundary

B-ERD evidence may later falsify hourly-only assumptions, falsify daily-only assumptions, discover coexistence, reveal likely regime changes, design full-interval qualification, or show that provider clarification is needed.

It may not directly:

~~~text
set C08-D4/D5 PASS under current B-PE-01
set B PASS
create full D completeness
authorize a backtest
~~~

## 22. Future execution authorization boundary

If B-ERD-01 contract becomes PASS, bounded execution is still a separate explicit authorization boundary because it downloads real provider bytes.

Execution must be limited to:

~~~text
presealed probes
presealed LocatorManifest
exact transport capture
diagnostic discrimination
STOP
~~~

No full acquisition and no backtest.

## 23. Correction record and corrected candidate verdict

Adversarial break demonstrated:

~~~text
BERD01-F01 — PROBE_COMPARISON_WINDOW_NOT_NORMATIVELY_FIXED
BERD01-F02 — REPRESENTATION_ABSENCE / MARKET_ABSENCE / TRANSPORT_FAILURE NOT CLOSED
BERD01-F03 — HTTP METHOD / RETRY POLICY DEFERRED
BERD01-F04 — MULTI-HYPOTHESIS OVERALL PROBE_REFUTED IS AMBIGUOUS
BERD01-F05 — H_UNKNOWN TRIGGER OVERCLAIMS UNOBSERVABLE UNKNOWN FAMILY
BERD01-F06 — STRUCTURED SEAL CANONICALIZATION NOT BOUND
BERD01-F07 — FULL D WARMUP REPRESENTATION COVERAGE NOT EXPLICIT
~~~

Only those demonstrated defects were corrected.

## 24. Corrected candidate verdict

~~~text
B-ERD-01 CONTRACT = CORRECTED PERSISTED CANDIDATE / FINAL RE-BREAK REQUIRED

B-PE-05 = NOT EXECUTED
C08-D4 = BLOCKED
C08-D5 = BLOCKED
B = BLOCKED

real BI5 activity = NONE
~~~

Next: persisted-HEAD final adversarial re-break of this corrected contract only.
