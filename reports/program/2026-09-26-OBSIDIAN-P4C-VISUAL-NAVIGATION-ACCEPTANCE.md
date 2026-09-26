# OBSIDIAN P4-C — VISUAL / NAVIGATION ACCEPTANCE

Date: 2026-09-26

## Scope

P4-C evaluates the rendered usability of the qualified P4-B native view bundle inside Obsidian.

This phase does not reopen P4-B technical qualification.

Qualified predecessor:

    35c354393d402b677e0088c9bad21c0143647fae

## Visual evidence

Evidence source:

- user-provided screenshot of `views/HOME.md`;
- user-provided screenshot of `views/canvas/ATDS-OVERVIEW.canvas`.

The screenshots show the real Obsidian UI after P4-B materialization.

## Observed PASS points

- the `views/` tree is visible and structurally coherent;
- `HOME.md` opens;
- the native Canvas opens;
- all six Canvas navigation nodes are present;
- the Canvas edges render;
- no plugin failure or missing-file error is visible;
- the central HOME node is visually distinguishable by position;
- the qualified native-only architecture is functioning.

## Observed usability defects

### VC-01 — Properties dominate HOME

The visible Obsidian Properties block occupies most of the first viewport.

Consequences:

- the actual navigation content begins below the primary visual focus;
- raw governance metadata and hashes compete with the human entry point;
- the page reads like a diagnostic record rather than a professional navigation home.

### VC-02 — Canvas cards expose metadata instead of meaning

The file nodes render their Properties blocks prominently.

Consequences:

- node purpose is not immediately readable;
- technical values are truncated;
- the visual graph communicates file metadata before architecture/navigation intent;
- scanning cost is higher than necessary.

### VC-03 — Technical identity is overexposed in primary UX

Projection hashes and contract identifiers are necessary for auditability but should not dominate the primary navigation surface.

They remain required in file metadata and may remain available through the Properties view/sidebar.

## Adjudication

**CORRECTION REQUIRED — VISUAL UX ONLY**

P4-B remains technically qualified.

No change to:

- canonical authority;
- generated projection;
- view semantic authority;
- projection digest;
- P4-A epistemic rules;
- plugin policy;
- Sync policy.

is justified by these screenshots.

## Minimal remediation authorized

Before redesigning any Markdown or Canvas file, apply the smallest native Obsidian UI change:

    Settings
      → Editor
      → Properties in document
      → Hidden

This is an Obsidian display preference only.

It does not remove YAML/frontmatter from the files and therefore preserves the P4-A/P4-B snapshot binding and audit metadata.

No community plugin, CSS snippet, Dataview, Sync, or file rewrite is authorized for this remediation.

## Recheck required

After the display preference is changed:

1. reopen `views/HOME.md`;
2. reopen `views/canvas/ATDS-OVERVIEW.canvas`;
3. capture both views;
4. reassess:
   - first-screen navigation visibility;
   - Canvas node readability;
   - hierarchy;
   - scanability;
   - whether file-node previews remain useful.

Only if the Canvas remains visually weak after Properties are hidden should a P4-C-R1 view-layout revision be implemented.

## Current verdict

**P4-C = CORRECTION REQUIRED, BOUNDED TO UI DISPLAY**

No content rewrite is authorized yet.


## Recheck after Properties hidden

A second user-provided Canvas screenshot was reviewed after applying the native Obsidian display setting that hides Properties in the document.

Observed improvement:

- file-node cards now expose human-facing headings and descriptions instead of governance metadata;
- the central HOME node is immediately identifiable;
- left-side maps and right-side dashboards form a readable visual hierarchy;
- navigation edges are visually understandable;
- no semantic-authority boundary was changed.

Remaining visible UX issues:

1. `SYSTEM-ARCHITECTURE` and `GOVERNANCE` show an Obsidian Mermaid rendering consent/prompt inside their card previews, adding visual noise;
2. Canvas file nodes repeat the note name twice: once as the Canvas/file label and once as the note H1;
3. HOME visual acceptance still requires the post-remediation screenshot requested by P4-C.

Intermediate disposition:

**CANVAS ACCEPTABLE WITH MINOR UX CORRECTIONS — P4-C OVERALL STILL OPEN**

No content rewrite is authorized from this screenshot alone.


## Final HOME recheck

A post-remediation user screenshot of `views/HOME.md` was reviewed with document Properties hidden.

Observed result:

- the human navigation content is visible in the first viewport;
- the page hierarchy is clear: entry title → projection binding → dashboards → maps → visual overview;
- dashboard links are immediately accessible;
- map links are immediately accessible;
- the Canvas entry is visible without navigating through technical metadata;
- the non-authoritative warning remains visible;
- projection identity remains auditable;
- no plugin-dependent rendering is required for HOME;
- no broken link or missing-file condition is visible.

Residual minor UX observations:

1. raw source commit and projection digest remain relatively prominent for a primary navigation page;
2. the editor/live-preview mode may expose Markdown editing affordances such as the heading marker while the cursor is active;
3. Mermaid consent/prompt text may still appear inside some Canvas file previews.

These are non-blocking usability refinements. They do not justify reopening P4-B or altering authority boundaries.

## Final P4-C adjudication

**PASS — VISUAL / NAVIGATION ACCEPTANCE, WITH MINOR NON-BLOCKING UX RESIDUALS**

The qualified P4-B bundle is accepted as usable for its initial objective:

- human entry point is readable;
- navigation hierarchy is understandable;
- native Canvas provides a coherent overview;
- dashboards/maps are discoverable;
- technical metadata remains available without dominating the primary interface;
- no community plugin, Sync, Dataview, custom JavaScript, custom CSS, or external dependency is required.

P4-C does not claim that the current visual layer is the final long-term UX. It qualifies it as a professional and usable V0.1 navigation surface.

## Closure

P4-C is closed PASS.

Any subsequent visual refinement must be a new bounded phase and must not silently overwrite human-owned views.
