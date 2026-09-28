# PHASE 20 — REDUNDANCY_MAP

Date: 2026-09-28  
Base HEAD: `f3e02454f4a3ea5bb133586141fe9d28656b348d`

Purpose: identify **overlap**, not automatically delete controls. Overlap may be justified when controls act at different temporal boundaries.

## Map

| Cluster | Overlapping controls | What is genuinely different | Redundancy assessment | Audit consequence |
|---|---|---|---|---|
| R-01 Identity stack | repo identity, branch, HEAD, TREE, protected blobs, preflight bindings | repo/branch selects target; HEAD/TREE selects state; blobs select protected objects | HIGH implementation overlap, LOW semantic redundancy | Candidate for one shared identity verifier |
| R-02 Qualification provenance | exact-byte materialization + persisted-HEAD re-break | materialization proves bytes; re-break proves behavior of persisted bytes | MEDIUM overlap, both materially useful | Can share one harness, should not collapse semantics |
| R-03 Documentary evidence | detailed report + recovery checkpoint | report carries evidence; checkpoint carries continuation state | HIGH content duplication observed | Checkpoint can become index/status + hashes; report remains detail |
| R-04 Contract/test freezing | contract freeze + frozen breaker + post-commit blob checks | freeze defines rule; breaker encodes falsification; blob check detects drift | LOW redundancy | KEEP as distinct guarantees |
| R-05 Human approval | historical per-step approvals + accelerated macro authorization + mandatory STOP | macro covers mechanical cycle; STOP reserves normative/authority changes | HIGH redundancy in repeated mechanical approvals | Legacy micro-approval pattern is removable from critical path candidate |
| R-06 Reproducibility | E1-07 preflight + repository safety identity rules + environment identity | safety rules are general; E1-07 binds experiment execution state | MEDIUM overlap | Shared implementation possible; preserve both scopes |
| R-07 Audit/adversarial protection | breaker suites + independent E1-06 reference | breakers test stated properties; reference tests implementation parity independently | LOW redundancy | Do not merge into one implementation |
| R-08 Data identity | AP0 hashes + H1 canonical digest + E1-07 dataset bindings | raw source, derived dataset and execution preflight are different layers | LOW redundancy | KEEP layered chain |
| R-09 Scope control | E1-01 scope freeze + Phase 19 scope freeze | E1-01 freezes experiment; Phase 19 freezes project critical path | LOW redundancy | Distinct scopes |
| R-10 Authority control | forbidden claims in E1-01/E1-04/E1-06/E1-07 + E1-08 gate | claim boundaries constrain interpretation; E1-08 constrains execution | MEDIUM textual repetition, LOW semantic redundancy | Central claim/authority registry could reduce copying |
| R-11 A0 vs E1 | A0 V0.3 evidence gaps + E1 readiness controls | A0 concerns upstream semantic projection; E1 is first experiment readiness | Not redundant | A0 gap expansion can remain deferred unless it invalidates E1 |
| R-12 GitHub vs Obsidian | GitHub evidence/state vs knowledge projection | GitHub is canonical; Obsidian is projection | Not redundant when boundary is respected | Obsidian should not re-enter backtest critical path |

## Key finding

The largest avoidable redundancy is **operational**, not scientific:

```text
manual identity repetition
+ repeated micro-authorization
+ duplicated report/checkpoint prose
```

The strongest scientific controls — frozen OOS, exact data identity, execution semantics, independent parity, persisted-head re-break — are layered rather than duplicative.

## Falsification condition

This map would be wrong if a supposedly overlapping control rejects a material failure that the proposed shared mechanism cannot reject. Therefore Phase 21 must not approve a merge without a regression test demonstrating preserved rejection behavior.
