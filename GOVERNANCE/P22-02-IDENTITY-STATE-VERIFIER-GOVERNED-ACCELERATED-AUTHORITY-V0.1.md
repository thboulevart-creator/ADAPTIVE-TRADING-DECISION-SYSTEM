# P22-02 — IDENTITY / STATE VERIFIER
## GOVERNED ACCELERATED AUTHORITY V0.1

Date: 2026-09-29

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branch: `integration/system-v1`

## 1. Human authorization

The human explicitly authorized:

```text
P22-02
—
IDENTITY / STATE VERIFIER
—
GOVERNED ACCELERATED ENGINEERING CYCLE
```

This authorization is intentionally bounded.

Its purpose is to allow P22-02 to collect and verify real Git repository state and produce a verified canonical-input snapshot consumable by the already-qualified P22-01 Pure State Projector.

This authorization does not grant autonomous repository authority.

## 2. Authorization base

Immediately before adoption, canonical GitHub state was independently revalidated as:

```text
repository =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

branch =
integration/system-v1

HEAD =
0a4570c37eadefa7ee22b41d979fcb6dfeeb5131

TREE =
00df67542c68c1899dfee0a201e13bd02d0c3b5d
```

Protected identities:

```text
PHASE_22_CONTRACT_BLOB =
afc519d3e937dfcde2ce1e0bf7d2646dd010a8ce

PHASE_22_ADOPTION_BLOB =
90f6405435c62869f220ebe8783fc138d133ee93

P22_01_CONTRACT_BLOB =
503a2f0d63b7de1a553119fed6280860a3125e0a

P22_01_RUNTIME_BLOB =
18b01a995f521377ec98bd4f24b7837a329ad139

P22_01_QUALIFICATION_BLOB =
02dee12b98855977d8c5435e8c97bdc0b7947b33

E1_TD_03B_AUTHORITY_BLOB =
7ea58d02387d67e7360356a10c0eaed441d0b2f4
```

Any unexplained mismatch before P22-02 begins requires STOP.

## 3. Sole objective

The only component authorized is:

```text
P22-02
IDENTITY / STATE VERIFIER
```

Its role is:

```text
REAL LOCAL GIT STATE
+
EXPECTED CANONICAL BINDINGS
        ↓
READ-ONLY VERIFICATION
        ↓
VERIFIED SNAPSHOT
        ↓
P22-01 PURE STATE PROJECTOR
        ↓
DERIVED ACTIVE STATE
```

P22-02 verifies evidence. P22-01 projects state. Neither component grants authority.

## 4. Required separation

P22-02 may:

```text
OBSERVE
VERIFY
COMPARE
CLASSIFY
REPORT
```

P22-02 may not:

```text
REPAIR
CHECKOUT
RESET
CLEAN
FETCH
PULL
MERGE
COMMIT
PUSH
DELETE
EDIT
REBASE
TAG
DEPLOY
```

A mismatch must remain a mismatch.

## 5. Authorized governed cycle

Within this single authorization:

```text
1. fresh GitHub identity/base verification
2. preregister P22-02 executable contract
3. preregister frozen test/breaker surface
4. persist contract and breaker before runtime
5. execute TEST-FIRST RED
6. persist RED evidence
7. implement minimum verifier
8. execute frozen breaker
9. implementation-only mechanical corrections if directly required
10. repeat frozen breaker as necessary
11. adversarial verification
12. verify P22-02 → P22-01 compatibility
13. real read-only qualification on fresh clean clone
14. independently compare local identities with GitHub canonical identities
15. verify protected blobs unchanged
16. exact persisted-HEAD re-break
17. authorized-path audit
18. persist qualification evidence
19. HARD STOP
```

No human micro-approval is required inside this exact cycle while all frozen boundaries pass.

## 6. Freeze rule

After first RED:

```text
P22_02_CONTRACT = FROZEN
P22_02_BREAKER = FROZEN
```

If contract/breaker correction is required after RED:

```text
STOP_FOR_HUMAN_ADJUDICATION
```

The agent must not weaken an expectation to manufacture PASS.

## 7. Authorized paths

Only:

```text
GOVERNANCE/P22-02-IDENTITY-STATE-VERIFIER-GOVERNED-ACCELERATED-AUTHORITY-V0.1.md
GOVERNANCE/P22-02-IDENTITY-STATE-VERIFIER-CONTRACT-V0.1.json
breakers/p22_02_identity_state_verifier_red_breaker.py
tools/p22_02_identity_state_verifier.py
reports/program/2026-09-29-P22-02-IDENTITY-STATE-VERIFIER-TEST-FIRST-RED.md
reports/program/2026-09-29-P22-02-IDENTITY-STATE-VERIFIER-QUALIFICATION.md
```

Optional only if technically necessary:

```text
.github/workflows/p22-02-identity-state-verifier-qualification.yml
```

No other repository path may be mutated.

## 8. Read-only Git surface

The runtime may invoke only preregistered observational Git operations.

Candidate minimum:

```text
git rev-parse --show-toplevel
git remote get-url origin
git branch --show-current
git rev-parse HEAD
git rev-parse HEAD^{tree}
git status --porcelain --untracked-files=all
git rev-parse HEAD:<protected-path>
```

Requirements:

```text
fixed argument arrays
no shell interpolation
shell=False
no arbitrary command runner
```

## 9. Network boundary

Runtime network operations are forbidden:

```text
git fetch
git pull
git ls-remote
HTTP
GitHub API
arbitrary remote access
```

Expected remote canonical bindings are supplied externally.

## 10. Required observations

At minimum:

```text
repository root
origin remote identity
repository_full_name
current branch
detached-head state
HEAD
TREE
working-tree state
tracked modifications
untracked-file presence
protected path existence
protected HEAD blob identities
```

## 11. Worktree classification

At minimum:

```text
CLEAN
DIRTY
UNKNOWN
```

Detached HEAD must be explicit and must not masquerade as a branch.

## 12. Fail-closed statuses

At least:

```text
PASS
BLOCKED_REPOSITORY_MISMATCH
BLOCKED_REMOTE_MISMATCH
BLOCKED_BRANCH_MISMATCH
BLOCKED_DETACHED_HEAD
BLOCKED_HEAD_DRIFT
BLOCKED_TREE_DRIFT
BLOCKED_PROTECTED_PATH_MISSING
BLOCKED_PROTECTED_BLOB_DRIFT
DIRTY_WORKTREE
UNKNOWN_LOCAL_STATE
INVALID_EXPECTED_BINDING
VERIFICATION_ERROR
```

## 13. Protected blob semantics

For each protected path:

```text
expected blob
observed HEAD blob
verification status
```

Mismatch must be surfaced, never repaired.

## 14. P22-01 compatibility

P22-02 output must provide a snapshot directly consumable by:

`tools/p22_01_pure_state_projector.py`

At minimum:

```text
repository
branch
head
tree
working_tree_state
protected_artifacts
```

Integration must demonstrate:

```text
P22-02 VERIFIED SNAPSHOT
        ↓
P22-01 PURE PROJECTOR
        ↓
DETERMINISTIC DERIVED ACTIVE STATE
```

## 15. Minimum frozen test families

```text
P01 exact repository accepted
P02 wrong repository blocked
P03 expected origin accepted
P04 wrong origin blocked
P05 correct branch accepted
P06 wrong branch blocked
P07 detached HEAD blocked when branch required
P08 exact HEAD accepted
P09 stale/wrong HEAD blocked
P10 exact TREE accepted
P11 wrong TREE blocked
P12 CLEAN worktree classified correctly
P13 tracked modification produces DIRTY
P14 untracked file produces DIRTY
P15 protected path exact blob passes
P16 protected blob mismatch blocks
P17 missing protected path blocks
P18 malformed expected SHA/binding fails closed
P19 subprocess execution uses fixed read-only allowlist
P20 no shell execution surface
P21 no network/fetch/pull surface
P22 no repository mutation command surface
P23 output deterministic and machine-readable
P24 P22-02 snapshot accepted by P22-01
P25 input expectations not silently modified
P26 verification failure cannot self-repair
P27 E1/E1-TD protected artifacts observational only
P28 TD-03B event budget cannot be consumed
```

## 16. Real qualification requirement

Synthetic tests alone are insufficient.

Final qualification must execute against:

```text
A FRESH CLEAN CLONE
OF
integration/system-v1
```

and verify actual origin, branch, HEAD, TREE, worktree and protected blobs against independently obtained GitHub canonical values.

## 17. Test side effects

Temporary repositories outside the canonical repository are permitted as non-canonical test fixtures.

Final qualification should use:

```text
PYTHONDONTWRITEBYTECODE=1
```

## 18. Protected Phase 22 boundaries

P22-02 must not modify P22-01 authority, contract, breaker, runtime, qualification, Phase 22 contract or Phase 22 adoption.

## 19. E1 / E1-TD hard isolation

P22-02 may not modify or execute E1/E1-TD research paths.

```text
TD03B_EVENT_BUDGET MUST REMAIN 0 / 1
```

No source acquisition, H1 construction, signal/trade generation, PnL, backtest or tail analysis is authorized.

## 20. Repository write authority

Writes are authorized only for the listed P22-02 artifacts on `integration/system-v1`.

No force push, merge, rebase, tag, release, branch deletion, history rewrite or unrelated branch movement.

Every write requires fresh repository/branch/HEAD verification.

Unexpected concurrent HEAD movement requires STOP.

## 21. Correction authority

After RED, runtime-only mechanical corrections are authorized only when contract and breaker remain unchanged and failure directly identifies a runtime defect.

Otherwise STOP.

## 22. Completion criteria

P22-02 PASS requires:

```text
authority persisted
contract persisted before runtime
breaker persisted before runtime
real RED observed
RED evidence persisted
minimal runtime persisted
frozen breaker PASS
adversarial cases PASS
P22-01 compatibility PASS
fresh-clone real qualification PASS
GitHub/local HEAD comparison PASS
GitHub/local TREE comparison PASS
protected blobs PASS
persisted-HEAD re-break PASS
authorized-path audit PASS
E1/E1-TD identities unchanged
TD03B event budget still 0 / 1
qualification evidence persisted
```

## 23. Post-cycle STOP

After qualification persistence:

```text
STOP = TRUE
P22_03 = NOT_AUTHORIZED
```

## 24. Authority summary

```text
P22_02_CONTRACT_PREREGISTRATION = AUTHORIZED
P22_02_BREAKER_PREREGISTRATION = AUTHORIZED
P22_02_TEST_FIRST_RED = AUTHORIZED
P22_02_MINIMAL_IMPLEMENTATION = AUTHORIZED
P22_02_IMPLEMENTATION_ONLY_MECHANICAL_CORRECTIONS = AUTHORIZED
P22_02_ADVERSARIAL_TESTING = AUTHORIZED
P22_01_INTEGRATION_TEST = AUTHORIZED
P22_02_REAL_READ_ONLY_FRESH_CLONE_QUALIFICATION = AUTHORIZED
P22_02_PERSISTED_HEAD_REBREAK = AUTHORIZED
P22_02_EVIDENCE_PERSISTENCE = AUTHORIZED

ARBITRARY_COMMAND_EXECUTION = NOT_AUTHORIZED
NETWORK_GIT_OPERATIONS = NOT_AUTHORIZED
AUTOMATIC_REPAIR = NOT_AUTHORIZED
MUTATION_OUTSIDE_P22_02_PATHS = NOT_AUTHORIZED
E1_OR_E1_TD_MUTATION = NOT_AUTHORIZED
TD03B_EVENT_CONSUMPTION = NOT_AUTHORIZED
STRATEGY_PERFORMANCE_ACCESS = NOT_AUTHORIZED
P22_03 = NOT_AUTHORIZED

FINAL_REQUIRED_STATE = STOP
```
