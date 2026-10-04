# P1-17 — CLAIM-SCOPED QUALIFIED PRODUCER EXECUTION BOUNDARY — ARCHITECTURE SELECTION V0.1

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Authorized parent HEAD:** `9e104a74dd9ccfee1d3a38e7b4786a817e51d1fe`  
**Authorized parent TREE:** `91aed9f7ccd138201584c5eac8a19a85c2b08b11`  
**Status:** `DOCUMENTARY ARCHITECTURE SELECTED — IMPLEMENTATION NOT AUTHORIZED`

## 1. Fresh-state result

The authorized parent was verified exactly before P1-17 analysis. The required RVO-05, DATA-02, P1.10B/P1.11B/P1.12B, AP1 and current Research Execution identities matched the authorization.

No real AP1 execution, market-result production, backtest or OOS consumption occurred.

## 2. Exact current boundary

The existing P1 chain is not generically executable even though its resource-binding stages are relatively generic.

```text
ExperimentSpecification
        ↓
P1.10B ExperimentExecutionBinding
        ↓
P1.11B QualifiedExperimentExecutionInput
        ↓
P1.12B LinkedExperimentExecution
        ↓
run_qualified_research
        ↓
BI5ResearchEngine
        ↓
*.bi5 only
```

Therefore the previously observed RVO-05 blocker is confirmed structurally:

```text
AP0 IDENTITY BINDING =
SUPPORTED BY P1.10B / P1.11B

AP0/AP1 EXECUTION THROUGH P1.12B =
UNSUPPORTED

BLOCKER =
BLOCKED_P1_TARGET_EXECUTION_SURFACE_UNSUPPORTED
```

## 3. AP1 producer properties relevant to this decision

The exact producer is:

```text
ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1
BLOB =
9f613063fb8a190a1ff6f2f8b12c97c4ed97712a
```

It is currently a standalone CLI. It binds itself to the exact AP0 manifest and dataset identity, rehashes all input files, checks schema/metadata/order/segments, calculates only the descriptive census, and writes one JSON result with schema `ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1`.

It does not expose a P1-native execution result, P1 experiment IDs, a producer execution receipt, or a P1 result attestation.

## 4. OPTION A vs OPTION B

### OPTION A — P1 invokes a qualified producer

```text
P1.11B qualified experiment input
        ↓
P1.12C producer-execution plan
        ↓
exact DATA-02 admission
        ↓
exact producer identity + exact runtime lock
        ↓
controlled producer invocation
        ↓
output byte/content verification
        ↓
source pre/post immutability verification
        ↓
P1.12C qualified producer execution result
```

Strengths:

- P1 remains the owner of the experiment execution lifecycle.
- The exact producer is executed under a pre-result plan rather than selected after output exposure.
- The producer code blob, dataset admission, parameters, environment and output bytes can be bound into one result identity.
- No trust in filename, path or caller-supplied result claims is required.
- The AP1 computation stays in AP1; P1 does not duplicate its logic.
- A content-addressed proof may later be persisted, but it remains evidence rather than authority.

Costs / new surface:

- P1 needs one narrowly scoped controlled producer-runner capability.
- Runtime/dependency identity must include Python, NumPy, PyArrow and timezone-data identity.
- P1.13B is currently exact-type coupled to P1.12B and therefore cannot consume a new P1.12C result without a later downstream owner change.

### OPTION B — P1 admits an externally executed cryptographically bound producer result

A checksum can establish content integrity. It cannot establish that the result was actually produced by the claimed code over the claimed source.

The repository already contains the P0.5 durable-replay rule:

```text
PERSISTED PROOF
!=
DOWNSTREAM AUTHORITY

EXTERNAL CLAIM
→ independent source-byte revalidation
→ deterministic replay
→ exact comparison
→ fresh local attestation
```

No qualified signing trust root/key lifecycle exists in the current relevant architecture.

Therefore OPTION B has only two forms:

1. **digest-only admission** — insufficient and rejected;
2. **external proof + deterministic replay by P1** — safe in principle, but the replay requires P1 to execute the exact producer anyway.

The second form is OPTION A plus an extra persistence/transport layer.

## 5. Architecture decision

```text
OPTION A =
SELECTED

OPTION B DIGEST-ONLY =
REJECTED

OPTION B WITH REPLAY =
DOMINATED AS PRIMARY EXECUTION ARCHITECTURE
```

This is not a discretionary trade-off requiring a human normative choice: under the repository's existing trust model, B without replay is insufficient and B with replay adds machinery to A without removing the need for A.

## 6. P1.12B extension vs sibling boundary

Extending P1.12B is rejected.

P1.12B has BI5-specific result semantics:

- `files_consumed`;
- `ticks_consumed`;
- first/last decoded tick timestamps;
- `stream_sha256` over decoded BI5 ticks.

Reusing those fields for an AP1 JSON producer would silently change their meaning.

Therefore:

```text
P1.12B =
KEEP UNCHANGED

TARGET =
P1.12C — CLAIM-SCOPED QUALIFIED PRODUCER EXECUTION BOUNDARY V1
```

P1.12C is a sibling boundary, not a replacement and not a generic process framework.

## 7. Critical downstream consequence

P1.13B currently requires:

```text
type(execution_result) is LinkedExperimentExecutionResult
AND
current P1.12B factory attestation
```

Therefore a correctly distinct P1.12C result cannot be silently passed into P1.13B.

This is an explicit second owner gap:

```text
P1.12C RESULT
→ P1.13B
=
BLOCKED_BY_EXACT_RESULT_TYPE_CONTRACT
```

P1-17 does not solve this by forging a P1.12B result.

A later separately authorized P1 downstream maturation must decide between:

- a sibling producer-aware evaluation boundary; or
- a carefully generalized common qualified-execution-result interface.

That future choice is outside P1-17.

## 8. Selected P1.12C input model

The pre-result execution plan must bind, before producer output exposure:

```text
experiment_execution_input_id
execution_binding_id
experiment_spec_id
request_id
revision_id
audit_id
scope_id

DATA02_ADMISSION_DIGEST
claim_scope_id
dataset_identity
ap0_manifest_sha256
dataset_file_set_digest
schema_identity
source_identity
usage_envelope_id

producer_id
producer_code_blob
producer_entrypoint
producer_semantic_parameter_digest
producer_invocation_contract_digest

runtime_lock_digest
python_version
numpy_version
pyarrow_version
timezone_database_identity
deterministic_environment_digest

expected_output_schema
expected_output_contract
maximum_output_bytes

result_exposed = false
execution_authority = false
trading_authority = false
capital_authority = false
```

Filesystem paths are transport handles, not identity.

## 9. Selected P1.12C result model

A qualified producer execution result must contain at minimum:

```text
producer_execution_result_id
producer_execution_plan_digest

experiment_execution_input_id
execution_binding_id
experiment_spec_id
request_id
revision_id
audit_id
scope_id

DATA02_ADMISSION_DIGEST
dataset_identity
dataset_file_set_digest_before
dataset_file_set_digest_after

producer_id
producer_code_blob
producer_parameter_digest
runtime_lock_digest

execution_status
exit_code

output_schema
output_size_bytes
output_sha256
result_identity
DATA02_RESULT_BINDING_DIGEST

producer_stdout_digest
producer_stderr_digest

reconstruction_class
reconstruction_descriptor_digest

scientific_authority = false
operational_authority = false
trading_authority = false
capital_authority = false
```

`dataset_file_set_digest_before == dataset_file_set_digest_after` is mandatory.

`EXECUTED` means only that the qualified producer execution completed and the exact output passed structural/identity checks.

## 10. AP1 output admission

For the exact AP1 producer, P1.12C must require:

- output bytes exist and are within the AP1 32 MiB cap;
- exact JSON schema `ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1`;
- status `AP1_COMPLETE`;
- input identity `USTECH_PROFILE_MINUTE_CORE_V0_1`;
- exact AP0 manifest SHA-256;
- exact producer output byte SHA-256;
- exact Data result binding through DATA-02;
- runtime identity compatible with the pre-result lock.

The output path or filename cannot grant identity.

## 11. Reconstructibility

The selected model follows the repository's existing durable-replay principle.

A durable producer execution proof is non-authoritative by itself.

Exact replay requires:

```text
same qualified experiment input identity
+ same DATA-02 admission identity
+ same dataset bytes
+ same producer blob
+ same semantic parameters
+ same runtime/dependency lock
+ same deterministic environment
→ same accepted output identity
```

A replay mismatch blocks.

`RUNTIME_ATTESTATION != DURABLE_RECONSTRUCTION`.

## 12. Synthetic testability finding

There is a material implementation-readiness constraint.

The exact AP1 helper hard-codes the real first-use surface:

- 61 files;
- 1,709,180 minute rows;
- 376,003,618 source ticks;
- 1,606 segments;
- exact AP0 manifest identity;
- exact F2 spread reconciliation constants.

Therefore a small synthetic fixture cannot truthfully masquerade as the exact AP1 producer input.

The future P1.12C boundary can be test-first qualified with a **separate synthetic test producer** having its own identity and schema. That can qualify producer-selection, invocation, immutability, output identity and authority boundaries.

It does **not** qualify exact AP1 compatibility.

```text
GENERIC P1.12C SYNTHETIC IMPLEMENTATION READINESS =
READY

EXACT AP1 SYNTHETIC EXECUTION QUALIFICATION =
BLOCKED_BY_AP1_FIXED_REAL_SURFACE

EXACT AP1 REAL EXECUTION =
NOT AUTHORIZED
```

## 13. Additional implementation prerequisite

AP1 records NumPy/PyArrow versions but the selected future boundary requires a pre-execution runtime lock, not merely post-result observation.

Before exact AP1 execution, P1.12C must bind an AP1-sufficient runtime identity including timezone-data identity.

This is a prerequisite, not permission to create it under P1-17.

## 14. Mandatory distinctions

```text
DATA_ADMISSION != PRODUCER_EXECUTION
PRODUCER_EXECUTION != P1_FINDING
EXECUTED != SUPPORTED
SUPPORTED != VALIDATED_STRATEGY
AVAILABLE_PRODUCER != QUALIFIED_PRODUCER
QUALIFIED_PRODUCER != AUTHORIZED_REAL_EXECUTION
RUNTIME_ATTESTATION != DURABLE_RECONSTRUCTION
P1_AUTHORITY != TRADING_AUTHORITY
```

## 15. P1-17 verdict

```text
ARCHITECTURE_SELECTION =
OPTION_A

BOUNDARY_SELECTION =
P1.12C SIBLING

P1.12B_MODIFICATION =
REJECTED

OPTION_B_AS_PRIMARY =
REJECTED

GENERIC_SYNTHETIC_IMPLEMENTATION_READINESS =
READY_FOR_SEPARATE_TEST_FIRST_AUTHORIZATION

EXACT_AP1_SYNTHETIC_QUALIFICATION =
BLOCKED

P1.13B_DOWNSTREAM_COMPATIBILITY =
BLOCKED

REAL_AP1_EXECUTION =
NOT_AUTHORIZED
```

P1-17 stops before implementation.
