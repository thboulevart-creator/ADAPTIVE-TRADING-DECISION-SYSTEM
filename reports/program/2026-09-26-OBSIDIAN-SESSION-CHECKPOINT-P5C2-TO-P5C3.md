# OBSIDIAN SESSION CHECKPOINT — P5-C2 → P5-C3

Date: 2026-09-26

## Purpose

Persist the exact stopping point for resumption in the next session.

## Current qualified branch state

Repository:

    thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Obsidian work branch:

    feat/obsidian-projection-p5c2-promotion-experiment-harness-v0.1

Current branch HEAD at checkpoint:

    33c6184d8404b6cb0f59dbb0ead68949ece27544

This branch contains the persisted P5-C2 qualification record.

## Qualified progression

Completed and closed PASS:

    P3-D2 — OneDrive first-open qualification
    P4-A  — human navigation contract
    P4-B  — native view bundle
    P4-C  — visual/navigation acceptance V0.1
    P5-A  — continuous projection engine contract
    P5-B  — dynamic current-head inventory contract
    P5-B2 — dynamic inventory implementation
    P5-C  — Windows/OneDrive promotion qualification protocol
    P5-C2 — filesystem promotion experiment

## P5-C2 empirical result

Selected filesystem publication primitive:

    IMMUTABLE_GENERATION_ATOMIC_POINTER

Observed PASS evidence:

    250 / 250 promotion cycles
    5001 reader samples
    250 reader samples during promotion cycles
    mixed_generation_count = 0
    missing_entrypoint_count = 0
    partial_generation_count = 0
    parse_error_count = 0
    crash recovery probe = PASS

Rejected / unsupported candidates:

    DIRECTORY_TWO_RENAME_SWAP
      = FAIL / PermissionError

    WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE
      = NOT_SUPPORTED / MOVEFILEEX_ERROR_5

Negative control:

    DIRECT_IN_PLACE_PER_FILE_REPLACE
      = correctly exposed non-atomic behavior
      = 4375 partial-generation observations
      = never qualifiable

Live Vault protection evidence:

    generated/ before digest
      46a8959efbf7ead73c8d79b3dd6268df94aa9176d5ca76721d7ad5f484217088

    generated/ after digest
      46a8959efbf7ead73c8d79b3dd6268df94aa9176d5ca76721d7ad5f484217088

    views/ before digest
      853e08b68f92a86ca4cdc8d91c78448debc87d631467c9b4daefecbea7fbd4bb

    views/ after digest
      853e08b68f92a86ca4cdc8d91c78448debc87d631467c9b4daefecbea7fbd4bb

    live_vault_modified = false

Important remaining restrictions:

    obsidian_open_qualified = false
    production_promotion_authorized = false

## Current live Vault

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

Current V0.1 user-facing layer:

    views/HOME.md
    views/dashboards/PROJECT-SNAPSHOT.md
    views/dashboards/QUALIFICATION-STATUS.md
    views/maps/SYSTEM-ARCHITECTURE.md
    views/maps/GOVERNANCE.md
    views/maps/RESEARCH-LIFECYCLE.md
    views/canvas/ATDS-OVERVIEW.canvas

P4-C accepted this V0.1 navigation layer as usable but not as the final visual architecture.

## Visual target reaffirmed

The long-term target is not merely a menu-style Vault.

The intended result is a highly refined, professional, dense but controlled visual knowledge architecture comparable in overall visual character to an Obsidian-style global knowledge graph:

- hundreds of project artifacts represented as navigable nodes;
- visible dependency and governance paths;
- architecture layers and lifecycle paths;
- clusters by artifact family / system area / epistemic state;
- controlled edges derived from qualified relationships;
- direct navigation from high-level system maps to exact source artifacts;
- continuous refresh from GitHub source changes.

The visual reference supplied by the user on 2026-09-26 is treated as a UX/visual-density target only, not as proof that a native Obsidian Graph alone is sufficient.

## Critical architectural issue for the final graph

P5-C2 selected immutable generations + atomic CURRENT pointer.

This safely publishes machine generations at filesystem level, but native Obsidian Graph/Search indexes files that physically exist in the Vault.

Therefore simply storing multiple immutable generations inside the ordinary indexed Markdown namespace would risk:

- duplicate nodes from old generations;
- stale links;
- graph inflation;
- search ambiguity;
- inability of native Graph to understand the CURRENT pointer as semantic selection authority.

The final graph architecture must solve this before production synchronization.

## Next governed boundary

Resume directly with:

    P5-C3 — OBSIDIAN-OPEN SANDBOX COMPATIBILITY QUALIFICATION

Goal:

Test the selected IMMUTABLE_GENERATION_ATOMIC_POINTER primitive while a sacrificial sandbox Vault is actually open in Obsidian.

Constraints:

- never use the real user Vault as the experiment target;
- preserve real Vault digests;
- no plugin installation;
- no Obsidian Sync;
- no production observer;
- no continuous production synchronization.

## Required work after P5-C3

If P5-C3 passes, proceed toward:

    P5-D — CONTINUOUS OBSERVER IMPLEMENTATION

Then:

    P5-E — END-TO-END NEAR-REAL-TIME QUALIFICATION

After the synchronization substrate is qualified, continue the visual program:

    P6 — CONTROLLED KNOWLEDGE GRAPH
    P7 — NATIVE BASES / DYNAMIC DASHBOARDS
    P8 — PROFESSIONAL VISUAL ARCHITECTURE
    P9 — OPERATIONAL WORKSPACES

## Visual-graph implementation direction to evaluate later

To reach the target visual density while preserving authority and freshness, the later graph program must compare at least these options:

1. Native Obsidian Graph over stable machine-managed live notes.
2. Generated native Canvas maps for deterministic architectural paths.
3. Native Bases for structured exploration.
4. A separately qualified custom visual layer/plugin only if native Graph cannot safely represent CURRENT-generation semantics under immutable publication.

No plugin is authorized by this checkpoint.

## Resume instruction

On next session:

1. verify GitHub branch/head above;
2. do not reopen P0-P5-C2;
3. begin P5-C3 directly;
4. keep the visual target and CURRENT-generation graph-indexing problem in scope;
5. do not use the real Vault for P5-C3 experiments.
