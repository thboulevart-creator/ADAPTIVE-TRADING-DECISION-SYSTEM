# OBSIDIAN P5-A — CONTINUOUS PROJECTION ENGINE PREFLIGHT

Date: 2026-09-26

## 1. Purpose

P5-A preregisters the architecture, safety model, state vocabulary, failure semantics and implementation gates for continuous GitHub → Obsidian projection.

P5-A does not start continuous synchronization.

## 2. Exact predecessor

Qualified P4-C closure:

    10355f467ccf8f87070ab18839b96ba6fc547d9d

## 3. Candidate branch

    feat/obsidian-projection-p5a-continuous-projection-contract-v0.1

## 4. Monitored canonical source

Repository:

    thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Remote:

    origin

Branch:

    integration/system-v1

Remote HEAD observed at preregistration:

    6aef3b1304313c3446c08a3a37b51ea61733f41e

This HEAD is not frozen as a runtime target. The future observer must resolve the current remote HEAD at each observation cycle.

## 5. Persisted candidate artifacts

Contract:

    tools/obsidian_projection/continuous_projection_contract_v0_1.json
    blob: 96ec1a768b8e9ff77d94bbcd36ee513678c258e6

Documentation:

    docs/OBSIDIAN-P5A-CONTINUOUS-PROJECTION-ENGINE-CONTRACT-V0.1.md
    blob: e1a2e91914d4d71bbec69aef68fb81f2591f4973

Contract breakers:

    tests/obsidian_projection/test_continuous_projection_contract_v0_1.py
    blob: e6e0593de1c4bba9313fb3ddd1fdc97fbd8bc9ad

## 6. Selected architecture

Candidate mechanism:

    LOCAL_REMOTE_REF_OBSERVER

Delivery semantics:

    NEAR_REAL_TIME_BOUNDED_LATENCY

Maximum target detection latency:

    60 seconds

Candidate polling interval:

    30 seconds

This is deliberately not described as zero-latency realtime.

## 7. Why this mechanism

Initial alternatives were considered:

- Obsidian Git auto pull/push — rejected because it weakens the canonical/derived boundary;
- GitHub Actions direct-to-local-Vault — rejected because hosted runners cannot safely mutate the qualified local Vault;
- public webhook — deferred because it introduces an inbound endpoint and unnecessary infrastructure before the basic architecture is proven;
- local remote-ref observer — selected because it can remain read-only toward GitHub and operate locally near the Vault.

## 8. Authority invariants

P5-A preserves:

    GitHub remote branch = CANONICAL
    isolated exact-head checkout = READ-ONLY EXECUTION INPUT
    projection = DERIVED
    Obsidian = OBSERVE / NAVIGATE / QUERY / VISUALIZE / UNDERSTAND

The future observer may not push, commit, mutate the user's canonical working tree, or create governance authority.

## 9. Critical design findings

### Dynamic inventory is a prerequisite

The existing frozen 74-artifact pilot cannot satisfy continuous mode.

Every exact source HEAD requires its own governed inventory.

### Last-known-good is mandatory

Any candidate failure leaves the live projection unchanged.

### Atomic promotion is not yet solved

The contract forbids mixed generations and direct in-place multi-file overwrite.

The exact Windows + OneDrive promotion primitive is intentionally deferred to empirical qualification.

Promotion while Obsidian is open is also not yet authorized.

### Human views remain protected

P4-B/P4-C `views/` remains human-owned and cannot be silently overwritten.

A future continuously refreshed visual layer therefore requires a machine-owned namespace, candidate:

    generated/live/

## 10. State model

Allowed projection states:

    CURRENT
    STALE
    BLOCKED
    ORPHAN
    MISSING

UNKNOWN may not be silently promoted to CURRENT.

## 11. Ordered runtime pipeline

The preregistered sequence is:

    OBSERVE_REMOTE_HEAD
      → VERIFY_REPOSITORY_IDENTITY
      → CLASSIFY_HEAD_TRANSITION
      → FETCH_EXACT_HEAD
      → CREATE_ISOLATED_CHECKOUT
      → BUILD_DYNAMIC_INVENTORY
      → CLASSIFY_ARTIFACTS
      → BUILD_DETERMINISTIC_PROJECTION_A
      → BUILD_DETERMINISTIC_PROJECTION_B
      → REQUIRE_A_EQUALS_B
      → RUN_PROJECTION_BREAKERS
      → BUILD_MACHINE_VIEW_LAYER_IF_AUTHORIZED
      → STAGE_COMPLETE_GENERATION
      → VERIFY_STAGED_GENERATION
      → PROMOTE_ATOMICALLY_OR_BLOCK
      → VERIFY_LIVE_GENERATION
      → RECORD_EVENT_AND_STATE

Any failed gate means:

    NO PROMOTION
    KEEP LAST KNOWN GOOD

## 12. Transition safety

Automatic promotion is limited to:

    INITIAL
    FAST_FORWARD

These states block automatic promotion:

    NON_FAST_FORWARD
    UNKNOWN

A history rewrite therefore cannot silently become the live Obsidian projection.

## 13. P5-A non-authorizations

P5-A does not authorize:

- background daemon execution;
- polling loop execution;
- Windows startup registration;
- scheduled-task creation;
- continuous Vault writes;
- generated-tree replacement;
- human-view overwrite;
- `.obsidian/` mutation.

## 14. Static remote review

The persisted contract was statically reviewed for:

- exact repository/branch identity;
- P4-C predecessor identity;
- bounded near-realtime semantics;
- GitHub push/commit prohibition;
- canonical-worktree isolation;
- no Git worktree-registry dependency;
- same-HEAD NOOP;
- force-push/unknown ancestry blocking;
- dynamic-inventory prerequisite;
- secret exclusion;
- deterministic double-build;
- last-known-good behavior;
- exact projection state vocabulary;
- mixed-generation prohibition;
- unqualified atomic primitive explicitly marked unresolved;
- protected human views;
- protected Obsidian config;
- separate future machine-live namespace;
- append-only event log;
- single-writer lock;
- no runtime authorization in P5-A;
- at least 30 unique breakers;
- ordered P5-B → P5-C → P5-D → P5-E gates.

Static remote review: PASS.

This is not local runtime qualification.

## 15. Required persisted local re-break

Before P5-A can close PASS:

1. recover the exact persisted P5-A HEAD;
2. run `py_compile` on the P5-A breaker;
3. execute the targeted P5-A breaker module;
4. execute the full `tests/obsidian_projection/test_*.py` suite;
5. preserve original repository branch/HEAD/status.

No P5-B implementation is authorized before this re-break passes.

## 16. Next gates after P5-A PASS

    P5-B
    DYNAMIC CURRENT-HEAD INVENTORY
    + SOURCE SELECTION CONTRACT

    P5-C
    WINDOWS / ONEDRIVE
    ATOMIC PROMOTION PRIMITIVE QUALIFICATION

    P5-D
    CONTINUOUS OBSERVER IMPLEMENTATION CANDIDATE

    P5-E
    END-TO-END NEAR-REAL-TIME QUALIFICATION

## 17. Current verdict

**P5-A CANDIDATE PERSISTED — LOCAL RE-BREAK REQUIRED**

No continuous synchronization success claim is authorized.
