# SESSION BACKUP — 2026-09-20 — B-PE-01 EVIDENCE CONTRACT PASS

## 0. Recovery

Repository:

`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch:

`integration/system-v1`

Starting HEAD:

`a6e2206426b1229eb454dd224858b5934383d0e3`

Starting action:

```text
B-PE-01 — native BI5 provider-sensitive physical semantics evidence contract
```

No provider evidence, BI5 payload or real acquisition was used.

## 1. Initial candidate

Commit:

`9d2a7bbb5e42af5261e2881c050f9442b998c5cb`

Initial candidate blob:

`d21ce35fe9acdcdc1b3b0828bb2525f75c15054a`

## 2. Initial adversarial break

Commit:

`47bd9055ba42a2bfe810d7c7e6d40a35cb9248c4`

Adversarial blob:

`a8bdb682b7d00eae4ca3c6b7c3fd839903117879`

Eight defects demonstrated:

```text
BPE-F01 SINGLE_PROVIDER_ESCAPE_UNDERCUTS_INDEPENDENCE_REQUIREMENT
BPE-F02 CLAIM_SUPPORT_CAN_BE_SELF_ASSERTED_WITHOUT_EXACT_SOURCE_ANCHOR
BPE-F03 LINEAGE_INDEPENDENCE_IS_SELF_ASSERTED
BPE-F04 TARGET_PROVIDER_SCOPE_VERSION_BINDING_NOT_CONCRETE_ENOUGH
BPE-F05 C07_MIXES_PROVIDER_FACT_WITH_PROJECT_DECODER_BEHAVIOR
BPE-F06 BROAD_CLAIM_CAN_PASS_WITH_UNPROVEN_REQUIRED_DIMENSION
BPE-F07 NO_CLOSED_PERSISTED_ADJUDICATION_OUTPUT_EVIDENCE_SET_BINDING
BPE-F08 POST_PASS_CONFLICT_SUPERSESSION_SEMANTICS_INCOMPLETE
```

## 3. First correction and re-break

First correction commit:

`98d0b09ed1a7ce548e772ba4c8c8ce0982e5fc2d`

First corrected blob:

`bd439862a57e7fa3cd3712b258cdef1efafa0810`

Persisted-head re-break commit:

`79ab840d2e9a9616c7bb262457704162cf7ad289`

Re-break blob:

`6fa8b9efdaadaa25fd9b10ab41622780e34601d4`

Residual defects:

```text
BPE-R01 INTEGRITY_DIGEST_AND_SEAL_CANONICALIZATION_DEFERRED
BPE-R02 SOURCE_ADMISSIBILITY_IS_NOT_A_PERSISTED_DECISION
BPE-R03 REOPEN_REQUIRED_EVENT_HAS_NO_CLOSED_SCHEMA_CURRENT_AUTHORITY_RULE
```

## 4. Residual correction

Commit:

`2dc7c9fff14efc9597797775cf8ed92878ed6456`

Final candidate blob:

`278a691b17cdd4b37e9c0e739f0fe9b56f014b29`

Corrections:

- SHA-256 exact-byte and canonical JSON integrity semantics;
- EvidenceAdmissibilityDecision with ADMISSIBLE/REJECTED/BLOCKED;
- sealed ProviderEvidenceReopenEvent;
- deterministic current-authority predicate.

## 5. Final persisted-head re-break

Final report:

`reports/data-qualification/bpe01_native_bi5_provider_evidence_contract_final_rebreak_2026-09-20.md`

All F01-F08/R01-R03 attacks and cross-attacks survived.

No new defect demonstrated.

Final verdict:

```text
B-PE-01 EVIDENCE CONTRACT = PASS
```

Provider claims remain:

```text
C01-C08 = NOT ADJUDICATED
B global executable gate = BLOCKED
```

## 6. Exactly one next governed action

Open only:

```text
B-PE-02 — native BI5 provider/reference evidence collection and C01-C08 adjudication
```

Scope:

- gather documentary/reference evidence only under the qualified B-PE-01 contract;
- create immutable source records and exact claim anchors;
- resolve evidence lineage/independence;
- adjudicate every mandatory dimension and C01-C08 claim;
- no project BI5 download or project acquisition.

No real data execution is authorized.
