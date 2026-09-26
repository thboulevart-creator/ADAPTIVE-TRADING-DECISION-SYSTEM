# OBSIDIAN P4-A — HUMAN NAVIGATION / VIEW LAYER CONTRACT V0.1

Date: 2026-09-26

## 1. Purpose

P4-A defines the first useful human-facing navigation layer for the qualified ATDS Obsidian Vault.

The objective is not to create another source of truth. The objective is to make the existing deterministic projection understandable and navigable in Obsidian without weakening the authority, epistemic, integrity, or first-open boundaries already qualified through P3-D2.

P4-A is a **contract-and-breakers phase only**. It does not write to the Vault.

## 2. Starting point

The predecessor boundary is the qualified P3-D2 first-open closure:

    4660a3e5daa57f38175d403b1a1fecef257796af

Qualified Vault:

    C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION

Bound deterministic projection:

    generated_file_count = 92
    projection_tree_digest_sha256 =
    bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0

P3-D2 established that the first open is qualified, the deterministic projection remained unchanged, `views/` remained empty, repository state remained preserved, community plugins were disabled, and Obsidian Sync was disabled.

## 3. Authority model

The authority hierarchy remains:

    GitHub / ATDS
        = CANONICAL TRUTH

    generated/
        = DERIVED
        = MACHINE-OWNED
        = DETERMINISTIC PROJECTION

    views/
        = VIEW
        = HUMAN-OWNED
        = NON-AUTHORITATIVE

    .obsidian/
        = UI CONFIGURATION
        = NON-SEMANTIC

P4-A does not reopen any prior qualification.

A view may explain, group, link, orient, or visualize information. A view may not authorize, qualify, change canonical truth, become semantic input, or create operational permission.

## 4. Native-first rule

The initial useful layer must work with standard Obsidian capabilities only.

Authorized initial formats:

- Markdown;
- native Obsidian Canvas JSON.

Not authorized in P4-A/P4-B initial scope:

- Dataview;
- Excalidraw;
- Tasks community plugin;
- custom JavaScript;
- custom CSS;
- remote embedded content;
- Obsidian Sync;
- Git automation from the Vault.

This keeps the first useful layer portable, inspectable, and independent of community-plugin execution.

## 5. Separation from P2

The deterministic P2 builder remains unchanged.

It MUST NOT:

- write `views/`;
- read `views/` as semantic input;
- derive authority from `views/`;
- modify `.obsidian/`.

A future P4-B implementation may seed the initial view bundle only under its own explicit contract. It is not an extension of P2 authority.

## 6. Initial information architecture

P4-A deliberately limits the first layer to seven files:

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

This is the smallest useful navigation surface that provides:

- one entry point;
- one factual snapshot dashboard;
- one status-oriented dashboard;
- three explanatory maps;
- one native visual overview.

More files require a later explicit expansion decision.

## 7. HOME

`views/HOME.md` is the human entry point.

It must make the authority boundary visible before navigation.

It must link to the six other initial views and may link to generated artifact records.

It must not present itself as a canonical document.

## 8. Dashboards

### PROJECT-SNAPSHOT

Purpose:

- show the identity of the projection being viewed;
- display the bound projection digest;
- display the projection source commit;
- display the view freshness state;
- expose explicitly scoped counts that can be recomputed from the bound projection.

It is a snapshot, not a live-control plane.

### QUALIFICATION-STATUS

Purpose:

- make qualification states easier to inspect;
- preserve exact scope;
- preserve UNKNOWN/BLOCKED distinctions;
- preserve separate status axes.

The following axes MUST NOT be collapsed into one synthetic status:

- qualification status;
- scientific status;
- authority role;
- epistemic role;
- temporal role;
- persistence state.

No overall quality, health, confidence, readiness, or maturity score is authorized.

## 9. Maps

The three Markdown maps are explanatory navigation surfaces.

### SYSTEM-ARCHITECTURE

Shows the major ATDS system areas and navigation routes.

### GOVERNANCE

Shows governance boundaries, qualification concepts, and authority separation.

### RESEARCH-LIFECYCLE

Shows how research/experience artifacts can be navigated without converting chronology or adjacency into semantic truth.

A map may contain explanatory prose, but unsupported claims must be omitted or explicitly marked UNKNOWN.

## 10. Canvas

`views/canvas/ATDS-OVERVIEW.canvas` uses native Obsidian Canvas only.

Canvas edges are NAVIGATION_ONLY by default.

A canvas edge may be described as a semantic relationship only when the edge is backed by a qualified relation record under:

    generated/relations/

A visual connection alone is never semantic evidence.

External URL nodes and files outside the Vault are forbidden in the initial canvas.

## 11. Wikilink semantics

Wikilinks and backlinks are navigation affordances only.

They do not establish:

- REFERENCES;
- USES_INPUT;
- PRODUCES;
- GOVERNS;
- TESTED_BY;
- CHALLENGED_BY;
- ADJUDICATED_BY;
- SUCCESSOR_OF.

Those semantic relation types remain governed by qualified generated relation records.

Filename similarity, directory proximity, chronology, backlink appearance, or Canvas adjacency do not create semantic authority.

## 12. Snapshot freshness

Every Markdown view must bind itself to a deterministic projection identity.

Required fields:

    view_contract_schema
    projection_tree_digest_sha256
    projection_source_commit
    projection_freshness

Allowed freshness states:

    BOUND
    STALE
    UNKNOWN

The initial P4-B bundle may claim `BOUND` only when the current Vault projection digest exactly equals the preregistered digest.

If that digest changes later, the view may remain readable but MUST NOT claim that it represents the current projection until it is requalified.

## 13. Markdown view metadata

Every initial Markdown view must include:

    view_schema
    view_id
    view_role
    authority_role
    semantic_authority
    projection_tree_digest_sha256
    projection_source_commit
    projection_freshness

Fixed values:

    view_schema = ATDS_OBSIDIAN_VIEW_V0_1
    authority_role = VIEW
    semantic_authority = NONE

The full canonical source body must not be copied into a view.

## 14. Human ownership and seeding

`views/` remains human-owned.

A future P4-B may perform one initial seed only if:

- `views/` is still empty;
- the projection digest is exact;
- the seed bundle is explicitly versioned;
- the seed writes only the seven preregistered paths;
- every target is created exclusively;
- no existing view is overwritten;
- `generated/` remains byte-identical;
- `.obsidian/` remains unchanged;
- repository state remains unchanged.

After initial seeding, automated overwrite is forbidden unless a later migration contract explicitly authorizes it.

## 15. Dashboard evidence rule

Dashboard facts must be supported by the bound generated projection or its qualified manifests.

Counts must be recomputable.

UNKNOWN must not disappear because it is inconvenient.

PASS must preserve its scope.

Execution success must not be rewritten as governed PASS.

CANONICAL must not be rewritten as QUALIFIED.

A dashboard may not add claims of causality, profitability, predictability, deployability, or operational authorization that are absent from the qualified source state.

## 16. P4-A forbidden actions

P4-A itself may not:

- write the Vault;
- create any of the seven view files;
- modify `generated/`;
- modify `.obsidian/`;
- modify P2;
- install a plugin;
- enable Sync;
- enable Git automation;
- introduce a network dependency.

## 17. P4-B candidate boundary

If P4-A passes its persisted re-break, the next candidate gate is:

    P4B_NATIVE_VIEW_BUNDLE_IMPLEMENTATION_CANDIDATE

P4-B may:

- read the bound deterministic projection;
- read build/integrity manifests;
- build and validate an initial native view bundle;
- write only `views/`;
- write only while `views/` is empty.

P4-B may not:

- modify `generated/`;
- modify `.obsidian/`;
- enable plugins or Sync;
- overwrite a human view;
- treat views as semantic input;
- alter canonical repository truth through the Vault.

## 18. Acceptance breakers

P4-A is broken if any implementation or test permits:

1. a view to become canonical truth;
2. a view to become qualification authority;
3. `views/` to become semantic input;
4. P2 to write `views/`;
5. generated bytes to change while creating views;
6. Obsidian configuration to change;
7. a community plugin to be required;
8. Obsidian Sync to be required or enabled;
9. Dataview to be required;
10. custom JavaScript or CSS;
11. a wikilink to become a semantic relation;
12. an unsupported Canvas edge to become a semantic relation;
13. qualification and scientific status to collapse;
14. UNKNOWN to be silently removed;
15. PASS scope to be erased;
16. a stale view to claim current;
17. projection digest binding to be absent;
18. unsupported claims to appear in a dashboard;
19. an existing human view to be overwritten;
20. more than seven initial view files;
21. an external network dependency.

## 19. P4-A success meaning

A P4-A PASS means only:

> the architecture and safety rules for a native, non-authoritative, snapshot-bound human navigation layer have been preregistered and survived their contract breakers.

It does not mean that any view exists in the real Vault.

It does not authorize P4-B unless the persisted P4-A contract and tests pass their local re-break.
