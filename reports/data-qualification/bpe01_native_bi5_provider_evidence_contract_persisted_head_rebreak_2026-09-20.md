# B-PE-01 — CORRECTED EVIDENCE CONTRACT — PERSISTED-HEAD ADVERSARIAL RE-BREAK

**Date:** 2026-09-20  
**Corrected candidate blob:** `bd439862a57e7fa3cd3712b258cdef1efafa0810`  
**Corrected candidate commit:** `98d0b09ed1a7ce548e772ba4c8c8ce0982e5fc2d`  
**Scope:** contract re-break only. No provider evidence gathered. No BI5 processed.

## 1. Re-break of previously demonstrated defects

The corrected candidate successfully closes:

```text
BPE-F01 — singleton provider escape
BPE-F02 — unanchored/self-asserted claim support
BPE-F03 — self-asserted lineage independence
BPE-F04 — insufficient target scope/version binding
BPE-F05 — C07 provider/project-decoder conflation
BPE-F06 — broad claim with unproven dimension
BPE-F07 — missing adjudication output/evidence-set binding
BPE-F08 — incomplete post-PASS supersession semantics
```

No regression of those eight defects was demonstrated.

## 2. Residual defects

### BPE-R01 — INTEGRITY_DIGEST_AND_SEAL_CANONICALIZATION_DEFERRED

Attack:

Construct two logically identical adjudication objects with different JSON member ordering/whitespace or two different evidence-set serializations.

The corrected candidate names:

- `content_integrity_digest`;
- `anchor_integrity_digest`;
- `evidence_set_digest`;
- `assertion_set_digest`;
- `lineage_resolution_integrity_digest`;
- `adjudication_seal`;

but explicitly defers canonical sealing rules.

Result:

The same logical adjudication can acquire multiple seals, or incompatible implementations can hash different projections while each claims conformance.

Verdict:

`DEMONSTRATED RESIDUAL DEFECT`.

Required correction:

Fix digest algorithm/domain and canonical JSON projection rules now, including which seal field is excluded from its own hash.

---

### BPE-R02 — SOURCE_ADMISSIBILITY_IS_NOT_A_PERSISTED_DECISION

Attack:

Include a source record in `evidence_records` whose source bytes are pinned but whose evidence class, immutable provenance, scope or project-origin status is invalid.

The corrected contract describes admissibility rules, but no closed persisted per-source admissibility object/status is required.

Result:

A later dimension adjudication can accidentally consume an inadmissible source without leaving an explicit fail-closed source-level decision.

Verdict:

`DEMONSTRATED RESIDUAL DEFECT`.

Required correction:

Create an `EvidenceAdmissibilityDecision` per source with exact status:

`ADMISSIBLE | REJECTED | BLOCKED`

and reason code/domain. Only ADMISSIBLE sources may contribute assertions to dimension PASS/FAIL.

---

### BPE-R03 — REOPEN_REQUIRED_EVENT_HAS_NO_CLOSED SCHEMA / CURRENT-AUTHORITY RULE

Attack:

After a current PASS, submit new conflicting evidence and merely state that a `REOPEN_REQUIRED` event exists.

The corrected contract does not define:

- event identity;
- exact prior adjudication binding;
- triggering evidence binding;
- event status;
- seal;
- rule for deciding whether an unresolved event exists.

Result:

Downstream B cannot deterministically verify that an adjudication remains current authority.

Verdict:

`DEMONSTRATED RESIDUAL DEFECT`.

Required correction:

Define a sealed `ProviderEvidenceReopenEvent` and current-authority predicate. An OPEN event against a PASS makes current provider authority BLOCKED until a superseding adjudication closes it.

---

## 3. Re-break verdict

```text
B-PE-01 CORRECTED EVIDENCE CONTRACT = FAIL
```

Reason:

Three persistence/control-plane defects remain.

No provider-truth claim C01-C08 was adjudicated.

## 4. Allowed correction scope

Correct only:

```text
BPE-R01
BPE-R02
BPE-R03
```

No evidence gathering and no production/runtime mutation.
