# MCEPR — ACTIVATION CONTRACT V0.1 — DOCUMENTARY QUALIFICATION

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Qualification base HEAD:** `5e75ee3b116269643f94c42534bcbf36957eab98`  
**Qualification base TREE:** `4f8048416eabdbfbf90631d02872c7e40b689ad9`

## 1. Qualified contract

```text
PATH =
GOVERNANCE/MCEPR-ACTIVATION-CONTRACT-V0.1.json

BLOB =
cf235747fc5218a3f1b492159f82593a6ee51392

STATUS =
DOCUMENTARY_CONTRACT_QUALIFIED
```

No cutover record, registry segment, real event, real relation, backfill, producer, consumer or runtime integration was created.

## 2. Selected activation model

```text
ACTIVATION_MODEL =
FORWARD_FIRST

OPERATOR_MODEL =
MANUAL_FIRST

SYNTHETIC_BOOTSTRAP_GENESIS =
FORBIDDEN

BACKFILL =
SEPARATE_FUTURE_FRONTIER

AUTOMATION =
SEPARATE_FUTURE_FRONTIER
```

The register starts from future reality rather than from a reconstruction exercise.

## 3. Cutover correction

The documentary review rejected making the activation-contract commit itself an implicit cutover.

That would blur:

- contract qualification;
- activation;
- the exact instant from which forward events become admissible.

V0.1 therefore defines a separate future immutable record:

```text
reports/program/evidence/cross-experiment-provenance-registry/
MCEPR-FORWARD-CUTOVER-V0.1.json
```

Its creation remains separately authorized.

The effective forward boundary is the later of:

1. the record's declared `cutover_utc`;
2. the commit timestamp of the first governed-branch commit that canonically introduces that exact cutover blob.

An event at or before that effective whole-second boundary is not forward-eligible.

## 4. Genesis rule

The first canonical segment is deliberately minimal:

```text
GENESIS =
1 REAL POST-CUTOVER EVENT
0 RELATIONS

parent_registry_ref =
null
```

Forbidden:

```text
EMPTY GENESIS
SYNTHETIC BOOTSTRAP EVENT
HISTORICAL EVENT
RELATION IN GENESIS DURING INITIAL PILOT
```

The registry is therefore not populated merely to prove that it can be populated.

## 5. Material adversarial finding — relation temporality

The review found one material issue in the earlier activation idea:

```text
EVENT
has occurred_at_utc

RELATION
has no intrinsic occurred_at_utc
```

Therefore a relation concerning historical influence could otherwise be inserted after the cutover and silently appear to belong to forward population.

The minimal correction is:

```text
INITIAL MANUAL PILOT =
EVENT ONLY

RELATION PERSISTENCE =
NOT AUTHORIZED DURING INITIAL PILOT
```

The first real relation will require a separate relation-temporality/admissibility decision after the forward event pilot.

This does not modify the four adopted relation types or the qualified implementation.

## 6. Manual pilot

The pilot is frozen as:

```text
ONE REAL EVENT PER SEGMENT
ZERO RELATIONS PER SEGMENT

MINIMUM =
3 CONSECUTIVE SUCCESSFUL CANONICAL APPENDS

MAXIMUM =
5 AUTHORIZED APPEND CYCLES
```

If 3 consecutive successes cannot be obtained within 5 future authorized cycles:

```text
PILOT =
BLOCKED

NEXT =
HUMAN REVIEW
```

There is no automatic expansion beyond five cycles.

## 7. Canonicality and append-only repository rule

A Git blob existing somewhere in the object database is not enough.

A canonical segment must be:

- reachable from the governed branch HEAD;
- located at the exact MCEPR segment root;
- valid under the frozen MCEPR validator.

The activation protocol adds an important repository-level invariant:

```text
EVERY PREVIOUSLY CANONICAL SEGMENT
must remain present
at the same path
with the same blob
in every later canonical MCEPR state.
```

Therefore deletion or rewrite of an old segment is fail-closed even if the remaining files happen to form another technically valid chain.

## 8. Concurrent repository activity

The repeated SFE/MCEPR parallel-work scenario is handled explicitly.

If Git HEAD changes but:

- the cutover blob is unchanged;
- the activation contract is unchanged;
- implementation and breaker blobs are unchanged;
- the complete prior MCEPR segment set is unchanged;
- all candidate decisive refs still resolve;

then the exact human-approved candidate segment blob can be placed on a tree based on the fresh Git HEAD.

If the MCEPR semantic state changes:

```text
OLD CANDIDATE =
STALE

ACTION =
BLOCKED
REBUILD
REVALIDATE
REAPPROVE EXACT BLOB
```

No automatic semantic merge is permitted.

## 9. Adversarial review

Twenty activation attacks were frozen and reviewed.

Key results:

```text
SYNTHETIC GENESIS               → BLOCKED
PRE-CUTOVER EVENT               → BLOCKED
EQUAL-SECOND CUTOVER AMBIGUITY  → NOT FORWARD-ELIGIBLE
CUTOVER MUTATION                → BLOCKED
ORPHAN GIT OBJECT               → NOT CANONICAL
PRIOR SEGMENT DELETION          → BLOCKED
PRIOR SEGMENT REWRITE           → BLOCKED
UNKNOWN SEGMENT-ROOT FILE       → BLOCKED
UNRELATED SFE HEAD DRIFT        → REVALIDATE / GIT-TREE REBASE ONLY
MCEPR HEAD DRIFT                → BLOCKED / REBUILD / REAPPROVE
CONCURRENT CHILDREN             → BLOCKED FORK
UNRESOLVABLE REF                → BLOCKED
RELATION DURING INITIAL PILOT   → BLOCKED
NO RELATION => NO INFLUENCE     → FORBIDDEN INFERENCE
3 SUCCESSES => COMPLETE         → FORBIDDEN INFERENCE
<3 CONSECUTIVE SUCCESS / 5      → BLOCKED HUMAN REVIEW
BULK EVENT SEGMENT              → FAIL
AUTO PRODUCER AFTER PILOT       → NOT AUTHORIZED
BACKFILL AFTER PILOT            → NOT AUTHORIZED
```

No additional runtime component or authority surface was required to close these attacks.

## 10. Pilot qualification meaning

A successful future pilot would establish only:

```text
forward event append protocol works
canonical parent chain remains stable
concurrency rules behave fail-closed
post-persistence replay succeeds
human exact-blob approval is preservable
```

It would not establish:

```text
REGISTRY COMPLETENESS
PRISTINE EVIDENCE
NO HISTORICAL EXPOSURE
SCIENTIFIC SUPPORT
SCIENTIFIC INDEPENDENCE
FAMILY MEMBERSHIP
N_BUDGET
N_FAMILLE
PERFORMANCE VALIDITY
OPERATIONAL AUTHORITY
```

## 11. Documentary verdict

```text
MCEPR_ACTIVATION_CONTRACT_V0_1 =
QUALIFIED

ACTIVATION_MODEL =
FORWARD_FIRST

GENESIS_RULE =
FIRST_REAL_POST_CUTOVER_EVENT_ONLY

INITIAL_PILOT =
EVENT_ONLY

MANUAL_PILOT =
3_TO_5_APPEND_CYCLES

FIRST_REAL_RELATION =
DEFERRED_PENDING_TEMPORALITY_ADMISSIBILITY

BACKFILL =
NOT_AUTHORIZED

AUTOMATION =
NOT_AUTHORIZED

REAL_REGISTRY_POPULATION =
NOT_AUTHORIZED

RUNTIME_COUPLING =
NONE

AUTHORITY_EXPANSION =
NONE
```

## 12. Next candidate frontier

The next candidate frontier is **not genesis**.

It is:

```text
MCEPR FORWARD CUTOVER RECORD V0.1
```

That record requires separate human authorization.

Only after the cutover record is canonical can a later real event become eligible to create the genesis.

## 13. STOP

```text
DOCUMENTARY_ACTIVATION_QUALIFICATION =
CLOSED

CUTOVER_CREATION =
NOT_AUTHORIZED

GENESIS =
NOT_AUTHORIZED

REAL_EVENT_PERSISTENCE =
NOT_AUTHORIZED

STOP =
TRUE
```
