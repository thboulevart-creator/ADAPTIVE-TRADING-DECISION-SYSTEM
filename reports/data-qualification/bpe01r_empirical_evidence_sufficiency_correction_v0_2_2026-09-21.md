# B-PE-01R — EMPIRICAL SUPERSESSION — CORRECTION RECORD V0.2

**Date:** 2026-09-21  
**Parent candidate blob:** `0a9ed4c6bcb921910f287da4646d5870061b9a31`  
**Adversarial break blob:** `6435acc3f87bacea8f8aeabbf704f5d626cdd1f2`  
**Scope:** closes only BPE01R-F01 through BPE01R-F03.

This record is normative over the parent candidate where they differ.

The corrected composite candidate identity is:

```text
B_PE_01R_OPERATIONAL_EMPIRICAL_SUPERSESSION_V0_2_CORRECTED
=
parent candidate
+
this correction record
```

No other parent-candidate requirement is weakened.

---

## 1. F01 correction — capture set, not atomic provider snapshot

Every occurrence of:

```text
qualification snapshot
provider archive snapshot
qualification_snapshot_root_sha256
```

in the parent candidate is superseded by:

```text
qualification capture set
qualification_capture_set_root_sha256
```

### 1.1 Exact semantics

```text
qualification_capture_set
=
the exact ordered set of provider response evidence captured by the project
for the sealed FULL_D_REPRESENTATION_DOMAIN inventory,
with each component retaining its own retrieval timestamp and provenance.
```

It establishes:

- what exact bytes/dispositions the project captured;
- which provider locator was requested for each interval;
- when each response was captured;
- how each response was classified;
- which exact bytes may later be consumed by D.

It does **not** establish:

```text
all provider objects coexisted simultaneously
in one atomic provider-side archive snapshot
```

and no such atomicity may be claimed from this path.

### 1.2 Capture-set root

The canonical ordered capture-set leaf for each interval is:

```text
{
  interval_id,
  representation_regime_id,
  provider_locator,
  retrieval_started_at_utc,
  retrieval_completed_at_utc,
  disposition,
  raw_sha256_or_qualified_empty_identity,
  capture_seal,
  diagnostic_seals
}
```

The exact ordered canonical leaf list yields:

```text
qualification_capture_set_root_sha256
```

The root proves the identity of the project's sequential capture set only.

### 1.3 D binding

D may use the operational supersession only when:

```text
D consumes the exact qualified captured bytes
OR
D re-retrieves and proves exact raw-hash equality
for every materialized component
```

Thus downstream validity is tied to exact evidence, not to an unproven atomic provider state.

### 1.4 Point-in-time atomicity boundary

If a future project objective requires:

```text
all components proven to have existed simultaneously
in one provider-atomic point-in-time archive state
```

then:

```text
BPE-C08-OP-V0.2 is insufficient
```

unless provider-atomicity is separately qualified.

---

## 2. F02 correction — closed successor adjudication state machine

A successor operational PASS must be represented by a sealed adjudication.

### 2.1 OperationalApplicabilityAdjudication

```text
schema =
B_PE_01R_OPERATIONAL_APPLICABILITY_ADJUDICATION_V0_2

adjudication_id
successor_contract_id
successor_contract_version
authority_scope_tuple
authority_scope_tuple_digest
qualification_capture_set_root_sha256
interval_inventory_root
evidence_record_ids
evidence_record_seals
C08_D4_OP_verdict
C08_D5_OP_verdict
BPE_C08_OP_verdict
material_contradiction_status
limitations
created_at_utc
adjudication_seal
```

Allowed dimension/claim verdicts:

```text
PASS
FAIL
BLOCKED
```

No majority vote.

The adjudication seal is:

```text
SHA256(canonical_json(adjudication_without_adjudication_seal))
```

using the inherited B-PE-01 canonical JSON rule.

### 2.2 OperationalEvidenceReopenEvent

```text
schema =
B_PE_01R_OPERATIONAL_EVIDENCE_REOPEN_EVENT_V0_2

event_id
target_adjudication_id
target_adjudication_seal
trigger_type
trigger_evidence_refs
event_status = OPEN | CLOSED
opened_at_utc
closed_by_adjudication_id_if_any
reason_codes
event_seal
```

Mandatory trigger classes include:

```text
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
```

Any OPEN event makes the historical operational PASS non-authoritative for new promotion.

### 2.3 OperationalAdjudicationSupersession

```text
schema =
B_PE_01R_OPERATIONAL_ADJUDICATION_SUPERSESSION_V0_2

supersession_id
prior_adjudication_id
prior_adjudication_seal
successor_adjudication_id
successor_adjudication_seal
reason_codes
created_at_utc
supersession_seal
```

A superseded adjudication remains historical evidence but has zero current promotion authority.

### 2.4 Current-authority predicate

An operational adjudication is current authority iff all are true:

```text
adjudication.BPE_C08_OP_verdict == PASS

AND adjudication.successor_contract_id/version
    == exact downstream-required successor contract identity

AND adjudication.authority_scope_tuple_digest
    == digest(exact downstream authority_scope_tuple)

AND adjudication.qualification_capture_set_root_sha256
    == downstream-bound qualification capture-set root

AND no later OperationalAdjudicationSupersession
    supersedes this adjudication

AND no OperationalEvidenceReopenEvent
    targeting this adjudication is OPEN

AND every applicable C01-C07 adjudication referenced by the scope tuple
    is itself current authority

AND evidence/capture integrity re-verification = PASS
```

If any predicate term is false:

```text
BPE-C08-OP-V0.2
is not current authority for new downstream promotion.
```

---

## 3. F03 correction — exact authority-scope tuple

The successor contract must bind one immutable scope tuple.

```text
schema =
B_PE_01R_OPERATIONAL_AUTHORITY_SCOPE_TUPLE_V0_2

provider_identity
instrument_identity
representation_rule_identity

full_d_representation_domain_identity
execution_window_freeze_identity
warmup_rule_identity
session_calendar_identity
interval_inventory_root

provider_delivery_identity_policy_id
locator_manifest_id
transport_policy_id

applicable_C01_C07_adjudications[]
  claim_id
  adjudication_id
  adjudication_seal
  current_authority_required = true

qualified_empty_rule_id_if_used
qualified_empty_rule_seal_if_used

qualification_capture_set_root_sha256

successor_contract_id
successor_contract_version
```

Canonical tuple digest:

```text
authority_scope_tuple_digest =
SHA256(canonical_json(authority_scope_tuple))
```

### 3.1 Exact-match downstream rule

The operational alternative may satisfy the C08 prerequisite for downstream B/D only when:

```text
downstream_required_authority_scope_tuple_digest
==
operational_adjudication.authority_scope_tuple_digest
```

No partial/superset/subset inference is allowed.

### 3.2 Any scope change requires new adjudication

Any change in any tuple member, including:

- instrument;
- research window;
- warmup;
- session calendar;
- representation rule;
- locator policy;
- transport policy when evidential meaning changes;
- interval inventory;
- C01-C07 current-authority adjudication;
- qualified-empty rule;
- capture-set root;
- successor contract version;

requires a new operational adjudication.

No prior PASS is inherited.

---

## 4. Corrected archive-mutation semantics

The parent candidate's mutation rule is refined to:

```text
qualified capture set A
→ remains historical evidence of exact bytes A

later same-locator retrieval yields bytes B != A
→ ARCHIVE_MUTATION_DETECTED
→ OPEN OperationalEvidenceReopenEvent
→ A cannot authorize a new D/backtest promotion

already completed research explicitly bound to bytes A
→ remains an accurate statement about bytes A
→ must not be relabeled as provider-current evidence
```

No provider-atomic snapshot claim exists.

---

## 5. Corrected downstream alternative

For the operational historical-backtest pipeline only:

```text
C08 prerequisite may be satisfied by:

A. current-authority BPE-C08 V0.1 documentary PASS

OR

B. current-authority BPE-C08-OP-V0.2 PASS
   whose authority_scope_tuple digest exactly matches
   the downstream required scope tuple
```

This does not modify C01-C07.

It does not convert documentary C08-D4/D5 to PASS.

---

## 6. Correction status

Closed:

```text
BPE01R-F01
BPE01R-F02
BPE01R-F03
```

Decision remains candidate:

```text
VERSIONED_EMPIRICAL_SUPERSESSION
```

Final persisted-head adversarial re-break is still required.

No new BI5 request, exhaustive qualification, D materialization or backtest occurred.
