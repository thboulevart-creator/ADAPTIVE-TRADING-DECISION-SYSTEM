# OBSIDIAN P5-B — DYNAMIC CURRENT-HEAD INVENTORY + SOURCE SELECTION CONTRACT V0.1

Date: 2026-09-26

## 1. Purpose

P5-B replaces the frozen 74-artifact pilot as the source-universe model for future continuous projection.

It defines how one exact Git commit is enumerated into a deterministic source inventory before semantic classification or projection.

P5-B is not a semantic classifier and does not infer qualification, scientific status, epistemic status, or authority from paths.

## 2. Predecessor and monitored source

Qualified predecessor:

    P5-A HEAD
    343d253074abe603eb61bebab29ba58f0bd9301c

Repository:

    thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Monitored branch:

    integration/system-v1

Reference HEAD observed while designing P5-B:

    6aef3b1304313c3446c08a3a37b51ea61733f41e

Reference tree:

    ac1e61838a72852cad96e003bfb593de567c2b6d

The observed counts in this document are evidence about that HEAD only. They are not future runtime constants.

## 3. Core rule

The inventory authority is the exact Git tree object of the selected source HEAD.

Equivalent enumeration:

    git ls-tree -r -l -z <EXACT_HEAD>

The working tree and Git index are not inventory authority.

The default selection rule is intentionally complete:

> every tracked regular blob is an inventory member unless an explicit safety exclusion blocks the entire HEAD.

This prevents new tracked project areas from disappearing silently from Obsidian.

## 4. Object and mode policy

Accepted objects:

    type = blob
    mode = 100644 or 100755

Blocked:

    symlink mode 120000
    gitlink mode 160000
    undecodable path

A blocked object prevents automatic projection of that HEAD.

## 5. Selection zones

Paths receive a non-semantic selection zone only for navigation and census:

    GOVERNANCE/        → GOVERNANCE
    docs/              → DOCUMENTATION
    evidence/          → EVIDENCE
    reports/           → REPORT
    requirements/      → REQUIREMENT
    src/               → IMPLEMENTATION
    tests/             → TEST
    tools/             → TOOL
    breakers/          → BREAKER
    .github/           → GITHUB_AUTOMATION_OR_CONFIG
    04-REFERENCE/      → REFERENCE
    99-BACKUP/         → HISTORICAL_LINEAGE
    root regular blob  → ROOT_DOCUMENT
    other tracked zone → OTHER_TRACKED

These labels are **selection provenance**, not semantic truth.

For example:

    selection_zone = TEST

does not itself prove:

    semantic_role = TESTED
    qualification_status = PASS
    authority = CANONICAL

Those remain separate governed decisions.

## 6. No silent drop

A tracked regular blob outside known zones is still inventoried as:

    OTHER_TRACKED

It is not silently ignored.

This is essential for continuous synchronization: a newly added project directory must become visible to the inventory immediately even before a richer zone rule exists.

## 7. Forbidden tracked surfaces

The following tracked surfaces block the HEAD rather than being projected:

    generated/
    views/
    .obsidian/
    .git/
    __pycache__/
    .pytest_cache/
    .mypy_cache/
    .venv/
    venv/
    node_modules/
    *.pyc
    *.pyo

Reason:

- derived Vault output must not recursively become source input;
- local Obsidian UI state must not become canonical project knowledge;
- runtime caches must not contaminate deterministic inventory;
- vendored/runtime trees require a separate explicit policy.

## 8. Sensitive paths

Candidate secret-bearing paths are never projected.

Examples include:

    .env
    .env.*
    *.pem
    *.key
    *.p12
    *.pfx
    id_rsa*
    **/secrets/**
    **/credentials/**
    **/*credential*
    **/*private-key*
    **/*private_key*

A match yields:

    BLOCK_HEAD_NO_PROJECTION

The live projection remains last-known-good.

Operational evidence may record only:

    count
    SHA-256(path)

and must not log the sensitive path in plaintext.

## 9. Two content modes

P5-B separates inventory membership from whether source body text may be read semantically.

### FULL_TEXT

A blob may be FULL_TEXT only if:

- size <= 1 MiB;
- extension is in the text allowlist;
- bytes are valid UTF-8;
- there is no NUL byte;
- the pinned secret scanner passes.

Candidate extensions include Markdown, Python, JSON, YAML, TXT, TOML, INI/CFG, CSV/TSV, XML/HTML/CSS, JavaScript/TypeScript, SQL, shell, PowerShell and Windows command scripts.

FULL_TEXT permits downstream semantic reading.

It still does not authorize copying the complete canonical body into the inventory.

### METADATA_ONLY

A blob becomes METADATA_ONLY when, for example:

- size > 1 MiB;
- extension is not in the text allowlist;
- UTF-8 decoding fails;
- a NUL byte is present.

The projection may retain only provenance metadata such as:

- source path;
- blob SHA;
- size;
- Git mode;
- selection zone;
- content mode.

Its body may not be used for semantic classification unless a later specialized parser is independently qualified.

This allows BI5 and large evidence payloads to remain visible as real project artifacts without loading their full payload into the knowledge layer.

## 10. Secret scanning

Every FULL_TEXT candidate must pass a pinned scanner version before semantic classification.

If the scanner is unavailable:

    BLOCK_HEAD

If a high-confidence secret is detected:

    BLOCK_HEAD_NO_PROJECTION

Secret values must never enter:

- the inventory;
- generated notes;
- logs;
- error messages.

A false-positive exception requires explicit governed approval.

## 11. Dynamic inventory record

The dynamic inventory schema is:

    ATDS_OBSIDIAN_DYNAMIC_INVENTORY_V0_1

Top-level identity binds:

- repository;
- branch;
- exact source commit;
- exact source tree;
- selection-contract version;
- blob counts;
- deterministic inventory digest.

Each entry contains exactly:

    source_path
    source_blob_sha
    source_blob_size
    git_mode
    selection_zone
    content_mode

Entries sort by UTF-8 bytewise source path.

No timestamp, hostname, username or absolute local path may contaminate deterministic inventory bytes.

## 12. Exact-head verification

Before acceptance:

- repository identity must match;
- branch must match;
- inventory commit must equal the observed remote HEAD;
- tree OID must equal the commit tree;
- every entry blob OID must match the tree;
- every entry size must match Git;
- FULL_TEXT raw blob length must be verified.

## 13. Delta semantics

Between two qualified inventories:

    new path                → ADDED
    removed path            → REMOVED
    same path / new blob    → MODIFIED
    same path / same blob   → UNCHANGED

Same blob at a new path may be noted as a possible rename only as:

    INFORMATIONAL_ONLY

It is not a semantic relationship.

A removed source can later support an ORPHAN state in the live projection.

An expected derived artifact absent from output can support MISSING.

## 14. Reference census at the design HEAD

At:

    source HEAD
    6aef3b1304313c3446c08a3a37b51ea61733f41e

the Git tree contains:

    908 tracked regular blobs
    100,818,496 bytes total

Under the P5-B V0.1 candidate rules:

    FULL_TEXT       = 890
    METADATA_ONLY   = 18
    symlinks        = 0
    gitlinks        = 0
    sensitive-path matches = 0

Zone census:

    REPORT                         265
    EVIDENCE                       151
    HISTORICAL_LINEAGE             100
    DOCUMENTATION                   88
    GITHUB_AUTOMATION_OR_CONFIG     84
    BREAKER                         53
    IMPLEMENTATION                  46
    TEST                            42
    TOOL                            42
    GOVERNANCE                      16
    REFERENCE                       16
    ROOT_DOCUMENT                    4
    REQUIREMENT                      1

The largest blob observed is:

    evidence/bfiq02/interval_inventory_v0_1.json
    22,826,236 bytes

It is therefore METADATA_ONLY.

The 908 / 890 / 18 counts are not hard-coded runtime requirements.

## 15. Relationship to the frozen pilot

The existing 74-artifact pilot remains historical qualification evidence for P0–P4.

P5-B does not mutate or reinterpret it.

Continuous mode may not reuse it as the current source universe.

The future dynamic inventory implementation must construct a new inventory independently for every exact monitored HEAD.

## 16. P5-B non-authorizations

P5-B does not yet authorize:

- runtime continuous inventory building;
- the P5 observer;
- Vault writes;
- projection rebuild;
- semantic-classifier changes;
- mutation of the frozen pilot inventory.

## 17. Required implementation step after contract qualification

After P5-B contract re-break PASS, the next bounded step is:

    P5-B2
    DYNAMIC INVENTORY IMPLEMENTATION CANDIDATE

P5-B2 must prove the contract against synthetic mutants and the current real HEAD before P5-C atomic-promotion work proceeds.

## 18. Success meaning

P5-B PASS means only:

> the rules determining which exact Git blobs enter continuous inventory, how content modes are assigned, how sensitive/runtime artifacts are blocked, and how deterministic provenance is recorded have been preregistered and survived their breakers.

It does not mean the dynamic inventory implementation is running.
