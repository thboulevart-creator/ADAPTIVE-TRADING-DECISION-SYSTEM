# OBSIDIAN P4-A — HUMAN NAVIGATION / VIEW LAYER PREFLIGHT

Date: 2026-09-26

## 1. Purpose

This preflight records the candidate contract boundary for the first useful human-facing Obsidian navigation layer after qualified P3-D2 first-open closure.

P4-A is intentionally contract-and-breakers only.

No Vault write is authorized by this phase.

## 2. Exact predecessor

P3-D2 qualified first-open closure:

    4660a3e5daa57f38175d403b1a1fecef257796af

The P4-A branch was created directly from that closure.

## 3. Candidate branch

    feat/obsidian-projection-p4a-human-navigation-contract-v0.1

## 4. Persisted candidate artifacts

Contract:

    tools/obsidian_projection/human_navigation_contract_v0_1.json
    blob: 699cbaf60141d8ecbb4f7f1afad214b6dd51f92b

Documentation:

    docs/OBSIDIAN-P4A-HUMAN-NAVIGATION-VIEW-LAYER-CONTRACT-V0.1.md
    blob: 493d16eadfc31436808cbd2c38851698b9723d89

Contract breakers:

    tests/obsidian_projection/test_human_navigation_contract_v0_1.py
    blob: d61ba1f9c41056588492b5c41d99d77908df2ae3

## 5. Fixed P4-A architecture

The candidate establishes:

- GitHub/ATDS remains canonical;
- `generated/` remains machine-owned and derived;
- `views/` is human-owned, non-authoritative, and forbidden as semantic input;
- P2 remains unchanged and cannot write `views/`;
- initial view layer uses native Markdown and Obsidian Canvas only;
- Dataview, Excalidraw, Tasks, custom JS/CSS, external network dependencies, community plugins, Obsidian Sync, and Vault Git automation remain outside this phase;
- wikilinks/backlinks are navigation only;
- Canvas edges are navigation only unless explicitly backed by a qualified generated relation;
- qualification/scientific/authority/epistemic/temporal/persistence axes remain separate;
- every initial Markdown view is snapshot-bound to a projection digest and source commit;
- stale views may remain readable but cannot claim current;
- the initial useful layer is deliberately capped at seven files.

## 6. Initial information architecture

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

## 7. Projection binding

The initial candidate remains bound to:

    generated_file_count = 92

    projection_tree_digest_sha256 =
    bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0

Any later P4-B seed must reverify this identity before writing `views/`.

## 8. Human ownership rule

P4-B, if later authorized, may perform only the first seed into an empty `views/`.

It may not overwrite existing human views.

After seeding, automated overwrite remains forbidden unless a later explicit migration contract authorizes it.

## 9. P4-A non-authorizations

P4-A does not authorize:

- writing any Vault file;
- creating the seven view files;
- changing generated projection bytes;
- changing Obsidian configuration;
- changing P2;
- installing or enabling plugins;
- enabling Sync;
- enabling Git automation;
- introducing an external network dependency.

## 10. Breaker intent

The persisted breaker suite must reject architectures that permit:

- authority inversion;
- semantic use of views;
- generated mutation;
- plugin or Sync dependency;
- wikilink/canvas graph inflation;
- epistemic-axis collapse;
- hidden UNKNOWN;
- erased PASS scope;
- stale-as-current presentation;
- unsupported dashboard claims;
- human-view overwrite;
- initial-scope inflation.

## 11. Required local re-break

Before P4-B implementation is authorized, the persisted candidate must be recovered from its persisted HEAD and execute:

1. `py_compile` of the P4-A breaker module;
2. targeted execution of `test_human_navigation_contract_v0_1.py`;
3. the full `tests/obsidian_projection/test_*.py` suite;
4. repository state preservation check.

No P4-B write may occur before that re-break passes.

## 12. Next gate

If and only if the persisted P4-A re-break passes:

    P4B_NATIVE_VIEW_BUNDLE_IMPLEMENTATION_CANDIDATE

P4-B will be a separate movement.

## 13. Current verdict

**P4-A CANDIDATE PERSISTED — LOCAL RE-BREAK REQUIRED**

No P4-A PASS is claimed by this preflight alone.
