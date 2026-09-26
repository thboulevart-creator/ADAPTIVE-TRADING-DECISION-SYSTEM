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
