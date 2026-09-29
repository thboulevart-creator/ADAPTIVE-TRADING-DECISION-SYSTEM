# P22-01 — PURE STATE PROJECTOR — GOVERNED ACCELERATED AUTHORITY V0.1

Date: 2026-09-29

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

## 1. Human authorization

The human explicitly stated:

```text
Ok créons la meilleure autorisation possible et c'est parti
```

This record interprets that instruction as a bounded macro-authorization for the complete P22-01 governed engineering cycle described below.

It does not authorize Phase 22 as a whole and does not transfer normative authority to the agent.

## 2. Authority creation base

Immediately before persistence of this authority, GitHub was independently revalidated as:

```text
repository =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

branch =
integration/system-v1

HEAD =
15980d6c39f85d8354562fcfcb110c3e61ff7b14

TREE =
93875984f5a6893edaaea467c4344a8547517fe9
```

Protected Phase 22 bindings:

```text
PHASE_22_CONTRACT_BLOB =
afc519d3e937dfcde2ce1e0bf7d2646dd010a8ce

PHASE_22_ADOPTION_BLOB =
90f6405435c62869f220ebe8783fc138d133ee93
```

Protected E1-TD binding:

```text
E1_TD_03B_AUTHORITY_BLOB =
7ea58d02387d67e7360356a10c0eaed441d0b2f4
```

Any mismatch before the P22-01 cycle begins must STOP.

## 3. Authorized objective

The only engineering objective authorized by this record is:

```text
P22-01
PURE STATE PROJECTOR
```

The projector must derive active project state from canonical repository evidence without creating a second independent authority.

Invariant:

```text
ACTIVE STATE = DERIVED
ACTIVE STATE != AUTHORITY
CACHE != AUTHORITY
```

## 4. Authorized governed cycle

Within this single P22-01 macro-authorization, the following sequence is authorized:

```text
1. preregister P22-01 executable contract and frozen acceptance properties
2. preregister a frozen P22-01 breaker/test surface
3. execute and persist TEST-FIRST RED evidence
4. implement the minimum P22-01 projector necessary to satisfy the frozen contract
5. run the frozen breaker
6. apply implementation-only mechanical corrections directly demonstrated by frozen-test failures
7. repeat the frozen breaker after such corrections
8. verify protected Phase 22 and E1-TD identities remain unchanged
9. perform exact persisted-HEAD re-break/qualification
10. persist the P22-01 qualification/evidence report
11. STOP
```

No intermediate human micro-approval is required inside this exact cycle when all frozen boundaries continue to pass.

## 5. Frozen correction rule

After the first RED execution, the P22-01 contract and breaker expectations are frozen.

Authorized corrections after RED are limited to the implementation target and mechanically necessary execution/qualification plumbing explicitly listed in this authority.

If a failing test suggests that the contract or breaker itself is wrong, incomplete, contradictory or semantically ambiguous:

```text
STOP_FOR_HUMAN_ADJUDICATION
```

The agent must not weaken, rewrite or delete a failing expectation to manufacture PASS.

## 6. Authorized repository paths

P22-01 may create or modify only the following Phase-22-specific paths:

```text
GOVERNANCE/P22-01-PURE-STATE-PROJECTOR-CONTRACT-V0.1.json

breakers/p22_01_pure_state_projector_red_breaker.py

tools/p22_01_pure_state_projector.py

.github/workflows/p22-01-pure-state-projector-qualification.yml

reports/program/2026-09-29-P22-01-PURE-STATE-PROJECTOR-TEST-FIRST-RED.md

reports/program/2026-09-29-P22-01-PURE-STATE-PROJECTOR-QUALIFICATION.md
```

This authority record itself is additionally authorized for persistence at:

```text
GOVERNANCE/P22-01-PURE-STATE-PROJECTOR-GOVERNED-ACCELERATED-AUTHORITY-V0.1.md
```

No other repository path may be mutated under this authority.

## 7. Local execution workspace

A clean disposable or dedicated local workspace derived from the exact authorized GitHub branch is permitted for:

```text
test execution
RED evidence collection
candidate verification
re-break
diagnostics
```

An existing local checkout with a detached HEAD, stale branch, dirty worktree or ambiguous provenance must not be repurposed silently.

Local temporary files outside the canonical repository may be used only for test execution and evidence capture and are not canonical authority.

## 8. Minimum P22-01 properties

The frozen contract/breaker must prove at least:

```text
P01 deterministic projection from identical canonical inputs
P02 canonical repository identity is explicit
P03 branch / HEAD / TREE are represented explicitly
P04 unavailable facts remain UNKNOWN and are never upgraded to PASS/CLEAN/AUTHORIZED
P05 working-tree state distinguishes CLEAN / DIRTY / UNKNOWN
P06 protected artifact identities are represented without silently repairing mismatch
P07 stale recovery/checkpoint state can be detected against canonical state
P08 cached/projected state is non-authoritative and reconstructible
P09 projector has no repository mutation capability
P10 E1/E1-TD protected research state is surfaced without being consumed or modified
P11 malformed or incomplete canonical input fails closed
P12 output is deterministic and machine-readable
```

## 9. Explicit prohibitions

This authority does not permit:

```text
MOMENTUM_V1 modification
E1 rerun
new backtest
PnL computation
new OOS inspection
tail-dependence computation
TD-03B event consumption
TD-03B source acquisition
TD window or threshold change
dataset substitution
strategy research
strategy modification
A0/A1/A2 reopening
Decision/ACTION reopening
Obsidian mutation
multi-project control-plane work
Agent Maître work
deployment
external action
file deletion
branch deletion
merge
force push
history rewrite
```

## 10. Commit/push authority

Repository commits required to persist the explicitly authorized P22-01 paths are authorized on:

```text
integration/system-v1
```

only.

This does not authorize merges, branch movement unrelated to ordinary linear P22-01 commits, force pushes, tags or releases.

Every write must be preceded by a fresh repository/branch/HEAD check.

## 11. Failure and STOP conditions

Immediate STOP is mandatory on any of:

```text
repository mismatch
branch mismatch
unexpected concurrent HEAD movement
protected Phase 22 blob drift
protected E1-TD blob drift
mutation outside authorized paths
semantic ambiguity
need to alter frozen contract/breaker after RED
need to access strategy performance
need to consume TD-03B
non-mechanical scope expansion
evidence contradiction
```

## 12. Completion condition

P22-01 may be declared PASS only if:

```text
contract persisted
breaker persisted and frozen
RED observed and persisted
minimal implementation persisted
frozen breaker PASS
persisted-HEAD re-break PASS
protected identities unchanged
qualification evidence persisted
no unauthorized path mutation
```

Otherwise P22-01 remains FAIL or BLOCKED with the reason persisted.

## 13. Post-cycle authority

After the P22-01 qualification report is persisted:

```text
STOP = TRUE
```

P22-02 is not implicitly authorized.

A separate human decision is required before opening the Identity / State Verifier boundary.
