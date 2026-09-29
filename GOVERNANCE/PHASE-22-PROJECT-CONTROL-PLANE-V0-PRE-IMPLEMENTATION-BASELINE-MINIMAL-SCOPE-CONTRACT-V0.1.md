# ATDS — PHASE 22
## PROJECT CONTROL PLANE V0
### PRE-IMPLEMENTATION BASELINE + MINIMAL SCOPE CONTRACT — CANDIDATE V0.1

**Status:** `DRAFT_FOR_HUMAN_ADJUDICATION`  
**Implementation authority:** `NONE`  
**Repository mutation authority:** `NONE`

---

## 1. PURPOSE

Phase 22 exists to reduce human middleware in ATDS without reducing experimental, repository, epistemic or authority guarantees.

The target is:

```text
REDUCE HUMAN TRANSPORT WORK
WITHOUT TRANSFERRING HUMAN AUTHORITY
```

The Project Control Plane V0 is an ATDS-only pilot.

It is not a universal agent framework.

---

## 2. CANONICAL BASELINE

```text
repository =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

branch =
integration/system-v1

baseline_head =
5a61c6150583234b486f6dc614f5071e89cbd3c0

baseline_tree =
50347ff1f8cd41491e949c2716f9fc4c9d182f64
```

GitHub repository state and validated governance/evidence artifacts remain canonical.

Conversation state, Obsidian state, cached manifests and recovery documents are not independent authorities.

---

## 3. VERIFIED MOTIVATING FAILURE

The current:

```text
04-REFERENCE/RECOVERY-CHECKPOINT.md
```

does not represent the complete current state of the repository.

It terminates before subsequent E1 execution, closure and E1-TD work.

Therefore:

```text
MANUALLY MAINTAINED ACTIVE STATE
MAY BECOME STALE
```

This is an observed project failure mode.

The Project Control Plane must not solve this by creating another manually maintained authoritative manifest.

---

## 4. TARGET STATE MODEL

The authoritative model shall be:

```text
CANONICAL REPOSITORY
+ GOVERNANCE DECISIONS
+ EVIDENCE
+ VERIFIED LOCAL GIT STATE WHEN AVAILABLE
                ↓
        PURE STATE PROJECTOR
                ↓
          ACTIVE STATE V0
```

Rule:

```text
ACTIVE STATE = DERIVED
ACTIVE STATE != AUTHORITY
CACHE != AUTHORITY
```

Any cached representation must be reproducible from canonical inputs.

---

## 5. V0 COMPONENTS

Project Control Plane V0 is limited initially to:

```text
P22-V0-01
PURE STATE PROJECTOR

P22-V0-02
IDENTITY / STATE VERIFIER

P22-V0-03
EVIDENCE ENVELOPE RECORDER
```

Nothing else is required for initial qualification.

---

## 6. PURE STATE PROJECTOR

The projector must derive, where evidence exists:

```text
repository
branch
remote_head
remote_tree
local_head
local_tree
working_tree_state

active_contracts
protected_artifact_blobs

current_frontier
open_blockers
hard_stops

last_completed_boundary
next_permitted_boundary

authority_state

experimental_exposure_state
```

Unknown information must remain explicitly:

```text
UNKNOWN
```

It must never be inferred as PASS, CLEAN or AUTHORIZED.

Example:

```text
local working tree not inspected
→ LOCAL_WORKTREE_STATE = UNKNOWN

not
→ CLEAN
```

---

## 7. IDENTITY VERIFIER

The verifier must mechanize repeated identity controls including:

```text
repository identity
branch identity
HEAD
TREE
protected blobs
contract identities
breaker identities
runtime identities
```

A mismatch produces a fail-closed status.

Example statuses:

```text
PASS
BLOCKED_REPOSITORY_MISMATCH
BLOCKED_BRANCH_MISMATCH
BLOCKED_HEAD_DRIFT
BLOCKED_TREE_DRIFT
BLOCKED_PROTECTED_BLOB_DRIFT
UNKNOWN_LOCAL_STATE
```

It must not automatically repair any mismatch.

---

## 8. EVIDENCE ENVELOPE

Every future Control Plane operation must be capable of producing an evidence envelope containing at minimum:

```text
OPERATION_ID
OPERATION_CLASS
COMMAND_OR_CHECK

START_HEAD
START_TREE

END_HEAD
END_TREE

EXIT_CODE

STDOUT
STDERR

FILES_CHANGED

TEST_RESULTS
PROBE_RESULTS

ARTIFACT_HASHES

STARTED_AT_UTC
FINISHED_AT_UTC

AUTHORITY_REFERENCE

FINAL_STATUS
```

The purpose is to remove manual copying of command outputs and identity values.

---

## 9. INITIAL OPERATION CLASSES

For V0:

### A. READ_ONLY_INFORMATIONAL

Examples:

```text
git rev-parse
git status
git diff
repository metadata
branch metadata
hash calculation
artifact identity verification
report inspection
state derivation
```

These may eventually be automatically executable when mechanically safe.

### B. TEST_OR_PROBE

Tests and probes must be treated separately because some tools can create temporary files, caches or generated outputs.

Their filesystem effects must therefore be measured rather than assumed absent.

### C. MUTATION

Includes:

```text
source modification
contract modification
test modification
file creation in repository
file deletion
commit
push
merge
branch movement
deployment
external side effect
```

For Project Control Plane V0:

```text
MUTATION = DISABLED
```

---

## 10. MECHANICAL != SELF-DECLARED

The system must never rely on:

```text
agent says "this is mechanical"
```

A future mechanical classification must be computed from evidence such as:

```text
protected paths
frozen contract identities
frozen test identities
before/after diff
behavioral differential
authority policy
```

Any unresolved semantic ambiguity produces:

```text
HUMAN_STOP
```

The classifier itself is not required in the first implementation slice.

---

## 11. HUMAN AUTHORITY PRESERVED

The following remain outside automatic authority:

```text
scope changes
contract semantic changes
strategy changes
new hypotheses
OOS/window changes
dataset substitution
threshold changes
authority-policy changes
real experiment authorization
rerun authorization
commit
push
merge
delete
deployment
external actions
```

Automation of evidence does not imply authorization of action.

---

## 12. E1 / E1-TD ISOLATION

Phase 22 must not reopen or alter:

```text
MOMENTUM_V1
E1
E1 OOS
E1 execution assumptions
E1 result
E1 experimental memory
E1-TD/H2
TD-01 thresholds
TD-02 temporal window
TD-03 dataset identity
TD-03A collector qualification
TD-03B event authority
```

Specifically:

```text
TD03B_EVENT_BUDGET = 0 / 1
```

must remain unchanged by Phase 22.

Project Control Plane qualification must not consume any E1-TD collection event.

---

## 13. NO PERFORMANCE ACCESS REQUIREMENT

Project Control Plane V0 does not require:

```text
PnL
strategy performance
tail-dependence result
new Momentum execution
new backtest
new OOS inspection
```

These are outside Phase 22 V0 scope.

---

## 14. INITIAL ACCEPTANCE TESTS

Before V0 can be considered qualified, tests must demonstrate at least:

### T22-01 — Wrong repository

Wrong repository identity:

```text
→ BLOCKED_REPOSITORY_MISMATCH
```

### T22-02 — Wrong branch

Wrong branch:

```text
→ BLOCKED_BRANCH_MISMATCH
```

### T22-03 — HEAD drift

Canonical state changes between observation boundaries:

```text
→ BLOCKED_HEAD_DRIFT
```

### T22-04 — TREE drift

Unexpected tree identity:

```text
→ BLOCKED_TREE_DRIFT
```

### T22-05 — Protected blob drift

Protected contract/runtime/test identity changes:

```text
→ BLOCKED_PROTECTED_BLOB_DRIFT
```

### T22-06 — Unknown local worktree

Unavailable local status:

```text
→ UNKNOWN_LOCAL_STATE
```

It must not become `CLEAN`.

### T22-07 — Stale recovery state

A recovery/checkpoint document disagrees with canonical repository evidence:

```text
→ STALE_DERIVED_STATE_DETECTED
```

Canonical GitHub state wins.

### T22-08 — Cache corruption

A stored Active State cache is altered:

```text
→ REBUILD_FROM_CANONICAL
```

No authority may be derived from the corrupted cache.

### T22-09 — Mutation attempt

Any V0 operation classified as repository mutation:

```text
→ BLOCKED_OUT_OF_SCOPE
```

### T22-10 — E1-TD isolation

Any attempt to consume TD-03B, compute performance or change H2:

```text
→ BLOCKED_PROTECTED_RESEARCH_TRACK
```

### T22-11 — Evidence completeness

A supposedly completed operation missing mandatory evidence fields:

```text
→ INCOMPLETE_EVIDENCE
```

### T22-12 — No silent retry

A failed or blocked operation:

```text
→ STOP
```

unless an existing contract explicitly permits deterministic replay.

---

## 15. HUMAN-COST MEASUREMENT

Historical human time is not known precisely enough to invent a quantitative baseline.

V0 shall therefore begin collecting prospective workflow telemetry.

Candidate measures:

```text
manual copy/paste transfers
manual identity entries
human authorization requests
human STOPs
state reconstruction operations
historical rereads
duplicate state/report text
machine checks executed
failed checks
unknown-state escalations
```

Timing may also be collected prospectively.

No historical time estimate shall be represented as measured fact.

---

## 16. NON-GOALS

Phase 22 V0 explicitly excludes:

```text
Agent Maître
multi-project orchestration
general-purpose autonomous agent
RAG platform
large Obsidian architecture
cloud orchestration
autonomous coding
automatic strategy research
automatic Git mutation
automatic authority granting
```

Pilot scope:

```text
PROJECT CONTROL PLANE
        ↓
      ATDS ONLY
```

---

## 17. IMPLEMENTATION SEQUENCING

If this contract is human-adopted, the next boundary should remain minimal:

```text
P22-01
PURE STATE PROJECTOR
TEST-FIRST CONTRACT + RED
```

Only after qualification:

```text
P22-02
IDENTITY VERIFIER
```

Then:

```text
P22-03
EVIDENCE ENVELOPE
```

Approval-gate automation and mutation orchestration remain later work.

---

## 18. CURRENT AUTHORITY

```text
PHASE_22_BASELINE = PRODUCED

PHASE_22_CONTRACT =
DRAFT_FOR_HUMAN_ADJUDICATION

PROJECT_CONTROL_PLANE_IMPLEMENTATION =
NOT_AUTHORIZED

REPOSITORY_MUTATION =
NOT_AUTHORIZED

E1_TD_MUTATION =
NOT_AUTHORIZED

TD03B_EVENT_CONSUMPTION =
NOT_AUTHORIZED

STOP =
TRUE
```

---

## 19. NEXT HUMAN BOUNDARY

The permitted next action is human adjudication of this contract:

```text
ADOPT
ADOPT_WITH_AMENDMENTS
REJECT
```

No implementation follows implicitly from production of this draft.
