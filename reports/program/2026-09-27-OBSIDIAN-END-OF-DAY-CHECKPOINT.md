# OBSIDIAN — END-OF-DAY CHECKPOINT

Date: 2026-09-27

## Purpose

Freeze the exact end-of-day state of the governed Obsidian projection work so the next session can resume without reconstructing context from chat history.

This document is evidence-only.
It does not authorize publication, promotion, CURRENT mutation, real-Vault writes, background observation, polling, startup persistence, or Graph/Search CURRENT semantics.

---

## 1. Where the day started

At the beginning of today's P5-D3E sequence:

- P5-D3D finite candidate evaluation implementation was already qualified;
- the qualified P5-D3D evaluator blob was:

      bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

- the next frontier was P5-D3E;
- the P5-D3E real exact-head sandbox contract existed but still required local governed re-break before implementation could be authorized;
- no real integration/system-v1 candidate had yet been qualified through P5-D3E;
- no publication or CURRENT transition was authorized.

The day therefore started at the boundary:

    qualified finite evaluator
        ↓
    P5-D3E contract qualification still required
        ↓
    real exact-head path not yet demonstrated

---

## 2. P5-D3E contract qualification completed

Contract branch:

    feat/obsidian-projection-p5d3e-real-exact-head-sandbox-v0.1

Qualified contract candidate:

    3d76f3402c7eaba6e911d5f6e3038e9720be2284

Contract blob:

    ae4b1691fae16fcd1616e265a089670b9654db4a

Contract qualification evidence commit:

    f413171075fb002b7c6080a10247cad65954f2be

Qualification report blob:

    0304fbeb54ee80a1b3c74cf8c0c3433e8eb6846c

USER-REPORTED LOCAL EXECUTION:

    Ran 1037 tests in 17.181s
    OK
    P5D3E_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3E_CONTRACT_REBREAK_COMPLETED=PASS

Consequence:

    P5-D3E implementation became authorized.

---

## 3. P5-D3E implementation built

Implementation branch:

    feat/obsidian-projection-p5d3e-real-exact-head-sandbox-implementation-v0.1

The implementation introduced:

    tools/obsidian_projection/p5d3e_verify.py
    tests/obsidian_projection/test_p5d3e_verify.py
    tests/obsidian_projection/test_p5d3e_adversarial.py
    docs/OBSIDIAN-P5D3E-REAL-EXACT-HEAD-SANDBOX-IMPLEMENTATION-V0.1.md

The harness established a strict split:

    resolve_real_candidate()
        ↓
    governed exact branch resolution
        ↓
    run_pre_resolved_sandbox()
        ↓
    network-free evaluator phase

Real wrapper:

    run_real_exact_head_qualification()

The public pre-resolved path cannot claim a real PASS.

---

## 4. Implementation defects found and closed

### 4.1 Invalid git_blob_oid import

First targeted implementation run failed because:

    p5d3e_verify.py

imported:

    git_blob_oid

from:

    git_source.py

but that symbol did not exist there.

USER-REPORTED LOCAL EXECUTION:

    Ran 134 tests in 2.672s
    FAILED (errors=2)

The failure was persisted.

Correction:

- remove invalid public import;
- add local canonical Git blob OID helper;
- use:

      SHA1("blob " + byte_length + NUL + raw_bytes)

- add known-vector unit breaker.

Corrected harness blob:

    bd7f63b08432a53eaff5deeb2147396eb60d723f

Corrected harness-test blob:

    fe47910cf7f10a09021d958d7ae60693d0def4bf

### 4.2 Dirty local worktree blocked qualification

A later qualification attempt correctly blocked because the local worktree contained:

    M tools/obsidian_projection/p5d3e_verify.py

No tests were accepted under that dirty state.

A safe external backup/recovery path was used before retrying.

### 4.3 Formatting-dependent alternates breaker

A later targeted run reported:

    Ran 153 tests in 8.252s
    FAILED (failures=1)

Static review identified a deterministic formatting-dependent adversarial assertion for:

    .git/objects/info/alternates

The runtime correctly enforced the path, but the test required the source code to be formatted on one physical line.

Only the adversarial breaker was corrected.

Final adversarial-test blob:

    6b159ede31fb26ac366f9c69cd72256ee553753c

No P5-D3E runtime semantics changed in that correction.

---

## 5. P5-D3E implementation qualification completed

Final qualified functional candidate:

    7c6ecec2498d48c4623ecd40aed6c3816f4930b9

Qualification evidence commit:

    1e03d539d48c0fb4760d1b6091e1b2faa125042b

Qualification report blob:

    c48f716b753f4aa09a714fd66681075ebabe07bb

Final qualified implementation artifacts:

P5-D3E contract:

    ae4b1691fae16fcd1616e265a089670b9654db4a

P5-D3E runtime harness:

    bd7f63b08432a53eaff5deeb2147396eb60d723f

P5-D3E harness tests:

    fe47910cf7f10a09021d958d7ae60693d0def4bf

P5-D3E adversarial tests:

    6b159ede31fb26ac366f9c69cd72256ee553753c

Qualified P5-D3D evaluator:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

USER-REPORTED LOCAL EXECUTION:

    Ran 1058 tests in 25.564s
    OK
    P5D3E_FULL_REBREAK=PASS
    CONTROL_CLONE_CLEAN_AFTER_TESTS=PASS

Focused pre-resolved sandbox:

    Ran 3 tests in 4.842s
    OK
    P5D3E_PRE_RESOLVED_SYNTHETIC_SANDBOX=PASS
    CONTROL_CLONE_CLEAN=PASS
    P5D3E_IMPLEMENTATION_QUALIFICATION_COMPLETED=PASS

Consequence:

    first real exact-head evaluation became authorized.

---

## 6. First real integration/system-v1 exact-head run completed

First real-run preflight evidence commit:

    1703733ad44015f11856b11361fa2d5f71381431

The run intentionally did not hardcode the contextual integration/system-v1 HEAD.

The qualified resolver performed the governed candidate-resolution path and froze the actual candidate observed at runtime.

Real candidate HEAD:

    89710b879751d7fcebccf75cd03e64368f1b0e96

Real candidate TREE:

    dc85bdb0708f4980e3a0cead0f15c6d077f90290

GitHub verification:

    commit message:
    A0: qualify governed V0.5 replay

At qualification persistence time integration/system-v1 still pointed to the same candidate HEAD.

USER-REPORTED REAL-RUN ADJUDICATION:

    PYTHON_EXIT_CODE=0
    REPORT_STATUS=PASS_REAL_EXACT_HEAD_FINITE_EVALUATION

    REAL_CANDIDATE_HEAD=89710b879751d7fcebccf75cd03e64368f1b0e96
    REAL_CANDIDATE_TREE=dc85bdb0708f4980e3a0cead0f15c6d077f90290

    REAL_BUILD_A_B_EQUAL=PASS
    REAL_METADATA_ONLY_BODY_READ_COUNT=0
    REAL_ARTIFACT_COMPLETENESS=PASS
    REAL_PACKAGE_SEALED_UNPROMOTED=PASS
    REAL_PACKAGE_REVERIFICATION=PASS

    P5D3E_REAL_EXACT_HEAD_QUALIFICATION=PASS
    CONTROL_CLONE_CLEAN_AFTER_REAL_RUN=PASS
    P5D3E_FIRST_REAL_EXACT_HEAD_RUN_COMPLETED=PASS

Real qualification evidence commit:

    a24c248a68f530f82a1f0c578036ccd4b8a54fee

Real qualification report blob:

    cfced8795db722d7fdb294112513ce2f0f9930a3

---

## 7. Exact end-of-day state

The following chain is now demonstrated on a real core candidate:

    integration/system-v1 exact HEAD
        ↓
    governed exact-head resolution
        ↓
    exact HEAD/TREE freeze
        ↓
    sacrificial isolated Git repository
        ↓
    P5-D2 controlled evaluation activation
        ↓
    P5-B2 DynamicInventory
        ↓
    P5-D3B current-head semantic bridge
        ↓
    Build A
        ↓
    Build B
        ↓
    deterministic equality
        ↓
    CHP-B01..B12
        ↓
    P5-D3C2 package staging
        ↓
    SEALED_UNPROMOTED
        ↓
    second read-only package verification
        ↓
    QUALIFIED

Critical real-path properties demonstrated:

    Build A = Build B
    metadata_only_body_read_count = 0
    artifact_record_count = source_record_count
    package = PASS_SEALED_UNPROMOTED
    package reverification = PASS
    P5-D2 result event emitted
    live projection unchanged
    real Vault unchanged
    CURRENT not created
    production promotion not authorized
    candidate repository cleaned
    evaluation workspace removed
    control repository clean

P5-D3E is therefore qualified both on:

    synthetic/pre-resolved implementation path

and:

    one real exact-head integration/system-v1 candidate path.

---

## 8. What is NOT yet built

The system still stops deliberately at:

    SEALED_UNPROMOTED

There is no qualified path yet from:

    SEALED_UNPROMOTED
        ↓
    live publication / CURRENT

Therefore none of the following exists as an authorized runtime boundary:

    actual promotion
    CURRENT mutation
    live generation switch
    real Vault publication
    crash-safe publication transaction
    rollback transaction
    live observer promotion confirmation tied to a physical publication
    background observer loop
    polling
    startup persistence
    Graph/Search CURRENT semantics

---

## 9. Work remaining before the next major block

The next major block is publication/promotion.

Before implementing any publication runtime, the following must be done contract-first.

### 9.1 Close P5-D3E formally

This end-of-day checkpoint records the closure state.

No further P5-D3E runtime change is currently required unless a later publication contract depends on an interface that reveals a gap.

### 9.2 Define the next governed frontier

A new contract must define the exact transition from:

    qualified SEALED_UNPROMOTED generation

to:

    live/current generation

The frontier name is not yet frozen.

Do not implement it before its contract is written, reviewed, preregistered and qualified.

### 9.3 Bind publication to existing qualified authorities

The next contract should reuse rather than reinvent:

- P5-C2 atomic publication/swap properties;
- P5-D2 logical PROMOTION_CONFIRMED event semantics;
- P5-D3C2 sealed package identity;
- P5-D3D/P5-D3E exact candidate and scientific identity evidence.

It must explicitly define which authority owns:

    physical publication
    logical confirmation
    current generation identity
    rollback authority

### 9.4 Define the publication state machine

At minimum define deterministic states such as:

    SEALED_UNPROMOTED
    PROMOTION_PREPARED
    PROMOTION_COMMITTED
    CURRENT_CONFIRMED
    PROMOTION_FAILED
    ROLLBACK_PREPARED
    ROLLBACK_COMMITTED

Exact names remain to be governed.

Must specify:

    allowed transitions
    forbidden transitions
    idempotency
    replay behavior
    crash recovery
    stale candidate handling
    already-current handling
    partial publication handling

### 9.5 Define CURRENT semantics

Before any pointer is written, define:

    exact CURRENT representation
    exact generation identity binding
    atomic write/swap mechanism
    parent/root restrictions
    no symlink/junction/reparse traversal
    single-link expectations
    read-after-write verification
    stale CURRENT rejection
    malformed CURRENT behavior
    interrupted write behavior

### 9.6 Define live-Vault publication boundary

The contract must define:

    exact authorized live root
    what may be created
    what may never be modified
    whether publication copies, renames or swaps a generation root
    how pre-existing data is protected
    how path aliases are rejected
    what evidence proves no unrelated file changed

### 9.7 Define rollback before promotion is allowed

Promotion must not be authorized before rollback semantics exist.

Need to preregister:

    previous-current identity
    rollback target identity
    rollback admissibility
    rollback atomicity
    rollback verification
    crash during rollback
    failed rollback outcome
    audit evidence

### 9.8 Define concurrency / single-writer rules

Need explicit behavior for:

    two promotion attempts
    promotion while another promotion holds lock
    stale lock
    crashed writer
    same generation promoted twice
    different generation competing for CURRENT

### 9.9 Preregister publication breakers

Before runtime implementation, the contract should include adversarial families covering at least:

    wrong candidate HEAD
    wrong candidate TREE
    wrong generation digest
    tampered SEALED package
    package no longer SEALED_UNPROMOTED
    stale candidate after newer qualification
    malformed CURRENT
    CURRENT points to unknown generation
    CURRENT points outside authorized root
    partial CURRENT write
    two writers
    hardlink alias
    symlink/junction/reparse alias
    wrong live root
    package/live-root overlap
    crash before swap
    crash during swap
    crash after swap but before confirmation
    confirmation without physical publication
    physical publication without matching confirmation
    promotion from REJECTED candidate
    promotion from BLOCKED candidate
    rollback to unqualified generation
    rollback after evidence mismatch
    repeated/idempotent promotion
    stale observer confirmation

### 9.10 Keep the next phase contract-only first

The next session should NOT begin by writing publication runtime.

The correct first action is:

    publication/promotion architecture review
        ↓
    exact contract
        ↓
    adversarial breaker registry
        ↓
    contract qualification
        ↓
    only then minimal runtime candidate

---

## 10. Current hard prohibition set

Still forbidden at end of day:

    production promotion
    CURRENT mutation
    real Vault write
    background observer
    polling
    Windows startup/task/service persistence
    Graph/Search CURRENT semantics

These prohibitions remain active until a later governed frontier explicitly qualifies them.

---

## 11. Resume point for next session

Resume exactly from:

    P5-D3E CLOSED / QUALIFIED
        ↓
    publication/promotion frontier NOT YET OPENED

First task next session:

    design the publication/promotion frontier contract

with explicit reuse analysis of:

    P5-C2
    P5-D2
    P5-D3C2
    P5-D3D
    P5-D3E

Do not implement publication runtime before that contract exists and passes its own governance boundary.
