# PHASE 20 — BACKTEST_BLOCKER_MAP

Date: 2026-09-28  
Base HEAD: `f3e02454f4a3ea5bb133586141fe9d28656b348d`

## Governing rule

A blocker belongs on the pre-E1 critical path only if failure of that control could materially invalidate the first E1 result, its interpretation, its reproducibility, or the authority to execute it.

## Active readiness map

| E1 control | Protected failure | Evidence | State | Blocks real E1 now? |
|---|---|---|---|---|
| E1-01 — Scope Freeze | post-result strategy/scope mutation | `E1-PRE-IMPLEMENTATION-FREEZE-PACKAGE-V0.md` | PASS | No |
| E1-02 — Window/OOS Freeze | cherry-picking / OOS movement | same freeze package + checkpoint | PASS | No |
| E1-03 — Exact gap-aware H1 identity | wrong/changed data, continuity ambiguity, irreproducible H1 | real AP0→H1 qualification | PASS | No |
| E1-04 — Execution/Cost Model | look-ahead fills, MID execution, BID/ASK errors, hidden cost assumptions | 22/22 frozen tests | PASS | No |
| E1-05 — Minimal Momentum Runner | orchestration/order/continuity errors | corrected 33/33 frozen tests | PASS | No |
| E1-06 — Adversarial + Independent Reference Parity | shared runner/accounting error; nondeterminism | 22/22 parity/adversarial tests | PASS | No |
| E1-07 — Exact Preflight/Reproducibility/Trace | wrong HEAD/TREE/data/runtime/environment/result trace | 30/30 frozen tests | PASS | No |
| **E1-08 — Explicit Human Run Authorization** | real experiment executed without bounded human authority | readiness state explicitly says NOT_OPENED | **NOT_OPENED** | **YES — sole remaining E1 blocker** |

## Readiness state

```text
E1-01 = PASS
E1-02 = PASS
E1-03 = PASS
E1-04 = PASS
E1-05 = PASS
E1-06 = PASS
E1-07 = PASS
E1-08 = NOT_OPENED

E1_READINESS = NOT_READY
```

## Explicit non-blockers for the first E1 run

These items remain open or future work, but current repository evidence does not place them on the E1 critical path:

| Item | Verified repository state | Why not current E1 blocker |
|---|---|---|
| A0 V0.3 remaining coverage gaps | `A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`; runtime defect not established | freeze package explicitly defers coverage-gap expansion post-E1 |
| A1 / A2 / DecisionPolicy / Decision / ACTION | closed | downstream architecture, not required to observe first E1 |
| C01 real confirmation | closed | confirmatory stage is distinct from exploratory E1 |
| MT5 / paper / broker / live / capital | closed | execution/promotion authority beyond offline exploratory result |
| Obsidian projection | no active surface on current branch | knowledge layer; not required for experimental validity |
| Project Control Plane V0 | future Phase 22+ | workflow automation, not prerequisite to E1 validity |
| Universal “Agent Maître” | future Phase 27 | generalization only after ATDS pilot evidence |

## Necessity test for any proposed new blocker

Before adding a ninth pre-E1 blocker, the proposer must identify:

1. the exact failure that can still occur after E1-01→E1-07;
2. why that failure materially invalidates the next E1 result;
3. why an existing control does not already reject it;
4. an executable or otherwise auditable falsification test;
5. the cost of delaying E1.

Absent those five elements, the candidate belongs outside the critical path.

## Current conclusion

```text
TECHNICAL READINESS CONTROLS CLOSED = 7 / 7
HUMAN RUN-AUTHORITY GATE = 1 OPEN
SOLE ACTIVE BLOCKER = E1-08
```
