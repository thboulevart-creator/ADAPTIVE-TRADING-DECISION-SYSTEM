# PHASE 20 — CONTROL_INVENTORY

Date: 2026-09-28  
Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`  
Audit base HEAD: `f3e02454f4a3ea5bb133586141fe9d28656b348d`  
Audit base TREE: `c6aeb0c2b881cfe08d22873b51973b88127919ca`

## Status discipline

This inventory is a **control-family inventory**, not a claim that every historical file in the repository is a separate active control.

Evidence labels:

- `VERIFIED` — directly supported by current GitHub artifacts or persisted execution evidence.
- `DERIVED` — audit consequence derived from verified controls.
- `UNKNOWN` — no persisted evidence sufficient to quantify or decide.

No simplification is applied by this document.

## Inventory

| ID | Control family | Risk / failure prevented | Current evidence | Current status | Critical-path relation |
|---|---|---|---|---|---|
| CI-01 | Repository identity verification | Acting on wrong repository | `GOVERNANCE/REPOSITORY-SAFETY-RULES.md` | VERIFIED / ACTIVE | Mandatory before mutation |
| CI-02 | Branch / base / HEAD / TREE verification | Stale or wrong lineage | Repository safety rules + E1-07 bindings | VERIFIED / ACTIVE | Mandatory |
| CI-03 | Protected Git blob identity verification | Silent mutation of qualified artifacts | E1-03→E1-07 reports/checkpoint | VERIFIED / ACTIVE | Mandatory |
| CI-04 | Contract freeze before implementation | Moving requirements after observing behavior | E1-03→E1-07 contracts | VERIFIED / ACTIVE | Mandatory |
| CI-05 | Frozen breaker/test surface | Test expectation drift / self-fulfilling PASS | E1-04→E1-07 breakers | VERIFIED / ACTIVE | Mandatory |
| CI-06 | Test-first RED | Candidate implemented before falsifiable test | E1-04, E1-05, E1-06, E1-07 RED evidence | VERIFIED / ACTIVE | Mandatory |
| CI-07 | Minimal implementation scope | Scope creep during correction | E1-04/E1-05/E1-07 reports | VERIFIED / ACTIVE | Mandatory |
| CI-08 | Adversarial breaker replay | Nominal-only correctness | E1-04→E1-07 qualification reports | VERIFIED / ACTIVE | Mandatory |
| CI-09 | Exact-byte materialization | Running different bytes than persisted bytes | E1-06/E1-07 reports | VERIFIED / ACTIVE | Mandatory for exact qualification |
| CI-10 | Persisted-HEAD re-break | Local candidate differs from canonical state | E1-06/E1-07 reports | VERIFIED / ACTIVE | Mandatory |
| CI-11 | Evidence report persistence | PASS without auditable evidence package | `reports/program/*E1*` | VERIFIED / ACTIVE | Supporting control |
| CI-12 | Recovery checkpoint persistence | Loss of frontier/state across sessions | `04-REFERENCE/RECOVERY-CHECKPOINT.md` | VERIFIED / ACTIVE | Supporting control |
| CI-13 | Human normative-decision boundary | Agent silently creates policy | `GOVERNANCE/DECISION-SUPPORT-AND-HUMAN-BOUNDARY.md` | VERIFIED / ACTIVE | Mandatory at normative choices |
| CI-14 | Accelerated governed macro authorization | Excessive human micro-approval while retaining hard STOPs | checkpoint §308 | VERIFIED / ACTIVE | Human-cost reduction control |
| CI-15 | E1-01 scope freeze | Strategy/scope changes after seeing results | `E1-PRE-IMPLEMENTATION-FREEZE-PACKAGE-V0.md` | VERIFIED / PASS | Backtest blocker closed |
| CI-16 | E1-02 window / OOS freeze | Temporal cherry-picking / post-result OOS movement | freeze package | VERIFIED / PASS | Backtest blocker closed |
| CI-17 | E1-03 exact gap-aware H1 identity | Dataset substitution, discontinuity ambiguity, non-reproducible H1 | E1-03 real qualification | VERIFIED / PASS | Backtest blocker closed |
| CI-18 | E1-04 execution/cost model | Same-bar execution, MID-as-fill, BID/ASK errors, hidden cost assumptions | E1-04 qualification | VERIFIED / PASS | Backtest blocker closed |
| CI-19 | E1-05 minimal Momentum runner | Orchestration/order/continuity errors | E1-05 qualification | VERIFIED / PASS | Backtest blocker closed |
| CI-20 | E1-06 adversarial + independent reference parity | Shared implementation error, PnL accounting divergence | E1-06 qualification | VERIFIED / PASS | Backtest blocker closed |
| CI-21 | E1-07 exact preflight / reproducibility / trace | Wrong HEAD/data/runner/environment/result trace at execution | E1-07 qualification | VERIFIED / PASS | Backtest blocker closed |
| CI-22 | E1-08 explicit one-shot human run authority | Executing real E1 without explicit bounded authorization | current readiness state | VERIFIED / NOT_OPENED | **Only remaining E1 blocker** |
| CI-23 | A0 V0.3 coverage-gap expansion | Missing executable evidence on A0 semantic surface | A0 V0.3 coverage review | VERIFIED / INCOMPLETE | Explicitly deferred post-E1 |
| CI-24 | C01 confirmatory path | Premature confirmatory interpretation | protected C01 state / A0 review | VERIFIED / CLOSED | Not current E1 blocker |
| CI-25 | Paper / broker / MT5 / live / capital gates | Escalation from research evidence to execution authority | freeze package + E1 reports | VERIFIED / CLOSED | Outside current backtest readiness |
| CI-26 | Obsidian knowledge projection | Manual knowledge drift / projection convenience | no Obsidian surface on current `integration/system-v1` tree | VERIFIED ABSENCE / DEFERRED | Not a backtest blocker |
| CI-27 | Phase 19 scope-freeze rule | New ideas recolonize critical path | human-adopted audit plan + E1 critical-path bridge | DERIVED / ACTIVE | Protects path to first result |
| CI-28 | POST_BACKTEST_BACKLOG routing | Non-critical work delays first result | human-adopted audit plan; no canonical backlog artifact found | UNKNOWN IMPLEMENTATION | Should not block E1 |
| CI-29 | Independent counter-expertise for genuine normative decisions | Human forced to guess technical policy | Decision Support and Human Boundary | VERIFIED / ACTIVE | Conditional, not every routine step |
| CI-30 | Qualification environment identity | Ambient runtime drift | E1-07 environment binding; earlier qualification environment lock | VERIFIED / ACTIVE | Reproducibility control |

## Current critical-path summary

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

The inventory therefore identifies **one remaining active E1 readiness gate: E1-08**.

## Material unknowns

1. Exact human minutes/hours per historical control are not persistently measured.
2. Exact machine cost per full qualification replay is not persistently measured.
3. A canonical `POST_BACKTEST_BACKLOG` artifact was not found on the current branch.
4. The long-run value/cost ratio of every historical non-E1 qualification layer has not yet been empirically measured against a simpler counterfactual.
