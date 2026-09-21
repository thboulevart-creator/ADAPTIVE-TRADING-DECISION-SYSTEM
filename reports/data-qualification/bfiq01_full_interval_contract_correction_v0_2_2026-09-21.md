# B-FIQ-01 — CORRECTION RECORD V0.2

Date: 2026-09-21  
Parent candidate blob: 171caf891e6943d27cd8b612cf01acc5ffb34d43  
Adversarial break blob: 44d7fc608ef99fcd3a0f0d6032107ade5371a93d  
Scope: closes only BFIQ01-F01 through BFIQ01-F04.

This record is normative over the parent candidate where they differ.

Composite identity:

~~~text
B_FIQ_01_USATECH_FULL_INTERVAL_EMPIRICAL_REPRESENTATION_QUALIFICATION_V0_2_CORRECTED
=
parent candidate
+
this correction record
~~~

No other parent-candidate requirement is weakened.

## 1. F01 correction — exact pre-rendered RequestManifest

Future execution requires one immutable pre-request artifact:

~~~text
schema =
B_FIQ_01_REQUEST_MANIFEST_V0_2

request_manifest_id
contract_id
contract_version

interval_inventory_id
interval_inventory_root

representation_regime_manifest_id
representation_regime_manifest_seal

provider_delivery_identity_policy_id
provider_delivery_identity_policy_seal

rows[]
  interval_ordinal
  interval_id
  expected_market_status
  provider_component_requirement
  regime_id_or_null
  exact_request_locator_or_null
  provider_delivery_endpoint_identity_or_null
  request_expected

required_request_count
closed_no_request_count

created_at_utc
request_manifest_root
request_manifest_seal
~~~

Rules:

### REQUIRED interval

Exactly one row:

~~~text
request_expected = true
regime_id_or_null != null
exact_request_locator_or_null != null
provider_delivery_endpoint_identity_or_null != null
~~~

### CALENDAR-CLOSED interval

Exactly one row:

~~~text
request_expected = false
regime_id_or_null = null
exact_request_locator_or_null = null
provider_delivery_endpoint_identity_or_null = null
~~~

### Root

~~~text
request_manifest_root =
SHA256(canonical_json(ordered exact rows))
~~~

The row order must equal IntervalInventory ordinal order.

After RequestManifest sealing:

~~~text
runtime locator rendering has zero normative authority
~~~

Every actual request must byte-for-byte match the exact sealed locator string and provider-delivery identity in its RequestManifest row.

Any mismatch:

~~~text
BLOCKED_LOCATOR
~~~

### Binding updates

RequestManifest ID/root/seal are mandatory inputs to:

- RequestBudget;
- ExecutionShardPlan;
- TransportCapture;
- QualificationExecutionResult;
- CompletenessProof;
- qualification_capture_set leaves;
- authority_scope_tuple.

RequestBudget planned_request_count must equal RequestManifest.required_request_count.

ExecutionShardPlan membership is evaluated against RequestManifest REQUIRED rows, not against runtime-rendered locators.

---

## 2. F02 correction — DiagnosticIndependenceManifest

Two paths cannot be called independent merely because tool names differ.

Future execution requires:

~~~text
schema =
B_FIQ_01_DIAGNOSTIC_INDEPENDENCE_MANIFEST_V0_2

manifest_id
contract_id
contract_version

raw_input_interface_identity

diagnostic_A
  decompressor_identity
  decompressor_version
  decompressor_binary_or_source_sha256
  parser_identity
  parser_source_blob_sha256
  projection_identity
  projection_source_blob_sha256
  invariant_evaluator_identity
  invariant_evaluator_source_blob_sha256

diagnostic_B
  decompressor_identity
  decompressor_version
  decompressor_binary_or_source_sha256
  parser_identity
  parser_source_blob_sha256
  projection_identity
  projection_source_blob_sha256
  invariant_evaluator_identity
  invariant_evaluator_source_blob_sha256

allowed_shared_artifacts[]
  artifact_identity
  artifact_hash
  justification
  source_semantic_adjudication_id_or_null

forbidden_shared_semantic_helpers[]
relationship_analysis
stage_independence_verdicts
overall_independence_verdict =
  PASS | BLOCKED

created_at_utc
manifest_seal
~~~

### Independence rules

Material stages:

~~~text
decompression
physical framing
primitive parsing
semantic projection
decisive invariant evaluation
~~~

At each material stage, the paths must not share one implementation lineage unless that stage is explicitly excluded from the independence claim and the remaining independent stages are proven sufficient by a separately qualified rule.

For B-FIQ-01 V0.2, the default is strict:

~~~text
parser implementation lineage must differ
projection implementation lineage must differ
decisive invariant evaluator lineage must differ
~~~

Allowed shared artifacts are limited to:

- exact raw body bytes;
- immutable schema definitions;
- immutable constants whose semantics already have current-authority adjudications;
- interval/request identities.

A shared parser helper, shared projection helper, generated copy, port derived from the other path, or common invariant evaluator yields:

~~~text
overall_independence_verdict = BLOCKED
~~~

and FULL_INTERVAL_QUALIFIED cannot PASS.

### Execution binding

Every DiagnosticResult must include:

~~~text
diagnostic_independence_manifest_id
diagnostic_independence_manifest_seal
implementation_stage_hashes
~~~

QualificationExecutionResult and authority_scope_tuple must bind the exact independence manifest ID/seal.

---

## 3. F03 correction — DurableEvidencePolicy

Future execution requires a sealed durability policy before the first request.

~~~text
schema =
B_FIQ_01_DURABLE_EVIDENCE_POLICY_V0_2

policy_id
policy_version

allowed_storage_classes[]
content_addressing_rule
immutable_versioning_rule
retention_requirement
retrieval_verification_method
repository_binding_requirement
access_control_requirement
audit_recovery_requirement
object_reference_encoding_rule
credential_non_persistence_rule

body_persistence_deadline_rule
temporary_staging_policy
failure_if_persistence_deadline_missed

created_at_utc
policy_seal
~~~

Minimum semantics:

~~~text
content_addressing_rule =
SHA256(exact body bytes)

temporary workflow artifacts =
staging only, never sufficient authority

body_persistence_deadline_rule =
every body required by a candidate PASS
must enter allowed durable storage
before QualificationExecutionResult can close PASS-candidate

failure_if_persistence_deadline_missed =
BLOCKED_INTEGRITY
~~~

Every DurableEvidenceObject record must bind:

~~~text
durable_evidence_policy_id
durable_evidence_policy_seal
raw_sha256
byte_length
durable_content_address
retrieval_verification_status
object_record_seal
~~~

Policy ID/seal are mandatory in:

- QualificationExecutionResult;
- CompletenessProof;
- authority_scope_tuple;
- every evidence-object record.

A policy change requires new execution/adjudication lineage.

---

## 4. F04 correction — closed QualificationExecutionResult and evidence membership

Future exhaustive execution must close one exact evidence set.

### 4.1 Deterministic evidence production cardinality

For every RequestManifest REQUIRED row, execution must emit exactly:

~~~text
1 TransportCapture
1 DiagnosticAResult
1 DiagnosticBResult
1 IntervalTerminalRecord
~~~

Diagnostic result records are mandatory even when diagnostics cannot run.

Allowed non-run diagnostic record:

~~~text
diagnostic_status = NOT_RUN
reason_code = exact upstream blocking reason
raw_response_sha256_or_null
diagnostic_result_seal
~~~

Thus execution failure cannot erase the expected diagnostic evidence identity.

For every RequestManifest CLOSED row, execution emits exactly:

~~~text
1 IntervalTerminalRecord
~~~

and zero TransportCapture/DiagnosticResult records.

No other execution-produced evidence record is admissible outside the closed registries below.

### 4.2 Deterministic evidence record identities

All execution-produced evidence IDs must be deterministic functions of:

~~~text
execution_lineage_id
interval_id
record_type
diagnostic_path_id_if_applicable
attempt_ordinal = 0
~~~

No second attempt ID exists inside one lineage.

### 4.3 QualificationExecutionResult

~~~text
schema =
B_FIQ_01_QUALIFICATION_EXECUTION_RESULT_V0_2

execution_result_id
execution_lineage_id

contract_id
contract_version

interval_inventory_id
interval_inventory_root

request_manifest_id
request_manifest_root
request_manifest_seal

provider_delivery_identity_policy_id
provider_delivery_identity_policy_seal

representation_regime_manifest_id
representation_regime_manifest_seal

transport_policy_id
transport_policy_seal

request_budget_id
request_budget_seal

execution_shard_plan_id
execution_shard_plan_seal

diagnostic_independence_manifest_id
diagnostic_independence_manifest_seal

durable_evidence_policy_id
durable_evidence_policy_seal

semantic_invariant_manifest_id
semantic_invariant_manifest_seal

qualified_empty_rule_id_or_null
qualified_empty_rule_seal_or_null

transport_capture_registry[]
  record_id
  record_seal

diagnostic_A_registry[]
  record_id
  record_seal

diagnostic_B_registry[]
  record_id
  record_seal

interval_terminal_registry[]
  record_id
  record_seal

durable_evidence_object_registry[]
  record_id
  record_seal

request_count
shard_completion_states

evidence_set_digest
qualification_capture_set_root_sha256
candidate_FULL_INTERVAL_verdict
limitations

created_at_utc
execution_result_seal
~~~

### 4.4 Evidence-set digest

~~~text
evidence_set_digest =
SHA256(
  canonical_json({
    exact sorted transport_capture_registry,
    exact sorted diagnostic_A_registry,
    exact sorted diagnostic_B_registry,
    exact sorted interval_terminal_registry,
    exact sorted durable_evidence_object_registry
  })
)
~~~

Sorting key is exact record ID lexical order.

The digest binds all execution-produced evidence required by deterministic cardinality rules.

A record may not be omitted because it is unfavorable.

A duplicate record ID, missing required record, unexpected extra record, or record seal mismatch yields:

~~~text
candidate_FULL_INTERVAL_verdict = BLOCKED
~~~

### 4.5 CompletenessProof binding

CompletenessProof must include:

~~~text
qualification_execution_result_id
qualification_execution_result_seal
evidence_set_digest
request_manifest_root
qualification_capture_set_root_sha256
~~~

It must prove deterministic registry cardinalities from RequestManifest row counts.

### 4.6 Operational adjudication binding

OperationalApplicabilityAdjudication must include:

~~~text
qualification_execution_result_id
qualification_execution_result_seal
evidence_set_digest
~~~

An adjudication cannot select a subset of execution evidence.

---

## 5. authority_scope_tuple additions

The parent authority_scope_tuple is extended with:

~~~text
request_manifest_id
request_manifest_root
request_manifest_seal

diagnostic_independence_manifest_id
diagnostic_independence_manifest_seal

durable_evidence_policy_id
durable_evidence_policy_seal

qualification_execution_result_id
qualification_execution_result_seal
evidence_set_digest
~~~

Downstream exact-match semantics remain unchanged.

---

## 6. qualification_capture_set leaf correction

For every provider-request interval, the leaf additionally binds:

~~~text
request_manifest_row_identity
exact_request_locator
provider_delivery_endpoint_identity
transport_capture_id
diagnostic_A_result_id
diagnostic_B_result_id
interval_terminal_record_id
durable_evidence_object_id_or_null
~~~

For calendar-closed intervals, the leaf binds:

~~~text
request_manifest_row_identity
interval_terminal_record_id
~~~

Therefore the capture-set root cannot be constructed from anonymous favorable summaries.

---

## 7. Correction status

Closed:

~~~text
BFIQ01-F01
BFIQ01-F02
BFIQ01-F03
BFIQ01-F04
~~~

Final persisted-head adversarial re-break remains required.

No provider request, exhaustive qualification, D materialization or backtest occurred.
