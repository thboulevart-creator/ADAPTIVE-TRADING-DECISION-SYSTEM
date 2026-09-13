# 99-BACKUP — DURABLE PROJECT MEMORY

## Purpose

This directory is the durable recovery layer for the ALGO ECOSYSTEM workstream.

It exists so that a new session can recover the project without reconstructing state from conversational history.

## Mandatory morning recovery order

Before substantive work, read:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. `99-BACKUP/README.md`
4. the newest dated `99-BACKUP/SESSION-*.md`
5. the artifacts explicitly referenced by the current checkpoint

## What belongs here

Each important work session must preserve the durable project context needed to continue safely:

- current repository and branch;
- reference/head commits;
- active research block;
- completed and locked verdicts;
- decisions and their reasons;
- hypotheses and assumptions;
- adversarial findings and corrections;
- important code paths and architecture contracts;
- datasets, contracts, hashes and evidence identities;
- artifacts created or modified;
- what is persisted on GitHub;
- what remains local or unpersisted;
- known divergences;
- failed approaches and why they failed;
- explicit prohibitions against repeating locked work;
- exactly one next governed action.

This is project memory, not a replacement for the actual source code or qualification evidence. The source-of-truth hierarchy in `AI-OPERATING-MEMORY.md` remains authoritative.

## Persistence rule

A workstream is not considered durably closed merely because its state is described in a conversation or checkpoint. Important executable artifacts must be versioned on the governed branch, or their absence must be explicitly recorded as BLOCKED / NON-PERSISTED.

## Session snapshots

Use one dated `SESSION-YYYY-MM-DD.md` per material workday/session. Update the snapshot before closing the workday whenever the project state materially changes.

Do not create multiple competing snapshots for the same state. The Recovery Checkpoint remains the authoritative current-state pointer; this directory preserves the broader context needed to understand and recover that state.
