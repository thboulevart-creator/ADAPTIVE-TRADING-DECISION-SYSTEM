# Q-RM-08 — Concrete Acquisition-Domain Declaration Template V1

**Status:** EXECUTABLE TEMPLATE — NOT A QUALIFIED ACQUISITION
**Version:** V1
**Date:** 2026-09-05
**Purpose:** provide the exact evidence container required to close Q-RM-08 without inventing project-specific acquisition facts.

## 1. Gate

A declaration is eligible for qualification only when every mandatory field is populated by verifiable evidence.

Until then:

`Q-RM-08 PROJECT-SPECIFIC ACQUISITION = BLOCKED`

No default provider, file set, date range, partition rule, or representation is inferred by this template.

## 2. Acquisition identity

```yaml
acquisition_id: <MANDATORY>
acquisition_version: <MANDATORY>
status: DRAFT | QUALIFIABLE | QUALIFIED | REJECTED
owner: <MANDATORY>
declared_at: <MANDATORY>
```

`acquisition_id` identifies the declared acquisition domain; it is not a filename, path, worker, chunk, hash, or physical ordering primitive.

## 3. Scope declaration

```yaml
asset_id: <MANDATORY>
instrument: <MANDATORY>
granularity: <MANDATORY>
market_scope: <MANDATORY>
market_time_reference: <MANDATORY>
expected_period:
  from: <MANDATORY>
  to: <MANDATORY>
```

The scope must be evidenced independently of filenames.

## 4. Complete component manifest

Every physical component belonging to the acquisition must be enumerated.

```yaml
components:
  - component_id: <MANDATORY>
    source_reference: <MANDATORY>
    representation: <MANDATORY>
    representation_version: <MANDATORY_OR_EXPLICIT_UNKNOWN>
    acquisition_role: PRIMARY | SUPPORTING | OTHER
    expected_content_scope: <MANDATORY>
    content_anchor: <MANDATORY_WHEN_AVAILABLE>
```

A worker, partition, file, object, archive, or stream is not automatically an acquisition domain. Membership must be declared and evidenced.

## 5. Completeness claim

The declaration must answer:

- Why is this component set complete for the declared acquisition domain?
- What evidence proves no required component is missing?
- What evidence distinguishes an empty component from a failed acquisition?
- Are partitions/chunks merely physical subdivisions of one acquisition?

Required field:

```yaml
completeness_evidence: <MANDATORY>
```

Absence of evidence => `BLOCKED`.

## 6. Acquisition boundaries

The domain must define what is inside and outside the acquisition.

```yaml
in_scope_rule: <MANDATORY>
out_of_scope_rule: <MANDATORY>
partition_fusion_rule: <MANDATORY>
reacquisition_rule: <MANDATORY>
```

Separate reacquisitions are not fused merely because their content is equal.

## 7. Failure-domain interface

Q-RM-04 evaluates anomaly impact against this declared acquisition domain.

```yaml
acquisition_fatal_classes: <MANDATORY>
unknown_scope_policy: QUALIFICATION_BLOCKED
```

This section may not weaken the universal Q-RM-04 rule.

## 8. Representation interface

```yaml
record_model_version: <MANDATORY>
format_binding_id: <MANDATORY>
format_binding_version: <MANDATORY>
qualification_contract_id: <MANDATORY>
qualification_contract_version: <MANDATORY>
```

Unknown, unsupported, incomplete, or contradictory dependencies prevent qualification.

## 9. Evidence requirements

A concrete declaration must be backed by evidence sufficient to reconstruct:

`acquisition domain → components → representations → record model → binding → qualification`

The following are explicitly insufficient alone:

- filename patterns;
- directory layout;
- parser defaults;
- library behavior;
- worker/chunk boundaries;
- content hash used as semantic identity;
- intended meaning;
- undocumented operator knowledge.

## 10. Qualification decision

```text
Q-RM-08 = PASS
only if the declared acquisition domain is complete, deterministic,
versioned, reconstructible, and evidenced.

Otherwise = BLOCKED.
```

`REJECTED` is reserved for a concrete declaration that has been evaluated and shown non-conforming; missing evidence is `BLOCKED`, not `REJECTED`.

## 11. Current project status

No project-specific acquisition declaration is promoted by this template.

The repository currently contains a non-normative provenance proposal and a provisional data contract; neither is silently promoted into this concrete declaration.

Therefore the current status remains:

**Q-RM-08 PROJECT-SPECIFIC ACQUISITION = BLOCKED**

## 12. Next admissible action

Populate this declaration from actual acquisition evidence. Then derive Q-RM-09 concrete format binding and Q-RM-10 concrete anomaly matrix from the declared representation(s).

Do not create canonical record positions before Q-RM-08 → Q-RM-10 and the qualification/freeze prerequisites are closed.
