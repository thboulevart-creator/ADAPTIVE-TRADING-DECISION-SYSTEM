# OBSIDIAN P5-D1 — CONTINUOUS OBSERVER CORE CONTRACT V0.1

Date: 2026-09-27

## 1. Purpose

P5-D1 defines the observer as a deterministic and auditable state machine before any background loop, polling cadence, Windows startup registration, scheduled task, service, or continuous production write authority exists.

The objective is deliberately narrower than "start continuous synchronization".

P5-D1 asks:

> Given one previous observer state and one normalized input event, what exact next state and decision are permitted?

The answer must be deterministic, fail-closed, reproducible and auditable.

## 2. Exact starting point

P5-D1 starts from the completed P5-C3R2 qualification chain.

Final P5-C3R2 qualification commit:

    00ca2946ce30b0e319658f8d5b903357b7ccfc5e

Qualified P5-C3R2 runtime candidate:

    b5f3a8de061772e15bc94b20095d419130c20781

The predecessor P5-C3R remains unqualified.

P5-D1 does not reopen P5-C3R2 gates.

## 3. Qualified predecessor components

P5-D1 depends on, but does not reimplement:

- P5-A continuous projection architecture;
- P5-B2 dynamic current-HEAD inventory;
- P5-C2 immutable-generation atomic pointer promotion primitive;
- P5-C3R2 Obsidian-open bounded reader EACCES compatibility.

The observer core is orchestration/state logic above these already qualified components.

## 4. Authority

The authority hierarchy remains:

    GitHub origin/integration/system-v1
        = CANONICAL

    observer core
        = DERIVED DECISION ENGINE

    isolated exact-head checkout
        = READ-ONLY EXECUTION INPUT

    generated projection
        = DERIVED

    Obsidian
        = OBSERVE / NAVIGATE / QUERY / VISUALIZE / UNDERSTAND

The observer core may not push, commit, mutate the canonical user worktree, overwrite human views, modify .obsidian, enable Sync or install plugins.

## 5. Pure transition model

The P5-D1 core is specified as:

    next_state, decision
        =
    TRANSITION(previous_state, normalized_input)

The transition itself may not:

- perform network I/O;
- perform filesystem I/O;
- launch processes;
- read wall-clock time;
- read environment variables;
- use randomness.

Those operations belong to future adapters around the deterministic core.

The same normalized inputs must produce byte-identical normalized outputs.

## 6. Deterministic state

Observer state contains:

    repository
    branch
    observer_phase
    remote_freshness
    latest_observed_head
    last_qualified_head
    live_projection_head
    projection_state
    pending_heads
    blocked_head
    last_failure_code
    last_event_sequence

Observer phases:

    IDLE
    CANDIDATE_PENDING
    EVALUATING
    BLOCKED
    STOPPED

Remote freshness:

    KNOWN
    UNKNOWN

Projection state vocabulary remains exactly:

    CURRENT
    STALE
    BLOCKED
    ORPHAN
    MISSING

Timestamps, PIDs and host paths are excluded from deterministic state.

## 7. Why remote freshness is a separate axis

A network failure must never create a fresh CURRENT claim.

The last-known-good projection may remain physically usable while current remote freshness is unknown.

Therefore:

    projection content availability

and:

    knowledge that it matches the latest canonical remote HEAD

are separate facts.

CURRENT presentation requires all three:

    remote_freshness = KNOWN
    latest_observed_head = live_projection_head
    live_projection_head = last_qualified_head

This prevents a network outage from silently presenting stale content as proven current.

## 8. HEAD transition rules

Exact transition classes are:

    INITIAL
    SAME
    FAST_FORWARD
    NON_FAST_FORWARD
    UNKNOWN

### SAME

    action = NOOP
    no queue growth
    no evaluation start

### INITIAL

May enter the automatic evaluation queue.

P5-D1 itself still performs no evaluation runtime.

### FAST_FORWARD

May enter the automatic evaluation queue.

### NON_FAST_FORWARD

    BLOCKED_REQUIRES_ADJUDICATION

No automatic evaluation or promotion.

### UNKNOWN

    BLOCKED_REQUIRES_ADJUDICATION

No automatic evaluation or promotion.

## 9. Evaluation semantics

An evaluation is always bound to one exact immutable HEAD.

A newer observed HEAD may not retarget an active evaluation.

EVALUATION_STARTED:

    observer phase = EVALUATING
    live projection unchanged

EVALUATION_PASSED:

    candidate becomes qualified pending promotion
    live projection unchanged

EVALUATION_FAILED:

    last-known-good remains unchanged
    projection becomes BLOCKED
    no promotion

P5-D1 defines these semantics but does not execute the evaluation pipeline.

## 10. Promotion semantics are model-only in P5-D1

P5-D1 models how state would change after an independently authorized confirmed promotion.

It does not authorize that promotion.

Even a qualified candidate must remain:

    QUALIFIED_PENDING_PROMOTION

until a later governed boundary grants the exact promotion action.

A promotion failure leaves the previous live projection unchanged.

## 11. Queue semantics

Pending heads are:

- exact SHA identities;
- unique;
- ordered by observation;
- immutable identities once queued.

A newer head may be queued while an older one is being evaluated.

An intermediate head may be marked:

    SUPERSEDED_NOT_PROMOTED

only after fast-forward containment is proven.

No observed unique HEAD may silently disappear from the audit trail.

Runtime queue capacity is deferred until P5-D4, where a bounded loop actually exists.

## 12. Audit model

Every deterministic transition produces digests for:

    previous_state
    normalized_input
    decision
    next_state

Append-only event minimum fields:

    sequence
    event_type
    previous_state_digest
    input_digest
    decision_digest
    next_state_digest
    reason_code

Volatile envelope fields such as timestamps, host identity or PID may be recorded for operations, but they must not affect deterministic digests.

The event log is evidence, not semantic authority.

## 13. Single writer

A future runtime must have one promotion writer.

Second instance result:

    NO_WRITE_BLOCKED_BY_LOCK

Lock acquisition itself is outside the pure transition function.

PID/lock-owner identity may never enter deterministic state digests.

Stale-lock recovery policy is deferred to P5-D3.

## 14. Last-known-good

The live projection head may change only after a separately confirmed promotion.

These events may not change it:

- remote observation failure;
- evaluation failure;
- promotion failure.

Recursive deletion of last-known-good is forbidden.

## 15. Reuse, do not reimplement

P5-D1 explicitly requires reuse of:

- dynamic inventory contract/implementation;
- qualified atomic pointer primitive;
- P5-C3R2 reader retry policy.

P5-D must orchestrate these components, not fork weaker copies.

## 16. P5-D1 non-authorizations

P5-D1 authorizes no runtime implementation.

Still forbidden:

    observer core implementation
    network remote observation execution
    remote fetch execution
    background observer execution
    polling loop execution
    production promotion
    continuous Vault write
    Windows startup registration
    scheduled task creation
    Windows service creation
    Graph/Search CURRENT semantics

## 17. Required breaker themes

The contract preregisters breakers for:

- SAME HEAD rebuilding;
- network failure creating CURRENT;
- freshness UNKNOWN shown as CURRENT;
- force-push/UNKNOWN automatic handling;
- active evaluation retargeting;
- queue duplication/reordering/loss;
- evaluation changing live projection;
- failed promotion changing last-known-good;
- non-deterministic time/PID/env/random dependence;
- I/O inside the pure transition;
- GitHub push/commit;
- canonical worktree mutation;
- human-view/.obsidian mutation;
- qualified component reimplementation;
- background runtime starting during P5-D1;
- production write during P5-D1;
- Windows persistence registration;
- Graph/Search semantic overclaim.

## 18. Next governed sequence

If P5-D1 qualifies:

    P5-D2
    ONE-SHOT OBSERVER TICK IMPLEMENTATION

Then:

    P5-D3
    CONTROLLED CANDIDATE EVALUATION PIPELINE

Then:

    P5-D4
    BOUNDED OBSERVER LOOP CANDIDATE

Only after those:

    P5-E
    END-TO-END NEAR-REAL-TIME QUALIFICATION

Graph/Search semantics remain:

    P6
    CONTROLLED KNOWLEDGE GRAPH ARCHITECTURE

## 19. Current boundary

P5-D1 is contract-and-breakers only.

No daemon exists.
No loop runs.
No GitHub polling has been authorized.
No production Vault synchronization has been authorized.
