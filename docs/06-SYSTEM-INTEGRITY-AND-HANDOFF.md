# 06 — SYSTEM INTEGRITY & HANDOFF PROTOCOL

## 1. Objective

Prevent the class of failure in which a long system document is transmitted incompletely, appears empty, is split inconsistently, or is worked on from a stale copy.

## 2. Single Source of Truth

The GitHub repository is the canonical source of truth for the system.

The canonical document chain is:

```text
00-MASTER-EXECUTION-CHECKLIST
01-SYSTEM-VISION
02-ASSET-PROFILE-DATABASE
03-REGIME-EXPERT-RESEARCH-FOUNDATION
04-VALIDATION-CRITERIA
05-DATA-CONTRACT
```

Documents 00–05 must live under `docs/`. Numbered system documents must not be duplicated at repository root.

## 3. Handoff Rule

AI agents must never be treated as the authoritative storage location for the system documents. Claude, ChatGPT, Perplexity or another model may read, audit, modify or propose changes, but the repository remains canonical.

For a handoff, the agent must identify the exact repository path and document version/commit being used. If the document cannot be retrieved completely, work stops rather than proceeding from a partial transmission.

## 4. Integrity Gate

`tools/validate-system.py` is the minimum machine gate. It verifies:

- all canonical documents 00–05 exist;
- files are non-empty;
- files are not suspiciously small;
- placeholder markers are absent;
- numbered documents are not accidentally duplicated outside `docs/`.

GitHub Actions runs this gate on relevant pushes and pull requests.

## 5. Change Control

A change to a canonical document must be committed to Git before it becomes an accepted system change. Draft text in an AI conversation is not an accepted version.

Preferred flow:

```text
REQUEST
  ↓
READ CANONICAL REPOSITORY
  ↓
ANALYSE / PROPOSE CHANGE
  ↓
EDIT REPOSITORY
  ↓
INTEGRITY GATE
  ↓
REVIEW
  ↓
MERGE / ACCEPT
```

## 6. Failure Rule

If any integrity check fails:

```text
STOP → DO NOT ANALYSE PARTIAL CONTENT → FIX SOURCE → RE-RUN GATE
```

This is mandatory. A model must not reconstruct missing sections from memory or continue from an incomplete attachment when the repository version is available.

## 7. Why This Exists

The system must be reproducible independently of the conversational interface. A lost context window, empty attachment, token limit, split message, model switch, or exhausted AI credit must not be capable of corrupting the canonical trading-system specification.
