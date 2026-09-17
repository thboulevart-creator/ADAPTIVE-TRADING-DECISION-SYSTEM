# ADJUDICATION — GROK COUNTER-EXPERTISE — P1.1 DECISION → ACTION AUTHORIZATION

**Status:** ADJUDICATED  
**External source:** Grok  
**Original target:** `304bf0c370c422b6cb8ea9159cbaf1c282ec01f9`  
**Corrected candidate:** `2777025fefb1a7edcd5f9017c5e8b6dff13972bf`  
**Date:** 2026-09-17

## 1. Principle

The Grok report is treated as a non-normative adversarial source. Each finding is accepted, narrowed, rejected or escalated only after comparison with the repository and executable attacks.

## 2. External findings adjudication

### CLAUDE-P1.1-01 — weakref/id in-process attestation

**Adjudication:** ACCEPTED AS `IN_PROCESS_LIMIT / FUTURE_AUTHORIZED_RISK`.

The current registries are intentionally live-object/in-process. Loss of object identity, process boundary, reload or serialization loses attestation and therefore fails closed. No current positive authorization bypass follows from that fact.

This remains a mandatory design question before any persistence/inter-process consumer or positive `AUTHORIZED` path is introduced.

### CLAUDE-P1.1-02 — monkeypatch / closure introspection

**Adjudication:** PARTIALLY ACCEPTED, EXTERNAL SEVERITY WAS TOO LOW FOR ONE SUBCASE.

Grok correctly identified that verifier names and closure registries are mutable/introspectable in the same Python process. New executable attacks G2–G4 confirmed that verifier substitution and direct closure-registry injection can forge the intermediate authenticity predicate, but the current block-only evaluator still ends `BLOCKED` after those attacks.

However, adjudication found a separate current defect not identified by Grok:

- `_blocked()` used the mutable module-level name `BLOCKED`;
- rebinding `authorization_module.BLOCKED = "AUTHORIZED"` caused `evaluate_pre_action_authorization()` to emit `verdict.verdict == "AUTHORIZED"`;
- `AuthorizationVerdict` could also be directly constructed with `verdict="AUTHORIZED"` because `typing.Literal` is not runtime enforcement.

These are current positive-looking verdict forgeries, not merely future risks.

### CLAUDE-P1.1-03 — SHA-256 identifiers truncated to 16 hex

**Adjudication:** ACCEPTED AS LOW / FUTURE RISK, SAFE TO DEFER.

The live-object registry additionally checks a full fingerprint. The 64-bit display/binding identifier must not be promoted to a standalone cryptographic authorization proof. Revisit before persisted/cross-process identity or positive authorization relies on it.

### CLAUDE-P1.1-04 — constraint binding dual path

**Adjudication:** ACCEPTED AS LOW / CODE-SIMPLICITY + FUTURE-AUTHORIZED RISK.

No current bypass was demonstrated. The `__binding_only__` reconstruction and equivalent fallback hash are redundant and should be simplified before a positive authorization design relies on `constraint_id` independently of the live Decision object.

No code change was made in this adjudication because it is not required to close the demonstrated block-only defect.

### CLAUDE-P1.1-05 — workflow trust dependency gap

**Adjudication:** ACCEPTED AS CURRENT WORKFLOW GAP — CORRECTED.

The P1.1 workflow now triggers on the immediate/transitive trust surfaces exercised by the qualified producer path, including:

- `src/research_run_evidence.py`;
- `src/context.py`;
- `src/decision_trace.py`;
- `src/data/dataset_admissibility.py`;
- `src/research/execution.py`;
- `src/research/input_binding.py`;
- `tests/research_runtime_fixture.py`;
- the external counter-expertise test file.

### CLAUDE-P1.1-06 — id reuse after weakref cleanup

**Adjudication:** ACCEPTED AS NOTE / FAIL-CLOSED ONLY.

No positive inheritance path exists after the cleanup callback removes the registry entry.

## 3. Additional adversarial attacks added

A new test surface `tests/test_decision_action_authorization_counterexpertise.py` adds:

- `G0` — monkeypatch module-level `BLOCKED` to `AUTHORIZED` must not alter emitted verdict semantics;
- `G1` — direct construction of an `AuthorizationVerdict` claiming `AUTHORIZED` must be rejected at runtime;
- `G2` — monkeypatch imported Decision verifier to always true; block-only final state must remain `BLOCKED`;
- `G3` — direct CPython closure registry injection for a forged Decision; even if intermediate attestation is forged, evaluator must remain `BLOCKED`;
- `G4` — direct closure registry injection for reconstructed constraints; evaluator must remain `BLOCKED`.

## 4. Persisted red proof

HEAD: `48f7af3f8445330d559355448b17ca899525f124`  
Workflow: `P1.1 Decision-Action Authorization Tier-A`  
Run/job: `35201673212 / 105137643728`  
Conclusion: **FAIL**

Protected `RESEARCH → DECISION` remained green.

External attacks produced exactly two failures:

1. G0: expected `BLOCKED`, obtained `AUTHORIZED` after rebinding the module constant;
2. G1: manual `AuthorizationVerdict(verdict="AUTHORIZED", ...)` was accepted instead of raising.

The other 44 tests passed.

## 5. Minimal correction

Commit: `2777025fefb1a7edcd5f9017c5e8b6dff13972bf`

Only the block-only verdict semantics were changed:

1. `AuthorizationVerdict.__post_init__()` now rejects every runtime verdict other than literal `"BLOCKED"`;
2. `_blocked()` now constructs with literal `"BLOCKED"`, not the mutable module-level `BLOCKED` name.

No ACTION, risk engine, acquisition, backtest or live surface was added.

## 6. Re-break proof

HEAD: `2777025fefb1a7edcd5f9017c5e8b6dff13972bf`  
Workflow: `P1.1 Decision-Action Authorization Tier-A`  
Run/job: `35201771267 / 105137965680`  
Conclusion: **SUCCESS**

Green steps include:

- exact persisted HEAD / P0.6 ancestry;
- bounded side-effect-free P1.1 surface;
- exact locked P0.6 environment;
- protected `RESEARCH → DECISION` re-break;
- A0–F5 plus G0–G4;
- clean worktree.

## 7. Current verdict

**Block-only candidate after Grok adjudication: PASS for the currently tested in-process fail-closed scope.**

**P1.1 global boundary: still BLOCKED.**

Reasons:

- no governed positive authorization policy exists;
- the current attestation threat model remains intentionally in-process and must be revisited before persistence/inter-process or any positive `AUTHORIZED` path;
- an independent Claude counter-expertise remains useful before opening any positive path.

## 8. Must-fix / decide before any future AUTHORIZED path

1. define the exact same-process hostile-code / monkeypatch / introspection threat model;
2. decide whether attestation must survive process/persistence boundaries and, if yes, replace or augment live-object registries;
3. simplify and requalify constraint binding semantics;
4. decide collision-resistance requirements for persisted/cross-process identifiers;
5. qualify the provenance/non-forgeability of any future positive authorization verdict itself;
6. re-run all P1.1 attacks on the persisted HEAD after any such change.
