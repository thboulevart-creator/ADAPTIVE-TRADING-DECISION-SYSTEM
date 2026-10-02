# MCEPR — IMPLEMENTATION CONTRACT V0.1 — DOCUMENTARY QUALIFICATION

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Qualification base HEAD:** `f9aaba1efcaccedc94ace147c7f72518f0e9bcd4`  
**Qualification base TREE:** `9b1a78d107744fca3a5a98ecdcf86fe183ec3c46`  
**G6 adjudication blob:** `93e3c87f24b8933fbdfe25b1806d42233b6ec328`

## 1. Qualified contract

Path:

`GOVERNANCE/MINIMAL-CROSS-EXPERIMENT-PROVENANCE-REGISTRY-IMPLEMENTATION-CONTRACT-V0.1.json`

Blob:

`55957058f610cca9de2e20b52d2ad1335f194d16`

Schema:

`ATDS_MINIMAL_CROSS_EXPERIMENT_PROVENANCE_REGISTRY_IMPLEMENTATION_CONTRACT_V0_1`

## 2. Authority boundary

This qualification covers the contract and breaker specification only.

```text
BREAKER_IMPLEMENTATION = NOT_AUTHORIZED
REGISTRY_IMPLEMENTATION = NOT_AUTHORIZED
REGISTRY_POPULATION = NOT_AUTHORIZED
BACKFILL = NOT_AUTHORIZED
RUNTIME_CHANGE = NOT_AUTHORIZED
P1_MODIFICATION = NOT_AUTHORIZED
SFE_MODIFICATION = NOT_AUTHORIZED
MEMORY_ENGINE_MODIFICATION = NOT_AUTHORIZED
DECISION_MODIFICATION = NOT_AUTHORIZED
```

No executable registry implementation or registry data was created.

## 3. Contract reductions and clarifications made during re-break

### C1 — relation source generalized without semantic expansion

The G5-R1 conceptual form used `SOURCE_EVENT_REF`. That is too narrow for the already adopted relation vocabulary because `RESERVED_FOR` and `CLASSIFIED_BY` can legitimately originate from an immutable non-event artifact.

V0.1 therefore uses `SOURCE_REF` with the same decisive-reference grammar as every other relation endpoint. This changes no relation type and grants no authority.

### C2 — no mutable current-head pointer

A separate mutable `HEAD` file would create a second source of truth. V0.1 instead derives the current head as the unique tip of the complete validated parent-linked chain.

```text
MULTIPLE TIPS / FORK
→ BLOCKED
```

### C3 — ADJUDICATED cannot self-authorize

A producer cannot make a relation authoritative by writing `relation_status = ADJUDICATED`.

V0.1 requires the relation's `basis_ref` to be a Git blob included in a separately human-authorized adjudication-basis allowlist supplied to validation.

If that authority context is absent:

```text
ADJUDICATED
→ BLOCKED
```

No path, filename or content heuristic may silently infer human authority.

## 4. Persistence surface

If implementation is later authorized, registry segments are limited to:

`reports/program/evidence/cross-experiment-provenance-registry/segments/`

Each segment filename is bound to the full content-derived registry identity:

```text
RGS-<64 lowercase hex>.json
```

No segment, genesis registry, backfill or directory population was created by this qualification.

## 5. Identity model

```text
EVENT_ID =
EVT- + SHA256(canonical event identity payload)

RELATION_ID =
REL- + SHA256(canonical relation identity payload)

REGISTRY_ID =
RGS- + SHA256(canonical segment identity payload)
```

The canonicalization profile follows the existing ATDS stable-hash pattern while adding fail-closed restrictions for duplicate keys, unknown fields and numbers in identity payloads.

## 6. Reference grammar

Only these decisive reference forms are admitted in V0.1:

```text
git_blob:<40 lowercase hex>
git_commit:<40 lowercase hex>
event:EVT-<64 lowercase hex>
relation:REL-<64 lowercase hex>
registry:RGS-<64 lowercase hex>
```

An existing ATDS object is referenced through the immutable Git blob or commit containing its canonical persisted representation. No second P1/SFE/dataset object namespace is created.

## 7. Relation vocabulary

Exact and closed:

```text
INFORMED_BY
PREREGISTERED_BY
RESERVED_FOR
CLASSIFIED_BY
```

Statuses remain:

```text
DECLARED
ADJUDICATED
DISPUTED
UNKNOWN
```

These statuses are provenance statuses, not scientific truth.

## 8. Supersession

A relation correction never rewrites an ancestor. A successor must reference the exact currently active ancestor relation and preserve `source_ref`, `relation_type`, and `target_ref`. Only status, basis and supersession lineage may change. The same prior relation cannot have two active direct successors.

## 9. PASS / FAIL / BLOCKED

```text
PASS
= technical integrity demonstrated on the declared registry-validation surface only

FAIL
= intrinsic deterministic contract violation

BLOCKED
= safe conclusion impossible because external resolution, authority context or chain uniqueness is missing/ambiguous
```

A PASS explicitly does not establish completeness, pristine status, scientific validity, family independence, `N_budget`, `N_famille`, performance, promotion or operational authority.

## 10. Breaker specification

```text
TEST_CASES_SPECIFIED = 50
EXECUTABLE_BREAKER_CREATED = FALSE
EXECUTABLE_BREAKER_RUN = NOT_RUN
```

The specified adversarial surface covers deterministic canonicalization; event/relation/segment content binding; duplicate-key and unknown-field rejection; timestamp/period integrity; reference syntax and resolution; chain genesis/parent/head/fork semantics; historical persistence; supersession; human-adjudication gating; retrospective event semantics; prohibition on completeness/pristine claims; prohibition on automatic `N_budget` / `N_famille`; and representability of all four adopted relation types.

## 11. Final documentary re-break

```text
FALSE_COMPLETENESS               → CLOSED BY EXPLICIT NON-CLAIM
FAKE_APPEND_ONLY                 → CLOSED BY CONTENT-BOUND PARENT CHAIN
AMBIGUOUS_REFERENCE              → CLOSED BY EXACT REFERENCE GRAMMAR
FORGEABLE_EVENT_ID               → CLOSED BY FULL CONTENT HASH
MUTABLE_RELATION_STATUS          → CLOSED BY RELATION ID + SUPERSESSION
RETROSPECTIVE_BACKDATING         → CLOSED BY OCCURRENCE/PERSISTENCE SEPARATION
AUTO_N_BUDGET                    → FORBIDDEN
AUTO_N_FAMILLE                   → FORBIDDEN
SECOND_SOURCE_OF_TRUTH           → CLOSED BY IMMUTABLE-ANCHOR RULE
REGISTRY_FORK                    → BLOCKED
SELF_AUTHORIZED_ADJUDICATION     → BLOCKED WITHOUT HUMAN-AUTHORIZED BASIS
NON_EVENT_RELATION_SOURCE        → REPRESENTABLE VIA SOURCE_REF
MUTABLE_HEAD_POINTER             → ELIMINATED
```

No new material gap was found within the documentary contract surface after these corrections.

## 12. Documentary verdict

```text
IMPLEMENTATION_CONTRACT_V0_1 =
PASS_DOCUMENTARY

CONTRACT_SCHEMA =
FROZEN_FOR_FUTURE_TEST_FIRST_OPENING

BREAKER_SPECIFICATION =
DEFINED_50_CASES

EXECUTABLE_QUALIFICATION =
NOT_PERFORMED

IMPLEMENTATION =
NOT_AUTHORIZED

REGISTRY_POPULATION =
NOT_AUTHORIZED

BACKFILL =
NOT_AUTHORIZED

RUNTIME_CHANGE =
NONE

AUTHORITY_EXPANSION =
NONE
```

## 13. Next candidate frontier

Only after separate human authorization:

```text
FROZEN BREAKER V0.1
→ EXPECTED RED AGAINST ABSENT IMPLEMENTATION
```

That future authorization must still not imply permission for minimal implementation unless separately stated.

## 14. STOP

```text
DOCUMENTARY_CONTRACT_QUALIFICATION =
CLOSED

STOP =
TRUE
```
