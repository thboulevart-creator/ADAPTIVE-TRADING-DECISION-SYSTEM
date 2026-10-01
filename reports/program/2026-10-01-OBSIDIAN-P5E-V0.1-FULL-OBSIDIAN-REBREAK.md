# P5-E V0.1 — FULL OBSIDIAN RE-BREAK

Date: 2026-10-01

## Final admissible verdict

```text
ADMISSIBLE_FULL_OBSIDIAN_REBREAK
= 1466 / 1466 PASS

CONTROL_CLONE_HEAD
= f146201301b150efb35713e7aed3f0105821d41c

CONTROL_CLONE_POST_STATUS
= CLEAN

P5D4_RUNTIME_BLOB
= UNCHANGED

REAL_VAULT_PRE_POST
= BYTE-FINGERPRINT_IDENTICAL

REAL_P5E
= CLOSED
```

This report distinguishes the final admissible evidence from two earlier non-admissible harness attempts.

## 1. Scope

This is qualification evidence for:

`P5-E — END-TO-END NEAR-REAL-TIME QUALIFICATION V0.1`

at the authorized:

`CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY`

stage.

No real P5-E polling, remote observation loop, evaluation, promotion, publication, Stage A, Stage B, P6, daemon, Scheduled Task, Windows Service, startup registration, Vault mutation, or CURRENT mutation was authorized or executed.

## 2. Earlier evidence attempts — not used as final proof

### 2.1 Primary-worktree full run

A full suite completed on the primary worktree and reported:

```text
Ran 1466 tests in 250.650s
OK
```

It began at:

`0e568da338043654de84949488413763f56d9cd9`

and P5-D4 runtime remained:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

However, the primary worktree had a provenance anomaly during the broader qualification flow: the P5-E contract/model were observed temporarily at non-authoritative worktree blobs and later returned to their committed blobs without a restoration action issued by the controlling flow.

A documentation-only commit also advanced the branch during that run.

Therefore this run is retained as functional evidence but is not the final admissible full-rebreak proof.

### 2.2 First isolated-clone wrapper attempt

A fresh exact control clone was created, but the PowerShell wrapper used `ErrorActionPreference=Stop`. A non-failing LF/CRLF warning emitted on native `stderr` was promoted by PowerShell to `NativeCommandError`, aborting the wrapper before a unittest verdict.

That attempt is classified:

```text
TEST_VERDICT
= NOT_OBTAINED

HARNESS_FAILURE
= POWERSHELL_STDERR_POLICY

QUALIFICATION_EVIDENCE
= NOT_ADMISSIBLE
```

No product/runtime correction resulted from this harness failure.

## 3. Final admissible execution identity

Fresh disposable clone origin:

`https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM.git`

Branch:

`feat/obsidian-projection-p5e-end-to-end-near-real-time-qualification-v0.1`

Exact clone HEAD:

`f146201301b150efb35713e7aed3f0105821d41c`

Pre-run control clone status:

`CLEAN`

Pinned blobs:

- P5-E contract: `e5c3d7a9d451aba65e8062078c6c10d23e586f39`
- P5-E synthetic model: `8662dd97a1c8a1af33d6593ae923384e96404b5a`
- P5-E base test: `2305e0768182d82657c34a7cb53c502714a2ab81`
- P5-E adversarial test: `6235c4b2addc16acd043832664440ec76f6dada2`
- P5-D4 runtime: `1825e53d195ba2a63b5b646a5b78eb77939b94b5`

## 4. Real-state pre-fingerprint

Immediately before the admissible run:

```text
CURRENT_SHA256
= 867c639b164d9bd9a37bf0045c3181c6dde93aebfcf47f1a384bb4c3668107b9

CURRENT_TMP_PRESENT
= false

VAULT_CONTENT_TREE_SHA256
= 1f9d192845950f3929714faa7a2f09fadad6a264aab3158ee22523951122ed9a
FILES = 2210

OBSIDIAN_TREE_SHA256
= 3d0b8704f662d5c1fe385ca15b99beca27f37c94b2284e392c2b0ba1ac98f7a9
FILES = 5

CURRENT_GENERATION_TREE_SHA256
= f6aee8f8e2dc1044946f0aae121c23b35d9887a3e7b2642753d29c03e15f22d3
FILES = 2110

P5D3G_EVENT_LOG_SHA256
= ad414d170626a0d238fc37161c4c04f54c660a17573d7f77607c0374045d7af2

P5D4_OBSERVER_EVENTS_SHA256
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

P5D4_CHECKPOINT_SHA256
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

P5D4_LAST_RUN_SHA256
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259

P5D4_OWNERSHIP_LOCK_PRESENT
= false
```

## 5. Command and result

```text
python -B -m unittest discover -s tests/obsidian_projection -p 'test_*.py'
```

Observed:

```text
Ran 1466 tests in 242.153s

OK

FULL_EXIT=0
FULL_SECONDS=243.785
```

Non-failing observations:

- one sample-worktree LF/CRLF warning;
- historical `ResourceWarning` messages for unclosed subprocess text streams.

Neither changed the unittest result.

Captured stderr evidence SHA-256:

`53832283fdc94523eb8c2800fcf740041f9aad909626612d5b77bfe97160e6bd`

## 6. Post-run integrity

After removing only generated Python bytecode residue inside the disposable clone:

```text
CONTROL_POST_STATUS_COUNT
= 0

CONTROL_HEAD_AFTER
= f146201301b150efb35713e7aed3f0105821d41c

P5D4_RUNTIME_BLOB_AFTER
= 1825e53d195ba2a63b5b646a5b78eb77939b94b5
```

The complete real-state post-fingerprint was byte-for-byte identical to the pre-fingerprint:

```text
PRE_POST_EQUAL
= true
```

Therefore the admissible full re-break produced no observed mutation of:

- live Vault content;
- `.obsidian`;
- active generation;
- `CURRENT.md`;
- `CURRENT.tmp`;
- P5-D3G publication evidence;
- P5-D4 event log;
- P5-D4 checkpoint;
- P5-D4 last-run state;
- P5-D4 ownership state.

## 7. Adjudication

```text
FULL_OBSIDIAN_REBREAK
= PASS

EXACT_REMOTE_HEAD
= VERIFIED

EXACT_CANDIDATE_BLOBS
= VERIFIED

CONTROL_CLONE_CLEAN_BEFORE
= PASS

CONTROL_CLONE_CLEAN_AFTER
= PASS

REAL_STATE_NON_MUTATION
= PASS

P5D4_RUNTIME_IDENTITY
= PRESERVED

REAL_P5E_EXECUTION
= NOT_PERFORMED
```
