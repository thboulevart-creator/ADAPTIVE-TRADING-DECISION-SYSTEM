# P1.1 — DECISION → ACTION AUTHORIZATION — QUALIFICATION

**Date:** 17 septembre 2026  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Contract:** `P1_1_DECISION_ACTION_AUTHORIZATION_BOUNDARY_V1`  
**Scope:** block-only pre-ACTION authorization boundary  
**State at this report:** **QUALIFIED CANDIDATE / FINAL DOCUMENTARY PERSISTED-HEAD REBREAK PENDING**

## 1. Qualified scope

P1.1 qualifies only the block-only boundary:

`qualified Decision → identity/content verification → authorization constraints → BLOCKED`

It does not create ACTION, execute an order, size a position, select leverage, set SL/TP, call a broker/exchange, acquire `.bi5`, run a real backtest or activate live behavior.

No positive `AUTHORIZED` policy exists in the qualified candidate.

## 2. Minimal implementation

The candidate adds/qualifies:

- downstream process-local attestation of producer-created `Decision` objects in `src/decision.py`;
- `AuthorizationConstraints` bound to the exact Decision identities;
- `AuthorizationVerdict` with runtime-enforced block-only semantics;
- `evaluate_pre_action_authorization(...)` with fail-closed checks;
- the Tier-A adversarial suite A0–F5 plus external counter-expertise attacks G0–G5;
- a path-scoped, P0.6-locked, read-only P1.1 workflow.

The constraint verifier was simplified to a single explicit identity calculation; the former redundant dual-path / `__binding_only__` reconstruction was removed.

## 3. Real adversarial red evidence

### 3.1 Verdict-forgery red

HEAD:

`48f7af3f8445330d559355448b17ca899525f124`

Run/job:

`35201673212 / 105137643728`

Observed result:

- `44 passed`;
- G0 failed because rebinding module-level `BLOCKED` to `AUTHORIZED` could make the evaluator emit an AUTHORIZED-looking string;
- G1 failed because `typing.Literal["BLOCKED"]` alone did not prevent direct construction of `AuthorizationVerdict(verdict="AUTHORIZED", ...)`.

Correction:

- runtime validation in `AuthorizationVerdict.__post_init__()`;
- `_blocked()` emits literal `"BLOCKED"` independently of a mutable module constant.

### 3.2 Closure-introspection red

External Claude review targeted the older `304bf0c...` candidate, but its closure-registry finding was independently reproduced on the corrected branch rather than accepted by authority.

Red HEAD:

`adf1558e46bbe27d1ab7c697d921f94b082b37b9`

P1.1 run/job:

`35233644836 / 105243882059`

P0.4 run/job:

`35233644848 / 105243882076`

Observed result:

- reflective access to CPython closure cells can mutate the process-local Decision and ResearchRunEvidence attestation registries;
- the same pattern is systemic upstream, not unique to P1.1;
- four closure-related attacks failed in the global regression while the rest of the suite remained green.

## 4. Adjudication of the closure finding

The correction deliberately does **not** pretend that a mutable Python dictionary can be made into an enclave against arbitrary code already executing inside the same interpreter.

The governed threat model now distinguishes:

- adversarial/untrusted input crossing the normal API boundary: must fail closed against reconstruction, copy, substitution, mutation and unsupported minting;
- arbitrary same-interpreter reflection/monkeypatch/closure-cell mutation: **process compromise**.

Process-local attestation remains acceptable for the current block-only integrity scope, because even a fully forged reflective chain must still terminate at the hard block-only policy gate.

A positive `AUTHORIZED` path is explicitly **BLOCKED** until either:

1. the authorization authority is isolated behind a separately qualified trust/process boundary with narrow inputs; or
2. another separately qualified attestation primitive provides equivalent resistance to the future caller threat model.

The 16-hex deterministic Decision/constraint identifiers are not treated as standalone security tokens and must be requalified before persisted, cross-process or positive authorization use.

## 5. External counter-expertise adjudication

### Grok

Useful findings retained:

- workflow trust-dependency coverage;
- process-local/reload/persistence limitations;
- future monkeypatch risks;
- 64-bit identifier posture;
- redundant constraint-verifier logic.

Grok's initial global PASS was not accepted as authority. Internal adversarial testing subsequently discovered the G0/G1 verdict-forgery defects that Grok had not identified.

### Claude

Useful findings retained:

- closure-cell registry mutability;
- workflow trust-dependency coverage;
- redundant verifier branch;
- future identifier-collision posture;
- process/reload/pickle limitations.

Claude audited the older `304bf0c...` target, so every material finding was rechecked against the corrected current lineage. The closure finding survived and was reproduced; obsolete workflow findings were adjudicated against the newer workflow state.

## 6. Workflow and composability corrections

P1.1 now watches immediate trust dependencies including:

- `src/research_run_evidence.py`;
- `src/context.py`;
- `src/context_identity.py`;
- `src/decision_trace.py`;
- relevant research/data surfaces;
- the qualification environment lock, requirements lock and verifier.

P0.4 and P0.5 explicitly retain the process-integrity probe. P0.2 was made composable with legitimate P1.1 evolution of `src/decision.py` while continuing to re-break the original anti-forgery properties rather than demanding obsolete byte identity.

## 7. Common persisted-HEAD qualification evidence

Common technical qualification HEAD:

`5a4c9f94cb330ad04b1c00cb8ebed86dfab746d5`

All relevant workflows completed **SUCCESS** on that exact SHA:

- P0.2 Decision Block Regression Guard: `35235197049 / 105249191301`;
- P0.3 Multi-Year Regression Guard: `35235197091`;
- P0.4 Research Producer Junction Tier-A: `35235197054 / 105249191568`;
- P0.5 Research Inter-Process Re-Attestation Tier-A: `35235197038 / 105249191096`;
- P0.6 System Reproducibility Tier-A: `35235197003 / 105249191263`;
- P1.1 Decision-Action Authorization Tier-A: `35235197002 / 105249190934`;
- DATA → CONTEXT: `35235197017`;
- CONTEXT → RESEARCH: `35235197013`;
- RESEARCH FINDINGS: `35235197055`;
- RESEARCH → DECISION: `35235197007`.

P1.1 specifically proved on the common HEAD:

- exact persisted HEAD / P0.6 ancestry;
- bounded and side-effect-free block-only candidate;
- exact P0.6 qualification environment;
- protected RESEARCH → DECISION re-break;
- A0–F5 plus G0–G5 counter-expertise attacks;
- clean worktree.

P0.4/P0.5/P0.6 also re-ran complete repository regressions and protected earlier boundaries on the same common HEAD.

## 8. Safety truth unchanged

P1.1 does not alter the closed safety state:

- global `111 / 91 / 20` → **BLOCKED**;
- selected window `2021-08-14 → 2026-08-14`;
- selected `68 / 68 / 0` → **PASS**;
- persisted freeze → **PASS**;
- acquisition → **BLOCKED**;
- `massive_acquisition_authorized = false`;
- `real_backtest_authorized = false`;
- live activation unauthorized.

## 9. Closure condition

This report, the P1.1 session backup and the Recovery Checkpoint must be persisted first.

Then one final read-only common persisted-HEAD re-break must succeed on the resulting documentary HEAD or on its immediate descendant differing only by a semantically neutral CI-trigger comment.

A successful final run closes the **P1.1 block-only boundary** directly as `CLOSED / PASS`. No additional documentary mutation is required afterward, preventing a recursive closure/requalification loop.

That closure does **not** authorize a positive `AUTHORIZED` path. Positive authorization remains `BLOCKED` pending the isolated/equivalently strong trust-boundary and identifier-security qualification described above.
