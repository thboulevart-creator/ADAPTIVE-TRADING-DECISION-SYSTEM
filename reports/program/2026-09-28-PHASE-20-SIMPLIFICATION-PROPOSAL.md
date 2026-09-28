# PHASE 20 — SIMPLIFICATION_PROPOSAL

Date: 2026-09-28  
Base HEAD: `f3e02454f4a3ea5bb133586141fe9d28656b348d`

## Status

**PROPOSAL ONLY — NO CHANGE APPLIED.**

The only allowed proposal labels are:

`KEEP` · `SIMPLIFY` · `MERGE` · `DEFER` · `REMOVE_CANDIDATE` · `UNKNOWN`

Phase 21 human adjudication is required before any methodological change.

## Proposal matrix

| SP | Control / workflow | Proposal | Evidence / rationale | Main risk if accepted incorrectly |
|---|---|---|---|---|
| SP-01 | GitHub as canonical source of truth | KEEP | Repository safety rule; prevents conversational-state drift | Wrong repository/state acted upon |
| SP-02 | Repo + branch + HEAD + TREE + protected-blob checks as separate manual steps | MERGE | Same identity surface repeatedly enumerated; E1-07 already models a canonical preflight | Shared verifier could omit a currently distinct check |
| SP-03 | Contract freeze before candidate implementation | KEEP | Prevents moving target after observing behavior | Post-hoc requirements |
| SP-04 | Frozen breaker/test expectations | KEEP | Central to test-first falsifiability | Tests adapted to implementation |
| SP-05 | Test-first RED | KEEP | E1-04→E1-07 shows clean separation between preregistration and implementation | False confidence from post-hoc tests |
| SP-06 | Exact-byte materialization + persisted-HEAD re-break tooling | MERGE | Different semantics but same harness can perform both | Merge must still prove bytes and behavior separately |
| SP-07 | Detailed qualification report | KEEP | Durable evidence package | Loss of audit detail |
| SP-08 | Recovery checkpoint repeating full report prose | SIMPLIFY | Strong content duplication; checkpoint only needs state, hashes, frontier and pointers | Over-simplification could impair recovery |
| SP-09 | Human approval for each mechanical correction inside a frozen authorized cycle | REMOVE_CANDIDATE | Accelerated mode already preserves hard STOPs while removing intermediate approvals | Agent could misclassify architectural change as mechanical |
| SP-10 | Macro authorization per governed control + mandatory STOP boundaries | KEEP | Demonstrated reduction in coordination overhead without weakening frozen surfaces | Too-broad authorization if boundaries are vague |
| SP-11 | OOS/window freeze | KEEP | Direct protection against result-driven window movement | Selection bias |
| SP-12 | Exact raw/H1 data identity and deterministic rebuild | KEEP | E1-03 protects experiment input truth | Dataset substitution / irreproducibility |
| SP-13 | E1-04 execution/cost semantics | KEEP | Directly changes observed result if wrong | Look-ahead / unrealistic execution |
| SP-14 | E1-06 independent reference parity | KEEP | Distinct independent implementation check | Shared bug could go undetected without it |
| SP-15 | E1-07 preflight + general repository identity verification implementation | MERGE | Overlapping identity plumbing; scopes remain distinct | Runtime-specific requirements could disappear |
| SP-16 | Repeated forbidden-claim lists copied across E1 artifacts | SIMPLIFY | Same authority boundaries recur in multiple documents | Central registry drift could weaken local explicitness |
| SP-17 | A0 V0.3 coverage-gap expansion before first E1 | DEFER | Freeze package explicitly defers it; no runtime defect established | A hidden A0 gap could matter if future evidence shows dependency |
| SP-18 | Real C01 confirmation before exploratory E1 | DEFER | Different confirmatory stage | Premature confirmation semantics |
| SP-19 | Obsidian work on the current backtest critical path | DEFER | Not present on current branch; Phase 26 purpose is later knowledge projection | Knowledge maintenance could lag |
| SP-20 | Project Control Plane before Phase 21 | DEFER | Plan explicitly places it after human methodology decision | Automating a method that is still changing |
| SP-21 | Universal multi-project control plane / “Agent Maître” now | DEFER | No ATDS pilot evidence yet | Premature abstraction |
| SP-22 | E1-08 explicit one-shot human authority | KEEP | Only remaining boundary between qualified tooling and real E1 execution | Unauthorized experiment / authority creep |
| SP-23 | Three-way external counter-expertise for every routine mechanical action | REMOVE_CANDIDATE | Normative document itself limits it to genuine consequential decisions | Removing it from genuine normative choices would weaken governance |
| SP-24 | Three-way counter-expertise for genuine human normative decisions | KEEP | Explicit validated governance rule | Human could be forced to decide without adversarial analysis |
| SP-25 | Full historical checkpoint reread on every small action | SIMPLIFY | Large accumulated checkpoint creates recurring context cost | Too-short state could omit an active invariant |
| SP-26 | Machine-readable compact active-state manifest | MERGE | Can unify frontier, protected identities, authority, blockers and current HEAD | New manifest must remain derived from canonical Git state |
| SP-27 | All historical non-E1 controls as permanent pre-backtest gates | UNKNOWN | No empirical counterfactual yet proves which old layers add marginal protection after E1 readiness | Premature deletion could remove a hidden dependency |

## Proposed Phase 21 decision set

The highest-leverage candidates for human adjudication are:

```text
SP-02  MERGE identity verification plumbing
SP-06  MERGE exact-byte + persisted-head qualification harness
SP-08  SIMPLIFY checkpoint duplication
SP-09  REMOVE_CANDIDATE repeated mechanical micro-approvals
SP-16  SIMPLIFY duplicated authority declarations
SP-25  SIMPLIFY full historical checkpoint rereads
SP-26  MERGE into compact machine-readable active-state manifest
```

The proposal deliberately does **not** recommend weakening:

```text
OOS freeze
data identity
execution/cost semantics
test-first RED
frozen breakers
independent parity
persisted-head verification
E1-08 human authority
```

## Decision rule

No row changes method, code, contracts, authority or workflow until Phase 21 human adjudication.
