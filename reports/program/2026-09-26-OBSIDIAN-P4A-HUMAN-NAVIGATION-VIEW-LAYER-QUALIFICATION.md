# OBSIDIAN P4-A — HUMAN NAVIGATION / VIEW LAYER QUALIFICATION

Date: 2026-09-26

## Scope

This record closes P4-A, the contract-and-breakers phase for the first native human navigation layer of the qualified ATDS Obsidian Vault.

## Persisted candidate

Branch:

    feat/obsidian-projection-p4a-human-navigation-contract-v0.1

Persisted candidate HEAD before local execution:

    8972bc36bf8dc62936f63f1595539b45e7026f60

P3-D2 predecessor closure:

    4660a3e5daa57f38175d403b1a1fecef257796af

## User-reported local execution

The user reported:

    Ran 277 tests in 8.056s
    OK

    P4A_PERSISTED_LOCAL_REBREAK_PASS

Control worktree:

    C:\Users\Boulevart\AppData\Local\Temp\ATDS-P4A-dfc578bb953e40dc9b92fdfdbd691afe

This runtime result is USER-REPORTED LOCAL EXECUTION, not independent execution evidence.

## Qualified boundary

P4-A is qualified only as the architecture and safety contract for a native, non-authoritative, snapshot-bound human navigation layer.

The qualified rules include:

- GitHub/ATDS remains canonical;
- `generated/` remains machine-owned, deterministic and derived;
- `views/` remains human-owned and non-authoritative;
- P2 may neither write `views/` nor consume it as semantic input;
- initial navigation uses only Markdown and native Obsidian Canvas;
- Dataview, Excalidraw, Tasks, custom JavaScript/CSS, community plugins, Obsidian Sync and Vault Git automation are outside scope;
- wikilinks/backlinks are navigation only;
- Canvas edges are navigation only unless backed by a qualified generated relation;
- qualification/scientific/authority/epistemic/temporal/persistence axes remain separate;
- every initial view is bound to a deterministic projection identity;
- stale views may remain readable but may not claim current;
- the initial bundle is capped at seven files.

## Qualified initial information architecture

    views/
    ├── HOME.md
    ├── dashboards/
    │   ├── PROJECT-SNAPSHOT.md
    │   └── QUALIFICATION-STATUS.md
    ├── maps/
    │   ├── SYSTEM-ARCHITECTURE.md
    │   ├── GOVERNANCE.md
    │   └── RESEARCH-LIFECYCLE.md
    └── canvas/
        └── ATDS-OVERVIEW.canvas

## Projection binding inherited by P4-B candidate

    generated_file_count = 92

    projection_tree_digest_sha256 =
    bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0

## Verdict

**PASS — P4-A HUMAN NAVIGATION / VIEW LAYER CONTRACT QUALIFIED**

This PASS does not mean the seven views exist in the real Vault.

The next authorized candidate boundary is:

    P4B_NATIVE_VIEW_BUNDLE_IMPLEMENTATION_CANDIDATE

P4-B must be a separate persisted movement and must not write the real Vault before its own persisted local re-break passes.
