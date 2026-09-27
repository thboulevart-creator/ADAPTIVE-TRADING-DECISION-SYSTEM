# OBSIDIAN P5-D2 — ONE-SHOT OBSERVER TICK V0.1

Date: 2026-09-27

## 1. Purpose

P5-D2 implements the P5-D1 observer state machine for the first time as one finite pure invocation.

The implemented boundary is:

    previous_state
          +
    normalized_input
          ↓
      one_shot_tick
          ↓
    next_state
    decision
    audit digests

Exactly one normalized input is consumed per call.

P5-D2 does not observe GitHub itself and does not mutate the Vault.

## 2. Qualified predecessor

P5-D1 qualification commit:

    dce36303982d73a37d8498400f0a13e708e841b6

P5-D1 contract blob:

    a20999ae991e07447e25ecd1592964f2d333449b

P5-D1 qualification report blob:

    fbe4a60f2349a96bf7a1f4c5dea0eb28328af841

P5-D2 does not reopen P5-D1.

## 3. Exact P5-D2 contract

Contract:

    tools/obsidian_projection/one_shot_observer_tick_contract_v0_1.json

Blob:

    5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3

Implementation:

    tools/obsidian_projection/observer_tick.py

The implementation pins that exact contract blob.

## 4. Pure runtime boundary

The P5-D2 module imports only pure standard-library facilities needed for:

- hashing;
- JSON canonicalization;
- HEAD-format validation;
- Python typing.

It does not import or invoke:

- network APIs;
- Git subprocesses;
- filesystem state stores;
- Windows process APIs;
- timers or sleep;
- randomness;
- environment variables;
- threads;
- multiprocessing;
- async tasks.

There is one public state-transition entrypoint:

    one_shot_tick(previous_state, normalized_input)

No repeated-tick loop exists.

## 5. Canonical state

State schema:

    ATDS_OBSIDIAN_OBSERVER_STATE_V0_1

Required axes remain separated:

    observer_phase
    remote_freshness
    projection_state

Observer phases:

    IDLE
    CANDIDATE_PENDING
    EVALUATING
    BLOCKED
    STOPPED

Remote freshness:

    KNOWN
    UNKNOWN

Projection state:

    CURRENT
    STALE
    BLOCKED
    ORPHAN
    MISSING

HEAD identities are lowercase 40-hex SHA-1 values or null where allowed.

Pending HEADs are FIFO and unique.

## 6. Strengthened state invariants

P5-D2 fail-closes invalid states before transition.

CURRENT requires:

    remote_freshness = KNOWN
    latest_observed_head = live_projection_head
    live_projection_head = last_qualified_head
    live_projection_head != null

EVALUATING requires a non-empty pending queue.

CANDIDATE_PENDING requires a qualified HEAD.

BLOCKED requires:

    projection_state = BLOCKED
    blocked_head != null
    last_failure_code != null

## 7. Canonical input

Input schema:

    ATDS_OBSIDIAN_OBSERVER_INPUT_V0_1

Every input includes exactly:

    schema
    event_type
    sequence
    observed_head
    transition_class
    candidate_head
    failure_code

Extra fields are rejected.

Sequence must be exactly:

    previous_state.last_event_sequence + 1

No skip and no replay are accepted.

## 8. HEAD classification consistency

P5-D2 does not determine ancestry.

The future adapter must provide the classification.

P5-D2 still verifies minimal consistency:

    INITIAL
        previous latest_observed_head must be null

    SAME
        observed_head must equal previous latest_observed_head

    FAST_FORWARD
    NON_FAST_FORWARD
    UNKNOWN
        previous latest_observed_head must exist
        observed_head must differ from it

This catches malformed normalized input without pretending to perform Git ancestry analysis.

## 9. Bootstrap

BOOTSTRAP is allowed only from the canonical initial state at sequence zero.

Initial state:

    observer_phase = IDLE
    remote_freshness = UNKNOWN
    latest_observed_head = null
    last_qualified_head = null
    live_projection_head = null
    projection_state = MISSING
    pending_heads = []
    blocked_head = null
    last_failure_code = null
    last_event_sequence = 0

BOOTSTRAP changes only event sequence.

## 10. Remote observation transitions

### INITIAL

Queues the exact observed HEAD.

No evaluation starts automatically.

### SAME

NOOP.

No queue growth.
No evaluation start.

If the projection had only become STALE because remote freshness was unknown, SAME may restore CURRENT only when all CURRENT invariants are again satisfied.

### FAST_FORWARD

Queues the exact new HEAD.

If an older candidate is being evaluated, the active evaluation remains bound to its original queue head.

### NON_FAST_FORWARD

Blocks.

No queue append.
No automatic evaluation.
No promotion.

### UNKNOWN

Blocks identically.

## 11. Sticky BLOCKED state

Once the observer is BLOCKED, a later remote observation does not silently clear the block.

A new observed HEAD may advance:

    latest_observed_head

but:

    observer_phase remains BLOCKED
    projection_state remains BLOCKED
    pending queue remains unchanged
    blocked_head remains unchanged
    blocking failure code remains unchanged
    live projection remains unchanged

The returned decision remains:

    BLOCK_REQUIRES_ADJUDICATION

The normalized input digest still records the newly observed HEAD and its supplied classification.

## 12. Network observation failure

REMOTE_OBSERVATION_FAILED:

    remote_freshness = UNKNOWN
    live_projection_head unchanged

If previous projection state was CURRENT:

    CURRENT → STALE

Other non-CURRENT projection states are retained.

The last-known-good live HEAD is never changed by a remote observation failure.

## 13. Evaluation transitions

### EVALUATION_STARTED

Allowed only from IDLE.

The candidate must equal:

    pending_heads[0]

State becomes:

    EVALUATING

The queue and live projection remain unchanged.

### EVALUATION_PASSED

Requires EVALUATING and exact queue-head candidate.

The queue head is removed.

Then:

    last_qualified_head = candidate
    observer_phase = CANDIDATE_PENDING

The live projection is unchanged.

This preserves:

    qualification != promotion

### EVALUATION_FAILED

Requires EVALUATING and exact queue-head candidate.

The failed candidate is removed from queue and becomes the blocked HEAD.

State becomes BLOCKED.

Live projection remains unchanged.

## 14. Promotion events are logical confirmations only

P5-D2 performs no promotion I/O.

PROMOTION_CONFIRMED means an external future governed component reports that promotion has already been confirmed.

It is accepted only when:

    observer_phase = CANDIDATE_PENDING
    candidate_head = last_qualified_head

Then logical state may set:

    live_projection_head = candidate

CURRENT is allowed only if remote freshness is KNOWN and the candidate is still the latest observed HEAD.

Otherwise the logical projection remains STALE.

PROMOTION_FAILED similarly records the externally reported failure but may not mutate the previous live projection HEAD.

For every P5-D2 decision:

    automatic_promotion_authorized = false
    production_write_authorized = false

## 15. Lock contention

LOCK_CONTENDED is a one-shot NOOP.

Semantic state is unchanged except for the monotonic event sequence.

No write authority is granted.

## 16. Shutdown

SHUTDOWN_REQUESTED sets:

    observer_phase = STOPPED

Pending HEADs and live projection identity are preserved.

STOPPED is terminal for P5-D2.

No later event is accepted.

## 17. Deterministic canonicalization

Canonical JSON:

    UTF-8
    sorted keys
    compact separators
    terminal LF
    NaN forbidden

Digest:

    SHA-256

The audit event binds:

    previous_state_digest
    input_digest
    decision_digest
    next_state_digest

The returned audit record contains no timestamp, PID, hostname or host path.

## 18. Failure behavior

Invalid state:

    raise ObserverTickError

Invalid normalized input:

    raise ObserverTickError

Invalid transition:

    raise ObserverTickError

No partial result is returned.

Caller-owned input dictionaries are cloned before transition and may not be mutated by P5-D2.

## 19. Test surfaces

Persisted P5-D2 test surfaces:

    test_one_shot_observer_tick_contract_v0_1.py
    test_observer_tick.py
    test_p5d2_adversarial.py

Current static counts:

    contract tests = 24
    behavioral tests = 54
    adversarial tests = 17
    preregistered required breakers = 67 unique

These counts are static repository facts, not execution evidence.

## 20. P5-D2 non-authorizations

Still forbidden:

    network adapter
    git adapter
    filesystem state store
    append-only disk event log
    background observer
    polling loop
    sleep/timer scheduling
    production promotion
    continuous Vault writes
    Windows startup registration
    scheduled task
    Windows service
    Graph/Search CURRENT semantics

## 21. Next governed boundary

If P5-D2 qualifies:

    P5-D3 — CONTROLLED CANDIDATE EVALUATION PIPELINE

P5-D3 may connect a finite orchestrator to already qualified components.

The bounded repeated observer loop remains deferred to:

    P5-D4

End-to-end near-real-time qualification remains:

    P5-E
