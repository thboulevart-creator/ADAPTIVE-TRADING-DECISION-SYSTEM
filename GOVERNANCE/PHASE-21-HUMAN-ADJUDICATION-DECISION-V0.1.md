# PHASE 21 — HUMAN ADJUDICATION DECISION V0.1

Date: 2026-09-28

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`  
Decision base HEAD: `2e2233a274712ed9ee85e09f787b1db1dea4c073`  
Decision base TREE: `04b15f734aa56c336906df0456deb95e9c7d150d`

## 1. Status and authority

```text
PHASE_21 = HUMAN_ADOPTED
METHOD_DIRECTION = ADOPTED
SIMPLIFICATION_IMPLEMENTATION = NOT_AUTHORIZED
E1_01_TO_E1_07_MUTATION = NOT_AUTHORIZED
REAL_E1_RUN = NOT_AUTHORIZED
E1_08 = NOT_OPENED
PROJECT_CONTROL_PLANE = NOT_AUTHORIZED
PHASE_22_PLUS = CLOSED
```

The human decision is:

> Adopt the target architecture and simplification rules now, freeze structural implementation until after the first real E1, add to E1-08 only the protections directly necessary to the irreversibility of OOS exposure, execute the first E1 only after a separate E1-08 authorization, persist the result, STOP, and only then begin reducing human middleware using the real experiment as evidence.

This document records the decision. It does not implement the simplifications.

---

## 2. Decision objective

Primary optimization objective:

```text
maximize reliable experimental knowledge
----------------------------------------
human time
```

subject to preserving the protections that materially defend:

- scientific validity;
- provenance;
- reproducibility;
- falsifiability;
- auditability;
- error confinement;
- explicit authority boundaries.

The adopted direction is:

```text
AUTOMATE WORK
DO NOT SILENTLY AUTOMATE AUTHORITY
```

Human intervention should progressively decrease only where the replacement control is mechanically decidable, independently checkable, or otherwise shown not to weaken the protected property.

---

## 3. Evidence and counter-expertise considered

Repository-native evidence considered includes:

- Phase 20 CONTROL_INVENTORY;
- Phase 20 REDUNDANCY_MAP;
- Phase 20 COST_MAP;
- Phase 20 BACKTEST_BLOCKER_MAP;
- Phase 20 SIMPLIFICATION_PROPOSAL;
- E1-01/E1-02 freeze package;
- E1-03 real AP0 → H1 qualification;
- E1-04 execution/cost qualification;
- E1-05 corrected runner qualification;
- E1-06 adversarial/reference parity qualification;
- E1-07 preflight/reproducibility/trace qualification;
- Repository Safety Rules;
- Decision Support and Human Boundary.

Independent counter-expertise presented to the human and compared before this decision:

1. **Grok independent review**
   - favored hybrid architecture;
   - identified mechanical/documentary over-governance;
   - supported derived state, bounded automation and append-only experimental memory;
   - warned against manifest authority, memory contamination and authority laundering.

2. **Claude independent blind review**
   - emphasized correlated-author / correlated-assumption risk;
   - identified the AP0 real-artifact case as evidence that independent-looking synthetic controls can share one wrong assumption;
   - distinguished implementation independence from assumption independence;
   - argued that OOS exposure is irreversible while infrastructure refactoring is reversible;
   - recommended exposure tracking and delaying structural refactor until after first E1.

3. **Independent internal analysis**
   - compared both counter-expert reviews against current GitHub evidence;
   - verified material repository claims before recommending adoption.

The two external reviews are decision inputs, not normative authorities.

---

## 4. Adopted Phase 21 classifications

| SP | Decision |
|---|---|
| SP-01 | KEEP |
| SP-02 | MERGE |
| SP-03 | KEEP |
| SP-04 | KEEP |
| SP-05 | KEEP |
| SP-06 | MERGE |
| SP-07 | KEEP |
| SP-08 | SIMPLIFY |
| SP-09 | SIMPLIFY |
| SP-10 | KEEP |
| SP-11 | KEEP |
| SP-12 | KEEP |
| SP-13 | KEEP |
| SP-14 | KEEP |
| SP-15 | MERGE |
| SP-16 | SIMPLIFY |
| SP-17 | DEFER |
| SP-18 | DEFER |
| SP-19 | DEFER |
| SP-20 | DEFER |
| SP-21 | DEFER |
| SP-22 | KEEP |
| SP-23 | REMOVE_CANDIDATE |
| SP-24 | KEEP |
| SP-25 | SIMPLIFY |
| SP-26 | SIMPLIFY |
| SP-27 | UNKNOWN |

These labels are methodological decisions. They are not executable permission to mutate the corresponding mechanisms before the sequencing conditions below are met.

---

## 5. Material changes from the Phase 20 proposal

### 5.1 SP-09 — mechanical micro-approvals

Phase 20 candidate:

`REMOVE_CANDIDATE`

Adopted Phase 21 decision:

`SIMPLIFY`

Reason:

A small diff, unchanged contract and unchanged frozen tests do not prove absence of semantic change.

The future target is not:

```text
agent declares "mechanical"
```

It is:

```text
mechanical classification is calculated
from protected paths + frozen contracts + frozen tests
+ behavioral differential + authority boundaries
```

Any semantic/authority ambiguity must fail closed to a human STOP.

### 5.2 SP-26 — active-state manifest

Phase 20 candidate:

`MERGE into compact machine-readable active-state manifest`

Adopted Phase 21 decision:

`SIMPLIFY`

Reason:

Current state should be **derived**, not trusted as an independent stored truth.

Target model:

```text
CANONICAL REPOSITORY / DECISIONS / EVIDENCE
                ↓
PURE STATE PROJECTOR
                ↓
ACTIVE STATE
```

A stored manifest may exist only as a discardable cache verified at read time.

```text
CACHE != AUTHORITY
```

---

## 6. Two new adopted principles

### P21-R1 — independence distinction

```text
INDEPENDENCE_OF_IMPLEMENTATION
!=
INDEPENDENCE_OF_ASSUMPTION
```

Separate code paths written under one shared interpretation may catch implementation defects while still sharing the same conceptual error.

Future qualification design must distinguish:

- implementation independence;
- data/source independence;
- assumption/specification independence;
- authority independence.

Where materially necessary, independent evidence should come from a source not generated from the same mistaken assumption: real artifacts, isolated-context oracle, external specification, or human oracle.

### P21-R2 — experimental memory must track exposure

```text
PERSISTENT_EXPERIMENTAL_MEMORY
MUST_TRACK_DATA_EXPOSURE
NOT_ONLY_RESULTS
```

A non-normative memory can still contaminate later experiments if it exposes prior OOS outcomes during hypothesis formation.

Future memory design must preserve at least:

- hypothesis identity;
- experiment identity;
- dataset identity;
- window identity;
- first performance exposure;
- hypothesis-family exposure;
- whether result information informed later revisions;
- domain of validity;
- epistemic status;
- supersession/refutation history.

A dataset/window may not be represented as clean independent OOS merely because its files are unchanged.

---

## 7. Sequencing decision

The adopted sequence is:

```text
PHASE 21 DECISION
        ↓
DO NOT REFACTOR E1-01 → E1-07
        ↓
DEFINE E1-08 PRECISELY
        ↓
E1-08 SEPARATE HUMAN ONE-SHOT AUTHORIZATION
        ↓
FIRST REAL E1
        ↓
PERSIST RESULT + TRACE
        ↓
HARD STOP
        ↓
ONLY THEN:
implement selected simplifications
and begin Phase 22+ work
```

Rationale:

- infrastructure refactoring is reversible;
- first observation of the frozen OOS is not;
- therefore the next high-value action is the experiment, not rebuilding the already-qualified pre-E1 pipeline.

---

## 8. E1-08 minimum protection direction

Phase 21 adopts that the future E1-08 definition should add only protections directly tied to the irreversible real run.

Candidate minimum set:

```text
1. OOS / prior-exposure declaration
2. input identity verification at actual consumption
3. explicit one-shot human run authority
4. exact E1-01 → E1-07 protected identities
5. mandatory result/trace envelope
6. no automatic rerun
7. no parameter or scope modification
8. STOP after result persistence
```

These items define the direction for E1-08.

They do **not** authorize E1-08 implementation or the real E1 run by this Phase 21 decision.

No new E1-09/E1-10/... blocker is created by this decision.

Any new proposed pre-E1 blocker must satisfy the adopted necessity rule and demonstrate the concrete failure that would materially invalidate the next E1 result.

---

## 9. Controls explicitly retained

The decision does not weaken:

- E1 scope freeze;
- frozen OOS/window;
- exact raw and H1 data identity;
- execution semantics;
- cost semantics;
- test-first RED;
- frozen breakers;
- adversarial testing;
- independent reference parity;
- exact-byte identity;
- persisted-HEAD re-break;
- preflight/reproducibility/trace;
- explicit human authority at consequential boundaries.

---

## 10. Deferred implementation targets

The following are directionally adopted but implementation is deferred until after the first E1 result:

- common identity verifier;
- common exact-byte / persisted-head qualification harness;
- compact derived recovery state;
- simplified authority/forbidden-use representation;
- calculated mechanical-vs-semantic classifier;
- replacement of full historical rereads;
- persistent experimental memory beyond the minimum E1 exposure record;
- Project Control Plane V0;
- Obsidian knowledge projection;
- multi-project central coordination.

---

## 11. Rejected alternatives

### Immediate structural refactor before E1

Rejected for now.

Reason:

It changes a qualified pipeline immediately before the first irreversible OOS observation and provides most of its benefit only on subsequent runs.

### Indefinite preservation of current manual middleware

Rejected as the long-term method.

Reason:

Phase 20 and both counter-expert reviews show recurring human cost from duplicated identity work, checkpoints, prose and mechanical approvals.

### New unbounded pre-E1 qualification layers

Rejected unless separately justified by the necessity rule.

Reason:

The program must not continually create new blockers without demonstrating that they protect the next result from a concrete material failure.

---

## 12. Residual uncertainty

The following remain explicit:

- Git history does not currently provide cryptographically distinct provenance between a human decision and an agent-written persistence of that decision.
- Separate implementations may still share one conceptual error.
- Exact hash-on-consumption behavior for the future real E1 must be verified in the E1-08 definition.
- The exact exposure-ledger representation is not yet frozen.
- The future mechanical/semantic classifier does not yet exist.
- No claim is made that the present governance is optimal for all future experiments.

These uncertainties do not themselves authorize additional pre-E1 phases.

---

## 13. Current authority state

```text
PHASE_20 = CLOSED
PHASE_21 = HUMAN_ADOPTED

E1-01 = PASS
E1-02 = PASS
E1-03 = PASS
E1-04 = PASS
E1-05 = PASS
E1-06 = PASS
E1-07 = PASS

E1-08 = NOT_OPENED
E1_READINESS = NOT_READY

REAL_E1_RUN = NOT_AUTHORIZED
REAL_DATA_PERFORMANCE_INTERPRETATION = NOT_AUTHORIZED
MT5 = CLOSED
PAPER = CLOSED
BROKER = CLOSED
LIVE = CLOSED
CAPITAL = CLOSED

SIMPLIFICATION_IMPLEMENTATION = NOT_AUTHORIZED
PHASE_22_PLUS = CLOSED
```

---

## 14. Next governed boundary

```text
E1-08
—
EXACT ONE-SHOT REAL E1 RUN AUTHORIZATION DEFINITION
```

The next step is to define that boundary precisely against the existing E1-01→E1-07 evidence.

No real E1 execution is authorized by this document.
