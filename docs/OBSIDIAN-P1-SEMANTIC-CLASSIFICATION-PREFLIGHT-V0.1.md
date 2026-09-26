# OBSIDIAN P1 — SEMANTIC CLASSIFICATION PREFLIGHT V0.1

Status: **CANDIDATE PREREGISTRATION ONLY**  
Source repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Frozen source commit: `7bd8c1312430dfc3def5523eb65397a5d6a5ae05`  
Frozen source tree: `66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b`  
Pilot corpus: **74 exact Git blobs**

## 1. Purpose

Pre-register the classification rules that P1 may later implement.

This step does **not** implement the classifier, renderer, relations, Obsidian Vault, Canvas, Bases, plugins or sync.

The objective is to prevent accidental semantic promotion from weak signals such as filenames, directory names, headings, self-reported status strings, test output, workflow success or recency.

## 2. Foundational rule

The classifier must prefer **UNKNOWN** to an unsupported semantic assertion.

A filename such as:

```text
...PASS...
...ADJUDICATION...
...BLOCKED...
...BACKUP...
```

does not by itself establish:

```text
qualification_status
procedure_role
semantic_role
temporal_role
authority
```

Path/name may be used only for exact frozen-inventory lookup, physical artifact-family classification, and candidate-parser selection.

## 3. Authority and persistence

For the frozen 74-source corpus:

```text
exact inventory membership
+ exact Git blob match
+ exact frozen tree membership
→ authority_role = CANONICAL
→ persistence_state = TRACKED_IN_GIT_TREE
```

This does not imply PASS, normativity, currentness or scientific support.

## 4. Qualification status

Default:

```text
qualification_status = UNKNOWN
```

Generic PASS/FAIL/BLOCKED extraction requires all of:

1. a procedure role capable of carrying a bounded verdict:
   - ADJUDICATION;
   - PREFLIGHT;
   - ADVERSARIAL_REVIEW;
2. an explicit terminal verdict block in the source body;
3. a qualification scope extracted or preregistered from that same source.

The following are explicitly insufficient:

- filename/path token;
- document title alone;
- PASS mentioned elsewhere in prose;
- machine `status` alone;
- successful test;
- killed mutant;
- workflow success;
- a profile's self-reported PASS;
- a handoff reporting another artifact's PASS.

## 5. Bounded BLOCKED exceptions

Two AP5 historical attempts do not contain a normal terminal Verdict section, but their exact content records a bounded BLOCKED attempt.

They may be represented only through exact source-path + exact blob-SHA overrides:

- AP5 R1 local AP4-binding attempt;
- AP5 R2 repeated local AP4-binding attempt.

This exception must never become a generic rule such as "BLOCKED in filename → BLOCKED".

## 6. Execution and test status separation

Examples from the frozen corpus:

- `AP6_COMPLETE_VERIFIED` in the AP6 seal is not governed PASS.
- `KILLED` in AP4 mutation results is not governed PASS.
- `python -m py_compile: PASS` inside an adjudication is execution evidence, not the adjudication verdict.
- `CORE_COMPLETE / PASS` inside the CORE profile does not self-qualify the profile record.

Qualification remains carried by the bounded decision/adjudication record.

## 7. Scientific status separation

```text
PASS ≠ SUPPORTED
FAIL ≠ REFUTED
BLOCKED ≠ NOT_INTERPRETABLE
```

`scientific_status` may be set only from explicit scientific-decision content.

No qualification status may be translated automatically onto the scientific axis.

## 8. Temporal role

Default:

```text
temporal_role = UNKNOWN
```

`HISTORICAL` requires both:

- frozen inventory class `HISTORICAL_LINEAGE`;
- session/attempt content supporting historical interpretation.

P1 has **no automatic CURRENT rule**.

Latest date, highest version, latest commit, filename and backlink count are all insufficient.

## 9. Limitations and non-claims

Limitations may be extracted only from:

- a dedicated Limitations/Limites section;
- an exact structured limitation field;
- an exact blob override.

Non-claims may be extracted only from:

- a dedicated Non-promotions section;
- an explicit negative list inside a clearly delimited Scope section;
- terminal-verdict boundary text;
- an exact blob override.

Generic scraping of negation words is forbidden.

## 10. Exact adversarial fixtures

The machine-readable registry freezes representative fixtures including:

- governance source;
- candidate protocol;
- preflight PASS;
- adversarial-review PASS;
- AP4/AP5/AP6/CORE adjudications;
- AP5 R1/R2 BLOCKED historical attempts;
- CORE profile with self-reported PASS but projected qualification UNKNOWN;
- mutation results with KILLED but qualification UNKNOWN;
- AP6 seal with AP6_COMPLETE_VERIFIED but qualification UNKNOWN;
- historical PASS handoff with qualification UNKNOWN;
- test and breaker source code with qualification UNKNOWN.

These fixtures are not a full 74-record classification table. They are adversarial anchors for implementation.

## 11. Forbidden promotions

The following conversions are invalid:

```text
CANONICAL → PASS
MACHINE_STATUS → QUALIFICATION_PASS
TEST_PASS → ARTIFACT_PASS
MUTANT_KILLED → ARTIFACT_PASS
WORKFLOW_SUCCESS → GOVERNED_PASS
PROFILE_SELF_STATUS_PASS → QUALIFICATION_PASS
HANDOFF_REPORTED_PASS → QUALIFICATION_PASS
PASS → SUPPORTED
LATEST → CURRENT
SEAL → RAW_ARTIFACT
WIKILINK → SEMANTIC_RELATION
```

## 12. Implementation gate

After this preregistration is persisted and re-broken, the only allowed next implementation is:

```text
P1 CLASSIFIER IMPLEMENTATION CANDIDATE
```

Still forbidden:

```text
renderer
Markdown note generation
relations generation
Vault creation
.obsidian
Canvas
Bases
plugins
sync
full-repository projection
```

## 13. Candidate verdict

**READY FOR PERSISTED-RULE RE-BREAK ONLY.**

This is not a classifier PASS and does not authorize rendering or Vault creation.
