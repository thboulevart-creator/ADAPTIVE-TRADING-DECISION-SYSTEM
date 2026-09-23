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

## 10. BACKTEST GATE — EXPLORATORY OFFLINE V0 EXCEPTION

**Qualification / confirmatoire.** Aucun backtest confirmatoire, aucun résultat destiné à valider une stratégie pour exploitation et aucune promotion probatoire ne peuvent commencer avant que les blocs de qualification **applicables au test et à la source** soient PASS. Le corpus, l'usage visé et les exigences applicables doivent être explicitement désignés ; un gate BI5 global non résolu ne devient pas PASS par l'usage d'une autre source.

**E0 — inventaire seulement.** Après adoption documentaire de la frontière `EXPLORATORY OFFLINE RESEARCH V0`, un inventaire en lecture seule de données historiques déjà existantes peut être ouvert **uniquement dans un environnement/emplacement autorisé par le propriétaire** et sous préflight de ressources. E0 n'est pas un backtest et ne calcule aucun signal de stratégie, trade, position, fill ou PnL. L'accès technique n'est pas une autorisation.

**E1 — exception exploratoire étroite.** Après adoption documentaire de cette même frontière, une simulation historique **offline, bornée, de statut exclusivement N0** peut être envisagée sans exiger le PASS de tous les blocs destinés à la qualification confirmatoire. Elle reste **interdite tant qu'une autorisation spécifique du propriétaire pour le run, un corpus identifié/admissible pour la question, les droits et l'environnement d'accès, les contrôles temporels/continuité pertinents, un protocole et un modèle de coûts/scénarios honnêtement étiquetés, des plafonds de ressources et une fiche de préflight acceptée ne sont pas réunis**. Le dossier de référence est le candidat V0 et sa revue/adjudication versionnés dans `reports/program/`. L'adoption de V0 n'autorise à elle seule aucune exécution E1.

Pour la **qualification de recherche** et selon le test concerné, maintenir les exigences applicables, dont :
- minimum cinq ans lorsque requis par le protocole de qualification, notamment la baseline Momentum V1 ;
- modélisation en vrais ticks lorsque la question ou le moteur d'exécution l'exige ;
- spread et coûts de transaction réalistes attestés ;
- validation hors échantillon à statut probatoire déclaré ;
- robustesse, notamment élargissement de spread lorsque pertinent ;
- MT5 `Every tick based on real ticks` lorsque le protocole de qualification MT5 l'exige ;
- aucune substitution silencieuse d'une modélisation faible à la preuve requise.

Aucune sonde E1 plus courte, en barres seules, brute ou sous coûts hypothétiques ne peut être rebaptisée « backtest de qualification PASS », « Momentum V1 baseline PASS » ou « OOS vierge » par ce seul fait. Les périodes réellement consultées doivent être tracées. Confirmatoire, paper, broker/live, capital réel, acquisition de nouveaux objets de marché, FULL_INTERVAL, D materialization et contact Dukascopy ne sont pas ouverts par E0/E1.

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

## 14. DURABLE SESSION BACKUP — MANDATORY

`99-BACKUP/` is the dedicated durable project-memory layer.

At the beginning of every substantive session, after reading this file and the Recovery Checkpoint, the AI MUST read the newest applicable `99-BACKUP/SESSION-YYYY-MM-DD.md` before searching for prior work.

At the end of every material session, the AI MUST preserve a dated session snapshot in `99-BACKUP/` containing the context required to recover the work without relying on conversational memory, including where relevant:

- code and artifact state;
- decisions and their reasons;
- hypotheses;
- experiments and results;
- failures and corrections;
- locked verdicts;
- important identities and hashes;
- what is on GitHub;
- what remains local or unpersisted;
- divergences;
- prohibited reruns;
- exactly one next governed action.

The backup layer does not replace source code or evidence. It prevents loss of project context and prevents repeated morning reconstruction of already completed work.

A workstream cannot be considered durably closed merely because its state appears in conversation. Important executable artifacts must be versioned on the governed branch, or their absence must be explicitly recorded as BLOCKED / NON-PERSISTED.
