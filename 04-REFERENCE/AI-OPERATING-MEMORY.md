# AI OPERATING MEMORY — ALGO ECOSYSTEM

> Durable operating memory for AI-assisted work on this repository.
>
> This file is a governance artifact. It is not a substitute for source code, tests, qualification reports, or evidence. It defines the rules the AI must consult before acting.

## 1. MANDATORY PRE-ACTION RULE

Before any substantive action in this repository, the AI MUST consult this file and the current Recovery Checkpoint when one exists.

The AI MUST NOT rely solely on conversational memory for project state, previously validated steps, paths, probes, reports, branches, commits, or decisions.

If the current state cannot be established from GitHub and available execution evidence, the AI must stop and classify the situation as **BLOCKED** rather than inventing missing state.

## 2. SOURCE OF TRUTH HIERARCHY

1. Current repository code and versioned artifacts on GitHub.
2. Versioned qualification reports, verdicts, and Recovery Checkpoints.
3. Reproducible execution evidence from the current worktree/session.
4. Conversation history.
5. AI recollection/inference.

Lower-level memory MUST NOT override higher-level evidence.

## 3. RECOVERY & TRACEABILITY INVARIANT

Every important workstream MUST maintain a versioned Recovery Checkpoint containing:

- current system/repository;
- branch;
- reference commit;
- current block;
- path already traversed;
- PASS / FAIL / BLOCKED states;
- evidence and artifact locations;
- code/tests/probes/data/contracts/reports state;
- errors and failed approaches;
- why each failure occurred;
- corrections applied;
- lessons preventing recurrence;
- missing evidence;
- last verdict;
- exactly one next action.

The objective is to recover the state without repeating validated work and without depending on conversation history.

## 4. EVIDENCE DISCIPLINE

- Never issue a false PASS.
- Allowed qualification verdicts: **PASS / FAIL / BLOCKED**.
- BLOCKED means the control could not be executed or proven; it is not PASS.
- Distinguish explicitly between:
  - current violation;
  - architectural exposure;
  - absence of proof;
  - historical evidence;
  - reproducible current evidence.
- Never invent a file, path, probe, contract, dataset, hash, branch, commit, or prior result.
- Verify actual repository state before modifying anything.

## 5. ADVERSARIAL QUALIFICATION PROTOCOL

For qualification work, follow:

**formalisation → candidate → adversarial break → correction → re-break → verdict**

A candidate is not validated merely because its normal path works.

Every important control must be attacked for bypasses, substituted inputs, incomplete inputs, stale assumptions, and misleading evidence where applicable.

## 6. CHANGE DISCIPLINE

- Do not modify `main` casually.
- Do not merge, rebase, reset, force-push, or discard work without explicit state/evidence review.
- Do not use `git add .` for qualification commits.
- Do not create parasite artifacts merely to make a test pass.
- Prefer clean rewrites or deliberate new files over fragile string replacement when changing code.
- Preserve validated baseline artifacts.
- Before any write, identify exactly what is being changed and why.

## 7. NO LOOPING / NO REPETITION

When an execution fails, first diagnose the exact failure.

Do not:

- retry the same command blindly;
- assume a previously temporary probe still exists;
- assume a path from another worktree;
- recreate a qualification step already proven unless the evidence is genuinely lost or invalidated.

Record the failure and correction in the Recovery Checkpoint when it is materially relevant.

## 8. EXPERIMENTAL MEMORY

The system should progressively preserve not only outcomes but also:

- hypotheses;
- experiments;
- tested explanations;
- results;
- failures;
- successful corrections;
- validated knowledge;
- reasons why an approach was rejected.

A result without its experimental context is insufficient for reliable recovery.

## 9. GOVERNANCE ARTIFACT CHAIN

For important qualification work, prefer the durable chain:

**Script → Report → Verdict → Conclusion → Recovery Checkpoint**

Each artifact must be traceable to the state it describes.

## 10. BACKTEST GATE

No real backtest may begin before all mandatory qualification blocks are PASS.

For the trading research pipeline, the backtest methodology must preserve the project requirements including, where applicable:

- minimum five years of data;
- real tick modelling;
- true spread and transaction costs;
- out-of-sample validation;
- robustness testing such as spread widening;
- MT5 `Every tick based on real ticks` when using MT5;
- no substitution of weaker data modelling for required evidence.

## 11. MINDSET

The AI must not seek to prove that another AI, hypothesis, or prior conclusion is right or wrong.

The objective is to determine what is true from evidence.

The AI must actively ask:

> **Where could I be wrong?**

and attack its own proposed conclusion before declaring validation.

## 12. CROSS-REPOSITORY RULE

When work spans multiple ALGO ECOSYSTEM repositories, the same operating rules apply. The AI must consult the applicable repository's durable operating memory and Recovery Checkpoint before acting.

If repositories disagree, do not silently choose one. Surface the conflict and classify the state until the conflict is resolved with evidence.

## 13. CURRENT STATUS

This file establishes the durable operating-memory protocol. It does not itself certify any qualification block or technical result.

The current technical state must be read from the repository's latest Recovery Checkpoint and qualification artifacts.
