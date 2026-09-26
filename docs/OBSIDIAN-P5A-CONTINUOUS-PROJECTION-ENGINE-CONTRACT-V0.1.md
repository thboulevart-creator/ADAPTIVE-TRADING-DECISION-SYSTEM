# OBSIDIAN P5-A — CONTINUOUS PROJECTION ENGINE CONTRACT V0.1

Date: 2026-09-26

## 1. Purpose

P5-A defines the architecture and safety contract for keeping the ATDS Obsidian projection synchronized with the canonical GitHub branch without turning Obsidian into a second source of truth.

The user goal is:

> when governed work changes the monitored ATDS branch on GitHub, the corresponding derived Obsidian representation should update automatically with bounded latency, without manual rebuilds.

P5-A is a contract-and-breakers phase only. It does not start a daemon, register a Windows task, poll GitHub continuously, or mutate the live Vault.

## 2. Exact predecessor

Qualified P4-C visual/navigation closure:

    10355f467ccf8f87070ab18839b96ba6fc547d9d

Qualified live Vault:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

Monitored canonical branch:

    integration/system-v1

Observed remote HEAD at preregistration:

    6aef3b1304313c3446c08a3a37b51ea61733f41e

The observed HEAD is evidence at preregistration time only. Continuous mode must always resolve the remote HEAD again at runtime.

## 3. Authority remains unchanged

The hierarchy remains:

    GitHub origin/integration/system-v1
        = CANONICAL

    isolated checkout of an exact observed HEAD
        = READ-ONLY EXECUTION INPUT

    generated projection
        = DERIVED

    human views
        = VIEW / NON-AUTHORITATIVE

    Obsidian
        = OBSERVE / NAVIGATE / QUERY / VISUALIZE / UNDERSTAND

The observer may not:

- push to GitHub;
- commit to GitHub;
- mutate the user's canonical working tree;
- create qualification authority;
- install plugins;
- enable Obsidian Sync;
- enable automatic Git behavior in the Vault.

## 4. What "real time" means

P5-A does not claim zero-latency realtime synchronization.

The initial target is:

    NEAR_REAL_TIME_BOUNDED_LATENCY

with:

    target maximum detection latency = 60 seconds
    candidate polling interval = 30 seconds

This distinction is deliberate. A local Vault cannot receive a GitHub event with zero infrastructure latency unless an inbound event channel is added.

## 5. Mechanism selection

Three mechanisms were considered.

### A. Obsidian Git automation

Rejected for the initial architecture.

Reason:

- it would mix canonical repository synchronization with the derived visualization environment;
- it risks automatic pull/commit/push behavior inside a governance-sensitive workflow;
- it would blur the existing GitHub → projection authority boundary.

### B. GitHub Actions writing directly to the Vault

Rejected.

Reason:

- GitHub Actions runs remotely;
- the qualified Vault is local Windows/OneDrive storage;
- a hosted runner cannot safely and directly perform the local atomic projection promotion.

### C. Public GitHub webhook

Not selected initially.

Reason:

- it requires a reachable inbound endpoint and additional deployment/security infrastructure;
- it is unnecessary to prove the architecture.

It remains a future optimization if a demonstrated latency need justifies it.

### D. Local remote-ref observer

Selected candidate.

The observer performs read-only remote-ref checks and reacts only when the exact monitored GitHub branch HEAD changes.

This keeps GitHub canonical while allowing the local projection engine to operate close to the Vault.

## 6. Observation loop

The candidate observer may use operations equivalent to:

    git ls-remote origin refs/heads/integration/system-v1

for lightweight observation and:

    git fetch --no-tags origin integration/system-v1

only when the observed HEAD requires qualification.

Repeated observation of the same HEAD is a NOOP.

A network failure does not change the live projection and may never cause a CURRENT claim.

Credentials or token-bearing URLs must not be logged.

## 7. Exact-head isolation

A new remote HEAD must be evaluated from an isolated checkout outside:

- the user canonical working tree;
- the Obsidian Vault;
- the existing Git worktree registry used by the canonical checkout.

The runtime checkout must prove:

- exact repository origin;
- exact monitored branch;
- exact fetched commit;
- checkout HEAD equals the observed remote HEAD.

No implicit use of whichever local branch happens to be checked out is allowed.

## 8. Branch transition classification

Every new observed HEAD is classified as one of:

    INITIAL
    FAST_FORWARD
    NON_FAST_FORWARD
    UNKNOWN

Automatic projection promotion is allowed only for:

    INITIAL
    FAST_FORWARD

A non-fast-forward transition or unknown ancestry is:

    BLOCKED_REQUIRES_ADJUDICATION

This prevents a silent force-push or history rewrite from becoming an automatically accepted projection state.

## 9. Event coalescing

Every observed unique HEAD must be recorded.

If a newer HEAD appears while a build is already running:

- the active build remains bound to its own exact HEAD;
- the newer HEAD is queued;
- the latest queued HEAD must eventually be evaluated.

An intermediate HEAD may be marked:

    SUPERSEDED_NOT_PROMOTED

only when it is proven to be contained by a later fast-forward HEAD.

The system may optimize redundant projection work, but it may not silently lose evidence that a HEAD was observed.

## 10. Dynamic inventory is mandatory

The existing P0/P1/P2 pilot was intentionally frozen around a fixed 74-artifact source universe.

That is not sufficient for continuous mode.

P5 continuous mode requires a fresh source inventory for each exact monitored HEAD.

Candidate source zones include:

    GOVERNANCE/
    docs/
    evidence/
    reports/
    requirements/
    src/
    tests/
    tools/
    breakers/
    .github/workflows/

The exact inclusion/exclusion rules are deferred to P5-B.

Before runtime, P5-B must define:

- what constitutes a projectable artifact;
- handling of binary and large artifacts;
- ignored/generated files;
- secret/credential exclusion;
- provenance for every included source.

No secret or credential may ever become projection content.

## 11. Qualification pipeline

The ordered P5 pipeline is:

    OBSERVE_REMOTE_HEAD
        ↓
    VERIFY_REPOSITORY_IDENTITY
        ↓
    CLASSIFY_HEAD_TRANSITION
        ↓
    FETCH_EXACT_HEAD
        ↓
    CREATE_ISOLATED_CHECKOUT
        ↓
    BUILD_DYNAMIC_INVENTORY
        ↓
    CLASSIFY_ARTIFACTS
        ↓
    BUILD_DETERMINISTIC_PROJECTION_A
        ↓
    BUILD_DETERMINISTIC_PROJECTION_B
        ↓
    REQUIRE A == B
        ↓
    RUN PROJECTION BREAKERS
        ↓
    BUILD MACHINE VIEW LAYER IF AUTHORIZED
        ↓
    STAGE COMPLETE GENERATION
        ↓
    VERIFY STAGED GENERATION
        ↓
    PROMOTE ATOMICALLY OR BLOCK
        ↓
    VERIFY LIVE GENERATION
        ↓
    RECORD EVENT AND STATE

Failure at any gate means:

    NO PROMOTION
    KEEP LAST KNOWN GOOD

Partial success is never promotable.

## 12. Generation identity

Every promoted generation must bind itself to:

- repository;
- branch;
- source HEAD;
- source tree;
- projection contract version;
- inventory digest;
- semantic-record digest;
- projection-tree digest;
- generated-file count;
- governed qualification-state transition.

The source HEAD in the generation identity must equal the isolated checkout HEAD used to build it.

Volatile host/daemon data is forbidden from deterministic projection digests.

## 13. Projection state model

The live system uses:

    CURRENT
    STALE
    BLOCKED
    ORPHAN
    MISSING

### CURRENT

The live projection source HEAD equals the latest qualified monitored remote HEAD.

### STALE

The remote HEAD is newer than the live projection HEAD, or the latest observed HEAD has not yet been promoted.

### BLOCKED

The latest observed HEAD failed qualification or requires human adjudication.

### ORPHAN

A derived artifact still exists in a generation context but its canonical source no longer exists in the current qualified source tree.

### MISSING

An expected derived artifact is absent.

UNKNOWN may never be silently mapped to CURRENT.

## 14. Last-known-good rule

Continuous mode is fail-closed for promotion and fail-open for reading the last known good projection.

If a candidate fails:

- the current live projection remains readable;
- the failed candidate does not modify it;
- evidence for the failed candidate is preserved outside the live projection;
- the live source HEAD remains explicitly recorded;
- the UI must be able to expose STALE or BLOCKED later.

## 15. Atomicity

P5 forbids direct multi-file overwrite of the live projection as a promotion mechanism.

A complete candidate generation must first exist in staging.

The target requirement is:

    no observer may expose a mixed generation

Candidate mechanism:

    STAGED GENERATION SWAP
    or an equivalent atomic visibility primitive

However, the exact Windows + OneDrive primitive is NOT yet qualified.

Likewise, promotion while Obsidian is open is NOT yet authorized.

P5-C must empirically test the promotion primitive before continuous mode can be enabled.

## 16. Existing human views

The P4-B/P4-C `views/` layer is human-owned.

P5 may not silently overwrite it.

This creates an important architectural distinction:

    views/
        = HUMAN / NON-AUTHORITATIVE / NOT AUTO-OVERWRITTEN

while the future continuously refreshed visual layer must live in a machine-owned namespace.

Candidate namespace:

    generated/live/

Future Bases, Graph support notes, Canvas, indexes and dashboards may be generated there only after a separate contract.

Human views may link to those machine-managed live views.

## 17. Runtime state and event log

Volatile observer state belongs outside the Vault, under LocalAppData or an equivalent local control root.

An append-only event log is required.

Each event records at least:

- observed time;
- remote HEAD;
- previous live HEAD;
- transition class;
- pipeline result;
- live HEAD after processing;
- projection state;
- failure code.

The event log is operational evidence, not semantic authority.

## 18. Concurrency

Exactly one promotion writer is permitted.

A second engine instance must fail closed on a lock.

Concurrent readers such as Obsidian may never be allowed to observe a partially promoted generation.

## 19. Recovery

Crash behavior must be explicit:

### Before promotion

No live mutation. Staging may be discarded or preserved for forensics.

### During an unqualified promotion primitive

Continuous mode becomes BLOCKED until adjudicated.

### After promotion but before operational state logging

State is reconstructed from the promoted generation identity.

The last-known-good generation must never be recursively deleted before the new generation is independently verified.

## 20. Operational observability

The future engine must report:

    observer_running
    latest_remote_head
    live_projection_head
    projection_state
    last_success_time
    last_failure_time
    last_failure_code
    queued_head_count

A later visual phase will surface this in Obsidian without granting it semantic authority.

## 21. P5-A non-authorizations

P5-A does NOT authorize:

- starting a background observer;
- starting a polling loop;
- creating a Windows Scheduled Task;
- creating a startup service;
- continuously writing the Vault;
- replacing `generated/`;
- overwriting human `views/`;
- modifying `.obsidian/`;
- enabling plugins or Sync.

## 22. Required breakers

The contract requires breakers for at least:

- GitHub push/commit from observer;
- canonical-working-tree mutation;
- repository/branch identity mismatch;
- wrong exact checkout HEAD;
- same-HEAD rebuild;
- force-push auto-acceptance;
- unknown ancestry auto-acceptance;
- frozen pilot misuse as dynamic inventory;
- secret projection;
- missing double-build determinism;
- candidate failure mutating live state;
- partial promotion;
- mixed generations;
- direct in-place multi-file promotion;
- last-known-good deletion before verification;
- human-view overwrite;
- `.obsidian/` mutation;
- Sync/plugin dependency;
- volatile daemon data contaminating deterministic digests;
- network failure claiming CURRENT;
- UNKNOWN/STALE claiming CURRENT;
- concurrent writer bypass;
- lost observed-HEAD event;
- unqualified Windows/OneDrive atomicity assumption;
- unqualified promotion while Obsidian is open.

## 23. Ordered next gates

P5-A intentionally decomposes implementation into four bounded steps:

### P5-B

    DYNAMIC CURRENT-HEAD INVENTORY
    + SOURCE SELECTION CONTRACT

This removes the frozen-pilot limitation.

### P5-C

    WINDOWS / ONEDRIVE
    ATOMIC PROMOTION PRIMITIVE QUALIFICATION

This proves that a complete generation can become visible without mixed state.

### P5-D

    CONTINUOUS OBSERVER IMPLEMENTATION CANDIDATE

This implements the actual local observer/queue/state machine.

### P5-E

    END-TO-END NEAR-REAL-TIME QUALIFICATION

This proves:

    GitHub HEAD changes
        ↓
    detection
        ↓
    exact-head qualification
        ↓
    safe promotion
        ↓
    Obsidian sees the new projection

within the bounded latency target.

## 24. Success meaning

A P5-A PASS means only:

> the continuous GitHub → Obsidian projection architecture, authority boundary, state model, failure behavior, and ordered implementation gates have been preregistered and survived their contract breakers.

It does not mean continuous synchronization is running.
