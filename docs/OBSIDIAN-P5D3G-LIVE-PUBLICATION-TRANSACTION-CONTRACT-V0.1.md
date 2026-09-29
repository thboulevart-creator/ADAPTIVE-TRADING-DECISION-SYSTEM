# OBSIDIAN P5-D3G — LIVE PUBLICATION TRANSACTION CONTRACT V0.1

Date: 2026-09-29

## 1. Objective

P5-D3G defines one finite governed publication transaction from a qualified retained P5-D3F handoff to the real Vault.

The contract authority is:

    tools/obsidian_projection/live_publication_transaction_contract_v0_1.json

P5-D3G is not a background observer and does not open P5-D4.

## 2. Required sequence

The transaction contract requires:

    verified retained handoff
        ↓
    read-only publication plan
        ↓
    explicit one-shot human authorization
        ↓
    exclusive writer ownership
        ↓
    current-prestate revalidation
        ↓
    immutable live-generation materialization
        ↓
    complete target verification
        ↓
    CURRENT.tmp exclusive write + fsync
        ↓
    atomic CURRENT.md replace with bounded retry
        ↓
    read-after-write verification
        ↓
    durable physical publication receipt
        ↓
    P5-D2 PROMOTION_CONFIRMED
        ↓
    durable logical-confirmation receipt

Physical publication and logical confirmation are separate facts.

## 3. P5-D3F input

Only a P5-D3F handoff that freshly reverifies as:

    PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED
    handoff_status = READY_UNAUTHORIZED
    package = PASS_SEALED_UNPROMOTED

is admissible.

All P5-D3F publication-authority flags must still be false before P5-D3G authorization.

The handoff is read-only input and may not be mutated.

## 4. Human authorization

No publication mutation may occur from:

    CLI invocation
    prior session approval
    wildcard approval
    configuration
    automatic policy

The human authorization must occur after the read-only plan and bind exactly to:

    plan digest
    candidate HEAD
    candidate TREE
    generation ID
    publication mode
    expected previous CURRENT state

One authorization permits one finite transaction only.

## 5. Single writer

Exactly one publisher may own the transaction.

Ownership is required before the first mutation and remains held until a terminal state.

Concurrent writers block.

An ambiguous or stale ownership state is not silently stolen.

## 6. Qualified publication primitive

P5-C2 qualified only:

    IMMUTABLE_GENERATION_ATOMIC_POINTER

P5-D3G therefore forbids fallback to:

    directory two-rename swap
    MoveFileEx directory replacement
    direct in-place generated-file mutation

## 7. P5-C3R2 productionization boundary

P5-C3R2 empirically qualified:

    CURRENT.tmp
    fsync
    os.replace(CURRENT.tmp, CURRENT.md)
    bounded writer sharing-conflict retries
    bounded reader access retries
    read-after-write verification

However the exact P5-C3R2 runtime is synthetic and hardcodes:

    GEN_A
    GEN_B

P5-D3G does not treat that hardcoded synthetic generation model as a production-generalized writer.

Its verified retry and atomic-pointer semantics are preserved, but arbitrary real generation IDs and the production wrapper require their own P5-D3G implementation qualification.

## 8. Production live-generation wrapper

The contract defines:

    <REAL_VAULT>/
        generations/
            <generation_id>/
                package/
                    generated/
                    _atds_generation/
                PUBLICATION-MANIFEST.json
                INDEX.md
        CURRENT.md

The inner:

    package/

is the exact sealed P5-D3F package.

It remains byte-exact and immutable.

Publication metadata stays outside the sealed package.

Existing mismatched or partial generation targets may never be overwritten.

An exact completed target may be reused only as part of governed recovery.

## 9. CURRENT

Production CURRENT schema:

    ATDS_OBSIDIAN_P5D3G_CURRENT_V0_1

Required identity includes:

    generation_id
    publication_generation_digest_sha256
    candidate_head
    candidate_tree

The link form is:

    [[generations/<generation_id>/INDEX|Open active generation]]

The target generation must be completely verified before CURRENT.tmp is created.

CURRENT.tmp must be:

    exclusively created
    flushed
    fsynced
    byte-verified

before atomic replace.

## 10. Retry semantics

Write retries are bounded to the previously qualified Windows sharing-conflict class:

    PermissionError
    winerror in {5, 32}

Bounded policy:

    deadline = 5 s
    initial backoff = 10 ms
    maximum backoff = 500 ms

On a retryable failed replace:

    CURRENT must still equal planned previous CURRENT
    CURRENT.tmp must still equal the planned candidate

After success:

    CURRENT.tmp must be absent
    CURRENT bytes must equal planned bytes
    CURRENT generation must equal target generation
    CURRENT digest must equal verified target digest

Reader access retry must preserve the qualified P5-C3R2 EACCES semantics.

## 11. Replace and bootstrap modes

The contract distinguishes:

    REPLACE_EXISTING_CURRENT
    BOOTSTRAP_NO_CURRENT

Replace mode requires exact capture and revalidation of the previous CURRENT and previous generation.

Bootstrap requires CURRENT to be absent and requires explicit bootstrap authorization.

Bootstrap ambiguity after pointer publication may not be resolved by automatically deleting CURRENT.

## 12. Crash recovery

Recovery is state-based.

Every recovery action must first reread:

    CURRENT
    CURRENT.tmp
    target generation
    persisted transaction evidence

Examples:

If CURRENT still points to the old generation and the new immutable target is complete, the transaction may resume.

If CURRENT already points to the new complete verified generation, recovery must complete forward rather than blindly roll back because an evidence write was interrupted.

If CURRENT points to the new generation but the target is invalid, replace mode may roll back only to the exact captured previous CURRENT after reverifying the previous generation.

Ambiguous states block for adjudication.

The last-known-good generation may not be deleted.

## 13. Physical versus logical confirmation

P5-D2 established:

    EVALUATION_PASSED != PROMOTION_CONFIRMED

P5-D3G adds:

    pointer replace != logical confirmation

PROMOTION_CONFIRMED may occur only after:

    target verified
    CURRENT verified
    physical publication receipt durably persisted

If physical publication is complete but logical confirmation cannot be recorded, the distinct recovery state is:

    PASS_PHYSICAL_PUBLICATION_LOGICAL_CONFIRMATION_PENDING

It must not be relabelled as full success or full failure.

## 14. Graph/Search

Multiple immutable generations may physically coexist.

P5-D3G makes no claim that Obsidian Graph/Search exposes only CURRENT.

That remains:

    P6 — CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE

## 15. Current authority boundary

This V0.1 contract authorizes only contract tests.

It does not authorize:

    P5-D3G runtime implementation
    sacrificial live-Vault execution
    production real-Vault execution
    real Vault writes
    CURRENT creation or mutation
    P5-D2 PROMOTION_CONFIRMED emission
    automatic publication
    background observer
    polling
    startup persistence
    scheduled task
    Windows service
    Graph/Search CURRENT semantics

## 16. Next gate

Only after this contract passes static review and a governed local re-break may the next candidate boundary open:

    P5-D3G —
    FINITE LIVE PUBLICATION TRANSACTION
    IMPLEMENTATION + SACRIFICIAL LIVE-VAULT QUALIFICATION

No real-Vault execution is part of that implementation qualification gate.
