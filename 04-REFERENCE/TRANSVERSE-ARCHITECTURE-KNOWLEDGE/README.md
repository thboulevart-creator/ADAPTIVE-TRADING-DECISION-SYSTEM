# Transverse Architecture Knowledge Dossier

**Status:** WORKING DOSSIER — NON-NORMATIVE
**Purpose:** Centralize architectural knowledge, candidate improvements, adjustment requirements and rejected ideas discovered through external sources, audits and cross-system analysis.

## Scope

This dossier is intended to serve the autonomous-system family, including:

- ADAPTIVE-TRADING-DECISION-SYSTEM
- AUTONOMOUS-CONTENT-INTELLIGENCE-SYSTEM
- future autonomous systems derived from the same architectural principles

It is a **knowledge and decision-preparation layer**, not a normative contract. It must never silently override an existing frozen contract.

## Why this exists

External material can contain valuable architectural mechanisms mixed with examples, opinions, marketing, obsolete assumptions or implementation-specific details. This dossier separates:

```text
SOURCE MATERIAL
    ↓
ATOMIC IDEA
    ↓
CURRENT-STATE COMPARISON
    ↓
STATUS
    ↓
RATIONALE
    ↓
ARCHITECTURAL DELTA
    ↓
DEPENDENCIES / IMPACT
    ↓
ARBITRATION
    ↓
IMPLEMENTATION PLAN
```

## Decision statuses

- `EXISTS_ALREADY` — materially covered by an existing governed artifact.
- `PARTIALLY_PRESENT` — principle exists but an important capability/interface is incomplete.
- `ABSENT` — not materially represented in the current architecture.
- `REDUNDANT` — duplicate of an existing capability with no justified architectural delta.
- `CONTRADICTORY` — conflicts with an existing contract, invariant or architectural principle.
- `ADJUSTMENT_REQUIRED` — existing element should be revised without necessarily adding a new component.
- `NEW_MODULE_REQUIRED` — requires a new architectural component or subsystem.
- `DEFERRED` — potentially valuable but not yet sufficiently specified or justified.
- `REJECTED` — retained only as a recorded negative decision, with rationale.

## Evidence rule

A statement that something is already implemented must point to the current repository artifact. A statement that something is absent must be based on a repository inspection, not on memory or assumption.

## Implementation rule

Nothing in this dossier becomes normative merely by being recorded here. Any change to a frozen contract must follow the repository's existing governance, contradiction, challenge and audit mechanisms.

## Current source baseline

Initial assessment performed against the current `main` branches on 2026-09-08. The current repositories already contain substantial architecture for validation, provenance, adversarial analysis, contradiction handling, upward challenge and experimental memory. The purpose of the dossier is therefore primarily to identify the **remaining delta**, not to recreate those mechanisms.

## Contents

- `01-SOURCE-EXTRACTION.md` — atomic findings extracted from the source text.
- `02-CURRENT-STATE-MATRIX.md` — comparison against the current architecture.
- `03-ARCHITECTURAL-DELTA.md` — retained changes, rationale, destination and dependency order.
- `04-REUSABLE-PATTERNS.md` — patterns suitable for future autonomous-system repositories.

## Governing principle

> **Do not add a feature because a source mentioned it. Add an architectural capability only when a verified gap exists and the capability improves the system without violating its contracts, invariants or ownership boundaries.**
